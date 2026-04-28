"""
build_review_plan.py
--------------------
Reads performance data and generates a class-wide AP Exam review
priority plan and individual student review plans.

Usage:
    python tools/build_review_plan.py

Output:
    review/class_review_reports/class-review-priority-[date].md
    review/student_review_plans/review-plan-[student_id]-[date].md
"""

import csv
import os
from collections import defaultdict
from datetime import date

RESULTS_FILE = os.path.join("data", "results.csv")
QUESTION_BANK_FILE = os.path.join("data", "question_bank.csv")
STANDARDS_MAP_FILE = os.path.join("data", "standards_map.csv")
STUDENTS_FILE = os.path.join("data", "students.csv")
UNIT_TRACKER_FILE = os.path.join("review", "unit_priority_tracker.csv")
OUTPUT_CLASS_DIR = os.path.join("review", "class_review_reports")
OUTPUT_STUDENT_DIR = os.path.join("review", "student_review_plans")

TODAY = str(date.today())


def load_csv(filepath):
    """Load a CSV file into a list of dicts."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def index_by(rows, key):
    """Return a dict mapping key field -> row."""
    return {row[key]: row for row in rows}


def compute_class_skill_averages(results, question_map, standards_map):
    """
    Compute class-level average percentage per skill.
    Returns a list of dicts sorted by pct ascending.
    """
    skill_totals = defaultdict(lambda: {"earned": 0.0, "possible": 0.0, "topic": "", "unit": ""})

    for row in results:
        qid = row["question_id"]
        if qid not in question_map:
            continue
        q = question_map[qid]
        skill = q["skill"]
        skill_totals[skill]["earned"] += float(row["points_earned"])
        skill_totals[skill]["possible"] += float(row["max_points"])
        skill_totals[skill]["topic"] = q["topic"]

    output = []
    for skill, totals in skill_totals.items():
        pct = (totals["earned"] / totals["possible"] * 100) if totals["possible"] else 0.0
        topic = totals["topic"]
        meta = standards_map.get((topic, skill), {})
        output.append({
            "skill": skill,
            "topic": topic,
            "pct": pct,
            "weight": meta.get("exam_weight_category", "Unknown"),
            "unit": meta.get("unit", "?"),
            "review_priority": meta.get("review_priority", "Unknown"),
        })

    output.sort(key=lambda r: r["pct"])
    return output


def compute_student_skill_averages(results, question_map):
    """
    Compute per-student skill averages.
    Returns a dict: student_id -> list of skill dicts.
    """
    student_skill = defaultdict(lambda: defaultdict(lambda: {"earned": 0.0, "possible": 0.0, "topic": ""}))

    for row in results:
        qid = row["question_id"]
        sid = row["student_id"]
        if qid not in question_map:
            continue
        skill = question_map[qid]["skill"]
        student_skill[sid][skill]["earned"] += float(row["points_earned"])
        student_skill[sid][skill]["possible"] += float(row["max_points"])
        student_skill[sid][skill]["topic"] = question_map[qid]["topic"]

    output = {}
    for sid, skills in student_skill.items():
        skill_list = []
        for skill, totals in skills.items():
            pct = (totals["earned"] / totals["possible"] * 100) if totals["possible"] else 0.0
            skill_list.append({
                "skill": skill,
                "topic": totals["topic"],
                "pct": pct,
            })
        skill_list.sort(key=lambda r: r["pct"])
        output[sid] = skill_list
    return output


def write_class_review_plan(class_skills):
    """Write the class review priority plan markdown file."""
    high = [s for s in class_skills if s["pct"] < 70 and s["weight"] in ("Core", "Foundational")]
    medium = [s for s in class_skills if 70 <= s["pct"] < 80 or (s["pct"] < 70 and s["weight"] == "Important")]
    maintenance = [s for s in class_skills if s["pct"] >= 80]

    lines = [
        f"# Class AP Review Priority Plan",
        f"",
        f"**Generated:** {TODAY}",
        f"**Data source:** data/results.csv",
        f"",
        f"---",
        f"",
        f"## High Priority — Reteach Before AP Exam",
        f"",
        f"These skills had class averages below 70% with Core or Foundational AP weight.",
        f"",
    ]

    if high:
        lines.append("| Skill | Topic | Class Avg | AP Weight |")
        lines.append("|-------|-------|-----------|-----------|")
        for s in high:
            lines.append(f"| {s['skill']} | {s['topic']} | {s['pct']:.1f}% | {s['weight']} |")
    else:
        lines.append("*No high-priority skills identified — class average above 70% on all Core skills.*")

    lines += [
        "",
        "---",
        "",
        "## Medium Priority — Targeted Review",
        "",
        "These skills had class averages between 70–80% or lower performance on Important-weight skills.",
        "",
    ]

    if medium:
        lines.append("| Skill | Topic | Class Avg | AP Weight |")
        lines.append("|-------|-------|-----------|-----------|")
        for s in medium:
            lines.append(f"| {s['skill']} | {s['topic']} | {s['pct']:.1f}% | {s['weight']} |")
    else:
        lines.append("*No medium-priority skills identified.*")

    lines += [
        "",
        "---",
        "",
        "## Maintenance — Spiral Review",
        "",
        "These skills had class averages at or above 80%. Include in spiral review but not deep reteach.",
        "",
    ]

    if maintenance:
        lines.append("| Skill | Topic | Class Avg |")
        lines.append("|-------|-------|-----------|")
        for s in maintenance:
            lines.append(f"| {s['skill']} | {s['topic']} | {s['pct']:.1f}% |")
    else:
        lines.append("*No skills at maintenance level yet.*")

    lines += [
        "",
        "---",
        "",
        "## Suggested 4-Week Review Schedule",
        "",
        "| Week | Focus |",
        "|------|-------|",
        "| Week 1 | High-priority skills — reteach and collaborative practice |",
        "| Week 2 | High-priority skills continued + medium-priority skills |",
        "| Week 3 | Mixed MCQ and FRQ practice across all units |",
        "| Week 4 | Timed AP practice sections, test strategy, and final review |",
        "",
        "---",
        "",
        f"*Run `python tools/build_review_plan.py` again after updating data/results.csv.*",
    ]

    os.makedirs(OUTPUT_CLASS_DIR, exist_ok=True)
    filename = f"class-review-priority-{TODAY}.md"
    filepath = os.path.join(OUTPUT_CLASS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  [OK] {filepath}")
    return filepath


def write_student_review_plan(student, skill_list, students_map):
    """Write a student-specific review plan markdown file."""
    sid = student["student_id"]
    name = f"{student['first_name']} {student['last_name']}"

    gaps = [s for s in skill_list if s["pct"] < 70]
    strengths = [s for s in skill_list if s["pct"] >= 80]

    lines = [
        f"# AP Review Plan — {name}",
        f"",
        f"**Student ID:** {sid}",
        f"**Section:** {student['section']}",
        f"**Generated:** {TODAY}",
        f"",
        f"---",
        f"",
        f"## Your Strengths",
        f"",
    ]

    if strengths:
        for s in strengths:
            lines.append(f"- {s['skill']} ({s['pct']:.1f}%) — keep it up!")
    else:
        lines.append("- No skills at 80%+ yet. Keep practicing!")

    lines += [
        "",
        "---",
        "",
        "## Priority Review Areas",
        "",
        "Focus your AP review time on these skills first:",
        "",
    ]

    if gaps:
        for i, s in enumerate(gaps, 1):
            lines.append(f"### {i}. {s['skill']}")
            lines.append(f"- **Topic:** {s['topic']}")
            lines.append(f"- **Your Average:** {s['pct']:.1f}%")
            lines.append(f"- **Action:** Review `curriculum/` unit materials and complete practice problems for this skill.")
            lines.append("")
    else:
        lines.append("*No skills below 70%. Great work! Focus on timed practice and written justification.*")

    lines += [
        "---",
        "",
        "## General AP Exam Tips",
        "",
        "- Always show your work on FRQ questions — partial credit is available.",
        "- Write complete justification sentences when asked to 'justify' or 'explain'.",
        "- Check units on all contextual problems.",
        "- For limits and continuity: know the three-part definition of continuity.",
        "- For integration: make sure your setup is correct before evaluating.",
        "",
        "---",
        "",
        f"*Generated by tools/build_review_plan.py | AP Calculus AB | {TODAY}*",
    ]

    os.makedirs(OUTPUT_STUDENT_DIR, exist_ok=True)
    filename = f"review-plan-{sid}-{TODAY}.md"
    filepath = os.path.join(OUTPUT_STUDENT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  [OK] {filepath}")


def main():
    results = load_csv(RESULTS_FILE)
    questions = load_csv(QUESTION_BANK_FILE)
    standards_rows = load_csv(STANDARDS_MAP_FILE)
    students = load_csv(STUDENTS_FILE)

    if not results:
        print("No results found in data/results.csv. Add student data first.")
        return

    question_map = index_by(questions, "question_id")
    students_map = index_by(students, "student_id")

    standards_map = {}
    for row in standards_rows:
        key = (row["topic"], row["skill"])
        standards_map[key] = row

    print("Building class review plan...")
    class_skills = compute_class_skill_averages(results, question_map, standards_map)
    write_class_review_plan(class_skills)

    print("\nBuilding student review plans...")
    student_skills = compute_student_skill_averages(results, question_map)
    for sid, skill_list in student_skills.items():
        if sid not in students_map:
            print(f"Warning: Student {sid} not in students.csv. Skipping.")
            continue
        write_student_review_plan(students_map[sid], skill_list, students_map)

    print(f"\nDone. Review plans written to {OUTPUT_CLASS_DIR}/ and {OUTPUT_STUDENT_DIR}/")


if __name__ == "__main__":
    main()
