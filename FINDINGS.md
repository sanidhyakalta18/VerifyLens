# VerifyLens benchmark findings

96 real OCR runs on 48 fictional documents, two preprocessing configurations. This small controlled dataset does not estimate real-world KYC performance.

[
  {
    "mode": "raw",
    "requests": 48,
    "field_accuracy_pct": 66.7,
    "average_ms": 1137.7
  },
  {
    "mode": "threshold",
    "requests": 48,
    "field_accuracy_pct": 66.7,
    "average_ms": 1379.8
  }
]

Both configurations extracted all labelled fields from clean and low-contrast samples. Both failed to recover fields on the deliberately blurred samples. Missing-ID samples recovered two of three expected fields and were flagged as incomplete. API execution succeeded despite these extraction failures.

Recommendation: use a document-quality check and recapture flow for unreadable images; expose missing-field reasons to users. Threshold preprocessing did not improve field accuracy on this dataset, so additional processing should be justified on a broader varied dataset before adoption. Compare other OCR engines and layouts next.

Latency is measured locally and depends on environment; no external provider or Bureau service was benchmarked.
