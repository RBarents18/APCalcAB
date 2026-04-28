# Google Drive Migration Guide

This guide explains how to migrate existing AP Calculus AB materials from Google Drive into this repository.

---

## Overview

Many teachers store curriculum materials, assessments, and student resources in Google Drive. This guide helps you systematically move that content into the structured repository so that everything is organized, versioned, and searchable.

---

## Step 1: Inventory Your Google Drive Content

Before migrating, catalog what you have. Use the template in `docs/master-content-inventory-template.csv` to list all files and folders in your Drive.

For each file, record:
- File name
- File type (Google Doc, Google Sheet, PDF, etc.)
- Topic or unit it belongs to
- Current Drive folder path
- Target repository path (where it should go)
- Notes on any updates needed

---

## Step 2: Identify the Right Repository Folder

Use this mapping to determine where each file belongs:

| Content Type | Repository Location |
|---|---|
| Lesson notes, overviews, objectives | `curriculum/unit-##-[name]/` |
| Practice problems | `curriculum/unit-##-[name]/practice.md` |
| Quizzes | `assessments/quizzes/` |
| Tests | `assessments/tests/` |
| AP FRQ sets | `assessments/frq/` |
| AP MCQ sets | `assessments/mcq/` |
| Scoring rubrics | `assessments/rubrics/` |
| Student roster data | `data/students.csv` |
| Assessment results | `data/results.csv` |
| Feedback templates | `feedback/templates/` |
| Review planning materials | `review/` |

---

## Step 3: Export and Convert Files

### Google Docs → Markdown
1. Open the Google Doc.
2. Go to **File → Download → Plain Text (.txt)**.
3. Copy the text into a new `.md` file in the appropriate repository folder.
4. Add Markdown formatting (headings, bold, lists) as needed.

### Google Sheets → CSV
1. Open the Google Sheet.
2. Go to **File → Download → Comma Separated Values (.csv)**.
3. Save the file into the appropriate `data/` path or replace the starter CSV.

### Google Slides → PDF
1. Open the Google Slides presentation.
2. Go to **File → Download → PDF Document (.pdf)**.
3. Save the PDF into the appropriate `curriculum/` or `assessments/` subfolder.

---

## Step 4: Apply the File Naming Convention

Rename files to follow the conventions in `docs/file-naming-conventions.md` before committing.

**Examples:**
- `unit01-quiz01-limits-intro.pdf`
- `unit03-notes-chain-rule.md`
- `frq-unit07-slope-fields-2026-11.pdf`

---

## Step 5: Update Data CSVs

If you have student data in Google Sheets, export and merge it into:
- `data/students.csv` — roster information
- `data/assessments.csv` — assessment metadata
- `data/question_bank.csv` — question-to-skill mapping
- `data/results.csv` — student scores

See each CSV file for the expected column structure.

---

## Step 6: Commit and Push

Once files are in place:

```bash
git add .
git commit -m "Migrate [Unit X] materials from Google Drive"
git push
```

---

## Google Drive Integration Options (Future)

In the future, the following integrations may be possible:
- **Google Apps Script** — automatically export sheets to CSV on a schedule
- **Google Drive API** — programmatically sync Drive folders to the repo
- **Zapier / Make** — trigger file downloads when Drive files are updated
- **Google Forms → results.csv** — import form response sheets as assessment results

For now, manual export and import is the recommended approach.

---

## Tips

- Migrate one unit at a time to avoid overwhelm.
- Start with curriculum materials before assessment data.
- Use consistent naming from the start — it is much easier than renaming later.
- Keep a copy in Google Drive until you have verified the repository version is complete.
