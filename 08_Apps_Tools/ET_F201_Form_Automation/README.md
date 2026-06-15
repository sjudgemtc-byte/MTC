# ET F201 Form Automation

This folder contains a local student-record form that creates a draft copy of `ET F201.docx`.

## How to use

1. Double-click `Start_ET_F201_Form.command`.
2. The form opens in your browser.
3. Enter the Student Setup details: student name, JSID / Participant ID, CRN, completed block level, and stream.
4. Tick the raw PTA score grid once as the student's baseline, for example `PLA.01`, `PLB.01`, or `1.01`.
5. Enter the exact ACSF rating cells to mark for each completed block, such as `PLB.13, 1.01`.
6. Select `Save Student Record` to keep the student setup for later.
7. For the next 200-hour block, use `Prepare next block` from the saved student records list. This keeps the PTA baseline and previous block outcomes.
8. Select `Review Missing Fields` to check what still needs to be confirmed.
9. Select `Create Draft Word Document` when you are ready to generate the ET F201 copy.
10. Review the generated Word document before uploading, sending, or submitting it.

Generated files are saved in:

```text
Generated Forms
```

Student records are saved in:

```text
Saved Drafts
```

## Safety notes

- The original downloaded `ET F201.docx` has been preserved.
- The app works from the copied template in `templates/ET F201.docx`.
- The form runs locally on this Mac.
- Leave unconfirmed fields blank until the evidence or instruction is available.
- Treat generated documents as drafts for review before use in official systems.
- If the date field is left blank, saved student records and generated Word files use `Date-Unspecified` in the file name.
- Each `.json` file in `Saved Drafts` is a reusable student record.
- PTA baseline raw scores are saved once for each indicator, for example `level_01 = PLB` displays as `PLB.01`.
- ACSF rating cells to mark can be saved by block, for example `progressive_completed_B1 = PLB.13, 1.01`.
- The generated coversheet is cumulative. If B2 is selected, it shows the PTA baseline plus B1 and B2 completed outcomes. If B3 is selected, it shows the PTA baseline plus B1, B2, and B3 outcomes.
- `Prepare next block` creates a new form view for the next block without re-entering the PTA baseline.
- Use the progressive assessment section to backfill students who already completed blocks under the manual system.
- Level 4 ratings can be stored in the student record, but the current ET F201 Word template only shows columns up to Level 3.
- Do not record unsupported ACSF/DLSF increases. Only tick an increase where the evidence supports it.
