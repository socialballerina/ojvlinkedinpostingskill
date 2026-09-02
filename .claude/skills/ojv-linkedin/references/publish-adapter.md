# Publish Adapter (OPTIONAL, OFF BY DEFAULT)

This file is deliberately separate from the drafting workflow. Nothing in `SKILL.md` calls it.
The engine is draft-first and stays draft-first even if this adapter is configured.

## State of LinkedIn company-page posting, as of September 2026

Posting to a LinkedIn company page programmatically requires the **Community Management API**,
which is not open to individual developers. Confirmed requirements:

- A registered legal entity, a verified business-domain email, a published privacy policy.
- A verified LinkedIn Company Page, with an admin role, associated with the app.
- Membership of the Marketing Developer Platform partner program.
- The `w_organization_social` scope for publishing as an organization.
- A **two-tier app review**. Standard Tier, the one needed for live production use, requires a
  separate access request and a screen recording demonstrating every stated use case.
- Approval takes weeks to months. Access is revoked if Standard Tier is not applied for within
  twelve months.

Sources:
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management-app-review
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-api-migration-guide

**Consequence for this skill.** OJV has no approved app and no credentials in the config table.
So there is no automatic publish path, and the skill must not pretend otherwise. It does not
attempt an API call, does not drive the LinkedIn composer with browser automation, and does not
schedule anything.

## The default handoff: manual paste

This is what happens today, and it is the recommended path at 3 posts per week.

1. The skill writes drafts and prints the run summary.
2. Naman reviews and approves in the conversation.
3. Naman copies the copy block out of the draft file, attaches the named image, pastes the alt
   text into LinkedIn's own alt-text field, and posts or schedules natively at 09:00 HKT.
4. The link, if any, goes in the first comment.
5. Naman moves the calendar row to `status=posted`, or asks the skill to do it.

LinkedIn's native scheduler covers a Monday, Wednesday, Friday 09:00 HKT cadence without any
tooling, so a third-party scheduler is a convenience, not a requirement.

## If a third-party scheduler is configured

Set `Publishing method` in the config table to `Buffer` or `Taplio`. Both hold approved LinkedIn
partner access, which is what makes them work where a self-built app would not.

The adapter's contract in that case:

- The skill's output stays identical: markdown drafts plus the run summary.
- The skill **may** produce a paste-ready block per post (copy, image filename, alt text, first
  comment, scheduled datetime in HKT) to reduce transcription errors.
- The skill still does not push to the scheduler's API unless the user has, in that same
  conversation, both configured credentials and explicitly asked for that post to be sent.
- Queuing into a scheduler counts as publishing, because a queued post goes out unattended. It
  therefore needs the same explicit approval as posting, per guardrail 6.

## If Community Management API access is ever granted

Do not implement it inside this skill. Write it as a separate script, invoked by hand, taking an
approved draft path as its argument, and require a `--confirm` flag plus the post ID printed back
for confirmation. Keep the credential outside the skill directory and outside the repo.

Minimum preconditions before any line of that code is written:
1. Standard Tier approval in hand for the specific use case "publishing OJV's own marketing
   content to OJV's own page".
2. `w_organization_social` granted, with Naman's admin role on page 106737084 confirmed.
3. A written rule for what happens on a failed post, so a retry loop cannot double-post.
4. Naman's explicit sign-off that per-post approval is still required. The guardrail does not
   lapse because the API exists.
