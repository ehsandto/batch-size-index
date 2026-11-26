# BatchSizeIndex

BatchSizeIndex finds the smallest quantity at or above a buyer's minimum using repeatable pack sizes. It returns the exact count of each pack in the solution and the threshold beyond which every multiple of the smallest common unit is attainable.

`index_catalog(coordinate, commitment)` accepts a full GitHub commit path and the exact SHA-256 of a catalog containing one to six distinct sizes from 1 through 64. The leader and validators independently fetch the entire document, check the digest, and use an LLM to classify the terms of each pack. Their complete canonical observations must match, including the full text and every offer label.

The contract derives residue tables using minimum reachable quantities modulo the smallest pack size after dividing by the greatest common divisor. The table includes a pack-count witness for each residue. Queries work with integer amounts up to 10^12 by adding repeats of the smallest pack. Runtime depends on the bounded pack sizes.

`get_catalog(commitment)` returns the original text, exact labels, and both tables. `quote(commitment, minimum)` returns the smallest quantity and a pack-count witness in two cases. The guaranteed result uses active offers. The possible result also admits packs whose terms are ambiguous. Both quantities model repeatable catalog terms.

In the fictional fixtures, a request for at least 17 requires 18 units when the nine-unit pack is withdrawn. When the nine-unit pack is active, the contract finds an exact 17. The threshold above which every integer is attainable falls from 18 to 11.

Install `requirements-dev.txt`, then run `python -m pytest tests -q` and `genvm-lint check contracts/BatchSizeIndex.py`.

[Submission](SUBMISSION.md) · [StudioNet proofs](LIVE_PROOFS.md)
