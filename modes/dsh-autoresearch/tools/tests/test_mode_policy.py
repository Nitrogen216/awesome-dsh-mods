#!/usr/bin/env python3
"""Static policy checks for the dsh_autoresearch V4 preset."""

from __future__ import annotations

import unittest
import re
from pathlib import Path

PRESET = Path(__file__).resolve().parents[2]


class ModePolicyTest(unittest.TestCase):
    """Protect the performance pipeline from old defensive-loop behavior."""

    def test_persona_contains_ordered_pipeline_and_read_only_class(self) -> None:
        config = (PRESET / "agent.cordis.yml").read_text(encoding="utf-8")
        stages = [
            "current state and baseline",
            "deep reading of related literature",
            "contribution/hypothesis mapping",
            "one minimal adaptation",
            "small-scale training screen",
            "full training confirmation",
            "promotion audit",
        ]
        positions = [config.index(stage) for stage in stages]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("status-report requests are read-only", config)
        self.assertIn("`improve-existing-project`", config)
        self.assertIn("`discover-research-idea`", config)
        self.assertIn("fetch: false", config)
        literature = (
            PRESET / "skills" / "literature-research" / "SKILL.md"
        ).read_text(encoding="utf-8")
        self.assertIn("never count it as a deep read", literature)

    def test_active_surface_has_no_old_state_or_hash_implementation(self) -> None:
        active_paths = [
            PRESET / "agent.cordis.yml",
            PRESET / "tools" / "transition_guard.py",
            *sorted((PRESET / "skills").glob("*/SKILL.md")),
            *sorted((PRESET / "templates" / "research").glob("*")),
        ]
        active = "\n".join(path.read_text(encoding="utf-8") for path in active_paths)
        for obsolete in (
            "stale_count",
            "next_transition_requires_governor",
            "content_hash",
            "hashlib",
            "STOP_FOR_HUMAN",
            "TRUNK_FROZEN",
        ):
            self.assertNotIn(obsolete, active)
        for obsolete_file in (
            "iteration_log.py",
            "provenance.py",
            "run_state.py",
        ):
            self.assertFalse((PRESET / "tools" / obsolete_file).exists())

    def test_all_skills_have_complete_frontmatter(self) -> None:
        skills = sorted((PRESET / "skills").glob("*/SKILL.md"))
        self.assertGreaterEqual(len(skills), 21)
        for skill in skills:
            text = skill.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("---\nname: "))
            self.assertIn("\ndescription: ", text.split("---", 2)[1])
            self.assertNotIn("TODO", text)

    def test_skill_catalog_is_isolated_at_discovery_and_execution(self) -> None:
        config = (PRESET / "agent.cordis.yml").read_text(encoding="utf-8")
        self.assertIn("providerName: dsh-autoresearch", config)
        self.assertIn("includeDefaultRoots: false", config)
        self.assertIn("name: './plugins/skill-isolation.mjs'", config)

        block = config.split("allowedSkills:", 1)[1].split("\n\n", 1)[0]
        allowed = set(re.findall(r"^\s+- ([a-z0-9-]+)$", block, re.MULTILINE))
        actual = {path.parent.name for path in (PRESET / "skills").glob("*/SKILL.md")}
        self.assertEqual(allowed, actual)

        policy = (PRESET / "plugins" / "skill-isolation.mjs").read_text(
            encoding="utf-8"
        )
        self.assertIn("ctx.tools.guard", policy)
        self.assertIn("exec.name !== 'skill'", policy)
        self.assertIn("curated preset skills", policy)

    def test_oracle_browser_pro_is_runtime_guarded_and_fail_closed(self) -> None:
        oracle = (PRESET / "skills" / "oracle" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        for expected in (
            "name: oracle",
            "call `oracle_governor`",
            "run_in_background: true",
            "dryRunCommand",
            "runCommand",
            "fails closed if Pro cannot be confirmed",
            "Responses remain advisory",
            "Never attach `.env` files",
            "require an `askgpt-governor` verdict of `consult_oracle`",
            "literal workspace-relative files",
        ):
            self.assertIn(expected, oracle)

        config = (PRESET / "agent.cordis.yml").read_text(encoding="utf-8")
        for expected in (
            "ORACLE / CHATGPT PRO ADVISOR",
            "automatic consultation is for major decisions only",
            "`oracle_governor` runtime tool with basis `major_decision`",
            "basis `explicit_user_request`",
            "The automatic gate passes only when all are true",
            "If it is unclear whether a choice meets every condition",
            "Never auto-call Oracle for an ordinary negative result",
            "Consult at most once for the same decision",
            "--dry-run summary --files-report",
            "rejects direct shell calls",
            "an Oracle answer never advances research state by itself",
            "name: './plugins/oracle-governor.mjs'",
            "thinkingTime: pro",
        ):
            self.assertIn(expected, config)

        runtime = (PRESET / "plugins" / "oracle-governor.mjs").read_text(
            encoding="utf-8"
        )
        for expected in (
            "ctx.tools.register",
            "name: 'oracle_governor'",
            "ctx.tools.guard",
            "dry_pending",
            "run_pending",
            "args.run_in_background !== true",
            "replayState(agent)",
            "explicit_user_request",
            "gpt-5.6-sol",
            "--dry-run", "summary", "--files-report",
        ):
            self.assertIn(expected, runtime)

    def test_only_governor_may_automatically_load_oracle(self) -> None:
        governor = (
            PRESET / "skills" / "askgpt-governor" / "SKILL.md"
        ).read_text(encoding="utf-8")
        oracle = (PRESET / "skills" / "oracle" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        for expected in (
            "sole reasoning gate for automatic Oracle calls",
            "all five conditions hold",
            "consult_oracle",
            "continue_local",
            "Two or three scientifically defensible alternatives remain",
            "cannot resolve the alternatives",
            "Never switch to API, a different model, a weaker thinking tier",
            "mapping:mechanism-family:v1",
            "Do not compute a hash or create a parallel advisor ledger",
            "call `oracle_governor` with basis `major_decision`",
        ):
            self.assertIn(expected, governor)

        for expected in (
            "This mode-local skill exposes the `oracle_governor` runtime path",
            "If login, account entitlement, picker selection, or CLI validation fails",
            "do not use API mode, GPT-5.5, base-Sol `extra-high`",
        ):
            self.assertIn(expected, oracle)

        direct_loaders = []
        for path in sorted((PRESET / "skills").glob("*/SKILL.md")):
            if path.parent.name == "oracle":
                continue
            if "load `oracle`" in path.read_text(encoding="utf-8").lower():
                direct_loaders.append(path.parent.name)
        self.assertEqual(direct_loaders, ["askgpt-governor"])

        phase_escalators = {
            "baseline-assessment",
            "contribution-hypothesis-map",
            "depth-research-loop",
            "experiment-plan",
            "experiment-run",
            "paper-plan",
            "promotion-review",
        }
        for name in phase_escalators:
            text = (PRESET / "skills" / name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("askgpt-governor", text)

        routine_owners = {
            "evidence-audit",
            "experiment-monitor",
            "literature-research",
            "minimal-adaptation",
            "paper-compile",
            "paper-figure",
            "paper-polish",
            "paper-write",
        }
        for name in routine_owners:
            text = (PRESET / "skills" / name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            self.assertNotIn("load `askgpt-governor`", text.lower())

    def test_paper_pipeline_is_separate_and_bounded(self) -> None:
        config = (PRESET / "agent.cordis.yml").read_text(encoding="utf-8")
        stages = [
            "evidence handoff",
            "claims and outline",
            "figures and tables",
            "section draft",
            "compile and render",
            "at most two issue-driven revision passes",
            "one final factual check",
        ]
        positions = [config.index(stage) for stage in stages]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("do not mutate research/STATE.json", config)
        self.assertIn(
            "do not advance research state or launch new experiments",
            config,
        )
        self.assertIn("V4 state-directed handoff", config)
        self.assertIn("venue-neutral research article and PDF", config)

        expected = {
            "paper-writing",
            "paper-plan",
            "paper-figure",
            "paper-write",
            "paper-compile",
            "paper-polish",
        }
        actual = {
            path.parent.name
            for path in (PRESET / "skills").glob("paper-*/SKILL.md")
        }
        self.assertEqual(actual, expected)

        paper_text = "\n".join(
            (PRESET / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            for name in sorted(expected)
        )
        self.assertIn("Do not mutate research/STATE.json", paper_text)
        self.assertIn("at most two", paper_text)
        self.assertIn("next_action.skill", paper_text)
        self.assertIn("venue-neutral", paper_text)
        lowered = paper_text.lower()
        for excluded in (
            "rebuttal",
            "resubmit",
            "kill-argument",
            "integrity-forensics",
            "paper_acceptance_contract",
            "audited_input_hashes",
            "sha256",
            "overall score",
        ):
            self.assertNotIn(excluded, lowered)

    def test_paper_templates_cover_plan_and_single_final_check(self) -> None:
        templates = PRESET / "templates" / "paper"
        plan = (templates / "PAPER_PLAN.md.tmpl").read_text(encoding="utf-8")
        final = (templates / "FINAL_CHECK.md.tmpl").read_text(encoding="utf-8")
        self.assertIn("Claims-evidence matrix", plan)
        self.assertIn("Contribution positioning", plan)
        self.assertIn("Reader-state and causal design chain", plan)
        self.assertIn("One-sentence takeaway", plan)
        self.assertIn("Three-second visual evidence", plan)
        self.assertIn("FINAL PAPER CHECK", final)
        self.assertIn("Forward logic and prose", final)
        self.assertIn("Figure takeaways", final)
        self.assertIn("Remaining evidence gaps", final)
        self.assertTrue((templates / "VENUE_NEUTRAL_MAIN.tex.tmpl").is_file())
        self.assertIn("venue-neutral", plan)
        self.assertIn("venue-neutral", final)

    def test_two_entrances_converge_on_native_experiment_bridge(self) -> None:
        existing = (
            PRESET / "skills" / "improve-existing-project" / "SKILL.md"
        ).read_text(encoding="utf-8")
        broad = (
            PRESET / "skills" / "discover-research-idea" / "SKILL.md"
        ).read_text(encoding="utf-8")
        bridge = (PRESET / "skills" / "experiment-bridge" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        loop = (PRESET / "skills" / "depth-research-loop" / "SKILL.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("--entry-mode existing-project", existing)
        self.assertIn("--entry-mode broad-direction", broad)
        self.assertIn("research/PROBLEM_ANCHOR.md", broad)
        self.assertIn("load `depth-research-loop`", existing.lower())
        self.assertIn("load `depth-research-loop`", broad.lower())
        self.assertIn("transition_guard.py reserve-run", bridge)
        self.assertIn("run_in_background: true", bridge)
        self.assertIn("scientific run ID", bridge)
        self.assertIn("DSH job ID", bridge)
        self.assertIn("experiment-bridge -> experiment-plan", loop)

        state = (PRESET / "templates" / "research" / "STATE.json.tmpl").read_text(
            encoding="utf-8"
        )
        for expected in (
            '"mode_version": 4',
            '"entry_mode"',
            '"deliverable"',
            '"target_venue"',
            '"run_counters"',
            '"promoted_evidence_id"',
        ):
            self.assertIn(expected, state)

    def test_paper_skills_share_forward_logic_and_figure_standard(self) -> None:
        reference = (PRESET / "references" / "paper-forward-logic.md").read_text(
            encoding="utf-8"
        )
        for expected in (
            "Separate global payoff from local explanation",
            "exposed problem",
            "insufficient default",
            "derived requirement",
            "paragraph should perform one reasoning move",
            "about three seconds",
            "every textual module into a box",
        ):
            self.assertIn(expected, reference)

        consumers = {
            "paper-writing",
            "paper-plan",
            "paper-write",
            "paper-figure",
            "paper-polish",
        }
        for name in consumers:
            text = (PRESET / "skills" / name / "SKILL.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("../../references/paper-forward-logic.md", text)

        config = (PRESET / "agent.cordis.yml").read_text(encoding="utf-8")
        for expected in (
            "forward logic",
            "insufficient default",
            "one inferential move",
            "three seconds",
            "every textual module into a box",
        ):
            self.assertIn(expected, config)

    def test_aris_adaptations_remain_bounded_and_claim_driven(self) -> None:
        literature = (PRESET / "skills" / "literature-research" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        experiment = (PRESET / "skills" / "experiment-plan" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        promotion = (PRESET / "skills" / "promotion-review" / "SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("repository's papers, bibliography, literature notes", literature)
        self.assertIn("parent executor deduplicates", literature)
        self.assertIn("writes `research/LITERATURE.md` once", literature)
        self.assertIn("which claim it tests", experiment)
        self.assertIn("valid failure means", experiment)
        self.assertIn("must-run comparisons", experiment)
        self.assertIn("result-to-claim table", promotion)
        self.assertIn("claims not supported", promotion)


if __name__ == "__main__":
    unittest.main()
