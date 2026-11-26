import hashlib
import json
import re
import sys
from itertools import combinations
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
PREFIX = "ehsandto/batch-size-index/" + "a" * 40 + "/fixtures/"
WITHDRAWN = ["ACTIVE", "ACTIVE", "INACTIVE"]
ACTIVE = ["ACTIVE", "ACTIVE", "ACTIVE"]


@pytest.fixture
def index(direct_deploy):
    instance = direct_deploy(str(ROOT / "contracts/BatchSizeIndex.py"))
    return instance, sys.modules[type(instance._instance).__module__]


def mock(vm, name, labels, tampered=False):
    body = (ROOT / "fixtures" / (name + ".json")).read_bytes()
    path = PREFIX + name + ".json"
    vm.clear_mocks()
    vm.mock_web(re.escape("https://raw.githubusercontent.com/" + path) + "$", {
        "method": "GET", "response": {"status": 200, "headers": {}, "body": body + (b" " if tampered else b"")},
    })
    vm.mock_llm(r".*BATCH SIZE INDEX EXTRACTION.*", json.dumps({"labels": labels}))
    return path, hashlib.sha256(body).hexdigest()


@pytest.mark.parametrize(("name", "labels", "expected"), [
    ("withdrawn", WITHDRAWN, {"quantity": 18, "packs": [[4, 1], [7, 2]], "step": 1, "all_multiples_from": 18}),
    ("active", ACTIVE, {"quantity": 17, "packs": [[4, 2], [9, 1]], "step": 1, "all_multiples_from": 11}),
])
def test_catalog_semantics_change_exact_quote(index, direct_vm, name, labels, expected):
    contract, _ = index
    args = mock(direct_vm, name, labels)
    key = contract.index_catalog(*args)
    assert key == args[1]
    assert direct_vm.run_validator()
    assert contract.get_catalog(key)["labels"] == labels
    assert contract.quote(key, 17) == {"guaranteed": expected, "possible": expected}


def test_validator_rejects_changed_label_and_hash(index, direct_vm):
    contract, _ = index
    args = mock(direct_vm, "withdrawn", WITHDRAWN)
    contract.index_catalog(*args)
    mock(direct_vm, "withdrawn", ACTIVE)
    assert not direct_vm.run_validator()
    mock(direct_vm, "withdrawn", WITHDRAWN, tampered=True)
    assert not direct_vm.run_validator()
    assert contract.index_catalog(*args) == args[1]


def test_unknown_offer_separates_guaranteed_and_possible(index, direct_vm):
    contract, _ = index
    key = contract.index_catalog(*mock(direct_vm, "active", ["ACTIVE", "ACTIVE", "UNKNOWN"]))
    assert direct_vm.run_validator()
    quote = contract.quote(key, 17)
    assert quote["guaranteed"]["quantity"] == 18
    assert quote["possible"]["quantity"] == 17


def test_no_eligible_packs(index, direct_vm):
    contract, _ = index
    key = contract.index_catalog(*mock(direct_vm, "withdrawn", ["INACTIVE"] * 3))
    assert contract.quote(key, 17) == {"guaranteed": None, "possible": None}


def test_modular_index_matches_dynamic_programming(index):
    _, module = index
    for count in (1, 2, 3):
        for sizes in combinations(range(1, 10), count):
            table = module.build_table(sizes)
            reachable = [True] + [False] * 96
            for total in range(1, len(reachable)):
                reachable[total] = any(total >= size and reachable[total - size] for size in sizes)
            step = table["unit"]
            last_hole = max((i for i in range(0, len(reachable), step) if not reachable[i]), default=-step)
            assert table["all_multiples_from"] == last_hole + step
            for floor in range(1, 65):
                quote = module.plan(table, floor)
                assert quote["quantity"] == next(i for i in range(floor, len(reachable)) if reachable[i])
                assert sum(size * count for size, count in quote["packs"]) == quote["quantity"]
                assert all(size in sizes and count > 0 for size, count in quote["packs"])
