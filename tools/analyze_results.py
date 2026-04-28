"""
analyze_results.py
------------------
Reads data/results.csv and data/question_bank.csv and prints a
skill-level performance summary for all recorded assessments.

Usage:
    python tools/analyze_results.py

Output:
    Prints a table of skills sorted by class average (ascending),
    making it easy to identify weak areas for review.
"""

import csv
import os
from collections import defaultdict

RESULTS_FILE = os.path.join("data", "results.csv")
QUESTION_BANK_FILE = os.path.join("data", "question_bank.csv")
STANDARDS_MAP_FILE = os.path.join("data", "standards_map.csv")


def load_question_bank(filepath):
    """Return a dict mapping question_id -> question row."""
    question_map = {}
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            question_map[row["question_id"]] = row
    return question_map


def load_standards_map(filepath):
    """Return a dict mapping (topic, skill) -> exam_weight_category and review_priority."""
    standards = {}
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            key = (row["topic"], row["skill"])
            standards[key] = {
                "exam_weight_category": row["exam_weight_category"],
                "review_priority": row["review_priority"],
            }
    return standards


def compute_skill_totals(results_filepath, question_map):
    """
    Aggregate points earned and possible by skill across all results.
    Returns a dict: skill -> {earned, possible, topic}.
    """
    skill_totals = defaultdict(lambda: {"earned": 0.0, "possible": 0.0, "topic": ""})

    with open(results_filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            qid = row["question_id"]
            if qid not in question_map:
                continue
            q = question_map[qid]
            skill = q["skill"]
            skill_totals[skill]["earned"] += float(row["points_earned"])
            skill_totals[skill]["possible"] += float(row["max_points"])
            skill_totals[skill]["topic"] = q["topic"]

    return skill_totals


def print_skill_summary(skill_totals, standards):
    """Print a formatted skill performance table sorted by percent ascending."""
    rows = []
    for skill, totals in skill_totals.items():
        earned = totals["earned"]
        possible = totals["possible"]
        pct = (earned / possible * 100) if possible else 0.0
        topic = totals["topic"]
        meta = standards.get((topic, skill), {})
        rows.append({
            "skill": skill,
            "topic": topic,
            "earned": earned,
            "possible": possible,
            "pct": pct,
            "weight": meta.get("exam_weight_category", "Unknown"),
            "priority": meta.get("review_priority", "Unknown"),
        })

    rows.sort(key=lambda r: r["pct"])

    print("=" * 90)
    print(f"{'SKILL PERFORMANCE SUMMARY':^90}")
    print("=" * 90)
    print(f"{'Skill':<50} {'Pct':>6}  {'Weight':<12} {'Priority':<8}")
    print("-" * 90)

    for r in rows:
        flag = " <-- REVIEW" if r["pct"] < 70 and r["weight"] == "Core" else ""
        print(
            f"{r['skill'][:49]:<50} {r['pct']:>5.1f}%  {r['weight']:<12} {r['priority']:<8}{flag}"
        )

    print("=" * 90)
    print(f"\nTotal skills tracked: {len(rows)}")

    weak = [r for r in rows if r["pct"] < 70]
    if weak:
        print(f"\nSkills below 70% ({len(weak)}):")
        for r in weak:
            print(f"  - {r['skill']} ({r['pct']:.1f}%) [{r['weight']}]")
    else:
        print("\nNo skills below 70%. Strong overall performance!")


def main():
    if not os.path.exists(RESULTS_FILE):
        print(f"Error: {RESULTS_FILE} not found. Add student results first.")
        return
    if not os.path.exists(QUESTION_BANK_FILE):
        print(f"Error: {QUESTION_BANK_FILE} not found.")
        return

    question_map = load_question_bank(QUESTION_BANK_FILE)
    standards = load_standards_map(STANDARDS_MAP_FILE) if os.path.exists(STANDARDS_MAP_FILE) else {}
    skill_totals = compute_skill_totals(RESULTS_FILE, question_map)

    if not skill_totals:
        print("No skill data found. Check that results.csv has matching question IDs.")
        return

    print_skill_summary(skill_totals, standards)


if __name__ == "__main__":
    main()
