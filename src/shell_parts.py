# Shared page parts (scene, extra CSS) copied from make_sample.py
SCENE = '''<svg class="scene" viewBox="0 0 800 200" preserveAspectRatio="xMidYMax slice" aria-hidden="true">
<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="var(--sky1)"/><stop offset="1" stop-color="var(--sky2)"/></linearGradient></defs>
<rect width="800" height="200" fill="url(#sky)"/><circle cx="300" cy="92" r="18" fill="var(--sun)"/>
<path d="M0 160 L80 132 L160 146 L250 120 L340 142 L430 126 L520 144 L800 130 V200 H0Z" fill="var(--m1)"/>
<path d="M0 176 L120 160 L260 170 L400 156 L560 168 L800 158 V200 H0Z" fill="var(--m2)"/>
<g><rect x="560" y="44" width="120" height="146" fill="var(--wall)"/><rect x="552" y="36" width="136" height="10" rx="2" fill="var(--roof)"/>
<g fill="var(--sky1)" opacity=".85">''' + "".join(f'<rect x="{572+c*20}" y="{56+r*16}" width="10" height="9" rx="1"/>' for r in range(7) for c in range(5)) + '''</g>
<path d="M590 172 h60 v-6 h-60z" fill="var(--wood)"/><rect x="606" y="172" width="28" height="18" fill="var(--roof)"/>
<rect x="480" y="104" width="70" height="86" fill="var(--wall)" opacity=".8"/><rect x="474" y="98" width="82" height="8" rx="2" fill="var(--roof)"/>
<g fill="var(--sky1)" opacity=".7">''' + "".join(f'<rect x="{490+c*18}" y="{116+r*16}" width="9" height="8" rx="1"/>' for r in range(4) for c in range(3)) + '''</g></g>
<g><path d="M720 200 Q724 160 716 128" stroke="var(--wood)" stroke-width="5" fill="none"/>
<path d="M716 128 q-26 -6 -40 10 M716 128 q-20 -18 -38 -12 M716 128 q22 -16 40 -6 M716 128 q26 2 34 18 M716 128 q2 -20 -6 -30" stroke="var(--pine)" stroke-width="6" fill="none" stroke-linecap="round"/></g>
</svg>'''

EXTRA_CSS = '''
/* sample-only additions: speaker labels, level chip, drills, TOEIC, class toggles */
.lvl{font-size:12px;font-weight:700;color:var(--accent);background:var(--accent-soft);border-radius:999px;padding:1px 9px;align-self:center}
.turn{display:grid;grid-template-columns:auto minmax(0,1fr);column-gap:8px;align-items:baseline}
.turn+.turn{margin-top:6px}
.turn .k,.turn .m{grid-column:2}
.who{font-size:12px;font-weight:700;color:var(--muted);white-space:nowrap}
.turn.s .who,.dlg .line.st .who{color:var(--accent)}
.dlg .line .k .who{margin-right:8px}
.line .k{font-family:var(--display);font-weight:500}
.word>.line.head .k{font-family:var(--display)}
.gl .en{color:var(--ink);font-weight:600}
.drill+.drill{margin-top:14px}
.dpat{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;padding:6px 12px;border-left:4px solid var(--accent);background:var(--accent-soft);border-radius:0 10px 10px 0}
.dpat b{font-family:var(--display);font-size:17px}
.dpat span{color:var(--muted);font-size:14px}
.drill .rows{border:1px solid var(--line);border-radius:10px;margin-top:6px;overflow:hidden}
.drill .line{grid-template-columns:minmax(0,1fr) 38px;padding:8px 12px}
.drill .line>div{grid-column:1;grid-row:1}.drill .line>.spk{grid-column:2;grid-row:1}
.seg .ll{display:inline!important}
.drill .line .k{font-size:16px}
.tq{border:1px solid var(--line);border-radius:12px;padding:10px 14px;display:flex;flex-direction:column;gap:8px}
.tq+.tq{margin-top:10px}
.tqh{display:flex;align-items:center;gap:10px}
.tqh .exn{display:grid;place-items:center;width:22px;height:22px;border-radius:50%;background:var(--accent-soft);color:var(--accent);font-size:12px;font-weight:700}
.tpart{font-size:13px;font-weight:700;color:var(--accent)}
.tqh .spk{margin-left:auto;width:34px;height:34px}
.tshow{order:2;display:inline-flex;align-items:center;gap:5px;font-size:13px;font-weight:500;color:var(--muted);cursor:pointer;white-space:nowrap}
.tshow input{accent-color:var(--accent)}
body:not(.show-lis) .tq.lis .tqq,body:not(.show-lis) .tq.lis .topt .ot{filter:blur(7px);user-select:none}
.topt .ol{font-weight:700}
.tqq{margin:0;font-family:var(--display);font-size:17px}
.tnote{margin:-4px 0 0;font-size:12.5px;color:var(--muted)}
.topts{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:6px}
.topt{text-align:left;border:1px solid var(--line);background:var(--sheet);color:var(--ink);border-radius:10px;padding:8px 12px;font:inherit;font-family:var(--display);font-size:15px;cursor:pointer}
.topt:hover:not(:disabled){border-color:var(--accent)}
.topt.right{border-color:var(--good);background:var(--good-soft)}
.topt.wrong{border-color:var(--bad);background:var(--bad-soft)}
.topt:disabled{cursor:default}
.twhy{margin:0;font-size:14px;color:var(--ink);background:var(--raise);border-radius:8px;padding:6px 10px}
.twhy b{color:var(--good)}
.class-row{display:flex;flex-wrap:wrap;justify-content:center;gap:6px 16px;width:100%;font-size:13px;color:var(--muted)}
.class-row label{display:inline-flex;align-items:center;gap:5px;cursor:pointer;white-space:nowrap}
.class-row input{accent-color:var(--accent)}
.hide-ko #view .m,.hide-ko #view .gm,.hide-ko #view .qa .a{filter:blur(6px);cursor:pointer;user-select:none}
.hide-en #view .k,.hide-en #view .tqq{filter:blur(7px);cursor:pointer;user-select:none}
.hide-st #view .dlg .line.st .k,.hide-st #view .turn.s .k{filter:blur(7px);cursor:pointer;user-select:none}
#view .show{filter:none!important}
.lesson{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:6px;margin:0;padding:0;list-style:none;counter-reset:st}
.lesson li{border:1px solid var(--line);border-radius:10px;padding:6px 10px;font-size:13.5px;line-height:1.45;counter-increment:st}
.lesson li b{display:block;color:var(--accent);font-size:13px}
.lesson li b::before{content:counter(st) ". "}
.groups .group.sep::before,.groups .group:last-child::after{content:"|";position:absolute;top:50%;transform:translate(-50%,-55%);color:var(--muted);opacity:.7;font-weight:400;pointer-events:none;border:0}
.groups .group.sep::before{left:-9px}
.groups .gsep+.group.sep::before{display:none!important}
.groups .gsep{flex:none;width:1.5px;height:1.05em;background:var(--muted);opacity:.55;align-self:center;margin-right:-8.5px;transform:translateY(-1px)}
.groups .group:last-child::after{left:calc(100% + 9px)}
.groups .group:last-child{margin-right:14px}
.band p.intro{font-size:14.5px;line-height:1.6}
.seg .sh{display:none}
@media (max-width:600px){.seg .lg{display:none}.seg .sh{display:inline}}
.sample-note{font-size:12.5px;color:var(--muted);text-align:center;margin:0}
'''

