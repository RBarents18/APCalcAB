"""
generate_feedback.py
--------------------
Reads student results, question bank, and assessment metadata and
generates individual student feedback reports in feedback/generated/.

Usage:
    python tools/generate_feedback.py [--assessment ASSESSMENT_ID]

Options:
    --assessment   Limit output to a specific assessment ID (e.g., U1Q1).
                   If omitted, generates feedback for all assessments.

Output:
    Markdown feedback files in feedback/generated/student-reports/
    One class summary per assessment in feedback/generated/class-reports/
"""

import csv
import os
import sys
from collections import defaultdict
from datetime import date

RESULTS_FILE = os.path.join("data", "results.csv")
QUESTION_BANK_FILE = os.path.join("data", "question_bank.csv")
ASSESSMENTS_FILE = os.path.join("data", "assessments.csv")
STUDENTS_FILE = os.path.join("data", "students.csv")
STANDARDS_MAP_FILE = os.path.join("data", "standards_map.csv")
STUDENT_TEMPLATE_FILE = os.path.join("feedback", "templates", "student_feedback_template.md")
OUTPUT_STUDENT_DIR = os.path.join("feedback", "generated", "student-reports")
OUTPUT_CLASS_DIR = os.path.join("feedback", "generated", "class-reports")


def load_csv(filepath):
    """Load a CSV file into a list of dicts."""
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found.")
        return []
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def index_by(rows, key):
    """Return a dict mapping key field -> row for the first match."""
    return {row[key]: row for row in rows}


def group_by(rows, key):
    """Return a dict mapping key field -> list of rows."""
    groups = defaultdict(list)
    for row in rows:
        groups[row[key]].append(row)
    return groups


def compute_student_skill_summary(student_results, question_map):
    """
    Given a list of result rows for one student on one assessment,
    return a list of skill summary dicts.
    """
    skill_totals = defaultdict(lambda: {"earned": 0.0, "possible": 0.0})
    for row in student_results:
        qid = row["question_id"]
        if qid not in question_map:
            continue
        skill = question_map[qid]["skill"]
        skill_totals[skill]["earned"] += float(row["points_earned"])
        skill_totals[skill]["possible"] += float(row["max_points"])

    summary = []
    for skill, totals in sorted(skill_totals.items()):
        earned = totals["earned"]
        possible = totals["possible"]
        pct = (earned / possible * 100) if possible else 0.0
        summary.append({
            "skill": skill,
            "earned": earned,
            "possible": possible,
            "pct": pct,
        })
    return summary


def identify_strengths_and_gaps(skill_summary):
    """Return (strengths list, gaps list) based on percentage thresholds."""
    strengths = [s for s in skill_summary if s["pct"] >= 80]
    gaps = [s for s in skill_summary if s["pct"] < 70]
    return strengths, gaps


def format_skill_table(skill_summary):
    """Format a skill summary as a Markdown table."""
    lines = ["| Skill | Points Earned | Points Possible | Percent |",
             "|-------|--------------|-----------------|---------|"]
    for s in skill_summary:
        lines.append(
            f"| {s['skill']} | {s['earned']:.1f} | {s['possible']:.1f} | {s['pct']:.1f}% |"
        )
    return "\n".join(lines)


def generate_student_report(student, assessment, student_results, question_map, template):
    """Generate a feedback report string for one student on one assessment."""
    total_earned = sum(float(r["points_earned"]) for r in student_results)
    total_possible = sum(float(r["max_points"]) for r in student_results)
    pct = (total_earned / total_possible * 100) if total_possible else 0.0

    skill_summary = compute_student_skill_summary(student_results, question_map)
    strengths, gaps = identify_strengths_and_gaps(skill_summary)

    strengths_text = (
        "\n".join(f"- Strong performance on: {s['skill']} ({s['pct']:.1f}%)" for s in strengths)
        if strengths else "- No skills at 80%+ on this assessment yet."
    )
    gaps_text = (
        "\n".join(f"- Growth area: {s['skill']} ({s['pct']:.1f}%)" for s in gaps)
        if gaps else "- No skills below 70% on this assessment. Great work!"
    )
    next_steps = (
        "\n".join(f"- Review practice problems for: {s['skill']}" for s in gaps)
        if gaps else "- Continue practicing all skills to maintain proficiency."
    )

    report = template
    report = report.replace("{{student_id}}", student["student_id"])
    report = report.replace("{{student_name}}", f"{student['first_name']} {student['last_name']}")
    report = report.replace("{{section}}", student["section"])
    report = report.replace("{{assessment_title}}", assessment["title"])
    report = report.replace("{{assessment_date}}", assessment["date"])
    report = report.replace("{{score_earned}}", f"{total_earned:.1f}")
    report = report.replace("{{score_possible}}", assessment["total_points"])
    report = report.replace("{{percent}}", f"{pct:.1f}")
    report = report.replace("{{strengths}}", strengths_text)
    report = report.replace("{{growth_areas}}", gaps_text)
    report = report.replace("{{skill_breakdown_rows}}", format_skill_table(skill_summary))
    report = report.replace("{{next_steps}}", next_steps)
    report = report.replace("{{ap_exam_connection}}", f"Skills from Unit {assessment['unit']} appear regularly on both MCQ and FRQ sections of the AP Exam.")
    report = report.replace("{{teacher_notes}}", "")
    report = report.replace("{{generation_date}}", str(date.today()))

    return report


def generate_class_summary(assessment, assessment_results, question_map, students_map):
    """Generate a class summary report string for one assessment."""
    student_scores = defaultdict(lambda: {"earned": 0.0, "possible": 0.0})
    for row in assessment_results:
        sid = row["student_id"]
        student_scores[sid]["earned"] += float(row["points_earned"])
        student_scores[sid]["possible"] += float(row["max_points"])

    percentages = [
        (v["earned"] / v["possible"] * 100) if v["possible"] else 0.0
        for v in student_scores.values()
    ]

    if not percentages:
        return None

    class_avg = sum(percentages) / len(percentages)
    high = max(percentages)
    low = min(percentages)
    n = len(percentages)
    variance = sum((p - class_avg) ** 2 for p in percentages) / n
    std_dev = variance ** 0.5

    skill_totals = defaultdict(lambda: {"earned": 0.0, "possible": 0.0})
    for row in assessment_results:
        qid = row["question_id"]
        if qid not in question_map:
            continue
        skill = question_map[qid]["skill"]
        skill_totals[skill]["earned"] += float(row["points_earned"])
        skill_totals[skill]["possible"] += float(row["max_points"])

    skill_rows = []
    for skill, totals in sorted(skill_totals.items()):
        pct = (totals["earned"] / totals["possible"] * 100) if totals["possible"] else 0.0
        skill_rows.append({"skill": skill, "pct": pct})

    skill_rows.sort(key=lambda r: r["pct"])

    skill_table_lines = ["| Skill | Class Average (%) | Priority |",
                         "|-------|------------------|----------|"]
    for r in skill_rows:
        priority = "High" if r["pct"] < 70 else ("Medium" if r["pct"] < 85 else "Low")
        skill_table_lines.append(f"| {r['skill']} | {r['pct']:.1f}% | {priority} |")

    strengths = [r for r in skill_rows if r["pct"] >= 80]
    gaps = [r for r in skill_rows if r["pct"] < 70]

    strengths_text = "\n".join(f"- {r['skill']} ({r['pct']:.1f}%)" for r in strengths) or "- No skills at 80%+ class average."
    gaps_text = "\n".join(f"- {r['skill']} ({r['pct']:.1f}%)" for r in gaps) or "- No skills below 70% class average."

    report = f"""# Class Assessment Summary

## Assessment Information
- **Assessment:** {assessment['title']}
- **Unit:** {assessment['unit']}
- **Date:** {assessment['date']}
- **Number of Students:** {n}

---

## Class Performance Snapshot

| Metric | Value |
|--------|-------|
| Class Average | {class_avg:.1f}% |
| Highest Score | {high:.1f}% |
| Lowest Score | {low:.1f}% |
| Standard Deviation | {std_dev:.1f}% |

---

## Skill Performance Summary

{chr(10).join(skill_table_lines)}

---

## Strongest Skills

{strengths_text}

---

## Weakest Skills

{gaps_text}

---

## Recommended Instructional Responses

{"Re-teach the following skills before moving on: " + ", ".join(r['skill'] for r in gaps) if gaps else "Class performance is strong. Continue with pacing."}

---

## Review Implications for AP Exam Preparation

{"Skills below 70% should be included in AP review sessions: " + ", ".join(r['skill'] for r in gaps) if gaps else "No immediate review priorities from this assessment."}

---

*Generated by tools/generate_feedback.py | AP Calculus AB | {date.today()}*
"""
    return report


def main():
    filter_assessment = None
    if "--assessment" in sys.argv:
        idx = sys.argv.index("--assessment")
        if idx + 1 < len(sys.argv):
            filter_assessment = sys.argv[idx + 1]

    results = load_csv(RESULTS_FILE)
    questions = load_csv(QUESTION_BANK_FILE)
    assessments = load_csv(ASSESSMENTS_FILE)
    students = load_csv(STUDENTS_FILE)

    question_map = index_by(questions, "question_id")
    assessment_map = index_by(assessments, "assessment_id")
    students_map = index_by(students, "student_id")

    if not os.path.exists(STUDENT_TEMPLATE_FILE):
        print(f"Error: Template not found at {STUDENT_TEMPLATE_FILE}")
        return

    with open(STUDENT_TEMPLATE_FILE, encoding="utf-8") as f:
        template = f.read()

    os.makedirs(OUTPUT_STUDENT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_CLASS_DIR, exist_ok=True)

    results_by_assessment = group_by(results, "assessment_id")
    assessment_ids = (
        [filter_assessment] if filter_assessment else list(results_by_assessment.keys())
    )

    report_count = 0
    for aid in assessment_ids:
        if aid not in assessment_map:
            print(f"Warning: Assessment '{aid}' not found in assessments.csv. Skipping.")
            continue
        assessment = assessment_map[aid]
        assessment_results = results_by_assessment.get(aid, [])

        results_by_student = group_by(assessment_results, "student_id")
        for sid, student_results in results_by_student.items():
            if sid not in students_map:
                print(f"Warning: Student '{sid}' not found in students.csv. Skipping.")
                continue
            student = students_map[sid]
            report = generate_student_report(
                student, assessment, student_results, question_map, template
            )
            filename = f"feedback-{sid}-{aid}.md"
            filepath = os.path.join(OUTPUT_STUDENT_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(report)
            report_count += 1
            print(f"  [OK] {filepath}")

        class_report = generate_class_summary(
            assessment, assessment_results, question_map, students_map
        )
        if class_report:
            filename = f"class-summary-{aid}.md"
            filepath = os.path.join(OUTPUT_CLASS_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(class_report)
            print(f"  [OK] {filepath}")

    print(f"\nDone. Generated {report_count} student report(s).")


if __name__ == "__main__":
    main()
