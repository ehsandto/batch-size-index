# BatchSizeIndex — Exact Quotes from Published Pack Terms

**Contribution type** Builder → Intelligent Contracts

BatchSizeIndex returns the smallest attainable quantity at or above a requested minimum. It also returns exact pack counts and the threshold after which every multiple of the common pack-size divisor is attainable.

The leader and validators independently fetch the complete commit-pinned catalog and verify its SHA-256. Each uses an LLM to decide which offers are currently active for unrestricted repeat ordering. Exact agreement covers every offer label and the full evidence. The accepted labels determine the set of pack sizes used by the solver. When terms are ambiguous, the contract distinguishes the smallest quantity attainable using confirmed offers from the smallest quantity that could be attained if ambiguous offers are active.

The fictional demonstration keeps the same pack sizes in both catalogs. With the nine-unit offer withdrawn, a minimum of 17 yields **18** using one pack of four and two of seven. With the nine-unit offer active, the contract yields **17** using two packs of four and one of nine. The eventual coverage threshold falls from 18 to 11.

GenVM lint and six tests passed. An independent dynamic program checked 8,256 minimum-quantity quotes and their pack-count witnesses.

StudioNet finalized the deployment and both catalog registrations with majority agreement and recorded validator execution. Live views returned both exact quotes and pack-count witnesses. The deployed source matched the pinned repository source.

[GitHub repository](https://github.com/ehsandto/batch-size-index) ·
[StudioNet deployment](https://explorer-studio.genlayer.com/address/0xA3f3513030110d5cfbdF3FC3c8625ca4596daf81) ·
[Proofs and receipts](https://github.com/ehsandto/batch-size-index/blob/main/LIVE_PROOFS.md)
