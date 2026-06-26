#!/usr/bin/env bash
set -euo pipefail

input_file="${1:-}"
output_format="${2:-docx}"
pandoc="/mnt/c/Program Files/Pandoc/pandoc.exe"
mmdc="${MMDC_BIN:-mmdc}"
mermaid_max_width_in="${MERMAID_MAX_WIDTH_IN:-6.5}"
mermaid_max_height_in="${MERMAID_MAX_HEIGHT_IN:-7.2}"

if [[ -z "$input_file" ]]; then
  echo "Open a Markdown file before running Ctrl+Shift+B." >&2
  exit 1
fi

if [[ ! -f "$input_file" ]]; then
  echo "File not found: $input_file" >&2
  exit 1
fi

if [[ "${input_file##*.}" != "md" ]]; then
  echo "Current file is not Markdown: $input_file" >&2
  exit 1
fi

if [[ ! -x "$pandoc" ]]; then
  echo "Windows Pandoc was not found at: $pandoc" >&2
  exit 1
fi

input_file="$(realpath "$input_file")"
base_path="${input_file%.*}"
work_dir="$(mktemp -d)"
processed_file="${work_dir}/input.md"
mermaid_dir="${work_dir}/mermaid"
mkdir -p "$mermaid_dir"
trap 'rm -rf "$work_dir"' EXIT

python3 - "$input_file" "$processed_file" "$mermaid_dir" "$mmdc" "$mermaid_max_width_in" "$mermaid_max_height_in" <<'PY'
import os
import re
import struct
import subprocess
import sys
from pathlib import Path

input_path = Path(sys.argv[1])
output_path = Path(sys.argv[2])
mermaid_dir = Path(sys.argv[3])
mmdc = sys.argv[4]
max_width_in = float(sys.argv[5])
max_height_in = float(sys.argv[6])


def png_dimensions(path):
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) < 24 or header[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError(f"Mermaid output is not a valid PNG: {path}")
    return struct.unpack(">II", header[16:24])


def image_size_attr(path):
    width_px, height_px = png_dimensions(path)
    if width_px <= 0 or height_px <= 0:
        return f"{{width={max_width_in}in}}"

    height_if_max_width = max_width_in * height_px / width_px
    if height_if_max_width <= max_height_in:
        return f"{{width={max_width_in}in}}"
    return f"{{height={max_height_in}in}}"

text = input_path.read_text(encoding="utf-8")
pattern = re.compile(r"```mermaid\s*\n(.*?)\n```", re.DOTALL)
matches = list(pattern.finditer(text))

if not matches:
    output_path.write_text(text, encoding="utf-8")
    sys.exit(0)

parts = []
last = 0

for index, match in enumerate(matches, start=1):
    diagram_source = match.group(1).strip() + "\n"
    stem = f"mermaid_{index:02d}"
    source_path = mermaid_dir / f"{stem}.mmd"
    image_path = mermaid_dir / f"{stem}.png"

    source_path.write_text(diagram_source, encoding="utf-8")
    subprocess.run(
        [
            mmdc,
            "-i",
            str(source_path),
            "-o",
            str(image_path),
            "-b",
            "transparent",
            "-s",
            "2",
        ],
        check=True,
    )

    image_rel = os.path.relpath(image_path, output_path.parent)
    image_attr = image_size_attr(image_path)
    parts.append(text[last:match.start()])
    parts.append(f"![Mermaid diagram {index}]({image_rel}){image_attr}\n")
    last = match.end()

parts.append(text[last:])
output_path.write_text("".join(parts), encoding="utf-8")
PY

case "$output_format" in
  docx)
    output_file="${base_path}.docx"
    "$pandoc" "$(wslpath -w "$processed_file")" \
      --standalone \
      --from markdown+smart+link_attributes \
      --to docx \
      --resource-path "$(wslpath -w "$work_dir")" \
      --output "$(wslpath -w "$output_file")"
    ;;
  pdf)
    output_file="${base_path}.pdf"
    temp_html="${base_path}.tmp.html"
    pdf_processed_file="${work_dir}/input_pdf.md"
    trap 'rm -rf "$work_dir"; rm -f "$temp_html"' EXIT

    cat > "$pdf_processed_file" <<'CSS'
<style>
img {
  max-width: 100%;
  break-inside: avoid;
  page-break-inside: avoid;
}
</style>

CSS
    cat "$processed_file" >> "$pdf_processed_file"

    "$pandoc" "$(wslpath -w "$pdf_processed_file")" \
      --standalone \
      --embed-resources \
      --from markdown+smart+link_attributes \
      --to html5 \
      --resource-path "$(wslpath -w "$work_dir")" \
      --metadata "title=$(basename "$base_path")" \
      --output "$(wslpath -w "$temp_html")"

    powershell.exe -NoProfile -ExecutionPolicy Bypass \
      -File "$(wslpath -w "${PWD}/06_scripts/export_html_to_pdf.ps1")" \
      "$(wslpath -w "$temp_html")" \
      "$(wslpath -w "$output_file")"

    rm -f "$temp_html"
    trap 'rm -rf "$work_dir"' EXIT
    ;;
  *)
    echo "Unsupported output format: $output_format" >&2
    echo "Use docx or pdf." >&2
    exit 1
    ;;
esac

echo "Created: $output_file"
