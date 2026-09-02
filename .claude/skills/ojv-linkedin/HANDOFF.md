# Handoff: running OJV's LinkedIn week

You are producing three LinkedIn posts a week for the Orange Juice Ventures company page.
Monday, Wednesday and Friday, 09:00 HKT. This page tells you the whole job. Everything else is
reference you only open when the run tells you to.

## What you actually do

Either press the button on the web tool, or, in Claude Code, say:

> run the week

The web tool runs exactly this skill: the button starts a GitHub Actions job that executes it in
Claude Code, then shows you the result. It also runs itself every Thursday at 10:00 HKT, so
next week's drafts usually exist before you ask for them. The skill will check what cannot be repeated, research candidate stories, pick one of
five archetypes per slot, write the three posts, pair an image with each or ask you to attach one,
and hand you a scheduling checklist.

Then you do three things:

1. **Read** `drafts/<week>/SCHEDULE.md`.
2. **Approve or amend.** Naman approves every post before it goes anywhere.
3. **Schedule them yourself** in LinkedIn, at 09:00 HKT, pasting from
   `drafts/<week>/paste/<post_id>.txt`.

The skill does not schedule and does not publish. That is deliberate, not a missing feature. See
`references/publish-adapter.md`.

## Before your first run

The web tool needs one credential that is not in this repo: an `ANTHROPIC_API_KEY` secret on the
GitHub repository. Without it a run fails on its first step and says so. See the repository README.


Fill the `TODO` rows in the config table at the top of `SKILL.md`. The two that block real work:

- **Enquiry destination** and **DM keyword.** Without them, Friday's offer post cannot have a
  destination, and you will get `TODO(config: ...)` markers sitting in the copy.
- **Raw image folder.** An absolute path where partners drop unlabelled photos. Without it, image
  intake cannot run, and the library will stay at six conference and portrait shots.

The rest can wait. `ContraVC published source` matters only once you post about the China Tech
Trek, but it matters a lot then, because ContraVC is the official partner on that trek and we do
not contradict what they have published.

## The run, in more detail than you will usually need

| Step | What happens | Where you come in |
| --- | --- | --- |
| 1 | `scripts/rotation-check.py` prints what the week cannot repeat | Nothing |
| 2 | Slots and archetypes chosen | Nothing |
| 3 | Stories found and every number verified against the source | Nothing |
| 4 | Three drafts written | Nothing |
| 5 | Images paired from the library | **You may be asked to attach a photo** |
| 6 to 7 | Links tagged, style gate run | Nothing |
| 8 | `SCHEDULE.md` and `paste/*.txt` written | **This is your input** |
| 9 to 10 | Trackers updated, summary printed | Read the summary |

## When it asks you for a photo

It will print a `PHOTO NEEDED` block naming the subject, setting and framing. This happens when
nothing in the library fits the post that was written, which is common for archetype A because the
library currently has no China ecosystem material at all.

Three ways to answer:

- **Attach a photo.** It gets described, tagged, added to the manifest and paired.
- **Reply `text only`.** The post ships without an image. Fine for A, B, C and D.
- **Say you will shoot it later.** The post is held and the slot goes to the next candidate.

Archetype E is the exception. It is a claim about a room that happened, so it needs a real photo.
If there is no photo, change the post.

## The five archetypes

Each post is exactly one of these, and the choice comes from what you actually have, not from
preference.

| | Archetype | Triggered by |
| --- | --- | --- |
| A | China signal to tour | Dated China deep-tech news with a checkable number |
| B | West into Asia | A US or European company with real traction in Asia, and a named mechanism |
| C | Asia into the West | The mirror case |
| D | Rejection to raise | A documented rejection count and a documented raise |
| E | Inside the room | Something OJV actually did: event, workshop, portfolio, partner on stage |

Typical week: Monday A/B/C/D with a soft close, Wednesday B/C/D with a medium CTA, Friday E or the
trek with the week's single hard CTA.

## Feeding it, so it gets better rather than repetitive

Two habits, and they are the whole difference between a page that compounds and one that recycles.

1. **Log what went out.** After posting, say "log performance" and paste the numbers. This fills
   `hook_pattern` and `entities`, which is what stops the skill writing about the same company or
   using the same hook shape next month. A post logged without those two fields is invisible to
   the next rotation check.
2. **Drop photos in the raw folder and say "intake images".** Especially anything from a trek, a
   factory floor, a robotics showroom or a partner on stage. The image library is the binding
   constraint on this whole operation right now.

Once a month: "monthly LinkedIn review". It ranks the five archetypes by enquiries per post and
tells you what to cut.

## Things you must not do

- Do not let a number into a post that you cannot find in the linked source. If it cannot be
  sourced, it gets cut. This applies to funding amounts, rejection counts, market shares and
  quotes.
- Do not imply OJV worked with a company it did not work with. Third-party cases are commentary
  and the copy says so out loud.
- Do not promise a fundraising outcome. The claim is a shorter, better-targeted investor list,
  never the yes.
- Do not post two hard CTAs in one week.
- Do not post about the China Tech Trek anything that contradicts ContraVC.
- Do not schedule anything Naman has not approved.

## Where things are

```
HANDOFF.md          you are here
SKILL.md            the run, the config, the guardrails, the error table
scripts/            rotation-check.py, style-gate.py
references/         voice, archetypes, funnel, images, publishing
data/               calendar, posted log, leads, stories seen
assets/images/      manifest.csv and the library
drafts/YYYY-WW/     drafts, SCHEDULE.md, paste/
```

Worked example of a finished week, including a post held for a photo:
`drafts/2026-W37/`.
