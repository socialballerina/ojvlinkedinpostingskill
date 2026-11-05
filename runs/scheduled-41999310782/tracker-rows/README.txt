These rows could not be written to .claude/skills/ojv-linkedin/data/ because this CI session was
refused write permission under .claude/. Append them by hand (skip the header line), oldest week
first:

1. runs/scheduled-39738926451/tracker-rows/  (W44, still unappended)
2. runs/scheduled-40839989263/tracker-rows/  (W45, still unappended)
3. runs/scheduled-41999310782/tracker-rows/  (W46, this run)
   content-calendar.append.csv -> data/content-calendar.csv   (2 rows: Monday and Wednesday only, Friday is empty)
   news-seen.append.csv        -> data/news-seen.csv          (8 rows)

One existing row also needs an edit, not an append: in data/news-seen.csv change
mcdonalds-china-citic-carlyle-2017-2025 to posted=scheduled, post_id=OJV-202646-W, and add to its
notes "Re-verified 5 Nov 2026; current count over 7,500 restaurants as of Nov 2025, China Daily HK
22 Dec 2025."

Drafts belong in .claude/skills/ojv-linkedin/drafts/2026-W46/ and are here in drafts/2026-W46/.
The held Friday draft is in held/ and is not on the calendar.
The image manifest was not changed. mic.jpg is assigned to OJV-202646-W; set used_on and post_id
when it actually goes out.
