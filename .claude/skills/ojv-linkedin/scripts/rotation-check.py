#!/usr/bin/env python3
"""What this week is allowed to repeat, and what it is not.

Usage:  python3 scripts/rotation-check.py 2026-09-14
        python3 scripts/rotation-check.py            (defaults to next Monday)

Reads data/content-calendar.csv, data/posted-log.csv, data/news-seen.csv and
assets/images/manifest.csv, then prints a hard allow/block table for the week
starting on the given Monday. Run this BEFORE researching. It replaces
remembering what went out, which nobody does reliably.

Nothing here is advisory. A BLOCKED row means do not use it this week.
"""
import csv
import os
import sys
from collections import Counter
from datetime import date, datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHETYPES = ["A", "B", "C", "D", "E"]
ARCH_NAME = {
    "A": "China signal to tour",
    "B": "West into Asia",
    "C": "Asia into the West",
    "D": "Rejection to raise",
    "E": "Inside the room (first party)",
}
IMAGE_REUSE_DAYS = 60
ENTITY_COOLDOWN_DAYS = 90
HOOK_COOLDOWN_DAYS = 14
SLOT_STREAK_LIMIT = 3


def load(name):
    path = os.path.join(ROOT, name)
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return [r for r in csv.DictReader(f) if any(v.strip() for v in r.values())]


def parse(d):
    try:
        return datetime.strptime(d.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        return None


def split_multi(v):
    return [x.strip() for x in (v or "").replace(",", ";").split(";") if x.strip()]


def next_monday(today):
    return today + timedelta(days=(7 - today.weekday()) % 7 or 7)


def main(argv):
    monday = parse(argv[1]) if len(argv) > 1 else next_monday(date.today())
    if monday is None:
        print("Could not read that date. Use YYYY-MM-DD.")
        return 2
    if monday.weekday() != 0:
        monday -= timedelta(days=monday.weekday())
        print("Note: snapped to the Monday of that week.\n")

    cal = load("data/content-calendar.csv")
    log = load("data/posted-log.csv")
    news = load("data/news-seen.csv")
    imgs = load("assets/images/manifest.csv")

    # history = anything already posted or already scheduled, most recent first
    hist = []
    for r in log:
        d = parse(r.get("posted_date", ""))
        if d:
            hist.append((d, r.get("archetype", ""), r.get("hook_pattern", ""),
                         split_multi(r.get("entities")), "", r.get("post_id", "")))
    for r in cal:
        d = parse(r.get("scheduled_date", ""))
        if d and r.get("status") in ("draft", "approved", "posted", "scheduled"):
            hist.append((d, r.get("archetype", ""), r.get("hook_pattern", ""),
                         split_multi(r.get("entities")), r.get("slot", ""), r.get("post_id", "")))
    hist.sort(reverse=True)

    print("ROTATION CHECK  week of %s  (Mon %s / Wed %s / Fri %s)" % (
        monday.isoformat(), monday.strftime("%d %b"),
        (monday + timedelta(days=2)).strftime("%d %b"),
        (monday + timedelta(days=4)).strftime("%d %b")))
    print("History: %d posts on record, most recent %s\n" % (
        len(hist), hist[0][0].isoformat() if hist else "none"))

    # ---- archetypes ----
    print("ARCHETYPES")
    this_week = [h for h in hist if monday <= h[0] <= monday + timedelta(days=6)]
    used_this_week = {h[1] for h in this_week}
    for a in ARCHETYPES:
        runs = [h for h in hist if h[1] == a]
        last = runs[0][0] if runs else None
        reasons = []
        if a in used_this_week:
            reasons.append("already in this week")
        # same archetype in the same slot for SLOT_STREAK_LIMIT consecutive weeks
        for slot in {h[4] for h in runs if h[4]}:
            weeks = sorted({h[0].isocalendar()[:2] for h in runs if h[4] == slot}, reverse=True)
            streak = 1
            for i in range(1, len(weeks)):
                prev_y, prev_w = weeks[i - 1]
                y, w = weeks[i]
                if (prev_y, prev_w - 1) == (y, w) or (prev_w == 1 and y == prev_y - 1):
                    streak += 1
                else:
                    break
            if streak >= SLOT_STREAK_LIMIT:
                reasons.append("%d weeks running in %s" % (streak, slot))
        state = "BLOCKED" if reasons else "ok"
        gap = "never used" if not last else "%d days ago" % (monday - last).days
        print("  %s  %-30s %-8s %-14s used %dx  %s" % (
            a, ARCH_NAME[a], state, gap, len(runs), "; ".join(reasons)))
    cold = [a for a in ARCHETYPES if not any(h[1] == a for h in hist)]
    if cold:
        print("  -> prefer: %s (never used)" % ", ".join(cold))

    # ---- hook patterns ----
    print("\nHOOK PATTERNS  (cooldown %d days)" % HOOK_COOLDOWN_DAYS)
    pats = [h for h in hist if h[2]]
    if not pats:
        print("  none on record")
    seen = set()
    for d, a, p, ents, slot, pid in pats:
        if p in seen:
            continue
        seen.add(p)
        age = (monday - d).days
        print("  %-18s last used %3d days ago  %s" % (
            p, age, "BLOCKED" if age < HOOK_COOLDOWN_DAYS else "ok"))

    # ---- entities ----
    print("\nENTITIES  (cooldown %d days: do not build another post around these)" % ENTITY_COOLDOWN_DAYS)
    ent_last = {}
    ent_count = Counter()
    for d, a, p, ents, slot, pid in hist:
        for e in ents:
            ent_count[e] += 1
            ent_last.setdefault(e, d)
    blocked = [(e, ent_last[e]) for e in ent_last if (monday - ent_last[e]).days < ENTITY_COOLDOWN_DAYS]
    if not blocked:
        print("  none")
    for e, d in sorted(blocked, key=lambda x: x[1], reverse=True):
        print("  BLOCKED  %-24s last %s (%d days), used %dx" % (
            e, d.isoformat(), (monday - d).days, ent_count[e]))

    # ---- stories ----
    print("\nSTORIES ALREADY POSTED OR SCHEDULED  (never post twice)")
    done = [r for r in news if r.get("posted", "").strip() in ("yes", "scheduled")]
    if not done:
        print("  none")
    for r in done:
        print("  %-44s %s  %s" % (r.get("story_key", "")[:44], r.get("archetype", ""), r.get("post_id", "")))
    open_c = [r for r in news if r.get("posted", "").strip() == "no"]
    if open_c:
        print("\n  Unused candidates on file, check these before searching:")
        for r in open_c:
            print("    %-42s %s  %s" % (r.get("story_key", "")[:42], r.get("archetype", ""),
                                        (r.get("notes", "") or "")[:60]))

    # ---- images ----
    print("\nIMAGES  (%d-day reuse lockout)" % IMAGE_REUSE_DAYS)
    # an image assigned to a scheduled post is spent, even though it has not shipped yet
    pending = {}
    for r in cal:
        d = parse(r.get("scheduled_date", ""))
        img = (r.get("image") or "").strip()
        if d and img and img != "NEEDS SHOOT" and r.get("status") in ("draft", "approved", "scheduled"):
            pending.setdefault(img, []).append(d)
    avail = Counter()
    for r in imgs:
        uses = split_multi(r.get("used_on"))
        dates = [d for d in (parse(u) for u in uses) if d]
        dates += pending.get(r.get("filename", ""), [])
        recent = any((monday - d).days < IMAGE_REUSE_DAYS for d in dates)
        flags = []
        if recent:
            when = max(dates)
            tag = "scheduled" if r.get("filename") in pending and when in pending.get(r.get("filename"), []) else "used"
            flags.append("LOCKED, %s %s" % (tag, when.isoformat()))
        if len(dates) >= 3:
            flags.append("STOP, used %dx" % len(dates))
        elif len(dates) == 2:
            flags.append("heavily used")
        if "consent-needed" in r.get("tags", ""):
            flags.append("consent-needed")
        if not flags:
            for a in split_multi(r.get("archetypes")):
                avail[a] += 1
        print("  %-22s %-12s %s" % (r.get("filename", ""), r.get("archetypes", ""),
                                    "; ".join(flags) or "available"))
    print("\n  Usable images per archetype: %s" % (
        ", ".join("%s=%d" % (a, avail.get(a, 0)) for a in ARCHETYPES + ["BTS"])))
    starved = [a for a in ARCHETYPES if avail.get(a, 0) == 0]
    if starved:
        print("  -> NO IMAGE for: %s. Expect to ask the author to attach one." % ", ".join(starved))

    print("\nDecide the week from the rows above, then research. Do not research first.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
