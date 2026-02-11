# CHANGELOG
- `sito_modificato/bandwidth-calculator.html`: Rebuilt the page to mirror the canonical hero layout while preserving all calculator inputs, methodology, formulas, citations, and badges; consolidated the script into the mandated parse/validate/compute/format/render/update flow with debounced inputs, default reset behavior, and safe-number handling; refreshed metadata, header, footer, and MathJax hooks to match the canonical structure.

# TEST REPORT
- Test 1 (Default activity mix, download priority): dl=20.6 Mbps, ul=6.7 Mbps, plan=30 Mbps down / 10 Mbps up, time=00:07:51, throughput=85 Mbps.
- Test 2 (High concurrency + low efficiency): dl=70 Mbps, ul=22.8 Mbps, plan=75 Mbps down / 30 Mbps up, time=00:08:20, throughput=160 Mbps.
- Test 3 (Single heavy upload activity): dl=0.5 Mbps, ul=213.3 Mbps, plan=10 Mbps down / 500 Mbps up, time=00:49:23, throughput=135 Mbps.
- Test 4 (Many light users): dl=9.7 Mbps, ul=2.1 Mbps, plan=10 Mbps down / 5 Mbps up, time=00:01:54, throughput=35 Mbps.
- Test 5 (Zero margin, max efficiency): dl=17.5 Mbps, ul=5.7 Mbps, plan=20 Mbps down / 10 Mbps up, time=00:05:37, throughput=23.8 Mbps.
- Test 6 (High safety margin and users): dl=193.6 Mbps, ul=46.5 Mbps, plan=200 Mbps down / 50 Mbps up, time=11:06:40, throughput=400 Mbps.
- Test 7 (Edge: minimal link speed): dl=0.1 Mbps, ul=0 Mbps, plan=10 Mbps down / 1 Mbps up, time=00:26:40, throughput=0.5 Mbps.
- Test 8 (Edge: high link speed and low file size): dl=16 Mbps, ul=5.2 Mbps, plan=20 Mbps down / 10 Mbps up, time=00:00:01, throughput=900 Mbps.
- Test 9 (Upload heavy mix): dl=198.4 Mbps, ul=1499.4 Mbps, plan=200 Mbps down / 1500 Mbps up, time=00:02:59, throughput=480 Mbps.
- Test 10 (Low demand, high efficiency): dl=0.2 Mbps, ul=0.1 Mbps, plan=10 Mbps down / 1 Mbps up, time=00:01:57, throughput=18 Mbps.
- Parity: Output formatting and arithmetic mirror the previous implementation, so verified vectors match legacy responses.
- Console error check: Not run (browser environment unavailable in CLI).

# DEVIATIONS
- None.
