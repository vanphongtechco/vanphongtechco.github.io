# -*- coding: utf-8 -*-
# Build /en/ and /zh/ pages from the Vietnamese index.html by exact string replacement.
import re, sys
try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass
from pathlib import Path
REPO = Path(__file__).resolve().parent.parent
VI = (REPO / "_tools" / "src" / "index.vi.html").read_text(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent)); from partners import block as _pb
from leaders import block as _lb
from pubs import block as _ub, patent_block as _pt
from news import block as _nb
from biobase import block as _bb

ADDR_EN = "No. 34, Lane 36A, Tran Dien Street, Phuong Liet Ward, Hanoi"
ADDR_ZH = "河内市方烈坊陈田街36A巷34号"

# (vi, en, zh) — exact substrings of the Vietnamese page
P = [
('<label for="fq">Tìm thiết bị</label>', '<label for="fq">Find equipment</label>', '<label for="fq">查找设备</label>'),
('placeholder="Nhập tên máy hoặc model, ví dụ: tủ an toàn sinh học, BKC-TL5C, OS20-Pro…"', 'placeholder="Equipment name or model, e.g. biosafety cabinet, BKC-TL5C, OS20-Pro…"', 'placeholder="输入设备名称或型号，例如：生物安全柜、BKC-TL5C、OS20-Pro…"'),
('<button class="btn cta" type="submit">Tìm</button>', '<button class="btn cta" type="submit">Search</button>', '<button class="btn cta" type="submit">搜索</button>'),
('<a href="/biobase/"><img', '<a href="/en/biobase/"><img', '<a href="/zh/biobase/"><img'),
('<a href="/drawell/"><img', '<a href="/en/drawell/"><img', '<a href="/zh/drawell/"><img'),
('<a class="fall" href="/san-pham/">Tất cả danh mục →</a>', '<a class="fall" href="/en/san-pham/">All categories →</a>', '<a class="fall" href="/zh/san-pham/">全部类别 →</a>'),
('__BB__', '', ''),
# head
('<html lang="vi">', '<html lang="en">', '<html lang="zh-CN">'),
('<title>Vân Phong – Thiết bị phòng thí nghiệm BIOBASE, Drawell chính hãng tại Hà Nội</title>', '<title>Van Phong – BIOBASE and Drawell laboratory equipment distributor in Vietnam</title>', '<title>Van Phong – 越南 BIOBASE、Drawell 实验室设备经销商</title>'),
('content="Vân Phong cung cấp thiết bị phòng thí nghiệm, y tế BIOBASE, Drawell chính hãng: tủ an toàn sinh học, máy ly tâm, tủ sấy, nồi hấp, máy quang phổ… Tư vấn chọn cấu hình, lắp đặt, bảo hành. Hotline 08.9999.0683 / 0986.818.013."', 'content="Van Phong supplies BIOBASE and Drawell laboratory and medical equipment in Vietnam: biosafety cabinets, centrifuges, ovens, autoclaves, spectrophotometers. Configuration advice, installation and warranty. Hotline +84 899 990 683 / +84 986 818 013."', 'content="Van Phong 在越南供应 BIOBASE、Drawell 实验室与医疗设备：生物安全柜、离心机、干燥箱、灭菌器、分光光度计等，提供选型、安装与保修服务。热线 +84 899 990 683 / +84 986 818 013。"'),
# language switcher
('<nav class="langs" aria-label="Ngôn ngữ"><a href="/" lang="vi" class="on">Tiếng Việt</a><a href="/en/" lang="en">English</a><a href="/zh/" lang="zh-CN">中文</a></nav>',
 '<nav class="langs" aria-label="Language"><a href="/" lang="vi">Tiếng Việt</a><a href="/en/" lang="en" class="on">English</a><a href="/zh/" lang="zh-CN">中文</a></nav>',
 '<nav class="langs" aria-label="语言"><a href="/" lang="vi">Tiếng Việt</a><a href="/en/" lang="en">English</a><a href="/zh/" lang="zh-CN" class="on">中文</a></nav>'),
# top strip / addresses
('Số 34, ngõ 36A, phố Trần Điền, phường Phương Liệt, TP. Hà Nội', ADDR_EN + ", Vietnam", "越南" + ADDR_ZH),
('Hotline: 08.9999.0683</span>', 'Hotline: +84 899 990 683</span>', '热线：+84 899 990 683</span>'),
('<a href="tel:0986818013" class="tel2"><span>0986.818.013</span>', '<a href="tel:+84986818013" class="tel2"><span>+84 986 818 013</span>', '<a href="tel:+84986818013" class="tel2"><span>+84 986 818 013</span>'),
# header
('aria-label="Vân Phong – trang chủ"', 'aria-label="Van Phong – home"', 'aria-label="Van Phong – 首页"'),
('<small>Công ty TNHH<br>Kỹ thuật &amp; Thương mại</small>', '<small>Technical &amp;<br>Trading Co., Ltd.</small>', '<small>技术与贸易<br>有限公司</small>'),
('aria-controls="mainNav">Menu</button>', 'aria-controls="mainNav">Menu</button>', 'aria-controls="mainNav">菜单</button>'),
('<a href="#top" class="on">Trang chủ</a>', '<a href="#top" class="on">Home</a>', '<a href="#top" class="on">首页</a>'),
('<a href="#gioi-thieu">Về Vân Phong</a><a href="#ban-lanh-dao">Ban lãnh đạo</a><a href="#chung-nhan">Chứng nhận</a>', '<a href="#gioi-thieu">About Van Phong</a><a href="#ban-lanh-dao">Leadership</a><a href="#chung-nhan">Certificates</a>', '<a href="#gioi-thieu">公司简介</a><a href="#ban-lanh-dao">管理团队</a><a href="#chung-nhan">证书</a>'),
('>Tin tức <span class="caret">', '>News <span class="caret">', '>新闻 <span class="caret">'),
('<a href="#tin-tuc">Tin tức</a><a href="#bai-bao">Bài báo khoa học</a><a href="#sang-che">Sáng chế</a>', '<a href="#tin-tuc">News</a><a href="#bai-bao">Publications</a><a href="#sang-che">Patents</a>', '<a href="#tin-tuc">新闻</a><a href="#bai-bao">科技论文</a><a href="#sang-che">专利</a>'),
('>Sản phẩm <span class="caret">', '>Products <span class="caret">', '>产品 <span class="caret">'),
('>Dịch vụ <span class="caret">', '>Services <span class="caret">', '>服务 <span class="caret">'),
('<a href="#linh-vuc">Nghiên cứu khoa học công nghệ</a><a href="#linh-vuc">Tư vấn xây dựng</a><a href="#linh-vuc">Thí nghiệm – Kiểm định</a><a href="#linh-vuc">Thiết kế – Chế tạo – Sửa chữa thiết bị</a><a href="#linh-vuc">Thương mại, xuất – nhập khẩu</a>',
 '<a href="#linh-vuc">Scientific &amp; technological research</a><a href="#linh-vuc">Construction consulting</a><a href="#linh-vuc">Testing – Inspection</a><a href="#linh-vuc">Equipment design – fabrication – repair</a><a href="#linh-vuc">Trading, import – export</a>',
 '<a href="#linh-vuc">科学技术研究</a><a href="#linh-vuc">建设咨询</a><a href="#linh-vuc">试验 – 检定</a><a href="#linh-vuc">设备设计 – 制造 – 维修</a><a href="#linh-vuc">贸易及进出口</a>'),
('<a href="#lien-he">Liên hệ</a>\n  </nav>', '<a href="#lien-he">Contact</a>\n  </nav>', '<a href="#lien-he">联系我们</a>\n  </nav>'),
('aria-label="Tìm sản phẩm" aria-expanded="false"', 'aria-label="Search products" aria-expanded="false"', 'aria-label="搜索产品" aria-expanded="false"'),
('placeholder="Nhập tên hoặc mã sản phẩm…" aria-label="Tìm sản phẩm"', 'placeholder="Enter product name or code…" aria-label="Search products"', 'placeholder="输入产品名称或编号…" aria-label="搜索产品"'),
('type="submit">Tìm kiếm</button>', 'type="submit">Search</button>', 'type="submit">搜索</button>'),
# hero
('alt="Vân Phong – Thiết bị phòng thí nghiệm: Phân tích – An toàn sinh học – Bảo quản mẫu"', 'alt="Van Phong – Laboratory equipment: analysis, biosafety, sample storage"', 'alt="Van Phong – 实验室设备：分析、生物安全、样品保存"'),
('alt="Vân Phong – Giải pháp công nghiệp &amp; tự động hóa: Máy móc – Điều khiển – Thiết bị đo"', 'alt="Van Phong – Industrial &amp; automation solutions: machinery, controls, instrumentation"', 'alt="Van Phong – 工业与自动化解决方案：机械、控制、测量仪表"'),
('<a class="hot" href="tel:0986818013"><i><svg viewBox="0 0 24 24"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg></i>Hotline: 0986.818.013</a>', '<a class="hot" href="tel:+84986818013"><i><svg viewBox="0 0 24 24"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg></i>Hotline: +84 986 818 013</a>', '<a class="hot" href="tel:+84986818013"><i><svg viewBox="0 0 24 24"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg></i>热线：+84 986 818 013</a>'),
('<a class="hot" href="tel:0899990683"><i><svg viewBox="0 0 24 24"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg></i>Hotline: 08.9999.0683</a>', '<a class="hot" href="tel:+84899990683"><i><svg viewBox="0 0 24 24"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg></i>Hotline: +84 899 990 683</a>', '<a class="hot" href="tel:+84899990683"><i><svg viewBox="0 0 24 24"><path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg></i>热线：+84 899 990 683</a>'),
('src="/banner-van-phong.jpg"', 'src="/banner-van-phong-en.jpg"', 'src="/banner-van-phong-zh.jpg"'),
('src="/banner-thiet-bi-ptn.jpg"', 'src="/banner-thiet-bi-ptn-en.jpg"', 'src="/banner-thiet-bi-ptn-zh.jpg"'),
('src="/banner-cong-nghiep.jpg"', 'src="/banner-cong-nghiep-en.jpg"', 'src="/banner-cong-nghiep-zh.jpg"'),
('alt="Drawell – Thiết bị phòng thí nghiệm. Vân Phong – đại lý phân phối chính hãng"', 'alt="Drawell – laboratory equipment. Van Phong – authorized distributor"', 'alt="Drawell – 实验室设备。Van Phong – 官方授权经销商"'),
('src="/banner-drawell.jpg"', 'src="/banner-drawell-en.jpg"', 'src="/banner-drawell-zh.jpg"'),
('src="/banner-biobase.jpg"', 'src="/banner-biobase-en.jpg"', 'src="/banner-biobase-zh.jpg"'),
('alt="Giải pháp thiết bị phòng thí nghiệm BIOBASE – An toàn, chính xác, đồng bộ"', 'alt="BIOBASE laboratory equipment solutions – safe, accurate, integrated"', 'alt="BIOBASE 实验室设备解决方案 – 安全、精准、配套"'),
('<a class="cert cert-real" href="/giay-to/drawell-uy-quyen.jpg" target="_blank" rel="noopener"><div class="doc real sq"><img src="/giay-to/drawell-uy-quyen.jpg" alt="Drawell Scientific Instruments Việt Nam – Ủy quyền chính hãng cho Công ty TNHH Kỹ thuật và Thương mại Vân Phong" width="1254" height="1254" loading="lazy"></div><b>Ủy quyền chính hãng Drawell</b><small>Drawell Scientific Instruments · Bấm để xem</small></a>', '<a class="cert cert-real" href="/giay-to/drawell-uy-quyen-en.jpg" target="_blank" rel="noopener"><div class="doc real sq"><img src="/giay-to/drawell-uy-quyen-en.jpg" alt="Drawell Scientific Instruments Vietnam – authorized distributor: Van Phong Technical and Trading Co., Ltd." width="1254" height="1254" loading="lazy"></div><b>Drawell authorized distributor</b><small>Drawell Scientific Instruments · Click to view</small></a>', '<a class="cert cert-real" href="/giay-to/drawell-uy-quyen-zh.jpg" target="_blank" rel="noopener"><div class="doc real sq"><img src="/giay-to/drawell-uy-quyen-zh.jpg" alt="Drawell 科学仪器越南 – 官方授权经销商：Van Phong 技术与贸易有限公司" width="1254" height="1254" loading="lazy"></div><b>Drawell 官方授权经销商</b><small>Drawell Scientific Instruments · 点击查看</small></a>'),
('alt="Vân Phong – Giải pháp kỹ thuật toàn diện: Thiết bị – Dịch vụ – Chuyển giao công nghệ cho Công nghiệp, Y tế, Phòng thí nghiệm, Giáo dục"', 'alt="Van Phong – Complete engineering solutions: equipment, services and technology transfer for industry, healthcare, laboratories and education"', 'alt="Van Phong – 全面技术解决方案：面向工业、医疗、实验室和教育的设备、服务与技术转让"'),
('<h2>Sản phẩm</h2>\n        <p class="lead">Thiết bị, vật tư cho Công nghiệp, Y tế, Phòng thí nghiệm, Giáo dục.</p>', '<h2>Products</h2>\n        <p class="lead">Equipment and supplies for industry, healthcare, laboratories and education.</p>', '<h2>产品</h2>\n        <p class="lead">面向工业、医疗、实验室和教育的设备与物资。</p>'),
('<b>Thiết bị công nghiệp</b><span>Máy cơ khí, bơm, quạt, hộp giảm tốc, phụ tùng</span>', '<b>Industrial equipment</b><span>Machinery, pumps, fans, gearboxes, spare parts</span>', '<b>工业设备</b><span>机械设备、泵、风机、减速机、备件</span>'),
('<b>Thiết bị y tế</b><span>Xét nghiệm, giường bệnh, tiệt trùng</span>', '<b>Medical equipment</b><span>Clinical analyzers, hospital beds, sterilization</span>', '<b>医疗设备</b><span>检验分析、病床、灭菌</span>'),
('<b>Thiết bị thí nghiệm</b><span>Tủ an toàn, tủ sấy, lò nung, cân, máy ly tâm, vật tư</span>', '<b>Laboratory equipment</b><span>Safety cabinets, ovens, furnaces, balances, centrifuges, consumables</span>', '<b>实验室设备</b><span>安全柜、干燥箱、马弗炉、天平、离心机、耗材</span>'),
('<b>Điện – Điện tử, Tự động hóa</b><span>PLC, biến tần, cảm biến, thiết bị đo</span>', '<b>Electrical, electronics &amp; automation</b><span>PLCs, inverters, sensors, instruments</span>', '<b>电气、电子与自动化</b><span>PLC、变频器、传感器、测量仪表</span>'),
('<b>Máy tính – Tin học</b><span>Máy tính, máy chủ, mạng, phần mềm</span>', '<b>Computers &amp; IT</b><span>Computers, servers, networking, software</span>', '<b>计算机与信息技术</b><span>计算机、服务器、网络、软件</span>'),
('href="#san-pham">Xem sản phẩm</a></p>', 'href="#san-pham">View products</a></p>', 'href="#san-pham">查看产品</a></p>'),
('<h2>Dịch vụ</h2>\n        <p class="lead">', '<h2>Services</h2>\n        <p class="lead">', '<h2>服务</h2>\n        <p class="lead">'),
('href="#linh-vuc">Xem dịch vụ</a></p>', 'href="#linh-vuc">View services</a></p>', 'href="#linh-vuc">查看服务</a></p>'),
('<p class="lead">Đồng hành từ tư vấn, thiết kế đến cung cấp, lắp đặt và bảo trì.</p>', '<p class="lead">With you from consulting and design to supply, installation and maintenance.</p>', '<p class="lead">从咨询、设计到供货、安装与维护，全程相伴。</p>'),
('<div><b>Nghiên cứu khoa học công nghệ</b><span>Phát triển, chuyển giao công nghệ</span></div>', '<div><b>Scientific &amp; technological research</b><span>Development, technology transfer</span></div>', '<div><b>科学技术研究</b><span>研发、技术转让</span></div>'),
('<div><b>Tư vấn xây dựng</b><span>Thiết kế · Thẩm tra · Giám sát</span></div>', '<div><b>Construction consulting</b><span>Design · Verification · Supervision</span></div>', '<div><b>建设咨询</b><span>设计 · 审查 · 监理</span></div>'),
('<div><b>Thí nghiệm – Kiểm định</b><span>Vật liệu, thiết bị</span></div>', '<div><b>Testing – Inspection</b><span>Materials, equipment</span></div>', '<div><b>试验 – 检定</b><span>材料、设备</span></div>'),
('<div><b>Thiết kế – Chế tạo – Sửa chữa thiết bị</b><span>Công nghiệp, Y tế, Phòng thí nghiệm</span></div>', '<div><b>Equipment design – fabrication – repair</b><span>Industrial, medical, laboratory</span></div>', '<div><b>设备设计 – 制造 – 维修</b><span>工业、医疗、实验室</span></div>'),
('<div><b>Thương mại, xuất – nhập khẩu</b><span>Vật tư, thiết bị, phần mềm</span></div>', '<div><b>Trading, import – export</b><span>Materials, equipment, software</span></div>', '<div><b>贸易及进出口</b><span>物资、设备、软件</span></div>'),
('aria-label="Ảnh trước"', 'aria-label="Previous slide"', 'aria-label="上一张"'),
('aria-label="Ảnh sau"', 'aria-label="Next slide"', 'aria-label="下一张"'),
# stats
# about
('alt="Phối cảnh trụ sở Công ty Vân Phong, số 34 ngõ 36A phố Trần Điền, Hà Nội"', 'alt="Rendering of Van Phong head office, No. 34 Lane 36A Tran Dien, Hanoi"', 'alt="Van Phong 公司总部效果图，河内陈田街36A巷34号"'),
('<figcaption>Trụ sở: Số 34, ngõ 36A, phố Trần Điền, Hà Nội</figcaption>', '<figcaption>Head office: No. 34, Lane 36A, Tran Dien Street, Hanoi</figcaption>', '<figcaption>总部：河内陈田街36A巷34号</figcaption>'),
('<h2>Giới thiệu</h2>', '<h2>About us</h2>', '<h2>关于我们</h2>'),
('<p>Công ty TNHH Kỹ thuật và Thương mại Vân Phong được thành lập ngày 25/06/2019 tại Hà Nội, hoạt động trong các lĩnh vực:</p>',
 '<p>Van Phong Technical and Trading Company Limited was established on 25 June 2019 in Hanoi and operates in the following fields:</p>',
 '<p>Van Phong 技术与贸易有限公司于2019年6月25日在越南河内成立，业务领域包括：</p>'),
('<li>Nghiên cứu khoa học công nghệ.</li>', '<li>Scientific and technological research.</li>', '<li>科学技术研究。</li>'),
('<li>Tư vấn xây dựng.</li>', '<li>Construction consulting.</li>', '<li>建设咨询。</li>'),
('<li>Thí nghiệm – Kiểm định.</li>', '<li>Testing – Inspection.</li>', '<li>试验 – 检定。</li>'),
('<li>Thiết kế – Chế tạo – Sửa chữa thiết bị.</li>', '<li>Design – Fabrication – Repair of equipment.</li>', '<li>设备设计 – 制造 – 维修。</li>'),
('<li>Thương mại, xuất – nhập khẩu.</li>', '<li>Trading, import – export.</li>', '<li>贸易及进出口。</li>'),
('<p><b>Mặt hàng:</b> Vật tư, thiết bị, phần mềm công nghiệp, y tế, giáo dục, phòng thí nghiệm, tin học máy tính.</p>',
 '<p><b>Products:</b> Materials, equipment and software for industry, healthcare, education, laboratories, computers and IT.</p>',
 '<p><b>经营产品：</b>工业、医疗、教育、实验室及计算机信息技术领域的物资、设备与软件。</p>'),
('<p>Ngành nghề kinh doanh chính: bán buôn máy móc, thiết bị và phụ tùng máy (mã ngành 4659). Phạm vi đa lĩnh vực giúp chúng tôi đồng hành cùng khách hàng từ khâu ý tưởng, thiết kế đến cung cấp, lắp đặt và bảo trì.</p>',
 '<p>Main business line: wholesale of machinery, equipment and spare parts (VSIC 4659). Our multidisciplinary scope lets us support customers from concept and design to supply, installation and maintenance.</p>',
 '<p>主营业务：机械、设备及零配件批发（行业代码 4659）。多领域的业务范围使我们能够从构思、设计到供货、安装与维护，全程服务客户。</p>'),
('<li><b>Sứ mệnh:</b> Giải pháp kỹ thuật tin cậy cho mọi khách hàng.</li>', '<li><b>Mission:</b> Reliable engineering solutions for every customer.</li>', '<li><b>使命：</b>为每一位客户提供可靠的技术解决方案。</li>'),
('<li><b>Tầm nhìn:</b> Đối tác kỹ thuật hàng đầu về công nghiệp, y tế và thí nghiệm.</li>', '<li><b>Vision:</b> A leading engineering partner in industry, healthcare and laboratories.</li>', '<li><b>愿景：</b>成为工业、医疗和实验室领域领先的技术合作伙伴。</li>'),
('<li><b>Giá trị cốt lõi:</b> Chính xác – Tận tâm – Hiệu quả.</li>', '<li><b>Core values:</b> Accuracy – Dedication – Efficiency.</li>', '<li><b>核心价值观：</b>精准 – 用心 – 高效。</li>'),
('<div class="legal">VAN PHONG TECHNICAL AND TRADING COMPANY LIMITED<br>VAN PHONG TECH CO., LTD. · MSDN 0108797479</div>',
 '<div class="legal">CÔNG TY TNHH KỸ THUẬT VÀ THƯƠNG MẠI VÂN PHONG<br>VAN PHONG TECH CO., LTD. · Enterprise code 0108797479</div>',
 '<div class="legal">VAN PHONG TECHNICAL AND TRADING COMPANY LIMITED<br>VAN PHONG TECH CO., LTD. · 企业代码 0108797479</div>'),
('href="#linh-vuc">Xem thêm &gt;&gt;</a>', 'href="#linh-vuc">Read more &gt;&gt;</a>', 'href="#linh-vuc">了解更多 &gt;&gt;</a>'),
# products sections
('<h2>Sản phẩm nổi bật</h2>', '<h2>Featured products</h2>', '<h2>热门产品</h2>'),
('aria-label="Trước"', 'aria-label="Previous"', 'aria-label="上一个"'),
('aria-label="Sau"', 'aria-label="Next"', 'aria-label="下一个"'),
('<div class="title"><h2>Sản phẩm</h2></div>\n  <div class="catalog">', '<div class="title"><h2>Products</h2></div>\n  <div class="catalog">', '<div class="title"><h2>产品</h2></div>\n  <div class="catalog">'),
('<h3 id="catTitle">Sản phẩm</h3>', '<h3 id="catTitle">Products</h3>', '<h3 id="catTitle">产品</h3>'),
('placeholder="Tìm theo tên, mã…" aria-label="Tìm sản phẩm"', 'placeholder="Search by name, code…" aria-label="Search products"', 'placeholder="按名称、编号搜索…" aria-label="搜索产品"'),
('type="submit">Tìm</button>', 'type="submit">Search</button>', 'type="submit">搜索</button>'),
('aria-label="Phân trang"', 'aria-label="Pagination"', 'aria-label="分页"'),
# fields
('<div class="title"><h2>Dịch vụ</h2></div>\n  <div class="fields">', '<div class="title"><h2>Services</h2></div>\n  <div class="fields">', '<div class="title"><h2>服务</h2></div>\n  <div class="fields">'),
('<h3>Nghiên cứu khoa học công nghệ</h3><ul><li>Nghiên cứu, phát triển sản phẩm</li><li>Chuyển giao công nghệ</li></ul>',
 '<h3>Scientific and technological research</h3><ul><li>Product research and development</li><li>Technology transfer</li></ul>',
 '<h3>科学技术研究</h3><ul><li>产品研究与开发</li><li>技术转让</li></ul>'),
('<h3>Tư vấn xây dựng</h3><ul><li>Tư vấn thiết kế</li><li>Tư vấn thẩm tra</li><li>Tư vấn giám sát</li></ul>',
 '<h3>Construction consulting</h3><ul><li>Design consulting</li><li>Design verification</li><li>Construction supervision</li></ul>',
 '<h3>建设咨询</h3><ul><li>设计咨询</li><li>设计审查</li><li>施工监理</li></ul>'),
('<h3>Thí nghiệm – Kiểm định</h3><ul><li>Thí nghiệm vật liệu, thiết bị</li><li>Kiểm định thiết bị</li><li>Phục vụ thiết kế, thi công, nghiệm thu</li></ul>',
 '<h3>Testing – Inspection</h3><ul><li>Testing of materials and equipment</li><li>Equipment inspection</li><li>Support for design, construction and acceptance</li></ul>',
 '<h3>试验 – 检定</h3><ul><li>材料及设备试验</li><li>设备检定</li><li>服务于设计、施工及验收</li></ul>'),
('<h3>Thiết kế – Chế tạo – Sửa chữa thiết bị</h3><ul><li>Công nghiệp</li><li>Y tế</li><li>Phòng thí nghiệm</li></ul>',
 '<h3>Design – Fabrication – Repair of equipment</h3><ul><li>Industrial</li><li>Medical</li><li>Laboratory</li></ul>',
 '<h3>设备设计 – 制造 – 维修</h3><ul><li>工业</li><li>医疗</li><li>实验室</li></ul>'),
('<h3>Thương mại, xuất – nhập khẩu</h3><p style="margin:0 0 4px;font-size:14px;color:#4A545E">Vật tư, thiết bị, phần mềm:</p><ul><li>Công nghiệp</li><li>Y tế</li><li>Giáo dục</li><li>Phòng thí nghiệm</li><li>Tin học máy tính</li></ul>',
 '<h3>Trading, import – export</h3><p style="margin:0 0 4px;font-size:14px;color:#4A545E">Materials, equipment, software:</p><ul><li>Industrial</li><li>Medical</li><li>Education</li><li>Laboratory</li><li>Computers &amp; IT</li></ul>',
 '<h3>贸易及进出口</h3><p style="margin:0 0 4px;font-size:14px;color:#4A545E">物资、设备、软件：</p><ul><li>工业</li><li>医疗</li><li>教育</li><li>实验室</li><li>计算机与信息技术</li></ul>'),
# news
# certificates
('<h2>Chứng nhận</h2><p>Bấm vào giấy tờ để xem.</p>', '<h2>Certificates</h2><p>Click a document to view it.</p>', '<h2>证书</h2><p>点击文件即可查看。</p>'),
('aria-label="Xem Giấy chứng nhận đăng ký doanh nghiệp"', 'aria-label="View Enterprise Registration Certificate"', 'aria-label="查看企业登记证书"'),
('alt="Giấy chứng nhận đăng ký doanh nghiệp – trang 1"', 'alt="Enterprise Registration Certificate – page 1"', 'alt="企业登记证书 – 第1页"'),
('<b>Giấy chứng nhận đăng ký doanh nghiệp</b><small>MSDN 0108797479 · thay đổi lần 4: 29/09/2026 · Bấm để xem</small>',
 '<b>Enterprise Registration Certificate</b><small>Enterprise code 0108797479 · 4th amendment: 29 Sep 2026 · Vietnamese original</small>',
 '<b>企业登记证书</b><small>企业代码 0108797479 · 第4次变更：2026-09-29 · 越文原件</small>'),
('href="/tai-lieu/ho-so-nang-luc-vi.pdf"', 'href="/tai-lieu/ho-so-nang-luc-en.pdf"', 'href="/tai-lieu/ho-so-nang-luc-zh.pdf"'),
('src="/tai-lieu/bia-vi-1.jpg" alt="Hồ sơ năng lực Vân Phong – trang bìa"', 'src="/tai-lieu/bia-en-1.jpg" alt="Van Phong company profile – cover"', 'src="/tai-lieu/bia-zh-1.jpg" alt="Van Phong 公司简介 – 封面"'),
('<b>Hồ sơ năng lực</b><small>Bản PDF · Bấm để xem, tải về</small>', '<b>Company Profile</b><small>PDF · Click to view or download</small>', '<b>公司简介</b><small>PDF · 点击查看或下载</small>'),
('<!--TRNOTE-->', '<p class="tr-note">Download the English translation: <a href="/tai-lieu/giay-chung-nhan-dkdn-en.pdf" target="_blank" rel="noopener">PDF</a></p>',
 '<p class="tr-note">下载中文译文：<a href="/tai-lieu/giay-chung-nhan-dkdn-zh.pdf" target="_blank" rel="noopener">PDF</a></p>'),
# quick links + footer
('<h2>Liên kết nhanh</h2>', '<h2>Quick links</h2>', '<h2>快速链接</h2>'),
('<h4>Liên hệ</h4>', '<h4>Contact</h4>', '<h4>联系方式</h4>'),
('<dt>Địa chỉ:</dt>', '<dt>Address:</dt>', '<dt>地址：</dt>'),
('<dt>Hotline:</dt><dd><a href="tel:0899990683">08.9999.0683</a> / <a href="tel:0986818013">0986.818.013</a></dd>', '<dt>Hotline:</dt><dd><a href="tel:+84899990683">+84 899 990 683</a> / <a href="tel:+84986818013">+84 986 818 013</a></dd>', '<dt>热线：</dt><dd><a href="tel:+84899990683">+84 899 990 683</a> / <a href="tel:+84986818013">+84 986 818 013</a></dd>'),
('<dt>Email:</dt>', '<dt>Email:</dt>', '<dt>邮箱：</dt>'),
('<dt>Website:</dt>', '<dt>Website:</dt>', '<dt>网站：</dt>'),
('<h4>Về Vân Phong</h4>', '<h4>About Van Phong</h4>', '<h4>关于 Van Phong</h4>'),
('<p style="margin:0">Công ty TNHH Kỹ thuật và Thương mại Vân Phong — Kỹ thuật – Thương mại. Vật tư, thiết bị, phần mềm công nghiệp, y tế, giáo dục, phòng thí nghiệm, tin học máy tính.</p>',
 '<p style="margin:0">Van Phong Technical and Trading Co., Ltd. — Engineering – Trading. Materials, equipment and software for industry, healthcare, education, laboratories, computers and IT.</p>',
 '<p style="margin:0">Van Phong 技术与贸易有限公司 —— 技术 – 贸易。工业、医疗、教育、实验室及计算机信息技术领域的物资、设备与软件。</p>'),
('<h4>Danh mục</h4>', '<h4>Categories</h4>', '<h4>产品分类</h4>'),
('<span>© 2026 Công ty TNHH Kỹ thuật và Thương mại Vân Phong</span><span>MSDN 0108797479</span>', '<span>© 2026 Van Phong Technical and Trading Co., Ltd.</span><span>Enterprise code 0108797479</span>', '<span>© 2026 Van Phong 技术与贸易有限公司</span><span>企业代码 0108797479</span>'),
('<a href="tel:0899990683"><span>', '<a href="tel:+84899990683"><span>', '<a href="tel:+84899990683"><span>'),
('aria-label="Zalo 08.9999.0683"', 'aria-label="Zalo +84 899 990 683"', 'aria-label="Zalo +84 899 990 683"'),
('<span class="tip">Zalo Vân Phong: 08.9999.0683</span>', '<span class="tip">Zalo Van Phong: +84 899 990 683</span>', '<span class="tip">Zalo Van Phong：+84 899 990 683</span>'),
('aria-label="Zalo 0986.818.013"', 'aria-label="Zalo +84 986 818 013"', 'aria-label="Zalo +84 986 818 013"'),
('<span class="tip">Zalo Ms Trâm (BIOBASE, Drawell): 0986.818.013</span>', '<span class="tip">Zalo Ms Tram (BIOBASE, Drawell): +84 986 818 013</span>', '<span class="tip">Zalo Tram 女士（BIOBASE、Drawell）：+84 986 818 013</span>'),
('<a class="fs call c2" href="tel:0986818013" aria-label="Gọi 0986.818.013"', '<a class="fs call c2" href="tel:+84986818013" aria-label="Call +84 986 818 013"', '<a class="fs call c2" href="tel:+84986818013" aria-label="致电 +84 986 818 013"'),
('<span class="tip">Ms Trâm: 0986.818.013</span>', '<span class="tip">Ms Tram: +84 986 818 013</span>', '<span class="tip">Tram 女士：+84 986 818 013</span>'),
('<a class="fs call" href="tel:0899990683"', '<a class="fs call" href="tel:+84899990683"', '<a class="fs call" href="tel:+84899990683"'),
('aria-label="Gọi 08.9999.0683"', 'aria-label="Call +84 899 990 683"', 'aria-label="致电 +84 899 990 683"'),
('<span class="tip">08.9999.0683</span>', '<span class="tip">+84 899 990 683</span>', '<span class="tip">+84 899 990 683</span>'),
('<!--TRCARD-->', '<button type="button" class="cert cert-real" data-gallery="/tai-lieu/dkdn-en-1.jpg|/tai-lieu/dkdn-en-2.jpg" data-note="English reference translation – no signature or seal. The Vietnamese original prevails." aria-label="View English translation of the Enterprise Registration Certificate"><div class="doc real"><img src="/tai-lieu/dkdn-en-nho-1.jpg" alt="English translation – page 1" width="397" height="562" loading="lazy"></div><b>Enterprise Registration Certificate – English translation</b><small>Reference translation · Click to view</small></button>',
 '<button type="button" class="cert cert-real" data-gallery="/tai-lieu/dkdn-zh-1.jpg|/tai-lieu/dkdn-zh-2.jpg" data-note="中文参考译文，无签字盖章，以越文原件为准。" aria-label="查看企业登记证书中文译文"><div class="doc real"><img src="/tai-lieu/dkdn-zh-nho-1.jpg" alt="中文译文 – 第1页" width="397" height="562" loading="lazy"></div><b>企业登记证书 – 中文译文</b><small>参考译文 · 点击查看</small></button>'),
("n:'Sàng đĩa đan xen CRS350-15 (350 t/h)', code:'CRS350-15', pdf:'crs350-15', img:'crs350-15', dwg:'/ban-ve/crs350-15-ban-ve.pdf', art:'2026-performance-evaluation-of-the-crs1414-intermeshing-rotary', d:'Sàng than: cỡ hạt cấp liệu 150 mm, cỡ hạt dưới sàng 15 mm, năng suất 350 t/h, động cơ 3 × 7,5 kW. Vân Phong tư vấn tính toán, lựa chọn thiết bị cho chủ đầu tư Công ty CP Than Vàng Danh – Vinacomin. Hãng sản xuất: Gongbei (Trung Quốc).'", "n:'CRS350-15 interlaced disc screen (350 t/h)', code:'CRS350-15', pdf:'crs350-15', img:'crs350-15', dwg:'/ban-ve/crs350-15-ban-ve.pdf', art:'2026-performance-evaluation-of-the-crs1414-intermeshing-rotary', d:'Coal screen: feed size 150 mm, undersize 15 mm, capacity 350 t/h, motors 3 × 7.5 kW. Van Phong provided sizing calculations and equipment selection for the project owner, Vang Danh Coal JSC – Vinacomin. Manufacturer: Gongbei (China).'", "n:'CRS350-15 交叉筛（350 t/h）', code:'CRS350-15', pdf:'crs350-15', img:'crs350-15', dwg:'/ban-ve/crs350-15-ban-ve.pdf', art:'2026-performance-evaluation-of-the-crs1414-intermeshing-rotary', d:'筛分物料：煤；入料粒度 150 mm，筛下粒度 15 mm，处理量 350 t/h，电机功率 3×7.5 kW。Van Phong 为业主 Vang Danh 煤炭股份公司（Vinacomin）提供计算选型咨询。制造商：石家庄功倍重型机械（中国）。'"),
("n:'Máy đông khô BIOBASE BK-FD10P (-60°C)', code:'BK-FD10P', pdf:'bk-fd10p', img:'https://img.waimaoniu.net/2587/2587-202509051725232976.jpg', d:'Máy sấy đông khô phòng thí nghiệm, nhiệt độ bẫy lạnh đến -60°C. Hãng BIOBASE.'", "n:'BIOBASE BK-FD10P freeze dryer (-60°C)', code:'BK-FD10P', pdf:'bk-fd10p', img:'https://img.waimaoniu.net/2587/2587-202509051725232976.jpg', d:'Laboratory freeze dryer with cold trap down to -60°C. Brand: BIOBASE.'", "n:'BIOBASE BK-FD10P 冷冻干燥机（-60°C）', code:'BK-FD10P', pdf:'bk-fd10p', img:'https://img.waimaoniu.net/2587/2587-202509051725232976.jpg', d:'实验室冷冻干燥机，冷阱温度可达 -60°C。品牌：BIOBASE。'"),
("n:'Tủ cấy vi sinh BIOBASE BBS-H1500', code:'BBS-H1500', pdf:'bbs-h1500', img:'https://img.waimaoniu.net/2587/2587-202511181524506151.jpg', d:'Tủ cấy vi sinh cho phòng thí nghiệm; cung cấp kèm lắp đặt, chạy thử, hướng dẫn sử dụng. Hãng BIOBASE.'", "n:'BIOBASE BBS-H1500 clean bench', code:'BBS-H1500', pdf:'bbs-h1500', img:'https://img.waimaoniu.net/2587/2587-202511181524506151.jpg', d:'Laboratory clean bench, supplied with installation, commissioning and user training. Brand: BIOBASE.'", "n:'BIOBASE BBS-H1500 超净工作台', code:'BBS-H1500', pdf:'bbs-h1500', img:'https://img.waimaoniu.net/2587/2587-202511181524506151.jpg', d:'实验室超净工作台，含安装、调试及使用培训。品牌：BIOBASE。'"),
("n:'Tủ cấy vi sinh BIOBASE BKCB-V900', code:'BKCB-V900', pdf:'bkcb-v900', img:'https://img.waimaoniu.net/2587/2587-202305301333138702.jpg', d:'Tủ cấy vi sinh dòng khí thổi đứng. Hãng BIOBASE.'", "n:'BIOBASE BKCB-V900 clean bench', code:'BKCB-V900', pdf:'bkcb-v900', img:'https://img.waimaoniu.net/2587/2587-202305301333138702.jpg', d:'Vertical laminar flow clean bench. Brand: BIOBASE.'", "n:'BIOBASE BKCB-V900 超净工作台', code:'BKCB-V900', pdf:'bkcb-v900', img:'https://img.waimaoniu.net/2587/2587-202305301333138702.jpg', d:'垂直层流超净工作台。品牌：BIOBASE。'"),
("n:'Máy khuấy cơ học Drawell OS20-Pro', code:'OS20-Pro', pdf:'os20-pro', img:'https://www.drawellanalytical.com/wp-content/uploads/2023/07/Overhead-Stirrer-OS70-Pro-OS40-Pro-OS20-Pro.jpg', d:'Máy khuấy đũa cơ học cho phòng thí nghiệm hóa học. Hãng Drawell.'", "n:'Drawell OS20-Pro overhead stirrer', code:'OS20-Pro', pdf:'os20-pro', img:'https://www.drawellanalytical.com/wp-content/uploads/2023/07/Overhead-Stirrer-OS70-Pro-OS40-Pro-OS20-Pro.jpg', d:'Overhead mechanical stirrer for chemistry laboratories. Brand: Drawell.'", "n:'Drawell OS20-Pro 顶置式机械搅拌器', code:'OS20-Pro', pdf:'os20-pro', img:'https://www.drawellanalytical.com/wp-content/uploads/2023/07/Overhead-Stirrer-OS70-Pro-OS40-Pro-OS20-Pro.jpg', d:'化学实验室用顶置式机械搅拌器。品牌：Drawell。'"),
('<a href="#doi-tac">Đối tác</a>', '<a href="#doi-tac">Partners</a>', '<a href="#doi-tac">合作伙伴</a>'),
("'+p.art+'.pdf\" target=\"_blank\" rel=\"noopener\">Bài báo ứng dụng (PDF)</a>", "'+p.art+'-en.pdf\" target=\"_blank\" rel=\"noopener\">Application paper (PDF)</a>", "'+p.art+'-zh.pdf\" target=\"_blank\" rel=\"noopener\">应用论文（PDF）</a>"),
("n:'Lò nung BIOBASE dòng MX', code:'MX series', img:'mx-series', vid:'/video/lo-nung-mx.mp4', d:'Nhiệt độ cao ổn định cho mọi phép thử nhiệt. Phù hợp cho trường đại học, viện nghiên cứu, phòng thí nghiệm và khu công nghiệp trong các phép thử tro hóa, nung mẫu, xử lý nhiệt và kiểm nghiệm vật liệu. Dung tích 6–30 lít, nhiệt độ tối đa 1000–1200 °C (model đặc biệt đến 1700 °C), độ chính xác ±1 °C; buồng sợi gốm, gia nhiệt 4 mặt. Quý khách vui lòng liên hệ để được tư vấn model phù hợp. Hãng BIOBASE.'", "n:'BIOBASE MX series muffle furnace', code:'MX series', img:'mx-series', vid:'/video/lo-nung-mx.mp4', d:'Stable high temperature for every thermal test. Suited to universities, research institutes, laboratories and industrial parks for ashing, sample calcination, heat treatment and materials testing. Chamber 6–30 L, max temperature 1000–1200 °C (special models up to 1700 °C), accuracy ±1 °C; ceramic fibre chamber, heating on 4 sides. Please contact us for advice on the right model for your laboratory. Manufacturer: BIOBASE.'", "n:'BIOBASE MX 系列马弗炉', code:'MX series', img:'mx-series', vid:'/video/lo-nung-mx.mp4', d:'稳定高温，满足各类热学试验。适用于高校、科研院所、实验室及工业园区的灰化、样品灼烧、热处理和材料检测。容积 6–30 L，最高温度 1000–1200 °C（特殊型号可达 1700 °C），控温精度 ±1 °C；陶瓷纤维炉膛，四面加热。欢迎联系我们，为您的实验室推荐合适型号。制造商：BIOBASE。'"),
("n:'Micropipette BIOBASE', code:'BIOBASE', img:'micropipette', d:'Thao tác hút, chia mẫu thể tích nhỏ. Kết hợp đầu côn thường hoặc đầu côn lọc phù hợp ứng dụng. Có loại đơn kênh và đa kênh.'", "n:'BIOBASE micropipettes', code:'BIOBASE', img:'micropipette', d:'For aspirating and dispensing small sample volumes. Use standard or filter tips to suit the application. Single-channel and multichannel models.'", "n:'BIOBASE 移液器', code:'BIOBASE', img:'micropipette', d:'用于小体积样品的吸取和分配。可根据应用搭配普通吸头或滤芯吸头。提供单道和多道型号。'"),
("n:'Máy đo pH BIOBASE', code:'BIOBASE', img:'may-do-ph', d:'Phục vụ kiểm tra pH mẫu nước, nguyên liệu và sản phẩm theo phương pháp của phòng lab. Lựa chọn kèm dung dịch chuẩn, dung dịch bảo quản và điện cực phù hợp.'", 'n:\'BIOBASE pH meters\', code:\'BIOBASE\', img:\'may-do-ph\', d:"For checking the pH of water samples, raw materials and products according to the lab\'s methods. Supplied with suitable buffer solutions, storage solution and electrodes."', "n:'BIOBASE pH 计', code:'BIOBASE', img:'may-do-ph', d:'按实验室方法检测水样、原料和产品的 pH 值。可配套选择标准缓冲液、保存液及合适的电极。'"),
("n:'Bộ lọc chân không BIOBASE', code:'BIOBASE', img:'bo-loc-chan-khong', d:'Phục vụ lọc mẫu, chuẩn bị mẫu và quy trình kiểm nghiệm phù hợp. Lựa chọn màng lọc theo kích thước lỗ, vật liệu màng và tính chất mẫu.'", "n:'BIOBASE vacuum filtration sets', code:'BIOBASE', img:'bo-loc-chan-khong', d:'For sample filtration, sample preparation and testing procedures. Membranes are chosen by pore size, membrane material and sample properties.'", "n:'BIOBASE 真空过滤装置', code:'BIOBASE', img:'bo-loc-chan-khong', d:'用于样品过滤、样品前处理及相关检测流程。滤膜按孔径、材质和样品性质选择。'"),
("n:'Máy lọc nước phòng thí nghiệm BIOBASE', code:'BIOBASE', img:'may-loc-nuoc', d:'Lựa chọn chất lượng nước và công suất theo nhu cầu sử dụng, đồng thời xác định đúng lõi lọc, màng RO và cột DI thay thế.'", "n:'BIOBASE laboratory water purifiers', code:'BIOBASE', img:'may-loc-nuoc', d:'Water quality and output are chosen to match demand, together with the correct replacement filter cartridges, RO membranes and DI columns.'", "n:'BIOBASE 实验室纯水机', code:'BIOBASE', img:'may-loc-nuoc', d:'根据用水需求选择水质和产水量，并确定匹配的替换滤芯、RO 膜和 DI 柱。'"),
("n:'Máy ly tâm và ống ly tâm BIOBASE', code:'BIOBASE', img:'ong-ly-tam', d:'Phục vụ tách và chuẩn bị mẫu. Cần chọn đồng bộ rotor, adapter và ống ly tâm theo yêu cầu công việc.'", "n:'BIOBASE centrifuges and centrifuge tubes', code:'BIOBASE', img:'ong-ly-tam', d:'For sample separation and preparation. Rotors, adapters and centrifuge tubes should be selected as a matched set for the work.'", "n:'BIOBASE 离心机及离心管', code:'BIOBASE', img:'ong-ly-tam', d:'用于样品分离和前处理。转子、适配器和离心管需按工作要求配套选择。'"),
('rel="noopener">Video giới thiệu</a>', 'rel="noopener">Video</a>', 'rel="noopener">产品视频</a>'),
('rel="noopener">Bản vẽ (PDF)</a>', 'rel="noopener">Drawing (PDF)</a>', 'rel="noopener">图纸（PDF）</a>'),
("__PARTNERS__", "__PARTNERS_EN__", "__PARTNERS_ZH__"),
("__LEADERS__", "", ""),
("__NEWS__", "", ""),
("__PUBS__", "", ""),
("__PATENT__", "", ""),
('<button type="button" aria-expanded="false" data-href="#gioi-thieu">Giới thiệu <span class="caret"></span></button>', '<button type="button" aria-expanded="false" data-href="#gioi-thieu">About us <span class="caret"></span></button>', '<button type="button" aria-expanded="false" data-href="#gioi-thieu">关于我们 <span class="caret"></span></button>'),
('<h2>Đối tác – Khách hàng</h2><p>Các đơn vị đã hợp tác cùng Vân Phong.</p>', '<h2>Partners &amp; Clients</h2><p>Organizations that have worked with Van Phong.</p>', '<h2>合作伙伴与客户</h2><p>与 Van Phong 合作过的单位。</p>'),
("n:'Sàng đĩa đan xen CRS1414 (150 t/h)', code:'CRS1414', pdf:'crs1414', art:'2026-performance-evaluation-of-the-crs1414-intermeshing-rotary', img:'crs1414', d:'Năng suất 150 t/h, 14 trục, mặt sàng rộng 1400 mm, cỡ hạt dưới sàng ≤ 8 mm, động cơ 14 × 3,0 kW, kích thước 3740 × 2587 × 1555 mm, khoảng 10 tấn. 01 thiết bị cấp cho hệ thống sàng – nghiền than Phân xưởng Nhiệt điện – Công ty Nhôm Lâm Đồng – TKV. Hãng sản xuất: Gongbei (Trung Quốc).'", "n:'CRS1414 interlaced disc screen (150 t/h)', code:'CRS1414', pdf:'crs1414', art:'2026-performance-evaluation-of-the-crs1414-intermeshing-rotary', img:'crs1414', d:'Capacity 150 t/h, 14 shafts, screen width 1400 mm, undersize ≤ 8 mm, motors 14 × 3.0 kW, dimensions 3740 × 2587 × 1555 mm, approx. 10 t. One unit supplied for the coal screening and crushing system of the Thermal Power Workshop, Lam Dong Aluminum Company – TKV. Manufacturer: Gongbei (China).'", "n:'CRS1414 交叉筛（150 t/h）', code:'CRS1414', pdf:'crs1414', art:'2026-performance-evaluation-of-the-crs1414-intermeshing-rotary', img:'crs1414', d:'处理量 150 t/h，14 根筛轴，筛面宽度 1400 mm，筛下粒度 ≤ 8 mm，电机 14×3.0 kW，外形尺寸 3740×2587×1555 mm，重约 10 吨。为林同铝业公司（TKV）热电车间煤炭筛分–破碎系统供应 1 台。制造商：石家庄功倍重型机械（中国）。'"),
('aria-label="Liên hệ nhanh"', 'aria-label="Quick contact"', 'aria-label="快速联系"'),
('aria-label="Lên đầu trang"', 'aria-label="Back to top"', 'aria-label="返回顶部"'),
('aria-label="Xem giấy tờ"', 'aria-label="Document viewer"', 'aria-label="文件查看"'),
('aria-label="Đóng"', 'aria-label="Close"', 'aria-label="关闭"'),
('<p class="lb-note" id="lbNote">Một số thông tin cá nhân đã được che.</p>', '<p class="lb-note" id="lbNote">Vietnamese original. Some personal data has been hidden.</p>', '<p class="lb-note" id="lbNote">越文原件，部分个人信息已隐去。</p>'),
# script data
("name:'Thiết bị công nghiệp', subs:['Máy và thiết bị cơ khí','Bơm, quạt, hộp giảm tốc','Vật tư, phụ tùng thay thế']",
 "name:'Industrial equipment', subs:['Mechanical machinery & equipment','Pumps, fans, gearboxes','Consumables & spare parts']",
 "name:'工业设备', subs:['机械设备','泵、风机、减速机','耗材及备品备件']"),
("name:'Thiết bị y tế', subs:['Thiết bị xét nghiệm','Giường, xe đẩy y tế','Thiết bị tiệt trùng','Thiết bị y tế khác']",
 "name:'Medical equipment', subs:['Clinical analyzers','Hospital beds & trolleys','Sterilization equipment','Other medical equipment']",
 "name:'医疗设备', subs:['检验分析设备','病床、医用推车','灭菌设备','其他医疗设备']"),
("name:'Thiết bị thí nghiệm', subs:['Tủ an toàn, tủ cấy, tủ hút','Tủ sấy, tủ ấm, lò nung','Cân, máy ly tâm','Máy đông khô, máy khuấy','Dụng cụ, máy đo, vật tư phòng thí nghiệm','Thiết bị đông lạnh, bảo quản mẫu','Thiết bị phân tích phòng thí nghiệm','Thiết bị quang học','Sinh học phân tử, thuốc thử','Thiết bị giải phẫu bệnh']",
 "name:'Laboratory equipment', subs:['Biosafety cabinets, clean benches, fume hoods','Ovens, incubators, furnaces','Balances, centrifuges','Freeze dryers, stirrers','Lab instruments, meters & consumables','Cold storage & sample preservation','Laboratory analyzers','Optical instruments','Molecular biology & reagents','Pathology equipment']",
 "name:'实验室设备', subs:['生物安全柜、超净工作台、通风橱','干燥箱、培养箱、马弗炉','天平、离心机','冷冻干燥机、搅拌器','实验室器具、仪表及耗材','低温冷藏与样品保存设备','实验室分析仪器','光学仪器','分子生物学与试剂','病理设备']"),
("name:'Điện – Điện tử, Tự động hóa', subs:['PLC, bộ điều khiển','Biến tần, khởi động mềm','Cảm biến, thiết bị đo']",
 "name:'Electrical, Electronics & Automation', subs:['PLCs, controllers','Inverters, soft starters','Sensors, measuring instruments']",
 "name:'电气电子与自动化', subs:['PLC、控制器','变频器、软启动器','传感器、测量仪器']"),
("name:'Máy tính – Tin học', subs:['Máy tính, máy chủ','Thiết bị mạng, camera','Phần mềm bản quyền']",
 "name:'Computers & IT', subs:['Computers, servers','Network equipment, cameras','Licensed software']",
 "name:'计算机与信息技术', subs:['计算机、服务器','网络设备、摄像机','正版软件']"),
("n:'Tủ an toàn sinh học cấp II A2 BIOBASE BSC-1300IIA2-X', code:'BSC-1300IIA2-X', img:'bsc-1300iia2-x', d:'Kích thước ngoài 1300 × 755 × 2200 mm, buồng thao tác 1150 × 600 × 660 mm. 2 bộ lọc ULPA 99,9995% @ 0,12 μm; vận tốc gió vào 0,53 m/s, gió xuống 0,33 m/s; 70% tuần hoàn, 30% thải. Cửa kính kéo điện, màn hình LCD, cảnh báo âm thanh – ánh sáng; độ ồn ≤ 65 dB. Hãng BIOBASE.'", "n:'BIOBASE BSC-1300IIA2-X Class II A2 biosafety cabinet', code:'BSC-1300IIA2-X', img:'bsc-1300iia2-x', d:'External size 1300 × 755 × 2200 mm, work zone 1150 × 600 × 660 mm. Two ULPA filters, 99.9995% @ 0.12 μm; inflow 0.53 m/s, downflow 0.33 m/s; 70% recirculation, 30% exhaust. Motorized front window, LCD display, audible and visual alarms; noise ≤ 65 dB. Manufacturer: BIOBASE.'", "n:'BIOBASE BSC-1300IIA2-X II级A2型生物安全柜', code:'BSC-1300IIA2-X', img:'bsc-1300iia2-x', d:'外形尺寸 1300 × 755 × 2200 mm，工作区 1150 × 600 × 660 mm。2 个 ULPA 过滤器，0.12 μm 效率 99.9995%；流入风速 0.53 m/s，下降风速 0.33 m/s；70% 循环，30% 外排。电动前窗，LCD 显示，声光报警；噪音 ≤ 65 dB。制造商：BIOBASE。'"),
("n:'Tủ hút khí độc không ống dẫn BIOBASE FH1000(C)', code:'FH1000(C)', img:'https://img.waimaoniu.net/2587/2587-202312140940153756.jpg', d:'Kích thước ngoài 1000 × 830 × 2140 mm, buồng 910 × 690 × 740 mm. Vận tốc hút 0,4–0,6 m/s, lưu lượng 136 m³/h; 2 bộ lọc than hoạt tính, quạt ly tâm điều chỉnh tốc độ; mặt bàn nhựa phenolic kháng hóa chất; độ ồn ≤ 58 dB(A); công suất 400 W. Hãng BIOBASE.'", "n:'BIOBASE FH1000(C) ductless fume hood', code:'FH1000(C)', img:'https://img.waimaoniu.net/2587/2587-202312140940153756.jpg', d:'External size 1000 × 830 × 2140 mm, chamber 910 × 690 × 740 mm. Face velocity 0.4–0.6 m/s, airflow 136 m³/h; two chemical filters, speed-adjustable centrifugal blower; chemical-resistant phenolic resin worktop; noise ≤ 58 dB(A); power 400 W. Manufacturer: BIOBASE.'", "n:'BIOBASE FH1000(C) 无管道通风柜', code:'FH1000(C)', img:'https://img.waimaoniu.net/2587/2587-202312140940153756.jpg', d:'外形尺寸 1000 × 830 × 2140 mm，内腔 910 × 690 × 740 mm。风速 0.4–0.6 m/s，风量 136 m³/h；2 个化学过滤器，离心风机可调速；耐化学酚醛树脂台面；噪音 ≤ 58 dB(A)；功率 400 W。制造商：BIOBASE。'"),
("n:'Tủ sấy đối lưu cưỡng bức BIOBASE BJPX-HGZ30L', code:'BJPX-HGZ30L', img:'https://img.waimaoniu.net/2587/2587-202308141137457377.jpg', d:'Dung tích 30 lít, nhiệt độ từ nhiệt độ phòng +10 °C đến 300 °C, độ phân giải 0,1 °C; gia nhiệt đáy, đối lưu cưỡng bức; hẹn giờ 0–9999 phút; 2 khay; màn hình LCD. Buồng 310 × 310 × 310 mm, ngoài 440 × 670 × 495 mm. Hãng BIOBASE.'", "n:'BIOBASE BJPX-HGZ30L forced air drying oven', code:'BJPX-HGZ30L', img:'https://img.waimaoniu.net/2587/2587-202308141137457377.jpg', d:'Capacity 30 L, temperature RT+10 °C to 300 °C, resolution 0.1 °C; bottom heating with forced convection; timer 0–9999 min; 2 shelves; LCD display. Chamber 310 × 310 × 310 mm, external 440 × 670 × 495 mm. Manufacturer: BIOBASE.'", "n:'BIOBASE BJPX-HGZ30L 鼓风干燥箱', code:'BJPX-HGZ30L', img:'https://img.waimaoniu.net/2587/2587-202308141137457377.jpg', d:'容积 30 L，温度范围室温+10 °C 至 300 °C，精度 0.1 °C；底部加热，强制对流；定时 0–9999 分钟；2 层搁板；LCD 显示。内腔 310 × 310 × 310 mm，外形 440 × 670 × 495 mm。制造商：BIOBASE。'"),
("n:'Máy ly tâm để bàn tốc độ thấp BIOBASE BKC-TL5C', code:'BKC-TL5C', img:'https://img.waimaoniu.net/2587/2587-202605231435530935.jpg', d:'Tốc độ tối đa 5000 vòng/phút, lực ly tâm tối đa 3962 × g, dung tích tối đa 4 × 500 ml; độ chính xác ±10 vòng/phút; hẹn giờ 1 giây – 99 giờ 59 phút; rotor văng cho nhiều cỡ ống lấy máu; độ ồn ≤ 65 dB(A). Hãng BIOBASE.'", "n:'BIOBASE BKC-TL5C tabletop low-speed centrifuge', code:'BKC-TL5C', img:'https://img.waimaoniu.net/2587/2587-202605231435530935.jpg', d:'Max speed 5000 rpm, max RCF 3962 × g, max capacity 4 × 500 ml; speed accuracy ±10 rpm; timer 1 s – 99 h 59 min; swing rotors for many blood collection tube sizes; noise ≤ 65 dB(A). Manufacturer: BIOBASE.'", "n:'BIOBASE BKC-TL5C 台式低速离心机', code:'BKC-TL5C', img:'https://img.waimaoniu.net/2587/2587-202605231435530935.jpg', d:'最高转速 5000 r/min，最大离心力 3962 × g，最大容量 4 × 500 ml；转速精度 ±10 r/min；定时 1 秒 – 99 小时 59 分；水平转子适配多种采血管；噪音 ≤ 65 dB(A)。制造商：BIOBASE。'"),
("n:'Cân phân tích điện tử BIOBASE BA2204C', code:'BA2204C', img:'https://img.waimaoniu.net/2587/2587-202205120910212715.jpg', d:'Mức cân 220 g, độ đọc 0,1 mg, độ lặp lại 0,2 mg; hiệu chuẩn nội tự động; thời gian ổn định 4 giây; đĩa cân Φ90 mm, buồng chắn gió kính. Hãng BIOBASE.'", "n:'BIOBASE BA2204C electronic analytical balance', code:'BA2204C', img:'https://img.waimaoniu.net/2587/2587-202205120910212715.jpg', d:'Capacity 220 g, readability 0.1 mg, repeatability 0.2 mg; automatic internal calibration; stabilisation time 4 s; Φ90 mm pan with glass draft shield. Manufacturer: BIOBASE.'", "n:'BIOBASE BA2204C 电子分析天平', code:'BA2204C', img:'https://img.waimaoniu.net/2587/2587-202205120910212715.jpg', d:'称量 220 g，读数精度 0.1 mg，重复性 0.2 mg；自动内校；稳定时间 4 秒；Φ90 mm 秤盘，玻璃防风罩。制造商：BIOBASE。'"),
("n:'Nồi hấp tiệt trùng đứng BIOBASE BKQ-B50II', code:'BKQ-B50II', img:'https://img.waimaoniu.net/2587/2587-202508231532134994.jpg', d:'Dung tích 50 lít, áp suất làm việc 0,23 MPa, nhiệt độ tiệt trùng 105–136 °C, độ phân giải 0,1 °C; buồng thép không gỉ S30408 Φ386 × 514 mm; công suất 4,4 kW. Hãng BIOBASE.'", "n:'BIOBASE BKQ-B50II vertical autoclave', code:'BKQ-B50II', img:'https://img.waimaoniu.net/2587/2587-202508231532134994.jpg', d:'Capacity 50 L, working pressure 0.23 MPa, sterilising temperature 105–136 °C, resolution 0.1 °C; S30408 stainless steel chamber Φ386 × 514 mm; power 4.4 kW. Manufacturer: BIOBASE.'", "n:'BIOBASE BKQ-B50II 立式压力蒸汽灭菌器', code:'BKQ-B50II', img:'https://img.waimaoniu.net/2587/2587-202508231532134994.jpg', d:'容积 50 L，工作压力 0.23 MPa，灭菌温度 105–136 °C，精度 0.1 °C；S30408 不锈钢内胆 Φ386 × 514 mm；功率 4.4 kW。制造商：BIOBASE。'"),
("n:'Máy phân tích huyết học 5 thành phần BIOBASE BK-6310', code:'BK-6310', img:'https://img.waimaoniu.net/2587/2587-202510291646311584.jpg', d:'60 mẫu/giờ; 5 thành phần bạch cầu, 25 thông số, 3 biểu đồ histogram và đồ thị phân tán 3D; tán xạ laser 3 góc kết hợp đo tổng trở; thể tích mẫu ≤ 20 μl; lưu 300.000 kết quả; kết nối LIS 2 chiều (HL7). Hãng BIOBASE.'", "n:'BIOBASE BK-6310 5-part hematology analyzer', code:'BK-6310', img:'https://img.waimaoniu.net/2587/2587-202510291646311584.jpg', d:'60 tests/hour; 5-part differential, 25 parameters, 3 histograms and 3D scattergram; tri-angle laser scatter with impedance method; sample volume ≤ 20 μl; stores 300,000 results; bi-directional LIS (HL7). Manufacturer: BIOBASE.'", "n:'BIOBASE BK-6310 五分类血液分析仪', code:'BK-6310', img:'https://img.waimaoniu.net/2587/2587-202510291646311584.jpg', d:'每小时 60 个测试；五分类，25 项参数，3 个直方图及 3D 散点图；三角度激光散射结合电阻抗法；样本量 ≤ 20 μl；可存储 300,000 条结果；双向 LIS（HL7）。制造商：BIOBASE。'"),
("n:'Giường bệnh điện 3 chức năng BIOBASE MF301D-11', code:'MF301D-11', img:'https://img.waimaoniu.net/2587/2587-202511251715078673.jpg', d:'Kích thước 2120 × 910 × 520–770 mm; nâng tựa lưng 0–70°, đùi 0–30°, bắp chân 0–10°; nâng hạ toàn giường 520–770 mm; tải an toàn 175 kg; nguồn 100–240 V; chống nước IPX4. Hãng BIOBASE.'", "n:'BIOBASE MF301D-11 three-function electric bed', code:'MF301D-11', img:'https://img.waimaoniu.net/2587/2587-202511251715078673.jpg', d:'Size 2120 × 910 × 520–770 mm; back rest 0–70°, thigh 0–30°, calf 0–10°; overall height 520–770 mm; safe load 175 kg; power 100–240 V; IPX4. Manufacturer: BIOBASE.'", "n:'BIOBASE MF301D-11 三功能电动病床', code:'MF301D-11', img:'https://img.waimaoniu.net/2587/2587-202511251715078673.jpg', d:'尺寸 2120 × 910 × 520–770 mm；背板 0–70°，大腿板 0–30°，小腿板 0–10°；整床升降 520–770 mm；安全负载 175 kg；电源 100–240 V；防护等级 IPX4。制造商：BIOBASE。'"),
("n:'Hộp giảm tốc công nghiệp', code:'VP-CN-01', d:'Chế tạo, sửa chữa, thay thế theo yêu cầu kỹ thuật.'", "n:'Industrial gearbox', code:'VP-CN-01', d:'Fabrication, repair and replacement to technical requirements.'", "n:'工业减速机', code:'VP-CN-01', d:'按技术要求制造、维修与更换。'"),
("n:'Bơm và quạt công nghiệp', code:'VP-CN-02', d:'Cung cấp, lắp đặt, bảo dưỡng cho nhà máy, công trường.'", "n:'Industrial pumps and fans', code:'VP-CN-02', d:'Supply, installation and maintenance for plants and sites.'", "n:'工业泵与风机', code:'VP-CN-02', d:'为工厂及工地供货、安装与保养。'"),
("n:'Bộ điều khiển PLC', code:'VP-DT-01', d:'Tủ điều khiển, lập trình tự động hóa dây chuyền.'", "n:'PLC controller', code:'VP-DT-01', d:'Control panels and production-line automation programming.'", "n:'PLC控制器', code:'VP-DT-01', d:'控制柜及生产线自动化编程。'"),
("n:'Biến tần, khởi động mềm', code:'VP-DT-02', d:'Điều khiển tốc độ động cơ, tiết kiệm điện năng.'", "n:'Inverters, soft starters', code:'VP-DT-02', d:'Motor speed control and energy saving.'", "n:'变频器、软启动器', code:'VP-DT-02', d:'电机调速，节约电能。'"),
("n:'Cảm biến và thiết bị đo', code:'VP-DT-03', d:'Đo nhiệt độ, áp suất, mức, lưu lượng.'", "n:'Sensors and instruments', code:'VP-DT-03', d:'Temperature, pressure, level and flow measurement.'", "n:'传感器与测量仪器', code:'VP-DT-03', d:'测量温度、压力、液位、流量。'"),
("n:'Máy tính trạm, máy chủ', code:'VP-TH-01', d:'Cấu hình theo nhu cầu văn phòng, kỹ thuật.'", "n:'Workstations, servers', code:'VP-TH-01', d:'Configured for office and engineering needs.'", "n:'工作站、服务器', code:'VP-TH-01', d:'按办公及工程需求配置。'"),
("n:'Máy tính để bàn, xách tay', code:'VP-TH-02', d:'Cung cấp, cài đặt, bảo hành tận nơi.'", "n:'Desktops, laptops', code:'VP-TH-02', d:'Supply, setup and on-site warranty.'", "n:'台式机、笔记本电脑', code:'VP-TH-02', d:'供货、安装及上门保修。'"),
("n:'Camera và thiết bị mạng', code:'VP-TH-03', d:'Lắp đặt mạng LAN, camera cho văn phòng, nhà xưởng.'", "n:'Cameras and network equipment', code:'VP-TH-03', d:'LAN and camera installation for offices and factories.'", "n:'摄像机与网络设备', code:'VP-TH-03', d:'为办公室及厂房安装局域网与监控摄像机。'"),
("n:'Phần mềm bản quyền', code:'VP-TH-04', d:'Phần mềm văn phòng và chuyên ngành kỹ thuật.'", "n:'Licensed software', code:'VP-TH-04', d:'Office and engineering software.'", "n:'正版软件', code:'VP-TH-04', d:'办公及工程专业软件。'"),
("aria-label=\"Ảnh '+(k+1)+'\"", "aria-label=\"Slide '+(k+1)+'\"", "aria-label=\"第'+(k+1)+'张\""),
("name:'Sản phẩm',subs:[]", "name:'Products',subs:[]", "name:'产品',subs:[]"),
("aria-label=\"Mở danh mục con\"", "aria-label=\"Expand subcategories\"", "aria-label=\"展开子分类\""),
("(cat?cat.name:'Sản phẩm')", "(cat?cat.name:'Products')", "(cat?cat.name:'产品')"),
("list.length+' sản phẩm'+(query.trim()?' khớp với “'+query.trim()+'”':'')", "list.length+' products'+(query.trim()?' matching “'+query.trim()+'”':'')", "'共 '+list.length+' 个产品'+(query.trim()?'，匹配“'+query.trim()+'”':'')"),
('"/catalog/vi/', '"/catalog/en/', '"/catalog/zh/'),
('>Tải catalog PDF<', '>Catalog PDF<', '>产品资料 PDF<'),
('<a href="#lien-he">Liên hệ báo giá →</a>', '<a href="#lien-he">Request a quote →</a>', '<a href="#lien-he">询价 →</a>'),
("'<div class=\"empty\">Không tìm thấy sản phẩm phù hợp. Gọi 08.9999.0683 / 0986.818.013 để được tư vấn.</div>'", "'<div class=\"empty\">No matching products. Call +84 899 990 683 / +84 986 818 013 for advice.</div>'", "'<div class=\"empty\">未找到匹配的产品。请致电 +84 899 990 683 / +84 986 818 013 咨询。</div>'"),
("aria-label=\"Trang trước\"", "aria-label=\"Previous page\"", "aria-label=\"上一页\""),
("aria-label=\"Trang sau\"", "aria-label=\"Next page\"", "aria-label=\"下一页\""),
("alt=\"Trang '+(k+1)+'\"", "alt=\"Page '+(k+1)+'\"", "alt=\"第'+(k+1)+'页\""),
]

ALLOW = {  # Vietnamese text allowed to remain on translated pages
 "Tiếng Việt", "CÔNG TY TNHH KỸ THUẬT VÀ THƯƠNG MẠI VÂN PHONG",
}
VCH = re.compile(r"[ăâđêôơưàảãáạằẳẵắặầẩẫấậèẻẽéẹềểễếệìỉĩíịòỏõóọồổỗốộờởỡớợùủũúụừửữứựỳỷỹýỵ]", re.I)

def build(idx):
    s = VI
    for row in P:
        vi, tr = row[0], row[idx]
        if vi == '__PARTNERS__': vi, tr = _pb('vi'), _pb('en' if idx == 1 else 'zh')
        if vi == '__LEADERS__': vi, tr = _lb('vi'), _lb('en' if idx == 1 else 'zh')
        if vi == '__NEWS__': vi, tr = _nb('vi'), _nb('en' if idx == 1 else 'zh')
        if vi == '__PUBS__': vi, tr = _ub('vi'), _ub('en' if idx == 1 else 'zh')
        if vi == '__BB__': vi, tr = _bb('vi'), _bb('en' if idx == 1 else 'zh')
        if vi == '__PATENT__': vi, tr = _pt('vi'), _pt('en' if idx == 1 else 'zh')
        n = s.count(vi)
        if n == 0: sys.exit(f"MISSING: {vi[:70]}")
        s = s.replace(vi, tr)
    # leftover Vietnamese check (ignore allowed strings and the Vietnamese-only norm() regex line)
    chk = s
    for a in ALLOW: chk = chk.replace(a, "")
    bad = [l.strip()[:120] for l in chk.splitlines() if VCH.search(l) and "normalize('NFD')" not in l]
    return s, bad

for idx, code in ((1, "en"), (2, "zh")):
    out, bad = build(idx)
    (REPO / code).mkdir(exist_ok=True)
    (REPO / code / "index.html").write_text(out, encoding="utf-8")
    print(code, "leftover:", len(bad)); [print("  ", b) for b in bad]
