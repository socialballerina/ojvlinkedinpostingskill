import re,glob,csv,os,shutil
R='runs/tranche-sched-40287082679/'
L='.claude/skills/ojv-linkedin/library/'; N=R+'library/'
order=open(R+'work/order.txt').read().split()
os.makedirs(N+'paste',exist_ok=True)
oldq={r['post_id']:r for r in csv.DictReader(open(L+'QUEUE.csv'))}
def src(pid):
    return N+pid+'.md' if os.path.exists(N+pid+'.md') and pid not in oldq else L+pid+'.md'
def block(s,name,nxt):
    return s.split('## '+name,1)[1].split('## '+nxt,1)[0].strip()
rows=[]
for i,pid in enumerate(order,1):
    s=open(src(pid)).read()
    # set queue_no in front matter
    head,fm,body=s.split('---',2)
    fm=re.sub(r'^queue_no:.*\n','',fm,flags=re.M)
    fm=re.sub(r'(^voice:.*\n)',r'\1queue_no: %d\n'%i,fm,flags=re.M)
    s2='---'+fm+'---'+body
    open(N+pid+'.md','w').write(s2)
    copy=block(s2,'Copy','Photo brief')
    pf=N+'paste/'+pid+'.txt'
    if pid in oldq:
        shutil.copy(L+'paste/'+pid+'.txt',pf)
        assert open(pf).read().strip()==copy, pid
    else:
        open(pf,'w').write(copy+'\n')
    d=dict(re.findall(r'^(\w+):\s*(.*)$',fm,re.M))
    brief=block(s2,'Photo brief','Alt text')
    pick=re.search(r'PICK:\s*(.*?)\nAVOID',brief,re.S).group(1).replace('\n',' ')
    if pid in oldq:
        r=dict(oldq[pid]); r['queue_no']=str(i)
    else:
        r=dict(queue_no=str(i),post_id=pid,archetype=d['archetype'],cta_tier=d['cta_tier'],
               hook_first_80=copy.split('\n')[0][:80],photo_brief_short=pick[:90],expires=d['expires'],status='library')
    rows.append(r)
w=csv.DictWriter(open(N+'QUEUE.csv','w',newline=''),fieldnames=list(rows[0].keys()))
w.writeheader(); w.writerows(rows)
print('ok',len(rows))
