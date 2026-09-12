from pathlib import Path
import re,json,base64

# Migration trigger 2026-09-12 v50.
ROOT=Path(__file__).resolve().parents[1]
master=ROOT/'master.html'
s=master.read_text(encoding='utf-8')
m=re.search(r'const D=(\[.*?\]);function dec',s,re.S)
if not m:
    raise SystemExit('Embedded module payload not found. Refusing to change master.html')
D=json.loads(m.group(1))
if len(D)!=5:
    raise SystemExit(f'Expected 5 modules, found {len(D)}. Refusing to change files.')
mods=['sistem','pemahaman','komsas','novel','pemindahan']
out=ROOT/'modules'; out.mkdir(exist_ok=True)
for name,payload in zip(mods,D):
    html=base64.b64decode(payload).decode('utf-8')
    if '<html' not in html.lower() or '<script' not in html.lower():
        raise SystemExit(f'Invalid {name} payload. Refusing migration.')
    (out/f'{name}.html').write_text(html,encoding='utf-8')

router='''<!doctype html><html lang="ms"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Tingkatan 2 Bahasa Melayu</title><style>*{box-sizing:border-box}body{margin:0;font-family:Arial,sans-serif;background:#f4f6f9;color:#172033}header{background:#111827;color:#fff;padding:14px 18px}main{max-width:1050px;margin:auto;padding:28px}.hero,.card{background:#fff;border:1px solid #e0e5ec;border-radius:18px;padding:22px}.grid{display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-top:14px}.card{text-decoration:none;color:inherit;display:block}.card:hover{transform:translateY(-2px);box-shadow:0 10px 28px #00000010}.tag{font-size:12px;color:#667085;font-weight:700}.card h2{margin:8px 0 0}@media(max-width:700px){.grid{grid-template-columns:1fr}}</style></head><body><header><b>Tingkatan 2 Bahasa Melayu</b></header><main><section class="hero"><h1>Latihan Tingkatan 2</h1><p>KSSM · DSKP · UASA</p></section><section class="grid"><a class="card" href="modules/sistem.html"><span class="tag">MODUL 01</span><h2>Sistem Bahasa</h2></a><a class="card" href="modules/pemahaman.html"><span class="tag">MODUL 02</span><h2>Pemahaman Petikan</h2></a><a class="card" href="modules/komsas.html"><span class="tag">MODUL 03</span><h2>KOMSAS Antologi</h2></a><a class="card" href="modules/novel.html"><span class="tag">MODUL 04</span><h2>Novel Jalan ke Puncak</h2></a><a class="card" href="modules/pemindahan.html"><span class="tag">MODUL 05</span><h2>Pemindahan Maklumat</h2></a></section></main></body></html>'''
master.write_text(router,encoding='utf-8')
print('Migration complete: 5 modules + lightweight master.html')
