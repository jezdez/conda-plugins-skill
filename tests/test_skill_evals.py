from __future__ import annotations

import json
from pathlib import Path


def test_skill_evaluation_cases_are_usable() -> None:
    root = Path(__file__).resolve().parent
    cases = json.loads((root / "skill_evals.json").read_text(encoding="utf-8"))
    skill = root.parent / "skills" / cases["skill_name"]
    assert (skill / "SKILL.md").is_file()
    assert cases["evals"]
    ids = [case["id"] for case in cases["evals"]]
    assert len(ids) == len(set(ids))
    for case in cases["evals"]:
        assert case["prompt"].strip()
        assert case["expected_output"].strip()
        assert case["assertions"]
        assert all(assertion.strip() for assertion in case["assertions"])
        for relative in case["files"]:
            path = (root / relative).resolve()
            assert path.is_relative_to(root / "fixtures")
            assert path.is_file()
    queries = cases["trigger_queries"]
    assert {query["should_trigger"] for query in queries} == {True, False}
    assert all(type(query["should_trigger"]) is bool for query in queries)
    assert all(query["query"].strip() for query in queries)
