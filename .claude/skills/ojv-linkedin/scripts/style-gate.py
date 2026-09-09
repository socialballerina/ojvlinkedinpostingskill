#!/usr/bin/env python3
"""Style gate for OJV LinkedIn drafts.

Usage: python3 scripts/style-gate.py drafts/2026-W37/*.md

Checks the `## Copy` block of each draft against the style rules in
references/brand-voice.md. Exits 1 if any draft fails, so it can gate a run.
Advisory only for judgement calls: it cannot check sourcing or tone.
"""
import re
import sys

BANNED = [
    "thrilled to announce", "excited to announce", "proud to announce",
    "game-changer", "game changer", "in today's fast-paced world",
    "revolutionizing", "revolutionising", "stay tuned",
    "underscores our dedication", "we look forward to supporting",
    "excited to share",
]
# The close is fixed. Both halves are mandatory and the wording does not vary.
CONTACT = "DM us, or write to us at hello@oj.ventures"
ASK = "work with us"


def check(path):
    text = open(path).read()
    if "## Copy" not in text:
        return ["no '## Copy' block found"]
    tail = text.split("## Copy", 1)[1]
    for marker in ("## Image", "## Photo brief"):
        tail = tail.split(marker, 1)[0]
    body = tail.strip()
    lines = [l for l in body.split("\n") if l.strip()]
    if not lines:
        return ["empty copy block"]

    hook = lines[0]
    tags = re.findall(r"#\w+", body)
    fails = []

    if "—" in body:
        fails.append("em dash present")
    for b in BANNED:
        if b in body.lower():
            fails.append("banned phrase: %s" % b)
    if len(hook) > 140:
        fails.append("hook is %d chars, limit 140" % len(hook))
    if not 900 <= len(body) <= 1450:
        fails.append("length %d chars, band is 900 to 1450" % len(body))
    if not 3 <= len(tags) <= 5:
        fails.append("%d hashtags, band is 3 to 5" % len(tags))
    if tags:
        tail = body.rstrip().split("\n")[-1]
        if not tail.strip().startswith("#"):
            fails.append("hashtags are not on the final line")

    # --- the mandatory close ---
    # Every post ends with the qualified ask, then the contact line, then at most a
    # source line and the hashtags. See references/post-archetypes.md.
    if CONTACT not in body:
        fails.append("no contact line: %r must appear in the close" % CONTACT)
    else:
        idx = max(i for i, l in enumerate(lines) if CONTACT in l)
        trailing = lines[idx + 1:]
        stray = [l for l in trailing
                 if not l.lstrip().startswith("#") and not l.lstrip().startswith("Source:")]
        if stray:
            fails.append("%d line(s) after the contact line: %r"
                         % (len(stray), stray[0][:60]))
        if idx == 0:
            fails.append("contact line has no ask above it")
        else:
            ask = lines[idx - 1]
            if ASK not in ask.lower():
                fails.append("the line above the contact line is not an ask (%r)" % ask[:60])
            elif ask.lstrip().lower().startswith("work with us"):
                fails.append("bare 'Work with us' ask, needs the 'If you want ...' qualifier")
        for l in lines[:idx + 1]:
            if l.rstrip().endswith("?") and l is lines[idx]:
                fails.append("the close is a question")
    if lines[-1].lstrip().startswith("#") and len(lines) > 1:
        last_prose = lines[-2]
    else:
        last_prose = lines[-1]
    if last_prose.rstrip().endswith("?"):
        fails.append("post ends on a question; the close must be the ask")

    inline = [t for t in tags if body.split(t)[0].rstrip().endswith((".", ",", "and", "in"))
              and not body.split(t)[0].rstrip().endswith("\n")]
    if len(re.findall(r"\w\s#\w+\s+\w", body)) > 0:
        fails.append("hashtag appears mid-sentence")

    return fails


def main(paths):
    # SCHEDULE.md and QUEUE files are handoff checklists, not drafts. Skip them so a
    # glob over a drafts directory does not report a spurious failure.
    paths = [p for p in paths
             if not p.split("/")[-1].upper().startswith(("SCHEDULE", "QUEUE"))]
    if not paths:
        print("no draft files to check")
        return 0
    bad = 0
    for p in paths:
        fails = check(p)
        name = p.split("/")[-1]
        if fails:
            bad += 1
            print("FAIL  %s" % name)
            for f in fails:
                print("        %s" % f)
        else:
            print("PASS  %s" % name)
    print("\n%d of %d drafts pass the style gate." % (len(paths) - bad, len(paths)))
    return 1 if bad else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
