/ojv-linkedin

If that skill did not load, read .claude/skills/ojv-linkedin/SKILL.md now and follow it. Every
relative path in the skill is relative to .claude/skills/ojv-linkedin/.

Write the next batch-library tranche: {{COUNT}} posts.

**Read `references/batch-library.md` in full before writing a single post.** It is the spec for
this mode. The two failure modes it exists to prevent are queueing posts that will read wrongly in
four months, and queueing posts that need a judgement call from the person publishing them.

You are running headless in CI, so nobody can answer a question. Where the skill says to ask a
person, record the request in `needsFromAuthor` and carry on with the rest.

## What this run must respect

1. **Only archetypes A, B, C, D and F2 can be batched.** E and F1 need first-party facts that
   either expire or need a client's sign-off. Do not substitute them in quietly.
2. **Continue the numbering.** Read `library/QUEUE.csv` and the existing `library/OJV-L*.md`
   files. The next id is one past the highest that exists. Never reuse an id.
3. **Rotation applies across the whole library, not just this tranche.** Apply the table under
   "Rotation inside the library". Read every existing draft's front matter first so you know
   which hook patterns, entities, stories and F2 segment-and-service pairs are already used.
   Countries and regions are not entities for this purpose; companies, named people and cities are.
4. **Dated past tense, nothing perishable.** No "this week", no "just announced", no deadlines,
   no "last year". Resolve every relative date in a source to an explicit year before it goes in
   the copy. Every post carries an `expires:` date.
5. **Archetype D is capped at 4 in this tranche.** See item 6 under "Honest limits of this mode".
   A rejection count that is a self-report contradicted by another source gets cut, not averaged.
   If fewer than the cap verify, write fewer and move the slack into B and C.
6. **Check what happened next.** Before drafting any post about a company's strategy, search the
   company name plus the current year. A post about a 2017 masterstroke that was reversed in 2025
   is a post that embarrasses the page.
7. **Every number traces to a sentence you actually read.** Quote it into the draft's
   `## Verified facts` block with the publisher and date. If a page will not load, say so in that
   block and either find another source or cut the number. Do not fill a number from memory.
8. **Photo brief, not a photo.** Each post ships a `## Photo brief` with PICK, AVOID and FALLBACK
   lines. The intern satisfies it from the shared drive.
9. **The mandatory close, on every single post.** No exceptions and no tier is exempt. The last
   two lines of every post, before the source line and the hashtags, are:

   ```
   <the qualified ask for that archetype>

   DM us, or write to us at hello@oj.ventures
   ```

   The per-archetype wording is the table under "The mandatory close" in
   `references/post-archetypes.md`. **No post ends on a question.** A question may sit in the
   body, and archetype F's diagnostic stack needs one, but the last words are always the ask.

   Two things that will fail the gate: a bare "Work with us." without the "If you want ..."
   qualifier, and anything placed after the contact line other than the source line and hashtags.

   For archetype D the object of the ask is the investor list, the targeting or the warm paths.
   **Never the raise and never the funding**, which is the same outcome rule as archetype D
   itself. `If you want your raise to look like this` is banned.

   Because every post now carries a real destination, do not invent DM keywords or promise
   keyword assets. A keyword is optional and only for comment velocity.

Config for this run, overriding the config table where a value is given:
- Booking link for archetype F: {{BOOKING_URL}}
- Raw image folder: not available in CI, so skip image intake entirely.

If the booking link above is empty, leave the literal marker `TODO(config: booking link)` at the
exact spot in any F2 copy and list it in `needsFromAuthor`. Do not invent a URL and do not drop
the CTA.

## What to write

For each post, `library/OJV-L###.md` with the front matter and the six sections, copying the shape
of the existing drafts exactly. Then `library/paste/OJV-L###.txt`, the copy alone, plain text.

Then, in this order:

1. Run the style gate and fix every failure in the draft, never in the gate:
   `python3 .claude/skills/ojv-linkedin/scripts/style-gate.py .claude/skills/ojv-linkedin/library/OJV-L*.md`
   It now checks the mandatory close as well as the 900 to 1,450 band, so a missing contact line
   or a trailing question is a hard failure, not a style preference.
2. Rewrite `library/QUEUE.csv` for the whole library, in publishing order: perishable first, then
   interleaved so the rotation rules hold, no two hard-CTA posts within five positions.
3. Append to `data/news-seen.csv` every story considered, used or not, with a note on why an
   unused one was dropped. A dropped candidate with a reason is worth as much as a used one.
4. Append to `data/content-calendar.csv` one row per new post with `status=library`, including
   `hook_pattern` and `entities`. A post logged without those two is invisible to the next
   rotation check.
5. Regenerate the site page:
   `python3 .claude/skills/ojv-linkedin/scripts/build-queue-page.py public/queue.html`

ALSO REQUIRED for this CI run. Write `runs/{{RUN_ID}}/result.json`, relative to the repository
root, with this exact shape:

{
  "runId": "{{RUN_ID}}",
  "state": "done",
  "mode": "tranche",
  "requested": {{COUNT}},
  "written": 0,
  "firstId": "OJV-L###",
  "lastId": "OJV-L###",
  "posts": [
    {
      "postId": "OJV-L###", "queueNo": 1,
      "archetype": "A", "archetypeName": "...", "ctaTier": "soft",
      "hookPattern": "...", "expires": "YYYY-MM-DD",
      "copy": "the finished post, real newlines",
      "entities": ["..."], "storyKey": "...",
      "sourceUrl": "...", "sourcePublisher": "...",
      "firstComment": "", "disclosure": "",
      "verified": true, "verificationNotes": "quote the weakest sourcing honestly",
      "styleGate": [], "photoBrief": "", "altText": "",
      "blockers": [], "draftPath": "library/OJV-L###.md"
    }
  ],
  "droppedCandidates": [{"storyKey": "...", "archetype": "D", "why": "..."}],
  "rotation": {"blockedHookPatterns": [], "blockedEntities": [], "usedF2Pairs": []},
  "needsFromAuthor": ["anything a person must supply, decide or confirm"],
  "notes": ""
}

Rules for that file:
- `written` is the real count. If only seven of ten verified, write seven and say why in `notes`.
  Seven sourced posts beat ten with three invented. A short tranche is a correct outcome, not a
  failed one.
- `styleGate` must be the real output of the gate for that draft, after fixes.
- `verificationNotes` names the weakest source in the post. Do not write "all verified" if a page
  returned 403 and you worked around it.
- Valid JSON only. No trailing commas, no comments, no markdown fence.
- Writing this file is not optional. Without it the run is reported as failed.

Do not commit anything. A later workflow step commits whatever you wrote.
