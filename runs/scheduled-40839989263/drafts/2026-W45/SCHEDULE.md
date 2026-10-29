# Week 2026-W45 scheduling checklist

Three posts. Company page: https://www.linkedin.com/company/orange-juice-ventures/
All times 09:00 HKT. Approver: Naman.

Work down this page. Copy each post from `paste/<post_id>.txt` so you are not stripping markdown
out of the draft by hand.

**Where these files are.** This CI session could not write under `.claude/skills/`, so this week's
drafts are in `runs/scheduled-40839989263/drafts/2026-W45/` and not in
`.claude/skills/ojv-linkedin/drafts/2026-W45/`. Move them there, and append the rows in
`runs/scheduled-40839989263/tracker-rows/` to the data files. **Last week's (W44) rows still have
not been appended either**, and until both weeks are on file the rotation check cannot see them.

**Blockers before anything is scheduled:**

- [ ] All three posts need a photo, or a decision to run text-only. See each PHOTO NEEDED block in
      the drafts.
- [ ] Friday: Naman confirms OJV really runs the first-APAC-hire diagnostic the post describes.
- [ ] Monday: check whether Costco Korea's FY2026 audit report (year to August 2026) is out. If it
      is, the revenue line is still true as dated but looks old. Update it or leave it.

---

## 1. Monday 2 November, 09:00 HKT

- **Post ID:** `OJV-202645-M`
- **Archetype:** B, West into Asia (Costco in Korea)
- **Funnel / CTA:** awareness / soft
- **Copy:** `paste/OJV-202645-M.txt` (1,366 characters)
- **Image:** none yet. Requested: a warehouse-store aisle with pallets of bulk goods, no branding
  legible, no faces. Stock search `warehouse store aisle pallets bulk goods` is acceptable.
- **Alt text (for the requested shot):** A long warehouse-store aisle with tall steel racking and
  pallets of bulk goods stacked high on both sides.
- **First comment:** the two sources, tagged:
  `https://www.kedglobal.com/retail/newsView/ked202411190017?utm_source=linkedin&utm_medium=organic&utm_campaign=B-OJV202645-M`
  `https://koreaherald.com/article/10620314?utm_source=linkedin&utm_medium=organic&utm_campaign=B-OJV202645-M`

Steps:

- [ ] Read the copy. Check the disclosure line "We have never worked with Costco" is intact.
- [ ] Attach the photo or decide text-only, and paste the alt text into LinkedIn's alt-text field
- [ ] Schedule for Mon 2 Nov, 09:00 HKT
- [ ] Post the source links as the first comment within a minute of it going live
- [ ] Tick here when scheduled

## 2. Wednesday 4 November, 09:00 HKT

- **Post ID:** `OJV-202645-W`
- **Archetype:** C, Asia into the West (Asics SportStyle in Europe)
- **Funnel / CTA:** interest / medium
- **Copy:** `paste/OJV-202645-W.txt` (1,377 characters)
- **Image:** none yet. Requested: a row of retro-style running sneakers on a shop shelf, no logos
  or stripes legible, no faces. Do not use stage-bodw.jpg or forbes-summit.jpg: third-party logos
  beside a post about branding.
- **Alt text (for the requested shot):** A row of retro-style running sneakers lined up on a pale
  shop shelf, toes facing the camera.
- **First comment:** the source, tagged:
  `https://assets.asics.com/system/media_libraries/25964/file.pdf?utm_source=linkedin&utm_medium=organic&utm_campaign=C-OJV202645-W`

Steps:

- [ ] Read the copy. Check the disclosure line "We have never worked with Asics" is intact.
- [ ] Attach the photo or decide text-only, paste the alt text
- [ ] Schedule for Wed 4 Nov, 09:00 HKT
- [ ] Post the source link as the first comment
- [ ] Tick here when scheduled

## 3. Friday 6 November, 09:00 HKT

- **Post ID:** `OJV-202645-F`
- **Archetype:** F2, situation to solved (diagnostic, first APAC hire)
- **Funnel / CTA:** enquiry / **hard, the week's only one**
- **Copy:** `paste/OJV-202645-F.txt` (1,302 characters)
- **Image:** none yet. Requested: Naman (or another OJV partner) in a working session at a
  whiteboard or small table, partner's face visible, the other person side-on or from behind
  unless they consent, nothing legible on the board.
- **Alt text (for the requested shot):** Naman Tekriwal of Orange Juice Ventures at a whiteboard in
  a working session, talking through a list of markets with a founder seen from behind.
- **First comment:** none. No source, and the contact line is already in the post.

Steps:

- [ ] Naman confirms this diagnostic is a real part of OJV's GTM advisory work. If not, kill it.
- [ ] Attach the team photo or decide text-only, paste the alt text
- [ ] Schedule for Fri 6 Nov, 09:00 HKT
- [ ] Tick here when scheduled

---

## After the posts have run

Come back and say **"log performance"** with the numbers from the page. That fills `hook_pattern`
and `entities` in `data/posted-log.csv`, which is what stops next week reusing the same hook shape
or writing about Costco again. A post logged without those two fields is invisible to the
rotation check.

Next week: Wednesday should not be C, and Friday must not be F (it would be three weeks running).
