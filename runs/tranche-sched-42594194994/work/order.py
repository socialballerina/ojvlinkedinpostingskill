import re,glob,random,csv
L='.claude/skills/ojv-linkedin/library/'
W='runs/tranche-sched-42594194994/work/'
NONENT={'india','japan','hungary','china','korea','uk','us','none','china biotech out-licensing','china industrial robotics'}
posts={}
for p in sorted(glob.glob(L+'OJV-L*.md')):
    s=open(p).read(); fm=dict(re.findall(r'^(\w+):\s*(.*)$',s.split('---')[1],re.M))
    if fm.get('status')=='killed': continue
    ents={e.strip().lower() for e in fm['entities'].split(';') if e.strip()}-NONENT
    posts[fm['post_id']]=dict(a=fm['archetype'],h=fm['hook_pattern'],e=ents,c=fm['cta_tier'],x=fm['expires'][:10])
old=[r['post_id'] for r in csv.DictReader(open(L+'QUEUE.csv')) if r['post_id'] in posts]
new=sorted(k for k in posts if k not in old)
def bad(q):
    v=[]
    for i in range(len(q)):
        P=posts[q[i]]
        if sum(posts[k]['a']==P['a'] for k in q[max(0,i-4):i+1])>2: v.append((i,'arch'))
        for j in range(max(0,i-5),i):
            if posts[q[j]]['h']==P['h']: v.append((i,'hook',q[j]))
        for j in range(max(0,i-19),i):
            if posts[q[j]]['e']&P['e']: v.append((i,'ent',q[j]))
            if j>i-5 and P['c']=='hard' and posts[q[j]]['c']=='hard': v.append((i,'hard',q[j]))
    # genre: keep the three US-food-in-China/India restructurings apart
    return v
def cost(q):
    c=0
    for i,k in enumerate(q):
        x=posts[k]['x']
        if x[:4].isdigit() and x<'2027-06-01': c+=i*(4 if x<'2027-01-01' else 1.5)
        if k in old: c+=abs(i-old.index(k))*0.4
    if abs(q.index('OJV-L033')-q.index('OJV-L008'))<8: c+=200
    return c
print('old order violations:',bad(old))
random.seed(11); allk=old+new; best=None
f=lambda q: len(bad(q))*1000+cost(q)
for r in range(80):
    q=old[:1]+random.sample(allk[1:],len(allk)-1) if r else old+new
    cur=f(q)
    for it in range(5000):
        i,j=random.sample(range(1,len(q)),2)
        q2=q[:]; q2[i],q2[j]=q2[j],q2[i]
        c2=f(q2)
        if c2<=cur: q,cur=q2,c2
    if not bad(q) and (best is None or cost(q)<best[0]): best=(cost(q),q)
print('best cost',best[0])
open(W+'order.txt','w').write('\n'.join(best[1]))
for i,k in enumerate(best[1],1): print(i,k,posts[k]['a'],posts[k]['c'],posts[k]['h'],posts[k]['x'],'NEW' if k in new else old.index(k)+1)
