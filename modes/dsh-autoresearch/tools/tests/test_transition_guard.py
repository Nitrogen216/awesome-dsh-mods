#!/usr/bin/env python3
"""Behavior tests for the dsh_autoresearch V4 transition guard."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

GUARD = Path(__file__).resolve().parents[1] / "transition_guard.py"


class GuardTest(unittest.TestCase):
    """Exercise scientific routing through the command-line interface."""

    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.research = self.root / "research"
        self.research.mkdir()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def run_guard(self, *args: str, ok: bool = True) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["python3", str(GUARD), *args],
            check=False,
            text=True,
            capture_output=True,
        )
        if ok and result.returncode != 0:
            self.fail(f"guard failed: {result.stderr}\n{result.stdout}")
        if not ok and result.returncode == 0:
            self.fail(f"guard unexpectedly passed: {result.stdout}")
        return result

    def init(
        self,
        *,
        entry_mode: str = "existing-project",
        deliverable: str = "method",
        target_venue: str | None = None,
    ) -> None:
        venue_args = ["--target-venue", target_venue] if target_venue else []
        self.run_guard(
            "init",
            str(self.root),
            "--entry-mode",
            entry_mode,
            "--deliverable",
            deliverable,
            *venue_args,
            "--objective",
            "improve validation Dice",
            "--primary-metric",
            "Dice",
            "--metric-direction",
            "higher",
            "--target-delta",
            "+0.5 Dice",
            "--baseline-run",
            "base-1",
            "--baseline-artifact",
            "Artifacts/base-1/results.json",
        )

    def apply(self, source: str, target: str, outcome: str, *extra: str) -> None:
        self.run_guard(
            "apply",
            str(self.root),
            "--from",
            source,
            "--to",
            target,
            "--outcome",
            outcome,
            *extra,
        )

    def state(self) -> dict[str, object]:
        return json.loads((self.research / "STATE.json").read_text(encoding="utf-8"))

    def allocate(self, count: int) -> list[str]:
        result = self.run_guard(
            "allocate-candidates", str(self.root), "--count", str(count)
        )
        return json.loads(result.stdout)["candidate_ids"]

    def reach_screening(self, candidate: str, count: int = 2) -> None:
        self.apply("baseline", "literature", "baseline_ready")
        self.apply("literature", "mapping", "literature_ready")
        self.allocate(count)
        self.apply(
            "mapping",
            "adaptation",
            "candidate_selected",
            "--candidate-id",
            candidate,
        )
        self.apply("adaptation", "screening", "implemented")

    def test_full_success_generates_stable_evidence_id(self) -> None:
        self.init()
        self.reach_screening("r1-c1")
        self.apply("screening", "confirmation", "screen_pass")
        self.apply("confirmation", "promotion", "confirmed")
        result = self.run_guard(
            "apply",
            str(self.root),
            "--from",
            "promotion",
            "--to",
            "frozen",
            "--outcome",
            "audit_pass",
        )
        output = json.loads(result.stdout)
        self.assertEqual(output["evidence_id"], "evidence-r1-c1-c1")
        self.assertIsNone(output["next_action"])
        self.assertEqual(
            self.state()["promoted_evidence_id"], "evidence-r1-c1-c1"
        )

    def test_paper_goal_hands_off_at_frozen_without_venue(self) -> None:
        self.init(deliverable="paper")
        self.reach_screening("r1-c1", count=1)
        self.apply("screening", "confirmation", "screen_pass")
        self.apply("confirmation", "promotion", "confirmed")
        result = self.run_guard(
            "apply",
            str(self.root),
            "--from",
            "promotion",
            "--to",
            "frozen",
            "--outcome",
            "audit_pass",
        )
        self.assertEqual(
            json.loads(result.stdout)["next_action"],
            {"skill": "paper-writing", "target_venue": "venue-neutral"},
        )
        shown = json.loads(
            self.run_guard("show", str(self.root)).stdout
        )
        self.assertEqual(shown["deliverable"], "paper")
        self.assertEqual(shown["next_action"]["skill"], "paper-writing")

    def test_named_venue_is_persisted_for_paper_handoff(self) -> None:
        self.init(
            entry_mode="broad-direction",
            deliverable="paper",
            target_venue="NeurIPS",
        )
        state = self.state()
        self.assertEqual(state["entry_mode"], "broad-direction")
        self.assertEqual(state["target_venue"], "NeurIPS")
        self.reach_screening("r1-c1", count=1)
        self.apply("screening", "confirmation", "screen_pass")
        self.apply("confirmation", "promotion", "confirmed")
        self.apply("promotion", "frozen", "audit_pass")
        shown = json.loads(self.run_guard("show", str(self.root)).stdout)
        self.assertEqual(
            shown["next_action"],
            {"skill": "paper-writing", "target_venue": "NeurIPS"},
        )

    def test_method_deliverable_rejects_a_target_venue(self) -> None:
        self.run_guard(
            "init",
            str(self.root),
            "--entry-mode",
            "existing-project",
            "--deliverable",
            "method",
            "--target-venue",
            "NeurIPS",
            "--objective",
            "improve validation Dice",
            "--primary-metric",
            "Dice",
            "--metric-direction",
            "higher",
            "--target-delta",
            "+0.5 Dice",
            "--baseline-run",
            "base-1",
            "--baseline-artifact",
            "Artifacts/base-1/results.json",
            ok=False,
        )
        self.assertFalse((self.research / "STATE.json").exists())

    def test_two_no_gain_candidates_force_literature_refresh(self) -> None:
        self.init()
        self.reach_screening("r1-c1")
        self.apply("screening", "mapping", "screen_fail")
        first = self.state()
        self.assertEqual(first["consecutive_no_gain"], 1)
        self.assertEqual(first["rejected_candidates"], ["r1-c1"])

        self.apply(
            "mapping",
            "adaptation",
            "candidate_selected",
            "--candidate-id",
            "r1-c2",
        )
        self.apply("adaptation", "screening", "implemented")
        self.run_guard(
            "apply",
            str(self.root),
            "--from",
            "screening",
            "--to",
            "mapping",
            "--outcome",
            "screen_fail",
            ok=False,
        )
        self.assertEqual(self.state()["phase"], "screening")

        self.apply("screening", "literature", "screen_fail")
        refreshed = self.state()
        self.assertEqual(refreshed["phase"], "literature")
        self.assertEqual(refreshed["consecutive_no_gain"], 0)
        self.assertEqual(refreshed["literature_revision"], 2)
        self.assertEqual(refreshed["candidate_pool"], [])
        self.assertEqual(
            refreshed["rejected_candidates"],
            ["r1-c1", "r1-c2"],
        )

    def test_illegal_stage_skip_is_rejected(self) -> None:
        self.init()
        self.run_guard(
            "check",
            str(self.root),
            "--from",
            "baseline",
            "--to",
            "screening",
            "--outcome",
            "implemented",
            ok=False,
        )
        self.assertEqual(self.state()["phase"], "baseline")

    def test_check_does_not_write(self) -> None:
        self.init()
        before = (self.research / "STATE.json").read_text(encoding="utf-8")
        self.run_guard(
            "check",
            str(self.root),
            "--from",
            "baseline",
            "--to",
            "literature",
            "--outcome",
            "baseline_ready",
        )
        after = (self.research / "STATE.json").read_text(encoding="utf-8")
        self.assertEqual(before, after)

    def test_candidate_ids_are_allocated_by_revision(self) -> None:
        self.init()
        self.apply("baseline", "literature", "baseline_ready")
        self.apply("literature", "mapping", "literature_ready")
        self.assertEqual(self.allocate(3), ["r1-c1", "r1-c2", "r1-c3"])
        self.run_guard(
            "apply",
            str(self.root),
            "--from",
            "mapping",
            "--to",
            "adaptation",
            "--outcome",
            "candidate_selected",
            "--candidate-id",
            "manual-id",
            ok=False,
        )

    def test_run_ids_are_reserved_separately_from_job_ids(self) -> None:
        self.init()
        self.reach_screening("r1-c1", count=1)
        first = json.loads(
            self.run_guard("reserve-run", str(self.root)).stdout
        )
        second = json.loads(
            self.run_guard("reserve-run", str(self.root)).stdout
        )
        self.assertEqual(first["id"], "r1-c1-screen-a1")
        self.assertEqual(second["id"], "r1-c1-screen-a2")
        self.apply("screening", "confirmation", "screen_pass")
        confirmation = json.loads(
            self.run_guard("reserve-run", str(self.root)).stdout
        )
        self.assertEqual(confirmation["id"], "r1-c1-confirm-a1")

    def test_migration_preserves_legacy_state(self) -> None:
        legacy = {
            "mode_version": 3,
            "phase": "experiment",
            "active_hypothesis": "H9",
        }
        (self.research / "STATE.json").write_text(
            json.dumps(legacy) + "\n", encoding="utf-8"
        )
        self.run_guard(
            "migrate",
            str(self.root),
            "--phase",
            "confirmation",
            "--entry-mode",
            "existing-project",
            "--deliverable",
            "method",
            "--objective",
            "improve validation Dice",
            "--primary-metric",
            "Dice",
            "--metric-direction",
            "higher",
            "--target-delta",
            "+0.5 Dice",
            "--baseline-run",
            "base-1",
            "--baseline-artifact",
            "Artifacts/base-1/results.json",
            "--candidate-id",
            "legacy-h9",
            "--candidate-pool",
            "legacy-h9",
        )
        self.assertEqual(self.state()["phase"], "confirmation")
        self.assertTrue((self.research / "STATE.v3.json").is_file())


if __name__ == "__main__":
    unittest.main()
