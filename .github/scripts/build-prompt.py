#!/usr/bin/env python3
"""Fill the weekly-run prompt from environment variables.

Inputs arrive as env vars rather than as GitHub Actions expressions interpolated
into a shell script, so a value someone types into the web form cannot break out
into the runner's shell.
"""
import os

TEMPLATE = ".github/prompts/weekly-run.md"
OUT = "/tmp/ojv-prompt.txt"

DEFAULT_OFFER = ("China Tech Trek, Hong Kong and Shenzhen, 13 to 17 October 2026, "
                 "run with ContraVC as official partner")

with open(TEMPLATE) as f:
    text = f.read()

news = os.environ.get("OJV_NEWS", "").strip()
# Nothing typed into a form may impersonate the prompt's own structure.
for marker in ("--- BEGIN OJV NEWS ---", "--- END OJV NEWS ---"):
    news = news.replace(marker, "[removed]")
news = news[:4000]

values = {
    "RUN_ID": os.environ.get("RUN_ID", "").strip(),
    "KEYWORD": os.environ.get("KEYWORD", "").strip() or "TODO(config: DM keyword)",
    "ENQUIRY_URL": os.environ.get("ENQUIRY_URL", "").strip() or "TODO(config: enquiry destination)",
    "OFFER": os.environ.get("OFFER", "").strip() or DEFAULT_OFFER,
    "OJV_NEWS": news or "(nothing supplied)",
}
for key, value in values.items():
    text = text.replace("{{%s}}" % key, value)

if "{{" in text:
    raise SystemExit("An unfilled placeholder is left in the prompt: %s" % text[text.index("{{"):][:40])

with open(OUT, "w") as f:
    f.write(text)
print("Wrote %s, %d bytes, run id %s" % (OUT, len(text), values["RUN_ID"]))
