#!/usr/bin/env bash
set -euo pipefail

project_root="${1:-}"
raw_dir="${2:-}"
output_dir="${3:-}"
config_file="${4:-semantic_project.yml}"
pandoc="/mnt/c/Program Files/Pandoc/pandoc.exe"

if [[ -z "$project_root" ]]; then
  echo "Usage: $0 <project_root> [raw_dir] [output_dir]" >&2
  exit 1
fi

cd "$project_root"

config_value() {
  local key="$1"
  if [[ ! -f "$config_file" ]]; then
    return 1
  fi
  awk -F ':' -v key="$key" '$1 == key { sub(/^[[:space:]]+/, "", $2); sub(/[[:space:]]+$/, "", $2); gsub(/^["'\'']|["'\'']$/, "", $2); print $2; exit }' "$config_file"
}

raw_dir="${raw_dir:-$(config_value raw_sources || true)}"
output_dir="${output_dir:-$(config_value extracted_texts || true)}"

if [[ -z "$raw_dir" || -z "$output_dir" ]]; then
  echo "Raw/output directories were not provided and config values are missing in: $config_file" >&2
  exit 1
fi

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
