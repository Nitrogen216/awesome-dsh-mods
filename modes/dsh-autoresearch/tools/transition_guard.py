#!/usr/bin/env python3
"""Enforce the dsh_autoresearch V4 performance pipeline.

The guard owns one canonical state file and an append-only transition history.
It records scientific routing decisions; it does not score ideas or audit
results.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

MODE_VERSION = 4
ENTRY_MODES = ("existing-project", "broad-direction")
DELIVERABLES = ("method", "paper")
PHASES = (
    "baseline",
    "literature",
    "mapping",
    "adaptation",
    "screening",
    "confirmation",
    "promotion",
    "frozen",
)

TRANSITION_OUTCOMES: dict[tuple[str, str], frozenset[str]] = {
    ("baseline", "literature"): frozenset({"baseline_ready"}),
    ("literature", "mapping"): frozenset({"literature_ready"}),
    ("mapping", "adaptation"): frozenset({"candidate_selected"}),
    ("mapping", "literature"): frozenset({"evidence_gap"}),
    ("adaptation", "screening"): frozenset({"implemented"}),
    ("adaptation", "mapping"): frozenset({"invalid"}),
    ("adaptation", "literature"): frozenset({"evidence_gap", "invalid"}),
    ("screening", "confirmation"): frozenset({"screen_pass"}),
    ("screening", "mapping"): frozenset({"screen_fail", "invalid"}),
    ("screening", "literature"): frozenset({"screen_fail", "evidence_gap", "invalid"}),
    ("confirmation", "promotion"): frozenset({"confirmed"}),
    ("confirmation", "mapping"): frozenset({"not_confirmed", "invalid"}),
    ("confirmation", "literature"): frozenset(
        {"not_confirmed", "evidence_gap", "invalid"}
    ),
    ("promotion", "frozen"): frozenset({"audit_pass"}),
    ("promotion", "confirmation"): frozenset({"audit_fix"}),
    ("promotion", "mapping"): frozenset({"audit_fail"}),
    ("promotion", "literature"): frozenset({"audit_fail"}),
}

NO_GAIN_OUTCOMES = frozenset({"screen_fail", "not_confirmed"})
REJECTING_OUTCOMES = frozenset(
    {"screen_fail", "not_confirmed", "invalid", "audit_fail"}
)


class TransitionError(ValueError):
    """Report an invalid pipeline state or transition."""


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _research_dir(root: str | Path) -> Path:
    project_root = Path(root).expanduser().resolve()
    if not project_root.is_dir():
        raise TransitionError(f"project root does not exist: {project_root}")
    return project_root / "research"


def _state_path(root: str | Path) -> Path:
    return _research_dir(root) / "STATE.json"


def _history_path(root: str | Path) -> Path:
    return _research_dir(root) / "PIPELINE.jsonl"


def _atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(payload)
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def _append_event(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def _parse_pool(raw: str | None) -> list[str] | None:
    if raw is None:
        return None
    values = [item.strip() for item in raw.split(",") if item.strip()]
    if not values:
        raise TransitionError("--candidate-pool must contain at least one id")
    if len(values) != len(set(values)):
        raise TransitionError("--candidate-pool contains duplicate ids")
    if len(values) > 5:
        raise TransitionError("candidate pool may contain at most five ids")
    return values


def _new_state(
    *,
    entry_mode: str,
    deliverable: str,
    target_venue: str | None,
    objective: str,
    primary_metric: str,
    metric_direction: str,
    target_delta: str,
    baseline_run: str,
    baseline_artifact: str,
    phase: str = "baseline",
    candidate_id: str | None = None,
    candidate_pool: list[str] | None = None,
    promoted_evidence_id: str | None = None,
) -> dict[str, Any]:
    pool = list(candidate_pool or [])
    if candidate_id and candidate_id not in pool:
        pool.append(candidate_id)
    state: dict[str, Any] = {
        "mode_version": MODE_VERSION,
        "entry_mode": entry_mode,
        "deliverable": deliverable,
        "target_venue": target_venue.strip() if target_venue else None,
        "phase": phase,
        "objective": objective.strip(),
        "primary_metric": primary_metric.strip(),
        "metric_direction": metric_direction,
        "target_delta": target_delta.strip(),
        "baseline": {
            "run_id": baseline_run.strip(),
            "artifact": baseline_artifact.strip(),
        },
        "literature_revision": 0 if phase == "baseline" else 1,
        "candidate_pool": pool,
        "rejected_candidates": [],
        "active_candidate_id": candidate_id,
        "screen_attempt": 0,
        "confirmation_attempt": 0,
        "run_counters": {"screening": 0, "confirmation": 0},
        "last_run": None,
        "promoted_evidence_id": promoted_evidence_id,
        "consecutive_no_gain": 0,
        "last_outcome": None,
        "last_transition": None,
    }
    _validate_state(state)
    return state


def _load_state(root: str | Path) -> dict[str, Any]:
    path = _state_path(root)
    if not path.is_file():
        raise TransitionError(
            f"missing {path}; establish baseline evidence and run the init command"
        )
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise TransitionError(f"cannot read valid JSON state: {error}") from error
    if not isinstance(state, dict):
        raise TransitionError("STATE.json must contain a JSON object")
    _validate_state(state)
    return state


def _validate_nonnegative_int(state: dict[str, Any], field: str) -> None:
    value = state.get(field)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise TransitionError(f"{field} must be a non-negative integer")


def _validate_state(state: dict[str, Any]) -> None:
    if state.get("mode_version") != MODE_VERSION:
        raise TransitionError(
            "legacy or unsupported STATE.json; run migrate explicitly for improvement work"
        )
    if state.get("phase") not in PHASES:
        raise TransitionError(f"unknown phase: {state.get('phase')!r}")
    if state.get("entry_mode") not in ENTRY_MODES:
        raise TransitionError(
            "entry_mode must be 'existing-project' or 'broad-direction'"
        )
    if state.get("deliverable") not in DELIVERABLES:
        raise TransitionError("deliverable must be 'method' or 'paper'")
    target_venue = state.get("target_venue")
    if target_venue is not None and (
        not isinstance(target_venue, str) or not target_venue.strip()
    ):
        raise TransitionError("target_venue must be null or a non-empty string")
    if state["deliverable"] == "method" and target_venue is not None:
        raise TransitionError("target_venue applies only to paper deliverables")
    for field in ("objective", "primary_metric", "target_delta"):
        value = state.get(field)
        if not isinstance(value, str) or not value.strip():
            raise TransitionError(f"{field} must be a non-empty string")
    if state.get("metric_direction") not in {"higher", "lower"}:
        raise TransitionError("metric_direction must be 'higher' or 'lower'")
    baseline = state.get("baseline")
    if not isinstance(baseline, dict):
        raise TransitionError("baseline must be an object")
    for field in ("run_id", "artifact"):
        value = baseline.get(field)
        if not isinstance(value, str) or not value.strip():
            raise TransitionError(f"baseline.{field} must be a non-empty string")
    for field in (
        "literature_revision",
        "screen_attempt",
        "confirmation_attempt",
        "consecutive_no_gain",
    ):
        _validate_nonnegative_int(state, field)
    run_counters = state.get("run_counters")
    if not isinstance(run_counters, dict) or set(run_counters) != {
        "screening",
        "confirmation",
    }:
        raise TransitionError(
            "run_counters must contain screening and confirmation"
        )
    for phase in ("screening", "confirmation"):
        value = run_counters[phase]
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise TransitionError(f"run_counters.{phase} must be non-negative")
    last_run = state.get("last_run")
    if last_run is not None:
        if not isinstance(last_run, dict) or set(last_run) != {
            "id",
            "phase",
            "candidate_id",
            "reserved_at",
        }:
            raise TransitionError("last_run must be null or a complete run record")
        if last_run["phase"] not in {"screening", "confirmation"}:
            raise TransitionError("last_run.phase must be screening or confirmation")
        for field in ("id", "candidate_id", "reserved_at"):
            if not isinstance(last_run[field], str) or not last_run[field]:
                raise TransitionError(f"last_run.{field} must be a non-empty string")
    evidence_id = state.get("promoted_evidence_id")
    if evidence_id is not None and (
        not isinstance(evidence_id, str) or not evidence_id.strip()
    ):
        raise TransitionError(
            "promoted_evidence_id must be null or a non-empty string"
        )
    if state["phase"] == "frozen" and evidence_id is None:
        raise TransitionError("frozen state requires promoted_evidence_id")
    pool = state.get("candidate_pool")
    rejected = state.get("rejected_candidates")
    if (
        not isinstance(pool, list)
        or any(not isinstance(item, str) or not item for item in pool)
        or len(pool) != len(set(pool))
        or len(pool) > 5
    ):
        raise TransitionError("candidate_pool must contain at most five unique ids")
    if (
        not isinstance(rejected, list)
        or any(not isinstance(item, str) or not item for item in rejected)
        or len(rejected) != len(set(rejected))
    ):
        raise TransitionError("rejected_candidates must contain unique ids")
    active = state.get("active_candidate_id")
    if active is not None and (not isinstance(active, str) or active not in pool):
        raise TransitionError("active_candidate_id must be null or present in candidate_pool")
    if state["phase"] in {"adaptation", "screening", "confirmation", "promotion"}:
        if active is None:
            raise TransitionError(f"phase {state['phase']} requires an active candidate")


def _mark_active_rejected(state: dict[str, Any]) -> None:
    active = state.get("active_candidate_id")
    if active and active not in state["rejected_candidates"]:
        state["rejected_candidates"].append(active)


def _transition(
    state: dict[str, Any],
    *,
    from_phase: str,
    to_phase: str,
    outcome: str,
    candidate_id: str | None,
    evidence_id: str | None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if from_phase not in PHASES or to_phase not in PHASES:
        raise TransitionError("from and to must be V4 pipeline phases")
    if state["phase"] != from_phase:
        raise TransitionError(
            f"state is in {state['phase']!r}, not requested --from {from_phase!r}"
        )
    allowed = TRANSITION_OUTCOMES.get((from_phase, to_phase))
    if allowed is None:
        raise TransitionError(f"illegal transition: {from_phase} -> {to_phase}")
    if outcome not in allowed:
        expected = ", ".join(sorted(allowed))
        raise TransitionError(
            f"outcome {outcome!r} is invalid for {from_phase} -> {to_phase}; "
            f"expected one of: {expected}"
        )

    next_state = copy.deepcopy(state)
    no_gain_before_refresh: int | None = None

    if (from_phase, to_phase) == ("mapping", "adaptation"):
        if not candidate_id:
            raise TransitionError("mapping -> adaptation requires --candidate-id")
        if candidate_id not in next_state["candidate_pool"]:
            raise TransitionError(
                "--candidate-id must be allocated by allocate-candidates"
            )
        if candidate_id in next_state["rejected_candidates"]:
            raise TransitionError(
                f"candidate {candidate_id!r} was already rejected; use a new revision id"
            )
        next_state["active_candidate_id"] = candidate_id
        next_state["last_run"] = None
    elif candidate_id is not None:
        raise TransitionError("--candidate-id applies only to mapping -> adaptation")

    if from_phase == "screening":
        next_state["screen_attempt"] += 1
    if from_phase == "confirmation":
        next_state["confirmation_attempt"] += 1

    if outcome in NO_GAIN_OUTCOMES:
        prospective_no_gain = next_state["consecutive_no_gain"] + 1
        if prospective_no_gain >= 2 and to_phase == "mapping":
            raise TransitionError(
                "two consecutive valid candidates showed no gain; route to literature"
            )
        next_state["consecutive_no_gain"] = prospective_no_gain
    elif outcome in {"screen_pass", "confirmed"}:
        next_state["consecutive_no_gain"] = 0

    if outcome in REJECTING_OUTCOMES:
        _mark_active_rejected(next_state)

    if to_phase in {"mapping", "literature"}:
        next_state["active_candidate_id"] = None
        next_state["last_run"] = None

    if to_phase == "literature":
        no_gain_before_refresh = next_state["consecutive_no_gain"]
        next_state["literature_revision"] += 1
        next_state["candidate_pool"] = []
        next_state["consecutive_no_gain"] = 0

    if (from_phase, to_phase) == ("promotion", "frozen"):
        resolved_evidence_id = (
            evidence_id.strip()
            if evidence_id and evidence_id.strip()
            else (
                f"evidence-{next_state['active_candidate_id']}-"
                f"c{next_state['confirmation_attempt']}"
            )
        )
        next_state["promoted_evidence_id"] = resolved_evidence_id
    elif evidence_id is not None:
        raise TransitionError("--evidence-id applies only to promotion -> frozen")
    else:
        resolved_evidence_id = None

    timestamp = _now()
    event: dict[str, Any] = {
        "ts": timestamp,
        "kind": "pipeline_transition",
        "from": from_phase,
        "to": to_phase,
        "outcome": outcome,
        "candidate_id": state.get("active_candidate_id")
        or next_state.get("active_candidate_id"),
        "evidence_id": resolved_evidence_id,
    }
    if no_gain_before_refresh is not None:
        event["consecutive_no_gain_before_refresh"] = no_gain_before_refresh

    next_state["phase"] = to_phase
    next_state["last_outcome"] = outcome
    next_state["last_transition"] = event
    _validate_state(next_state)
    return next_state, event


def _next_action(state: dict[str, Any]) -> dict[str, str] | None:
    """Return the handoff implied by a terminal research state."""
    if state["phase"] == "frozen" and state["deliverable"] == "paper":
        return {
            "skill": "paper-writing",
            "target_venue": state["target_venue"] or "venue-neutral",
        }
    return None


def _command_init(args: argparse.Namespace) -> int:
    path = _state_path(args.root)
    if path.exists():
        raise TransitionError(f"refusing to overwrite existing state: {path}")
    state = _new_state(
        entry_mode=args.entry_mode,
        deliverable=args.deliverable,
        target_venue=args.target_venue,
        objective=args.objective,
        primary_metric=args.primary_metric,
        metric_direction=args.metric_direction,
        target_delta=args.target_delta,
        baseline_run=args.baseline_run,
        baseline_artifact=args.baseline_artifact,
    )
    event = {
        "ts": _now(),
        "kind": "pipeline_initialized",
        "phase": "baseline",
        "entry_mode": state["entry_mode"],
        "deliverable": state["deliverable"],
        "objective": state["objective"],
        "primary_metric": state["primary_metric"],
        "target_delta": state["target_delta"],
    }
    _atomic_write_json(path, state)
    _append_event(_history_path(args.root), event)
    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0


def _command_migrate(args: argparse.Namespace) -> int:
    path = _state_path(args.root)
    if not path.is_file():
        raise TransitionError(f"missing legacy state: {path}")
    try:
        legacy = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise TransitionError(f"cannot read legacy state: {error}") from error
    if isinstance(legacy, dict) and legacy.get("mode_version") == MODE_VERSION:
        raise TransitionError("state is already V4")
    if isinstance(legacy, dict) and isinstance(legacy.get("mode_version"), int):
        backup = path.with_name(f"STATE.v{legacy['mode_version']}.json")
    else:
        backup = path.with_name("STATE.legacy.json")
    if backup.exists():
        raise TransitionError(f"legacy backup already exists: {backup}")
    if args.phase == "frozen" and not args.evidence_id:
        raise TransitionError("migrating to frozen requires --evidence-id")
    if args.phase != "frozen" and args.evidence_id is not None:
        raise TransitionError("--evidence-id applies only when migrating to frozen")
    pool = _parse_pool(args.candidate_pool)
    state = _new_state(
        entry_mode=args.entry_mode,
        deliverable=args.deliverable,
        target_venue=args.target_venue,
        objective=args.objective,
        primary_metric=args.primary_metric,
        metric_direction=args.metric_direction,
        target_delta=args.target_delta,
        baseline_run=args.baseline_run,
        baseline_artifact=args.baseline_artifact,
        phase=args.phase,
        candidate_id=args.candidate_id,
        candidate_pool=pool,
        promoted_evidence_id=args.evidence_id,
    )
    shutil.copyfile(path, backup)
    event = {
        "ts": _now(),
        "kind": "pipeline_migrated",
        "legacy_backup": str(backup),
        "phase": args.phase,
        "candidate_id": args.candidate_id,
        "entry_mode": state["entry_mode"],
        "deliverable": state["deliverable"],
    }
    state["last_transition"] = event
    _atomic_write_json(path, state)
    _append_event(_history_path(args.root), event)
    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0


def _command_show(args: argparse.Namespace) -> int:
    state = _load_state(args.root)
    output = copy.deepcopy(state)
    output["next_action"] = _next_action(state)
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


def _command_allocate_candidates(args: argparse.Namespace) -> int:
    state = _load_state(args.root)
    if state["phase"] != "mapping":
        raise TransitionError("candidate ids may be allocated only in mapping")
    if isinstance(args.count, bool) or not 1 <= args.count <= 5:
        raise TransitionError("--count must be between one and five")
    if len(state["candidate_pool"]) + args.count > 5:
        raise TransitionError("candidate pool may contain at most five ids")
    start = len(state["candidate_pool"]) + 1
    ids = [
        f"r{state['literature_revision']}-c{ordinal}"
        for ordinal in range(start, start + args.count)
    ]
    state["candidate_pool"].extend(ids)
    event = {
        "ts": _now(),
        "kind": "candidate_ids_allocated",
        "literature_revision": state["literature_revision"],
        "candidate_ids": ids,
    }
    state["last_transition"] = event
    _validate_state(state)
    _atomic_write_json(_state_path(args.root), state)
    _append_event(_history_path(args.root), event)
    print(
        json.dumps(
            {"candidate_ids": ids, "candidate_pool": state["candidate_pool"]},
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def _command_reserve_run(args: argparse.Namespace) -> int:
    state = _load_state(args.root)
    phase = state["phase"]
    if phase not in {"screening", "confirmation"}:
        raise TransitionError("runs may be reserved only in screening or confirmation")
    candidate_id = state["active_candidate_id"]
    if candidate_id is None:
        raise TransitionError(f"phase {phase} requires an active candidate")
    state["run_counters"][phase] += 1
    attempt = state["run_counters"][phase]
    label = "screen" if phase == "screening" else "confirm"
    run = {
        "id": f"{candidate_id}-{label}-a{attempt}",
        "phase": phase,
        "candidate_id": candidate_id,
        "reserved_at": _now(),
    }
    state["last_run"] = run
    event = {"ts": run["reserved_at"], "kind": "experiment_run_reserved", **run}
    state["last_transition"] = event
    _validate_state(state)
    _atomic_write_json(_state_path(args.root), state)
    _append_event(_history_path(args.root), event)
    print(json.dumps(run, ensure_ascii=False, indent=2))
    return 0


def _command_transition(args: argparse.Namespace, *, apply: bool) -> int:
    state = _load_state(args.root)
    next_state, event = _transition(
        state,
        from_phase=args.from_phase,
        to_phase=args.to_phase,
        outcome=args.outcome,
        candidate_id=args.candidate_id,
        evidence_id=args.evidence_id,
    )
    if apply:
        _atomic_write_json(_state_path(args.root), next_state)
        _append_event(_history_path(args.root), event)
    print(
        json.dumps(
            {
                "ok": True,
                "applied": apply,
                "phase": next_state["phase"],
                "outcome": next_state["last_outcome"],
                "active_candidate_id": next_state["active_candidate_id"],
                "consecutive_no_gain": next_state["consecutive_no_gain"],
                "literature_revision": next_state["literature_revision"],
                "evidence_id": event["evidence_id"],
                "last_run_id": (
                    next_state["last_run"]["id"]
                    if next_state["last_run"] is not None
                    else None
                ),
                "next_action": _next_action(next_state),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


def _add_baseline_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--entry-mode", choices=ENTRY_MODES, required=True)
    parser.add_argument("--deliverable", choices=DELIVERABLES, required=True)
    parser.add_argument("--target-venue")
    parser.add_argument("--objective", required=True)
    parser.add_argument("--primary-metric", required=True)
    parser.add_argument(
        "--metric-direction", choices=("higher", "lower"), required=True
    )
    parser.add_argument("--target-delta", required=True)
    parser.add_argument("--baseline-run", required=True)
    parser.add_argument("--baseline-artifact", required=True)


def _add_transition_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("root")
    parser.add_argument("--from", dest="from_phase", choices=PHASES, required=True)
    parser.add_argument("--to", dest="to_phase", choices=PHASES, required=True)
    parser.add_argument("--outcome", required=True)
    parser.add_argument("--candidate-id")
    parser.add_argument("--evidence-id")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="dsh_autoresearch V4 performance-pipeline guard"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="initialize V4 after baseline")
    init_parser.add_argument("root")
    _add_baseline_arguments(init_parser)

    migrate_parser = subparsers.add_parser(
        "migrate", help="replace a legacy state while preserving its versioned backup"
    )
    migrate_parser.add_argument("root")
    migrate_parser.add_argument("--phase", choices=PHASES, required=True)
    _add_baseline_arguments(migrate_parser)
    migrate_parser.add_argument("--candidate-id")
    migrate_parser.add_argument("--candidate-pool")
    migrate_parser.add_argument(
        "--evidence-id", help="required when migrating directly to frozen"
    )

    show_parser = subparsers.add_parser("show", help="show canonical V4 state")
    show_parser.add_argument("root")

    allocate_parser = subparsers.add_parser(
        "allocate-candidates", help="allocate stable candidate ids in mapping"
    )
    allocate_parser.add_argument("root")
    allocate_parser.add_argument("--count", type=int, required=True)

    reserve_parser = subparsers.add_parser(
        "reserve-run", help="reserve the next scientific experiment run id"
    )
    reserve_parser.add_argument("root")

    check_parser = subparsers.add_parser("check", help="validate without writing")
    _add_transition_arguments(check_parser)

    apply_parser = subparsers.add_parser("apply", help="validate and persist")
    _add_transition_arguments(apply_parser)
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    try:
        if args.command == "init":
            return _command_init(args)
        if args.command == "migrate":
            return _command_migrate(args)
        if args.command == "show":
            return _command_show(args)
        if args.command == "allocate-candidates":
            return _command_allocate_candidates(args)
        if args.command == "reserve-run":
            return _command_reserve_run(args)
        if args.command == "check":
            return _command_transition(args, apply=False)
        if args.command == "apply":
            return _command_transition(args, apply=True)
    except TransitionError as error:
        parser.error(str(error))
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
