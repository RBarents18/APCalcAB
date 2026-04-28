# End-of-Year AP Calculus AB Review Workflow

## Purpose

Use assessment data collected throughout the year to shape a targeted, evidence-based AP Exam review plan. The goal is to maximize score improvement by focusing review time where class data shows the greatest need.

---

## Review Process

### Step 1: Aggregate Performance Data
Run `tools/analyze_results.py` to generate a skill-level performance summary across all assessments.

### Step 2: Update the Unit Priority Tracker
Update `review/unit_priority_tracker.csv` with current class averages and adjust priority levels based on the data.

### Step 3: Identify Class-Wide Weak Areas
Look for skills with class averages below 70%, especially in high AP weight categories (`exam_weight_category = Core` in `data/standards_map.csv`).

### Step 4: Identify Individual Student Weak Areas
Run `tools/generate_feedback.py` to create individual review plans in `review/student_review_plans/`.

### Step 5: Rank Review Topics by Urgency
Use the formula: **Urgency = low class performance + high AP exam weight**

### Step 6: Build Whole-Class Review Sessions
Plan 2–3 week review block sessions addressing:
- High-priority units (class avg < 70%, Core weight)
- Common FRQ formats and written justification practice
- Mixed-topic MCQ sets for pacing and retrieval

### Step 7: Build Targeted Small-Group or Individual Plans
Generate student-specific review plans using `tools/build_review_plan.py`.

### Step 8: Reassess and Adjust
After review sessions, re-assess on targeted skills and update `data/results.csv` with new data.

---

## Review Priority Categories

| Category | Criteria |
|----------|----------|
| **High Priority** | Class avg < 70% AND Core AP exam weight |
| **Medium Priority** | Class avg 70–80% OR Important AP weight with weak performance |
| **Maintenance** | Class avg > 80% — include in spiral review, not deep reteach |

---

## Suggested Review Sequence (Last 4 Weeks)

| Week | Focus |
|------|-------|
| Week 1 | High-priority units: limits, derivatives, integration |
| Week 2 | High-priority units: applications of derivatives, FTC |
| Week 3 | Medium-priority units: differential equations, area/volume |
| Week 4 | Mixed AP MCQ + FRQ practice, timed sections, test strategy |

---

## Suggested Output Files

- `review/class_review_reports/class-review-priority-[date].md` — overall class review plan
- `review/student_review_plans/review-plan-[student_id]-[date].md` — individual student plans

---

## Tools

| Script | Purpose |
|--------|---------|
| `tools/analyze_results.py` | Skill-level performance summary |
| `tools/generate_feedback.py` | Student and class feedback reports |
| `tools/build_review_plan.py` | Class and individual review priority lists |
