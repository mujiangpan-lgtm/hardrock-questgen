# Cloud task 3: full scoring round, then lift the weakest chapters (2026-10-06)

The goal is a book average near **8**. Since round 2, climate was redone locally (`art_styles.d/climate.json`
plus the new `pixel_*` motifs in `artlib.py`, documented in ART_GUIDE.md "Round 7"). Rewards also changed,
but that does not affect the art.

**Budget is tight:** about $34 of prepaid credit is left, and after that the owner's own quota is used.
Stop at about $30 total. Use sonnet 5.5 for every subagent (model id `claude-sonnet-5-5`), not the plain
`sonnet` alias.

## Setup

Same as `CLOUD_TASK.md`: pip, fonts-noto-cjk, decrypt `packdata.tar.gz.enc` with the key from your task
message, then run `python build.py --check`.

## Step 1: reference build and blind scoring of all 19 chapters (do this first, keep it cheap)

1. Build and preview everything into `_stage_ref`:
   ```
   QGEN_STAGE=_stage_ref python build.py --stage
   QGEN_STAGE=_stage_ref QPREVIEW_SCREEN=29 python preview.py <all 19 stems>
   ```
   (stem list in `CLOUD_TASK.md` Task B). Copy the screen29 previews into `_art_review/r3_before/`.
2. Make the contact sheet:
   ```
   python tools/contact.py _art_review/r3_before <19 keys> 4
   ```
3. Run **one** fresh critic that scores all 19 previews blind, on both lenses (director and player), with
   the rubric in `CLOUD_TASK.md`. It must not read any earlier critique files. It writes
   `_art_review/critique_r3_before.json` with, per chapter: director, player, up to 4 issues with
   screen-fraction positions, and what_for_8.

## Step 2: fix the weakest chapters, lowest average first

- Take the chapters whose average is **below 7.5**, sorted from lowest up.
- Fix them one after another with **one** sonnet-5.5 subagent each, at most 2 in parallel. Each fixer:
  - reads ART_GUIDE.md (Rounds 5-7) and its chapter's issues, and uses the strongest chapters' specs
    as technique references: create, pneumatic, storage, iron_age, climate;
  - works only on its own `art_styles.d/<key>.json`;
  - may add opt-in `artlib.py` motifs, but never changes an existing default;
  - uses at most 5 stage builds;
  - saves the spec after every improvement;
  - restores the original if the result is not clearly better.
- Before each new chapter, check the spend. When about $25 is used, stop starting new chapters and go to
  Step 3.
- Log every chapter that was skipped and the reason.
- **Proof that nothing else changed** (required if `artlib.py` was edited):
  1. Do a final full stage build into `_stage_final`.
  2. Every generated texture of the chapters you did NOT edit must be byte-identical to `_stage_ref`.
     Compare md5 of `_stage_*/textures/*.png`, ignoring files that start with an edited chapter's
     key + "_".
  3. Their `ftb_quests_theme.txt` lines must be identical too.

## Step 3: re-score and deliver

1. Preview the edited chapters from `_stage_final` and copy them into `_art_review/r3_after/`.
2. Run one fresh blind critic (same rubric, both lenses) that scores **only the edited chapters**, with
   `_art_review/r3_before/contact_sheet.png` as book context. It writes `_art_review/critique_r3_after.json`.
3. Append a "Round 3" section to `_art_review/RESULTS.md` covering:
   - the scores of all 19 chapters before;
   - the edited chapters before → after;
   - the new book average (unedited chapters keep their before score);
   - what changed;
   - artlib additions;
   - skipped chapters;
   - spend.
4. Commit to a new branch `art-fixes-3` (from main) and push. Do not merge.

Rules, as before:
- Never run `build.py` without `--stage` or `--check`.
- Do not edit `chapters/*.py`, `qlib.py`, `registry.json` or `build.py`.
- Never commit `_packdata/` or the key.
