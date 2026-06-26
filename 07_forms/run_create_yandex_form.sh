#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPS_DIR="$SCRIPT_DIR/.deps"

if [[ ! -d "$DEPS_DIR" ]]; then
  echo "Dependencies are not installed. Run: python3 -m pip install --target \"$DEPS_DIR\" -r \"$SCRIPT_DIR/requirements.txt\"" >&2
  exit 1
fi

export PYTHONPATH="$DEPS_DIR${PYTHONPATH:+:$PYTHONPATH}"
exec python3 "$SCRIPT_DIR/create_yandex_form.py" "$@"
