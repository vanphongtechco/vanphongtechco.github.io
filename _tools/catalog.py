# -*- coding: utf-8 -*-
# Vân Phong product datasheets (VI / EN / ZH), 1 page A4 each.
# Specs only from verified sources: contracts 105/106/107 VECA-VP, device label, Drawell quotation,
# Gongbei CRS1414 manual + spec sheet, CRS350-15 drawing.
import asyncio, html, re
from pathlib import Path
from playwright.async_api import async_playwright
e = html.escape
REPO = Path(__file__).resolve().parent.parent
import tempfile
CAT = Path(tempfile.gettempdir()) / "vp-cat"
OUT = REPO / "catalog"
SRC = (REPO / "index.html").read_text(encoding="utf-8")
def icon(k): return re.search(r"\b" + k + r":'(<svg.*?</svg>)'", SRC).group(1)

def S(*a):  # same value in all languages
    return a[0] if len(a) == 1 else a

L = {
 "vi": dict(lang="vi", tag="Kỹ thuật – Thương mại", ds="THÔNG TIN SẢN PHẨM", spec="Thông số kỹ thuật", feat="Đặc điểm nổi bật",
            app="Ứng dụng", sup="Cung cấp bao gồm", svc="Dịch vụ của Vân Phong", mfr="Hãng sản xuất", org="Xuất xứ",
            svcs=["Tư vấn lựa chọn cấu hình phù hợp nhu cầu", "Cung cấp chính hãng, đủ chứng từ CO, CQ", "Vận chuyển, lắp đặt, chạy thử, hướng dẫn sử dụng", "Bảo hành, bảo trì, sửa chữa, cung cấp vật tư thay thế"],
            note="Thông số theo tài liệu của nhà sản xuất và hồ sơ cung cấp thực tế; có thể thay đổi theo phiên bản. Vui lòng liên hệ để nhận cấu hình và báo giá chính xác.",
            co="CÔNG TY TNHH KỸ THUẬT VÀ THƯƠNG MẠI VÂN PHONG", addr="Số 34, ngõ 36A Trần Điền, P. Phương Liệt, TP. Hà Nội",
            hot="Hotline / Zalo: 08.9999.0683 / 0986.818.013", font="Inter"),
 "en": dict(lang="en", tag="Engineering – Trading", ds="PRODUCT DATASHEET", spec="Technical specifications", feat="Key features",
            app="Applications", sup="Scope of supply", svc="Van Phong services", mfr="Manufacturer", org="Origin",
            svcs=["Advice on the right configuration for your needs", "Genuine products with full CO/CQ documents", "Delivery, installation, commissioning and user training", "Warranty, maintenance, repair and spare parts"],
            note="Specifications are based on manufacturer documents and actual supply records and may change with the model version. Please contact us for the exact configuration and quotation.",
            co="VAN PHONG TECHNICAL AND TRADING CO., LTD.", addr="No. 34, Lane 36A Tran Dien, Phuong Liet Ward, Hanoi, Vietnam",
            hot="Hotline / WhatsApp: +84 899 990 683 / +84 986 818 013", font="Inter"),
 "zh": dict(lang="zh-CN", tag="技术 – 贸易", ds="产品资料", spec="技术参数", feat="产品特点",
            app="应用领域", sup="供货范围", svc="Van Phong 服务", mfr="制造商", org="产地",
            svcs=["根据需求提供配置选型咨询", "原厂正品，提供完整 CO/CQ 文件", "运输、安装、调试及操作培训", "保修、维护、维修及备件供应"],
            note="参数依据制造商资料及实际供货文件，可能随型号版本变化。请联系我们获取准确配置及报价。",
            co="VAN PHONG 技术与贸易有限公司", addr="越南河内市方烈坊陈田36A巷34号",
            hot="热线 / WhatsApp：+84 899 990 683 / +84 986 818 013", font="Noto Sans CJK SC"),
}

# rows: (label_vi, label_en, label_zh, value) ; value str or (vi,en,zh)
P = [
dict(slug="crs1414", code="CRS1414", icon="screen",
 name=("Sàng đĩa đan xen CRS1414", "CRS1414 Interlaced Disc Roller Screen", "CRS1414 交错盘式滚轴筛"),
 mfr=("Gongbei Heavy Machinery", "Gongbei Heavy Machinery", "石家庄功倍重型机械"), org=("Trung Quốc", "China", "中国"),
 lead=("Sàng phân loại than năng suất 150 t/h, 14 trục đĩa đan xen, cho cỡ hạt dưới sàng ≤ 8 mm; làm việc ổn định với than ẩm, dính. Vân Phong tư vấn tính toán, lựa chọn thiết bị cho chủ đầu tư.",
       "150 t/h coal classifying screen with 14 interlaced disc shafts and ≤ 8 mm undersize; stable with wet and sticky coal. Van Phong provided sizing calculations and equipment selection for the project owner.",
       "处理量 150 t/h 的煤炭分级筛，14 根交错盘轴，筛下粒度 ≤ 8 mm，适用于潮湿、黏性煤料。Van Phong 为业主提供计算选型咨询。"),
 rows=[("Năng suất", "Capacity", "处理能力", "150 t/h"),
       ("Số trục sàng", "Number of shafts", "筛轴数量", "14"),
       ("Chiều rộng mặt sàng", "Screen width", "筛面宽度", "1400 mm"),
       ("Cỡ hạt cấp liệu", "Feed size", "入料粒度", "≤ 200 mm"),
       ("Cỡ hạt dưới sàng", "Undersize (discharge)", "筛下粒度", "≤ 8 mm"),
       ("Động cơ", "Motors", "电机", ("14 × 3,0 kW", "14 × 3.0 kW", "14 × 3.0 kW")),
       ("Tốc độ trục", "Shaft speed", "轴转速", ("85 vòng/phút", "85 rpm", "85 r/min")),
       ("Hiệu suất sàng", "Screening efficiency", "筛分效率", ("≥ 80 – 85 % (tùy độ ẩm)", "≥ 80 – 85 % (depending on moisture)", "≥ 80 – 85 %（视含水率）")),
       ("Kích thước (D × R × C)", "Dimensions (L × W × H)", "外形尺寸（长×宽×高）", "3740 × 2587 × 1555 mm"),
       ("Khối lượng", "Weight", "重量", ("≈ 10 000 kg", "≈ 10,000 kg", "约 10,000 kg"))],
 feat=(["Đĩa sàng hợp kim chịu mài mòn, tuổi thọ cao", "Hộp giảm tốc bánh răng tôi cứng, vận hành ổn định", "Có lược làm sạch, chống bết dính, tắc lưới", "Kết cấu thấp, gọn, dễ bố trí vào dây chuyền sẵn có"],
       ["Wear-resistant alloy discs for long service life", "Hard-tooth-surface gear reducers for stable operation", "Cleaning combs prevent clogging with sticky material", "Low, compact frame that fits existing lines"],
       ["耐磨合金筛盘，使用寿命长", "硬齿面减速机，运行平稳", "配清理梳，防止黏料堵塞", "结构低矮紧凑，便于改造现有生产线"]),
 app=("Than nguyên khai, than cho nhà máy nhiệt điện, quặng bauxite. 01 thiết bị cấp cho hệ thống sàng – nghiền than Phân xưởng Nhiệt điện – Công ty Nhôm Lâm Đồng – TKV.",
      "Raw coal, power-plant coal and bauxite. One unit supplied for the coal screening and crushing system of the Thermal Power Workshop, Lam Dong Aluminum Company – TKV.",
      "原煤、电厂动力煤及铝土矿。为林同铝业公司（TKV）热电车间煤炭筛分–破碎系统供应 1 台。"), sup=None),
dict(slug="crs350-15", code="CRS350-15", icon="screen",
 name=("Sàng đĩa đan xen CRS350-15", "CRS350-15 Interlaced Disc Roller Screen", "CRS350-15 交错盘式滚轴筛"),
 mfr=("Gongbei Heavy Machinery", "Gongbei Heavy Machinery", "石家庄功倍重型机械"), org=("Trung Quốc", "China", "中国"),
 lead=("Sàng phân loại than năng suất 350 t/h, cỡ hạt cấp liệu 150 mm, phân cấp 15 mm. Vân Phong tư vấn tính toán, lựa chọn thiết bị cho chủ đầu tư.",
       "350 t/h coal classifying screen, 150 mm feed, 15 mm cut size. Van Phong provided sizing calculations and equipment selection for the project owner.",
       "处理量 350 t/h 的煤炭分级筛，入料 150 mm，分级粒度 15 mm。Van Phong 为业主提供计算选型咨询。"),
 rows=[("Vật liệu sàng", "Material", "物料", ("Than", "Coal", "煤")),
       ("Năng suất", "Capacity", "处理能力", "350 t/h"),
       ("Cỡ hạt cấp liệu", "Feed size", "入料粒度", "≤ 150 mm"),
       ("Cỡ hạt dưới sàng", "Undersize", "筛下粒度", "15 mm"),
       ("Động cơ", "Motors", "电机", ("3 × 7,5 kW", "3 × 7.5 kW", "3 × 7.5 kW")),
       ("Kích thước mặt bằng", "Footprint", "占地尺寸", "3830 × 1550 mm"),
       ("Chiều cao", "Height", "高度", "1550 mm")],
 feat=(["Đĩa sàng đan xen tự làm sạch, không bết dính", "Truyền động nhóm, ít động cơ, dễ bảo trì", "Chiều cao thấp, thay thế sàng rung không cần cải tạo lớn", "Thiết kế theo điều kiện thực tế từng mỏ"],
       ["Self-cleaning interlaced discs, no blinding", "Group drive: few motors, easy maintenance", "Low height: replaces vibrating screens with minimal rework", "Designed for actual site conditions"],
       ["交错筛盘自清理，不糊筛", "分组驱动，电机少，维护方便", "高度低，可直接替换振动筛", "按矿山实际工况设计"]),
 app=("Sàng phân loại than tại mỏ và nhà máy tuyển. Phương án tư vấn cho Công ty CP Than Vàng Danh – Vinacomin.",
      "Coal classification at mines and preparation plants. Solution proposed for Vang Danh Coal JSC – Vinacomin.",
      "矿山及选煤厂煤炭分级。为 Vang Danh 煤炭股份公司（Vinacomin）提供的咨询方案。"), sup=None),
dict(slug="bk-fd10p", code="BK-FD10P", icon="freeze",
 name=("Máy đông khô BK-FD10P (-60°C)", "BK-FD10P Freeze Dryer (-60°C)", "BK-FD10P 冻干机（-60°C）"),
 mfr=("BIOBASE", "BIOBASE", "BIOBASE（博科）"), org=("Trung Quốc", "China", "中国"),
 lead=("Máy đông khô phòng thí nghiệm, buồng tiêu chuẩn kèm giá 8 nhánh, bẫy lạnh đến -60°C.",
       "Laboratory freeze dryer with standard chamber, 8-port manifold and -60°C cold trap.",
       "实验室冻干机，标准型冻干室，8 口歧管，冷阱温度 -60°C。"),
 rows=[("Nhiệt độ bẫy lạnh", "Cold trap temperature", "冷阱温度", ("≤ -60°C (không tải)", "≤ -60°C (no load)", "≤ -60°C（空载）")),
       ("Dung tích bẫy lạnh", "Cold trap capacity", "冷阱容量", ("6 lít", "6 L", "6 L")),
       ("Kích thước bẫy lạnh", "Cold trap size", "冷阱尺寸", "Φ219 × 140 mm"),
       ("Khả năng giữ đá", "Ice capacity", "捕水能力", ("3 – 4 lít/24 h", "3 – 4 L/24 h", "3 – 4 L/24 h")),
       ("Độ chân không", "Vacuum", "真空度", "< 5 Pa"),
       ("Diện tích làm lạnh", "Shelf area", "冻干面积", ("0,12 m²", "0.12 m²", "0.12 m²")),
       ("Khay", "Trays", "托盘", ("4 khay Φ200 × 20 mm, cách nhau 50 mm", "4 × Φ200 × 20 mm, 50 mm spacing", "4 个 Φ200 × 20 mm，间距 50 mm")),
       ("Tải tiêu chuẩn", "Standard load", "标准装载量", ("1,2 lít", "1.2 L", "1.2 L")),
       ("Buồng đông khô", "Drying chamber", "冻干室", "Φ260 × 465 mm"),
       ("Thời gian sấy", "Drying time", "干燥时间", ("24 – 36 h/mẻ", "24 – 36 h/batch", "24 – 36 h/批")),
       ("Môi chất lạnh", "Refrigerant", "制冷剂", "R600a + R23"),
       ("Nguồn điện / công suất", "Power supply / power", "电源 / 功率", ("220 V, 50/60 Hz / 1,3 kW", "220 V, 50/60 Hz / 1.3 kW", "220 V，50/60 Hz / 1.3 kW")),
       ("Kích thước máy (R × S × C)", "Dimensions (W × D × H)", "外形尺寸（宽×深×高）", "640 × 610 × 550 mm")],
 feat=None,
 app=("Đông khô mẫu sinh học, vi sinh, thực phẩm, dược phẩm trong phòng thí nghiệm, viện nghiên cứu, trường đại học.",
      "Freeze drying of biological, microbial, food and pharmaceutical samples in laboratories, institutes and universities.",
      "适用于实验室、科研院所和高校的生物、微生物、食品、药品样品冻干。"),
 sup=(["Máy chính kèm buồng đông khô, 4 khay", "Giá để bình đông khô: 4 cái", "Bơm chân không 2 lít/giây", "Bộ bình: 100/200/250/500 ml × 2 mỗi loại + 8 van", "Tài liệu hướng dẫn sử dụng"],
      ["Main unit with drying chamber and 4 trays", "Flask racks: 4", "Vacuum pump 2 L/s", "Flasks 100/200/250/500 ml × 2 each + 8 valves", "User manual"],
      ["主机及冻干室，4 个托盘", "冻干瓶架 4 个", "真空泵 2 L/s", "冻干瓶 100/200/250/500 ml 各 2 个 + 8 个阀门", "使用说明书"])),
dict(slug="bbs-h1500", code="BBS-H1500", icon="bench",
 name=("Tủ cấy vi sinh BBS-H1500", "BBS-H1500 Clean Bench", "BBS-H1500 超净工作台"),
 mfr=("BIOBASE", "BIOBASE", "BIOBASE（博科）"), org=("Trung Quốc", "China", "中国"),
 lead=("Tủ cấy vi sinh khổ lớn 1,5 m, lọc HEPA 99,995 %, cấp sạch ISO 5, màn hình LCD.",
       "1.5 m clean bench with 99.995 % HEPA filtration, ISO 5 cleanliness and LCD display.",
       "1.5 米超净工作台，HEPA 过滤效率 99.995 %，ISO 5 洁净度，LCD 显示。"),
 rows=[("Kích thước ngoài (R × S × C)", "External size (W × D × H)", "外部尺寸（宽×深×高）", "1500 × 810 × 1740 mm"),
       ("Buồng thao tác (R × S × C)", "Work zone (W × D × H)", "工作区（宽×深×高）", "1400 × 550 × 600 mm"),
       ("Chiều cao mặt làm việc", "Work surface height", "台面高度", "800 mm"),
       ("Tốc độ dòng khí", "Air velocity", "风速", ("0,3 – 0,45 m/s", "0.3 – 0.45 m/s", "0.3 – 0.45 m/s")),
       ("Lọc HEPA", "HEPA filter", "HEPA 过滤器", ("99,995 % @ 0,3 μm", "99.995 % @ 0.3 μm", "99.995 % @ 0.3 μm")),
       ("Cấp sạch", "Cleanliness", "洁净等级", "ISO 5 (Class 100)"),
       ("Khuẩn lạc", "Colony count", "沉降菌", ("≤ 0,5 CFU/30 phút", "≤ 0.5 CFU/30 min", "≤ 0.5 CFU/30 min")),
       ("Độ ồn / độ sáng / độ rung", "Noise / light / vibration", "噪音 / 照度 / 振动", "≤ 65 dB(A) / ≥ 300 lux / ≤ 5 μm"),
       ("Vật liệu", "Construction", "材质", ("Thân thép sơn kháng khuẩn; mặt bàn inox 304; kính cường lực 8 mm chống UV", "Antibacterial-coated steel body; SUS 304 worktop; 8 mm UV-blocking tempered glass", "抗菌喷涂钢板箱体；304 不锈钢台面；8 mm 防紫外钢化玻璃")),
       ("Ổ cắm chống nước", "Waterproof sockets", "防水插座", ("2 ổ, tổng 1000 W", "2, max. 1000 W", "2 个，最大 1000 W")),
       ("Nguồn điện / công suất", "Power supply / power", "电源 / 功率", ("220 V ± 10 %, 50/60 Hz / 1250 W", "220 V ± 10 %, 50/60 Hz / 1250 W", "220 V ± 10 %，50/60 Hz / 1250 W")),
       ("Khối lượng", "Weight", "重量", "216 kg")],
 feat=None,
 app=("Thao tác vô trùng: nuôi cấy vi sinh, cấy mô, chuẩn bị mẫu trong phòng thí nghiệm, bệnh viện, nhà máy thực phẩm – dược phẩm.",
      "Aseptic work: microbial culture, tissue culture and sample preparation in labs, hospitals and food/pharma plants.",
      "无菌操作：微生物培养、组织培养及样品制备，适用于实验室、医院及食品药品工厂。"),
 sup=(["Tủ cấy kèm chân tủ đồng bộ", "Bộ lọc HEPA lắp sẵn", "2 đèn UV, 1 đèn LED", "2 ổ cắm chống nước", "Tài liệu hướng dẫn sử dụng"],
      ["Bench with matching stand", "Pre-installed HEPA filter", "2 UV lamps, 1 LED lamp", "2 waterproof sockets", "User manual"],
      ["工作台及配套底座", "预装 HEPA 过滤器", "2 支紫外灯，1 支 LED 灯", "2 个防水插座", "使用说明书"])),
dict(slug="bkcb-v900", code="BKCB-V900", icon="bench",
 name=("Tủ cấy vi sinh BKCB-V900", "BKCB-V900 Vertical Clean Bench", "BKCB-V900 垂直流超净工作台"),
 mfr=("BIOBASE", "BIOBASE", "BIOBASE（博科）"), org=("Trung Quốc", "China", "中国"),
 lead=("Tủ cấy vi sinh dòng khí thổi đứng, lọc HEPA H14, cấp sạch ISO 5, gọn cho phòng thí nghiệm nhỏ.",
       "Vertical laminar-flow clean bench with H14 HEPA filter and ISO 5 cleanliness, compact for small labs.",
       "垂直层流超净工作台，H14 HEPA 过滤器，ISO 5 洁净度，适合小型实验室。"),
 rows=[("Kiểu dòng khí", "Airflow", "气流方式", ("Thổi đứng", "Vertical", "垂直流")),
       ("Kích thước ngoài (R × S × C)", "External size (W × D × H)", "外部尺寸（宽×深×高）", "900 × 630 × 1760 mm"),
       ("Kích thước trong (R × S × C)", "Internal size (W × D × H)", "内部尺寸（宽×深×高）", "800 × 515 × 550 mm"),
       ("Chiều cao mặt làm việc", "Work surface height", "台面高度", "750 mm"),
       ("Độ mở an toàn / tối đa", "Safe / max. opening", "安全 / 最大开口", "200 / 350 mm"),
       ("Tốc độ dòng khí", "Air velocity", "风速", ("0,2 – 0,45 m/s", "0.2 – 0.45 m/s", "0.2 – 0.45 m/s")),
       ("Lọc HEPA", "HEPA filter", "HEPA 过滤器", ("H14, ≥ 99,995 % @ 0,3 μm", "H14, ≥ 99.995 % @ 0.3 μm", "H14，≥ 99.995 % @ 0.3 μm")),
       ("Cấp sạch", "Cleanliness", "洁净等级", "ISO 5 (Class 100)"),
       ("Khuẩn lạc", "Colony count", "沉降菌", ("≤ 0,5 CFU/30 phút", "≤ 0.5 CFU/30 min", "≤ 0.5 CFU/30 min")),
       ("Độ ồn / độ sáng / độ rung", "Noise / light / vibration", "噪音 / 照度 / 振动", "≤ 65 dB(A) / ≥ 300 lux / ≤ 5 μm"),
       ("Quạt", "Fan motor", "风机", ("120 W, 2450 vòng/phút", "120 W, 2450 rpm", "120 W，2450 r/min")),
       ("Nguồn điện", "Power supply", "电源", ("220 V ± 10 %, 50 Hz", "220 V ± 10 %, 50 Hz", "220 V ± 10 %，50 Hz"))],
 feat=None,
 app=("Thao tác vô trùng cho phòng thí nghiệm vi sinh, sinh học, trường học, cơ sở y tế.",
      "Aseptic work in microbiology and biology labs, schools and healthcare facilities.",
      "适用于微生物及生物实验室、学校和医疗机构的无菌操作。"),
 sup=(["Tủ cấy kèm chân", "2 đèn UV, 1 đèn LED", "Tài liệu hướng dẫn sử dụng"],
      ["Bench with stand", "2 UV lamps, 1 LED lamp", "User manual"],
      ["工作台及底座", "2 支紫外灯，1 支 LED 灯", "使用说明书"])),
dict(slug="os20-pro", code="OS20-Pro", icon="stirrer",
 name=("Máy khuấy đũa cơ học OS20-Pro", "OS20-Pro Overhead Stirrer", "OS20-Pro 顶置式搅拌器"),
 mfr=("Drawell", "Drawell", "Drawell"), org=("Trung Quốc", "China", "中国"),
 lead=("Máy khuấy đũa động cơ DC không chổi than, 50 – 2200 vòng/phút, hiển thị LCD tốc độ và mô-men, khuấy tới 20 lít.",
       "Brushless DC overhead stirrer, 50 – 2200 rpm, LCD speed and torque display, up to 20 L.",
       "无刷直流电机顶置式搅拌器，50 – 2200 r/min，LCD 显示转速和扭矩，最大搅拌量 20 L。"),
 rows=[("Thể tích khuấy tối đa (H₂O)", "Max. stirring volume (H₂O)", "最大搅拌量（水）", ("20 lít", "20 L", "20 L")),
       ("Động cơ", "Motor", "电机", ("DC không chổi than; vào 60 W / ra 50 W", "Brushless DC; input 60 W / output 50 W", "无刷直流；输入 60 W / 输出 50 W")),
       ("Dải tốc độ", "Speed range", "转速范围", ("50 – 2200 vòng/phút", "50 – 2200 rpm", "50 – 2200 r/min")),
       ("Độ chính xác hiển thị", "Display accuracy", "显示精度", ("± 3 vòng/phút", "± 3 rpm", "± 3 r/min")),
       ("Hiển thị", "Display", "显示", ("LCD tốc độ và mô-men", "LCD speed and torque", "LCD 转速和扭矩")),
       ("Mô-men xoắn tối đa", "Max. torque", "最大扭矩", "40 Ncm"),
       ("Độ nhớt tối đa", "Max. viscosity", "最大粘度", "10 000 mPas"),
       ("Đầu kẹp", "Chuck range", "夹头范围", ("0,5 – 10 mm", "0.5 – 10 mm", "0.5 – 10 mm")),
       ("Bảo vệ", "Protection", "保护", ("Báo quá tải LED; IP21", "LED overload alarm; IP21", "LED 过载提示；IP21")),
       ("Nguồn điện / công suất", "Power supply / power", "电源 / 功率", ("100 – 220 VAC, 50 Hz / 70 W", "100 – 220 VAC, 50 Hz / 70 W", "100 – 220 VAC，50 Hz / 70 W")),
       ("Kích thước / khối lượng", "Dimensions / weight", "尺寸 / 重量", ("83 × 220 × 186 mm / 2,8 kg", "83 × 220 × 186 mm / 2.8 kg", "83 × 220 × 186 mm / 2.8 kg"))],
 feat=None,
 app=("Khuấy trộn, hòa tan, phản ứng hóa học trong phòng thí nghiệm hóa học, vật liệu, thực phẩm, dược phẩm.",
      "Mixing, dissolving and chemical reactions in chemistry, materials, food and pharmaceutical labs.",
      "适用于化学、材料、食品、医药实验室的混合、溶解及化学反应。"),
 sup=(["Máy khuấy chính", "Cánh khuấy PTFE, trục 35 cm", "Cánh khuấy chữ thập inox 316L, trục 40 cm", "Giá đỡ: đế 20 × 31 cm, cần 78 cm"],
      ["Main stirrer unit", "PTFE stirring paddle, 35 cm shaft", "SUS 316L cross stirrer, 40 cm shaft", "Stand: 20 × 31 cm base, 78 cm rod"],
      ["搅拌器主机", "PTFE 搅拌桨，杆长 35 cm", "316L 不锈钢十字搅拌桨，杆长 40 cm", "支架：底座 20 × 31 cm，立杆 78 cm"])),
]
IDX = {"vi": 0, "en": 1, "zh": 2}

CSS = """@page{size:A4;margin:0}
*{box-sizing:border-box}
body{margin:0;font-family:"%s","Inter","Noto Sans CJK SC",Arial,sans-serif;color:#1d2733;font-size:9.6pt;line-height:1.45}
.pg{width:210mm;height:297mm;position:relative;padding:0 15mm}
.hd{display:flex;justify-content:space-between;align-items:center;padding:9mm 0 5mm;border-bottom:2.2pt solid #1580BF}
.hd img{height:12mm}.hd .t{text-align:right;color:#0E2A47;font-weight:700;font-size:9pt;letter-spacing:.06em}.hd .t span{display:block;color:#F07C1B;font-weight:600;letter-spacing:0}
.hero{display:grid;grid-template-columns:1fr 40mm;gap:8mm;margin:6mm 0 3mm;align-items:center}
.code{display:inline-block;background:#0E2A47;color:#fff;font-weight:700;padding:1mm 3mm;font-size:9pt;border-radius:1mm}
h1{font-size:19pt;line-height:1.2;margin:2.5mm 0 2mm;color:#0E2A47}
.meta{color:#555;font-size:9pt}.meta b{color:#1d2733}
.lead{margin-top:3mm;font-size:10.5pt;color:#283746}
.ic{width:40mm;height:40mm;border-radius:3mm;background:linear-gradient(135deg,#EAF4FB,#D5E8F5);display:grid;place-items:center;color:#1580BF}
.ic svg{width:26mm;height:26mm}
.hero:has(.ph){grid-template-columns:1fr 56mm}.ic.ph{width:56mm;height:56mm;background:#fff;border:.5pt solid #dde6ee}.ic.ph img{width:100%%;height:100%%;object-fit:contain;padding:1.5mm}
h2{font-size:11pt;color:#1580BF;margin:4mm 0 1.6mm;padding-bottom:1mm;border-bottom:.6pt solid #cfdbe6;text-transform:uppercase;letter-spacing:.03em}
table{width:100%%;border-collapse:collapse}
td{padding:1.15mm 2.5mm;border-bottom:.5pt solid #e3e9ef;vertical-align:top}
tr:nth-child(odd) td{background:#F5F8FB}
td:first-child{width:62mm;color:#4a5866;font-weight:600}
.two{display:grid;grid-template-columns:1fr 1fr;gap:8mm}
ul{margin:0;padding-left:4.5mm}li{margin:.6mm 0}
p{margin:0}
.note{margin-top:5mm;font-size:8pt;color:#6b7785;font-style:italic}
.ft{position:absolute;left:0;right:0;bottom:0;background:#0E2A47;color:#fff;padding:5mm 15mm;font-size:8.6pt;display:flex;justify-content:space-between;gap:6mm}
.ft b{display:block;font-size:9pt}.ft>div:first-child{flex:1.4}.ft .r{white-space:nowrap}.ft .r{text-align:right;color:#cfe3f3}
"""

def pic(p):
    f = REPO / "anh-san-pham" / f"{p['slug']}.jpg"
    if f.exists(): return f'<div class="ic ph"><img src="file://{f}"></div>'
    return f'<div class="ic">{icon(p["icon"])}</div>'

def val(v, i): return v if isinstance(v, str) else v[i]

def doc(p, k):
    t, i = L[k], IDX[k]
    rows = "".join(f"<tr><td>{e(r[i])}</td><td>{e(val(r[3], i))}</td></tr>" for r in p["rows"])
    blocks = []
    if p.get("feat"): blocks.append((t["feat"], "<ul>" + "".join(f"<li>{e(x)}</li>" for x in p["feat"][i]) + "</ul>"))
    if p.get("sup"): blocks.append((t["sup"], "<ul>" + "".join(f"<li>{e(x)}</li>" for x in p["sup"][i]) + "</ul>"))
    blocks.append((t["svc"], "<ul>" + "".join(f"<li>{e(x)}</li>" for x in t["svcs"]) + "</ul>"))
    two = "".join(f"<div><h2>{e(h)}</h2>{b}</div>" for h, b in blocks[:2])
    rest = "".join(f"<h2>{e(h)}</h2>{b}" for h, b in blocks[2:])
    return f"""<!doctype html><html lang="{t['lang']}"><head><meta charset="utf-8"><style>{CSS % t['font']}</style></head><body><div class="pg">
<div class="hd"><img src="file://{REPO}/logo.png"><div class="t">{e(t['ds'])}<span>{e(t['tag'])}</span></div></div>
<div class="hero"><div><span class="code">{e(p['code'])}</span><h1>{e(p['name'][i])}</h1>
{f'<div class="meta">{e(t["mfr"])}: <b>{e(p["mfr"][i])}</b> · {e(t["org"])}: <b>{e(p["org"][i])}</b></div>' if p['mfr'] else ''}
<p class="lead">{e(p['lead'][i])}</p></div>{pic(p)}</div>
<h2>{e(t['spec'])}</h2><table>{rows}</table>
<h2>{e(t['app'])}</h2><p>{e(p['app'][i])}</p>
<div class="two">{two}</div>{rest}
<p class="note">{e(t['note'])}</p>
<div class="ft"><div><b>{e(t['co'])}</b>{e(t['addr'])}</div><div class="r">{e(t['hot'])}<br>info@vanphongtechco.com.vn · www.vanphongtechco.com.vn</div></div>
</div></body></html>"""

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        for k in L:
            (OUT / k).mkdir(parents=True, exist_ok=True)
            for p in P:
                h = CAT / f"{p['slug']}-{k}.html"; h.parent.mkdir(exist_ok=True)
                h.write_text(doc(p, k), encoding="utf-8")
                pg = await b.new_page(); await pg.goto(h.as_uri())
                pdf = OUT / k / f"{p['slug']}.pdf"
                await pg.pdf(path=str(pdf), format="A4", print_background=True, prefer_css_page_size=True)
                await pg.set_viewport_size({"width": 794, "height": 1123})
                await pg.screenshot(path=f"{CAT}/{p['slug']}-{k}.png", full_page=True)
                await pg.close()
        await b.close()
if __name__ == "__main__":
    asyncio.run(main())
