#!/usr/bin/env bash
set -euo pipefail

project_root="${1:-}"
raw_dir="${2:-00_input/documents/electricians_knowledge_base/raw}"
output_dir="${3:-00_input/documents/electricians_knowledge_base/extracted}"
pandoc="/mnt/c/Program Files/Pandoc/pandoc.exe"

if [[ -z "$project_root" ]]; then
  echo "Usage: $0 <project_root> [raw_dir] [output_dir]" >&2
  exit 1
fi

cd "$project_root"

if [[ ! -d "$raw_dir" ]]; then
  echo "Raw directory not found: $raw_dir" >&2
  exit 1
fi

mkdir -p "$output_dir"

extract_docx() {
  local input_file="$1"
  local base_name output_file
  base_name="$(basename "${input_file%.*}")"
  output_file="$output_dir/${base_name}.md"

  "$pandoc" \
    "$(wslpath -w "$input_file")" \
    --from docx \
    --to gfm \
    --wrap=none \
    --output "$(wslpath -w "$output_file")"
}

extract_pdf() {
  local input_file="$1"
  local base_name output_file
  base_name="$(basename "${input_file%.*}")"
  output_file="$output_dir/${base_name}.txt"

  gs -q -dNOPAUSE -dBATCH \
    -sDEVICE=txtwrite \
    -sOutputFile="$output_file" \
    "$input_file"
}

if [[ ! -x "$pandoc" ]]; then
  echo "Pandoc was not found at: $pandoc" >&2
  exit 1
fi

shopt -s nullglob
for input_file in "$raw_dir"/*; do
  case "${input_file##*.}" in
    docx|DOCX)
      extract_docx "$input_file"
      ;;
    pdf|PDF)
      extract_pdf "$input_file"
      ;;
  esac
done
