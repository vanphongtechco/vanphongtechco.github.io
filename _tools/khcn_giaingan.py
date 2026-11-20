#!/usr/bin/env python3
"""Cập nhật số liệu giải ngân cho khcn/index.html từ file "Theo dõi chi phí" (Hoàng Tố Uyên).
Dùng: python3 khcn_giaingan.py <thư mục chứa 'Đề tài năm 2025 đã rà soát.xlsx', 'Đề tài năm 2026 đã rà soát.xlsx'> <khcn/index.html> [ngày cập nhật file dd/mm/yyyy] [thư mục QĐ nghiệm thu hàng tháng (docx)]
- Chỉ thay khối GN (đã chi, theo tháng, chưa rõ tháng) và câu nguồn; giữ nguyên phần nghiệm thu (ntCuoi, ntKy, daNT, pctNT).
- In ra các điểm rà soát: dòng tổng ≠ cộng các mục, khoản không xác định được tháng, đề tài thiếu sheet.
"""
import openpyxl, re, sys, json, datetime, os
from collections import defaultdict

DE_TAI = {'01NT/26': 500, '02NT/26': 4898.5, '03NT/26': 2280, '05NT/25': 4028, '02NT/25': 2105, '03NT/25': 1965.867, '04NT/25': 3650.654}   # tổng KP (trđ)

def thang(r):
    for c in (r[1], r[2], r[3]):
        if isinstance(c, datetime.datetime): return c.strftime('%Y-%m')
    for c in (r[2], r[1], r[3]):
        s = str(c or '')
        m = re.search(r'(?i)(?:^|\b)(?:t|tháng)\s*(\d{1,2})\s*/+\s*(\d{2,4})', s)
        if m and 1 <= int(m[1]) <= 12:
            y = int(m[2]); y = y + 2000 if y < 100 else y
            return f'{y}-{int(m[1]):02d}'
        m = re.search(r'(?i)quý\s*(\d)\s*/\s*(\d{4})', s)
        if m: return f'{m[2]}-{int(m[1])*3:02d}'
        m = re.search(r'(\d{1,2})/(\d{1,2})/(\d{4})', s)
        if m: return f'{m[3]}-{int(m[2]):02d}'
    return None

def doc(thu_muc):
    kq, ghi_chu = {}, []
    for fn in ('Đề tài năm 2025 đã rà soát.xlsx', 'Đề tài năm 2026 đã rà soát.xlsx'):
        p = os.path.join(thu_muc, fn)
        if not os.path.exists(p): ghi_chu.append('Không thấy file ' + fn); continue
        wb = openpyxl.load_workbook(p, data_only=True)
        for ws in wb.worksheets:
            m = re.match(r'(\d\d)NT(\d\d)', ws.title)
            if not m: continue
            sdk = f'{m[1]}NT/{m[2]}'
            if sdk not in DE_TAI: continue
            rows = list(ws.iter_rows(values_only=True))
            tot = next((i for i, r in enumerate(rows) if i > 12 and str(r[1] or '').strip().upper().startswith(('TỔNG', 'CỘNG')) and isinstance(r[8], (int, float))), None)
            if tot is None: ghi_chu.append(f'{sdk}: không tìm thấy dòng Tổng cộng'); continue
            mo, chua_ro, cong_muc = defaultdict(float), 0.0, 0.0
            for i in range(12, tot):
                r = rows[i]; a = str(r[1] or '').strip()
                if re.match(r'^[IVX]+/', a):
                    if isinstance(r[8], (int, float)): cong_muc += r[8]
                    continue
                v = r[8]
                if not isinstance(v, (int, float)) or not v: continue
                k = thang(r)
                if k: mo[k] += v
                elif r[4] is None: chua_ro += v
            da_chi = rows[tot][8] or 0
            if abs(cong_muc - da_chi) > 1000: ghi_chu.append(f'{sdk}: dòng Tổng cộng {da_chi:,.0f} ≠ cộng các mục I/II/... {cong_muc:,.0f}')
            th = {k: round(x / 1e6, 2) for k, x in sorted(mo.items()) if k >= '2025-01'}
            d = round(da_chi / 1e6, 2)
            cr = round(d - sum(th.values()), 2)
            cuoi = max(mo) if mo else None
            if cr > 0.5 and cuoi:   # khoản không ghi ngày: tạm đưa vào tháng chi cuối cùng của đề tài
                th[cuoi] = round(th.get(cuoi, 0) + cr, 2)
                ghi_chu.append(f'{sdk}: {cr:,.1f} trđ không ghi ngày → tạm đưa vào tháng {cuoi}')
            kq[sdk] = {'daChi': d, 'pctChi': round(d / DE_TAI[sdk] * 100, 1), 'thang': th, 'chuaRo': cr, 'chuaRoVao': cuoi}
    for s in DE_TAI:
        if s not in kq: ghi_chu.append(f'{s}: không có sheet trong file theo dõi chi phí')
    return kq, ghi_chu

def nghiem_thu(qd_dir):
    """Đọc các QĐ nghiệm thu dạng docx (tên YYYY-MM-QD-nghiem-thu*.docx): lũy kế đã NT và tháng NT gần nhất có khối lượng > 0."""
    import docx, glob
    kq = {}
    for f in sorted(glob.glob(os.path.join(qd_dir, '*-QD-nghiem-thu*.docx'))):
        m = re.match(r'(\d{4})-(\d{2})', os.path.basename(f))
        if not m: continue
        ky = f'T{int(m[2])}/{m[1]}'
        for tb in docx.Document(f).tables:
            for r in tb.rows:
                c = list(dict.fromkeys(x.text.strip().replace('\n', ' ') for x in r.cells))
                sdk = next((x for x in c if x in DE_TAI), None)
                if not sdk: continue
                i = c.index(sdk)
                so = lambda x: float(x.replace('.', '').replace(',', '.')) if re.fullmatch(r'[\d.,]+', x or '') else None
                vals = c[i+1:]
                try: tong, da = so(vals[2]), so(vals[3])
                except Exception: continue
                pct = so(vals[5]) if len(vals) > 5 else None
                gt = so(vals[6]) if len(vals) > 6 else None
                if da is None: continue
                d = kq.setdefault(sdk, {})
                d['daNT'] = round((da + (gt or 0)) / 1000, 1)
                d['pctNT'] = round(d['daNT'] / DE_TAI[sdk] * 100)
                if pct and gt:
                    d['ntCuoi'] = ky
                    d['ntKy'] = f"{pct:g}% – {gt/1000:,.1f} trđ".replace(',', 'X').replace('.', ',').replace('X', '.')
    return kq

def cap_nhat(html_path, kq, ngay):
    s = open(html_path, encoding='utf-8').read()
    m = re.search(r'const GN=(\{.*?\});\n', s)
    gn = json.loads(m[1])
    doi = []
    for sdk, v in kq.items():
        cu = gn.setdefault(sdk, {})
        for k in ('daChi', 'daNT', 'ntCuoi', 'ntKy'):
            if k in v and cu.get(k) != v[k]: doi.append(f"{sdk}: {k} {cu.get(k)} → {v[k]}")
        cu.update(v)
    s = s[:m.start(1)] + json.dumps(gn, ensure_ascii=False) + s[m.end(1):]
    s = re.sub(r'(Theo dõi chi phí, cập nhật )[^)]*(\))', r'\g<1>' + ngay + r'\2', s, count=1)
    open(html_path, 'w', encoding='utf-8').write(s)
    return doi

if __name__ == '__main__':
    kq, ghi_chu = doc(sys.argv[1])
    if len(sys.argv) > 4:
        for sdk, v in nghiem_thu(sys.argv[4]).items(): kq.setdefault(sdk, {}).update(v)
    ngay = sys.argv[3] if len(sys.argv) > 3 else datetime.date.today().strftime('%d/%m/%Y')
    doi = cap_nhat(sys.argv[2], kq, ngay)
    print('THAY ĐỔI:', *(doi or ['(không đổi)']), sep='\n- ')
    print('RÀ SOÁT:', *(ghi_chu or ['(không có lưu ý)']), sep='\n- ')
