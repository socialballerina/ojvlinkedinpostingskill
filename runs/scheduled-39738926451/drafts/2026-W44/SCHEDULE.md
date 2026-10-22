# Week 2026-W44 scheduling checklist

Three posts. Company page: https://www.linkedin.com/company/orange-juice-ventures/
All times 09:00 HKT. Approver: Naman.

Copy each post from `paste/<post_id>.txt` so you are not stripping markdown out of the draft by
hand.

**Note on where these files are.** This CI run could not write under `.claude/skills/`, so this
week's drafts are in `runs/scheduled-39738926451/drafts/2026-W44/` instead of the skill's
`drafts/2026-W44/`. The tracker rows have not been appended yet. See
`runs/scheduled-39738926451/tracker-rows/README.txt`.

**Blockers before anything is scheduled:**

- [ ] All three posts need a photo, or a decision to run text-only. Each PHOTO NEEDED block is below.
- [ ] Friday: Naman to confirm OJV runs the corporate-pilot conversation the post describes.
- [ ] Monday: confirm SMIC has not published its 3Q26 results before 26 October. If it has, kill
      or rewrite the post.
- [ ] The China Tech Trek (13 to 17 October 2026) has already run. Decide what the flagship offer
      is now, so the config table can be updated before the next trek-adjacent post.

---

## 1. Monday 26 October, 09:00 HKT

- **Post ID:** `OJV-202644-M`
- **Archetype:** A, China signal to tour
- **Funnel / CTA:** awareness / soft
- **Copy:** `paste/OJV-202644-M.txt` (1,288 characters)
- **Image:** none yet, see below
- **Alt text (if the briefed photo is used):** Close-up of a silicon wafer, its grid of chip dies
  catching the light against a plain background.
- **First comment:** the filing, tagged:
  `https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0813/2026081300353.pdf?utm_source=linkedin&utm_medium=organic&utm_campaign=A-OJV-202644-M`

```
PHOTO NEEDED for OJV-202644-M (archetype A, Monday)

The post says   : China's largest foundry now earns about nine dollars in ten at home, and the
                  growth is coming from industrial and automotive chips
Nothing in the library fits because: no China, semiconductor or industrial material in the library
Please attach   : close-up of a silicon wafer or a tray of packaged chips, die pattern in focus,
                  no logos, no readable labels, no faces, landscape
Or reply "text only" and this post ships without an image.
```

Steps:

- [ ] Check SMIC has not released 3Q26 results
- [ ] Attach a photo or decide text-only, then paste the alt text into LinkedIn's alt-text field
- [ ] Schedule for Mon 26 Oct, 09:00 HKT
- [ ] Post the source link as the first comment once it is live
- [ ] Tick here when scheduled

## 2. Wednesday 28 October, 09:00 HKT

- **Post ID:** `OJV-202644-W`
- **Archetype:** C, Asia into the West
- **Funnel / CTA:** interest / medium (no keyword; the DM keyword is still TODO)
- **Copy:** `paste/OJV-202644-W.txt` (1,386 characters)
- **Image:** none yet, see below
- **Alt text (if the briefed photo is used):** A row of new SUVs parked on a dealership forecourt,
  the lit showroom behind them.
- **First comment:** the source, tagged:
  `https://www.motoringresearch.com/car-news/omoda-jaecoo-100k-uk-sales/?utm_source=linkedin&utm_medium=organic&utm_campaign=C-OJV-202644-W`

```
PHOTO NEEDED for OJV-202644-W (archetype C, Wednesday)

The post says   : an unknown car brand won British private buyers through a dealership network
Nothing in the library fits because: no retail, showroom or UK street material in the library
Please attach   : wide shot of a UK dealership forecourt or showroom, a row of new SUVs, no
                  badges or signage legible, no faces, eye level, daylight
Or reply "text only" and this post ships without an image.
```

Steps:

- [ ] Check the disclosure line "We have never worked with Omoda, Jaecoo or Chery" is intact
- [ ] Attach a photo or decide text-only, then paste the alt text
- [ ] Schedule for Wed 28 Oct, 09:00 HKT
- [ ] Post the source link as the first comment once it is live
- [ ] Tick here when scheduled

## 3. Friday 30 October, 09:00 HKT

- **Post ID:** `OJV-202644-F`
- **Archetype:** F2, situation to solved (diagnostic)
- **Funnel / CTA:** enquiry / **hard, the week's only one**
- **Copy:** `paste/OJV-202644-F.txt` (1,257 characters)
- **Image:** none yet, needs a team photo, see below
- **Alt text (if the briefed photo is used):** An OJV partner leaning over a notebook across a
  small table from a founder, mid-conversation, in window light.
- **First comment:** none. The post has no outbound link.

```
PHOTO NEEDED for OJV-202644-F (archetype F2, Friday)

The post says   : OJV sits down with a founder and works out whether a corporate pilot has anyone
                  on the other side who can sign
Nothing in the library fits because: every partner shot is a stage, a backdrop or a studio
                  portrait, and the two cleanest are locked until November
Please attach   : Naman (or another OJV partner) across a small table from a founder, mid-
                  conversation, notebook or laptop with nothing legible, partner's face visible,
                  founder side-on or from behind unless they consent, natural light, landscape
Or reply "text only" and this post ships without an image.
```

Steps:

- [ ] Naman confirms the service description is accurate
- [ ] If OJV-L001 (also a "Give us 60 minutes" hook) is queued within 14 days, move one of them
- [ ] Attach the photo or decide text-only, then paste the alt text
- [ ] Schedule for Fri 30 Oct, 09:00 HKT
- [ ] Tick here when scheduled

---

## After the posts have run

Come back and say **"log performance"** with the numbers from the page. That fills `hook_pattern`
and `entities` in `data/posted-log.csv`, which is what stops next week from repeating a hook shape
or a company. Log any DM or email enquiry as a row in `data/leads.csv`.
