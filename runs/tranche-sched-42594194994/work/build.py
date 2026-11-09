import re,csv,os
L='.claude/skills/ojv-linkedin/library/'; W='runs/tranche-sched-42594194994/work/'
order=open(W+'order.txt').read().split()
oldq={r['post_id']:r for r in csv.DictReader(open(L+'QUEUE.csv'))}
def block(s,name,nxt): return s.split('## '+name,1)[1].split('## '+nxt,1)[0].strip()
rows=[]
for i,pid in enumerate(order,1):
    s=open(L+pid+'.md').read()
    head,fm,body=s.split('---',2)
    fm=re.sub(r'^queue_no:.*\n','',fm,flags=re.M)
    fm=re.sub(r'(^voice:.*\n)',r'\1queue_no: %d\n'%i,fm,flags=re.M)
    s2='---'+fm+'---'+body
    open(L+pid+'.md','w').write(s2)
    copy=block(s2,'Copy','Photo brief')
    pf=L+'paste/'+pid+'.txt'
    if pid in oldq:
        assert open(pf).read().strip()==copy, pid
    else:
        open(pf,'w').write(copy+'\n')
    d=dict(re.findall(r'^(\w+):\s*(.*)$',fm,re.M))
    pick=re.search(r'PICK:\s*(.*?)\nAVOID',block(s2,'Photo brief','Alt text'),re.S).group(1).replace('\n',' ')
    if pid in oldq: r=dict(oldq[pid]); r['queue_no']=str(i)
    else: r=dict(queue_no=str(i),post_id=pid,archetype=d['archetype'],cta_tier=d['cta_tier'],hook_first_80=copy.split('\n')[0][:80],photo_brief_short=pick[:90],expires=d['expires'],status='library')
    rows.append(r)
# drop queue_no line from killed L002
s=open(L+'OJV-L002.md').read(); open(L+'OJV-L002.md','w').write(re.sub(r'^queue_no:.*\n','',s,flags=re.M))
w=csv.DictWriter(open(L+'QUEUE.csv','w',newline=''),fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print('queue rows',len(rows))
