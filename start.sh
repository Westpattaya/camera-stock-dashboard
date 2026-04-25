#!/bin/bash
cd "$(dirname "$0")"
SRC="/Users/fordudjw/Downloads/Update log.csv"
if [ -f "$SRC" ]; then
  cp "$SRC" "./Update log.csv"
  echo "✓ Orders CSV copied from Downloads"
else
  echo "⚠ Orders CSV not found at: $SRC"
fi
RS_SRC="/Users/fordudjw/Downloads/restock_log.csv"
if [ -f "$RS_SRC" ]; then
  cp "$RS_SRC" "./restock_log.csv"
  echo "✓ Restock log copied from Downloads"
fi
echo "Dashboard → http://localhost:8080/camera_dashboard_v3.html"
echo "Press Ctrl+C to stop."
open "http://localhost:8080/camera_dashboard_v3.html"
python3 -m http.server 8080
