#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
COLLECTION_DIR="${1:-$SCRIPT_DIR/templates/bruno}"
ENV_NAME="${2:-staging}"
REPORT_DIR="$SCRIPT_DIR/../reports"
mkdir -p "$REPORT_DIR"

if ! command -v bru >/dev/null 2>&1; then
  echo "bru command not found. Please install Bruno CLI first."
  echo "npm i -g @usebruno/cli"
  exit 1
fi

TS="$(date +%Y%m%d-%H%M%S)"
REPORT_JSON="$REPORT_DIR/bru-report-${TS}.json"

echo "Running Bruno collection: $COLLECTION_DIR (env=$ENV_NAME)"

# Report validation is verified with Bruno CLI 4.2.1; unsupported formats fail explicitly.
(cd "$COLLECTION_DIR" && bru run --env "$ENV_NAME" --reporter-json "$REPORT_JSON")
python3 "$SCRIPT_DIR/check_bruno_report.py" "$REPORT_JSON"

echo "Report generated: $REPORT_JSON"
