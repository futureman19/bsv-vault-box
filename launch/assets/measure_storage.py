"""Measured byte scenarios; proposals only, no storage service calls."""
import json
import math
from collections import defaultdict
from pathlib import Path
ROOT = Path(__file__).resolve().parent
m = json.loads((ROOT / 'candidate-manifest.json').read_bytes())
a = json.loads((ROOT / 'acceptance-report.json').read_bytes())
roles = defaultdict(int)
for item in m['items']:
    for f in item['files']: roles[f['role']] += f['bytes']
size = a['archive']['bytes']
result = {'bytes_by_role': dict(roles), 'zip_bytes': size, 'zip_decimal_GB': size / 10**9,
          'R2_standard_single_zip_full_month': {
              'storage_only_USD_before_free_tier_rounded': math.ceil(size / 10**9) * .015,
              'storage_only_USD_if_10GB_free_tier_entirely_available': 0,
              'class_A_USD_per_million_rounded': 4.50, 'class_B_USD_per_million_rounded': .36,
              'internet_egress_USD': 0,
              'assumptions': 'One unchanged copy for full month; decimal GB conservative; account usage, operations, taxes and other services separate. Account entitlements not inspected.'},
          'source': 'https://developers.cloudflare.com/r2/pricing/index.md',
          'retrieval': 'Official pricing indexed search extract. Direct HTML fetch HTTP403; web_extract backend unavailable. No full-page capture claimed.',
          'purchase_or_upload': False,
          'options': ['Two offline copies on separately held existing disks: zero service charge, disk/hardware/electricity unpriced.',
                      'R2 Standard object store: paid availability depends on account and operator; no permanence guarantee.',
                      'IPFS pinning on independent providers: not quoted, no CID asserted or upload performed.',
                      'On-chain bytes: no fee quote or transaction; not recommended/authorized by this task.']}
(ROOT / 'storage-proposal.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
