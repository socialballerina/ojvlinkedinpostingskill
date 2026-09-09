# Funnel and CTA Ladder

## The four stages

| # | Stage | What content does here | CTA tier | What "working" looks like |
| --- | --- | --- | --- | --- |
| 1 | **Awareness** | Reach content. A China signal, a cross-border pattern, an opinion worth arguing with. No offer. | **Soft** | Impressions, comments from people who are not already in the network, follows |
| 2 | **Interest** | Proof content. A named case, a specific unlock, a number with a source. Shows we know the mechanism. | **Medium** | Comments carrying the keyword, link clicks, profile visits |
| 3 | **Enquiry** | Offer content. The trek, the advisory, the fundraising support. Dates, keyword, destination. | **Hard** | DM keyword uses, enquiry link submissions, inbound DMs |
| 4 | **Booked** | Not a post. The handoff out of LinkedIn into a call. | n/a | Calls held, logged in `leads.csv` as `stage=booked` |

## The mandatory close, and what the tiers now mean

**Every post ends with a qualified ask and the contact line**, whatever its tier. Changed
10 September 2026 by Naman's decision; the reasoning and what it overrode are in
`references/brand-voice.md` rule 9.

```
If you want <the specific thing this post is about> to look like this, work with us.

DM us, or write to us at hello@oj.ventures
```

So the tiers no longer decide *whether* a post asks. They decide **how much offer language sits
above the ask**:

| Tier | What it may add above the close | What it may not do |
| --- | --- | --- |
| **Soft** | Nothing. The ask is the last two lines and there is no offer language anywhere earlier. | Name a price, a date, a keyword or a link |
| **Medium** | One line naming the relevant service as a mechanism, e.g. "that is most of what our GTM advisory work actually is". | Dates, pricing, capacity |
| **Hard** | The full offer block: dates, cities, partner, capacity, and the booking or enquiry destination. | Two offers in one post |

**The ratio rule still exists, and now measures the body.** Roughly 2 value : 1 offer meant eight
value posts to four offer posts in a month. It now means: on a soft post, at most the closing two
lines are offer; on a medium post, at most three. If more than a quarter of a post's lines are
about OJV rather than about the subject, it is an offer post whatever its label, and the monthly
review counts it as one.

## The CTA ladder

Each tier has permitted forms above the mandatory close. Do not mix tiers inside one post.

### Soft (awareness)
- The mandatory close, and nothing above it.
- The line before the ask should be the sharpest sentence of the argument, not a question. A
  question immediately followed by an ask reads as though the question was never sincere.

No links. No keyword. No dates. A question may sit in the body but never last.

### Medium (interest)
- "Comment `<KEYWORD>` and we will send you `<the useful thing>`." The useful thing must exist
  before the post goes out. If it does not exist, this is not a medium CTA, it is a promise.
- One UTM-tagged link to something genuinely useful and not gated: a teardown, a checklist, a
  market note.
- "DM us if you want the longer version."

One CTA only. No dates, no pricing, no "book a call".

### Hard (enquiry)
- Trek dates, cities and partner, plus the DM keyword, plus the enquiry link.
- "Comment `<KEYWORD>` or DM the keyword and we will send the itinerary."
- Enquiry link, UTM tagged, in the first comment rather than the body unless the link is the
  whole point of the post.
- Capacity or deadline facts, but only real ones. Never invent scarcity.

Never end on a question. The close is always the ask.

## Weekly pattern

| Day | Slot | Funnel stage | CTA tier | Archetype |
| --- | --- | --- | --- | --- |
| Monday 09:00 HKT | awareness | 1 | soft | A (no trek mention), B, C or D |
| Wednesday 09:00 HKT | proof | 2 | medium | B, C or D |
| Friday 09:00 HKT | offer, or first-party proof | 3 | hard | **E by default.** A instead, with the trek, when a strong China signal is live and the trek is inside 8 weeks. |

Friday is archetype E's home, because E is the only archetype where OJV is the subject, and the
offer slot is the one place that is appropriate. It is also the only archetype that does not need
external news, which is what keeps a 3-per-week cadence honest in a thin week.

Rules that bind the pattern:

1. **Ratio, measured in lines not posts.** See the table above. Every post asks now, so the
   guard against reading as an ad account is that the ask stays two lines on a soft post and the
   rest of the post is about the subject.
2. **One hard CTA per week.** Unchanged, and it now means one post per week may carry the full
   offer block above the close. Every other post still closes with the ask, just without dates,
   pricing or a destination.
3. **Archetype fatigue.** No archetype twice in the same week. No archetype three weeks running in
   the same slot.
4. **Hook fatigue.** No hook pattern (see the table in `brand-voice.md`) twice in a fortnight.
5. **Slot beats archetype.** If an archetype's default CTA tier is higher than the slot allows,
   downgrade the CTA and cut the offer paragraph. Do not upgrade the slot.
6. **Friday's face.** An archetype E post needs an actual partner in the image: Jason Li, Lee
   Murphy, Daniel Csontos or Naman Tekriwal, or the room itself. A logo is not a face, and E is
   the one archetype with no text-only fallback.
7. **Three archetypes, three slots.** Never the same archetype twice in a week. With five
   archetypes and three slots this is always satisfiable, so there is no excuse for it.
8. **The rotation check decides, not the drafter.** `scripts/rotation-check.py` reads the calendar,
   the posted log, the story list and the image manifest and prints hard BLOCKED rows. Run it
   before researching. Rules 1 to 7 above are enforced by it, not by anybody's memory.

## Mechanics

### UTM tagging
Every outbound link, every time, so the monthly review can attribute enquiries to archetypes.

```
utm_source=linkedin
utm_medium=organic
utm_campaign=<archetype>-<post_id>
```

Example: `?utm_source=linkedin&utm_medium=organic&utm_campaign=A-OJV202637-F`

Append with `?` if the URL has no query string, `&` if it does. Record the tagged link in the
draft file and the untagged source URL in the calendar's `source_url` column, so the calendar
stays readable and the draft stays clickable.

### DM keywords
- One keyword per offer, not per post. The trek keyword is set in the SKILL.md config table.
- Uppercase, one word, no numbers, easy to type on a phone. Suggested: **TREK** for the tour,
  **PULL** and **STORY** for the medium-CTA assets referenced in the archetype examples.
- Every keyword use gets a row in `data/leads.csv` with `keyword_used` and `source_post_id`. A
  keyword that is not logged is a lost lead, and the monthly review cannot see it.
- A keyword must map to something that exists and to a named owner who sends it. Set the owner in
  the `owner` column, default Naman.

### Comment velocity
Comments in the first hour drive distribution more than any other lever available to a page with
a few hundred followers. So:

- **Any comment asking a real question gets a reply within a few hours.** Same working day,
  always. First hour where possible.
- Reply with a sentence that adds something, not "thanks for sharing". A reply that answers the
  question keeps the thread alive and pulls the asker's network into the post.
- Keyword comments get a reply in the thread ("sent") **and** a DM with the thing. The public
  reply is what makes the next person comment.
- Reactions are not a signal worth chasing. Comments and DMs are. Rank posts by those in the
  monthly review.
- Never reply to a keyword comment with just a link, because a link in a reply drags the post's
  reach down the same way a link in the body does.

### Attribution, honestly
LinkedIn organic attribution is lossy. A DM three weeks after a post is real and unattributable.
Log it as `source_post_id=unattributed` rather than guessing, and read the monthly ranking as
directional. If an archetype has fewer than 3 posts logged, it has no ranking, and the review
must say so rather than ranking a sample of one.
