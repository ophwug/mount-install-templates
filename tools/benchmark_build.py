#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import time
from pathlib import Path

import build_mega_templates


ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> None:
    print("+ " + " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


def timed(cmd: list[str]) -> float:
    start = time.perf_counter()
    run(cmd)
    return time.perf_counter() - start


def groups_for_scope(scope: str) -> list[str]:
    groups = ["universal-letter", "universal-a4"]
    if scope == "all":
        groups.extend(["vehicle-letter", "vehicle-a4"])
    return groups


def make_target_for_scope(scope: str) -> str:
    return "universal-render" if scope == "universal" else "render-templates"


def expected_outputs(scope: str) -> list[Path]:
    return build_mega_templates.expected_outputs(groups_for_scope(scope))


def remove_render_outputs(scope: str) -> None:
    for output in expected_outputs(scope):
        output.unlink(missing_ok=True)
    shutil.rmtree(ROOT / "build" / "mega", ignore_errors=True)

    for typ in (ROOT / "build").glob("*_letter.typ"):
        typ.unlink(missing_ok=True)
    for typ in (ROOT / "build").glob("*_a4.typ"):
        typ.unlink(missing_ok=True)
    for typ in (ROOT / "build" / "vehicles").glob("*/*.typ"):
        typ.unlink(missing_ok=True)


def verify_outputs(scope: str) -> int:
    outputs = expected_outputs(scope)
    missing = [output for output in outputs if not output.exists()]
    if missing:
        sample = "\n".join(str(path.relative_to(ROOT)) for path in missing[:10])
        raise RuntimeError(f"missing {len(missing)} expected outputs:\n{sample}")
    return len(outputs)


def prebuild_shared_prereqs(scope: str, jobs: int) -> None:
    prereqs = [
        "build/c3_mount.svg",
        "build/c3x_mount.svg",
        "build/c4_mount.svg",
        "build/konik_batman_mount.svg",
        "build/konik_quickmount_mount.svg",
    ]
    if scope == "all":
        prereqs.extend(
            [
                "vehicles/2020_corolla/gen/offsets.svg",
                "vehicles/2020_hyundai_santa_fe/gen/offsets.svg",
            ]
        )
    run(["make", "-j", str(jobs), *prereqs])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare individual vs mega Typst builds.")
    parser.add_argument("--scope", choices=("universal", "all"), default="universal")
    parser.add_argument("--jobs", type=int, default=os.cpu_count() or 1)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = make_target_for_scope(args.scope)

    prebuild_shared_prereqs(args.scope, args.jobs)

    remove_render_outputs(args.scope)
    old_seconds = timed(["make", "-j", str(args.jobs), "INDIVIDUAL=1", target])
    old_count = verify_outputs(args.scope)

    remove_render_outputs(args.scope)
    new_seconds = timed(["make", "-j", str(args.jobs), target])
    new_count = verify_outputs(args.scope)

    if old_count != new_count:
        raise RuntimeError(f"old output count {old_count} != new output count {new_count}")

    speedup = old_seconds / new_seconds if new_seconds > 0 else float("inf")
    print(f"scope={args.scope}")
    print(f"jobs={args.jobs}")
    print(f"old_individual_seconds={old_seconds:.3f}")
    print(f"new_mega_seconds={new_seconds:.3f}")
    print(f"speedup={speedup:.2f}x")
    print(f"outputs_checked={new_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
