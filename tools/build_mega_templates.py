#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from pypdf import PdfReader, PdfWriter


ROOT = Path(__file__).resolve().parents[1]
BUILD_DIR = ROOT / "build"
MEGA_DIR = BUILD_DIR / "mega"
UNIVERSAL_OFFSETS_MM = (
    (45, 75),
    (50, 80),
    (55, 85),
    (60, 90),
    (65, 95),
    (70, 100),
    (75, 105),
    (80, 110),
    (85, 115),
    (90, 120),
    (95, 125),
)
UNIVERSAL_MOUNTS = (
    ("c3", "comma three", False),
    ("c3x", "comma 3x", False),
    ("c4", "comma four", False),
    ("konik_batman", "Konik Batman", True),
    ("konik_quickmount", "Konik Quick Mount", True),
)
VEHICLE_MOUNTS = (
    ("c3", "comma three", 35),
    ("c3x", "comma 3x", 35),
    ("c4", "comma four", 44),
)
VEHICLE_VARIANT_OFFSETS_MM = (45, 50, 55, 60, 65)
VEHICLE_VARIANT_DIRS = ("2020_corolla", "2020_hyundai_santa_fe")


@dataclass(frozen=True)
class Render:
    pdf: Path
    png: Path
    body: str


def run_git(args: list[str], default: str = "") -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()
    except subprocess.CalledProcessError:
        return default


def git_url() -> str:
    url = run_git(["config", "--get", "remote.origin.url"])
    if url.startswith("git@github.com:"):
        url = "https://github.com/" + url.removeprefix("git@github.com:")
    if url.endswith(".git"):
        url = url.removesuffix(".git")
    return url


def typst_str(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def template_call(args: dict[str, str]) -> str:
    rendered = ", ".join(f"{key}: {value}" for key, value in args.items())
    return f"#template({rendered})"


def common_git_args() -> dict[str, str]:
    return {
        "repo-url": typst_str(git_url()),
        "commit-hash": typst_str(run_git(["rev-parse", "--short", "HEAD"])),
        "commit-date": typst_str(run_git(["log", "-1", "--format=%cd", "--date=short"])),
        "revision": typst_str(run_git(["rev-list", "--count", "HEAD"])),
    }


def universal_renders(paper: str) -> list[Render]:
    renders: list[Render] = []
    suffix = "a4" if paper == "a4" else "letter"
    git_args = common_git_args()

    for mount, label, is_konik in UNIVERSAL_MOUNTS:
        for primary, secondary in UNIVERSAL_OFFSETS_MM:
            stem = f"{mount}_mount_{primary}_{secondary}mm"
            args = {
                "mount-name": typst_str(
                    f"{label} (paired {primary}mm/{secondary}mm)"
                ),
                "footprint-label": typst_str(label),
                "svg-file": typst_str(f"build/{mount}_mount.svg"),
                "clearance-offset": f"{primary}mm",
                "secondary-clearance-offset": f"{secondary}mm",
                **git_args,
                "min-radius": "500mm",
                "top-padding": "2cm",
            }
            if paper == "a4":
                args["paper-size"] = typst_str("a4")
            if is_konik:
                args["feedback-community-url"] = typst_str("https://discord.gg/HCb2DbEKJD")
                args["feedback-community-label"] = typst_str("Konik Discord")
                args["feedback-community-channel"] = typst_str("")
            renders.append(
                Render(
                    pdf=BUILD_DIR / f"{stem}_{suffix}.pdf",
                    png=BUILD_DIR / f"{stem}_{suffix}.png",
                    body=template_call(args),
                )
            )
    return renders


def vehicle_dirs() -> list[str]:
    vehicles_root = ROOT / "vehicles"
    return sorted(path.name for path in vehicles_root.iterdir() if path.is_dir())


def vehicle_name(vehicle: str) -> str:
    return (ROOT / "vehicles" / vehicle / "name.txt").read_text().strip()


def vehicle_renders(paper: str) -> list[Render]:
    renders: list[Render] = []
    suffix = "a4" if paper == "a4" else "letter"
    git_args = common_git_args()

    for vehicle in vehicle_dirs():
        name = vehicle_name(vehicle)
        for mount, label, offset in VEHICLE_MOUNTS:
            stem = f"{mount}_mount"
            args = {
                "mount-name": typst_str(f"{label} ({name})"),
                "footprint-label": typst_str(label),
                "svg-file": typst_str(f"build/{mount}_mount.svg"),
                "clearance-offset": f"{offset}mm",
                "custom-clearance-svg": typst_str(f"/vehicles/{vehicle}/gen/offsets.svg"),
                **git_args,
                "min-radius": "500mm",
                "top-padding": "2cm",
            }
            if paper == "a4":
                args["paper-size"] = typst_str("a4")
            renders.append(
                Render(
                    pdf=BUILD_DIR / "vehicles" / vehicle / f"{stem}_{suffix}.pdf",
                    png=BUILD_DIR / "vehicles" / vehicle / f"{stem}_{suffix}.png",
                    body=template_call(args),
                )
            )

    for vehicle in VEHICLE_VARIANT_DIRS:
        name = vehicle_name(vehicle)
        for mount, label, _default_offset in VEHICLE_MOUNTS:
            for offset in VEHICLE_VARIANT_OFFSETS_MM:
                stem = f"{mount}_mount_{offset}mm"
                args = {
                    "mount-name": typst_str(f"{label} ({name})"),
                    "footprint-label": typst_str(label),
                    "svg-file": typst_str(f"build/{mount}_mount.svg"),
                    "clearance-offset": f"{offset}mm",
                    "custom-clearance-svg": typst_str(
                        f"/vehicles/{vehicle}/gen/offsets.svg"
                    ),
                    **git_args,
                    "min-radius": "500mm",
                    "top-padding": "2cm",
                }
                if paper == "a4":
                    args["paper-size"] = typst_str("a4")
                renders.append(
                    Render(
                        pdf=BUILD_DIR / "vehicles" / vehicle / f"{stem}_{suffix}.pdf",
                        png=BUILD_DIR / "vehicles" / vehicle / f"{stem}_{suffix}.png",
                        body=template_call(args),
                    )
                )
    return renders


def group_renders(group: str) -> list[Render]:
    if group == "universal-letter":
        return universal_renders("letter")
    if group == "universal-a4":
        return universal_renders("a4")
    if group == "vehicle-letter":
        return vehicle_renders("letter")
    if group == "vehicle-a4":
        return vehicle_renders("a4")
    raise ValueError(f"unknown group: {group}")


def group_stem(group: str) -> str:
    return group.replace("-", "_")


def write_typst(group: str, renders: list[Render]) -> Path:
    MEGA_DIR.mkdir(parents=True, exist_ok=True)
    typ_path = MEGA_DIR / f"{group_stem(group)}.typ"
    parts = ['#import "/template.typ": template', ""]
    for index, render in enumerate(renders):
        parts.append(render.body)
        if index != len(renders) - 1:
            parts.append("#pagebreak()")
        parts.append("")
    typ_path.write_text("\n".join(parts))
    return typ_path


def run(cmd: list[str]) -> None:
    print("+ " + " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


def split_pdf(mega_pdf: Path, renders: list[Render]) -> None:
    reader = PdfReader(mega_pdf)
    if len(reader.pages) != len(renders):
        raise RuntimeError(
            f"{mega_pdf} has {len(reader.pages)} pages, expected {len(renders)}"
        )
    for page, render in zip(reader.pages, renders, strict=True):
        render.pdf.parent.mkdir(parents=True, exist_ok=True)
        writer = PdfWriter()
        writer.add_page(page)
        with render.pdf.open("wb") as file:
            writer.write(file)


def move_png_pages(group: str, renders: list[Render]) -> None:
    for index, render in enumerate(renders, start=1):
        page_png = MEGA_DIR / f"{group_stem(group)}_page-{index}.png"
        if not page_png.exists():
            raise RuntimeError(f"missing Typst PNG page: {page_png}")
        render.png.parent.mkdir(parents=True, exist_ok=True)
        page_png.replace(render.png)


def touch_outputs(stamp: Path | None, renders: list[Render]) -> None:
    if stamp is not None:
        stamp.parent.mkdir(parents=True, exist_ok=True)
        stamp.touch()
    for render in renders:
        render.pdf.touch()
        render.png.touch()


def build_group(group: str, typst: str, ppi: int, stamp: Path | None) -> None:
    renders = group_renders(group)
    typ_path = write_typst(group, renders)
    mega_pdf = MEGA_DIR / f"{group_stem(group)}.pdf"
    png_pattern = MEGA_DIR / f"{group_stem(group)}_page-{{p}}.png"

    for stale_png in MEGA_DIR.glob(f"{group_stem(group)}_page-*.png"):
        stale_png.unlink()

    run([typst, "compile", str(typ_path), str(mega_pdf), "--root", ".", "--font-path", "fonts"])
    split_pdf(mega_pdf, renders)
    run(
        [
            typst,
            "compile",
            str(typ_path),
            str(png_pattern),
            "--root",
            ".",
            "--font-path",
            "fonts",
            "--ppi",
            str(ppi),
        ]
    )
    move_png_pages(group, renders)
    touch_outputs(stamp, renders)
    print(f"built_group={group} pages={len(renders)}")


def expected_outputs(groups: list[str]) -> list[Path]:
    outputs: list[Path] = []
    for group in groups:
        for render in group_renders(group):
            outputs.extend((render.pdf, render.png))
    return outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build grouped Typst template PDFs/PNGs.")
    parser.add_argument(
        "--group",
        dest="groups",
        action="append",
        choices=("universal-letter", "universal-a4", "vehicle-letter", "vehicle-a4"),
        required=True,
        help="Mega render group to build. May be repeated.",
    )
    parser.add_argument("--typst", default="typst")
    parser.add_argument("--ppi", type=int, default=144)
    parser.add_argument("--stamp", type=Path)
    parser.add_argument(
        "--list-outputs",
        action="store_true",
        help="Print expected output paths for the selected groups without building.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.list_outputs:
        for output in expected_outputs(args.groups):
            print(output.relative_to(ROOT))
        return 0

    stamp = args.stamp
    if stamp is not None and len(args.groups) != 1:
        print("--stamp can only be used with one --group", file=sys.stderr)
        return 2
    for group in args.groups:
        build_group(group, args.typst, args.ppi, stamp)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
