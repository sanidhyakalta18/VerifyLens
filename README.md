# VerifyLens
Local document OCR evaluation and API analytics demo for a risk-platform analyst portfolio.

## Quick start on macOS
```bash
brew install tesseract
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 generate.py
python3 benchmark.py --reset
python3 app.py
```
Open http://127.0.0.1:8000. Select a PNG from `samples` to run real OCR.
Tests: `python3 -m unittest test_core.py`.

## Scope
48 generated fictional membership, employee and student cards, with clean, blurred, low-contrast and missing-field conditions. Ground truth records in manifest.json retain all three expected fields, including intentionally absent fields. Two preprocessing configurations of the same Tesseract engine are compared; this is not a comparison of two providers. No model training, external KYC service, fraud detection, or authenticity verification is implemented.

## Metrics
API success measures successful OCR execution. Field completion measures presence of three required fields and a date-format check. Field accuracy measures exact case-insensitive matches against labelled expected values; uploads without labels are excluded from its denominator. p95 uses nearest rank on observed processing latency. Latencies are environment-dependent OCR processing measurements, not network round-trip benchmarks. Dashboard refreshes on load and after uploads.

SQL queries in core.py calculate segmented performance and failure reasons. benchmark_results.json is a reproducible local experiment snapshot; repeated benchmark runs accumulate unless --reset is used. The dashboard database also contains subsequent uploaded documents. HTTP errors are separate from extraction mismatches.

## API
GET /health; GET /api/analytics; POST /api/verify?mode=raw or threshold with a PNG/JPEG body (5 MB maximum).
```bash
curl --data-binary @samples/membership_0_clean.png 'http://127.0.0.1:8000/api/verify?mode=raw'
```
Only PNG/JPEG are the intended demo inputs; no PDF extraction is provided. Local HTTPServer is deliberately bound to loopback and is unsuitable for production or public hosting. No authentication or rate limiting. Do not upload real identity documents. Extracted fields are stored locally; raw uploaded files are not retained. Delete results.sqlite to remove local logs.

## Attribution
Application code was created for this project; no code from the previously considered fastapi-ocr repository was copied. OCR is supplied by Tesseract (Apache 2.0): https://github.com/tesseract-ocr/tesseract. Image operations use Pillow: https://github.com/python-pillow/Pillow. Install dependencies separately and retain their licenses when redistributing them.
