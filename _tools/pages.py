# -*- coding: utf-8 -*-
"""Sinh các trang tĩnh từ danh sách sản phẩm (3 thứ tiếng):
- /san-pham/<slug>/            trang chi tiết từng sản phẩm (thông số, nút "Nhận báo giá <model>", người tư vấn)
- /san-pham/                   tổng quan danh mục
- /danh-muc/<slug>/            danh sách theo mục con
- /biobase/, /drawell/ (+ /<hãng>/<mục>/)  trang hãng
- /data/products-<lang>.js     dữ liệu sản phẩm cho trang chủ (tải riêng, có cache)
- sitemap.xml, robots.txt, 404.html
Đọc CATS, PRODUCTS từ index.html, en/index.html, zh/index.html (do build.py + i18n.py sinh ra). build.py gọi file này cuối cùng."""
import json, re, shutil, subprocess, sys, unicodedata, html, hashlib
from pathlib import Path
T = Path(__file__).resolve().parent; REPO = T.parent
SITE = "https://www.vanphongtechco.com.vn"
LANGS = {"vi": "", "en": "en/", "zh": "zh/"}
e = lambda s: html.escape(str(s or ""), quote=True)

def extract(path):
    js = r"""
const fs=require('fs');const s=fs.readFileSync(process.argv[1],'utf8');
const grab=(name)=>{const i=s.indexOf('const '+name+' = [');const j=s.indexOf('\n];',i);return eval(s.slice(i+('const '+name+' = ').length,j+2));};
process.stdout.write(JSON.stringify({cats:grab('CATS'),products:grab('PRODUCTS')}));"""
    return json.loads(subprocess.run(["node", "-e", js, str(path)], capture_output=True, text=True, check=True).stdout)

def slugify(s, n=80):
    s = s.replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:n].strip("-")

norm = lambda c: re.sub(r"[^A-Z0-9]", "", (c or "").upper())
toks = lambda c: {norm(x) for x in re.split(r"[/,]|\s+-\s+", c or "") if len(norm(x)) >= 4}

def brand(p):
    s = (p.get("n", "") + " " + p.get("d", "")).upper()
    for b in ("DRAWELL", "BIOBASE", "DAIHAN", "BOXUN", "GONGBEI", "TAILIN", "TRANSCEND", "KINGMAX"):
        if b in s: return b
    return ""

L = {
 "vi": dict(home="Trang chủ", prod="Sản phẩm", code="Model", cat="Danh mục", brand="Hãng", call="Gọi", zalo="Nhắn Zalo",
            catalog="Tải catalog PDF", paper="Bài báo ứng dụng (PDF)", dwg="Bản vẽ (PDF)", video="Video giới thiệu", related="Sản phẩm cùng danh mục",
            intro="Giới thiệu", spec="Thông số kỹ thuật", spec_note="Theo catalogue của hãng. Thông số có thể thay đổi theo model và phiên bản; Vân Phong xác nhận lại khi báo giá.",
            getq="Nhận báo giá", form_h="Yêu cầu báo giá", f_name="Họ tên", f_phone="Số điện thoại", f_need="Thiết bị hoặc nhu cầu cần tư vấn", f_send="Gửi yêu cầu",
            f_note="Yêu cầu được gửi thẳng tới Vân Phong (info@vanphongtechco.com.vn); bản xác nhận gửi về email của Quý khách. Hoặc gửi model, ảnh thiết bị qua Zalo.", f_email="Email", f_ok="Đã gửi yêu cầu {c}. Vân Phong sẽ liên hệ lại trong giờ làm việc.", f_err="Chưa gửi được, đang mở email để Quý khách gửi trực tiếp.", f_bad="Vui lòng nhập họ tên, số điện thoại và email hợp lệ.", qhead="Liên hệ báo giá",
            advisor="Người tư vấn", tram="Ms Ngọc Trâm – phụ trách BIOBASE, Drawell", sales="Phòng Kinh doanh Vân Phong",
            need_h="Để báo giá đúng cấu hình, anh/chị cho biết:",
            needs=["Model hoặc ảnh thiết bị (nếu đã có)", "Ứng dụng, loại mẫu và số lượng mẫu mỗi ngày", "Tiêu chuẩn, phương pháp thử cần đáp ứng", "Địa điểm lắp đặt và thời gian cần thiết bị"],
            svc_h="Giao hàng, lắp đặt, bảo hành", svc="Thời hạn bảo hành, thời gian giao hàng và phạm vi lắp đặt, hướng dẫn sử dụng được ghi rõ trong báo giá theo từng model.",
            all="Tất cả sản phẩm", items="sản phẩm", viewall="Xem tất cả", origin="Xuất xứ: Trung Quốc",
            company="Công ty TNHH Kỹ thuật và Thương mại Vân Phong", addr="Số 34, ngõ 36A, phố Trần Điền, phường Phương Liệt, TP. Hà Nội",
            hot="Hotline", lang="vi", ogl="vi_VN", nf="Không tìm thấy trang", nf2="Trang này không tồn tại hoặc đã được chuyển. Mời anh/chị về trang chủ hoặc xem danh mục sản phẩm."),
 "en": dict(home="Home", prod="Products", code="Model", cat="Category", brand="Brand", call="Call", zalo="Chat on Zalo",
            catalog="Download catalog (PDF)", paper="Application paper (PDF)", dwg="Drawing (PDF)", video="Video", related="Related products",
            intro="Overview", spec="Specifications", spec_note="From the manufacturer catalogue. Specifications may vary by model and version; Van Phong confirms them in the quotation.",
            getq="Get a quote for", form_h="Request a quotation", f_name="Name", f_phone="Phone", f_need="Equipment or requirement", f_send="Send request",
            f_note="Your request goes straight to Van Phong (info@vanphongtechco.com.vn) and a confirmation is emailed to you. You can also send the model or a photo via Zalo.", f_email="Email", f_ok="Request {c} sent. Van Phong will contact you during business hours.", f_err="Could not send; opening your email app instead.", f_bad="Please enter your name, phone number and a valid email.", qhead="Request a quotation",
            advisor="Your contact", tram="Ms Ngoc Tram – BIOBASE and Drawell specialist", sales="Van Phong sales team",
            need_h="For an accurate configuration and quotation, please tell us:",
            needs=["Model or a photo of the equipment (if known)", "Application, sample type and number of samples per day", "Standards or test methods to meet", "Installation site and required delivery date"],
            svc_h="Delivery, installation, warranty", svc="Warranty period, delivery lead time and the scope of installation and training are stated in the quotation for each model.",
            all="All products", items="products", viewall="View all", origin="Origin: China",
            company="Van Phong Technical and Trading Co., Ltd.", addr="No. 34, Lane 36A, Tran Dien Street, Phuong Liet Ward, Hanoi, Vietnam",
            hot="Hotline", lang="en", ogl="en_US", nf="Page not found", nf2="This page does not exist or has moved. Please go to the home page or browse the product catalogue."),
 "zh": dict(home="首页", prod="产品", code="型号", cat="类别", brand="品牌", call="致电", zalo="Zalo 咨询",
            catalog="下载产品目录（PDF）", paper="应用论文（PDF）", dwg="图纸（PDF）", video="产品视频", related="同类产品",
            intro="产品介绍", spec="技术参数", spec_note="参数来自厂家样本，可能因型号和版本而不同，以 Van Phong 报价确认为准。",
            getq="获取报价：", form_h="询价", f_name="姓名", f_phone="电话", f_need="所需设备或需求", f_send="发送询价",
            f_note="询价将直接发送至 Vân Phong（info@vanphongtechco.com.vn），确认邮件将发送到您的邮箱。也可通过 Zalo 发送型号或设备照片。", f_email="邮箱", f_ok="询价 {c} 已提交，Vân Phong 将在工作时间与您联系。", f_err="提交失败，正在打开邮件应用。", f_bad="请填写姓名、电话和有效邮箱。", qhead="询价",
            advisor="联系人", tram="Ngoc Tram 女士 – BIOBASE、Drawell 产品顾问", sales="Van Phong 销售部",
            need_h="为准确配置和报价，请告知：",
            needs=["型号或设备照片（如有）", "用途、样品类型及每日样品数量", "需满足的标准或检测方法", "安装地点及需要到货的时间"],
            svc_h="交货、安装、保修", svc="保修期、交货期以及安装和培训范围将在每个型号的报价中注明。",
            all="全部产品", items="个产品", viewall="查看全部", origin="产地：中国",
            company="Van Phong 技术与贸易有限公司", addr="越南河内市芳烈坊陈巅街 36A 巷 34 号",
            hot="热线", lang="zh-CN", ogl="zh_CN", nf="页面未找到", nf2="该页面不存在或已移动。请返回首页或浏览产品目录。"),
}
PH = {"vi": {"hot": ("08.9999.0683", "0899990683"), "tram": ("0986.818.013", "0986818013")},
      "en": {"hot": ("+84 899 990 683", "+84899990683"), "tram": ("+84 986 818 013", "+84986818013")},
      "zh": {"hot": ("+84 899 990 683", "+84899990683"), "tram": ("+84 986 818 013", "+84986818013")}}
ART_SUF = {"vi": "", "en": "-en", "zh": "-zh"}
BRAND_INFO = {
 "biobase": dict(key="BIOBASE", logo="/logo-doi-tac/biobase.png",
   vi="BIOBASE Group (Tế Nam, Sơn Đông, Trung Quốc) sản xuất thiết bị phòng thí nghiệm và y tế: tủ an toàn sinh học, tủ hút, tủ lạnh âm sâu, nồi hấp, máy ly tâm, máy phân tích lâm sàng. Vân Phong cung cấp, lắp đặt, hướng dẫn sử dụng và bảo hành thiết bị BIOBASE tại Việt Nam.",
   en="BIOBASE Group (Jinan, Shandong, China) manufactures laboratory and medical equipment: biosafety cabinets, fume hoods, ultra-low freezers, autoclaves, centrifuges and clinical analyzers. Van Phong supplies, installs, trains users and provides warranty service for BIOBASE equipment in Vietnam.",
   zh="BIOBASE 集团（中国山东济南）生产实验室与医疗设备：生物安全柜、通风橱、超低温冰箱、高压灭菌器、离心机和临床分析仪等。Van Phong 在越南提供 BIOBASE 设备的供货、安装、操作培训和保修服务。"),
 "drawell": dict(key="DRAWELL", logo="/logo-doi-tac/drawell.png",
   vi="Chongqing Drawell Instrument (Trùng Khánh, Trung Quốc) sản xuất thiết bị phân tích và phòng thí nghiệm: quang phổ, sắc ký, phân tích nguyên tố, XRF, máy cô quay, máy ly tâm, tủ ấm, nồi hấp. Vân Phong là đại lý phân phối chính hãng Drawell tại Việt Nam.",
   en="Chongqing Drawell Instrument (Chongqing, China) manufactures analytical and laboratory instruments: spectroscopy, chromatography, elemental analysis, XRF, rotary evaporators, centrifuges, incubators and autoclaves. Van Phong is an authorized Drawell distributor in Vietnam.",
   zh="重庆德瑞沃仪器（中国重庆）生产分析与实验室仪器：光谱、色谱、元素分析、XRF、旋转蒸发仪、离心机、培养箱、灭菌器等。Van Phong 是 Drawell 在越南的官方授权经销商。"),
}

BRAND_TW = {"TRANSCEND", "KINGMAX"}
ORIG_TW = {"vi": "Thương hiệu Đài Loan", "en": "Taiwanese brand", "zh": "台湾品牌"}
GIA_L = {"vi": ("Giá tham khảo", "đ", "chưa gồm VAT"), "en": ("Reference price", "VND", "excl. VAT"), "zh": ("参考价", "越南盾", "不含增值税")}
def gia_html(p, lang, cls="gia"):
    g = p.get("gia")
    if not g: return ""
    lab, cur, vat = GIA_L[lang]
    num = f"{int(g):,}".replace(",", "." if lang == "vi" else ",")
    tu = ({"vi": "từ ", "en": "from ", "zh": "起 "}[lang] if p.get("tu") else "")
    return f'<p class="{cls}">{lab}: {tu}<b>{num} {cur}</b> <span>({vat})</span></p>'

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
h1.pt{font-size:clamp(24px,3vw,32px);color:var(--navy);margin:8px 0 6px}.lead{color:var(--muted);max-width:820px}
.pd{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.1fr);gap:40px;padding:18px 0 28px;align-items:start}
.pd .ph{border:1px solid var(--line);border-radius:10px;background:#fff;aspect-ratio:1;display:grid;place-items:center;overflow:hidden}
.pd .ph img{width:100%;height:100%;object-fit:contain}
.tag{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;color:var(--blue)}
.pd h1{font-size:clamp(24px,3vw,32px);line-height:1.25;color:var(--navy);margin:6px 0 14px}
.pd dl{display:grid;grid-template-columns:auto 1fr;gap:6px 18px;margin:0 0 16px;font-size:14px}.pd dt{color:var(--muted)}.pd dd{margin:0;font-weight:600}
h2.h{font-size:19px;color:var(--navy);margin:26px 0 10px}.desc{font-size:16px;margin:0 0 12px}.yt{position:relative;padding-top:56.25%;border-radius:10px;overflow:hidden;background:#000}.yt iframe{position:absolute;inset:0;width:100%;height:100%;border:0}.note{color:var(--muted);font-size:13.5px}
.btns{display:flex;flex-wrap:wrap;gap:10px;margin:14px 0}.btn{display:inline-flex;align-items:center;gap:8px;padding:11px 18px;border-radius:6px;font-weight:700;font-size:14px;border:1px solid var(--line);color:var(--navy);background:#fff;cursor:pointer;font-family:inherit}
.btn.cta{background:var(--cta);border-color:var(--cta);color:#fff}.btn.blue{background:var(--blue);border-color:var(--blue);color:#fff}.btn:hover{filter:brightness(1.05)}
.adv{border:1px solid var(--line);border-left:4px solid var(--blue);border-radius:8px;padding:12px 16px;margin:14px 0;background:#F7FAFD;font-size:14px}.adv b{color:var(--navy)}
table.spec{width:100%;border-collapse:collapse;font-size:14px;margin:6px 0 8px}table.spec td{border:1px solid var(--line);padding:7px 10px;vertical-align:top}
table.spec tr:nth-child(odd) td{background:#F7F9FB}table.spec td:first-child{font-weight:600;color:var(--navy);width:32%}
.spec-wrap{overflow-x:auto}
video.pv{width:100%;max-height:640px;background:#000;border-radius:8px;display:block}
.two{display:grid;grid-template-columns:1.2fr 1fr;gap:28px;align-items:start;margin-bottom:34px}
.gia{margin:6px 0 12px;font-size:15px;color:var(--navy)}.gia b{color:#D35400;font-size:19px}.gia span{color:var(--muted);font-size:13px}.cg{margin:4px 0 0;font-size:12.5px;color:var(--muted)}.cg b{color:#D35400}.cg span{display:none}
.qbox{border:1px solid var(--line);border-radius:10px;padding:18px 18px 8px;background:#fff;box-shadow:0 6px 18px rgba(14,47,90,.06)}
.qbox h2{margin:0 0 10px;font-size:19px;color:var(--navy)}.qbox label{display:block;font-size:13px;font-weight:600;color:var(--navy);margin:8px 0 4px}
.qbox input,.qbox textarea{width:100%;font:inherit;font-size:14px;padding:9px 11px;border:1px solid #C6D0DA;border-radius:6px}.qbox textarea{min-height:76px}
ul.chk{margin:4px 0 0;padding-left:18px}ul.chk li{margin:3px 0}
.rel{background:var(--grey);padding:36px 0 44px}.rel h2{color:var(--navy);margin:0 0 18px;font-size:22px}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px}
.cards a{background:#fff;border:1px solid var(--line);border-radius:8px;overflow:hidden;display:flex;flex-direction:column;transition:box-shadow .2s,transform .2s}
.cards a:hover{box-shadow:0 8px 20px rgba(14,47,90,.12);transform:translateY(-2px)}
.cards .t{aspect-ratio:4/3;display:grid;place-items:center;background:#fff;padding:8px}.cards .t img{width:100%;height:100%;object-fit:contain}
.cards b{display:block;padding:10px 12px 4px;font-size:14px;line-height:1.35;color:var(--navy)}.cards small{display:block;padding:0 12px 12px;color:var(--muted);font-size:12.5px}
.tiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin:14px 0 30px}
.tiles a{border:1px solid var(--line);border-radius:8px;padding:12px 14px;display:flex;justify-content:space-between;gap:10px;font-weight:600;color:var(--navy);background:#fff}
.tiles a:hover{border-color:var(--blue);color:var(--blue)}.tiles span{color:var(--muted);font-weight:500}
.brandhead{display:flex;gap:24px;align-items:center;padding:10px 0 8px}.brandhead img{height:54px;width:auto}
section.blk{padding:6px 0 26px}
footer{background:#2B3038;color:#C9CED6;padding:26px 0;font-size:14px}footer b{color:#fff}footer a{color:#fff}
@media (max-width:860px){.pd,.two{grid-template-columns:1fr;gap:20px}header nav .hide{display:none}header .logo img{height:32px}header nav{gap:12px}.langs{white-space:nowrap}}"""

def head(lang, title, desc, path, extra=""):
    t = L[lang]; url = f"{SITE}/{LANGS[lang]}{path}"
    alts = "".join(f'<link rel="alternate" hreflang="{L[k]["lang"]}" href="{SITE}/{LANGS[k]}{path}">' for k in LANGS)
    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)[:300]}">
<link rel="canonical" href="{url}">{alts}
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)[:300]}"><meta property="og:url" content="{url}"><meta property="og:locale" content="{t['ogl']}">{extra}
<link rel="icon" href="/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap">
<style>{CSS}</style>
</head>
<body>
<header><div class="wrap"><a class="logo" href="/{LANGS[lang]}"><img src="/logo.png" alt="Vân Phong" width="600" height="107"></a>
<nav><a class="hide" href="/{LANGS[lang]}">{t['home']}</a><a href="/{LANGS[lang]}san-pham/">{t['prod']}</a><a class="hide" href="/{LANGS[lang]}biobase/">BIOBASE</a><a class="hide" href="/{LANGS[lang]}drawell/">Drawell</a><a class="hide" href="/{LANGS[lang]}tin-tuc/">{ {"vi":"Tin tức","en":"News","zh":"新闻"}[lang] }</a>
<span class="langs">{"".join(f'<a href="/{LANGS[k]}{path}"{" class=on" if k == lang else ""}>{ {"vi":"VI","en":"EN","zh":"中文"}[k] }</a>' for k in LANGS)}</span></nav></div></header>
"""

def foot(lang):
    t = L[lang]; h = PH[lang]
    return f"""<footer><div class="wrap"><b>{t['company']}</b><br>{t['addr']}<br>{t['hot']}: <a href="tel:{h['hot'][1]}">{h['hot'][0]}</a> / <a href="tel:{h['tram'][1]}">{h['tram'][0]}</a> · <a href="mailto:info@vanphongtechco.com.vn">info@vanphongtechco.com.vn</a></div></footer>
<script>document.addEventListener('submit',function(ev){{var f=ev.target;if(!f.matches('form.qf'))return;ev.preventDefault();var g=function(n){{return (f.elements[n]&&f.elements[n].value||'').trim()}};
var d=f.dataset,mail=function(){{var b=g('need')+'\\n\\n'+g('name')+' – '+g('phone')+' – '+g('email')+'\\n'+location.href;location.href='mailto:info@vanphongtechco.com.vn?subject='+encodeURIComponent(d.subject)+'&body='+encodeURIComponent(b);}};
var m=f.querySelector('.qmsg')||f.insertBefore(Object.assign(document.createElement('p'),{{className:'qmsg'}}),f.firstChild),say=function(t,bad){{m.textContent=t;m.style.cssText='padding:9px 11px;border-radius:6px;font-size:14px;margin:0 0 6px;background:'+(bad?'#FFF0F0;color:#A01818':'#E9F7EF;color:#17733D');}};
if(!g('name')||g('phone').replace(/\\D/g,'').length<8||!/^[^\\s@]+@[^\\s@]+\\.[^\\s@]{{2,}}$/.test(g('email'))){{say(d.bad,1);return;}}
if(!window.VQ_API){{mail();return;}}var bt=f.querySelector('button[type=submit]');bt.disabled=true;var tk=window.VQ_tok&&window.VQ_tok();
fetch(window.VQ_API,{{method:'POST',body:JSON.stringify({{action:'submitQuote',token:tk&&tk.t||'',name:g('name'),phone:g('phone'),email:g('email').toLowerCase(),note:g('need'),items:[{{s:d.s,n:d.n,c:d.c,q:1}}],lang:d.lang,page:location.href}})}}).then(function(r){{return r.json()}}).then(function(r){{if(!r.ok)throw r;say(d.ok.replace('{{c}}',r.code));f.elements.need.value='';}}).catch(function(){{say(d.err,1);setTimeout(mail,1200);}}).then(function(){{bt.disabled=false;}});}});</script>
<script src="/assets/bao-gia.js" defer></script>
</body>
</html>
"""

def card(lang, q, slug, cats):
    t = L[lang]; src = img_src(q); c = cats.get(q["c"]); sub = c["subs"][q["s"]] if c else ""
    im = f'<img src="{e(src)}" alt="{e(q["n"])}" loading="lazy">' if src else ""
    return f'<a href="/{LANGS[lang]}san-pham/{slug}/"><span class="t">{im}</span><b>{e(q["n"])}</b><small>{e(q.get("code") or sub)}</small>{gia_html(q, lang, "cg")}</a>'

def quote_box(lang, p, adv, slug="", head_txt=None):
    t = L[lang]; model = p.get("code") or p["n"]
    subj = f'{t["form_h"]}: {model}'
    need = f'{t["form_h"]}: {p["n"]}' + (f' ({p["code"]})' if p.get("code") and p["code"] not in p["n"] else "")
    h = PH[lang][adv]
    return f"""<div class="qbox" id="bao-gia"><h2>{head_txt or (t['getq'] + ' ' + e(model))}</h2>
<form class="qf" data-subject="{e(subj)}" data-s="{e(slug)}" data-n="{e(p['n'])}" data-c="{e(p.get('code') or '')}" data-lang="{lang}" data-ok="{e(t['f_ok'])}" data-err="{e(t['f_err'])}" data-bad="{e(t['f_bad'])}">
<label for="qn">{t['f_name']}</label><input id="qn" name="name" required autocomplete="name">
<label for="qp">{t['f_phone']}</label><input id="qp" name="phone" type="tel" required autocomplete="tel">
<label for="qe">{t['f_email']}</label><input id="qe" name="email" type="email" required autocomplete="email">
<label for="qd">{t['f_need']}</label><textarea id="qd" name="need">{e(need)}</textarea>
<div class="btns"><button class="btn cta" type="submit">{t['f_send']}</button><a class="btn" href="https://zalo.me/{h[1].lstrip('+').replace('84','0',1) if h[1].startswith('+84') else h[1]}" target="_blank" rel="noopener">{t['zalo']} {h[0]}</a></div>
<p class="note">{t['f_note']}</p></form></div>"""

_TTSV = __import__("hashlib").md5((REPO / "assets" / "doc-bai.js").read_bytes()).hexdigest()[:8]
_MP = T / "bb" / "manual.json"
MANUAL = json.loads(_MP.read_text(encoding="utf-8")) if _MP.exists() else {}

def page(lang, p, cat, slug, related, spec, cats):
    t = L[lang]; pre = "/" + LANGS[lang]; sub = cat["subs"][p["s"]] if cat else ""
    src = img_src(p); b = brand(p); adv = "tram" if b in ("BIOBASE", "DRAWELL", "DAIHAN", "BOXUN") or p["c"] in ("tn", "yt") else "hot"
    btns = []
    if p.get("pdf"): btns.append(f'<a class="btn" href="/catalog/{lang}/{e(p["pdf"])}.pdf" target="_blank" rel="noopener">{t["catalog"]}</a>')
    if p.get("art"): btns.append(f'<a class="btn" href="/bai-bao/{e(p["art"])}{ART_SUF[lang]}.pdf" target="_blank" rel="noopener">{t["paper"]}</a>')
    if p.get("dwg"): btns.append(f'<a class="btn" href="{e(p["dwg"])}" target="_blank" rel="noopener">{t["dwg"]}</a>')
    if p.get("vid"): btns.append(f'<a class="btn" href="#video">▶ {t["video"]}</a>')
    h = PH[lang][adv]; model = p.get("code") or ""
    who = t["tram"] if adv == "tram" else t["sales"]
    advbox = f'<div class="adv">{t["advisor"]}: <b>{who}</b><br><a href="tel:{h[1]}"><b>{t["call"]} {h[0]}</b></a> · Zalo {h[0]}</div>'
    spec_html = ""
    vid_html = ""
    if p.get("vid"):
        poster = p["vid"][:-4] + ".jpg"
        vid_html = f'<h2 class="h">{t["video"]}</h2><video id="video" class="pv" src="{e(p["vid"])}" poster="{e(poster)}" controls playsinline preload="none"></video>'
    man = MANUAL.get(p.get("k") or "") or MANUAL.get("code:" + (p.get("code") or ""), {})
    about_html = "".join(f"<li>{e(x[2:])}</li>" if x.startswith("• ") else f"<p>{e(x)}</p>" for x in man.get("about", {}).get(lang, []))
    about_html = re.sub(r"((?:<li>.*?</li>)+)", r'<ul class="chk">\1</ul>', about_html)
    if about_html: about_html = f'<div class="about"><h2 class="h">{t["intro"]}</h2>' + about_html + f'</div><script src="/assets/doc-bai.js?v={_TTSV}" defer></script>'
    if man.get("spec", {}).get(lang): spec = man["spec"][lang]
    if man.get("yt"):
        Y = man["yt"]["id"]; C = e(man["yt"]["cap"][lang])
        vid_html += f'<h2 class="h">{t["video"]}</h2>' + f'<div class="yt"><iframe src="https://www.youtube-nocookie.com/embed/{Y}" title="{C}" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen></iframe></div><p class="note">{C}</p>'
    if spec:
        rows = "".join("<tr>" + "".join(f"<td>{e(c)}</td>" for c in r) + "</tr>" for r in spec)
        spec_html = f'<h2 class="h">{t["spec"]}</h2><div class="spec-wrap"><table class="spec">{rows}</table></div><p class="note">{man.get("note", {}).get(lang) or t["spec_note"]}</p>'
    rel = "".join(card(lang, q, s, cats) for q, s in related)
    ld = {"@context": "https://schema.org", "@type": "Product", "name": p["n"], "description": p.get("d", ""), "sku": model,
          "url": f"{SITE}{pre}san-pham/{slug}/"}
    if b: ld["brand"] = {"@type": "Brand", "name": b.title() if b != "BIOBASE" else b}
    if src: ld["image"] = src if src.startswith("http") else SITE + src
    extra = (f'<meta property="og:type" content="product">' + (f'<meta property="og:image" content="{e(ld["image"])}">' if src else "")
             + f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>')
    title = f'{p["n"]} – Vân Phong'
    return head(lang, title, p.get("d", ""), f"san-pham/{slug}/", extra) + f"""<main class="wrap">
<div class="crumbs"><a href="{pre}">{t['home']}</a> › <a href="{pre}san-pham/">{t['prod']}</a> › <a href="{pre}danh-muc/{catslug(cat, p['s'])}/">{e(sub)}</a></div>
<div class="pd">
<div class="ph">{f'<img src="{e(src)}" alt="{e(p["n"])}">' if src else ''}</div>
<div>
<span class="tag">{e(sub)}</span>
<h1>{e(p['n'])}</h1>
<dl>{f"<dt>{t['code']}</dt><dd>{e(model)}</dd>" if model else ''}{f"<dt>{t['brand']}</dt><dd>{e(b.title() if b != 'BIOBASE' else b)} · {ORIG_TW[lang] if b in BRAND_TW else t['origin']}</dd>" if b and b != 'GONGBEI' else ''}<dt>{t['cat']}</dt><dd>{e(cat['name'] if cat else '')} – {e(sub)}</dd></dl>
<p class="desc">{e(p.get('d'))}</p>{gia_html(p, lang)}
{('<div class="btns">' + ''.join(btns) + '</div>') if btns else ''}
<div class="btns"><a class="btn cta" href="#bao-gia">{t['getq']} {e(model or p['n'][:40])}</a><a class="btn blue" href="tel:{h[1]}">{t['call']} {h[0]}</a></div>
{advbox}
</div></div>
<div class="two">
<div>{about_html}{vid_html}{spec_html}
<h2 class="h">{t['need_h']}</h2><ul class="chk">{''.join(f'<li>{x}</li>' for x in t['needs'])}</ul>
<h2 class="h">{t['svc_h']}</h2><p>{t['svc']}</p></div>
{quote_box(lang, p, adv, slug)}
</div>
</main>
{f'<section class="rel"><div class="wrap"><h2>{t["related"]}</h2><div class="cards">{rel}</div></div></section>' if rel else ''}
""" + foot(lang)

CATSUB = {}
def catslug(cat, s):
    if not cat: return "khac"
    return CATSUB.get((cat["id"], s), f"{cat['id']}-{s}")

def listing(lang, title, lead, path, crumbs, body):
    t = L[lang]; pre = "/" + LANGS[lang]
    cr = " › ".join([f'<a href="{pre}">{t["home"]}</a>'] + crumbs)
    return head(lang, f"{title} – Vân Phong", lead, path) + f"""<main class="wrap">
<div class="crumbs">{cr}</div>
<h1 class="pt">{e(title)}</h1><p class="lead">{e(lead)}</p>
{body}
</main>
""" + foot(lang)

def main():
    data = {k: extract(REPO / (LANGS[k] + "index.html")) for k in LANGS}
    n = len(data["vi"]["products"])
    for k in LANGS:
        if len(data[k]["products"]) != n: sys.exit(f"Số sản phẩm {k} khác tiếng Việt")
    # slugs
    slugs, seen = [], set()
    for p in data["vi"]["products"]:
        base = slugify(p["n"] + ("" if slugify(p.get("code", "")) in slugify(p["n"]) else " " + p.get("code", ""))) or "san-pham"
        s, i = base, 2
        while s in seen: s = f"{base}-{i}"; i += 1
        seen.add(s); slugs.append(s)
    # category slugs (from Vietnamese names)
    for c in data["vi"]["cats"]:
        for si, sn in enumerate(c["subs"]): CATSUB[(c["id"], si)] = slugify(sn, 60)
    # specs: by key and by model code
    specs = {}
    sp = T / "bb" / "specs.json"
    if sp.exists(): specs = json.loads(sp.read_text(encoding="utf-8"))
    by_code = {}
    for key, rows in specs.items():
        pass
    src_codes = {}
    pj = T / "bb" / "products.json"
    if pj.exists():
        for q in json.loads(pj.read_text(encoding="utf-8")):
            k = f"{q.get('src','vn')}:{q['i']}"
            if k in specs:
                for tk in toks(q.get("code")): src_codes.setdefault(tk, k)
    def spec_for(p):
        k = p.get("k")
        if k and k in specs: return specs[k]
        for tk in toks(p.get("code")):
            if tk in src_codes: return specs[src_codes[tk]]
        return None
    urls = []
    for out in ("san-pham", "danh-muc", "biobase", "drawell"):
        for pre in LANGS.values():
            d = REPO / pre / out
            if d.exists(): shutil.rmtree(d)
    for lang, pre in LANGS.items():
        t = L[lang]; P = "/" + pre
        cats = {c["id"]: c for c in data[lang]["cats"]}; prods = data[lang]["products"]
        bysub = {}
        for i, p in enumerate(prods): bysub.setdefault((p["c"], p["s"]), []).append(i)
        for idx, (p, s) in enumerate(zip(prods, slugs)):
            same = bysub[(p["c"], p["s"])]
            pos = same.index(idx); near = [j for j in same[max(0, pos - 4):pos + 5] if j != idx][:8]
            d = REPO / pre / "san-pham" / s; d.mkdir(parents=True, exist_ok=True)
            (d / "index.html").write_text(page(lang, p, cats.get(p["c"]), s, [(prods[j], slugs[j]) for j in near], spec_for(p), cats), encoding="utf-8")
            urls.append(f"{SITE}/{pre}san-pham/{s}/")
        # category pages
        overview = []
        for c in data[lang]["cats"]:
            tiles = []
            for si, sn in enumerate(c["subs"]):
                ids = bysub.get((c["id"], si), [])
                if not ids: continue
                cs = CATSUB[(c["id"], si)]
                tiles.append(f'<a href="{P}danh-muc/{cs}/">{e(sn)} <span>{len(ids)}</span></a>')
                body = '<section class="blk"><div class="cards">' + "".join(card(lang, prods[j], slugs[j], cats) for j in ids) + "</div></section>"
                d = REPO / pre / "danh-muc" / cs; d.mkdir(parents=True, exist_ok=True)
                (d / "index.html").write_text(listing(lang, sn, f"{c['name']} · {len(ids)} {t['items']}", f"danh-muc/{cs}/",
                    [f'<a href="{P}san-pham/">{t["prod"]}</a>', e(c["name"])], body), encoding="utf-8")
                urls.append(f"{SITE}/{pre}danh-muc/{cs}/")
            if tiles: overview.append(f'<h2 class="h">{e(c["name"])}</h2><div class="tiles">{"".join(tiles)}</div>')
        brands = "".join(f'<a href="{P}{b}/"><img src="{BRAND_INFO[b]["logo"]}" alt="{b}" style="height:30px;width:auto"> <span>{sum(1 for p in prods if brand(p)==BRAND_INFO[b]["key"])}</span></a>' for b in BRAND_INFO)
        d = REPO / pre / "san-pham"; d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(listing(lang, t["prod"], f"{len(prods)} {t['items']}", "san-pham/", [e(t["prod"])],
            f'<div class="tiles">{brands}</div>' + "".join(overview)), encoding="utf-8")
        urls.append(f"{SITE}/{pre}san-pham/")
        # brand pages
        for b, info in BRAND_INFO.items():
            ids = [i for i, p in enumerate(prods) if brand(p) == info["key"]]
            groups = {}
            for i in ids: groups.setdefault((prods[i]["c"], prods[i]["s"]), []).append(i)
            tiles = []; secs = []
            for (cid, si), g in sorted(groups.items(), key=lambda x: -len(x[1])):
                sn = cats[cid]["subs"][si]; cs = CATSUB[(cid, si)]
                tiles.append(f'<a href="{P}{b}/{cs}/">{e(sn)} <span>{len(g)}</span></a>')
                body = '<section class="blk"><div class="cards">' + "".join(card(lang, prods[j], slugs[j], cats) for j in g) + "</div></section>"
                dd = REPO / pre / b / cs; dd.mkdir(parents=True, exist_ok=True)
                (dd / "index.html").write_text(listing(lang, f"{info['key'].title() if b=='drawell' else 'BIOBASE'} – {sn}", f"{len(g)} {t['items']} · {t['origin']}", f"{b}/{cs}/",
                    [f'<a href="{P}{b}/">{"Drawell" if b=="drawell" else "BIOBASE"}</a>'], body), encoding="utf-8")
                urls.append(f"{SITE}/{pre}{b}/{cs}/")
                secs.append(f'<h2 class="h">{e(sn)} <span class="note">({len(g)})</span></h2><div class="cards">' + "".join(card(lang, prods[j], slugs[j], cats) for j in g[:8]) + f'</div><p><a href="{P}{b}/{cs}/" style="color:var(--blue);font-weight:600">{t["viewall"]} →</a></p>')
            h = PH[lang]["tram"]
            bv = ('<video class="pv" src="/video/biobase-giai-phap-ptn.mp4" poster="/video/biobase-giai-phap-ptn.jpg" controls playsinline preload="none" style="max-width:420px;margin:6px 0 18px"></video>' if b == "biobase" else "")
            top = (f'<div class="brandhead"><img src="{info["logo"]}" alt="{info["key"]}"></div><p>{e(info[lang])}</p>'
                   f'<div class="adv">{t["advisor"]}: <b>{t["tram"]}</b><br><a href="tel:{h[1]}"><b>{t["call"]} {h[0]}</b></a> · Zalo {h[0]} · info@vanphongtechco.com.vn</div>'
                   f'{bv}<div class="tiles">{"".join(tiles)}</div>')
            name = "Drawell" if b == "drawell" else "BIOBASE"
            dd = REPO / pre / b; dd.mkdir(parents=True, exist_ok=True)
            (dd / "index.html").write_text(listing(lang, name, f"{len(ids)} {t['items']} · {t['origin']}", f"{b}/", [name], top + "".join(secs)), encoding="utf-8")
            urls.append(f"{SITE}/{pre}{b}/")
        # 404
        if lang == "vi":
            (REPO / "404.html").write_text(listing(lang, t["nf"], t["nf2"], "404.html", [], f'<p class="btns"><a class="btn cta" href="/">{t["home"]}</a><a class="btn" href="/san-pham/">{t["prod"]}</a><a class="btn" href="/biobase/">BIOBASE</a><a class="btn" href="/drawell/">Drawell</a></p>'), encoding="utf-8")
        # homepage: slugs, then move product data to /data/products-<lang>.js
        f = REPO / pre / "index.html"; hh = f.read_text(encoding="utf-8")
        i = hh.index("const SLUGS = "); j = hh.index("const PRODUCTS = [", i); k2 = hh.index("\n];", j) + 3
        payload = "window.__S=" + json.dumps(slugs, ensure_ascii=False, separators=(",", ":")) + ";\nwindow.__P=" + json.dumps(prods, ensure_ascii=False, separators=(",", ":")) + ";\n"
        (REPO / "data").mkdir(exist_ok=True)
        (REPO / "data" / f"products-{lang}.js").write_text(payload, encoding="utf-8")
        ver = hashlib.md5(payload.encode()).hexdigest()[:8]
        hh = hh[:i] + "const SLUGS = window.__S, PRODUCTS = window.__P;" + hh[k2:]
        m = hh.rfind("<script>", 0, hh.index("const SLUGS = window.__S"))
        hh = hh[:m] + f'<script src="/data/products-{lang}.js?v={ver}"></script>\n' + hh[m:]
        f.write_text(hh, encoding="utf-8")
    # news pages: /tin-tuc/ and /tin-tuc/<slug>/ (images in /tin-tuc/*.jpg are kept)
    import news as NW
    for lang, pre in LANGS.items():
        base = REPO / pre / "tin-tuc"
        if base.exists():
            for d in base.iterdir():
                if d.is_dir(): shutil.rmtree(d)
        base.mkdir(parents=True, exist_ok=True)
        ex = f"<style>{NW.CSS}</style>"; P = "/" + pre
        (base / "index.html").write_text(listing(lang, NW.H[lang], NW.UI[lang]["lead"], "tin-tuc/", [e(NW.H[lang])], '<section class="blk">' + NW.cards(lang) + "</section>").replace("</head>", ex + "</head>", 1), encoding="utf-8")
        urls.append(f"{SITE}/{pre}tin-tuc/")
        for nw in NW.N:
            s = NW.slug(nw); d = base / s; d.mkdir(parents=True, exist_ok=True)
            img = nw["img"] if nw["img"].startswith("http") else SITE + nw["img"]
            meta = f'<meta property="og:type" content="article"><meta property="og:image" content="{e(img)}">' + ex
            meta += f'<script src="/assets/doc-bai.js?v={_TTSV}" defer></script>'
            others = [m for m in NW.N if m is not nw][:3]
            qp, qs = None, ""
            for _t, _h in nw.get("links", {}).get(lang, []):
                _m = re.search(r"/san-pham/([^/]+)/", _h)
                if _m and _m.group(1) in slugs: qs = _m.group(1); qp = data[lang]["products"][slugs.index(qs)]; break
            tplain = re.sub("<[^>]+>", "", nw["title"][lang]).split(" — ")[0].split(" —— ")[0]
            if qp:
                adv = "tram" if brand(qp) in ("BIOBASE", "DRAWELL", "DAIHAN", "BOXUN") or qp["c"] in ("tn", "yt") else "hot"
                qbox = quote_box(lang, qp, adv, qs)
            else:
                adv = "hot"; qbox = quote_box(lang, {"n": tplain, "code": ""}, adv, "", L[lang]["qhead"])
            hh_ = PH[lang][adv]; who = L[lang]["tram"] if adv == "tram" else L[lang]["sales"]
            slot = f'<div class="vq-slot" data-s="{e(qs)}" data-n="{e(qp["n"])}" data-c="{e(qp.get("code") or "")}"></div>' if qp else ""
            nq = (f'<div class="art nq"><div class="adv">{L[lang]["advisor"]}: <b>{who}</b><br><a href="tel:{hh_[1]}"><b>{L[lang]["call"]} {hh_[0]}</b></a> · Zalo {hh_[0]} · info@vanphongtechco.com.vn</div>{slot}{qbox}</div>')
            body = (f'<div class="crumbs"><a href="{P}">{L[lang]["home"]}</a> › <a href="{P}tin-tuc/">{NW.H[lang]}</a></div>' + NW.article(nw, lang) + nq
                    + f'<section class="rel" style="background:#F0F2F4"><div class="wrap"><h2>{NW.UI[lang]["other"]}</h2>{NW.cards(lang, others)}<p class="nall"><a class="btn" href="{P}tin-tuc/">{NW.UI[lang]["back"]}</a></p></div></section>')
            html_ = head(lang, f'{re.sub("<[^>]+>", "", nw["title"][lang])} – Vân Phong', NW.summary(nw, lang, 280), f"tin-tuc/{s}/", meta)
            html_ += '<main class="wrap">' + body.replace('<section class="rel"', '</main><section class="rel"', 1) + foot(lang)
            (d / "index.html").write_text(html_, encoding="utf-8")
            urls.append(f"{SITE}/{pre}tin-tuc/{s}/")
    home = [f"{SITE}/{p}" for p in LANGS.values()]
    (REPO / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{u}</loc></url>\n" for u in home + urls) + "</urlset>\n", encoding="utf-8")
    (REPO / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /_tools/\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print(f"pages: {n} x {len(LANGS)} + danh mục + hãng; sitemap {len(home) + len(urls)} URL")

if __name__ == "__main__":
    main()
