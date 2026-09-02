---
name: ojv-linkedin
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch
description: Weekly LinkedIn content engine for Orange Juice Ventures (oj.ventures), the Hong Kong venture studio positioning as APAC's super-connector. One run produces three scheduling-ready posts for Monday, Wednesday and Friday: researches candidate stories, picks one of five archetypes per post (China signal to tour, West into Asia, Asia into the West, rejection to raise, inside the room), drafts in OJV voice, assigns an image from the tagged library or asks the author to attach one, writes alt text, tags links with UTMs, and refuses to repeat an archetype, hook pattern, story, company or image that went out recently. The author schedules the posts themselves; this skill never publishes. Use whenever the user says "run the week", "plan the OJV week", "generate this week's posts", "three posts for next week", "OJV post", "draft a LinkedIn post for OJV", "post from this link", "post from this photo", "intake images", "tag the new photos", "log performance", "log LinkedIn numbers", "monthly LinkedIn review", "which archetype is working", or names the China Tech Trek in a content context.
---

# OJV LinkedIn Content Engine

Produces one week of LinkedIn content for the Orange Juice Ventures company page: three posts,
Monday, Wednesday and Friday, 09:00 HKT. Research, archetype choice, drafting, image pairing and
repetition control all happen inside one run.

**The output is scheduling-ready, not published.** The run hands the author a paste-ready block
per post and a checklist. The author schedules them in LinkedIn themselves. This skill never
posts, never schedules and never DMs. See `references/publish-adapter.md` for why.

**New here?** Read `HANDOFF.md` first. It is one page and it is the whole job.

---

## The weekly run

This is the default. If someone invokes this skill without saying what they want, do this.

```bash
python3 scripts/rotation-check.py            # start here, always
```

### Step 1. Check what the week cannot repeat

Run `scripts/rotation-check.py <monday>`, or with no argument for next Monday. It reads the
calendar, the posted log, the story list and the image manifest, then prints hard BLOCKED rows
for archetypes, hook patterns, entities, stories and images.

Read it before searching for anything. A blocked archetype is out even if the news is perfect.
Do not research first and rationalise afterwards, because that is how the page ends up posting
about Unitree three times in a month.

If the script reports `NO IMAGE for: <archetypes>`, expect step 5 to ask the author for a photo,
and say so early rather than at the end.

### Step 2. Decide the three slots

| Day | Funnel stage | CTA tier | Archetype |
| --- | --- | --- | --- |
| Monday 09:00 HKT | awareness | soft | A, B, C or D |
| Wednesday 09:00 HKT | proof | medium | B, C or D |
| Friday 09:00 HKT | offer, or first-party proof | hard (max one per week) | E, or A when a China signal is live and the trek is inside 8 weeks |

Three posts, three different archetypes. Selection rules are in
`references/post-archetypes.md`, under "Choosing the archetype for a slot". Full funnel and CTA
detail is in `references/funnel-and-cta.md`.

### Step 3. Find and verify the stories

1. Check the unused candidates the rotation check listed from `data/news-seen.csv` before
   searching. Someone already did that work.
2. Search for at least three candidates per archetype in play. WebSearch to find, WebFetch on the
   primary source to verify. Trade press is fine, aggregators are not, for numbers.
3. A story is a candidate only if the specific numbers can be read in the article. Quote the
   sentence into your working notes for every number that will appear in a draft.
4. Drop any story whose `story_key` or `source_url` is already in `data/news-seen.csv` as posted
   or scheduled.
5. Archetype E needs no external story. It needs something OJV actually did. If nothing is on
   file, ask the author what happened this month rather than inventing a room.

### Step 4. Draft

Draft the copy first, before touching images. Skeletons and worked examples are in
`references/post-archetypes.md`. Voice and style rules are in `references/brand-voice.md`.

Every draft goes to `drafts/YYYY-WW/<post_id>-archetype<X>-<slug>.md` with front matter, the
copy, the image, alt text, the source, the verified facts, and the guardrail notes. Copy the
shape of the existing drafts in `drafts/2026-W37/`.

### Step 5. Assign an image, or ask for one

The image supports the post, so pair after the copy is finished, never before.

1. Filter `assets/images/manifest.csv` by the archetype, drop anything the rotation check locked,
   drop anything tagged `consent-needed` unless the author has cleared it, and sort coldest first.
2. Check the shortlist against what the finished copy actually claims. Tagged for the archetype is
   not the same as right for the post.
3. Write alt text for the selection.

**If nothing fits, ask the author.** Do not force a pair and do not silently go text-only. Print
this and stop for a reply:

```
PHOTO NEEDED for <post_id> (<archetype>, <day>)

The post says   : <one line on what the copy claims>
Nothing in the library fits because: <reason>
Please attach   : <subject, setting, framing, whether a partner should be in frame>
Example         : "mid-shot of a components stall in Huaqiangbei, trays of actuators in focus,
                   stall depth visible behind, no faces, eye level"
Or reply "text only" and this post ships without an image.
```

If the author attaches a photo, run the image intake workflow on it first so it is described,
tagged and in the manifest, then pair it and write alt text.

Archetype E is the exception: it requires an image, because the post is a claim about a room that
happened. Text only is not an acceptable fallback for E.

### Step 6. Tag the links

Every outbound link, every time:
`?utm_source=linkedin&utm_medium=organic&utm_campaign=<archetype>-<post_id>`

The tagged link goes in the draft. The untagged URL goes in the calendar's `source_url`.

### Step 7. Run the gates

```bash
python3 scripts/style-gate.py drafts/YYYY-WW/*.md
```

It exits non-zero on failure. Fix the draft, never the gate. Then read each draft against
guardrails 1 to 7 below, which no script can check.

### Step 8. Write the scheduling handoff

This is what the author actually uses. Produce both:

1. `drafts/YYYY-WW/SCHEDULE.md`, a checklist with one block per post: the date and time, the
   plain copy, the image filename, the alt text, the first comment, and a tick box.
2. `drafts/YYYY-WW/paste/<post_id>.txt`, the copy alone, plain text, no markdown, no headings,
   nothing to strip. The author selects all and copies.

Copy the format of `drafts/2026-W37/SCHEDULE.md`.

### Step 9. Update the trackers

- `data/content-calendar.csv`: one row per post, `status=draft`, including `hook_pattern` and
  `entities`, which is what makes next week's rotation check work. A missing `entities` value
  silently breaks repetition control.
- `data/news-seen.csv`: every story considered, posted or not. Unused candidates with a note on
  why are worth as much as used ones.

### Step 10. Print the run summary

The format is at the end of this file. Print it every time.

---

## Other things to ask for

### Post from a news URL
WebFetch it. If it fails or is paywalled, say so and stop, do not draft from a headline. Extract
the verifiable specifics, pick the archetype from the input-trigger table, check `news-seen.csv`,
then run steps 4 to 10 for that single post.

### Post from an image
If the image is not in the manifest, intake it first. Read its `archetypes` column and pick one it
can actually carry. An image alone is not a post, so either the author supplies the angle or you
find a story that fits the archetype. Draft, then confirm the image still fits the finished copy.

### Intake images
1. Read the raw image folder from the config table. If it is `TODO`, ask for the path and stop.
2. List files not already in `assets/images/manifest.csv`, matched on filename. Report the count.
3. Copy them into `assets/images/raw/`. Never modify the originals.
4. Look at each one with the Read tool and write a description, tags, archetypes, people and
   notes, per `references/image-intake.md`.
5. Never guess a city. Never name a person you are not sure of. Flag anything unusable.
6. Append one row per image with `used_on` and `post_id` empty. Print what was added.

### Log performance
Numbers come from the author or from the page with the browser tools. Never estimate one.
Append to `data/posted-log.csv` including `hook_pattern` and `entities`, move the calendar row to
`status=posted`, set `used_on` and `post_id` on the images that shipped, append inbound enquiries
to `data/leads.csv` with `source_post_id` and `keyword_used`, then report enquiries per post by
archetype and CTA tier.

### Monthly review
Rank the five archetypes by enquiries per post, then comments per post. Print the sample size next
to every rank, and label anything under 3 posts as no signal. Check the shipped value-to-offer
ratio against the 2:1 target. Flag hook patterns used more than 3 times or with falling median
impressions. Recommend next month as a concrete slot allocation. Report images used more than
twice and how much of the library has never been used.

---

## Config

Fill every `TODO` before the first hard-CTA post. Soft and medium posts can be drafted without
them.

| Setting | Value |
| --- | --- |
| Company page URL | https://www.linkedin.com/company/orange-juice-ventures/ |
| Posting cadence | 3 per week, Monday / Wednesday / Friday, 09:00 HKT |
| Current flagship offer | China Tech Trek, Hong Kong and Shenzhen, 13 to 17 October 2026, run with ContraVC as official partner |
| Enquiry destination | `TODO` (form or calendar link) |
| DM keyword for tour enquiries | `TODO` (suggested: **TREK**) |
| Raw image folder | `TODO` (absolute path; drop unlabelled photos here) |
| Approver | Naman. Every post reviewed before it is scheduled. |
| Publishing method | `TODO` (manual paste, Buffer, or Taplio) |
| ContraVC published source | `TODO` (site or LinkedIn page URL, needed for guardrail 5) |
| Naman's personal profile URL | `TODO` (for posts routed to the personal voice) |
| UTM base | `utm_source=linkedin&utm_medium=organic&utm_campaign=<archetype>-<post_id>` |

Paths are relative to this skill directory.

## Layout

```
HANDOFF.md                       read this first if you are new
SKILL.md                         this file
scripts/rotation-check.py        what the week cannot repeat. Run before researching.
scripts/style-gate.py            runnable style check, exits non-zero
references/brand-voice.md        researched voice rules, style rules, personal vs company voice
references/post-archetypes.md    the five archetypes, selection logic, skeletons, examples
references/funnel-and-cta.md     four-stage funnel, CTA ladder, weekly pattern, mechanics
references/image-intake.md       tag vocabulary, rotation, alt-text rules, pairing rule
references/publish-adapter.md    OPTIONAL, OFF BY DEFAULT. LinkedIn API state, manual handoff.
data/content-calendar.csv        planned and drafted posts
data/posted-log.csv              what went out and how it performed
data/leads.csv                   inbound enquiries attributed to a post
data/news-seen.csv               story deduplication
assets/images/manifest.csv       tagged image library
assets/images/raw/               library copies of images
drafts/YYYY-WW/                  drafts, SCHEDULE.md, paste/
```

## The five archetypes

| | Archetype | Native tier | Input trigger |
| --- | --- | --- | --- |
| A | China signal to tour | awareness to interest | Dated China deep-tech news with a checkable number |
| B | West into Asia | interest to consideration | US or European company with documented traction in Asia, and a named mechanism |
| C | Asia into the West | interest to consideration | Asian company with documented traction in the West, and a named mechanism |
| D | Rejection to raise | interest to consideration | A documented rejection count and a documented raise |
| E | Inside the room | interest to enquiry | Something OJV actually did: event, workshop, portfolio move, partner on stage, trek update |

## How repetition is prevented

Not by memory. By `scripts/rotation-check.py` reading what is on file. It blocks:

| Blocked | Window | Source of truth |
| --- | --- | --- |
| The same archetype twice in one week | the week | calendar + posted log |
| The same archetype in the same slot 3 weeks running | 3 weeks | calendar + posted log |
| The same hook pattern | 14 days | `hook_pattern` column |
| The same company, person or city as a post's subject | 90 days | `entities` column |
| The same story, ever | forever | `data/news-seen.csv` |
| The same image | 60 days, and a hard stop at 3 uses | manifest `used_on` plus scheduled posts |

This only works if step 9 is done properly. **A post logged without `hook_pattern` and
`entities` is invisible to next week's check.** Fill both, every time.

## Guardrails

Run these on every draft. Report the result in the run summary.

1. **No fabrication.** Never invent a statistic, funding number, rejection count, date or quote.
   Every number traces to a sentence in the linked source. If it cannot be verified, drop it or
   write around it. First-party numbers in archetype E are attributed in the copy and checked with
   the partner who owns them.
2. **No implied client relationship.** Third-party cases are commentary and the copy must say so
   in its own words. Archetype E is the mirror: claim only what OJV actually did. Co-hosted means
   co-hosted.
3. **No guaranteed outcomes**, especially archetype D. The claim is a shorter, better-targeted
   list, never the yes. Approved and banned phrasings are in `references/post-archetypes.md`.
4. **No investment advice**, no return projections, no valuation from rumour.
5. **ContraVC alignment.** Before any China Tech Trek post, check the ContraVC published source in
   the config table and confirm the draft does not contradict it on dates, cities, itinerary,
   pricing, capacity or positioning. If that source is `TODO` or unreachable, the draft may still
   be written, but the summary must carry `TREK POST UNVERIFIED AGAINST CONTRAVC` and the copy must
   not state itinerary specifics beyond the dates and cities in the config table.
6. **Never publish or schedule.** Not by API, not by driving the LinkedIn composer, not by pushing
   to a scheduler. Queuing counts as publishing, because a queued post goes out unattended. The
   author schedules, after approval.
7. **No named third party's face without consent.** A partner's face is fine. A stranger in a
   conference photo is not, unless the author confirms it.
8. **Style gate.** Run it, do not eyeball it:

   ```bash
   python3 scripts/style-gate.py drafts/YYYY-WW/*.md
   ```

   It checks em dashes, banned phrases, hook length, the 900 to 1,300 character band, hashtag count
   and placement, and question-plus-CTA closes. Fix the draft, do not weaken the gate. It cannot
   check sourcing, disclosure or tone, so guardrails 1 to 7 still need a human read.

## Error handling

| Situation | Do this |
| --- | --- |
| A config value needed for the run is `TODO` | Draft everything that does not depend on it, leave a literal `TODO(config: <setting>)` marker at the exact spot in the copy, and list it in the summary. Only stop outright if the whole workflow depends on it, such as intake with no raw image folder. |
| The rotation check blocks every archetype that fits the available news | Say so, and take the least-bad option in this order: use an unused candidate already on file; run archetype E from something OJV did; ship two posts instead of three. Never unblock yourself. |
| WebFetch returns 999, 403 or a login wall (normal for LinkedIn) | Do not draft from the headline. Try the publisher's own domain, or a country subdomain for public LinkedIn pages such as `hk.linkedin.com/in/<slug>`. Then the signed-in browser tools. If still blocked, report the URL unverifiable and pick another story. |
| A number is in aggregator coverage but not the primary source | Cut the number. |
| The story is already in `news-seen.csv` as posted or scheduled | Stop, name the earlier `post_id` and date, offer the next candidate. |
| No image fits the finished copy | Print the PHOTO NEEDED block in step 5 and wait. Never force a pair. |
| The author cannot supply a photo | Ship text-only for A, B, C and D, and say so in the summary. For archetype E, change the post rather than dropping the image. |
| The only fitting image is inside the 60-day window | Report the conflict with the last-used date and offer the next best image or text-only. Never silently reuse. |
| A CSV is missing or its header does not match | Recreate it from the header spec below, say that you did, and never overwrite existing rows. |
| Fewer than 3 verified stories for the week | Ship what is verified. Say which slot is empty and why. |
| The author asks for a second hard CTA in one week | Refuse it, explain the one-hard-CTA rule, offer next Friday. |
| A draft's facts cannot be verified at all | Do not write the file. Report the gap. |
| The author asks you to post or schedule it | Decline, per guardrail 6, and point at `drafts/YYYY-WW/SCHEDULE.md`. |

## Data file headers

Create with exactly these headers. Do not reorder.

- `data/content-calendar.csv`
  `post_id,scheduled_date,slot,archetype,funnel_tier,hook,hook_pattern,entities,status,image,cta_tier,source_url,draft_path`
- `data/posted-log.csv`
  `post_id,posted_date,archetype,cta_tier,hook_pattern,entities,impressions,reactions,comments,reposts,dm_enquiries,link_clicks,notes`
- `data/leads.csv`
  `date,name,headline,company,source_post_id,keyword_used,stage,owner,notes`
- `data/news-seen.csv`
  `date_seen,story_key,source_url,archetype,posted,post_id,notes`
- `assets/images/manifest.csv`
  `filename,description,tags,archetypes,people,used_on,post_id,notes`

`post_id`: `OJV-YYYYWW-<M|W|F>`, for example `OJV-202637-F`. `status`: `draft`, `approved`,
`scheduled`, `posted`, `killed`. `cta_tier`: `soft`, `medium`, `hard`. `funnel_tier`: `awareness`,
`interest`, `enquiry`, `booked`. `entities` and `hook_pattern` are semicolon separated.
`hook_pattern` values: `reframe`, `by-design`, `contrarian-bet`, `local-claim-broken`,
`number-first`, plus any new one added to `references/brand-voice.md` in the same run.

## Run summary

Print this at the end of every run. No exceptions.

```
OJV LINKEDIN RUN SUMMARY
Week          : <ISO week>   Slots: <Mon date> / <Wed date> / <Fri date>
Rotation check: <n> archetypes blocked, <n> entities blocked, <n> hook patterns blocked
Drafts written: <n>  ->  <paths>

| Day | Post ID | Archetype | Funnel | CTA | Hook (first 140 chars) | Image | Source |
|-----|---------|-----------|--------|-----|------------------------|-------|--------|

Guardrail check : PASS / FLAGGED   <one line per flag>
Style gate      : PASS / FAIL      <which rule, which draft>
Sources verified: <n>/<n>          <any unverified, named>
Photos          : <n> assigned, <n> awaiting the author, <n> text-only
Config TODOs hit: <settings, or none>
Trackers updated: <files and row counts>

READY TO SCHEDULE, NOT SCHEDULED.
Author's next steps:
  1. Read drafts/<week>/SCHEDULE.md
  2. Approve or amend the three posts
  3. <anything blocking: a photo, a config value, a first-party number to confirm>
  4. Schedule in LinkedIn at 09:00 HKT, paste files are in drafts/<week>/paste/
```
