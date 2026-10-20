#!/usr/bin/env bash
# Cold run: clone the repository into a fresh folder, build a fresh environment, follow the README, time it.
# Usage: bash scripts/cold_run.sh [git-url-or-path] [target-dir]
set -u
SRC="${1:-$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)}"
DST="${2:-$(mktemp -d)/nvda-cold-run}"
START=$(date +%s)
echo "== cold run started $(date -Iseconds 2>/dev/null || date)"; echo "source: $SRC"; echo "target: $DST"
git clone -q "$SRC" "$DST" || { echo "FIRST FAILURE: git clone"; exit 1; }
cd "$DST" || exit 1
echo "commit: $(git rev-parse --short HEAD)"
python3 -m venv .venv || { echo "FIRST FAILURE: venv"; exit 1; }
# shellcheck disable=SC1091
source .venv/bin/activate
pip install -q -r requirements.txt || { echo "FIRST FAILURE: pip install"; exit 1; }
python -m pytest -q || { echo "FIRST FAILURE: pytest"; exit 1; }
python analysis.py || { echo "FIRST FAILURE: analysis.py"; exit 1; }
python analysis.py --break
echo "== visible output ready after $(( $(date +%s) - START )) s"
streamlit run app.py --server.headless true --server.port 8799 > streamlit.log 2>&1 &
APP=$!
for i in $(seq 1 30); do sleep 1; if curl -s -o /dev/null -w '%{http_code}' http://localhost:8799/ | grep -q 200; then echo "app answered HTTP 200 after $i s"; break; fi; done
kill $APP 2>/dev/null
echo "== cold run finished after $(( $(date +%s) - START )) s"
