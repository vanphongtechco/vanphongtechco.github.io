# -*- coding: utf-8 -*-
"""Cập nhật toàn bộ web sau khi sửa: python3 _tools/build.py
1) Dựng lại các khối Ban lãnh đạo / Tin tức / Bài báo / Sáng chế trong index.html (tiếng Việt)
2) Sinh /en/index.html và /zh/index.html từ bản tiếng Việt (i18n.py)
Thêm 'catalog' để dựng lại các file catalog PDF (cần: pip install playwright && playwright install chromium)."""
import re, sys, subprocess
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
from pathlib import Path
T = Path(__file__).resolve().parent; REPO = T.parent
sys.path.insert(0, str(T))
import leaders, news, pubs, partners
idx = REPO / "index.html"; h = idx.read_text(encoding="utf-8")
for tag, fn in (("LEADERS", leaders.block), ("NEWS", news.block), ("PUBS", pubs.block), ("PATENT", pubs.patent_block)):
    h, n = re.subn(rf"<!--{tag}-->.*?<!--/{tag}-->", lambda m: f"<!--{tag}-->" + fn("vi") + f"<!--/{tag}-->", h, flags=re.S)
    if n != 1: sys.exit(f"Không tìm thấy khối <!--{tag}--> trong index.html")
h, n = re.subn(r'(<div class="partners">\n).*?(\n  </div>)', lambda m: m.group(1) + partners.block("vi") + m.group(2), h, count=1, flags=re.S)
if n != 1: sys.exit("Không tìm thấy khối đối tác trong index.html")
idx.write_text(h, encoding="utf-8")
r = subprocess.run([sys.executable, str(T / "i18n.py")])
if r.returncode: sys.exit("LỖI: xem dòng MISSING ở trên – chưa có bản dịch cho đoạn tiếng Việt vừa sửa (thêm vào bảng P trong _tools/i18n.py).")
if "catalog" in sys.argv: subprocess.run([sys.executable, str(T / "catalog.py")], check=True)
print("XONG – kiểm tra rồi commit/push.")
