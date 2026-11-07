# -*- coding: utf-8 -*-
"""Sinh trang riêng cho từng sản phẩm: /san-pham/<slug>/, /en/san-pham/<slug>/, /zh/san-pham/<slug>/.
Đọc mảng CATS, PRODUCTS từ index.html của 3 thứ tiếng (cùng thứ tự), ghi danh sách slug vào /*SLUGS*/ ở cả 3 trang chủ.
build.py gọi file này sau i18n.py."""
import json, re, shutil, subprocess, sys, unicodedata, html
from pathlib import Path
T = Path(__file__).resolve().parent; REPO = T.parent
SITE = "https://www.vanphongtechco.com.vn"
LANGS = {"vi": "", "en": "en/", "zh": "zh/"}

def extract(path):
    js = r"""
const fs=require('fs');const s=fs.readFileSync(process.argv[1],'utf8');
const grab=(name)=>{const i=s.indexOf('const '+name+' = [');const j=s.indexOf('\n];',i);return eval(s.slice(i+('const '+name+' = ').length,j+2));};
process.stdout.write(JSON.stringify({cats:grab('CATS'),products:grab('PRODUCTS')}));"""
    out = subprocess.run(["node", "-e", js, str(path)], capture_output=True, text=True, check=True).stdout
    return json.loads(out)

def slugify(s):
    s = s.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:80].strip("-")

L = {
 "vi": dict(home="Trang chủ", prod="Sản phẩm", code="Mã sản phẩm", cat="Danh mục", quote="Liên hệ báo giá", call="Gọi", zalo="Nhắn Zalo",
            catalog="Tải catalog PDF", paper="Bài báo ứng dụng (PDF)", dwg="Bản vẽ (PDF)", video="Video giới thiệu", related="Sản phẩm cùng danh mục",
            back="← Sản phẩm", intro="Giới thiệu", note="Vân Phong tư vấn lựa chọn cấu hình, báo giá, giao hàng, lắp đặt, hướng dẫn sử dụng và bảo hành tận nơi.",
            company="Công ty TNHH Kỹ thuật và Thương mại Vân Phong", addr="Số 34, ngõ 36A, phố Trần Điền, phường Phương Liệt, TP. Hà Nội",
            hot="Hotline", lang="vi", ogl="vi_VN"),
 "en": dict(home="Home", prod="Products", code="Model", cat="Category", quote="Request a quote", call="Call", zalo="Chat on Zalo",
            catalog="Download catalog (PDF)", paper="Application paper (PDF)", dwg="Drawing (PDF)", video="Video", related="Related products",
            back="← Products", intro="Overview", note="Van Phong advises on configuration and provides quotation, delivery, installation, user training and on-site warranty service.",
            company="Van Phong Technical and Trading Co., Ltd.", addr="No. 34, Lane 36A, Tran Dien Street, Phuong Liet Ward, Hanoi, Vietnam",
            hot="Hotline", lang="en", ogl="en_US"),
 "zh": dict(home="首页", prod="产品", code="型号", cat="类别", quote="询价", call="致电", zalo="Zalo 咨询",
            catalog="下载产品目录（PDF）", paper="应用论文（PDF）", dwg="图纸（PDF）", video="产品视频", related="同类产品",
            back="← 产品", intro="产品介绍", note="Van Phong 提供选型咨询、报价、交货、安装、操作培训及上门保修服务。",
            company="Van Phong 技术与贸易有限公司", addr="越南河内市芳烈坊陈巅街 36A 巷 34 号",
            hot="热线", lang="zh-CN", ogl="zh_CN"),
}
PHONES = {"vi": [("08.9999.0683", "0899990683"), ("0986.818.013", "0986818013")],
          "en": [("+84 899 990 683", "+84899990683"), ("+84 986 818 013", "+84986818013")],
          "zh": [("+84 899 990 683", "+84899990683"), ("+84 986 818 013", "+84986818013")]}
ART_SUF = {"vi": "", "en": "-en", "zh": "-zh"}
e = lambda s: html.escape(str(s or ""), quote=True)

def img_src(p):
    im = p.get("img") or ""
    if not im: return ""
    return im if re.match(r"https?:", im) else f"/anh-san-pham/{im}.jpg"

CSS = """:root{--navy:#0E2F5A;--blue:#1580BF;--cta:#F07C1B;--grey:#F0F2F4;--line:#DCE1E6;--fg:#1F2933;--muted:#5F6B77;--font:"Be Vietnam Pro","Segoe UI",Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:#fff;color:var(--fg);font:15px/1.65 var(--font)}img{max-width:100%;height:auto;display:block}a{color:inherit;text-decoration:none}
.wrap{max-width:1180px;margin:0 auto;padding:0 16px}
header{border-bottom:1px solid var(--line);background:#fff;position:sticky;top:0;z-index:5}
header .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:68px}
header .logo img{height:40px;width:auto}header nav{display:flex;gap:18px;align-items:center;font-weight:600;font-size:14px;color:var(--navy)}
header nav a:hover{color:var(--blue)}.langs a{font-weight:500;color:var(--muted);margin-left:8px}.langs a.on{color:var(--navy);font-weight:700}
.crumbs{font-size:13px;color:var(--muted);padding:16px 0 4px}.crumbs a{color:var(--blue)}
.pd{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:40px;padding:18px 0 40px;align-items:start}
.pd .ph{border:1px solid var(--line);border-radius:10px;background:#fff;aspect-ratio:1;display:grid;place-items:center;overflow:hidden}
.pd .ph img{width:100%;height:100%;object-fit:contain}
.pd .tag{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--blue)}
.pd h1{font-size:clamp(24px,3vw,32px);line-height:1.25;color:var(--navy);margin:6px 0 14px}
.pd dl{display:grid;grid-template-columns:auto 1fr;gap:6px 18px;margin:0 0 18px;font-size:14px}.pd dt{color:var(--muted)}.pd dd{margin:0;font-weight:600}
.pd h2{font-size:17px;color:var(--navy);margin:18px 0 6px}.pd .desc{font-size:16px;margin:0 0 12px}.pd .note{color:var(--muted);font-size:14px}
.btns{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0}.btn{display:inline-flex;align-items:center;gap:8px;padding:11px 18px;border-radius:6px;font-weight:700;font-size:14px;border:1px solid var(--line);color:var(--navy);background:#fff}
.btn.cta{background:var(--cta);border-color:var(--cta);color:#fff}.btn.blue{background:var(--blue);border-color:var(--blue);color:#fff}.btn:hover{filter:brightness(1.05)}
.rel{background:var(--grey);padding:36px 0 44px}.rel h2{color:var(--navy);margin:0 0 18px;font-size:22px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px}
.cards a{background:#fff;border:1px solid var(--line);border-radius:8px;overflow:hidden;display:flex;flex-direction:column;transition:box-shadow .2s,transform .2s}
.cards a:hover{box-shadow:0 8px 20px rgba(14,47,90,.12);transform:translateY(-2px)}
.cards .t{aspect-ratio:4/3;display:grid;place-items:center;background:#fff;padding:8px}.cards .t img{width:100%;height:100%;object-fit:contain}
.cards b{display:block;padding:10px 12px 12px;font-size:14px;line-height:1.35;color:var(--navy)}
footer{background:#2B3038;color:#C9CED6;padding:26px 0;font-size:14px}footer b{color:#fff}footer a{color:#fff}
@media (max-width:820px){.pd{grid-template-columns:1fr;gap:20px}header nav .hide{display:none}header .logo img{height:32px}header nav{gap:12px}.langs{white-space:nowrap}}"""

def page(lang, p, cat, slug, slugs_by_lang, related, products):
    t = L[lang]; pre = "/" + LANGS[lang]; sub = cat["subs"][p["s"]] if cat else ""
    src = img_src(p); url = f"{SITE}{pre}san-pham/{slug}/"
    btns = []
    if p.get("pdf"): btns.append(f'<a class="btn" href="/catalog/{lang}/{e(p["pdf"])}.pdf" target="_blank" rel="noopener">{t["catalog"]}</a>')
    if p.get("art"): btns.append(f'<a class="btn" href="/bai-bao/{e(p["art"])}{ART_SUF[lang]}.pdf" target="_blank" rel="noopener">{t["paper"]}</a>')
    if p.get("dwg"): btns.append(f'<a class="btn" href="{e(p["dwg"])}" target="_blank" rel="noopener">{t["dwg"]}</a>')
    if p.get("vid"): btns.append(f'<a class="btn" href="{e(p["vid"])}" target="_blank" rel="noopener">{t["video"]}</a>')
    phones = PHONES[lang]
    contact = (f'<a class="btn cta" href="{pre}#lien-he">{t["quote"]}</a>'
               + "".join(f'<a class="btn blue" href="tel:{tel}">{t["call"]} {disp}</a>' for disp, tel in phones)
               + f'<a class="btn" href="https://zalo.me/0899990683" target="_blank" rel="noopener">{t["zalo"]}</a>')
    rel = "".join(f'<a href="{pre}san-pham/{s}/"><span class="t">{("<img src=" + chr(34) + e(img_src(q)) + chr(34) + " alt=" + chr(34) + e(q["n"]) + chr(34) + " loading=" + chr(34) + "lazy" + chr(34) + ">") if img_src(q) else ""}</span><b>{e(q["n"])}</b></a>' for q, s in related)
    alts = "".join(f'<link rel="alternate" hreflang="{L[k]["lang"]}" href="{SITE}/{LANGS[k]}san-pham/{slug}/">' for k in LANGS)
    langs = "".join(f'<a href="/{LANGS[k]}san-pham/{slug}/"{" class=on" if k == lang else ""}>{ {"vi":"VI","en":"EN","zh":"中文"}[k] }</a>' for k in LANGS)
    desc_meta = e(p.get("d", ""))[:300]
    ld = {"@context": "https://schema.org", "@type": "Product", "name": p["n"], "description": p.get("d", ""), "sku": p.get("code", ""),
          "brand": {"@type": "Brand", "name": "BIOBASE" if "BIOBASE" in (p["n"] + p.get("d", "")).upper() else "Vân Phong"}, "url": url}
    if src: ld["image"] = src if src.startswith("http") else SITE + src
    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(p['n'])} – Vân Phong</title>
<meta name="description" content="{desc_meta}">
<link rel="canonical" href="{url}">{alts}
<meta property="og:type" content="product"><meta property="og:title" content="{e(p['n'])}"><meta property="og:description" content="{desc_meta}"><meta property="og:url" content="{url}"><meta property="og:locale" content="{t['ogl']}">{f'<meta property="og:image" content="{e(ld["image"])}">' if src else ''}
<link rel="icon" href="/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<header><div class="wrap"><a class="logo" href="{pre}"><img src="/logo.png" alt="Vân Phong" width="600" height="107"></a>
<nav><a class="hide" href="{pre}">{t['home']}</a><a href="{pre}#san-pham">{t['prod']}</a><a class="hide" href="{pre}#lien-he">{t['quote']}</a><span class="langs">{langs}</span></nav></div></header>
<main class="wrap">
<div class="crumbs"><a href="{pre}">{t['home']}</a> › <a href="{pre}#san-pham">{t['prod']}</a> › {e(cat['name'] if cat else '')} › {e(sub)}</div>
<div class="pd">
<div class="ph">{f'<img src="{e(src)}" alt="{e(p["n"])}">' if src else ''}</div>
<div>
<span class="tag">{e(sub)}</span>
<h1>{e(p['n'])}</h1>
<dl>{f"<dt>{t['code']}</dt><dd>{e(p.get('code'))}</dd>" if p.get('code') else ''}<dt>{t['cat']}</dt><dd>{e(cat['name'] if cat else '')} – {e(sub)}</dd></dl>
<h2>{t['intro']}</h2>
<p class="desc">{e(p.get('d'))}</p>
{('<div class="btns">' + ''.join(btns) + '</div>') if btns else ''}
<div class="btns">{contact}</div>
<p class="note">{t['note']}</p>
<p><a href="{pre}#san-pham" style="color:var(--blue);font-weight:600">{t['back']}</a></p>
</div></div>
</main>
{f'<section class="rel"><div class="wrap"><h2>{t["related"]}</h2><div class="cards">{rel}</div></div></section>' if rel else ''}
<footer><div class="wrap"><b>{t['company']}</b><br>{t['addr']}<br>{t['hot']}: {' / '.join(f'<a href="tel:{tel}">{d}</a>' for d, tel in phones)} · <a href="mailto:info@vanphongtechco.com.vn">info@vanphongtechco.com.vn</a></div></footer>
</body>
</html>
"""

def main():
    data = {k: extract(REPO / (LANGS[k] + "index.html")) for k in LANGS}
    n = len(data["vi"]["products"])
    for k in LANGS:
        if len(data[k]["products"]) != n: sys.exit(f"Số sản phẩm {k} khác tiếng Việt")
    slugs, seen = [], set()
    for p in data["vi"]["products"]:
        base = slugify(p["n"] + ("" if slugify(p.get("code", "")) in slugify(p["n"]) else " " + p.get("code", ""))) or "san-pham"
        s, i = base, 2
        while s in seen: s = f"{base}-{i}"; i += 1
        seen.add(s); slugs.append(s)
    for k, pre in LANGS.items():
        out = REPO / pre / "san-pham"
        if out.exists(): shutil.rmtree(out)
        cats = {c["id"]: c for c in data[k]["cats"]}; prods = data[k]["products"]
        for idx, (p, s) in enumerate(zip(prods, slugs)):
            same = [(q, slugs[j]) for j, q in enumerate(prods) if j != idx and q["c"] == p["c"] and q["s"] == p["s"]]
            near = [x for x in same if abs(prods.index(x[0]) - idx) < 40][:8] or same[:8]
            d = out / s; d.mkdir(parents=True, exist_ok=True)
            (d / "index.html").write_text(page(k, p, cats.get(p["c"]), s, None, near, prods), encoding="utf-8")
        f = REPO / pre / "index.html"; h = f.read_text(encoding="utf-8")
        h, c = re.subn(r"/\*SLUGS\*/.*?/\*/SLUGS\*/", "/*SLUGS*/" + json.dumps(slugs) + "/*/SLUGS*/", h, count=1, flags=re.S)
        if c != 1: sys.exit(f"Không thấy /*SLUGS*/ trong {f}")
        f.write_text(h, encoding="utf-8")
    # sitemap
    urls = [f"{SITE}/{LANGS[k]}" for k in LANGS] + [f"{SITE}/{LANGS[k]}san-pham/{s}/" for k in LANGS for s in slugs]
    (REPO / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    print(f"pages: {n} x {len(LANGS)}")

if __name__ == "__main__":
    main()
