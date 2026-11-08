# -*- coding: utf-8 -*-
"""Sản phẩm BIOBASE lấy từ biobase.com.vn (3 thứ tiếng) – dữ liệu ở _tools/bb/products.json.
Mỗi mục: code, img (URL ảnh), c, s, vi/en/zh: {n, d}. build.py chèn vào mảng PRODUCTS của index.html giữa /*BB*/ và /*/BB*/."""
import json
from pathlib import Path
DATA = json.loads((Path(__file__).resolve().parent / "bb" / "products.json").read_text(encoding="utf-8"))
def _q(s): return s.replace("\\", "").replace("'", "’").replace("\n", " ")
def block(lang):
    out = []
    for p in DATA:
        t = p[lang]
        out.append(f"  {{c:'{p['c']}', s:{int(p['s'])}, n:'{_q(t['n'])}', code:'{_q(p.get('code',''))}', img:'{_q(p['img'])}', d:'{_q(t['d'])}', i:'sensor', k:'{p.get('src','vn')}:{p['i']}'"+(f", vid:'{p['vid']}'" if p.get('vid') else "")+"},")
    return "/*BB*/\n" + "\n".join(out) + "\n  /*/BB*/"
