# The Batch Library

How to produce a large queue of posts in advance, so that publishing requires one decision from
one person: pick a picture, paste, post.

The weekly run in `SKILL.md` writes three posts pegged to this week's news. The batch library is
the other mode. It writes tens of posts at once, holds them in a queue, and lets the intern work
down the queue without judgement calls, research or approvals mid-week.

Both modes write the same voice, the same archetypes and the same guardrails. What changes is
what a post is allowed to contain.

---

## The rule that makes batching possible

**A library post is written in the dated past tense and contains nothing perishable.**

This is the whole trick, and breaking it is how a queue of a hundred posts turns into a hundred
posts that cannot be published.

| Never in a library post | Write instead |
| --- | --- |
| "This week ..." | "In August 2026 ..." |
| "Just announced" | "When <company> announced this in August 2026" |
| "Yesterday's news that ..." | "<Company>'s <month year> filing showed ..." |
| "Our trek next month" | "Our next China Tech Trek runs 13 to 17 October 2026" |
| "The market is currently ..." | "As of August 2026 the market was ..." |
| A number that will be revised | A number from a filing or a closed quarter |
| "Register by Friday" | No deadline language at all. Deadlines belong to the weekly run. |

The test: **if a post would read wrongly when published four months from now, it does not belong
in the library.** Send it to the weekly run instead.

---

## What can and cannot be batched

| Archetype | Batch? | Why |
| --- | --- | --- |
| A. China signal to tour | Yes, with a soft or medium CTA | The signal is a dated fact. Write it as history, not as news. A hard-CTA trek version of A is **not** batchable, because trek dates and capacity move. |
| B. West into Asia | Yes | A completed expansion is a case study. It does not go stale. |
| C. Asia into the West | Yes | Same. |
| D. Rejection to raise | Yes | The raise already happened. |
| E. Inside the room | **No** | It is a claim about something OJV did recently. It expires in days and cannot be written before the event. |
| F1. Engagement post | **No** | Needs a real engagement plus client sign-off. Written live, one at a time. |
| F2. Diagnostic post | Yes, capped | Contains no perishable fact at all. But it is the same claim every time, so cap it and vary the segment. |

So a batch is built from A, B, C, D and F2. E and F1 stay in the weekly run. Any plan that claims
otherwise is a plan to publish something untrue.

---

## Composition of a hundred

One hundred posts is roughly eight months at three a week. Composition, and the reasoning:

| Archetype | Count | CTA mix | Why this many |
| --- | --- | --- | --- |
| A. China signal | 25 | 20 soft, 5 medium | The largest single block, because it is the page's differentiated territory and the trek is the flagship offer. Capped at 25 so the page is not only a China account. |
| B. West into Asia | 22 | 12 soft, 10 medium | The core GTM advisory argument, and the archetype that speaks to the paying buyer. |
| C. Asia into the West | 22 | 12 soft, 10 medium | Balances B, and reaches the Asian founders who are the other half of the super-connector claim. |
| D. Rejection to raise | 16 | 12 soft, 4 medium | Travels furthest organically, but it is emotionally one-note. Sixteen is about the ceiling before it reads as a genre. |
| F2. Diagnostic | 15 | 15 hard | One offer post roughly every seventh post, which sits comfortably inside 2 value : 1 offer, and inside one hard CTA per week. |
| **Total** | **100** | 56 soft, 29 medium, 15 hard | |

Constraints the composition has to satisfy, and does:

- **Value to offer, 2:1 or better.** 85 value posts to 15 offer posts is 5.7:1. Comfortable.
- **One hard CTA per week.** 15 hard posts across roughly 33 weeks. Never queue two adjacent.
- **F2 variety.** Fifteen diagnostic posts must not be fifteen versions of one post. Vary on two
  axes and never repeat a pair:

  | Service line | Segments to write it for |
  | --- | --- |
  | GTM advisory | Series A SaaS, hardware, consumer, enterprise software |
  | Lead generation | founder-led sales, no local team, channel-first |
  | Fundraising support | pre-seed, Series A, Asian founder raising in the US |
  | OJV Educate, exec tours | corporate strategy teams, family offices |
  | OJV Educate, universities | university spinouts, tech transfer offices |

  That is fifteen distinct segment-and-service pairs, which is the cap. A sixteenth F2 would
  repeat one.

---

## Numbering and status

Library posts are not assigned to a date until someone schedules them, so they do not use the
weekly `OJV-YYYYWW-<M|W|F>` scheme.

- **Post id:** `OJV-L###`, zero padded, `OJV-L001` to `OJV-L100`.
- **Status vocabulary gains `library`**, meaning written, gated, queued, not yet dated.
- When the intern schedules one, its calendar row moves to `scheduled` and gains a
  `scheduled_date`. The post id does not change, so performance logging still ties back.
- UTM campaign for a library post: `<archetype>-OJV-L###`, the same shape as the weekly run.

---

## The tranche procedure

Write in tranches of ten. Never more, because verification is the bottleneck and a long run
drifts. A tranche is a complete unit of work: ten posts researched, verified, drafted, gated,
paste-filed and logged before the next tranche starts.

For each tranche:

1. **Run the rotation check.** `python3 scripts/rotation-check.py` plus the library-aware pass
   described under "Rotation inside the library" below. Read it before searching.
2. **Assemble candidates.** Ten stories, one per post, each with a primary source you have
   actually opened. Aim for fifteen candidates to end with ten, because roughly a third fail
   verification.
3. **Verify every number.** Quote the sentence carrying each number into the draft's
   `## Verified facts` block, with the publisher and the date. A number you cannot quote does not
   go in. This is the step that takes the time, and it is not skippable in batch mode. Batch mode
   makes the writing cheaper, not the sourcing.
4. **Check the dated-past-tense rule** on every draft, against the table at the top of this file.
5. **Draft**, to `library/OJV-L###.md`.
6. **Gate.** `python3 scripts/style-gate.py library/OJV-L0*.md`
7. **Write the paste files** and the queue rows.
8. **Log** every story to `data/news-seen.csv`, used or not, and every post to
   `data/content-calendar.csv` with `status=library`.
9. **Print the tranche summary** before starting the next one.

Ten tranches make a hundred posts. Expect the sourcing, not the drafting, to set the pace.

---

## Rotation inside the library

The weekly rotation check protects against repetition in time. A library needs the same
protection in queue order, because the intern will publish in queue order.

Enforce, across the queue as written:

| Rule | Window |
| --- | --- |
| No archetype more than twice in any five consecutive queue positions | 5 |
| No hook pattern twice in any six consecutive positions | 6 |
| No entity twice in any twenty consecutive positions | 20 |
| No entity more than three times in the whole hundred | 100 |

**What counts as an entity here.** Companies, named people, and cities. **Countries and regions do
not count**, because China, India and APAC are the page's beat and blocking them would block the
page. This is narrower than the weekly rotation check's entity rule, and deliberately so: the
weekly rule is about not writing about the same subject twice in a quarter, while the queue rule is
about not reading repetitive three posts in a row. Tranche 1 ran three posts whose subject sat in
China and two in India; that is the beat working, not a repetition failure.
| No two hard-CTA posts adjacent, and no more than one per five positions | 5 |
| No story key twice, ever | forever |
| No F2 segment-and-service pair twice | forever |

Then interleave the queue so those hold. It is easier to write ten of one archetype and then
shuffle than to alternate while drafting, so write by archetype and order at the end.

---

## Expiry

Every library post carries `expires:` in its front matter, and the queue is sorted so the
perishable posts go first.

| Archetype | Shelf life | Reason |
| --- | --- | --- |
| A. China signal | 6 months from the source date | Deep-tech numbers get superseded. A robotics valuation from a year ago invites a correction in the comments. |
| B, C | 18 months | Completed expansions stay true. |
| D | 18 months | A closed raise stays closed. |
| F2 | No expiry, but re-read before posting | It expires only when the service description changes. |

An expired post is not published. It is either rewritten with a current source or killed, and
either way the calendar row moves to `killed` with a note. Check expiry at the top of every
weekly session that touches the library.

---

## What the intern actually receives

Three things, and nothing else.

**1. `library/QUEUE.csv`** The work list, in publishing order.

```
queue_no,post_id,archetype,cta_tier,hook_first_80,photo_brief_short,expires,status
```

**2. `library/OJV-L###.md`** One file per post. The intern reads only the top of it. Structure:

```markdown
---
post_id: OJV-L047
archetype: B
cta_tier: soft
hook_pattern: reframe
entities: Notion; Japan
expires: 2028-03-01
status: library
voice: company-page
---

## Copy
<the post, exactly as it should appear, hashtags included>

## Photo brief
PICK: <one line: subject, setting, framing>
AVOID: <what must not be in frame>
FALLBACK: text-only is acceptable        (or: not acceptable)

## Alt text
<one sentence, written for the brief, adjust only if the chosen photo differs materially>

## First comment
<the source line with the UTM-tagged link, to be posted as the first comment>

## Verified facts
<every number, with the quoted sentence, publisher and date. The intern does not need this.
It exists so that a comment challenging a number can be answered in under a minute.>
```

**3. `library/paste/OJV-L###.txt`** The copy alone. Plain text. No front matter, no headings,
nothing to strip. Select all, copy, paste.

### The intern's whole job

1. Open `QUEUE.csv`, take the top row that is still `library`.
2. Open `library/paste/<post_id>.txt`, select all, copy, paste into LinkedIn.
3. Read the photo brief in `library/OJV-L###.md`. Pick a photo from the shared drive that
   satisfies it. If nothing does, and the brief says text-only is acceptable, post without one.
4. Paste the alt text into LinkedIn's alt-text field.
5. Post, or schedule for 09:00 HKT.
6. Post the first comment, if the file has one.
7. Mark the queue row `posted` with the date.

Nothing in that list requires a judgement about content. That is the design goal, and any
library post that forces the intern to decide something about the copy has failed and should be
rewritten.

### The photo brief, and why it replaces the manifest

The weekly run assigns a specific file from `assets/images/manifest.csv`. The library cannot,
because the right photo may not exist yet when the post is written, and because the intern is
the one standing in the shared drive.

So a library post ships with a brief instead. Rules for writing one:

- **Name a subject, a setting and a framing.** "Mid-shot of a components stall in Huaqiangbei,
  trays of actuators in focus, stall depth visible behind, eye level."
- **Say what must not be in frame.** Faces of strangers. A competitor's logo. A whiteboard with
  a client's name on it.
- **Set the fallback honestly.** Text-only is acceptable for A, B, C, D and F2. It is not
  acceptable for E or F1, which is one more reason those two are not in the library.
- **Never brief a photo that implies a claim the copy does not make.** A factory floor photo on
  a post about a company OJV has never worked with implies we were there.
- **Never brief a stock photo.** If the honest answer is that no real photo fits, the fallback is
  text-only, not a stock image.

---

## What the intern must never do

Put this at the top of the shared drive folder, not just in this file.

- Do not change a number. Not to round it, not to update it. If a number looks wrong, flag it.
- Do not add or remove hashtags.
- Do not post two hard-CTA posts in the same week. The queue order already prevents this if it
  is followed.
- Do not skip ahead past an expiring post to get to a more interesting one.
- Do not publish a post whose `expires` date has passed. Flag it instead.
- Do not write a new post. An empty queue is a signal to ask for another tranche.
- Do not reply to a comment that challenges a fact. Pass it to Naman with the post id, and the
  `## Verified facts` block is the answer.

---

## Honest limits of this mode

Worth saying plainly, because the alternative is discovering it in month three.

1. **Batching does not reduce the research.** A hundred sourced posts is a hundred primary
   sources opened and quoted. The saving is in drafting, scheduling and context-switching, not
   in verification.
2. **The page will be less timely.** A library post cannot react to this week's news. If the page
   wants to be part of a live conversation, that is the weekly run's job, and the two modes should
   run alongside each other rather than one replacing the other.
3. **Performance feedback arrives late.** Writing a hundred posts before the first ten have been
   measured means committing to hook patterns and archetypes on no evidence. Mitigation: write
   the first tranche, publish it, log it, and read the numbers before writing tranches four
   onward. The composition table above is a starting hypothesis, not a finding.
4. **F1 and E remain manual.** The two archetypes with real first-party proof, which are the two
   most credible things the page can publish, cannot be batched. A library-only page slowly
   becomes a commentary page.
5. **A hundred posts is a lot of surface area for one wrong number.** The `## Verified facts`
   block per post is the mitigation, and it is why it is mandatory rather than nice to have.
6. **Archetype D does not scale to sixteen posts.** Found the hard way in tranche 1. A D post needs
   a rejection count and a raise, both documented, and that combination is genuinely rare in public
   sources. Five candidates were dropped in one tranche: two had no count at all, one had rejections
   from customers rather than investors, one founder states publicly that he never pitched, and one
   rested on a self-reported figure that two sources give differently. The only clean case found was
   written by the founder himself, and he is not an Asian founder, which archetype D prefers.

   Consequences for the composition table above. Either **cut D from 16 to about 8** and move the
   rest into B and C, or widen D's trigger to admit the adjacent shape: a founder with a documented
   run of failures before a documented raise, which is far better attested. Do not widen it
   silently, and do not fill a D slot by estimating a rejection count. Decide before tranche 2.

7. **Check what happened next.** A library post about a company's strategy has to be checked for
   later developments, not just for whether the original facts were true. Tranche 1 nearly shipped
   a post celebrating Starbucks buying out its China joint venture in 2017, which would have been
   overtaken by Starbucks selling control of that same business in 2025. The arc turned out to be a
   better post than the moment. Search the company name plus the current year before drafting.
