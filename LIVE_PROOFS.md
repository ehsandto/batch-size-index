# StudioNet proofs

[Contract on StudioNet](https://explorer-studio.genlayer.com/address/0xA3f3513030110d5cfbdF3FC3c8625ca4596daf81) ·
[Pinned source](https://github.com/ehsandto/batch-size-index/blob/a1558cd5354daec4fac737d452c59f4660ecec65/contracts/BatchSizeIndex.py) ·
[Machine-readable receipts and readbacks](PROOFS.json)

All three transactions finalized with `SUCCESS`, `MAJORITY_AGREE`, and recorded validator execution. Deployed source matched the pinned repository bytes after line-ending normalization. Each catalog read returned the complete pinned text and expected labels.

| Transaction | Agree votes | Minimum quote for 17 |
| --- | --- | --- |
| [Deploy](https://explorer-studio.genlayer.com/tx/0xe1362ba5d2a65c659129f2e7135607e71da7e993e049c3606c8ee2d761d46f28) | 3 | — |
| [Index withdrawn offer](https://explorer-studio.genlayer.com/tx/0x9c90d9db488571a12e507a5c91212b87728fb668d54938d5e5ca7d62520b7015) | 3 | 18 using one pack of 4 and two of 7 |
| [Index active offer](https://explorer-studio.genlayer.com/tx/0x5a533e8fc3cf0a3e5161955c1f52aad5b5b2f135d7b9fa894bb53bf3de404a60) | 3 | 17 using two packs of 4 and one of 9 |

The coverage threshold was 18 with the nine-unit pack withdrawn and 11 with it active. The fixture catalogs are fictional. The `UNKNOWN` branch was exercised in the local tests.

StudioNet initially interpreted raw quote calldata as RLP and rejected the view call. The proof harness now retries that specific parser error with the SDK's RLP read envelope. Both quotes and witnesses then verified.

`npm ci` followed by `node scripts/live.mjs --verify-only` checks the receipts, source, catalogs, and returned witnesses.
