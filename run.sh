#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python -m pip install -r requirements-dev.txt --break-system-packages -q
if [ $# -eq 0 ]; then
  python -m pytest -q
else
  python -m veritiscan "$@"
fi