#!/usr/bin/env python3
"""Write a run marker or validate a run result. No shell heredocs, so nothing
depends on YAML block-scalar indentation."""
import json
import os
import sys
from datetime import datetime, timezone

cmd = sys.argv[1]
run_id = sys.argv[2]
d = os.path.join("runs", run_id)
os.makedirs(d, exist_ok=True)
status_path = os.path.join(d, "status.json")
result_path = os.path.join(d, "result.json")


def write(obj):
    with open(status_path, "w") as f:
        json.dump(obj, f, indent=2)
        f.write("\n")


now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
run_url = os.environ.get("RUN_URL", "")

if cmd == "start":
    write({"runId": run_id, "state": "running", "startedAt": now, "workflowRunUrl": run_url})
    print("marked running")

elif cmd == "fail":
    write({"runId": run_id, "state": "failed", "finishedAt": now,
           "error": sys.argv[3] if len(sys.argv) > 3 else "The run failed.",
           "workflowRunUrl": run_url})
    print("marked failed")

elif cmd == "finish":
    claude_outcome = os.environ.get("CLAUDE_OUTCOME", "unknown")
    if not os.path.exists(result_path):
        if os.path.exists(status_path):
            try:
                with open(status_path) as f:
                    prior = json.load(f)
                if prior.get("state") == "failed" and prior.get("error"):
                    print("keeping the earlier failure reason")
                    sys.exit(0)
            except (json.JSONDecodeError, OSError):
                pass
        write({
            "runId": run_id, "state": "failed", "finishedAt": now,
            "error": "The run finished without writing result.json (Claude step: %s). Open the workflow log." % claude_outcome,
            "workflowRunUrl": run_url,
        })
        print("FAILED: no result.json")
        sys.exit(0)

    try:
        with open(result_path) as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        write({
            "runId": run_id, "state": "failed", "finishedAt": now,
            "error": "result.json was not valid JSON: %s" % e, "workflowRunUrl": run_url,
        })
        print("FAILED: result.json is not valid JSON")
        sys.exit(0)

    posts = data.get("posts")
    if not isinstance(posts, list) or not posts:
        write({
            "runId": run_id, "state": "failed", "finishedAt": now,
            "error": "result.json carried no posts.", "workflowRunUrl": run_url,
        })
        print("FAILED: no posts in result.json")
        sys.exit(0)

    # normalise the bits the front end depends on, so a missing field cannot break it
    data["runId"] = run_id
    data["state"] = "done"
    data.setdefault("generatedAt", now)
    data["workflowRunUrl"] = run_url
    for p in posts:
        p.setdefault("copy", "")
        p["charCount"] = len(p.get("copy", "").strip())
        for k, dflt in (("blockers", []), ("entities", []), ("styleGate", []),
                        ("needsTeamPhoto", False), ("verified", False),
                        ("photoQuery", ""), ("photoBrief", ""), ("altText", ""),
                        ("firstComment", ""), ("disclosure", ""), ("image", "")):
            p.setdefault(k, dflt)
    with open(result_path, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    write({"runId": run_id, "state": "done", "finishedAt": now,
           "posts": len(posts), "workflowRunUrl": run_url})
    print("done: %d posts" % len(posts))

elif cmd == "dry":
    # Smoke test of the whole handshake without spending a Claude run.
    from datetime import timedelta
    today = datetime.now(timezone.utc).date()
    monday = today + timedelta(days=(7 - today.weekday()) % 7 or 7)
    iso = monday.isocalendar()
    tag = "%d%02d" % (iso[0], iso[1])
    slots = [("Monday", 0, "awareness", "soft", "D"), ("Wednesday", 2, "proof", "medium", "B"),
             ("Friday", 4, "offer", "hard", "E")]
    posts = []
    for day, off, slot, cta, arch in slots:
        date = monday + timedelta(days=off)
        body = ("DRY RUN. This is a pipeline smoke test, not a real post.\n\n"
                "It exists to prove the dispatch, commit, poll and render path works "
                "before a real Claude Code run is spent on it.\n\n"
                "Do not schedule this.\n\n#DryRun #Pipeline #Test")
        posts.append({
            "postId": "OJV-%s-%s" % (tag, day[0]), "day": day, "date": date.isoformat(),
            "slot": slot, "archetype": arch, "archetypeName": "dry run",
            "ctaTier": cta, "hookPattern": "number-first", "copy": body,
            "charCount": len(body), "entities": [], "sourceUrl": "", "sourcePublisher": "",
            "firstComment": "", "disclosure": "", "verified": False,
            "verificationNotes": "Dry run, nothing was researched.", "styleGate": [],
            "image": "", "altText": "", "needsTeamPhoto": arch == "E",
            "photoBrief": "Dry run: a real archetype E post would ask for a partner photo here.",
            "photoQuery": "" if arch == "E" else "office meeting",
            "whyThisSlot": "Dry run.", "blockers": ["This is a dry run. Discard it."],
            "draftPath": "",
        })
    with open(result_path, "w") as f:
        json.dump({
            "runId": run_id, "state": "done", "week": "%d-W%02d" % (iso[0], iso[1]),
            "generatedAt": now, "dryRun": True, "posts": posts,
            "rotation": {"blockedArchetypes": [], "blockedEntities": [], "blockedHookPatterns": []},
            "needsFromAuthor": ["This was a dry run. Press the button again without dry run for real posts."],
            "notes": "Dry run: the Claude Code step was skipped.",
        }, f, indent=2)
        f.write("\n")
    print("wrote a dry-run result")

else:
    print("unknown command %s" % cmd)
    sys.exit(1)
