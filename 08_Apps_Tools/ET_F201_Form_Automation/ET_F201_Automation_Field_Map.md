# ET F201 Automation Field Map

This note tracks how the local form maps Simon's instructions into the ET F201 Word document.

## Current Workflow

1. Open `Start_ET_F201_Form.command`.
2. Enter or load a saved student record.
3. Save the student record while collecting details.
4. Use `Prepare next block` from a saved student record when the same student reaches the next 200-hour block.
5. Create the Word document only after the details have been checked.
6. Review the Word document before using it in any official system.

## Confirmed Field Rules

| Simon's instruction | App field | ET F201 location | Current status |
|---|---|---|---|
| Student name is Terence Walker | Participant full name | Participant's Full Name | Saved in student record |
| JSID is 5427853609 | JSID / Participant ID | Participant ID | Saved in student record |
| CRN is 209529672V | CRN | CRN | Saved in student record |
| Basic stream calculated using the rule of 7 | Tuition stream = Basic; Stream calculation note records rule of 7 | Top row, Tuition Stream, Basic checkbox | Saved in student record; Basic will render with an X in the checkbox |
| Block level is B1 after 200 hours of attendance | Completed block level = B1; Block note records 200-hour rule | BLOCK row | Saved in student record |
| Terence PTA screenshot provided 2026-06-13 | PTA baseline tick grid fields level_01 to level_13 | Overall ACSF Rating grid | Visible PTA scores saved in student record as a one-time baseline |
| Terence completed PLB.13 and 1.01 after 200 hours | progressive_completed_B1 = PLB.13, 1.01 | Overall ACSF Rating grid and outcomes claimed section | Saved as B1 ACSF rating cells to mark |
| Terence B2 assessment will be 1.12 and 1.13 after 400 hours | progressive_completed_B2 = 1.12, 1.13 | Overall ACSF Rating grid and outcomes claimed section | Saved as B2 ACSF rating cells to mark |
| Coversheet should build cumulatively | Selected block controls cumulative output | Overall ACSF Rating grid and outcomes claimed section | B2 includes B1 + B2, B3 includes B1 + B2 + B3, and so on |
| Simon only marks PTA once | `Prepare next block` keeps PTA fields and previous outcomes | App workflow before Word generation | Added shortcut for moving a saved draft to the next block |
| PTA baseline should be manually ticked | One raw score choice per PTA indicator, such as PLA.01 or PLB.01 | App student record | PTA baseline section changed from dropdowns to a raw score tick/select grid |
| Overall ACSF Rating field is not required | No app field required | N/A | Removed from the form and validation |

## Terence Walker Student Record

Saved B1 record:

```text
Saved Drafts/Date-Unspecified_Walker-Terence_ET-F201_Block-B1.json
```

Saved B2 record:

```text
Saved Drafts/Date-Unspecified_Walker-Terence_ET-F201_Block-B2.json
```

Current confirmed B1 details:

```text
Participant full name: Terence Walker
JSID / Participant ID: 5427853609
CRN: 209529672V
Tuition stream: Basic
Completed block level: B1
Block note: B1 reached after 200 hours of attendance.
Progressive assessment completed outcomes for B1: PLB.13, 1.01
Stream calculation note: Basic stream calculated using the rule of 7.
Trainer name: Simon Judge
PTA indicator scores: PLB.01, 1.02, 1.03, 1.04, 1.05, 1.06, 2.07, 2.08, 1.09, 1.10, 1.11, PLB.12, PLA.13
```

Current confirmed B2 details:

```text
Completed block level: B2
Block note: B2 reached after 400 hours of attendance. This coversheet should reflect the Pre-Training Assessment baseline plus B1 and B2 progressive assessment completions.
Progressive assessment completed outcomes for B1: PLB.13, 1.01
Progressive assessment completed outcomes for B2: 1.12, 1.13
Generated B2 coversheet summary: Cumulative completed outcomes through B2: B1: PLB.13, 1.01; B2: 1.12, 1.13
```

Earlier preserved record copies:

```text
Saved Drafts/Date-Unspecified_Walker-Terence_ET-F201_Block-Unspecified.json
Saved Drafts/2026-06-13_Walker-Terence_ET-F201_Block-Unspecified.json
```

## Not Yet Confirmed

The following fields should remain blank or unselected until Simon provides instructions or visible evidence:

- Training load
- Completion date
- ACSF/DLSF current scores
- Any additional ACSF/DLSF increases or outcomes claimed beyond the confirmed B1 outcomes
- CGEA / FSK / EAL units
- WFA Online Portal checked status
- Centre Manager / Senior Trainer fields

## Next Details To Collect

Use this order while Simon describes the student example:

1. Block number
2. Participant ID and CRN
3. Training load
4. Current ACSF/DLSF scores for each visible indicator
5. Which progressive assessment outcomes have been completed for this block
6. Units or outcomes being claimed
7. WFA Online Portal checked status
8. Completion date
9. Centre Manager details, only if Simon confirms they should be included

## Compliance Notes

- Do not invent evidence or assessment outcomes.
- Record ACSF/DLSF increases only where Simon confirms the evidence supports them.
- Treat generated Word documents as drafts for review before upload or submission.
- If the completion date is not confirmed, leave the app date field blank; the file name will show `Date-Unspecified`.
