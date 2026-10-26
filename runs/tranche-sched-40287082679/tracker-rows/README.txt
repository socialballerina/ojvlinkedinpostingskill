These rows could not be written to .claude/skills/ojv-linkedin/data/ because the Write tool was
denied for paths under .claude/ in this CI session. Append them by hand (skip the header line), or
let the next step do it:

content-calendar.append.csv -> data/content-calendar.csv   (10 rows, status=library)
news-seen.append.csv        -> data/news-seen.csv          (26 rows: 9 used, 17 considered and not used)

The library itself is mirrored in runs/tranche-sched-40287082679/library/ and is complete:
copy library/OJV-L*.md, library/paste/*.txt and library/QUEUE.csv over
.claude/skills/ojv-linkedin/library/. The 20 existing drafts in the mirror differ from the
originals only in their queue_no front-matter line; copy and paste text are byte-identical.
public/queue.html was regenerated from the mirror and already reflects all 30 posts.
