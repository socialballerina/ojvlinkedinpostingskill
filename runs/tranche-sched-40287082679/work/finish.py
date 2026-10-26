import re,csv,json,os,subprocess
R='runs/tranche-sched-40287082679/'; N=R+'library/'
new=['OJV-L%03d'%i for i in range(21,31)]
order=open(R+'work/order.txt').read().split()
AN={'A':'China signal to tour','B':'West into Asia','C':'Asia into the West','D':'Rejection to raise','F2':'Situation to solved (F2 diagnostic)'}
PUB={'OJV-L021':'Hesai Group via SEC EDGAR (6-K Exhibit 99.1)','OJV-L022':'Pony AI Inc. via SEC EDGAR (6-K Exhibit 99.1)','OJV-L023':'CGTN','OJV-L024':'Walmart (corporate newsroom); BW Retail World for FY26','OJV-L025':'Apple Newsroom India','OJV-L026':'Mynavi News','OJV-L027':'Entrepreneur (founder byline)','OJV-L028':'Fast Retailing (IR release)','OJV-L029':'The Korea Times','OJV-L030':''}
def block(s,name,nxt): return s.split('## '+name,1)[1].split('## '+nxt,1)[0].strip()
gate=open(R+'work/gate.txt').read().splitlines()
posts=[];cal=[];seen=[]
blockers={'OJV-L021':['Hesai Q3 2026 results (due about 10 November 2026) will be the newer quarter; the Q2 figures stay true but reread before posting.'],
 'OJV-L022':['Pony.ai Q3 2026 results (18 November 2026) supersede the fleet count; reread before posting after January 2027.'],
 'OJV-L025':["Cook's succession (announced April 2026) was taken from press reports, not Apple's release; confirm before posting."],
 'OJV-L027':['The 106 count is a single self-report by the founder; approver should accept or cut.'],
 'OJV-L030':['Naman to confirm the four diagnostic items (certification, channel, landed price, service).','TODO(config: booking link) is recorded in the draft notes, not in the paste copy, matching OJV-L001, L007 and L011.']}
for pid in new:
    s=open(N+pid+'.md').read(); fm=dict(re.findall(r'^(\w+):\s*(.*)$',s.split('---')[1],re.M))
    copy=block(s,'Copy','Photo brief'); fc=block(s,'First comment','Verified facts')
    m=re.search(r'(https?://\S+?)\?utm_',fc); url=m.group(1) if m else ''
    vf=block(s,'Verified facts','Guardrail notes'); weak=re.search(r'Weakest sourcing:(.*)',vf,re.S)
    weak=' '.join(weak.group(1).split()) if weak else 'No third-party fact in the post; the four diagnostic items await Naman.'
    disc=next((l for l in copy.split('\n') if 'commentary' in l.lower()),'')
    ents=[] if fm['entities']=='none' else [e.strip() for e in fm['entities'].split(';')]
    posts.append(dict(postId=pid,queueNo=order.index(pid)+1,archetype=fm['archetype'],archetypeName=AN[fm['archetype']],ctaTier=fm['cta_tier'],
      hookPattern=fm['hook_pattern'],expires=fm['expires'] if fm['expires']!='none' else 'none',copy=copy,entities=ents,storyKey=fm['story_key'],
      sourceUrl=url,sourcePublisher=PUB[pid],firstComment=fc if url else '',disclosure=disc,verified=True,verificationNotes=weak,
      styleGate=[l for l in gate if pid+'.md' in l],photoBrief=block(s,'Photo brief','Alt text'),
      altText=block(s,'Alt text','First comment').split('\n\n')[0],blockers=blockers.get(pid,[]),draftPath='library/%s.md'%pid))
    cal.append([pid,'','',fm['archetype'],fm['funnel_tier'],copy.split('\n')[0],fm['hook_pattern'],';'.join(ents) or 'none','library','PHOTO-BRIEF',fm['cta_tier'],url,'library/%s.md'%pid])
    if url: seen.append(['2026-10-26',fm['story_key'],url,fm['archetype'],'library',pid,'Used in tranche-sched-40287082679. See Verified facts in the draft for the weakest source.'])
dropped=[
 ('china-orbital-launches-2025-record','A','https://english.spacechina.com/n17212/c4521283/content.html','UNUSED, verified reserve. CASC 73 launches in 2025 (CASC, 5 Jan 2026); national total 93 (China Daily) vs 92 (NASASpaceflight). Held back: 2025 data, national count conflicts, and 2026 launch failures would need sourcing.'),
 ('horizon-robotics-h1-2026','A','','DROPPED. HKEX interim PDF unreadable; 2.218m chip shipments only in secondary sources; core operating losses widened and headline profit came from non-operating items.'),
 ('weride-robotaxi-2026','A','','NOT CHECKED. Same story shape as Pony.ai (OJV-L022); one robotaxi post per tranche.'),
 ('dji-2026','A','','NOT CHECKED. Private company; no clean dated number found.'),
 ('amex-china-clearing-licence','B','','DROPPED. Strong regulatory-sequencing mechanism (LianLian JV, first foreign clearing licence) but no documented traction in China: no cards, volume or revenue figures.'),
 ('mastercard-china-clearing-jv','B','','NOT CHECKED. Same angle as Amex with the same probable lack of traction data.'),
 ('duolingo-japan','B','','DROPPED. No Japan-specific figure in 2025 or 2026 filings; only "fastest-growing region" for Asia.'),
 ('costco-korea-japan-taiwan','B','','DROPPED. No clear mechanism beyond exporting the format; not researched further.'),
 ('jollibee-north-america-beyond-diaspora','C','https://www.nrn.com/quick-service/jollibee-embraces-differentiation-over-imitation-in-u-s-market-push','UNUSED, verified reserve. NA same-store sales +10.2% in 2025 and Q2 2026 NA system sales +21.6% (JFC releases read only on republication pages; originals 403). Store counts mix brands; US AUV conflicts ($5m vs $4.5m). Good later candidate.'),
 ('webtoon-us-canvas','C','','DROPPED. Q2 2026 revenue down 2.8% and net loss widened (SEC 8-K, 10 Aug 2026); undercuts the it-worked spine.'),
 ('roborock-europe-us','C','','DROPPED. 2025 overseas revenue RMB10.442bn, 56% of total, but no US or Europe split and no named Western mechanism in the primary source.'),
 ('samyang-buldak-us','C','','DROPPED. No Samyang filing or IR source for US or Europe numbers; the CEO "unsatisfactory" remark not found in the fetched article.'),
 ('schultz-il-giornale-217-of-242','D','https://finance.yahoo.com/news/starbucks-howard-schultz-moved-seattle-153007171.html','DROPPED. 217 of 242 in the book quote, but Gale (Encyclopedia.com) gives 24 of 242 said yes, implying 218; cut, not averaged. Raise amount varies ($400k to $1.7m). Also Starbucks is an entity in OJV-L008 and not an Asian founder.'),
 ('rapido-75-investor-rejections','D','','DROPPED. No founder source for the 75 count (Guntupalli gave none when asked, Outlook Business Dec 2025); secondary sources disagree on which founder was rejected.'),
 ('touchten-67-vcs','D','','DROPPED. e27 403 and DailySocial 404; "pitched to 67" is not a rejection count.'),
 ('meesho-lenskart-groww-boat-licious-rejections','D','','DROPPED. No documented investor-rejection count found for any of them.'),
 ('stoa-money-300-rejections','D','','NOT CHECKED. Not Asia-linked and source not opened.'),
]
for k,a,u,w in dropped: seen.append(['2026-10-26',k,u,a,'no','',w])
os.makedirs(R+'tracker-rows',exist_ok=True)
H1='post_id,scheduled_date,slot,archetype,funnel_tier,hook,hook_pattern,entities,status,image,cta_tier,source_url,draft_path'.split(',')
H2='date_seen,story_key,source_url,archetype,posted,post_id,notes'.split(',')
for f,h,rows in ((R+'tracker-rows/content-calendar.append.csv',H1,cal),(R+'tracker-rows/news-seen.append.csv',H2,seen)):
    w=csv.writer(open(f,'w',newline='')); w.writerow(h); w.writerows(rows)
open(R+'tracker-rows/README.txt','w').write('''These rows could not be written to .claude/skills/ojv-linkedin/data/ because the Write tool was
denied for paths under .claude/ in this CI session. Append them by hand (skip the header line), or
let the next step do it:

content-calendar.append.csv -> data/content-calendar.csv   (10 rows, status=library)
news-seen.append.csv        -> data/news-seen.csv          (%d rows: 9 used, %d considered and not used)

The library itself is mirrored in runs/tranche-sched-40287082679/library/ and is complete:
copy library/OJV-L*.md, library/paste/*.txt and library/QUEUE.csv over
.claude/skills/ojv-linkedin/library/. The 20 existing drafts in the mirror differ from the
originals only in their queue_no front-matter line; copy and paste text are byte-identical.
public/queue.html was regenerated from the mirror and already reflects all 30 posts.
'''%(len(seen),len(dropped)))
res=dict(runId='tranche-sched-40287082679',state='done',mode='tranche',requested=10,written=len(posts),firstId=new[0],lastId=new[-1],posts=posts,
 droppedCandidates=[dict(storyKey=k,archetype=a,why=w) for k,a,u,w in dropped],
 rotation=dict(blockedHookPatterns=[],
  blockedEntities=sorted({e for pid in order if pid not in new for e in re.search(r'^entities:\s*(.*)$',open(N+pid+'.md').read(),re.M).group(1).replace(';',',').split(',') if e.strip() and e.strip().lower() not in ('none','india','japan','hungary','china biotech out-licensing','china industrial robotics')}|{'SMIC','Omoda','Jaecoo','Chery','Unitree','Notion','Canva','Melanie Perkins'}),
  usedF2Pairs=['GTM advisory x company entering APAC (OJV-L001)','Fundraising support x mid-raise founder (OJV-L007)','Lead generation x no local team (OJV-L011)','GTM advisory x hardware (OJV-L030, new)']),
 needsFromAuthor=[
  'WRITE PERMISSION: the Write tool was denied for every path under .claude/ in this CI session, so the tranche is in runs/tranche-sched-40287082679/library/ (a complete 30-post mirror with QUEUE.csv and paste files) and the tracker rows are in runs/tranche-sched-40287082679/tracker-rows/. Copy them into .claude/skills/ojv-linkedin/ as described in tracker-rows/README.txt. public/queue.html is already regenerated.',
  'OJV-L002 (queue 1) expires 2026-10-31, five days after this run. Publish it by then or kill it.',
  'Booking link for archetype F was empty. TODO(config: booking link) is recorded in the OJV-L030 draft notes, not in the paste copy, to match OJV-L001, L007 and L011 and SKILL.md, which says F needs no link. Decide whether F2 posts carry one; if so it goes directly above the "If you are ..." ask in all four.',
  'Naman to confirm the four hardware diagnostic items in OJV-L030 (certification, channel, landed price, service).',
  'OJV-L027 (Ukhi) rests on one self-reported count of 106, from the founder\'s own article. Nothing contradicts it, but approve or cut.',
  'Archetype D decision (batch-library.md, honest limit 6) is still open. This tranche verified 1 of 6 D candidates. Recommend cutting D to about 8 across the hundred.',
  'Before tranche 4 (the next one), supply performance numbers for anything already published from the library (batch-library.md, honest limit 3). No posted-log rows exist yet.',
  'Approver review (Naman) of all ten posts before any is scheduled.'],
 notes='Ten of ten written: A 3 (L021 Hesai, L022 Pony.ai, L023 China energy storage), B 3 (L024 Walmart-Flipkart, L025 Apple India, L026 Uber Japan), C 2 (L028 Uniqlo, L029 APR Medicube), D 1 (L027 Ukhi), F2 1 (L030 GTM advisory x hardware). D was capped at 4 but only Ukhi verified, so the slack went into A and B. E and F1 were not attempted because they cannot be batched. Sourcing was done by four parallel research agents, each told to quote verbatim from opened pages; the quotes are as returned by the fetch tool. Every draft passes the style gate; the whole 30-post library passes. QUEUE.csv was rewritten for all 30 posts under the rotation rules (no archetype more than twice in 5, no hook pattern twice in 6, no shared entity within 20, hard-CTA posts at positions 9, 15, 20 and 25). Some existing posts moved a few positions to make room for the perishable new A posts. Because .claude/ was not writable through the Write tool, all library and tracker output is in runs/tranche-sched-40287082679/ (see README in tracker-rows); public/queue.html was regenerated from that mirror. Image intake skipped: no raw image folder in CI. Nothing was committed, scheduled or published.')
json.dump(res,open(R+'result.json','w'),indent=2,ensure_ascii=False)
print(len(posts),len(seen),len(dropped))
