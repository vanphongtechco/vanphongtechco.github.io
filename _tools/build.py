# -*- coding: utf-8 -*-
"""Cập nhật toàn bộ web sau khi sửa: python3 _tools/build.py
1) Dựng lại các khối Ban lãnh đạo / Tin tức / Bài báo / Sáng chế trong _tools/src/index.vi.html (bản gốc tiếng Việt), chép ra index.html
2) Sinh /en/index.html và /zh/index.html từ bản tiếng Việt (i18n.py)
Thêm 'catalog' để dựng lại các file catalog PDF (cần: pip install playwright && playwright install chromium)."""
import re, sys, subprocess
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
from pathlib import Path
T = Path(__file__).resolve().parent; REPO = T.parent
sys.path.insert(0, str(T))
import leaders, news, pubs, partners, biobase
idx = T / "src" / "index.vi.html"; h = idx.read_text(encoding="utf-8")
for tag, fn in (("LEADERS", leaders.block), ("NEWS", news.block), ("PUBS", pubs.block), ("PATENT", pubs.patent_block)):
    h, n = re.subn(rf"<!--{tag}-->.*?<!--/{tag}-->", lambda m: f"<!--{tag}-->" + fn("vi") + f"<!--/{tag}-->", h, flags=re.S)
    if n != 1: sys.exit(f"Không tìm thấy khối <!--{tag}--> trong index.html")
h, n = re.subn(r"/\*BB\*/.*?/\*/BB\*/", lambda m: biobase.block("vi"), h, count=1, flags=re.S)
if n != 1: sys.exit("Không tìm thấy khối /*BB*/ trong index.html")
h, n = re.subn(r'(<div class="partners">\n).*?(\n  </div>)', lambda m: m.group(1) + partners.block("vi") + m.group(2), h, count=1, flags=re.S)
if n != 1: sys.exit("Không tìm thấy khối đối tác trong index.html")
idx.write_text(h, encoding="utf-8")
(REPO / "index.html").write_text(h, encoding="utf-8")
r = subprocess.run([sys.executable, str(T / "i18n.py")])
if r.returncode: sys.exit("LỖI: xem dòng MISSING ở trên – chưa có bản dịch cho đoạn tiếng Việt vừa sửa (thêm vào bảng P trong _tools/i18n.py).")
r = subprocess.run([sys.executable, str(T / "pages.py")])
if r.returncode: sys.exit("LỖI khi sinh trang sản phẩm")
# cache-busting cho assets/bao-gia.js trên mọi trang
import hashlib
_v = hashlib.md5((REPO / "assets" / "bao-gia.js").read_bytes()).hexdigest()[:8]
_v2 = hashlib.md5((REPO / "assets" / "doc-bai.js").read_bytes()).hexdigest()[:8]
for _f in REPO.rglob("*.html"):
    if ".git" in _f.parts or "_tools" in _f.parts: continue
    _t = _f.read_text(encoding="utf-8")
    _n = re.sub(r'/assets/bao-gia\.js(\?v=[0-9a-f]+)?"', f'/assets/bao-gia.js?v={_v}"', _t)
    _n = re.sub(r'/assets/doc-bai\.js(\?v=[0-9a-f]+)?"', f'/assets/doc-bai.js?v={_v2}"', _n)
    if _n != _t: _f.write_text(_n, encoding="utf-8")
if "catalog" in sys.argv: subprocess.run([sys.executable, str(T / "catalog.py")], check=True)
print("XONG – kiểm tra rồi commit/push.")
