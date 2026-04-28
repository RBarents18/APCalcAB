# AP Calculus AB Master Repository

This repository supports instruction, assessment, student feedback, and AP Exam preparation for AP Calculus AB.

## Course Units

The repository is organized around the 8 official AP Calculus AB units:

| # | Unit |
|---|------|
| 1 | Limits and Continuity |
| 2 | Differentiation: Definition and Fundamental Properties |
| 3 | Differentiation: Composite, Implicit, and Inverse Functions |
| 4 | Contextual Applications of Differentiation |
| 5 | Analytical Applications of Differentiation |
| 6 | Integration and Accumulation of Change |
| 7 | Differential Equations |
| 8 | Applications of Integration |

## Repository Goals

- Organize curriculum materials by unit
- Store assessment metadata and student results
- Generate customized student feedback
- Identify growth areas by topic and skill
- Shape end-of-year AP review using class performance data
- Provide a structure that can absorb content migrated from Google Drive

## Folder Structure

```
APCalcAB/
├── README.md
├── curriculum/          # Unit-level instructional resources
│   ├── unit-01-limits-and-continuity/
│   ├── unit-02-differentiation-definition-and-fundamental-properties/
│   ├── unit-03-differentiation-composite-implicit-and-inverse-functions/
│   ├── unit-04-contextual-applications-of-differentiation/
│   ├── unit-05-analytical-applications-of-differentiation/
│   ├── unit-06-integration-and-accumulation-of-change/
│   ├── unit-07-differential-equations/
│   └── unit-08-applications-of-integration/
├── assessments/         # Quizzes, tests, FRQs, MCQs, rubrics
│   ├── quizzes/
│   ├── tests/
│   ├── frq/
│   ├── mcq/
│   └── rubrics/
├── data/                # CSVs for roster, assessments, questions, results
├── feedback/            # Feedback templates and generated reports
│   ├── templates/
│   └── generated/
├── review/              # AP Exam review planning materials
│   ├── student_review_plans/
│   └── class_review_reports/
├── tools/               # Python scripts for analysis and report generation
└── docs/                # Migration guides, naming conventions, inventory
```

## Main Sections

### `curriculum/`
Each unit folder contains four files:
- `overview.md` – unit description, major topics, AP Exam focus
- `objectives.md` – specific learning objectives aligned to the unit
- `skills.md` – AP skill categories and specific skills practiced
- `practice.md` – starter practice problems and activity ideas

### `assessments/`
Stores quizzes, tests, AP-style MCQs and FRQs, and scoring rubrics organized by subfolder.

### `data/`
Structured CSV files that power analysis and feedback:
- `students.csv` – student roster
- `assessments.csv` – assessment metadata
- `question_bank.csv` – question-to-skill mapping
- `results.csv` – per-question student performance
- `standards_map.csv` – topic/skill-to-unit and AP weight mapping

### `feedback/`
Templates and generated reports:
- `templates/` – reusable markdown templates for student and class reports
- `generated/` – output from `tools/generate_feedback.py`

### `review/`
AP Exam review planning:
- `overview.md` – review workflow and priority categories
- `unit_priority_tracker.csv` – class performance and priority by unit
- `student_review_plans/` – individual student review outputs
- `class_review_reports/` – whole-class summaries

### `tools/`
Python scripts that read CSVs and produce useful outputs:
- `analyze_results.py` – skill-level performance summary
- `generate_feedback.py` – per-student feedback reports
- `build_review_plan.py` – class review priority list

### `docs/`
Reference documents:
- `google-drive-migration-guide.md` – instructions for migrating Drive content here
- `master-content-inventory-template.csv` – template for cataloging existing materials
- `file-naming-conventions.md` – consistent naming rules for the whole repo

## Suggested Workflow

1. Add or update unit materials in `curriculum/`
2. Record assessment metadata in `data/assessments.csv`
3. Map each question to a skill in `data/question_bank.csv`
4. Import student scores into `data/results.csv`
5. Run `tools/analyze_results.py` to view skill-level performance
6. Run `tools/generate_feedback.py` to produce student reports in `feedback/generated/`
7. Run `tools/build_review_plan.py` to update `review/` priorities
8. Adjust instruction and AP review based on outputs

## Future Enhancements

- Automated performance dashboard
- Integration with Google Forms, Canvas, or AP Classroom exports
- Student-specific study packet generation
- Visual mastery tracking by unit and skill
