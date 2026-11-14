#!/usr/bin/env python3
"""Builds index.html (the audit-workpaper viewer) from claims_final.csv.
  python build_all.py                      -> claims_final.csv -> index.html
  python build_all.py my.csv out.html      -> custom paths
  python build_all.py --only-verified      -> hide provisional / unverifiable rows
Rows with status incomplete / excluded / draft are never shown."""
import csv, json, sys, datetime

args = [a for a in sys.argv[1:] if not a.startswith("--")]
SRC = args[0] if args else "claims_final.csv"
OUT = args[1] if len(args) > 1 else "index.html"
ONLY_VERIFIED = "--only-verified" in sys.argv

META = {
    "title": "Do Their Numbers Match?",
    "sub": "A pilot audit of quantitative claims about Nigeria\u2019s economy, each traced to its primary comparator.",
    "author": "Trisma Kuulbudam",
    "event": "Apart Research AI x Epistemics Sprint, Nov 2026",
    "built": datetime.date.today().isoformat(),
}
NAMES = {"N01": "Below the Target", "N02a": "The Q4 Print", "N02b": "The Annual Print", "N03": "Just Fourteen",
         "N04": "The New Method", "N07": "Seven Point Four", "N08": "The Net Figure", "N17": "The Gross Figure",
         "N19": "The December Print", "N21": "Six Point Five One", "N22": "The Seven Seventy-Two", "N33": "Which November"}
FIELDS = ["id", "sample", "claim_text", "speaker", "speaker_type", "date", "metric", "claimed_value", "claimed_period",
          "claim_url", "comparator", "primary_url", "primary_excerpt", "primary_value", "label", "definition_note",
          "notes", "status", "evidence_type", "independence_group", "case_name"]

rows = []
with open(SRC, encoding="utf-8-sig", newline="") as f:
    for r in csv.DictReader(f):
        st = (r.get("status") or "").strip().lower()
        if st in {"incomplete", "excluded", "draft"}:
            continue
        if ONLY_VERIFIED and st != "verified":
            continue
        o = {k: (r.get(k) or "").strip() for k in FIELDS}
        o["case_name"] = o["case_name"] or NAMES.get(o["id"], o["id"])
        rows.append(o)

def js(o):  # safe to embed inside <script>
    return json.dumps(o, ensure_ascii=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")

TEMPLATE = r'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Do Their Numbers Match? Audit file</title>
<style>
:root{--bg:#f3f1ea;--sheet:#fffefb;--ink:#17150f;--mut:#6b665a;--rule:#d9d4c5;--grid:#e9e5d8;--acc:#1f3b73;
--match:#1f6f4a;--rounding:#8a6a14;--definition:#5b3d8f;--period:#1f4e8c;--numerical:#a3261e;--unsupported:#b4540a;--unverifiable:#5d6169;
--serif:"Iowan Old Style",Charter,"Palatino Linotype",Georgia,serif;--sans:system-ui,-apple-system,"Segoe UI",sans-serif;--mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace}
@media(prefers-color-scheme:dark){:root{--bg:#14130f;--sheet:#1c1b16;--ink:#ece8da;--mut:#a39d8c;--rule:#38352c;--grid:#25231d;--acc:#8fb0ff;
--match:#5fc592;--rounding:#d9b24a;--definition:#b496ee;--period:#7fb0ff;--numerical:#ff7a6e;--unsupported:#ff9b52;--unverifiable:#a0a4ac}}
*{box-sizing:border-box;margin:0}body{background:var(--bg);color:var(--ink);font:15px/1.55 var(--sans)}
.wrap{max-width:1240px;margin:0 auto;padding:0 28px 90px}a{color:var(--acc)}button{font:inherit;color:inherit;cursor:pointer}
:focus-visible{outline:2px solid var(--acc);outline-offset:2px}
header.top{padding:46px 0 28px;border-bottom:2px solid var(--ink);background:repeating-linear-gradient(transparent 0 27px,var(--grid) 27px 28px)}
.k{font:600 11px var(--mono);letter-spacing:.16em;text-transform:uppercase;color:var(--mut)}
h1{font:600 clamp(36px,6vw,70px)/1 var(--serif);letter-spacing:-.02em;margin:10px 0 12px}
.sub{font:italic 20px/1.4 var(--serif);color:var(--mut);max-width:740px}
.meta{display:flex;flex-wrap:wrap;gap:8px 40px;margin-top:22px}.meta b{display:block;font:600 13px var(--mono);color:var(--ink);margin-top:2px;letter-spacing:0;text-transform:none}
h2{font:600 26px var(--serif);margin:54px 0 6px;letter-spacing:-.01em}.lead{color:var(--mut);max-width:780px;margin-bottom:18px}
.find{display:grid;grid-template-columns:1.2fr 1fr 1fr;gap:0;border:1px solid var(--ink);background:var(--sheet);margin-top:26px}
.find>div{padding:20px 24px;border-right:1px solid var(--rule)}.find>div:last-child{border:0}
.big{font:600 48px/1 var(--serif);font-variant-numeric:lining-nums}.find p{color:var(--mut);margin-top:8px;font-size:14px}
.pill{display:inline-flex;gap:6px;align-items:center;font:600 11px var(--mono);letter-spacing:.06em;margin:6px 12px 0 0}
.dot{width:10px;height:10px;border-radius:50%;background:currentColor;display:inline-block}
.warn{margin-top:14px;padding:10px 16px;border-left:4px solid var(--rounding);background:var(--sheet);font-size:14px;color:var(--mut)}
.tools{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:16px}
.chip{border:1px solid var(--ink);background:var(--sheet);padding:5px 11px;font:600 11px var(--mono);letter-spacing:.06em;text-transform:uppercase}
.chip.on{background:var(--ink);color:var(--bg)}input[type=search]{flex:1;min-width:180px;max-width:320px;padding:7px 11px;border:1px solid var(--ink);background:var(--sheet);color:var(--ink);font:14px var(--sans)}
.board{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(190px,1fr);gap:14px;overflow-x:auto;padding-bottom:6px}
.lane{border-top:3px solid var(--ink);padding-top:8px}.lane h3{font:600 12px var(--mono);letter-spacing:.12em;text-transform:uppercase}
.lane small{display:block;color:var(--mut);font-size:12px;margin-bottom:8px}
.card{display:block;width:100%;text-align:left;margin:0 0 8px;padding:10px 12px;background:var(--sheet);border:1px solid var(--rule);border-left:5px solid var(--c);transition:.12s}
.card:hover{transform:translateY(-1px);border-color:var(--ink)}.card.sel{outline:2px solid var(--ink);outline-offset:1px}.card.dim{opacity:.22}
.card b{font:600 11px var(--mono);color:var(--c);letter-spacing:.08em}.card i{display:block;font:600 15px var(--serif)}.card span{font-size:12px;color:var(--mut)}
.card .g{float:right;font:600 10px var(--mono);border:1px solid var(--mut);padding:0 5px;color:var(--mut)}
.sheet{background:var(--sheet);border:1px solid var(--ink);box-shadow:6px 6px 0 var(--rule)}
.sh{display:flex;flex-wrap:wrap;gap:14px 28px;align-items:center;padding:16px 24px;border-bottom:2px solid var(--ink);background:repeating-linear-gradient(transparent 0 23px,var(--grid) 23px 24px)}
.sh h3{font:600 28px var(--serif);font-style:italic}.sh .sp{flex:1}
.stamp{font:700 11px var(--mono);letter-spacing:.14em;text-transform:uppercase;color:var(--c);border:2px solid var(--c);padding:6px 10px;transform:rotate(-2deg);box-shadow:inset 0 0 0 2px var(--sheet),inset 0 0 0 3px var(--c);background:var(--sheet)}
.stamp.prov{border-style:dashed}
.cols{display:grid;grid-template-columns:1fr 1fr 1fr}.col{padding:22px 24px;border-right:1px solid var(--rule)}.col:last-child{border:0}
.col h4{margin-bottom:10px}blockquote{font:italic 16.5px/1.55 var(--serif);border-left:3px solid var(--rule);padding-left:14px;margin:8px 0 12px}
mark{background:none;color:var(--ink);font-weight:700;box-shadow:inset 0 -.5em 0 color-mix(in srgb,var(--c) 28%,transparent)}
.src{font:12px var(--mono);color:var(--mut)}.btn{border:1px solid var(--ink);background:none;padding:4px 10px;font:600 11px var(--mono);margin:6px 8px 0 0}
.tie{width:100%;border-collapse:collapse;font-size:14px}.tie td{padding:7px 0;border-bottom:1px dotted var(--rule);vertical-align:top}.tie td:first-child{color:var(--mut);width:42%;padding-right:10px}
.tick{display:inline-block;width:20px;height:20px;border-radius:50%;text-align:center;font:700 12px/20px var(--mono);color:#fff;margin-right:6px}
.t-ok{background:var(--match)}.t-no{background:var(--numerical)}.t-na{background:var(--unverifiable)}.t-b{background:var(--rounding)}
.ladder{border-top:2px solid var(--ink);padding:16px 24px 20px}.rung{display:grid;grid-template-columns:30px 220px 1fr;padding:6px 0;border-bottom:1px dotted var(--rule);color:var(--mut);font-size:14px}
.rung.stop{color:var(--ink);background:color-mix(in srgb,var(--c) 14%,transparent);font-weight:600;margin:0 -8px;padding:6px 8px;border-left:4px solid var(--c)}.rung.after{opacity:.45}
.note{margin-top:12px;padding:12px 16px;border-left:4px solid var(--rounding);background:var(--bg);font-size:14px}
.rev{border-top:1px solid var(--rule);padding:16px 24px;background:var(--bg);display:grid;grid-template-columns:1fr 1fr;gap:6px 28px}
.rev label{display:block;font-size:14px}textarea{width:100%;height:64px;padding:8px;border:1px solid var(--ink);background:var(--sheet);color:var(--ink);font:14px var(--sans)}
.ex{background:var(--sheet);border:1px solid var(--ink);padding:24px;margin-bottom:22px}.ex h3{font:italic 600 24px var(--serif)}
.sel2{display:flex;flex-wrap:wrap;gap:10px 22px;margin:14px 0}.sel2 label{font:600 11px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--mut)}
select{display:block;margin-top:3px;padding:6px 10px;border:1px solid var(--ink);background:var(--sheet);color:var(--ink);font:600 14px var(--mono)}
.res{font:600 44px/1 var(--serif)}table.t{width:100%;border-collapse:collapse;font-size:14px;margin-top:12px}.t th{font:600 10px var(--mono);letter-spacing:.12em;text-transform:uppercase;text-align:left;color:var(--mut);border-bottom:1px solid var(--ink);padding:6px}
.t td{padding:7px 6px;border-bottom:1px dotted var(--rule);font-variant-numeric:tabular-nums}.two{display:grid;grid-template-columns:1fr 1fr;gap:28px}
.bar{height:16px;background:var(--match);margin:3px 0}.bar.b2{background:var(--period)}
ul.lim{padding-left:20px;max-width:820px}ul.lim li{margin:5px 0}footer{margin-top:60px;padding-top:16px;border-top:2px solid var(--ink);color:var(--mut);font-size:13px}
@media(max-width:900px){.find,.cols,.two,.rev{grid-template-columns:1fr}.col,.find>div{border-right:0;border-bottom:1px solid var(--rule)}.rung{grid-template-columns:26px 1fr}.rung span:last-child{grid-column:2}}
@media print{.tools,.rev,.board,.sel2{display:none}.sheet,.ex{box-shadow:none}}
</style></head><body><div class="wrap">
<header class="top"><div class="k">W/P 00 &middot; Audit file</div><h1 id="ti"></h1><p class="sub" id="su"></p><div class="meta" id="me"></div></header>
<section id="find"></section>
<h2>Index of records</h2><p class="lead">Records are grouped by the source they share. Records in one lane are not independent confirmations. Select a record to open its workpaper.</p>
<div class="tools" id="tools"></div><div class="board" id="board"></div>
<h2>Workpaper</h2><div id="sheet"></div>
<h2>Where the figures come apart</h2><p class="lead">Three cross-record exhibits. Every number is recomputed live from the inputs shown, so you can check the arithmetic yourself.</p>
<div id="ex"></div>
<h2>Method and limits</h2><div id="method"></div>
<footer id="foot"></footer></div>
<script>
const D=__DATA__,M=__META__,$=s=>document.querySelector(s),esc=s=>(s||'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const V=[['unverifiable','Unverifiable','The relevant figure cannot be located in the available evidence.'],['unsupported','Source does not support claim','The cited source does not establish the statement being checked.'],['definition','Definition mismatch','Different metric definitions or calculation conventions.'],['period','Period mismatch','Different periods, base dates or statistical vintages.'],['match','Match','Agrees at the stated precision.'],['rounding','Rounding difference','Consistent after reasonable rounding or approximate wording.'],['numerical','Numerical discrepancy','A material difference remains after period, definition and rounding checks.']];
const VN=Object.fromEntries(V.map(v=>[v[0],v[1]]));
const cls=l=>{l=(l||'').toLowerCase();return/unverif/.test(l)?'unverifiable':/not support|unsupported/.test(l)?'unsupported':/definition/.test(l)?'definition':/period|vintage/.test(l)?'period':/round/.test(l)?'rounding':/numerical|true mismatch/.test(l)?'numerical':'match'};
const grp=r=>{if(r.independence_group)return r.independence_group;const m=(r.metric||'').toLowerCase();return/inflation|cpi/.test(m)?'CPI':/gdp/.test(m)?'GDP':/unemploy/.test(m)?'Labour':/exchange|naira/.test(m)?'Exchange rate':/reserve/.test(m)?'Reserves':/oil/.test(m)?'Oil':/faac/.test(m)?'FAAC':'Other'};
D.forEach(r=>{r.c=cls(r.label);r.g=grp(r);r.q=r.c==='unverifiable'?'C':/provisional|corroborat|secondary|reproduc/i.test([r.status,r.label,r.evidence_type].join(' '))?'B':'A';r.prov=r.q==='B'&&r.c==='match'});
const GR={A:'Primary file opened',B:'Official statement via a secondary copy',C:'Not locatable in a primary source'};
const cnt=(a,f)=>a.reduce((o,r)=>(o[f(r)]=(o[f(r)]||0)+1,o),{});
let S={q:'',c:null,s:null,id:null},R={};try{R=JSON.parse(localStorage.getItem('wp-rev')||'{}')}catch(e){}
const save=()=>{try{localStorage.setItem('wp-rev',JSON.stringify(R))}catch(e){}};
const col=c=>'var(--'+c+')';
$('#ti').textContent=M.title;$('#su').textContent=M.sub;document.title=M.title+' | Audit file';
$('#me').innerHTML=[['Prepared by',M.author],['Event',M.event],['Records',D.length+' in '+new Set(D.map(r=>r.g)).size+' source groups'],['Built',M.built]].map(x=>`<div class="k">${x[0]}<b>${esc(x[1])}</b></div>`).join('');
function findings(){const g=cnt(D,r=>r.q),sm=cnt(D,r=>r.sample||'unlabelled'),v=cnt(D,r=>r.c);
const pills=o=>V.filter(x=>o[x[0]]).map(x=>`<span class="pill" style="color:${col(x[0])}"><i class="dot"></i>${x[1]} ${o[x[0]]}</span>`).join('');
const bySample=Object.keys(sm).map(k=>{const sub=D.filter(r=>(r.sample||'unlabelled')===k);return `<p><b>${esc(k)}</b> (${sub.length}) ${pills(cnt(sub,r=>r.c))}</p>`}).join('');
$('#find').innerHTML=`<div class="find"><div><div class="k">Records</div><div class="big">${D.length}</div><p>across ${new Set(D.map(r=>r.g)).size} source groups. Natural and stress samples are never pooled.</p></div>
<div><div class="k">Evidence grade</div><p style="margin-top:12px;color:var(--ink)"><b>A</b> ${g.A||0} &middot; ${GR.A}<br><b>B</b> ${g.B||0} &middot; ${GR.B}<br><b>C</b> ${g.C||0} &middot; ${GR.C}</p></div>
<div><div class="k">Verdicts by sample</div>${bySample}</div></div>
<div class="warn">These counts describe this dataset only. They are not estimates of how accurate Nigerian public communications are, and no intent is inferred.</div>`}
function tools(){const cs=V.filter(x=>D.some(r=>r.c===x[0]));
$('#tools').innerHTML=`<input type="search" id="q" placeholder="Search claim, speaker, ID" value="${esc(S.q)}">`+cs.map(x=>`<button class="chip ${S.c===x[0]?'on':''}" data-c="${x[0]}">${x[1]}</button>`).join('')+[...new Set(D.map(r=>r.sample).filter(Boolean))].map(s=>`<button class="chip ${S.s===s?'on':''}" data-s="${esc(s)}">${esc(s)}</button>`).join('')+`<span class="k" id="prog"></span>`;
$('#q').oninput=e=>{S.q=e.target.value;board()};
$('#tools').querySelectorAll('[data-c]').forEach(b=>b.onclick=()=>{S.c=S.c===b.dataset.c?null:b.dataset.c;tools();board()});
$('#tools').querySelectorAll('[data-s]').forEach(b=>b.onclick=()=>{S.s=S.s===b.dataset.s?null:b.dataset.s;tools();board()});prog()}
const done=id=>R[id]&&R[id].k&&R[id].k.filter(Boolean).length===4;
function prog(){const n=D.filter(r=>done(r.id)).length;$('#prog').textContent='Reviewed '+n+' / '+D.length}
const hit=r=>(!S.c||r.c===S.c)&&(!S.s||r.sample===S.s)&&(!S.q||[r.id,r.case_name,r.claim_text,r.speaker].join(' ').toLowerCase().includes(S.q.toLowerCase()));
function board(){const gs=cnt(D,r=>r.g),order=Object.keys(gs).sort((a,b)=>gs[b]-gs[a]);
$('#board').innerHTML=order.map(g=>`<div class="lane"><h3>${esc(g)}</h3><small>${gs[g]} record${gs[g]>1?'s':''}, one shared source family</small>`+D.filter(r=>r.g===g).map(r=>`<button class="card ${hit(r)?'':'dim'} ${S.id===r.id?'sel':''}" style="--c:${col(r.c)}" data-id="${esc(r.id)}"><span class="g" title="${GR[r.q]}">${r.q}</span><b>${esc(r.id)}${done(r.id)?' \u2713':''}</b><i>${esc(r.case_name)}</i><span>${VN[r.c]}${r.prov?' (provisional)':''}</span></button>`).join('')+'</div>').join('');
$('#board').querySelectorAll('.card').forEach(b=>b.onclick=()=>open(b.dataset.id))}
const tokens=s=>[...new Set((s||'').match(/\d[\d,]*\.?\d*/g)||[])].map(t=>t.replace(/[.,]$/,''));
const rx=t=>t.map(x=>x.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).sort((a,b)=>b.length-a.length).join('|');
const hl=(txt,t)=>{const e=esc(txt);return t.length?e.replace(new RegExp('(?<![\\d.,])('+rx(t)+')(?!\\d)','g'),'<mark>$1</mark>'):e};
function open(id,noHash){const r=D.find(x=>x.id===id);if(!r)return;S.id=id;if(!noHash)history.replaceState(null,'','#'+id);board();const T=tokens(r.claimed_value),found=T.length&&T.every(t=>new RegExp('(?<![\\d.,])'+rx([t])+'(?!\\d)').test(r.primary_excerpt||''));
const k=V.findIndex(v=>v[0]===r.c),rv=R[id]||{k:[0,0,0,0],n:''};
const lnk=(u,l)=>u&&/^https?:/.test(u)?`<a href="${esc(u)}" target="_blank" rel="noopener">${l} &#8599;</a>`:`<span class="src">${l}: no link recorded</span>`;
$('#sheet').innerHTML=`<div class="sheet" style="--c:${col(r.c)}"><div class="sh"><span class="k">W/P ${esc(r.id)}</span><h3>${esc(r.case_name)}</h3><span class="k">${esc(r.g)} &middot; ${esc(r.sample||'unlabelled')} &middot; grade ${r.q}</span><span class="sp"></span><span class="stamp ${r.prov?'prov':''}">${VN[r.c]}${r.prov?' &middot; provisional':''}</span></div>
<div class="cols"><div class="col"><div class="k">A &middot; The claim</div><blockquote>${hl(r.claim_text,T)}</blockquote><div class="src">${esc(r.speaker)} &middot; ${esc(r.speaker_type)} &middot; ${esc(r.date)}</div><p style="margin-top:8px">${lnk(r.claim_url,'Open claim source')}</p></div>
<div class="col"><div class="k">B &middot; The comparator</div><p class="src" style="margin:8px 0 0">${esc(r.comparator)}</p><blockquote>${r.primary_excerpt?hl(r.primary_excerpt,T):'<span class="src">No excerpt recorded.</span>'}</blockquote><p>${lnk(r.primary_url,'Open comparator')}</p><button class="btn" id="cp">Copy search phrase</button><button class="btn" id="cl">Copy link to record</button></div>
<div class="col"><div class="k">C &middot; Tie-out</div><table class="tie"><tr><td>Claimed</td><td><b>${esc(r.claimed_value)}</b><br><span class="src">${esc(r.claimed_period)}</span></td></tr><tr><td>Comparator value</td><td><b>${esc(r.primary_value||'see excerpt')}</b></td></tr>
<tr><td>Figure text-match</td><td>${!T.length?'<span class="tick t-na">&ndash;</span>No numeric figure':found?'<span class="tick t-ok">&#10003;</span>Found in excerpt':'<span class="tick t-na">&#9675;</span>Not found as text'}<br><span class="src">Exact string test. Derived figures and unit changes will not match.</span></td></tr>
<tr><td>Evidence grade</td><td><span class="tick ${r.q==='A'?'t-ok':r.q==='B'?'t-b':'t-na'}">${r.q}</span>${GR[r.q]}</td></tr></table></div></div>
<div class="ladder"><div class="k" style="margin-bottom:6px">Decision ladder: the first rule that applies decides</div>${V.map((v,i)=>`<div class="rung ${i===k?'stop':i>k?'after':''}"><span>${i+1}</span><span>${v[1]}</span><span>${i===k?'Applies. '+v[2]:i<k?'Not triggered.':'Not reached.'}</span></div>`).join('')}
${r.definition_note||r.notes?`<div class="note"><b>Recorded explanation.</b> ${esc([r.definition_note,r.notes].filter(Boolean).join(' '))}</div>`:''}</div>
<div class="rev"><div class="k" style="grid-column:1/-1">Reviewer sign-off (saved in this browser only)</div><div>${['The claim wording matches the claim source.','The excerpt appears in the comparator.','Claimed and comparator values were compared correctly.','The verdict follows the rule order.'].map((t,i)=>`<label><input type="checkbox" data-i="${i}" ${rv.k[i]?'checked':''}> ${t}</label>`).join('')}</div><div><textarea id="nt" placeholder="Reviewer note">${esc(rv.n)}</textarea><button class="btn" id="ex1">Export all review notes (JSON)</button></div></div></div>`;
$('#cp').onclick=()=>navigator.clipboard&&navigator.clipboard.writeText((r.primary_excerpt||'').split(/\s+/).slice(0,6).join(' '));
$('#cl').onclick=()=>navigator.clipboard&&navigator.clipboard.writeText(location.href.split('#')[0]+'#'+id);
$('#sheet').querySelectorAll('[data-i]').forEach(c=>c.onchange=()=>{R[id]=R[id]||{k:[0,0,0,0],n:''};R[id].k[c.dataset.i]=c.checked?1:0;save();prog();board()});
$('#nt').oninput=e=>{R[id]=R[id]||{k:[0,0,0,0],n:''};R[id].n=e.target.value;save()};
$('#ex1').onclick=()=>{const a=document.createElement('a');a.href=URL.createObjectURL(new Blob([JSON.stringify(R,null,2)],{type:'application/json'}));a.download='review-notes.json';a.click()}}
const FX=[['Nairametrics',1429,1535,7.4,'new','N07'],['The Sun',1435,1535,6.51,'old','N21'],['BusinessDay, year on year',1435.75,1535.82,6.96,'new',''],['BusinessDay, full year',1435.75,1541.36,7.4,'new','']];
const pc=(c,b,d)=>(b-c)/(d==='old'?b:c)*100,dp=n=>(String(n).split('.')[1]||'').length;
const st=(p,c)=>{const e=Math.abs(p-c);return e<=.5*Math.pow(10,-dp(p))+1e-9?['t-ok','reproduced']:e<=.02?['t-b','within 0.02 pp, input rounding']:['t-no','not reproduced']};
let X={c:1435.75,b:1535.82,d:'new',v:'rev'};
function exhibits(){const o=a=>a.map(x=>`<option>${x}</option>`).join(''),res=pc(X.c,X.b,X.d),m=FX.filter(f=>f[1]==X.c&&f[2]==X.b&&f[4]===X.d).map(f=>f[0]);
const nov=X.v==='orig'?14.45:17.33,df=15.15-nov,cp=[['Sep',18.02,20.98],['Oct',16.05,18.97],['Nov',14.45,17.33]],sx=v=>40+(v-13)*60;
const svg=`<svg viewBox="0 0 560 170" width="100%" role="img" aria-label="Original and revised monthly inflation"><g font-family="monospace" font-size="11" fill="currentColor">${cp.map((p,i)=>`<text x="4" y="${38+i*34}">${p[0]}</text><line x1="${sx(p[1])}" x2="${sx(p[2])}" y1="${34+i*34}" y2="${34+i*34}" stroke="currentColor" stroke-width="2" opacity=".5"/><circle cx="${sx(p[1])}" cy="${34+i*34}" r="6" fill="var(--rounding)"/><circle cx="${sx(p[2])}" cy="${34+i*34}" r="6" fill="var(--definition)"/><text x="${sx(p[1])-18}" y="${24+i*34}">${p[1]}</text><text x="${sx(p[2])-8}" y="${24+i*34}">${p[2]}</text>`).join('')}<text x="4" y="142">Dec</text><circle cx="${sx(15.15)}" cy="138" r="6" fill="var(--match)"/><text x="${sx(15.15)-14}" y="128">15.15</text><text x="${sx(15.15)+14}" y="142">revised basis only</text></g></svg>`;
$('#ex').innerHTML=`<div class="ex"><div class="k">Exhibit A &middot; N07, N21</div><h3>One close of the naira, four published percentages</h3><div class="sel2"><label>Closing rate<select id="xc">${o([1429,1435,1435.75])}</select></label><label>2024 base<select id="xb">${o([1535,1535.82,1541.36])}</select></label><label>Divide by<select id="xd"><option value="old">old rate (base)</option><option value="new">new rate (close)</option></select></label><div><div class="k">Result</div><div class="res">${res.toFixed(2)}%</div></div></div>
<p>${m.length?'This recipe is the one behind: <b>'+m.join(', ')+'</b>.':'No outlet in the table used this exact recipe.'}</p>
<table class="t"><tr><th>Outlet</th><th>Close</th><th>Base</th><th>Reported</th><th>Recipe</th><th>Recomputed</th><th>Status</th></tr>${FX.map(f=>{const c=pc(f[1],f[2],f[4]),s=st(f[3],c);return `<tr><td>${f[0]}</td><td>${f[1]}</td><td>${f[2]}</td><td>${f[3]}%</td><td>${f[4]==='old'?'base':'close'} as denominator</td><td>${c.toFixed(2)}%</td><td><span class="tick ${s[0]}"></span>${s[1]}</td></tr>`}).join('')}</table>
<div class="warn">These are media reports of CBN data. The CBN daily series was not retrieved, so the 1,429 versus 1,435.75 gap stays unresolved and N07 and N21 are Unverifiable.</div></div>
<div class="ex"><div class="k">Exhibit B &middot; N01, N03, N19, N33</div><h3>Which November?</h3><div class="two"><div>${svg}<p class="src">Amber: first published. Purple: revised in the December 2025 release. Source: Nairametrics, 16 Jan 2026. NBS tables not opened by the author.</p></div><div><div class="sel2"><button class="chip ${X.v==='orig'?'on':''}" data-v="orig">November as first published</button><button class="chip ${X.v==='rev'?'on':''}" data-v="rev">November as revised</button></div><div class="res">${df>0?'+':'\u2212'}${Math.abs(df).toFixed(2)} pp</div><p>December 15.15% against November ${nov}%: <b>&ldquo;eased from November&rdquo; ${df<0?'holds':'does not hold'}.</b></p><p class="src">${X.v==='orig'?'Mixes bases: December exists only on the revised 2024 = 100 reference.':'Like for like: both months use the revised reference.'}</p></div></div></div>
<div class="ex"><div class="k">Exhibit C &middot; N17</div><h3>Two CBN series, two end-2025 reserves</h3><div class="two">${[['CBN statement, via Nairametrics, 2 Mar 2026','40.19','45.71','bar'],['CBN website daily data, via BusinessDay, 31 Dec 2025','40.88','45.48','bar b2']].map(s=>`<div><div class="k">${s[0]}</div><p class="src">Gross reserves, US$bn: 2024 ${s[1]}, 2025 ${s[2]}</p><div class="${s[3]}" style="width:${s[1]*2}%"></div><div class="${s[3]}" style="width:${s[2]*2}%"></div><b>Change ${(s[2]-s[1]).toFixed(2)}bn</b></div>`).join('')}</div><p class="src" style="margin-top:10px">Different observations and dates. Described separately, not treated as a contradiction.</p></div>`;
$('#xc').value=X.c;$('#xb').value=X.b;$('#xd').value=X.d;
['xc','xb'].forEach(i=>$('#'+i).onchange=e=>{X[i==='xc'?'c':'b']=+e.target.value;exhibits()});$('#xd').onchange=e=>{X.d=e.target.value;exhibits()};
$('#ex').querySelectorAll('[data-v]').forEach(b=>b.onclick=()=>{X.v=b.dataset.v;exhibits()})}
$('#method').innerHTML=`<p class="lead">Each record gets the first rule that applies, in this order.</p>${V.map((v,i)=>`<div class="rung" style="--c:${col(v[0])}"><span>${i+1}</span><span style="color:${col(v[0])};font-weight:700">${v[1]}</span><span>${v[2]}</span></div>`).join('')}
<p class="lead" style="margin-top:18px">Evidence grades: <b>A</b> ${GR.A}. <b>B</b> ${GR.B}; a Match at this grade is provisional. <b>C</b> ${GR.C}.</p>
<ul class="lim"><li>A small, selected pilot. The stress sample is chosen for difficulty and is reported separately.</li><li>Records in one source group share a release, statement or series, so row counts overstate independent evidence.</li><li>Single-annotator review. No agreement score is reported.</li><li>No model evaluation. This is a dataset and a procedure, not a measure of AI accuracy.</li><li>Labels describe how a statement relates to a comparator. They say nothing about a speaker&rsquo;s honesty or intent. Do not rank people or outlets with this data.</li></ul>`;
$('#foot').textContent=M.author+'. Generated by build_all.py on '+M.built+' from the records shown above. Sign-off marks live in this browser only.';
findings();tools();board();exhibits();
const go=()=>{const h=decodeURIComponent(location.hash.slice(1));open(D.some(r=>r.id===h)?h:(D[0]||{}).id,1)};go();addEventListener('hashchange',go);
addEventListener('keydown',e=>{if(/INPUT|TEXTAREA|SELECT/.test(e.target.tagName))return;const v=D.filter(hit),i=v.findIndex(r=>r.id===S.id);if(e.key==='j'&&v[i+1])open(v[i+1].id);if(e.key==='k'&&v[i-1])open(v[i-1].id)});
</script></body></html>'''

html = TEMPLATE.replace("__DATA__", js(rows)).replace("__META__", js(META))
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
print(f"Wrote {OUT} with {len(rows)} records from {SRC} ({len(html)//1024} KB)")

# ---- open the page automatically ----
# python build_all.py            -> builds, then opens index.html in your browser
# python build_all.py --serve    -> builds, then serves it at http://127.0.0.1:8000 (for live testing)
# python build_all.py --no-open  -> builds only
import os, webbrowser
from pathlib import Path

if "--no-open" not in sys.argv:
    if "--serve" in sys.argv:
        import http.server, socketserver, functools, threading
        folder = str(Path(OUT).resolve().parent)
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=folder)
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("127.0.0.1", 8000), handler) as srv:
            url = "http://127.0.0.1:8000/" + os.path.basename(OUT)
            print("Serving " + url + "  (press Ctrl+C to stop)")
            threading.Timer(0.8, lambda: webbrowser.open(url)).start()
            try:
                srv.serve_forever()
            except KeyboardInterrupt:
                print("Stopped.")
    else:
        webbrowser.open(Path(OUT).resolve().as_uri())
        print("Opened " + str(Path(OUT).resolve()))
