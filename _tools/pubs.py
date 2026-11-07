# -*- coding: utf-8 -*-
# Publications: copy originals (IEMM-redacted), render full translations to PDF, and build the website section per language.
import json, re, shutil, html, asyncio, unicodedata
from pathlib import Path
e = html.escape
SRC = Path(__file__).resolve().parent / 'papers'; REPO = Path(__file__).resolve().parent.parent; OUT = REPO / 'bai-bao'
META = json.load(open(SRC / 'meta.json', encoding='utf-8'))

def slug(m):
    t = unicodedata.normalize('NFKD', m['title_en']).encode('ascii', 'ignore').decode().lower()
    t = re.sub(r'[^a-z0-9]+', '-', t).strip('-')
    return f"{m['year']}-" + '-'.join(t.split('-')[:7])
for m in META: m['slug'] = slug(m)

T = {
 'vi': dict(h='Bài báo khoa học', sub='Các công trình công bố của TS. Lê Thanh Bình và cộng sự trên tạp chí và hội nghị khoa học quốc tế.',
            j='Bài đăng tạp chí', c='Báo cáo hội nghị', abs='Tóm tắt', orig='Bài gốc (PDF)', tr='Bản dịch tiếng Việt (PDF)', en_off='Bản tiếng Anh của tạp chí (PDF)',
            banner='BẢN DỊCH THAM KHẢO do Công ty TNHH Kỹ thuật và Thương mại Vân Phong thực hiện. Bản gốc đã công bố là văn bản chính thức; hình vẽ xem trong bản gốc.',
            ln={'ru': 'tiếng Nga', 'en': 'tiếng Anh', 'vi': 'tiếng Việt'}, font='Inter'),
 'en': dict(h='Scientific publications', sub='Papers published by Dr. Le Thanh Binh and co-authors in international journals and conference proceedings.',
            j='Journal articles', c='Conference papers', abs='Abstract', orig='Original paper (PDF)', tr='English translation (PDF)', en_off='Official English version (PDF)',
            banner='REFERENCE TRANSLATION prepared by Van Phong Technical and Trading Co., Ltd. The published original is the authoritative text; see it for figures.',
            ln={'ru': 'Russian', 'en': 'English', 'vi': 'Vietnamese'}, font='Inter'),
 'zh': dict(h='科技论文', sub='黎清平博士及合作者在国际期刊和学术会议上发表的论文。',
            j='期刊论文', c='会议论文', abs='摘要', orig='原文（PDF）', tr='中文译本（PDF）', en_off='期刊官方英文版（PDF）',
            banner='参考译文，由 Van Phong 技术与贸易有限公司翻译。以已发表的原文为准；图表请参阅原文。',
            ln={'ru': '俄文', 'en': '英文', 'vi': '越南文'}, font='Noto Sans CJK SC'),
}

PAGES = {'1Pku66_Cc1dVpfXkKgOYoa-WdHbh-RQYW': [0, 6, 7, 8, 9]}   # proceedings cover + the paper only
SRCFILE = {'11cIRph9x4IdzdT6CkxoyN6vHKmVXk5aI': SRC / 'out' / 'vi_full.pdf'}  # cover + pp. 12-14 + p. 18 (continuation)
def copy_originals():
    from pypdf import PdfReader, PdfWriter
    OUT.mkdir(exist_ok=True)
    for m in META:
        red = SRC / 'out' / f"{m['id']}.pdf"
        src = SRCFILE.get(m['id']) or (red if red.exists() else SRC / f"{m['id']}.pdf")
        dst = OUT / f"{m['slug']}.pdf"
        if not src.exists(): continue  # bản gốc đã có sẵn trong /bai-bao
        if m['id'] in PAGES:
            r = PdfReader(str(src)); w = PdfWriter()
            for i in PAGES[m['id']]: w.add_page(r.pages[i])
            w.write(str(dst))
        else:
            shutil.copy(src, dst)
        if m.get('alt_en_pdf'): shutil.copy(SRC / f"{m['alt_en_pdf']}.pdf", OUT / f"{m['slug']}-en-official.pdf")

CSS = """@page{size:A4;margin:16mm 17mm 18mm}
body{font-family:"%s","Inter","Noto Sans CJK SC",Arial,sans-serif;font-size:10.2pt;line-height:1.5;color:#1d2733}
.top{display:flex;justify-content:space-between;align-items:center;border-bottom:1.6pt solid #1580BF;padding-bottom:3mm;margin-bottom:4mm}
.top img{height:10mm}.top span{font-size:8pt;color:#555}
.ban{border:1pt solid #F07C1B;background:#FFF4EA;color:#9A4A06;padding:2.5mm 3.5mm;font-size:8.4pt;margin-bottom:5mm}
h1{font-size:15pt;line-height:1.3;color:#0E2A47;margin:0 0 2mm}h2{font-size:11.5pt;color:#1580BF;margin:5mm 0 2mm}h3{font-size:10.5pt;margin:4mm 0 1.5mm}
.authors{font-weight:600;margin:0 0 1mm}.src{color:#555;font-size:9pt;margin:0 0 3mm}.kw{font-style:italic}
p{margin:0 0 2mm;text-align:justify}.formula{text-align:center;margin:2.5mm 0;font-family:"Cambria Math","Times New Roman",serif;font-style:italic}
.fig{border:.5pt dashed #9aa9b8;background:#F5F8FB;padding:2mm 3mm;margin:3mm 0;font-size:9pt;color:#405060}
table{border-collapse:collapse;width:100%%;margin:3mm 0;font-size:8.8pt}th,td{border:.5pt solid #b9c4cf;padding:1mm 1.6mm;vertical-align:top}th{background:#EEF3F8}
li{margin:.6mm 0}
"""

async def render_translations():
    from playwright.async_api import async_playwright
    done = []
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        items = list(META) + ([{'id': 'patent', 'slug': 'patent-ru-167383'}] if (SRC / 'patent.json').exists() else [])
        for m in items:
            for lg in ('vi', 'en', 'zh'):
                frag = SRC / 'tr' / f"{m['id']}.{lg}.html"
                if not frag.exists(): continue
                t = T[lg]
                doc = f"""<!doctype html><html lang="{'zh-CN' if lg=='zh' else lg}"><head><meta charset="utf-8"><style>{CSS % t['font']}</style></head><body>
<div class="top"><img src="file://{REPO}/logo.png"><span>www.vanphongtechco.com.vn</span></div>
<div class="ban">{e(t['banner'])}</div>{frag.read_text(encoding='utf-8')}</body></html>"""
                h = SRC / 'tr' / f"_{m['id']}.{lg}.full.html"; h.write_text(doc, encoding='utf-8')
                pg = await b.new_page(); await pg.goto(h.as_uri())
                await pg.pdf(path=str(OUT / f"{m['slug']}-{lg}.pdf"), format='A4', print_background=True, prefer_css_page_size=True,
                             display_header_footer=True, header_template='<span></span>',
                             footer_template='<div style="font-size:7pt;color:#888;width:100%;text-align:center"><span class="pageNumber"></span> / <span class="totalPages"></span></div>')
                await pg.close(); done.append((m['slug'], lg))
        await b.close()
    return done

def block(lang):
    t = T[lang]
    def item(m):
        title = m[f'title_{lang}']; orig = m['title_orig']
        links = [f'<a href="/bai-bao/{m["slug"]}.pdf" target="_blank" rel="noopener">{e(t["orig"])} · {e(t["ln"][m["lang_orig"]])}</a>']
        if lang == 'en' and m.get('alt_en_pdf'):
            links.append(f'<a href="/bai-bao/{m["slug"]}-en-official.pdf" target="_blank" rel="noopener">{e(t["en_off"])}</a>')
        if (OUT / f"{m['slug']}-{lang}.pdf").exists():
            links.append(f'<a class="tr" href="/bai-bao/{m["slug"]}-{lang}.pdf" target="_blank" rel="noopener">{e(t["tr"])}</a>')
        meta = ' · '.join(x for x in [e(m['venue_en'] if lang != 'vi' or m['lang_orig'] != 'vi' else m['venue_orig']), e(m.get('index', '').replace('ВАК', 'VAK'))] if x)
        doi = f' · DOI: <a href="https://doi.org/{e(m["doi"])}" target="_blank" rel="noopener">{e(m["doi"])}</a>' if m.get('doi') else ''
        ot = f'<p class="ot">{e(orig)}</p>' if orig.strip() != title.strip() else ''
        main = f"/bai-bao/{m['slug']}-{lang}.pdf" if (OUT / f"{m['slug']}-{lang}.pdf").exists() else f"/bai-bao/{m['slug']}.pdf"
        return f"""    <li class="pub"><span class="yr">{m['year']}</span><div>
      <h4><a href="{main}" target="_blank" rel="noopener">{e(title)}</a></h4>{ot}
      <p class="au">{e(m['authors_en'] if lang != 'vi' or m['lang_orig'] != 'vi' else m['authors_orig'])}</p>
      <p class="ve">{meta}{doi}</p>
      <details><summary>{e(t['abs'])}</summary><p>{e(m[f'abstract_{lang}'])}</p></details>
      <p class="dl">{' '.join(links)}</p></div></li>"""
    js = [m for m in META if m['kind'] == 'journal']; cs = [m for m in META if m['kind'] != 'journal']
    out = f"""<section class="grey" id="bai-bao"><div class="wrap">
  <div class="title"><h2>{e(t['h'])}</h2><p>{e(t['sub'])}</p></div>
  <h3 class="pubh">{e(t['j'])} ({len(js)})</h3>
  <ol class="pubs">
{chr(10).join(item(m) for m in js)}
  </ol>
  <h3 class="pubh">{e(t['c'])} ({len(cs)})</h3>
  <ol class="pubs">
{chr(10).join(item(m) for m in cs)}
  </ol>
</div></section>"""
    return out

# ---------- Patent section ----------
PT = {
 'vi': dict(h='Sáng chế', sub='Văn bằng bảo hộ sở hữu trí tuệ của TS. Lê Thanh Bình và cộng sự.', no='Số bằng', app='Đơn', pri='Ngày ưu tiên', pub='Công bố', ipc='IPC',
            inv='Tác giả', hold='Chủ văn bằng', orig='Văn bằng gốc (PDF) · tiếng Nga', tr='Bản dịch tiếng Việt (PDF)', abs='Tóm tắt'),
 'en': dict(h='Patents', sub='Intellectual property titles held by Dr. Le Thanh Binh and co-inventors.', no='Patent No.', app='Application', pri='Priority date', pub='Published', ipc='IPC',
            inv='Inventors', hold='Patent holder', orig='Original patent (PDF) · Russian', tr='English translation (PDF)', abs='Abstract'),
 'zh': dict(h='专利', sub='黎清平博士及合作者获得的知识产权证书。', no='专利号', app='申请', pri='优先权日', pub='公告', ipc='国际专利分类',
            inv='发明人', hold='专利权人', orig='专利原文（PDF）· 俄文', tr='中文译本（PDF）', abs='摘要'),
}
def patent_files():
    pj = SRC / 'patent.json'
    if not pj.exists(): return None
    if (SRC / 'patent.pdf').exists(): shutil.copy(SRC / 'patent.pdf', OUT / 'patent-ru-167383.pdf')
    return json.load(open(pj, encoding='utf-8'))

def patent_block(lang):
    P = json.load(open(SRC / 'patent.json', encoding='utf-8')); t = PT[lang]
    links = [f'<a href="/bai-bao/patent-ru-167383.pdf" target="_blank" rel="noopener">{e(t["orig"])}</a>']
    if (OUT / f'patent-ru-167383-{lang}.pdf').exists():
        links.append(f'<a class="tr" href="/bai-bao/patent-ru-167383-{lang}.pdf" target="_blank" rel="noopener">{e(t["tr"])}</a>')
    title = P[f'title_{lang}']
    return f"""<section id="sang-che"><div class="wrap">
  <div class="title"><h2>{e(t['h'])}</h2><p>{e(t['sub'])}</p></div>
  <ol class="pubs">
    <li class="pub"><span class="yr">{e(P['publication_date'][-4:] if P['publication_date'][-4:].isdigit() else '2017')}</span><div>
      <h4><a href="{'/bai-bao/patent-ru-167383-'+lang+'.pdf' if (OUT / f'patent-ru-167383-{lang}.pdf').exists() else '/bai-bao/patent-ru-167383.pdf'}" target="_blank" rel="noopener">{e(title)}</a></h4><p class="ot">{e(P['title_orig'])}</p>
      <p class="au">{e(P[f'type_{lang}'])} · {e(t['no'])}: <b>{e(P['number'])}</b></p>
      <p class="au">{e(t['inv'])}: {e(P['authors_en'].replace('Le Thanh Binh', 'Lê Thanh Bình') if lang == 'vi' else P['authors_en'])}</p>
      <p class="ve">{e(t['hold'])}: {e(P['holder_en'] if lang != 'vi' else P['holder_en'])} · {e(t['app'])}: {e(P['application'])} · {e(t['pub'])}: {e(P['publication_date'])} · {e(t['ipc'])}: {e(P['ipc'])}</p>
      <details><summary>{e(t['abs'])}</summary><p>{e(P[f'abstract_{lang}'])}</p></details>
      <p class="dl">{' '.join(links)}</p></div></li>
  </ol>
</div></section>"""


if __name__ == '__main__':
    import sys
    copy_originals(); patent_files()
    if 'render' in sys.argv: print(len(asyncio.run(render_translations())), 'translations')
    print([m['slug'] for m in META])

