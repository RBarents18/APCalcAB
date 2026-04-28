#!/usr/bin/env python3
"""
tools/export_site_data.py
=========================
Reads existing repository CSV/markdown data and writes starter JSON files
into site/data/ for use by the static HTML course hub.

Outputs:
  site/data/units.json            – unit metadata from review/unit_priority_tracker.csv
  site/data/review-priorities.json – skill priorities from data/standards_map.csv

Run from the repository root:
    python tools/export_site_data.py

No third-party dependencies required (stdlib only).
"""

import csv
import json
import os
import sys
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR  = REPO_ROOT / "data"
REVIEW_DIR = REPO_ROOT / "review"
SITE_DATA_DIR = REPO_ROOT / "site" / "data"

STANDARDS_MAP_FILE    = DATA_DIR / "standards_map.csv"
UNIT_TRACKER_FILE     = REVIEW_DIR / "unit_priority_tracker.csv"


# ── Unit metadata (hard-coded for robustness; matches curriculum folders) ──
UNIT_META = {
    1: {
        "slug": "unit-01-limits-and-continuity",
        "name": "Limits and Continuity",
        "description": (
            "Students explore how limits allow us to understand function behavior "
            "near a point and at infinity, building the conceptual foundation for "
            "all of calculus."
        ),
        "exam_weight_category": "Foundational",
        "key_skills": [
            "Estimate limits from graphs, tables & equations",
            "Evaluate one-sided and infinite limits",
            "Determine continuity at a point and on an interval",
            "Classify discontinuities",
            "Apply the Intermediate Value Theorem",
        ],
    },
    2: {
        "slug": "unit-02-differentiation-definition-and-fundamental-properties",
        "name": "Differentiation: Definition and Fundamental Properties",
        "description": (
            "Students apply limits to define the derivative and develop fluency "
            "with basic differentiation rules across multiple representations."
        ),
        "exam_weight_category": "Core",
        "key_skills": [
            "Define and interpret the derivative as a rate of change",
            "Apply power, product, and quotient rules",
            "Differentiate trig, exponential & logarithmic functions",
            "Determine differentiability and connect to continuity",
            "Write equations of tangent lines",
        ],
    },
    3: {
        "slug": "unit-03-differentiation-composite-implicit-and-inverse-functions",
        "name": "Differentiation: Composite, Implicit, and Inverse Functions",
        "description": (
            "Students master the chain rule, implicit differentiation, and "
            "derivatives of inverse functions, including higher-order derivatives."
        ),
        "exam_weight_category": "Core",
        "key_skills": [
            "Apply the chain rule to composite functions",
            "Use implicit differentiation",
            "Find derivatives of inverse and inverse trig functions",
            "Compute higher-order derivatives",
        ],
    },
    4: {
        "slug": "unit-04-contextual-applications-of-differentiation",
        "name": "Contextual Applications of Differentiation",
        "description": (
            "Students apply derivatives to model and solve real-world problems "
            "involving rates of change, motion, and approximation."
        ),
        "exam_weight_category": "Core",
        "key_skills": [
            "Interpret derivatives in applied contexts",
            "Model velocity and acceleration",
            "Set up and solve related rates problems",
            "Use linearization to approximate values",
            "Apply L'Hôpital's Rule",
        ],
    },
    5: {
        "slug": "unit-05-analytical-applications-of-differentiation",
        "name": "Analytical Applications of Differentiation",
        "description": (
            "Students analyze relationships among a function and its derivatives "
            "to solve optimization problems and justify conclusions about behavior."
        ),
        "exam_weight_category": "Core",
        "key_skills": [
            "Apply the Mean Value Theorem",
            "Determine intervals of increase/decrease and critical points",
            "Use first and second derivative tests",
            "Determine concavity and locate inflection points",
            "Solve applied optimization problems",
        ],
    },
    6: {
        "slug": "unit-06-integration-and-accumulation-of-change",
        "name": "Integration and Accumulation of Change",
        "description": (
            "Students apply limits to define definite integrals and discover how "
            "the Fundamental Theorem of Calculus connects differentiation and integration."
        ),
        "exam_weight_category": "Core",
        "key_skills": [
            "Compute and interpret Riemann sums",
            "Evaluate definite integrals",
            "Apply both parts of the Fundamental Theorem of Calculus",
            "Find antiderivatives using u-substitution",
            "Interpret definite integrals in context",
        ],
    },
    7: {
        "slug": "unit-07-differential-equations",
        "name": "Differential Equations",
        "description": (
            "Students solve differential equations and apply them to model "
            "exponential growth, decay, and other real-world phenomena."
        ),
        "exam_weight_category": "Important",
        "key_skills": [
            "Interpret and sketch slope fields",
            "Approximate solutions using Euler's method",
            "Solve separable differential equations",
            "Model exponential growth and decay",
        ],
    },
    8: {
        "slug": "unit-08-applications-of-integration",
        "name": "Applications of Integration",
        "description": (
            "Students use integration to solve problems involving net change, "
            "area between curves, and volumes of 3-D solids."
        ),
        "exam_weight_category": "Core",
        "key_skills": [
            "Find the average value of a function",
            "Analyze particle motion using integrals",
            "Calculate area between curves",
            "Find volume using disk and washer methods",
            "Find volume using known cross-section shapes",
        ],
    },
}


# ── Helpers ────────────────────────────────────────────────────────────

def load_csv(path: Path) -> list[dict]:
    """Read a CSV file and return a list of row dicts. Returns [] if missing."""
    if not path.exists():
        print(f"  [warn] File not found: {path}", file=sys.stderr)
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  [ok] Wrote {path.relative_to(REPO_ROOT)}")


# ── Export: units.json ─────────────────────────────────────────────────

def export_units() -> None:
    tracker_rows = load_csv(UNIT_TRACKER_FILE)

    # Build lookup from tracker CSV  (unit number → row)
    tracker_map: dict[int, dict] = {}
    for row in tracker_rows:
        try:
            unit_num = int(row.get("unit", 0))
            tracker_map[unit_num] = row
        except ValueError:
            pass

    units_out = []
    for num in range(1, 9):
        meta  = UNIT_META[num]
        track = tracker_map.get(num, {})

        try:
            avg_pct = float(track.get("class_average_pct", 0))
        except ValueError:
            avg_pct = 0.0

        units_out.append({
            "unit":                 num,
            "slug":                 meta["slug"],
            "name":                 meta["name"],
            "description":          meta["description"],
            "exam_weight_category": track.get("exam_weight_category") or meta["exam_weight_category"],
            "priority_level":       track.get("priority_level", "High"),
            "class_average_pct":    avg_pct,
            "notes":                track.get("notes", ""),
            "key_skills":           meta["key_skills"],
        })

    write_json(SITE_DATA_DIR / "units.json", {"units": units_out})


# ── Export: review-priorities.json ────────────────────────────────────

def export_review_priorities() -> None:
    standards_rows = load_csv(STANDARDS_MAP_FILE)

    skills_out = []
    for row in standards_rows:
        try:
            unit_num = int(row.get("unit", 0))
        except ValueError:
            unit_num = 0

        skills_out.append({
            "unit":               unit_num,
            "topic":              row.get("topic", ""),
            "skill":              row.get("skill", ""),
            "exam_weight_category": row.get("exam_weight_category", ""),
            "review_priority":    row.get("review_priority", ""),
        })

    # Group counts for the summary field
    from collections import Counter
    counts = Counter(s["review_priority"] for s in skills_out)

    write_json(
        SITE_DATA_DIR / "review-priorities.json",
        {
            "generated_from": "data/standards_map.csv",
            "summary": {
                "High":   counts.get("High",   0),
                "Medium": counts.get("Medium", 0),
                "Low":    counts.get("Low",    0),
            },
            "skills": skills_out,
        },
    )


# ── Main ───────────────────────────────────────────────────────────────

def main() -> None:
    print("AP Calculus AB — Site Data Export")
    print(f"  Source root : {REPO_ROOT}")
    print(f"  Output dir  : {SITE_DATA_DIR}")
    print()

    SITE_DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Exporting units.json …")
    export_units()

    print("Exporting review-priorities.json …")
    export_review_priorities()

    print()
    print("Done. Reload site/review.html to see live data.")


if __name__ == "__main__":
    main()
