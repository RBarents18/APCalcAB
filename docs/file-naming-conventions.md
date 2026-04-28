# File Naming Conventions

This document defines the naming conventions used throughout the AP Calculus AB repository. Consistent naming makes files easy to find, sort, and reference in scripts.

---

## General Principles

1. Use **lowercase** for all file and folder names.
2. Use **hyphens** (`-`) to separate words, not underscores or spaces.
3. Keep names **descriptive but concise**.
4. Include **unit numbers** with two digits (e.g., `unit01`, not `unit1`).
5. Include **dates** in ISO format (`YYYY-MM-DD`) when relevant.
6. Use standard file extensions: `.md`, `.csv`, `.py`, `.pdf`, `.docx`.

---

## Folder Naming

| Folder | Convention | Example |
|--------|-----------|---------|
| Curriculum units | `unit##-[slug]` | `unit-01-limits-and-continuity` |
| Assessment subfolders | short descriptive names | `quizzes`, `tests`, `frq`, `mcq`, `rubrics` |
| Data files | descriptive noun | `students`, `results`, `question_bank` |
| Feedback subfolders | `templates`, `generated` | as-is |
| Review subfolders | descriptive noun | `student_review_plans`, `class_review_reports` |

---

## Curriculum Files

Each unit folder contains these four files with exact names:

| File | Purpose |
|------|---------|
| `overview.md` | Unit description and major topics |
| `objectives.md` | Specific learning objectives |
| `skills.md` | AP skill categories and key vocabulary |
| `practice.md` | Practice problems and activity ideas |

---

## Assessment Files

### Quizzes
`unit##-quiz##-[short-title].[ext]`

| Field | Description |
|-------|-------------|
| `unit##` | Two-digit unit number (e.g., `unit01`) |
| `quiz##` | Two-digit quiz number within the unit |
| `[short-title]` | 1–3 hyphenated words describing the content |

**Examples:**
- `unit01-quiz01-limits-intro.pdf`
- `unit03-quiz02-chain-rule.docx`
- `unit06-quiz01-riemann-sums.pdf`

### Tests
`unit##-test##-[short-title].[ext]`

**Examples:**
- `unit02-test01-differentiation-fundamentals.pdf`
- `unit05-test01-analytical-applications.pdf`

### FRQ Sets
`frq-[unit-or-topic]-[YYYY-MM].[ext]`

**Examples:**
- `frq-unit07-slope-fields-2026-11.pdf`
- `frq-ap-review-set01-2027-04.pdf`

### MCQ Sets
`mcq-[unit-or-topic]-[YYYY-MM].[ext]`

**Examples:**
- `mcq-unit01-limits-2026-09.pdf`
- `mcq-ap-review-full-2027-04.pdf`

### Rubrics
`rubric-[assessment-id]-[short-title].[ext]`

**Examples:**
- `rubric-U1Q1-limits-quiz.pdf`
- `rubric-U7FRQ1-slope-fields.pdf`

---

## Data Files

Data files use descriptive snake_case names (underscores are acceptable for CSV data files to distinguish from folder/doc names).

| File | Naming |
|------|--------|
| Student roster | `students.csv` |
| Assessment metadata | `assessments.csv` |
| Question bank | `question_bank.csv` |
| Student results | `results.csv` |
| Standards/skill map | `standards_map.csv` |

---

## Generated Feedback Files

| Type | Convention | Example |
|------|-----------|---------|
| Student report | `feedback-[student_id]-[assessment_id].md` | `feedback-1001-U1Q1.md` |
| Class summary | `class-summary-[assessment_id].md` | `class-summary-U1Q1.md` |

---

## Generated Review Files

| Type | Convention | Example |
|------|-----------|---------|
| Class review plan | `class-review-priority-[YYYY-MM-DD].md` | `class-review-priority-2027-04-22.md` |
| Student review plan | `review-plan-[student_id]-[YYYY-MM-DD].md` | `review-plan-1001-2027-04-22.md` |

---

## Assessment IDs (for `data/assessments.csv`)

Use a short code combining unit and assessment type:

| Format | Example | Meaning |
|--------|---------|---------|
| `U#Q#` | `U1Q1` | Unit 1, Quiz 1 |
| `U#T#` | `U2T1` | Unit 2, Test 1 |
| `U#FRQ#` | `U7FRQ1` | Unit 7, FRQ Set 1 |
| `APREV#` | `APREV1` | AP Review Set 1 |

---

## Notes

- When migrating files from Google Drive, rename them to follow these conventions before committing.
- Use `docs/master-content-inventory-template.csv` to track files and their target paths during migration.
