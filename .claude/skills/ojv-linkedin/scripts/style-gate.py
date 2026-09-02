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
]
CTA_MARKERS = ("Comment ", "DM ", "Enquiries", "Follow the page", "utm_")


def check(path):
    text = open(path).read()
    if "## Copy" not in text:
        return ["no '## Copy' block found"]
    body = text.split("## Copy", 1)[1].split("## Image", 1)[0].strip()
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
    if not 900 <= len(body) <= 1300:
        fails.append("length %d chars, band is 900 to 1300" % len(body))
    if not 3 <= len(tags) <= 5:
        fails.append("%d hashtags, band is 3 to 5" % len(tags))
    if tags:
        tail = body.rstrip().split("\n")[-1]
        if not tail.strip().startswith("#"):
            fails.append("hashtags are not on the final line")

    close = lines[-2] if lines[-1].lstrip().startswith("#") else lines[-1]
    has_q = close.rstrip().endswith("?")
    has_cta = any(m in close for m in CTA_MARKERS)
    if has_q and has_cta:
        fails.append("close carries both a question and a CTA")

    inline = [t for t in tags if body.split(t)[0].rstrip().endswith((".", ",", "and", "in"))
              and not body.split(t)[0].rstrip().endswith("\n")]
    if len(re.findall(r"\w\s#\w+\s+\w", body)) > 0:
        fails.append("hashtag appears mid-sentence")

    return fails


def main(paths):
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
