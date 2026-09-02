---
post_id: OJV-202637-F
scheduled: 2026-09-11 09:00 HKT
slot: Friday / offer
archetype: E (Inside the room)
funnel_tier: enquiry
cta_tier: hard
voice: company-page
image: NEEDS SHOOT
status: draft
blockers: TODO(config) enquiry destination; image needed (see below); first-party numbers
  unchecked with Carta/Endowus; TREK POST UNVERIFIED AGAINST CONTRAVC
target_path: drafts/2026-W37/OJV-202637-F-archetypeE-summerdrinks.md (replaces the file at
  drafts/2026-W37/OJV-202637-F-archetypeA-unitree-trek.md, which this week's rotation check now
  blocks; that file's content should be moved aside or deleted once this one is applied)
---

## Why this post is in this slot

Friday is the week's single hard CTA. Archetype A (the Unitree/trek post this replaces) is
BLOCKED this week because `data/content-calendar.csv` already carries a draft row for this exact
week under archetype A. E is the only archetype rotation-check leaves open for Friday (it is
Friday's default per the weekly pattern table regardless), and this run was given a genuine,
first-party OJV event to draw on: summer drinks in Hong Kong with Carta and Endowus. That is
exactly the input archetype E requires, so it is used rather than inventing a room. Two other
pieces of OJV news were supplied for this run (Jason Li judging at Hong Kong Fintech Week x
StartmeupHK, and Preferrd joining the advisory portfolio); both are held back rather than folded
into this post, so the post stays about one specific, checkable room rather than three
loosely-connected updates. Either is a candidate for a future E slot.

## Copy

August in Hong Kong is supposed to be the quiet month, empty calendars, everyone away.

We pulled more than 150 signups anyway.

Last month we ran summer drinks with Carta and Endowus. Gelato, cold beer, a room of founders and investors.

No panels. No pitch decks. No agenda.

That was the design, not a shortcut. A panel gives forty people permission to sit quietly and watch four people talk. Take the panel away and the same forty people have to actually meet each other, which is the only reason any of them showed up.

Startups do not scale on capital alone. They scale on access, to the right operators and the right partners at the right time. Our job is to keep building the rooms where that happens.

Thanks to Carta and Endowus for co-hosting.

The next one runs alongside the China Tech Trek: Hong Kong and Shenzhen, 13 to 17 October 2026, with ContraVC as official partner.

Comment TREK and we will send you the details.
Enquiries: TODO(config: enquiry destination)

#HongKong #Founders #APAC #VentureStudio

## Image

`NEEDS SHOOT`. Archetype E has no text-only fallback: this post is a claim about a specific room
that happened, so it needs a real photo from that room (a partner's face, a co-host, or the venue
itself), not a generic library shot.

Two images in the manifest are tagged `BTS` and currently available (`stage-bodw.jpg`,
`forbes-summit.jpg`), but neither is used here. Both are unrelated events (a design-week
conference stage and a 2023 Forbes Summit in Singapore) with visible third-party branding from
companies that have nothing to do with this post. Using either to illustrate a specific claim
about the August Carta/Endowus drinks event would misrepresent what is in the frame, which the
pairing rule in `references/image-intake.md` forbids ("never force a pair").

```
PHOTO NEEDED for OJV-202637-F (archetype E, Friday)

The post says   : more than 150 people came to a co-hosted, no-agenda drinks event in Hong Kong
                  last month with Carta and Endowus.
Nothing in the library fits because: the library has no photos from this specific event. It has
                  six unrelated conference and portrait shots of one partner from other
                  occasions, none of which can honestly stand in for this room.
Please attach   : a real photo from the August summer drinks event. A named partner (Naman,
                  Jason Li, Lee Murphy or Daniel Csontos) or a Carta/Endowus co-host in the room,
                  or a candid wide shot of the room itself with people talking, no panel, no
                  slide deck visible. Faces of attendees who are not partners or co-hosts need
                  their consent confirmed before this ships, per guardrail 7.
Or reply "text only": not available for archetype E. If no photo exists, change the post to a
                  different archetype/story rather than shipping this one without an image.
```

This run could not intake new images: the raw image folder is unavailable in this CI run per the
run's config override, so pairing was restricted to what is already in `assets/images/manifest.csv`,
and nothing there fits.

## Source

First-party. No external source; the event, headcount and co-hosts are from the OJV news supplied
for this run: "Ran summer drinks in Hong Kong last month with Carta and Endowus: 150+ signups off
our own list, no panels, no pitch decks, no agenda."

Per "First-party numbers in archetype E" in `references/post-archetypes.md`, this number must be
checked with the partner who owns the signup list before the post is scheduled. That check could
not be run in this session (headless, nobody to confirm with). Flagged as a blocker below and in
`needsFromAuthor`.

The trek dates, cities and partner name (Hong Kong and Shenzhen, 13 to 17 October 2026, with
ContraVC as official partner) are taken directly from this run's config override and are not
sourced further than that.

## Verified facts used

- "More than 150 signups", the Carta/Endowus co-hosting, "no panels, no pitch decks, no agenda":
  as supplied in this run's OJV news input, treated as first-party fact per the skill's
  instructions, not independently verified against an external source (none exists for a
  first-party event). NOT checked with Carta or Endowus in this session; see blockers.
- Trek dates (13 to 17 October 2026), cities (Hong Kong and Shenzhen) and partner (ContraVC):
  from this run's config override, matching `SKILL.md`'s config table.
- Deliberately NOT used in this post: Jason Li judging at Hong Kong Fintech Week x StartmeupHK,
  and Preferrd joining the advisory portfolio. Both are real per the supplied OJV news, but kept
  out to hold this post to one checkable room rather than three unrelated updates in one post.

## Guardrail notes

- Archetype E is the one archetype where OJV is the subject; the claim made ("we ran this event,
  these were the co-hosts, this was the headcount") is bounded to what OJV says it did, and
  credits Carta and Endowus by name for co-hosting, not for running the event.
- ContraVC alignment (guardrail 5): the ContraVC published source in the config table is `TODO`
  and unreachable in this session. Per the guardrail, this draft states only the dates, cities and
  partner name given in the config override, and no itinerary, pricing or capacity specifics.
  **TREK POST UNVERIFIED AGAINST CONTRAVC.**
- Hard CTA, no closing question. One config TODO (enquiry destination) sits inline where the
  value belongs, per the run's error-handling instructions for a TODO config value.
- DM keyword TREK, per this run's config override.
- First-party number ("more than 150 signups") is not independently checked with the partner who
  owns the signup list. This is a blocker, not a guardrail pass: do not schedule until Naman or
  the list owner confirms the figure.
- Image is outstanding; per the skill's own rule, this post must not ship text-only. See the
  PHOTO NEEDED block above.
