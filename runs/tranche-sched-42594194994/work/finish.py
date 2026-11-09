import re,csv,json,os
L='.claude/skills/ojv-linkedin/library/'; D='.claude/skills/ojv-linkedin/data/'; R='runs/tranche-sched-42594194994/'
new=['OJV-L%03d'%i for i in range(31,41)]
order=open(R+'work/order.txt').read().split()
AN={'A':'China signal to tour','B':'West into Asia','C':'Asia into the West','D':'Rejection to raise','F2':'Situation to solved (F2 diagnostic)'}
PUB={'OJV-L031':'International Federation of Robotics','OJV-L032':'Counterpoint Research','OJV-L033':'Yum China Holdings via SEC EDGAR (8-K Exhibit 99.1); Nation\'s Restaurant News for 2016','OJV-L034':'Business Today (Arnab Dutta); Coca-Cola earnings call transcript via The Motley Fool','OJV-L035':'PTI via The Quint; Business Today (PTI); DT Next (PTI)','OJV-L036':'Hyundai Motor America releases (archive copies, The Auto Channel); NPR via KPBS','OJV-L037':'The Korea Herald; CJ Group newsroom; FoodIngredientsFirst','OJV-L038':'Kikkoman Corporation (company history page)','OJV-L039':'','OJV-L040':''}
def block(s,name,nxt): return s.split('## '+name,1)[1].split('## '+nxt,1)[0].strip()
gate=open(R+'work/gate.txt').read().splitlines()
F2B=['TODO(config: booking link): booking link was empty in the run config; recorded in the draft First comment block, not in the paste copy, matching every earlier F2 and SKILL.md (F needs no link).']
blockers={
 'OJV-L031':['Approver: confirm OJV-L002 is killed; this post replaces it with the 2025 figures.'],
 'OJV-L032':['Single tracker (Counterpoint). Other trackers reportedly count AgiBot lower; copy attributes every figure to Counterpoint by name.'],
 'OJV-L033':['Genre overlap with OJV-L008 (Starbucks China) and weekly OJV-202646-W (McDonald\'s China); queued 17 positions from OJV-L008.'],
 'OJV-L034':['Neglect years rest on the seller Ramesh Chauhan\'s account in one outlet; attributed in the copy.'],
 'OJV-L039':['Naman to confirm the four exec-tour scoping items (the question, the visits, who travels, the flight home).']+F2B,
 'OJV-L040':['Naman to confirm the four founder-led-sales diagnostic items.']+F2B}
posts=[];cal=[];seen=[]
for pid in new:
    s=open(L+pid+'.md').read(); fm=dict(re.findall(r'^(\w+):\s*(.*)$',s.split('---')[1],re.M))
    copy=block(s,'Copy','Photo brief'); fc=block(s,'First comment','Verified facts')
    m=re.search(r'(https?://\S+?)\?utm_',fc); url=m.group(1) if m else ''
    vf=block(s,'Verified facts','Guardrail notes'); wk=re.search(r'Weakest sourcing:(.*)',vf,re.S)
    weak=' '.join(wk.group(1).split()) if wk else 'No third-party fact in the post. The weakest element is the four diagnostic items, which describe an OJV method and await Naman\'s confirmation.'
    disc=next((l for l in copy.split('\n') if 'commentary' in l.lower() or 'nothing to do with this one' in l.lower()),'')
    ents=[] if fm['entities']=='none' else [e.strip() for e in fm['entities'].split(';')]
    posts.append(dict(postId=pid,queueNo=order.index(pid)+1,archetype=fm['archetype'],archetypeName=AN[fm['archetype']],ctaTier=fm['cta_tier'],
      hookPattern=fm['hook_pattern'],expires=fm['expires'],copy=copy,entities=ents,storyKey=fm['story_key'],
      sourceUrl=url,sourcePublisher=PUB[pid],firstComment=fc if url else '',disclosure=disc,verified=True,verificationNotes=weak,
      styleGate=[l.strip() for l in gate if pid+'.md' in l],photoBrief=block(s,'Photo brief','Alt text'),
      altText=block(s,'Alt text','First comment').split('\n\n')[0],blockers=blockers.get(pid,[]),draftPath='library/%s.md'%pid))
    cal.append([pid,'','',fm['archetype'],fm['funnel_tier'],copy.split('\n')[0],fm['hook_pattern'],';'.join(ents) or 'none','library','PHOTO-BRIEF',fm['cta_tier'],url,'library/%s.md'%pid])
    seen.append(['2026-11-09',fm['story_key'],url,fm['archetype'],'library',pid,'Used in tranche-sched-42594194994. See Verified facts in the draft for the weakest source.'])
dropped=[
 ('cpca-sep-2026-nev-exports-vs-domestic-retail','A','https://news.metal.com/newscontent/104152267-cpca-september-passenger-vehicle-exports-reached-917000-units-up-737-yoy','UNUSED, verified reserve. CPCA via SMM and GoodCarBadCar, 12 Oct 2026: September 2026 passenger NEV exports 558,000 (+163.5%), domestic NEV retail -16.7%. Held back: same month and theme as OJV-L013 (BYD overseas, September 2026); CPCA original not reached. Expires 2027-04-12.'),
 ('nbs-sep-2026-industrial-robot-output','A','https://www.stats.gov.cn/english/PressRelease/202610/t20261020_1965665.html','UNUSED, verified reserve. NBS: Jan-Sep 2026 industrial robot output 794,781 sets, +29.1% (table row). Held back: overlaps OJV-L031 (IFR); NBS output is not comparable with IFR installations.'),
 ('ehang-q3-2026-deliveries','A','','NOT USABLE YET. Q3 2026 results not published by 9 Nov 2026; Q2 figures not verified on a fetched page.'),
 ('agibot-2025-revenue','A','','DROPPED. RMB 1.05bn appeared only in an aggregator snippet.'),
 ('huawei-ascend-landspace-nmpa-2026','A','','NOT CHECKED. Research time went to verified candidates.'),
 ('lululemon-mainland-china-community-model','B','','DROPPED on what-happened-next. Q2 FY2026 release (3 Sep 2026): China Mainland revenue -2% and comparable sales -8% in constant currency, after +29% in FY2025; CEO transition. No primary source for the ambassador model. A first agent report quoted China +25% with no working URL; that figure was false and discarded. Possible later rise-and-stall post.'),
 ('hindustan-unilever-sachets','B','','DROPPED. A research agent supplied a "40% of turnover" sachet quote with no readable page behind it; not verifiable. Sachet pioneering is also widely credited to others, so the mechanism is not clearly HUL\'s.'),
 ('mondelez-oreo-china','B','','DROPPED. Best figures only in an FT repost PDF and a Foreign Policy summary of a paywalled WSJ piece; no primary.'),
 ('kfc-japan-christmas','B','','DROPPED. Overlaps the KFC brand in OJV-L033; Carlyle took KFC Holdings Japan private in 2024 (snippet only) and Carlyle is a weekly-run entity.'),
 ('decathlon-shopify-stripe-asia','B','','NOT CHECKED. Private or no country-level figures expected.'),
 ('freshworks-us-pricing','C','','DROPPED. S-1 frames it as global from day one, not a move into the West with a named mechanism; 11% layoffs reported May 2026 (not opened).'),
 ('jollibee-north-america-beyond-diaspora','C','','DROPPED again. FY2025 NA same-store sales +10.2% from wire copies only; no documented mechanism; store counts mix brands.'),
 ('lenovo-ibm-daiso-ajinomoto','C','','NOT CHECKED. Three C candidates verified first.'),
 ('glossier-emily-weiss-11-of-12','D','https://intothegloss.com/2016/11/glossier-series-b-funding-announcement/','DROPPED. Her own post says only "Everyone else said no"; the 11-of-12 count is Fortune narration via Wikipedia; seed amount conflicts ($1M vs $2M); stepped down as CEO 2022.'),
 ('fave-kfit-cc-yeoh-61-rejections','D','','DROPPED. Best Asian lead, but "61 rejections" seen only in podcast search snippets; every episode page failed (403/503/404); raise amount conflicts ($2.25M vs TechCrunch $3.25M). Worth a second look with a transcript.'),
 ('stage-vinay-singhal-500-rejections','D','https://yourstory.com/2022/05/yourstory-uncut-vinay-singhal-stage-ott-platform-startup-netflix','DROPPED. Count is reporter narration and the same article gives 100+ pitches and 500 rejections.'),
 ('zette-yehong-zhu-180-rejections','D','','DROPPED. 180 only in a Substack headline (403); snippet body says "hundreds"; raise verified ($1.7M pre-seed).'),
 ('carta-henry-ward-300-rejections','D','','DROPPED. 300 only in a podcast title; nothing in his own words.'),
 ('indiegogo-93-rejections','D','','DROPPED. 93 (How I Built This title) vs 90 (Entrepreneur headline). Cut, not averaged.'),
 ('mobikwik-mamaearth-classpass-walker-tonkean-canavi-joel-neoh','D','','DROPPED. No documented investor-rejection count for any of them.'),
]
for k,a,u,w in dropped: seen.append(['2026-11-09',k,u,a,'no','',w])
for f,rows in ((D+'content-calendar.csv',cal),(D+'news-seen.csv',seen)):
    w=csv.writer(open(f,'a',newline='')); w.writerows(rows)
# L002 calendar row -> killed
rows=list(csv.reader(open(D+'content-calendar.csv')))
for r in rows:
    if r[0]=='OJV-L002': r[8]='killed'
csv.writer(open(D+'content-calendar.csv','w',newline='')).writerows(rows)
seen_l002=['2026-11-09','ifr-world-robotics-2025-china-54pc','',  'A','killed','OJV-L002','OJV-L002 killed unpublished: expired 2026-10-31. Superseded by OJV-L031 (ifr-world-robotics-2026-china-2025-installs).']
csv.writer(open(D+'news-seen.csv','a',newline='')).writerow(seen_l002)
ents=set()
for pid in order:
    if pid in new: continue
    e=re.search(r'^entities:\s*(.*)$',open(L+pid+'.md').read(),re.M).group(1)
    ents|={x.strip() for x in e.split(';') if x.strip() and x.strip().lower() not in ('none','india','japan','hungary','china biotech out-licensing','china industrial robotics')}
ents|={'SMIC','Omoda','Jaecoo','Chery','Unitree','Notion','Canva','Melanie Perkins','Cambricon','McDonald\'s','CITIC','Carlyle','Asics','Homeplus','E-Mart','Costco'}
res=dict(runId='tranche-sched-42594194994',state='done',mode='tranche',requested=10,written=len(posts),firstId=new[0],lastId=new[-1],posts=posts,
 droppedCandidates=[dict(storyKey=k,archetype=a,why=w) for k,a,u,w in dropped],
 rotation=dict(blockedHookPatterns=[],blockedEntities=sorted(ents),
  usedF2Pairs=['GTM advisory x company entering APAC (OJV-L001)','Fundraising support x mid-raise founder (OJV-L007)','Lead generation x no local team (OJV-L011)','GTM advisory x hardware (OJV-L030)','OJV Educate exec tours x corporate strategy teams (OJV-L039, new)','Lead generation x founder-led sales (OJV-L040, new)']),
 needsFromAuthor=[
  'Booking link for archetype F was empty in the run config. TODO(config: booking link) is recorded in the First comment block of OJV-L039 and OJV-L040, not in the paste copy, because SKILL.md says F needs no link and no earlier F2 (L001, L007, L011, L030) has a slot for one. If F2 posts should carry a link, it goes on its own line directly above the "If you are ..." ask in all six.',
  'Naman to confirm the four diagnostic items in OJV-L039 (exec tours: the question, the visits, who travels, the flight home) and OJV-L040 (founder-led sales: who replies, why they reply, what the founder says on the call, what is written down).',
  'OJV-L002 expired on 2026-10-31 unpublished and has been killed (draft status, calendar row, news-seen note) and removed from QUEUE.csv. OJV-L031 replaces it with IFR World Robotics 2026 figures. Confirm, or revive L002 with a rewrite.',
  'OJV-L010 (queue 1) expires 2026-12-31. Publish before then or recheck the UBTECH 5,000-unit target.',
  'Archetype D decision (batch-library.md honest limit 6) is still open and now urgent: this tranche verified 0 of 13 D candidates, after 1 of 6 last tranche. Library holds 3 D posts against a plan of 16. Decide: cut D to about 8, or explicitly widen the trigger to documented failures before a documented raise.',
  'This was tranche 4, written with no performance data (data/posted-log.csv has no rows). batch-library.md asks for the numbers before tranche 4. Supply them before any tranche 5.',
  'Tranche 3 (OJV-L021 to L030) had only been written to runs/tranche-sched-40287082679/ because .claude/ was not writable then. This run merged it into the library and appended its tracker rows; please check nothing in it was edited by hand in the meantime.',
  'Weekly-run tracker rows in runs/scheduled-39738926451, -40839989263 and -41999310782/tracker-rows/ are still not appended to data/. This run did not merge them; their entities were respected by hand in rotation.',
  'A research agent returned fabricated quotes and dead URLs for three B candidates (Yum China menu, Lululemon China +25%, HUL sachets). All were re-checked by direct fetch: the false items were cut or the candidate dropped. Worth knowing when reading earlier agent-sourced tranches.',
  'Approver review (Naman) of all ten posts before any is scheduled.'],
 notes='Ten of ten written, OJV-L031 to OJV-L040: A 2 (L031 IFR World Robotics 2026, L032 AgiBot via Counterpoint), B 3 (L033 Yum China, L034 Coca-Cola and Thums Up, L035 Maggi relaunch), C 3 (L036 Hyundai warranty, L037 CJ and Schwan\'s, L038 Kikkoman), D 0, F2 2 (L039 OJV Educate x corporate strategy teams, L040 lead generation x founder-led sales). D was capped at 4; none of 13 candidates passed (no count in the founder\'s own words, conflicting counts, or unreachable pages), so the slack went into B and C as instructed. E and F1 were not attempted because they cannot be batched. Sourcing by four parallel research agents, then every load-bearing quote in the B and C posts and the A headline figures re-fetched by the drafter; one agent report contained fabricated quotes, which were discarded. Numbering continued at L031 because L021 to L030 existed in the tranche-3 mirror; that mirror was merged into the library first (the earlier write-permission problem did not recur). OJV-L002 expired 2026-10-31 and was killed and removed from the queue. QUEUE.csv rewritten for all 39 live posts: no archetype more than twice in 5, no hook pattern twice in 6, no shared entity within 20, hard-CTA posts at 8, 14, 21, 26, 31 and 36, perishable posts first (L010 at 1; new A posts at 19 and 20, expiring Feb and Mar 2027). All 40 library drafts pass the style gate. Image intake skipped: no raw image folder in CI. Nothing was committed, scheduled or published.')
os.makedirs(R,exist_ok=True)
json.dump(res,open(R+'result.json','w'),indent=2,ensure_ascii=False)
print(len(posts),len(seen),len(dropped))
