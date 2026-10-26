import re,glob,random,csv,sys
L='.claude/skills/ojv-linkedin/library/'; N='runs/tranche-sched-40287082679/library/'
COUNTRIES={'india','japan','hungary','china','korea','uk','us','none','china biotech out-licensing','china industrial robotics'}
posts={}
for p in glob.glob(L+'OJV-L*.md')+glob.glob(N+'OJV-L*.md'):
    s=open(p).read(); fm=dict(re.findall(r'^(\w+):\s*(.*)$',s.split('---')[1],re.M))
    ents={e.strip().lower() for e in fm['entities'].split(';') if e.strip()}-COUNTRIES
    posts[fm['post_id']]=dict(a=fm['archetype'],h=fm['hook_pattern'],e=ents,c=fm['cta_tier'],x=fm['expires'][:10],path=p)
old=[r['post_id'] for r in csv.DictReader(open(L+'QUEUE.csv'))]
def bad(q):
    v=[]
    for i in range(len(q)):
        P=posts[q[i]]
        w=q[max(0,i-4):i+1]
        if sum(posts[k]['a']==P['a'] for k in w)>2: v.append((i,'arch'))
        for j in range(max(0,i-5),i):
            if posts[q[j]]['h']==P['h']: v.append((i,'hook',q[j]))
        for j in range(max(0,i-19),i):
            if posts[q[j]]['e']&P['e']: v.append((i,'ent',q[j],posts[q[j]]['e']&P['e']))
            if j>i-5 and P['c']=='hard' and posts[q[j]]['c']=='hard': v.append((i,'hard',q[j]))
    return v
def cost(q):
    c=0
    for i,k in enumerate(q):
        x=posts[k]['x']
        if x[:4].isdigit() and x<'2027-05-01': c+=i*(3 if x<'2027-01-01' else 1)
        if k in old: c+=abs(i-old.index(k))*0.5
    return c
new=sorted(k for k in posts if k not in old)
print('old violations',bad(old))
best=None
random.seed(1)
for t in range(40000):
    q=old[:]
    for k in new:
        q.insert(random.randint(2,len(q)),k)
    if bad(q): continue
    c=cost(q)
    if best is None or c<best[0]: best=(c,q)
print(best)
if best:
  for i,k in enumerate(best[1],1): print(i,k,posts[k]['a'],posts[k]['c'],posts[k]['h'],posts[k]['x'],sorted(posts[k]['e']))
# local search over full permutation, first two fixed
random.seed(7)
allk=old+new
bestq=None
for restart in range(60):
    q=allk[:2]+random.sample(allk[2:],len(allk)-2)
    f=lambda q: len(bad(q))*1000+cost(q)
    cur=f(q)
    for it in range(6000):
        i,j=random.sample(range(2,len(q)),2)
        q2=q[:]; q2[i],q2[j]=q2[j],q2[i]
        c2=f(q2)
        if c2<=cur: q,cur=q2,c2
    if not bad(q) and (bestq is None or cost(q)<bestq[0]): bestq=(cost(q),q)
print(bestq)
if bestq:
  open('runs/tranche-sched-40287082679/work/order.txt','w').write('\n'.join(bestq[1]))
  for i,k in enumerate(bestq[1],1): print(i,k,posts[k]['a'],posts[k]['c'],posts[k]['h'],posts[k]['x'],'old' if k in old else 'NEW',old.index(k)+1 if k in old else '')
