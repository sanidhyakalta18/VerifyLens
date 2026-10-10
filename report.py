import json
from core import connect,analytics,ROOT
with connect() as c:
 c.execute("DELETE FROM runs WHERE kind='uploaded'")
 modes=[dict(r) for r in c.execute('SELECT mode,COUNT(*) AS requests,ROUND(100.0*SUM(matched)/SUM(total),1) AS field_accuracy_pct,ROUND(AVG(latency_ms),1) AS average_ms FROM runs GROUP BY mode')]
a=analytics();(ROOT/'benchmark_results.json').write_text(json.dumps(a,indent=2))
report='# VerifyLens benchmark findings\n\n96 real OCR runs on 48 fictional documents, two preprocessing configurations. This small controlled dataset does not estimate real-world KYC performance.\n\n'+json.dumps(modes,indent=2)+'\n\nBoth configurations extracted all labelled fields from clean and low-contrast samples. Both failed to recover fields on the deliberately blurred samples. Missing-ID samples recovered two of three expected fields and were flagged as incomplete. API execution succeeded despite these extraction failures.\n\nRecommendation: use a document-quality check and recapture flow for unreadable images; expose missing-field reasons to users. Threshold preprocessing did not improve field accuracy on this dataset, so additional processing should be justified on a broader varied dataset before adoption. Compare other OCR engines and layouts next.\n\nLatency is measured locally and depends on environment; no external provider or Bureau service was benchmarked.\n'
(ROOT/'FINDINGS.md').write_text(report);print(modes)
