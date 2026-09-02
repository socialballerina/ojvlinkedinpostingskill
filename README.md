# OJV LinkedIn posting skill and one-button tool

Weekly LinkedIn content for Orange Juice Ventures' company page. Three posts a week, Monday,
Wednesday and Friday, 09:00 HKT.

**There is no Anthropic API key anywhere in this repo.** The model is Claude Code itself, running
in GitHub Actions, authenticated by an OAuth token tied to a Claude subscription. Vercel only
starts the run and shows the results.

```
  intern presses the button
        |
  Vercel  POST /api/run ......... dispatches the workflow
        |
  GitHub Actions ................ runs Claude Code with the ojv-linkedin skill,
        |                         billed to the Claude subscription
        |                         commits runs/<id>/result.json back to this repo
        |
  Vercel  GET /api/status ....... polls for that file
        |
  intern copies each post, picks or attaches a photo, and schedules it on LinkedIn
```

Nothing publishes. A person schedules every post after Naman approves it.

---

## Setup

Two credentials, and only you can create them. Everything else is done.

### 1. The Claude token, required

The Claude Code CLI is installed. On this machine:

```bash
claude setup-token
```

It prints a long-lived token (`sk-ant-oat01-...`) tied to your Claude subscription. Add it as a
repository secret:

```bash
gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo socialballerina/ojvlinkedinpostingskill
```

Paste when prompted; it does not echo. Requires a Pro, Max, Team or Enterprise plan. Runs are
billed to that subscription, not to API credits. Also install
[github.com/apps/claude](https://github.com/apps/claude) on the repository.

Until this exists, a run fails on its first step and the page says exactly that, rather than
failing somewhere deep inside the action. Verified.

### 2. A GitHub token for the button, optional

Without it, the workflow still runs on its Thursday schedule and the page still shows the result,
because the repository is public and results are readable with no credential. The token only
enables the on-demand button.

Create a **fine-grained** token at
[github.com/settings/personal-access-tokens/new](https://github.com/settings/personal-access-tokens/new),
scoped to this repository only:

| Permission | Access |
| --- | --- |
| Actions | Read and write |
| Contents | Read-only |

Add it in Vercel, Project Settings, Environment Variables, as `GITHUB_TOKEN`, then redeploy.

`APP_PASSWORD` is already set.

### Cost

GitHub Actions minutes are free on a public repository. Model usage comes out of the Claude
subscription that issued the OAuth token, so there is no per-click API bill. A run is one Claude
Code session, roughly 5 to 12 minutes.

---

## Using it

One button. It dispatches the workflow, then polls. The tab can be closed while the run goes; the
run id is kept in the browser and reconnects on return. On load, the page shows the most recent
result there is, so there is usually something to look at before pressing anything.

The workflow also runs itself every Thursday at 10:00 HKT, so next week's three drafts exist
before Monday whether or not anyone presses the button.

Each finished post shows the copy, the archetype and CTA tier, the source link, the style-gate
result, whether the sources were verified, and either photo options or a request for a photo.

### The five archetypes

Every post is exactly one of these, chosen from what the research actually found.

| | Archetype | Triggered by |
| --- | --- | --- |
| A | China signal to tour | Dated China deep-tech news with a checkable number |
| B | West into Asia | A US or European company with documented traction in Asia, and a named mechanism |
| C | Asia into the West | The mirror case |
| D | Rejection to raise | A documented rejection count and a documented raise |
| E | Inside the room | Something OJV actually did: event, workshop, portfolio, partner on stage |

Archetype E is Friday's default and the only one where OJV is the subject. It needs the
**"what has OJV done lately"** box filled in, because it cannot be researched from the web. Leave
it empty and the run says so in `needsFromAuthor` rather than inventing an OJV event. Top it up
monthly.

### Photos

Stock is only offered where a generic scene can honestly illustrate the post, searched from
Openverse with Wikimedia Commons as a fallback. Both keyless. Only `CC0`, public domain and
`CC BY` are requested, and `CC BY` results are flagged with the exact credit line to put in the
first comment.

The run asks the intern for a photo instead whenever the post is about OJV, a partner or an event,
because a stock photo of a stranger standing in for an OJV room is a misrepresentation rather than
a design shortcut. Archetype E always asks, and has no text-only fallback.

Nothing is AI-generated. A synthetic factory floor presented as what Shenzhen looks like would
break the same rule the copy guardrails exist to enforce.

### How it avoids repeating itself

The skill's own rotation check reads the trackers committed in this repo:

| Blocked | Window | Source of truth |
| --- | --- | --- |
| The same archetype twice in a week | the week | `data/content-calendar.csv` |
| The same archetype in the same slot 3 weeks running | 3 weeks | calendar and posted log |
| The same hook pattern | 14 days | `hook_pattern` column |
| The same company, person or city as a post's subject | 90 days | `entities` column |
| The same story | forever | `data/news-seen.csv` |
| The same image | 60 days, hard stop at 3 uses | `assets/images/manifest.csv` |

Because each run commits its updated trackers and drafts back to this repo, the memory is shared
and durable rather than living in one browser. **Download log** exports rows for
`data/posted-log.csv` once posts have actually run, which is what feeds performance back in.

---

## The skill

`.claude/skills/ojv-linkedin/`. Clone this repo, open Claude Code in it, and the skill is
available: say "run the week", or `/ojv-linkedin`. That path is also how the GitHub Actions run
invokes it, so the web tool and a local Claude Code session execute exactly the same instructions.
There is no second copy of the voice rules to drift.

Start with [`HANDOFF.md`](.claude/skills/ojv-linkedin/HANDOFF.md), which is one page.
[`SKILL.md`](.claude/skills/ojv-linkedin/SKILL.md) has the config table, the ten-step weekly run,
the guardrails and the error table.

Two runnable checks:

```bash
python3 .claude/skills/ojv-linkedin/scripts/rotation-check.py
python3 .claude/skills/ojv-linkedin/scripts/style-gate.py .claude/skills/ojv-linkedin/drafts/2026-W37/*.md
```

`drafts/2026-W37/` is a worked week, including a post deliberately held back because no image in
the library could carry it honestly.

---

## Guardrails

- No invented statistic, funding number, rejection count, date or quote. Every number traces to a
  source that was actually opened.
- No implied client relationship. Third-party cases carry an explicit disclosure line in the body.
- No guaranteed fundraising outcome. The claim is a shorter, better-targeted investor list, never
  the yes.
- No investment advice, no return projections, no valuation from rumour.
- Nothing about the China Tech Trek that contradicts ContraVC, who are the official partner on it.
- No em dashes, no "thrilled to announce", 3 to 5 hashtags, 900 to 1,300 characters, hook inside
  140 characters, and a close that is a question or a CTA but never both.

The style rules are checked mechanically by `scripts/style-gate.py` inside the run, and again by
`api/_lib.js` before the page renders anything, so the UI never simply trusts the run's own claim.

## Why there is no publish button

Posting to a LinkedIn company page programmatically needs the Community Management API: a
registered legal entity, a verified page, the Marketing Developer Platform partner programme, the
`w_organization_social` scope, and a two-tier app review with a screen recording. Approval runs
weeks to months.

So the tool hands a person a finished post and that person schedules it. Queuing into a scheduler
counts as publishing, because a queued post goes out unattended. See
[`publish-adapter.md`](.claude/skills/ojv-linkedin/references/publish-adapter.md).

## Tests

```bash
cd test && node handlers.mjs
```

22 checks over the auth gate on every endpoint, method guards, input validation, GitHub error
reporting, credential-free reads of the public repo, the live Creative Commons photo search with
query relaxation and licence filtering, and the style gate's parity with the skill's Python gate.
No credentials needed, nothing billed.

The pipeline itself was verified by dispatching real workflow runs with `dry_run=true`, which
skips Claude and writes a synthetic result. To repeat it:

```bash
gh workflow run generate-week.yml --repo socialballerina/ojvlinkedinpostingskill \
  -f run_id="dryrun-$(date -u +%Y%m%d-%H%M%S)" -f dry_run=true
```

That exercises dispatch, the running marker, the commit and push with retry, the result
validation, the pruning, and the poll path, without spending a Claude run.

## Notes

- `runs/` accumulates one folder per run, committed to this repo. It is a public repository, so
  drafts are publicly visible. Delete old folders freely; nothing reads them after the intern has
  scheduled the posts.
- Only one run at a time. `/api/run` returns 409 if a run is already going, so two presses of the
  button cannot both push to `main` and collide.
