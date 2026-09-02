# OJV LinkedIn posting skill and one-button tool

Two things in one repo, for Orange Juice Ventures' LinkedIn company page.

| | What it is | Who uses it |
| --- | --- | --- |
| **`skill/`** | A Claude Code skill. The full weekly workflow: rotation control, five archetypes, image manifest, CSV trackers, guardrails. | Naman, or anyone working in Claude Code |
| **`api/` + `public/`** | A one-button web tool deployed on Vercel. Press it, get three scheduling-ready posts. | The intern |

Both draft only. **Neither publishes, schedules, or sends a DM.** Posts are scheduled by a person, on LinkedIn, after Naman approves them.

---

## The web tool

One button. It runs four short steps so no single request has to hold everything:

1. **Rotation check.** Reads the saved history in the browser and works out what this week may not repeat: archetypes, hook patterns, subjects used in the last 90 days, and stories already posted.
2. **Research.** Claude searches the web, opens primary sources, and picks one verified story per slot. Every number it keeps must be quotable from the source it opened.
3. **Drafting.** One call per post. Monday awareness with a soft close, Wednesday proof with a medium CTA, Friday the week's single hard CTA.
4. **Photos.** Licence-free options from Openverse, falling back to Wikimedia Commons. Both keyless.

Then the intern copies each post, picks or attaches a photo, and schedules it on LinkedIn.

### The five archetypes

Every post is exactly one of these, chosen from what the research actually found.

| | Archetype | Triggered by |
| --- | --- | --- |
| A | China signal to tour | Dated China deep-tech news with a checkable number |
| B | West into Asia | A US or European company with documented traction in Asia, and a named mechanism |
| C | Asia into the West | The mirror case |
| D | Rejection to raise | A documented rejection count and a documented raise |
| E | Inside the room | Something OJV actually did: event, workshop, portfolio, partner on stage |

Archetype E is Friday's default and it is the only one where OJV is the subject. It needs the **"what has OJV done lately"** box filled in, because it cannot be researched from the web. If that box is empty the tool says so rather than inventing an OJV event.

### Photos, and why some posts ask the intern for one

Stock photography is only offered where a generic scene can honestly illustrate the post. The tool asks the intern for a photo instead whenever the post is about OJV, a partner, or an event, because a stock photo of a stranger in a conference hall standing in for an OJV room is a misrepresentation, not a design shortcut.

Nothing is AI-generated. A synthetic image of a factory floor presented as documentary evidence of what Shenzhen looks like would break the same rule the copy guardrails exist to enforce.

Licences: only `CC0`, public domain and `CC BY` are requested. `CC BY` results are flagged `credit needed` and the tool prints the exact credit line to put in the first comment.

### How it avoids repeating itself

History lives in the intern's browser (`localStorage`) and is fed into the research step as hard blocks:

| Blocked | Window |
| --- | --- |
| The same archetype twice in a week | the week |
| The same hook pattern | 14 days |
| The same company, person or city as a post's subject | 90 days |
| The same story | forever |

This only works if the intern presses **Mark scheduled** on each post. That is the whole feedback loop. **Download log** exports rows for `skill/data/posted-log.csv` so the Claude Code skill and the web tool share one memory.

Browser storage is per-device, so it is a real limitation: a different laptop starts with a blank history. Moving this to Vercel KV or Postgres is the obvious next step.

---

## Deploying it

### 1. Import the repo into Vercel

Go to [vercel.com/new](https://vercel.com/new), pick this repository, and deploy. No build step, no framework preset. Vercel serves `public/` and turns `api/*.js` into functions on its own.

### 2. Set two environment variables

In **Project Settings, Environment Variables**:

| Name | Value |
| --- | --- |
| `ANTHROPIC_API_KEY` | An Anthropic API key from [console.anthropic.com](https://console.anthropic.com) |
| `APP_PASSWORD` | Any long random string. This is what the intern types. |

Optional: `OJV_MODEL` overrides the model, which defaults to `claude-opus-5`.

Redeploy after adding them. The tool refuses to run with either one missing, rather than failing halfway through a run.

### 3. Send the intern the URL and the password

They type the password once and the browser remembers it.

### Cost

Every press of the button is one research call plus three drafting calls against `claude-opus-5` with web search enabled. Budget on the order of a couple of dollars per week at three posts a week, and set a spend limit in the Anthropic console. The password gate exists mainly so that a public URL cannot burn credits.

### Local development

```bash
npm install
cp .env.example .env.local   # fill in both values
npx vercel dev
```

---

## The Claude Code skill

Everything under `skill/`. Start with [`skill/HANDOFF.md`](skill/HANDOFF.md), which is one page. [`skill/SKILL.md`](skill/SKILL.md) has the config table, the ten-step weekly run, the guardrails and the error table.

Two runnable checks:

```bash
python3 skill/scripts/rotation-check.py            # what this week may not repeat
python3 skill/scripts/style-gate.py skill/drafts/2026-W37/*.md
```

`skill/drafts/2026-W37/` is a worked week, including a post deliberately held back because no image in the library could carry it honestly.

The skill is the source of truth for voice and archetypes. `api/_voice.js` is a condensed copy of it for the web tool. **If you change the voice in `skill/references/`, update `api/_voice.js` too.**

---

## Guardrails, enforced in both halves

- No invented statistic, funding number, rejection count, date or quote. Every number traces to a source that was actually opened.
- No implied client relationship. Third-party cases carry an explicit disclosure line in the body.
- No guaranteed fundraising outcome. The claim is a shorter, better-targeted investor list, never the yes.
- No investment advice, no return projections, no valuation from rumour.
- Nothing about the China Tech Trek that contradicts ContraVC, who are the official partner on it.
- No em dashes, no "thrilled to announce", 3 to 5 hashtags, 900 to 1,300 characters, hook inside 140 characters, and a close that is a question or a CTA but never both. Checked mechanically by `skill/scripts/style-gate.py` and by the same rules in `api/_lib.js`.

## Why there is no publish button

Posting to a LinkedIn company page programmatically needs the Community Management API: a registered legal entity, a verified page, the Marketing Developer Platform partner programme, the `w_organization_social` scope, and a two-tier app review with a screen recording. Approval runs weeks to months.

So this tool hands a person a finished post and that person schedules it. Queuing into a scheduler counts as publishing, because a queued post goes out unattended. See [`skill/references/publish-adapter.md`](skill/references/publish-adapter.md).

---

## Tests

```bash
cd test && node handlers.mjs
```

Exercises the auth gate, request routing, the live Creative Commons photo search including query
relaxation, the licence filter, and the style gate's parity with `skill/scripts/style-gate.py`.
It does not call Claude, so it needs no API key and costs nothing. 16 checks.
