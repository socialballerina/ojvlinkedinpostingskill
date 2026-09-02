# Image Intake, Tagging and Pairing

The raw material is deliberately unlabelled: photos from China's ecosystem, factory floors,
robotics showrooms, conference halls, city shots, and photos of the four partners. Intake turns
that pile into a library that can be queried by archetype.

## Manifest

`assets/images/manifest.csv`

`filename,description,tags,archetypes,people,used_on,post_id,notes`

| Column | Rule |
| --- | --- |
| `filename` | As copied into `assets/images/raw/`. The join key. Never renamed after intake. |
| `description` | One factual sentence about what is visible. No mood words, no interpretation. |
| `tags` | Semicolon separated, from the vocabulary below. |
| `archetypes` | Semicolon separated from `A;B;C;D;BTS`. `BTS` is behind-the-scenes. Empty means the image carries no archetype and is library filler. |
| `people` | Semicolon separated. Named partners only where confident, else `unknown`, `unidentified-others`, or `none`. |
| `used_on` | Semicolon separated ISO dates, appended each time the image ships. Empty until used. |
| `post_id` | Semicolon separated post IDs, in the same order as `used_on`. |
| `notes` | City-inference basis, quality problems, consent problems, anything disqualifying. |

## Tag vocabulary

Use these. Add a new tag only when nothing fits, and add it to this file in the same run.

**Subject:** `factory-floor` `robotics` `production-line` `hardware-market` `showroom`
`ev` `battery` `semiconductor` `drone` `lab` `product-closeup` `whiteboard` `screen`
**Setting:** `conference` `stage` `panel` `booth` `office` `workshop` `dinner` `street`
`skyline` `transport` `campus` `factory` `studio` `portrait-setting`
**City:** `hongkong` `shenzhen` `guangzhou` `shanghai` `beijing` `singapore` `hangzhou`
`city-unknown`
**People:** `jason-li` `lee-murphy` `daniel-csontos` `naman-tekriwal` `founders` `investors`
`crowd` `no-people` `unidentified-others`
**Mood:** `energetic` `focused` `formal` `candid` `scale` `gritty` `polished` `quiet`
**Quality flags:** `low-res` `blurred` `poor-light` `crop-needed` `logo-visible`
`screen-content-visible` `consent-needed`

## Which archetype an image can carry

| Archetype | Wants | Never |
| --- | --- | --- |
| A. China signal to tour | `factory-floor` `robotics` `production-line` `hardware-market` `showroom` `shenzhen` `guangzhou` `scale` `gritty` | A conference stage. An A post is about the ground, so a podium photo undercuts the copy. |
| B. West into Asia | `conference` `workshop` `panel` `skyline` of the target market, `founders` | A China factory floor. Wrong geography reads as careless. |
| C. Asia into the West | `conference` `stage` `portrait-setting` `founders`, Western city shots | A China-specific setting, for the same reason. |
| D. Rejection to raise | `portrait-setting` `workshop` `office` `focused` `quiet` `candid`, a partner alone or one to one | Crowds, celebration shots, and anything that reads as a victory lap over someone else's rejection. |
| BTS Friday | Any setting with a **named partner's face** | `no-people`. A behind-the-scenes post with no person in it is not behind the scenes. |

## Rotation rules

1. **60-day lockout.** An image whose most recent `used_on` is within 60 days of the scheduled
   date is unavailable. Report the conflict, do not override it silently.
2. **Twice is the flag.** Two entries in `used_on` means flag it in the run summary as
   `heavily used` and prefer anything else. Three is a hard stop unless the user overrides in the
   same message.
3. **Prefer cold.** Sort candidates by number of prior uses ascending, then by oldest `used_on`.
4. **Never two identical settings in one week.** Three conference-hall photos in one week makes
   the page look like it only attends events.
5. `consent-needed` images do not ship until the user confirms in the conversation.

## Pairing rule

**The image supports the post.** So:

1. Draft the copy first. Always.
2. Then filter the manifest by the archetype, exclude the 60-day window, sort cold-first.
3. Then check the shortlist against what the finished copy actually claims. An A post whose
   on-the-ground section is about component lead times wants a parts market, not a humanoid on a
   stage, even though both are tagged `A`.
4. If nothing fits, say so. Mark the draft `image: NEEDS SHOOT` and name the shot: subject,
   setting, framing, and whether a partner should be in it. For example: "Needed: mid-shot of a
   components stall in Huaqiangbei, trays of actuators or connectors in focus, no faces, taken
   at eye level so the density reads."
5. Never force a pair. A text-only post beats a post with a photo that contradicts it.

## Alt text

Every selected image gets alt text, written into the draft file. Rules:

- Describe what is in the frame, for someone who cannot see it. Do not editorialise, and do not
  restate the post's argument.
- 1 to 2 sentences, under roughly 200 characters.
- Name a partner if they are the subject and identifiable.
- Name the city only if the manifest recorded a basis for it.
- No "image of" or "photo of" prefix.
- If the image carries readable text that matters, include it.

Good: "Naman Tekriwal on stage at a Hong Kong conference, mid-sentence, a slide behind him
showing a market map of APAC."
Bad: "A photo showing the energy and opportunity of the APAC startup ecosystem."

## Intake safety

- Read the original files, never modify them. Work from the copies in `assets/images/raw/`.
- Never guess a city. Infer only from readable signage, a recognisable skyline, or a filename that
  states it, and record the basis in `notes`.
- Never name a person you are not confident about. `unidentified-others` is the correct answer,
  and a wrong name in a manifest becomes a wrong name in a caption.
- Flag `screen-content-visible` on any photo with a legible laptop, phone or presentation screen,
  and do not use it until the user confirms the content is publishable.
- Flag `logo-visible` where a third party's brand is readable, because an A or B post with
  another firm's logo in it implies a relationship.
