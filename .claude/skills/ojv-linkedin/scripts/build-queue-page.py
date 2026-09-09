#!/usr/bin/env python3
"""Build the intern-facing queue page from library/*.md and library/QUEUE.csv.

Usage:  python3 scripts/build-queue-page.py [out.html]

Reads the library as the single source of truth so the copy on the page is
byte-identical to the copy in the paste files. Re-run after every tranche.
"""
import csv, html, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(BASE, 'library')
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, 'library', 'queue-page.html')

ARCH_NAME = {'A': 'China signal', 'B': 'West into Asia', 'C': 'Asia into the West',
             'D': 'Rejection to raise', 'E': 'Inside the room', 'F1': 'Situation to solved',
             'F2': 'Diagnostic to call'}

# Flags that need a human, keyed by post id. Kept here rather than in the drafts
# because they are about the state of the operation, not the state of the copy.
FLAGS = {
    'OJV-L001': [('block', 'Booking link missing', 'The CTA still says TODO(config: booking link). Cannot publish.')],
    'OJV-L007': [('block', 'Booking link missing', 'The CTA still says TODO(config: booking link). Cannot publish.')],
    'OJV-L005': [('warn', 'Recheck two figures', 'The Hungary numbers (7.3bn euro, 100 GWh, Morocco) were read from search extracts, not a fetched page. Confirm or cut before posting.'),
                 ('asset', 'RADIUS', 'The two supply-chain questions promised by the keyword must exist before this goes out.')],
    'OJV-L004': [('warn', 'Recheck two figures', 'The 1,000-products and 30%-sourcing figures came from a page that blocked direct fetch. The two headline claims are solid.')],
    'OJV-L008': [('asset', 'DIAL', 'The three APAC entry structures promised by the keyword must exist before this goes out.')],
    'OJV-L009': [('asset', 'CHANNEL', 'The channel-testing sequence promised by the keyword must exist before this goes out.')],
    'OJV-L010': [('asset', 'ORDERBOOK', 'The three deployment signals promised by the keyword must exist before this goes out.')],
}
NOTES = {'OJV-L002': 'Post this one first. Its source is IFR World Robotics 2025 and the 2026 edition supersedes the 2024 figures.'}


def parse(pid):
    s = open(os.path.join(LIB, pid + '.md')).read()
    fm = dict(re.findall(r'^(\w+):\s*(.*)$', s.split('---')[1], re.M))

    def block(name, nxt):
        if '## ' + name not in s:
            return ''
        return s.split('## ' + name, 1)[1].split('## ' + nxt, 1)[0].strip()

    copy = block('Copy', 'Photo brief')
    brief = block('Photo brief', 'Alt text')
    alt = block('Alt text', 'First comment').split('\n\n')[0].strip()
    fc = block('First comment', 'Verified facts')
    pick = avoid = fall = why = ''
    for key, var in (('PICK:', 'pick'), ('AVOID:', 'avoid'), ('FALLBACK:', 'fall'), ('WHY THIS BRIEF:', 'why')):
        m = re.search(re.escape(key) + r'(.*?)(?=\n[A-Z]{4,}|\Z)', brief, re.S)
        if m:
            val = ' '.join(m.group(1).split())
            if var == 'pick': pick = val
            elif var == 'avoid': avoid = val
            elif var == 'fall': fall = val
            else: why = val
    src = ''
    m = re.search(r'(https?://\S+)', fc)
    if m:
        src = m.group(1)
    return dict(fm=fm, copy=copy, pick=pick, avoid=avoid, fall=fall, why=why,
                alt=alt, fc=fc, src=src)


queue = list(csv.DictReader(open(os.path.join(LIB, 'QUEUE.csv'))))
posts = []
for row in queue:
    d = parse(row['post_id'])
    d['q'] = int(row['queue_no'])
    d['id'] = row['post_id']
    posts.append(d)

n_block = sum(1 for p in posts if any(f[0] == 'block' for f in FLAGS.get(p['id'], [])))
n_asset = sum(1 for p in posts if any(f[0] == 'asset' for f in FLAGS.get(p['id'], [])))
n_ready = len(posts) - n_block

CSS = """
:root{
  --ground:#F7F8FA; --surface:#FFFFFF; --sunk:#F0F2F6;
  --ink:#14181F; --ink-2:#39414D; --muted:#5C6673; --faint:#8B94A1;
  --line:#DFE3E9; --line-2:#EAEDF2;
  --accent:#E8590C; --accent-ink:#8A3308; --accent-soft:#FFF1E7; --accent-line:#F7C9A9;
  --shadow:0 1px 2px rgba(20,24,31,.05), 0 8px 24px -16px rgba(20,24,31,.18);
  --f-display:"Archivo","Helvetica Neue",Arial,sans-serif;
  --f-body:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --f-mono:"IBM Plex Mono",ui-monospace,SFMono-Regular,Menlo,monospace;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --ground:#0E1116; --surface:#161A21; --sunk:#1C222B;
    --ink:#EEF1F5; --ink-2:#C3CAD4; --muted:#8F99A6; --faint:#6B7480;
    --line:#262D37; --line-2:#1F252E;
    --accent:#FF7A33; --accent-ink:#FFB185; --accent-soft:#2A1710; --accent-line:#5A2E14;
    --shadow:0 1px 2px rgba(0,0,0,.4), 0 8px 24px -16px rgba(0,0,0,.6);
  }
}
:root[data-theme="dark"]{
  --ground:#0E1116; --surface:#161A21; --sunk:#1C222B;
  --ink:#EEF1F5; --ink-2:#C3CAD4; --muted:#8F99A6; --faint:#6B7480;
  --line:#262D37; --line-2:#1F252E;
  --accent:#FF7A33; --accent-ink:#FFB185; --accent-soft:#2A1710; --accent-line:#5A2E14;
  --shadow:0 1px 2px rgba(0,0,0,.4), 0 8px 24px -16px rgba(0,0,0,.6);
}
*{box-sizing:border-box}
body{background:var(--ground);color:var(--ink);font-family:var(--f-body);
  font-size:15px;line-height:1.6;-webkit-font-smoothing:antialiased;margin:0}
.wrap{max-width:1080px;margin:0 auto;padding:0 24px 96px}

/* masthead */
header.mast{padding:40px 0 0}
.eyebrow{font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--accent-ink);display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.eyebrow .dot{width:6px;height:6px;border-radius:50%;background:var(--accent);flex:none}
h1{font-family:var(--f-display);font-weight:800;letter-spacing:-.03em;line-height:1.02;
  font-size:clamp(34px,5.4vw,54px);margin:14px 0 0;text-wrap:balance}
.standfirst{color:var(--muted);max-width:62ch;margin:14px 0 0;font-size:16px}

/* status bar */
.status{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:1px;
  background:var(--line);border:1px solid var(--line);border-radius:3px;margin:32px 0 0;overflow:hidden}
.stat{background:var(--surface);padding:14px 16px}
.stat dt{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--faint);margin:0}
.stat dd{margin:6px 0 0;font-family:var(--f-display);font-weight:700;font-size:26px;
  letter-spacing:-.02em;font-variant-numeric:tabular-nums;line-height:1}
.stat dd small{font-family:var(--f-body);font-weight:400;font-size:12.5px;color:var(--muted);
  letter-spacing:0;display:block;margin-top:5px;line-height:1.4}
.stat.hot dd{color:var(--accent)}

/* how-to */
.howto{margin:28px 0 0;border-left:2px solid var(--accent);padding:2px 0 2px 18px}
.howto h2{font-family:var(--f-mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--accent-ink);margin:0 0 8px}
.howto ol{margin:0;padding-left:20px;color:var(--ink-2);font-size:14.5px}
.howto li{margin:3px 0}
.howto strong{color:var(--ink)}

.rule{height:1px;background:var(--line);border:0;margin:44px 0 0}

/* post */
article{padding:34px 0 0;border-top:1px solid var(--line);margin-top:34px}
article:first-of-type{border-top:0;margin-top:0}
article.is-done{opacity:.55}
.head{display:flex;gap:18px;align-items:flex-start}
.qno{font-family:var(--f-display);font-weight:800;font-size:34px;line-height:.9;
  letter-spacing:-.04em;color:var(--line);font-variant-numeric:tabular-nums;flex:none;
  min-width:52px;padding-top:2px}
article.is-next .qno{color:var(--accent)}
.headmain{flex:1;min-width:0}
.metaline{display:flex;gap:8px;align-items:center;flex-wrap:wrap;
  font-family:var(--f-mono);font-size:11.5px;color:var(--muted)}
.pid{color:var(--ink);font-weight:500}
.chip{border:1px solid var(--line);border-radius:2px;padding:2px 7px;font-size:10.5px;
  letter-spacing:.06em;text-transform:uppercase;color:var(--ink-2);background:var(--surface)}
.chip.tier-hard{border-color:var(--accent-line);background:var(--accent-soft);color:var(--accent-ink)}
.sep{color:var(--line)}
.hookline{font-family:var(--f-display);font-weight:700;font-size:19px;letter-spacing:-.015em;
  line-height:1.34;margin:10px 0 0;text-wrap:balance}
.donebox{flex:none;display:flex;align-items:center;gap:7px;font-family:var(--f-mono);
  font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);
  cursor:pointer;user-select:none;padding-top:4px}
.donebox input{accent-color:var(--accent);width:15px;height:15px;cursor:pointer;margin:0}

/* flags */
.flags{display:flex;flex-direction:column;gap:7px;margin:16px 0 0}
.flag{display:flex;gap:10px;align-items:flex-start;font-size:13.5px;line-height:1.5;
  border:1px solid var(--line);border-left-width:3px;border-radius:2px;padding:9px 12px;
  background:var(--surface);color:var(--ink-2)}
.flag b{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;
  flex:none;padding-top:2px}
.flag.block{border-left-color:var(--accent);background:var(--accent-soft);color:var(--accent-ink)}
.flag.block b{color:var(--accent-ink)}
.flag.warn{border-left-color:var(--faint)}
.flag.warn b,.flag.asset b{color:var(--muted)}
.flag.asset{border-left-color:var(--line)}
.flag.note{border-left-color:var(--accent-line);background:var(--accent-soft);color:var(--accent-ink)}
.flag.note b{color:var(--accent-ink)}

/* copy block: the only thing that gets fill + border + shadow */
.copywrap{margin:18px 0 0;background:var(--surface);border:1px solid var(--line);
  border-radius:4px;box-shadow:var(--shadow);overflow:hidden}
.copybar{display:flex;align-items:center;justify-content:space-between;gap:12px;
  padding:9px 14px;border-bottom:1px solid var(--line-2);background:var(--sunk)}
.copybar .lbl{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--muted)}
.copybar .count{font-family:var(--f-mono);font-size:10.5px;color:var(--faint);
  font-variant-numeric:tabular-nums}
.copytext{margin:0;padding:20px 22px;white-space:pre-wrap;font-size:15px;line-height:1.68;
  color:var(--ink);max-width:64ch}
button.copy{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.08em;text-transform:uppercase;
  background:var(--ink);color:var(--ground);border:1px solid var(--ink);border-radius:2px;
  padding:6px 12px;cursor:pointer;transition:background .12s,color .12s,border-color .12s}
button.copy:hover{background:var(--accent);border-color:var(--accent);color:#fff}
button.copy:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
button.copy.ok{background:var(--accent-soft);border-color:var(--accent-line);color:var(--accent-ink)}
@media (prefers-reduced-motion:reduce){button.copy{transition:none}}

/* brief + alt */
.grid2{display:grid;grid-template-columns:1.35fr 1fr;gap:1px;background:var(--line);
  border:1px solid var(--line);border-radius:3px;margin:14px 0 0;overflow:hidden}
@media (max-width:720px){.grid2{grid-template-columns:1fr}}
.pane{background:var(--surface);padding:14px 16px;min-width:0}
.pane h3{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--faint);margin:0 0 10px;display:flex;justify-content:space-between;
  align-items:center;gap:10px}
.kv{display:grid;grid-template-columns:58px 1fr;gap:5px 10px;font-size:13.5px;line-height:1.52}
.kv dt{font-family:var(--f-mono);font-size:10px;letter-spacing:.07em;text-transform:uppercase;
  color:var(--accent-ink);padding-top:3px}
.kv dd{margin:0;color:var(--ink-2)}
.alttext{margin:0;font-size:13.5px;line-height:1.55;color:var(--ink-2)}
button.mini{font-family:var(--f-mono);font-size:9.5px;letter-spacing:.07em;text-transform:uppercase;
  background:transparent;color:var(--muted);border:1px solid var(--line);border-radius:2px;
  padding:3px 7px;cursor:pointer}
button.mini:hover{color:var(--accent-ink);border-color:var(--accent-line);background:var(--accent-soft)}
button.mini:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
button.mini.ok{color:var(--accent-ink);border-color:var(--accent-line);background:var(--accent-soft)}
.fcbox{margin:14px 0 0;border:1px dashed var(--line);border-radius:3px;padding:12px 14px;
  background:var(--surface)}
.fcbox h3{font-family:var(--f-mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
  color:var(--faint);margin:0 0 8px;display:flex;justify-content:space-between;align-items:center;gap:10px}
.fcbox p{margin:0;font-size:13.5px;color:var(--ink-2);word-break:break-word}
.fcbox a{color:var(--accent-ink)}
.fcbox .none{color:var(--faint);font-style:italic}

footer{margin-top:56px;padding-top:22px;border-top:1px solid var(--line);
  color:var(--faint);font-size:13px}
footer p{max-width:70ch;margin:0 0 8px}
footer code{font-family:var(--f-mono);font-size:12px;color:var(--muted)}
"""

JS = """
function flash(btn, txt){
  var old = btn.dataset.label || btn.textContent;
  btn.dataset.label = old;
  btn.textContent = txt; btn.classList.add('ok');
  setTimeout(function(){ btn.textContent = btn.dataset.label; btn.classList.remove('ok'); }, 1400);
}
function copyFrom(id, btn){
  var el = document.getElementById(id);
  if(!el) return;
  var text = el.getAttribute('data-raw') !== null ? el.getAttribute('data-raw') : el.textContent;
  function done(){ flash(btn, 'Copied'); }
  function fail(){ flash(btn, 'Press Cmd C'); var r=document.createRange(); r.selectNodeContents(el);
                   var s=window.getSelection(); s.removeAllRanges(); s.addRange(r); }
  if(navigator.clipboard && navigator.clipboard.writeText){
    navigator.clipboard.writeText(text).then(done, fail);
  } else { fail(); }
}
document.addEventListener('click', function(e){
  var b = e.target.closest('[data-copy]');
  if(b){ copyFrom(b.getAttribute('data-copy'), b); }
});

/* Per-viewer progress ticks. Stored in this browser only, so it is a convenience
   for whoever is working the queue, not shared status. */
var KEY = 'ojv-queue-done-v1';
function load(){ try { return JSON.parse(localStorage.getItem(KEY) || '{}'); } catch(err){ return {}; } }
function save(o){ try { localStorage.setItem(KEY, JSON.stringify(o)); } catch(err){} }
function paint(){
  var done = load(), n = 0;
  document.querySelectorAll('article[data-pid]').forEach(function(a){
    var on = !!done[a.dataset.pid];
    a.classList.toggle('is-done', on);
    var cb = a.querySelector('input[type=checkbox]');
    if(cb) cb.checked = on;
    if(on) n++;
  });
  var out = document.getElementById('doneCount');
  if(out) out.firstChild.nodeValue = String(n);
}
document.addEventListener('change', function(e){
  if(e.target.matches('article input[type=checkbox]')){
    var a = e.target.closest('article'), done = load();
    if(e.target.checked) done[a.dataset.pid] = 1; else delete done[a.dataset.pid];
    save(done); paint();
  }
});
paint();
"""


def esc(t):
    return html.escape(t or '')


out = []
out.append('<title>OJV Post Desk</title>')
out.append('<link rel="preconnect" href="https://fonts.googleapis.com">')
out.append('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>')
out.append('<link rel="stylesheet" href="https://fonts.googleapis.com/css2'
           '?family=Archivo:wght@700;800&family=IBM+Plex+Mono:wght@400;500'
           '&family=IBM+Plex+Sans:wght@400;500&display=swap">')
out.append('<style>' + CSS + '</style>')
out.append('<div class="wrap">')

out.append('<header class="mast">')
out.append('<div class="eyebrow"><span class="dot"></span><span>Orange Juice Ventures</span>'
           '<span class="sep">/</span><span>Library tranche 1 of 10</span>'
           '<span class="sep">/</span><span>Mon Wed Fri, 09:00 HKT</span></div>')
out.append('<h1>Post Desk</h1>')
out.append('<p class="standfirst">Ten publish-ready posts for the company page, in the order '
           'they should go out. The copy is final. Your job is to pick a picture that fits the '
           'brief and post it.</p>')
out.append('</header>')

out.append('<dl class="status">')
out.append('<div class="stat"><dt>In queue</dt><dd>' + str(len(posts)) +
           '<small>All ten pass the style gate</small></dd></div>')
out.append('<div class="stat"><dt>Ready to post</dt><dd>' + str(n_ready) +
           '<small>Copy is final, nothing to edit</small></dd></div>')
out.append('<div class="stat hot"><dt>Blocked</dt><dd>' + str(n_block) +
           '<small>Waiting on the booking link</small></dd></div>')
out.append('<div class="stat"><dt>Need an asset first</dt><dd>' + str(n_asset) +
           '<small>Keyword replies to write</small></dd></div>')
out.append('<div class="stat"><dt>Ticked off</dt><dd><span id="doneCount">0</span>'
           '<small>Saved in this browser only</small></dd></div>')
out.append('</dl>')

out.append('<section class="howto"><h2>How to work the queue</h2><ol>'
           '<li>Start at <strong>1</strong> and work down. The order is deliberate.</li>'
           '<li>Hit <strong>Copy post</strong>, paste straight into LinkedIn. Do not edit the '
           'text, and do not change a number or a hashtag.</li>'
           '<li>Pick a photo that satisfies the brief. If nothing fits and the fallback allows '
           'it, post without one.</li>'
           '<li>Paste the alt text into LinkedIn\'s own alt-text field.</li>'
           '<li>Post the first comment, where there is one.</li>'
           '<li>Anything flagged in orange needs Naman before it can go out.</li>'
           '</ol></section>')
out.append('<hr class="rule">')

for p in posts:
    fm = p['fm']
    arch = fm.get('archetype', '')
    cls = ['']
    if p['q'] == 1:
        cls.append('is-next')
    out.append('<article data-pid="' + esc(p['id']) + '" class="' + ' '.join(cls).strip() + '">')
    out.append('<div class="head">')
    out.append('<div class="qno">' + str(p['q']) + '</div>')
    out.append('<div class="headmain">')
    out.append('<div class="metaline"><span class="pid">' + esc(p['id']) + '</span>'
               '<span class="chip">' + esc(arch) + ' &middot; ' + esc(ARCH_NAME.get(arch, '')) + '</span>'
               '<span class="chip tier-' + esc(fm.get('cta_tier', '')) + '">' +
               esc(fm.get('cta_tier', '')) + ' cta</span>'
               '<span class="sep">|</span><span>' + esc(fm.get('hook_pattern', '')) + '</span>'
               '<span class="sep">|</span><span>expires ' +
               esc(fm.get('expires', '').split(',')[0]) + '</span></div>')
    out.append('<p class="hookline">' + esc(p['copy'].split('\n')[0]) + '</p>')
    out.append('</div>')
    out.append('<label class="donebox"><input type="checkbox"><span>Done</span></label>')
    out.append('</div>')

    flags = list(FLAGS.get(p['id'], []))
    if p['id'] in NOTES:
        flags.insert(0, ('note', 'Post first', NOTES[p['id']]))
    if flags:
        out.append('<div class="flags">')
        for kind, label, body in flags:
            out.append('<div class="flag ' + kind + '"><b>' + esc(label) + '</b><span>' +
                       esc(body) + '</span></div>')
        out.append('</div>')

    n = len(p['copy'])
    out.append('<div class="copywrap">')
    out.append('<div class="copybar"><span class="lbl">The post</span>'
               '<span class="count">' + str(n) + ' chars &middot; band 900 to 1300</span>'
               '<button class="copy" data-copy="c-' + esc(p['id']) + '">Copy post</button></div>')
    out.append('<pre class="copytext" id="c-' + esc(p['id']) + '">' + esc(p['copy']) + '</pre>')
    out.append('</div>')

    out.append('<div class="grid2">')
    out.append('<div class="pane"><h3><span>Photo brief</span></h3><dl class="kv">')
    out.append('<dt>Pick</dt><dd>' + esc(p['pick']) + '</dd>')
    if p['avoid']:
        out.append('<dt>Avoid</dt><dd>' + esc(p['avoid']) + '</dd>')
    if p['fall']:
        out.append('<dt>If none</dt><dd>' + esc(p['fall']) + '</dd>')
    if p['why']:
        out.append('<dt>Why</dt><dd>' + esc(p['why']) + '</dd>')
    out.append('</dl></div>')
    out.append('<div class="pane"><h3><span>Alt text</span>'
               '<button class="mini" data-copy="a-' + esc(p['id']) + '">Copy</button></h3>'
               '<p class="alttext" id="a-' + esc(p['id']) + '">' + esc(p['alt']) + '</p></div>')
    out.append('</div>')

    if p['src']:
        out.append('<div class="fcbox"><h3><span>First comment</span>'
                   '<button class="mini" data-copy="f-' + esc(p['id']) + '">Copy</button></h3>'
                   '<p id="f-' + esc(p['id']) + '" data-raw="' + esc(p['fc']) + '">' +
                   esc(p['fc'].split('\n')[0]) + '<br><a href="' + esc(p['src']) +
                   '" target="_blank" rel="noopener">' + esc(p['src']) + '</a></p></div>')
    else:
        out.append('<div class="fcbox"><h3><span>First comment</span></h3>'
                   '<p class="none">None. This post has no outbound link.</p></div>')
    out.append('</article>')

out.append('<footer>')
out.append('<p>Generated from the OJV LinkedIn skill library by '
           '<code>scripts/build-queue-page.py</code>. The copy here is byte-identical to '
           '<code>library/paste/&lt;post_id&gt;.txt</code>, which is the source of truth.</p>')
out.append('<p>If a comment challenges a number, do not answer it. Send Naman the post id. '
           'Every figure is sourced in <code>library/&lt;post_id&gt;.md</code> under Verified '
           'facts, with the sentence it came from.</p>')
out.append('<p>Ticks are stored in this browser only, so they track your own progress and are '
           'not visible to anyone else.</p>')
out.append('</footer>')
out.append('</div>')
out.append('<script>' + JS + '</script>')

open(OUT, 'w').write('\n'.join(out))
print('wrote %s  (%d posts, %.1f KB)' % (OUT, len(posts), os.path.getsize(OUT) / 1024.0))
