#!/usr/bin/env bash
set -euo pipefail

input_file="${1:-}"
output_format="${2:-docx}"
pandoc="/mnt/c/Program Files/Pandoc/pandoc.exe"

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

case "$output_format" in
  docx)
    output_file="${base_path}.docx"
    "$pandoc" "$(wslpath -w "$input_file")" \
      --standalone \
      --from markdown+smart \
      --to docx \
      --output "$(wslpath -w "$output_file")"
    ;;
  pdf)
    output_file="${base_path}.pdf"
    temp_html="${base_path}.tmp.html"
    trap 'rm -f "$temp_html"' EXIT

    "$pandoc" "$(wslpath -w "$input_file")" \
      --standalone \
      --from markdown+smart \
      --to html5 \
      --metadata "title=$(basename "$base_path")" \
      --output "$(wslpath -w "$temp_html")"

    powershell.exe -NoProfile -ExecutionPolicy Bypass \
      -File "$(wslpath -w "${PWD}/07_scripts/export_html_to_pdf.ps1")" \
      "$(wslpath -w "$temp_html")" \
      "$(wslpath -w "$output_file")"

    rm -f "$temp_html"
    trap - EXIT
    ;;
  *)
    echo "Unsupported output format: $output_format" >&2
    echo "Use docx or pdf." >&2
    exit 1
    ;;
esac

echo "Created: $output_file"
