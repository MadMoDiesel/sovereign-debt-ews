#!/usr/bin/env bash
# Build Erickson_2026_debt_ews.pdf from PAPER.md.
#   PAPER.md --pandoc--> paper.html (self-contained, paper.css inlined)
#   paper.html --headless Chromium--> PDF, no browser header/footer.
# Usage: ./build_paper.sh            (uses `chromium`, `google-chrome`, or $CHROME)
set -euo pipefail
cd "$(dirname "$0")"

OUT=Erickson_2026_debt_ews.pdf
CHROME="${CHROME:-$(command -v chromium || command -v chromium-browser || command -v google-chrome || command -v google-chrome-stable || true)}"
[ -n "$CHROME" ] || { echo "No Chromium/Chrome binary found; set CHROME=/path/to/chrome" >&2; exit 1; }

pandoc PAPER.md \
  --standalone --embed-resources \
  --from markdown+pipe_tables+smart \
  --css paper.css \
  --metadata pagetitle="Can Sovereign Debt Early-Warning Dashboards Be Validated?" \
  --metadata lang=en \
  -o paper.html

"$CHROME" --headless=new --no-sandbox --disable-gpu \
  --no-pdf-header-footer \
  --run-all-compositor-stages-before-draw --virtual-time-budget=10000 \
  --print-to-pdf="$OUT" "file://$PWD/paper.html" 2>/dev/null

echo "wrote $OUT"
# Sanity checks (need poppler-utils): no Type 3 fonts, page count.
if command -v pdffonts >/dev/null; then
  if pdffonts "$OUT" | grep -q "Type 3"; then echo "WARNING: Type 3 font present (arXiv rejects these)" >&2; fi
  pdfinfo "$OUT" | grep -E "^Pages"
fi
