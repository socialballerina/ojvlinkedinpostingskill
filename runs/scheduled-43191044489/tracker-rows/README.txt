These rows could not be written to .claude/skills/ojv-linkedin/data/ because this CI session was
refused write permission under .claude/. Append them by hand (skip the header line), oldest week first:

1. runs/scheduled-39738926451/tracker-rows/  (W44, still unappended)
2. runs/scheduled-40839989263/tracker-rows/  (W45, still unappended)
3. runs/scheduled-41999310782/tracker-rows/  (W46, still unappended)
4. runs/scheduled-43191044489/tracker-rows/  (W47, this run)
   content-calendar.append.csv -> data/content-calendar.csv   (3 rows)
   news-seen.append.csv        -> data/news-seen.csv          (7 rows)

The nbs-sep-2026-industrial-robot-output row already exists in data/news-seen.csv (2026-11-09,
posted=no). Edit that row to posted=scheduled, post_id=OJV-202647-M instead of adding a duplicate.

Drafts belong in .claude/skills/ojv-linkedin/drafts/2026-W47/ and are in drafts/2026-W47/ here.
The image manifest was not changed. studio-blazer.jpg is assigned to OJV-202647-W; set used_on and
post_id when it actually goes out.
