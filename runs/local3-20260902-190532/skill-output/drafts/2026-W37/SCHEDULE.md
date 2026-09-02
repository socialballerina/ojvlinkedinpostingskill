# Week 2026-W37 scheduling checklist

Two posts this run, not three. Company page: https://www.linkedin.com/company/orange-juice-ventures/
All times 09:00 HKT. Approver: Naman.

**Why only two.** `scripts/rotation-check.py` for the week of 2026-09-07 found archetypes A, B and
D already on file for this exact week (Monday D/Canva, Wednesday B/Notion, Friday A/Unitree, all
`status=draft` in `data/content-calendar.csv` before this run). Only C and E were open, and E is
Friday-only per the weekly pattern table. That leaves one archetype (C) for two candidate slots
(Monday, Wednesday); it was placed on Wednesday because C's native funnel tier (interest to
consideration) fits the proof/medium-CTA slot better than Monday's soft/awareness slot. Monday
ships empty this week. This is the skill's own documented least-bad path when only two archetypes
have verified material ("ship two posts, say which slot is empty and why"), not a shortcut taken
to avoid research.

This draft set replaces the Wednesday (B/Notion) and Friday (A/Unitree) posts from the earlier
example on file for this week; those two stories were not posted and remain usable in a future
week once their archetypes are unblocked. Monday's D/Canva draft is untouched by this run.

**Platform note:** this run's session could not write to `.claude/skills/ojv-linkedin/` (Write and
Edit were both blocked there for the whole session, apparently a permission boundary protecting
the skill's own directory tree). Everything below is staged at
`runs/local3-20260902-190532/skill-output/` instead of the real `drafts/2026-W37/` location. A
human (or a rerun with edit permission on the skill directory) needs to move these files into
place: this `SCHEDULE.md` and `paste/` over the existing ones, the two new draft `.md` files
alongside (replacing) `OJV-202637-W-archetypeB-notion-japan.md` and
`OJV-202637-F-archetypeA-unitree-trek.md`, and the calendar/news-seen row changes in
`skill-output/data/`.

**Blockers before anything is scheduled:**

- [ ] Friday needs a real photo from the actual August summer drinks event, or a decision to run
      a different story instead. Archetype E cannot ship text-only. See the PHOTO NEEDED block in
      the Friday draft.
- [ ] Friday's enquiry destination is still `TODO` in the config table and sits inline in the
      copy. Fill it in `SKILL.md` and re-run, or edit the paste file. (The DM keyword TREK was
      supplied for this run and is already filled in.)
- [ ] Friday's first-party number ("more than 150 signups") has not been checked with whoever
      owns the Carta/Endowus signup list, per the archetype E rule that first-party numbers are
      confirmed with the partner who owns them before scheduling.
- [ ] Friday: **TREK POST UNVERIFIED AGAINST CONTRAVC.** The ContraVC published source in the
      config table is `TODO`. This draft states only the dates, cities and partner name from the
      config override, nothing else about the itinerary. Confirm against what ContraVC has
      published before this goes out.
- [ ] Wednesday's CTA promises three questions ("Comment CHANNEL and we will send you the three
      questions...") that do not exist yet. Either write them or change the close to a plain
      question before scheduling.
- [ ] Monday has no post this week. Decide whether to leave the slot empty, revive the existing
      Canva/D draft on file (archetype D is blocked by rotation-check only because that same draft
      is on record; it was never actually posted), or wait for next week.

---

## 1. Wednesday 9 September, 09:00 HKT

- **Post ID:** `OJV-202637-W`
- **Archetype:** C, Asia into the West
- **Funnel / CTA:** interest / medium, keyword `CHANNEL`
- **Copy:** `paste/OJV-202637-W.txt` (1,225 characters)
- **Image:** `assets/images/raw/stage-bodw.jpg`
- **Alt text:** Naman Tekriwal on a conference stage in Hong Kong, speaking into a headset
  microphone, illuminated signage and portrait panels behind him.
- **First comment:** post the Pop Mart source link here, tagged:
  `https://finance.yahoo.com/markets/stocks/articles/pop-mart-reports-first-half-114000738.html?utm_source=linkedin&utm_medium=organic&utm_campaign=C-OJV202637-W`

Steps:

- [ ] Decide the `CHANNEL` blocker above. Do not schedule a CTA that promises a document nobody
      has written.
- [ ] Read the copy. Check the disclosure line "We have never worked with Pop Mart" is intact.
- [ ] Attach `stage-bodw.jpg`, paste the alt text
- [ ] Schedule for Wed 9 Sep, 09:00 HKT
- [ ] Post the source link as the first comment within a minute of it going live
- [ ] Tick here when scheduled

## 2. Friday 11 September, 09:00 HKT

- **Post ID:** `OJV-202637-F`
- **Archetype:** E, Inside the room
- **Funnel / CTA:** enquiry / **hard, the week's only one**
- **Copy:** `paste/OJV-202637-F.txt` (1,021 characters)
- **Image:** none yet, see below
- **First comment:** the enquiry link once it exists, tagged
  `?utm_source=linkedin&utm_medium=organic&utm_campaign=E-OJV202637-F`

```
PHOTO NEEDED for OJV-202637-F (archetype E, Friday)

The post says   : more than 150 people came to a co-hosted, no-agenda drinks event in Hong Kong
                  last month with Carta and Endowus
Nothing in the library fits because: the library has no photos from this specific event, only six
                  unrelated conference and portrait shots of one partner from other occasions
Please attach   : a real photo from the August summer drinks event. A named partner or a
                  Carta/Endowus co-host in the room, or a candid wide shot of the room itself,
                  no panel, no slide deck visible. Confirm consent for any attendee face that is
                  not a partner or co-host.
Archetype E does not ship text-only. If no photo exists, this slot needs a different story rather
than this post without an image.
```

Steps:

- [ ] Attach a real photo from the actual event (not a substitute from the library)
- [ ] Confirm the "150+ signups" figure with whoever owns the Carta/Endowus signup list
- [ ] Fill the enquiry destination, or edit it out of the copy (TREK keyword is already filled in)
- [ ] **Check against ContraVC.** They are the official partner on the trek and the config table
      has no link to what they have published. This post states only dates, cities and the partner
      name for that reason. Confirm those three match ContraVC before it goes out.
- [ ] Confirm the trek dates are still 13 to 17 October 2026
- [ ] Schedule for Fri 11 Sep, 09:00 HKT
- [ ] Tick here when scheduled

---

## After the posts have run

Come back and say **"log performance"** with the numbers from the page. That fills `hook_pattern`
and `entities` in `data/posted-log.csv`, which is what stops next week reusing the same hook shape
or writing about Pop Mart or the Carta/Endowus event again. A post logged without those two fields
is invisible to the rotation check.

Log any DM or comment that used a keyword as a row in `data/leads.csv`.
