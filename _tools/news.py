# -*- coding: utf-8 -*-
import re, unicodedata
# News items (Tin tức), newest first.
N = [dict(
  video="/video/biobase-kit-tach-chiet-dr1110.mp4", img="/video/biobase-kit-tach-chiet-dr1110.jpg", vw=720, vh=1280, date={"vi": "13/11/2026", "en": "13 November 2026", "zh": "2026年11月13日"},
  tag={"vi": "Sinh học phân tử", "en": "Molecular biology", "zh": "分子生物学"},
  title={"vi": "Kit tách chiết axit nucleic BIOBASE phương pháp hạt từ — DNA/RNA tinh sạch cho PCR, RT-PCR", "en": "BIOBASE magnetic-bead nucleic acid extraction kits — purified DNA/RNA for PCR and RT-PCR", "zh": "BIOBASE 磁珠法核酸提取试剂盒 —— 为 PCR、RT-PCR 提供纯化 DNA/RNA"},
  intro={"vi": ["Làm PCR, bạn đã chọn đúng kit tách chiết DNA/RNA chưa? Vân Phong giới thiệu bộ kit tách chiết axit nucleic BIOBASE theo phương pháp hạt từ — hỗ trợ thu nhận DNA/RNA tinh sạch để sử dụng trong các bước phân tích tiếp theo như PCR và RT-PCR.", "Những điểm đáng chú ý:"], "en": ["Doing PCR — have you chosen the right DNA/RNA extraction kit? Van Phong introduces BIOBASE magnetic-bead nucleic acid extraction kits, which help obtain purified DNA/RNA for downstream analysis such as PCR and RT-PCR.", "Highlights:"], "zh": ["做 PCR，您选对 DNA/RNA 提取试剂盒了吗？Vân Phong 为您介绍 BIOBASE 磁珠法核酸提取试剂盒，可获得纯化的 DNA/RNA，用于 PCR、RT-PCR 等后续分析。", "产品亮点："]},
  bullets=True,
  items={'vi': [('', 'Kết hợp hạt từ và hệ dung dịch đệm để tách chiết, tinh sạch axit nucleic.'), ('', 'Nhiều quy cách đóng gói, phù hợp với nhu cầu xử lý mẫu.'), ('', 'Dòng DR1110 quy cách 32T/kit và 64T/kit, tương thích với máy tách chiết BIOBASE BK-HS32 và BK-AutoHS96.')], 'en': [('', 'Magnetic beads combined with a buffer system for nucleic acid extraction and purification.'), ('', 'Several pack sizes to suit different sample-processing needs.'), ('', 'DR1110 series in 32T/kit and 64T/kit packs, compatible with BIOBASE BK-HS32 and BK-AutoHS96 extractors.')], 'zh': [('', '磁珠与缓冲液体系结合，用于核酸提取与纯化。'), ('', '多种包装规格，满足不同样品处理需求。'), ('', 'DR1110 系列提供 32T/盒和 64T/盒规格，适配 BIOBASE BK-HS32 和 BK-AutoHS96 核酸提取仪。')]},
  outro={"vi": "Tư vấn, nhận catalogue, báo giá: Ms Ngọc Trâm – 0986.818.013 (Zalo).", "en": "Advice, catalogue and quotations: Ms Ngoc Tram – +84 986 818 013 (Zalo).", "zh": "咨询、索取样本与报价：Ngọc Trâm 女士 – +84 986 818 013（Zalo）。"},
  links={"vi": [("Xem sản phẩm", "/san-pham/bo-kit-tach-chiet-axit-nucleic-phuong-phap-hat-tu-biobase-dr1110-dr1127-dr1136/")], "en": [("View product", "/en/san-pham/bo-kit-tach-chiet-axit-nucleic-phuong-phap-hat-tu-biobase-dr1110-dr1127-dr1136/")], "zh": [("查看产品", "/zh/san-pham/bo-kit-tach-chiet-axit-nucleic-phuong-phap-hat-tu-biobase-dr1110-dr1127-dr1136/")]},
  cta={"vi": "Liên hệ tư vấn", "en": "Contact us", "zh": "联系咨询"},
), dict(
  video="/video/biobase-mx-rd.mp4", img="/video/biobase-mx-rd.jpg", vw=1280, vh=720, date={"vi": "13/11/2026", "en": "13 November 2026", "zh": "2026年11月13日"},
  tag={"vi": "Thiết bị phòng thí nghiệm", "en": "Laboratory equipment", "zh": "实验室设备"},
  title={"vi": "Máy lắc xoay BIOBASE dòng MX-RD — Trộn mẫu đồng đều, kết quả đáng tin cậy", "en": "BIOBASE MX-RD series rotator — uniform mixing, reliable results", "zh": "BIOBASE MX-RD 系列旋转混匀仪 —— 混匀均匀，结果可靠"},
  intro={"vi": ["Trong các xét nghiệm hóa học, sinh học và môi trường, mẫu được trộn đồng đều là điều kiện tiên quyết để kết quả phân tích phản ánh đúng bản chất của mẫu. Máy lắc xoay BIOBASE dòng MX-RD là thiết bị phòng thí nghiệm đa năng, trộn đồng đều chất lỏng, bột và huyền phù bằng chuyển động xoay tròn nhẹ nhàng, ổn định.", "Thông số kỹ thuật chính:"], "en": ["In chemical, biological and environmental testing, thoroughly mixed samples are a prerequisite for results that truly reflect the sample. The BIOBASE MX-RD series rotator is a versatile laboratory instrument that mixes liquids, powders and suspensions uniformly through gentle, steady rotation.", "Main specifications:"], "zh": ["在化学、生物和环境检测中，样品混合均匀是分析结果真实反映样品本质的前提。BIOBASE MX-RD 系列旋转混匀仪是一款多功能实验室设备，以轻柔、平稳的旋转运动均匀混合液体、粉末和悬浮液。", "主要技术参数："]},
  bullets=True,
  items={'vi': [('', 'MX-RD-Pro: dải tốc độ 10–70 vòng/phút; góc trộn điều chỉnh 0–90°; hẹn giờ 1–1199 phút, vận hành liên tục hoặc theo thời gian hẹn; màn hình LCD hiển thị tốc độ và thời gian; đĩa trộn và kẹp giữ ống bằng thép không gỉ; công suất 40 W.'), ('', 'MX-RD-E: dải tốc độ điều chỉnh 0–80 vòng/phút; vận hành liên tục; công suất 20 W; đĩa trộn thép không gỉ phủ oxy hóa; cấp bảo vệ IP21.'), ('', 'Nguồn điện AC 100–240 V, 50/60 Hz, phù hợp nhiều điều kiện lưới điện.'), ('', 'Phụ kiện đa dạng, tương thích nhiều cỡ ống nghiệm, đáp ứng linh hoạt từng quy trình trộn mẫu.'), ('', 'Dùng cho xét nghiệm hóa học, sinh học, môi trường; trộn máu, nuôi cấy huyền phù tế bào và các quy trình chuẩn bị mẫu thường quy.')], 'en': [('', 'MX-RD-Pro: speed 10–70 rpm; adjustable mixing angle 0–90°; timer 1–1199 min, continuous or timed operation; LCD showing speed and time; stainless steel mixing disc and tube clamps; 40 W.'), ('', 'MX-RD-E: adjustable speed 0–80 rpm; continuous operation; 20 W; oxidation-coated stainless steel mixing disc; IP21 protection.'), ('', 'Power supply AC 100–240 V, 50/60 Hz, suitable for a wide range of mains conditions.'), ('', 'A wide choice of accessories fitting many tube sizes, adaptable to each mixing procedure.'), ('', 'For chemical, biological and environmental testing; blood mixing, cell suspension culture and routine sample preparation.')], 'zh': [('', 'MX-RD-Pro：转速 10–70 rpm；混匀角度 0–90° 可调；定时 1–1199 分钟，可连续或定时运行；LCD 显示转速和时间；不锈钢混匀盘及试管夹；功率 40 W。'), ('', 'MX-RD-E：转速 0–80 rpm 可调；连续运行；功率 20 W；氧化涂层不锈钢混匀盘；防护等级 IP21。'), ('', '电源 AC 100–240 V，50/60 Hz，适应多种电网条件。'), ('', '配件丰富，兼容多种规格试管，灵活满足不同混匀流程。'), ('', '适用于化学、生物、环境检测；血液混匀、细胞悬浮培养及常规样品前处理。')]},
  outro={"vi": "Ứng dụng: trường đại học, viện nghiên cứu, bệnh viện, phòng thí nghiệm và khu công nghiệp. Tư vấn, nhận catalogue, báo giá: Ms Ngọc Trâm – 0986.818.013 (Zalo).", "en": "Applications: universities, research institutes, hospitals, laboratories and industrial parks. Advice, catalogue and quotations: Ms Ngoc Tram – +84 986 818 013 (Zalo).", "zh": "应用：高校、科研院所、医院、实验室和工业园区。 咨询、索取样本与报价：Ngọc Trâm 女士 – +84 986 818 013（Zalo）。"},
  links={"vi": [("Xem sản phẩm", "/san-pham/may-lac-xoay-biobase-dong-mx-rd-mx-rd-pro-mx-rd-e-bk-rd20/")], "en": [("View product", "/en/san-pham/may-lac-xoay-biobase-dong-mx-rd-mx-rd-pro-mx-rd-e-bk-rd20/")], "zh": [("查看产品", "/zh/san-pham/may-lac-xoay-biobase-dong-mx-rd-mx-rd-pro-mx-rd-e-bk-rd20/")]},
  cta={"vi": "Liên hệ tư vấn", "en": "Contact us", "zh": "联系咨询"},
), dict(
  video="/video/drawell-dw-180b.mp4", img="/video/drawell-dw-180b.jpg", vw=1280, vh=720, date={"vi": "10/11/2026", "en": "10 November 2026", "zh": "2026年11月10日"},
  tag={"vi": "Thiết bị phân tích", "en": "Analytical instruments", "zh": "分析仪器"},
  title={"vi": "Máy quang phổ hấp thụ nguyên tử Drawell DW-180B loại ngọn lửa — Phân tích nguyên tố chính xác, hiệu năng cao", "en": "Drawell DW-180B flame atomic absorption spectrophotometer — accurate, high-performance elemental analysis", "zh": "Drawell DW-180B 火焰原子吸收分光光度计 —— 准确、高效的元素分析"},
  intro={"vi": ["Máy quang phổ hấp thụ nguyên tử là thiết bị phòng thí nghiệm hiệu năng cao, được thiết kế để phân tích chính xác nhiều nguyên tố. DW-180B là dòng máy quang phổ hấp thụ nguyên tử sử dụng hệ ngọn lửa thế hệ mới, giá thành hợp lý, hiệu năng cao, với nhiều cải tiến đáng kể về độ tin cậy và tính thuận tiện khi sử dụng.", "Theo công bố của hãng, doanh số đạt hơn 100 máy trong năm đầu tiên sau khi ra mắt, không ghi nhận vấn đề chất lượng cần xử lý sau bán hàng và nhận được mức độ hài lòng cao từ khách hàng.", "Thông số chính: dải bước sóng 170–900 nm; sai số bước sóng không quá ±0,10 nm, độ lặp lại ≤ 0,05 nm; độ ổn định đường nền: độ trôi trong 30 phút ≤ 0,002 Abs, nhiễu ≤ 0,001 Abs; đầu đốt titan 10 cm, buồng phun PPS chống ăn mòn. Các đặc điểm nổi bật:"], "en": ["The atomic absorption spectrophotometer is a high-performance laboratory instrument designed for accurate analysis of many elements. The DW-180B is a new-generation flame atomic absorption spectrophotometer offering reasonable cost, high performance and significant improvements in reliability and ease of use.", "According to the manufacturer, more than 100 units were sold in the first year after launch, with no after-sales quality issues reported and high customer satisfaction.", "Key specifications: wavelength range 170–900 nm; wavelength accuracy within ±0.10 nm, repeatability ≤ 0.05 nm; baseline stability: 30-min drift ≤ 0.002 Abs, noise ≤ 0.001 Abs; 10 cm titanium burner, corrosion-resistant PPS spray chamber. Highlights:"], "zh": ["原子吸收分光光度计是高性能实验室仪器，可准确分析多种元素。DW-180B 是新一代火焰原子吸收分光光度计，价格合理、性能优异，在可靠性和易用性方面均有显著改进。", "据厂家公布，该机型上市第一年销量超过 100 台，未出现需售后处理的质量问题，客户满意度高。", "主要参数：波长范围 170–900 nm；波长误差不超过 ±0.10 nm，重复性 ≤ 0.05 nm；基线稳定性：30 分钟漂移 ≤ 0.002 Abs，噪声 ≤ 0.001 Abs；10 cm 钛燃烧头，耐腐蚀 PPS 雾化室。产品特点："]},
  bullets=True,
  items={'vi': [('', 'Điều khiển hoàn toàn tự động bằng máy tính.'), ('', 'Bộ gá xoay 8 vị trí đèn, hỗ trợ làm nóng đồng thời 4 đèn.'), ('', 'Sử dụng đèn catốt rỗng tiêu chuẩn 1,5 inch; dòng điện đèn điều chỉnh trong khoảng 0–15 mA.'), ('', 'Bộ đơn sắc Czerny–Turner, cách tử nhiễu xạ phẳng 1.800 vạch/mm.'), ('', 'Độ rộng khe phổ 0,1; 0,2; 0,4; 0,8; 1,6 và 2,4 nm, chuyển đổi tự động.'), ('', 'Hệ thống báo động an toàn toàn diện, bảo vệ kép bằng phần mềm và phần cứng; hỗ trợ đọc kết quả bằng bàn đạp chân khi đo ngọn lửa.')], 'en': [('', 'Fully automatic computer control.'), ('', '8-position lamp turret with simultaneous preheating of 4 lamps.'), ('', 'Standard 1.5-inch hollow cathode lamps; lamp current adjustable from 0 to 15 mA.'), ('', 'Czerny–Turner monochromator with a 1800 lines/mm plane diffraction grating.'), ('', 'Spectral bandwidth 0.1, 0.2, 0.4, 0.8, 1.6 and 2.4 nm, switched automatically.'), ('', 'Comprehensive safety alarm system with dual software and hardware protection; foot-pedal reading in flame mode.')], 'zh': [('', '全自动计算机控制。'), ('', '8 灯位转塔，可同时预热 4 只灯。'), ('', '采用标准 1.5 英寸空心阴极灯；灯电流 0–15 mA 可调。'), ('', 'Czerny–Turner 单色器，1800 线/mm 平面衍射光栅。'), ('', '光谱带宽 0.1、0.2、0.4、0.8、1.6 和 2.4 nm，自动切换。'), ('', '完善的安全报警系统，软硬件双重保护；火焰模式支持脚踏读数。')]},
  outro={"vi": "Ứng dụng: phân tích nguyên tố trong địa chất và khoáng sản, phân tích đất, năng lượng mới, giám sát môi trường, phân tích chất lượng nước, an toàn thực phẩm và dược phẩm. Mời Quý khách xem video kèm theo để quan sát trực tiếp thiết bị, khoang đèn và buồng đốt. Tư vấn, nhận catalogue, báo giá: Ms Ngọc Trâm – 0986.818.013 (Zalo).", "en": "Applications: elemental analysis in geology and mining, soil analysis, new energy, environmental monitoring, water quality analysis, food and pharmaceutical safety. Watch the video above to see the instrument, lamp compartment and burner up close. Advice, catalogue and quotations: Ms Ngoc Tram – +84 986 818 013 (Zalo).", "zh": "应用：地质与矿产、土壤分析、新能源、环境监测、水质分析、食品及药品安全等领域的元素分析。 请观看上方视频，近距离了解仪器、灯室和燃烧室。 咨询、索取样本与报价：Ngọc Trâm 女士 – +84 986 818 013（Zalo）。"},
  links={"vi": [("Xem sản phẩm", "/san-pham/may-quang-pho-hap-thu-nguyen-tu-ngon-lua-drawell-dw-180b/")], "en": [("View product", "/en/san-pham/may-quang-pho-hap-thu-nguyen-tu-ngon-lua-drawell-dw-180b/")], "zh": [("查看产品", "/zh/san-pham/may-quang-pho-hap-thu-nguyen-tu-ngon-lua-drawell-dw-180b/")]},
  cta={"vi": "Liên hệ tư vấn", "en": "Contact us", "zh": "联系咨询"},
), dict(
  video="/video/biobase-bjpx-h30l.mp4", img="/video/biobase-bjpx-h30l.jpg", vw=1280, vh=720, date={"vi": "10/11/2026", "en": "10 November 2026", "zh": "2026年11月10日"},
  tag={"vi": "Thiết bị phòng thí nghiệm", "en": "Laboratory equipment", "zh": "实验室设备"},
  title={"vi": "Tủ ấm giữ nhiệt BIOBASE BJPX-H30L — Nhiệt độ ổn định cho từng mẻ nuôi cấy", "en": "BIOBASE BJPX-H30L incubator — stable temperature for every culture batch", "zh": "BIOBASE BJPX-H30L 恒温培养箱 —— 每一批培养都温度稳定"},
  intro={"vi": ["Trong nuôi cấy và thí nghiệm, nhiệt độ dao động dù chỉ vài phần mười độ cũng có thể ảnh hưởng trực tiếp tới kết quả. Tủ ấm giữ nhiệt BIOBASE BJPX-H30L kiểm soát nhiệt độ ổn định, điều chỉnh chính xác trong dải nhiệt rộng, đáp ứng các nhu cầu thí nghiệm khác nhau tại phòng thí nghiệm.", "Thông số chính: dung tích 30 lít; dải nhiệt độ từ nhiệt độ phòng +5 °C đến 85 °C; độ dao động nhiệt ±0,2 °C và độ đồng đều ±0,5 °C tại 37 °C; độ chính xác 0,1 °C, cảm biến PT100, màn hình LCD; hẹn giờ 0–9999 phút; công suất 150 W, nguồn AC 220 V, 50/60 Hz; khoang trong 310 × 310 × 310 mm, 2 khay. Ưu điểm nổi bật:"], "en": ["In culture work and experiments, a temperature fluctuation of even a few tenths of a degree can directly affect the results. The BIOBASE BJPX-H30L incubator provides stable temperature control with precise adjustment over a wide range, meeting a variety of laboratory needs.", "Key specifications: 30 L capacity; temperature range from room temperature +5 °C to 85 °C; fluctuation ±0.2 °C and uniformity ±0.5 °C at 37 °C; accuracy 0.1 °C, PT100 sensor, LCD display; timer 0–9999 min; 150 W, AC 220 V, 50/60 Hz; interior 310 × 310 × 310 mm, 2 trays. Highlights:"], "zh": ["在培养和实验中，即使零点几度的温度波动也可能直接影响结果。BIOBASE BJPX-H30L 恒温培养箱温控稳定，可在较宽温度范围内精确调节，满足实验室的多种实验需求。", "主要参数：容积 30 L；温度范围室温 +5 °C 至 85 °C；37 °C 时波动度 ±0.2 °C、均匀度 ±0.5 °C；精度 0.1 °C，PT100 传感器，LCD 显示；定时 0–9999 分钟；功率 150 W，电源 AC 220 V，50/60 Hz；内胆 310 × 310 × 310 mm，2 层托盘。产品优势："]},
  bullets=True,
  items={'vi': [('', 'Khoang trong bằng thép không gỉ chải cao cấp, bốn góc bo tròn bán nguyệt, dễ vệ sinh.'), ('', 'Mặt trong bọc lá nhôm, lớp cách nhiệt chất lượng cao, giữ nhiệt tốt và phân bố nhiệt đồng đều.'), ('', 'Bảo vệ rò điện và quá áp, báo động quá nhiệt, công tắc kiểm soát nhiệt tự ngắt điện khi quá nhiệt, bảo vệ an toàn cho thiết bị và mẫu.')], 'en': [('', 'Premium brushed stainless steel chamber with semi-circular rounded corners for easy cleaning.'), ('', 'Aluminium-foil lined interior and high-quality insulation for good heat retention and uniform heat distribution.'), ('', 'Leakage and overvoltage protection, over-temperature alarm and a thermal cut-off switch that disconnects power on overheating, keeping the unit and samples safe.')], 'zh': [('', '优质拉丝不锈钢内胆，四角半圆弧过渡，易于清洁。'), ('', '内表面覆铝箔，优质保温层，保温性能好，温度分布均匀。'), ('', '漏电及过压保护、超温报警，超温时温控开关自动断电，保护设备和样品安全。')]},
  outro={"vi": "Ứng dụng: nuôi cấy vi sinh, bảo quản và xử lý mẫu tại trường đại học, viện nghiên cứu, bệnh viện, phòng thí nghiệm và khu công nghiệp. Tư vấn, nhận catalogue, báo giá: Ms Ngọc Trâm – 0986.818.013 (Zalo).", "en": "Applications: microbial culture, sample storage and processing at universities, research institutes, hospitals, laboratories and industrial parks. Advice, catalogue and quotations: Ms Ngoc Tram – +84 986 818 013 (Zalo).", "zh": "应用：微生物培养、样品保存与处理，适用于高校、科研院所、医院、实验室和工业园区。 咨询、索取样本与报价：Ngọc Trâm 女士 – +84 986 818 013（Zalo）。"},
  links={"vi": [("Xem sản phẩm", "/san-pham/tu-am-giu-nhiet-biobase-bjpx-h30l/")], "en": [("View product", "/en/san-pham/tu-am-giu-nhiet-biobase-bjpx-h30l/")], "zh": [("查看产品", "/zh/san-pham/tu-am-giu-nhiet-biobase-bjpx-h30l/")]},
  cta={"vi": "Liên hệ tư vấn", "en": "Contact us", "zh": "联系咨询"},
), dict(
  video="/video/drawell-dw-ftir-530a.mp4", img="/video/drawell-dw-ftir-530a.jpg", vw=1280, vh=720, date={"vi": "10/11/2026", "en": "10 November 2026", "zh": "2026年11月10日"},
  tag={"vi": "Thiết bị phân tích", "en": "Analytical instruments", "zh": "分析仪器"},
  title={"vi": "Máy quang phổ hồng ngoại FT-IR Drawell DW-FTIR-530A — Nhận diện vật liệu chính xác, nhanh chóng",
         "en": "Drawell DW-FTIR-530A FT-IR spectrometer — accurate, fast material identification",
         "zh": "Drawell DW-FTIR-530A 傅里叶红外光谱仪 —— 准确、快速识别材料"},
  intro={"vi": ["Trong kiểm soát chất lượng và phân tích phòng thí nghiệm, nhận diện đúng thành phần vật liệu ngay từ đầu vào có ý nghĩa quyết định đối với độ tin cậy của toàn bộ kết quả. Máy quang phổ hồng ngoại FT-IR Drawell DW-FTIR-530A được thiết kế cho nhu cầu nhận diện vật liệu thường quy, kiểm soát chất lượng và phân tích mẫu bột, polymer, màng mỏng, chất lỏng, dầu và khí, với chi phí bảo trì thường quy thấp.",
                "Thông số chính: tỷ số tín hiệu trên nhiễu cao hơn 20.000:1; dải phổ 7800–350 cm⁻¹; độ phân giải 0,85 cm⁻¹; độ chính xác số sóng ±0,01 cm⁻¹; đầu dò tiêu chuẩn LiTaO3, tùy chọn đầu dò nhiệt điện ổn định nhiệt và đầu dò MCT làm lạnh bán dẫn. Đặc điểm nổi bật:"],
         "en": ["In quality control and laboratory analysis, correctly identifying material composition at incoming inspection is decisive for the reliability of every result that follows. The Drawell DW-FTIR-530A FT-IR spectrometer is designed for routine material identification, quality control and analysis of powders, polymers, thin films, liquids, oils and gases, with low routine maintenance costs.",
                "Key specifications: signal-to-noise ratio better than 20,000:1; spectral range 7800–350 cm⁻¹; resolution 0.85 cm⁻¹; wavenumber accuracy ±0.01 cm⁻¹; standard LiTaO3 detector, with optional temperature-stabilized pyroelectric and thermoelectrically cooled MCT detectors. Highlights:"],
         "zh": ["在质量控制和实验室分析中，从来料环节准确识别材料成分，对整个结果的可靠性至关重要。Drawell DW-FTIR-530A 傅里叶变换红外光谱仪专为常规材料识别、质量控制以及粉末、聚合物、薄膜、液体、油品和气体样品分析而设计，日常维护成本低。",
                "主要参数：信噪比优于 20000:1；光谱范围 7800–350 cm⁻¹；分辨率 0.85 cm⁻¹；波数精度 ±0.01 cm⁻¹；标配 LiTaO3 检测器，可选温控热释电检测器和半导体制冷 MCT 检测器。产品特点："]},
  bullets=True,
  items={'vi': [('', 'Giao thoa kế Michelson góc khối với công nghệ căn chỉnh gương cố định đã được cấp bằng sáng chế; gương mạ vàng cho độ ổn định quang học lâu dài và độ nhạy cao.'), ('', 'Kết cấu mô-đun chắc chắn trên đế nhôm đúc, tản nhiệt tốt, chống rung; chống nhiễu điện từ theo tiêu chuẩn CE.'), ('', 'Hệ quang học chống ẩm với giao thoa kế kín nhiều lớp: hộp hút ẩm dung lượng lớn, cửa sổ quan sát chất hút ẩm, giám sát nhiệt độ và độ ẩm theo thời gian thực.'), ('', 'Khoang mẫu rộng, linh hoạt phụ kiện: đo truyền qua, ATR, ô mẫu lỏng, ô mẫu khí và phản xạ khuếch tán.'), ('', 'Chẩn đoán trạng thái thiết bị theo thời gian thực; kết nối Ethernet và Wi-Fi phục vụ vận hành, truyền dữ liệu từ xa.'), ('', 'Phần mềm trạm làm việc FTOS Suite mạnh mẽ, thân thiện với người sử dụng.')], 'en': [('', 'Cube-corner Michelson interferometer with patented fixed-mirror alignment technology; gold-coated mirrors for long-term optical stability and high sensitivity.'), ('', 'Robust modular design on a cast aluminium base with good heat dissipation and vibration resistance; electromagnetic interference protection to CE standards.'), ('', 'Moisture-proof optics with a multi-layer sealed interferometer: large-capacity desiccant box, desiccant inspection window, real-time temperature and humidity monitoring.'), ('', 'Large sample compartment for flexible accessories: transmission, ATR, liquid cell, gas cell and diffuse reflectance.'), ('', 'Real-time instrument status diagnostics; Ethernet and Wi-Fi connectivity for remote operation and data transfer.'), ('', 'Powerful, user-friendly FTOS Suite workstation software.')], 'zh': [('', '角锥迈克尔逊干涉仪，采用专利动镜固定准直技术；镀金反射镜，光学性能长期稳定，灵敏度高。'), ('', '铸铝底座模块化结构，坚固耐用，散热好，抗振动；电磁抗干扰符合 CE 标准。'), ('', '防潮光学系统，多层密封干涉仪：大容量干燥剂盒、干燥剂观察窗、温湿度实时监控。'), ('', '大样品仓，附件灵活：透射、ATR、液体池、气体池和漫反射。'), ('', '实时诊断仪器状态；支持以太网和 Wi-Fi，便于远程操作和数据传输。'), ('', '功能强大、操作友好的 FTOS Suite 工作站软件。')]},
  outro={"vi": "Ứng dụng: nhận diện và so sánh polymer, cao su, màng và lớp phủ; kiểm tra nguyên liệu dược phẩm, hóa chất; phân tích dầu bôi trơn, dung môi và chất lỏng; phân tích bột và nguyên liệu dạng rắn tại trường đại học, viện nghiên cứu, phòng thí nghiệm kiểm soát chất lượng và doanh nghiệp sản xuất. Tư vấn, nhận catalogue, báo giá: Ms Ngọc Trâm – 0986.818.013 (Zalo).",
         "en": "Applications: identification and comparison of polymers, rubber, films and coatings; inspection of pharmaceutical raw materials and chemicals; analysis of lubricants, solvents and liquids; analysis of powders and solid materials at universities, research institutes, QC laboratories and manufacturers. Advice, catalogue and quotations: Ms Ngoc Tram – +84 986 818 013 (Zalo).",
         "zh": "应用：聚合物、橡胶、薄膜和涂层的识别与比对；药品原料、化学品检验；润滑油、溶剂及液体分析；粉末和固体原料分析，适用于高校、科研院所、质控实验室和生产企业。咨询、索取样本与报价：Ngọc Trâm 女士 – +84 986 818 013（Zalo）。"},
  links={"vi": [("Xem sản phẩm", "/san-pham/may-quang-pho-hong-ngoai-ft-ir-drawell-dw-ftir-530a/")], "en": [("View product", "/en/san-pham/may-quang-pho-hong-ngoai-ft-ir-drawell-dw-ftir-530a/")], "zh": [("查看产品", "/zh/san-pham/may-quang-pho-hong-ngoai-ft-ir-drawell-dw-ftir-530a/")]},
  cta={"vi": "Liên hệ tư vấn", "en": "Contact us", "zh": "联系咨询"},
), dict(
  img="https://img.waimaoniu.net/2587/2587-202210151359498707.jpg", date={"vi": "09/11/2026", "en": "9 November 2026", "zh": "2026年11月9日"},
  tag={"vi": "Thiết bị phòng thí nghiệm", "en": "Laboratory equipment", "zh": "实验室设备"},
  title={"vi": "Máy rửa siêu âm BIOBASE dòng UC-VAD — Làm sạch sâu đến từng chi tiết",
         "en": "BIOBASE UC-VAD series ultrasonic cleaners — deep cleaning down to every detail",
         "zh": "BIOBASE UC-VAD 系列超声波清洗机 —— 深层清洁，细致入微"},
  intro={"vi": ["Trong phòng thí nghiệm, làm sạch dụng cụ bám bẩn ở khe hẹp và bề mặt có hình dạng phức tạp luôn là công đoạn tốn nhiều thời gian nhất. Máy rửa siêu âm BIOBASE dòng UC-VAD làm sạch bằng sóng siêu âm, không gây ô nhiễm, không làm hư hại vật rửa, đồng thời tăng tốc quá trình hòa tan và nhũ hóa, giúp rút ngắn đáng kể thời gian làm sạch mỗi ngày.",
                "Model tiêu biểu UC-48VAD: dung tích 22,5 lít, công suất siêu âm 480 W, công suất gia nhiệt 500 W. Thông số kỹ thuật chính:"],
         "en": ["In the laboratory, cleaning labware soiled in narrow gaps and on complex surfaces is often the most time-consuming task. BIOBASE UC-VAD series ultrasonic cleaners clean with ultrasonic waves, without contamination or damage to the items, while speeding up dissolution and emulsification, considerably shortening daily cleaning time.",
                "Typical model UC-48VAD: 22.5 L capacity, 480 W ultrasonic power, 500 W heating power. Main specifications:"],
         "zh": ["在实验室中，清洗窄缝和复杂形状表面上的污垢往往是最耗时的环节。BIOBASE UC-VAD 系列超声波清洗机利用超声波清洗，无污染、不损伤被清洗物，同时加速溶解和乳化过程，显著缩短每日清洗时间。",
                "典型型号 UC-48VAD：容量 22.5 L，超声功率 480 W，加热功率 500 W。主要技术参数："]},
  bullets=True, yt="WvV5iL2Hupg",
  ytcap={"vi": "Video: máy rửa siêu âm BIOBASE UC-48AD (dòng UC-AD, tần số 40 kHz)", "en": "Video: BIOBASE UC-48AD ultrasonic cleaner (UC-AD series, 40 kHz)", "zh": "视频：BIOBASE UC-48AD 超声波清洗机（UC-AD 系列，40 kHz）"},
  items={"vi": [("Tần số", "tần số kép 28/40 kHz"), ("Thời gian rửa", "1–99 phút; gia nhiệt từ nhiệt độ phòng tới 80 °C"),
                ("Vật liệu", "vỏ và khoang rửa bằng thép không gỉ 304, chống ăn mòn"), ("Hiển thị", "màn hình LED rõ ràng"),
                ("Nguồn điện", "220 V, 50 Hz"), ("Phụ kiện tiêu chuẩn", "nắp cách âm, giỏ rửa, ống PVC"),
                ("5 mức dung tích", "6,5 / 10 / 15 / 22,5 / 30 lít (UC-18VAD, UC-24VAD, UC-36VAD, UC-48VAD, UC-60VAD), công suất siêu âm từ 180 W đến 600 W, đáp ứng linh hoạt quy mô của từng phòng thí nghiệm")],
         "en": [("Frequency", "dual frequency 28/40 kHz"), ("Cleaning time", "1–99 min; heating from room temperature to 80 °C"),
                ("Material", "SUS 304 stainless steel housing and tank, corrosion resistant"), ("Display", "clear LED display"),
                ("Power supply", "220 V, 50 Hz"), ("Standard accessories", "sound-insulating lid, basket, PVC hose"),
                ("5 capacities", "6.5 / 10 / 15 / 22.5 / 30 L (UC-18VAD, UC-24VAD, UC-36VAD, UC-48VAD, UC-60VAD), ultrasonic power from 180 W to 600 W, to suit laboratories of every size")],
         "zh": [("频率", "双频 28/40 kHz"), ("清洗时间", "1–99 分钟；加热范围室温至 80 °C"),
                ("材质", "外壳和清洗槽采用 304 不锈钢，耐腐蚀"), ("显示", "清晰的 LED 显示屏"),
                ("电源", "220 V，50 Hz"), ("标准配件", "隔音盖、清洗篮、PVC 软管"),
                ("5 种容量", "6.5 / 10 / 15 / 22.5 / 30 L（UC-18VAD、UC-24VAD、UC-36VAD、UC-48VAD、UC-60VAD），超声功率 180–600 W，灵活满足不同规模实验室的需求")]},
  outro={"vi": "Ứng dụng: phòng thí nghiệm, trường đại học, viện nghiên cứu, ngành điện tử, cơ khí, hóa chất và các đơn vị dịch vụ. Tư vấn, báo giá: Ms Ngọc Trâm – 0986.818.013 (Zalo).",
         "en": "Applications: laboratories, universities, research institutes, electronics, mechanical engineering, chemical industry and service providers. Advice and quotations: Ms Ngoc Tram – +84 986 818 013 (Zalo).",
         "zh": "应用：实验室、高校、科研院所，以及电子、机械、化工行业和服务机构。咨询与报价：Ngọc Trâm 女士 – +84 986 818 013（Zalo）。"},
  links={"vi": [("Xem sản phẩm", "/san-pham/may-rua-sieu-am-hai-tan-so-biobase-uc-vad-uc-18vad-uc-24vad-uc-36vad-uc-48vad-uc/")], "en": [("View product", "/en/san-pham/may-rua-sieu-am-hai-tan-so-biobase-uc-vad-uc-18vad-uc-24vad-uc-36vad-uc-48vad-uc/")], "zh": [("查看产品", "/zh/san-pham/may-rua-sieu-am-hai-tan-so-biobase-uc-vad-uc-18vad-uc-24vad-uc-36vad-uc-48vad-uc/")]},
  cta={"vi": "Liên hệ tư vấn", "en": "Contact us", "zh": "联系咨询"},
), dict(
  img="/anh-san-pham/crs1414.jpg", date={"vi": "01/11/2026", "en": "1 November 2026", "zh": "2026年11月1日"},
  tag={"vi": "Ứng dụng thực tế", "en": "Field application", "zh": "应用案例"},
  title={"vi": "Sàng đĩa quay đan xen CRS1414 vận hành hiệu quả tại Công ty Nhôm Lâm Đồng – TKV",
         "en": "CRS1414 intermeshing rotary disc screen in operation at Lam Dong Aluminum Company – TKV",
         "zh": "CRS1414 交错旋转盘式筛在林同铝业公司（TKV）高效运行"},
  intro={"vi": ["Sàng đĩa quay đan xen CRS1414 (năng suất 150 t/h, 14 trục, mặt sàng rộng 1400 mm, cỡ hạt dưới sàng ≤ 8 mm) được đưa vào hệ thống sàng – nghiền than của Phân xưởng Nhiệt điện – Công ty Nhôm Lâm Đồng – TKV, khắc phục hiện tượng bám dính, bít tắc của sàng rung khi sàng than có độ ẩm cao.",
                "Kết quả chạy thử: hiệu suất sàng trung bình đạt 85,8% khi độ ẩm than khoảng 8,2%; sau khi cải thiện phân bố dòng liệu và lót composite cho máng cấp liệu, hiệu suất sàng tăng lên trên 90%. Tỷ lệ hạt dưới 1 mm trong than sau xử lý giảm từ 53,1% xuống 42,1%, hạn chế nghiền thừa; không ghi nhận hạt lớn hơn 16 mm."],
         "en": ["The CRS1414 intermeshing rotary disc screen (150 t/h, 14 shafts, 1400 mm screen width, undersize ≤ 8 mm) was installed in the coal screening and crushing system of the Thermal Power Workshop at Lam Dong Aluminum Company – TKV, overcoming the adhesion and blinding that affect vibrating screens with high-moisture coal.",
                "Test results: average screening efficiency of 85.8% at a coal moisture of about 8.2%; after improving feed distribution and lining the feed chute with composite, efficiency rose above 90%. The share of particles below 1 mm in the processed coal fell from 53.1% to 42.1%, limiting over-crushing, and no particles larger than 16 mm were detected."],
         "zh": ["CRS1414 交错旋转盘式筛（产能 150 t/h，14 轴，筛面宽 1400 mm，筛下粒度 ≤ 8 mm）应用于林同铝业公司（TKV）热电车间的煤筛分破碎系统，解决了振动筛筛分高水分煤时的物料黏附和堵塞问题。",
                "试运行结果：煤平均水分约 8.2% 时，平均筛分效率达 85.8%；改善料流分布并为给料溜槽加装复合材料衬板后，筛分效率提高到 90% 以上。处理后煤中小于 1 mm 颗粒的比例由 53.1% 降至 42.1%，抑制了过粉碎；未发现大于 16 mm 的颗粒。"]},
  outro={"vi": "Kết quả được trình bày chi tiết trong bài báo khoa học của TS. Lê Thanh Bình (2026).",
         "en": "The results are presented in detail in a scientific paper by Dr. Le Thanh Binh (2026).",
         "zh": "详细结果见黎清平博士的科学论文（2026）。"},
  links={"vi": [("Đọc bài báo (PDF)", "/bai-bao/2026-performance-evaluation-of-the-crs1414-intermeshing-rotary.pdf")],
         "en": [("Read the paper – English (PDF)", "/bai-bao/2026-performance-evaluation-of-the-crs1414-intermeshing-rotary-en.pdf"), ("Original – Vietnamese (PDF)", "/bai-bao/2026-performance-evaluation-of-the-crs1414-intermeshing-rotary.pdf")],
         "zh": [("阅读论文 – 中文（PDF）", "/bai-bao/2026-performance-evaluation-of-the-crs1414-intermeshing-rotary-zh.pdf"), ("越南语原文（PDF）", "/bai-bao/2026-performance-evaluation-of-the-crs1414-intermeshing-rotary.pdf")]},
  cta={"vi": "Liên hệ tư vấn", "en": "Contact us", "zh": "联系咨询"},
), dict(
  video="/video/lo-nung-mx.mp4", img="/tin-tuc/lo-nung-mx.jpg", date={"vi": "01/11/2026", "en": "1 November 2026", "zh": "2026年11月1日"},
  tag={"vi": "Thiết bị phòng thí nghiệm", "en": "Laboratory equipment", "zh": "实验室设备"},
  title={"vi": "Lò nung BIOBASE dòng MX — Nhiệt độ cao ổn định cho mọi phép thử nhiệt",
         "en": "BIOBASE MX series muffle furnaces — stable high temperature for every thermal test",
         "zh": "BIOBASE MX 系列马弗炉 —— 稳定高温，满足各类热学试验"},
  intro={"vi": ["Lò nung BIOBASE dòng MX phù hợp cho trường đại học, viện nghiên cứu, phòng thí nghiệm và khu công nghiệp trong các phép thử tro hóa, nung mẫu, xử lý nhiệt và kiểm nghiệm vật liệu.",
                "Dung tích buồng 6–30 lít, nhiệt độ tối đa 1000–1200 °C (model đặc biệt đến 1700 °C), độ chính xác ±1 °C; buồng sợi gốm, gia nhiệt 4 mặt."],
         "en": ["BIOBASE MX series muffle furnaces suit universities, research institutes, laboratories and industrial parks for ashing, sample calcination, heat treatment and materials testing.",
                "Chamber 6–30 L, max temperature 1000–1200 °C (special models up to 1700 °C), accuracy ±1 °C; ceramic fibre chamber, heating on 4 sides."],
         "zh": ["BIOBASE MX 系列马弗炉适用于高校、科研院所、实验室及工业园区的灰化、样品灼烧、热处理和材料检测。",
                "炉膛容积 6–30 L，最高温度 1000–1200 °C（特殊型号可达 1700 °C），控温精度 ±1 °C；陶瓷纤维炉膛，四面加热。"]},
  outro={"vi": "Quý khách vui lòng liên hệ để được tư vấn model phù hợp cho phòng thí nghiệm của mình.",
         "en": "Please contact us for advice on the right model for your laboratory.",
         "zh": "欢迎联系我们，为您的实验室推荐合适型号。"},
  cta={"vi": "Liên hệ tư vấn", "en": "Contact us", "zh": "联系咨询"},
), dict(  img="/tin-tuc/vat-tu-phong-thi-nghiem.jpg", date={"vi": "01/11/2026", "en": "1 November 2026", "zh": "2026年11月1日"},
  tag={"vi": "Vật tư phòng thí nghiệm", "en": "Laboratory consumables", "zh": "实验室耗材"},
  title={"vi": "Phòng lab của anh/chị đang cần thiết bị hay bổ sung vật tư?",
         "en": "Does your lab need equipment or a consumables refill?",
         "zh": "您的实验室需要添置设备还是补充耗材？"},
  intro={"vi": ["Chọn thiết bị phù hợp ngay từ đầu giúp phòng thí nghiệm chủ động hơn khi tìm vật tư, thay thế linh kiện và duy trì công việc hằng ngày.",
                "Giới thiệu 5 nhóm thiết bị BIOBASE dành cho phòng thí nghiệm, bộ phận QC/QA và nhà máy trong khu công nghiệp:"],
         "en": ["Choosing the right equipment from the start makes it easier for a laboratory to source consumables, replace parts and keep daily work running.",
                "Five groups of BIOBASE equipment for laboratories, QC/QA departments and factories in industrial parks:"],
         "zh": ["从一开始就选对设备，实验室在采购耗材、更换配件和维持日常工作时会更加主动。",
                "以下为适用于实验室、QC/QA 部门及工业园区工厂的 5 类 BIOBASE 设备："]},
  items={"vi": [("Micropipette", "Thao tác hút, chia mẫu thể tích nhỏ. Kết hợp đầu côn thường hoặc đầu côn lọc phù hợp ứng dụng."),
                ("Máy đo pH", "Phục vụ kiểm tra pH mẫu nước, nguyên liệu và sản phẩm theo phương pháp của phòng lab. Lựa chọn kèm dung dịch chuẩn, dung dịch bảo quản và điện cực phù hợp."),
                ("Bộ lọc chân không", "Phục vụ lọc mẫu, chuẩn bị mẫu và quy trình kiểm nghiệm phù hợp. Lựa chọn màng lọc theo kích thước lỗ, vật liệu màng và tính chất mẫu."),
                ("Máy lọc nước phòng thí nghiệm", "Lựa chọn chất lượng nước và công suất theo nhu cầu sử dụng, đồng thời xác định đúng lõi lọc, màng RO và cột DI thay thế."),
                ("Máy ly tâm", "Phục vụ tách và chuẩn bị mẫu. Cần chọn đồng bộ rotor, adapter và ống ly tâm theo yêu cầu công việc.")],
         "en": [("Micropipettes", "For aspirating and dispensing small sample volumes. Use standard or filter tips to suit the application."),
                ("pH meters", "For checking the pH of water samples, raw materials and products according to the lab's methods. Supplied with suitable buffer solutions, storage solution and electrodes."),
                ("Vacuum filtration sets", "For sample filtration, sample preparation and testing procedures. Membranes are chosen by pore size, membrane material and sample properties."),
                ("Laboratory water purifiers", "Water quality and output are chosen to match demand, together with the correct replacement filter cartridges, RO membranes and DI columns."),
                ("Centrifuges", "For sample separation and preparation. Rotors, adapters and centrifuge tubes should be selected as a matched set for the work.")],
         "zh": [("移液器", "用于小体积样品的吸取和分配。可根据应用搭配普通吸头或滤芯吸头。"),
                ("pH 计", "按实验室方法检测水样、原料和产品的 pH 值。可配套选择标准缓冲液、保存液及合适的电极。"),
                ("真空过滤装置", "用于样品过滤、样品前处理及相关检测流程。滤膜按孔径、材质和样品性质选择。"),
                ("实验室纯水机", "根据用水需求选择水质和产水量，并确定匹配的替换滤芯、RO 膜和 DI 柱。"),
                ("离心机", "用于样品分离和前处理。转子、适配器和离心管需按工作要求配套选择。")]},
  outro={"vi": "Anh/chị gửi tên thiết bị, model đang sử dụng hoặc nhu cầu kiểm nghiệm để trao đổi cấu hình và vật tư phù hợp.",
         "en": "Send us the name and model of the equipment you use, or your testing needs, and we will advise on a suitable configuration and consumables.",
         "zh": "请告知您正在使用的设备名称、型号或检测需求，我们将为您推荐合适的配置和耗材。"},
  cta={"vi": "Liên hệ tư vấn", "en": "Contact us", "zh": "联系咨询"},
)]
H = {"vi": "Tin tức", "en": "News", "zh": "新闻"}
PRE = {"vi": "/", "en": "/en/", "zh": "/zh/"}
UI = {"vi": dict(all="Xem tất cả tin tức", more="Xem tiếp →", lead="Tin tức, ứng dụng thực tế và giới thiệu thiết bị của Vân Phong.", back="← Tất cả tin tức", other="Tin khác"),
      "en": dict(all="View all news", more="Read more →", lead="News, field applications and equipment introductions from Van Phong.", back="← All news", other="More news"),
      "zh": dict(all="查看全部新闻", more="阅读全文 →", lead="Vân Phong 新闻、应用案例及设备介绍。", back="← 全部新闻", other="其他新闻")}
CSS = """.ncards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px;max-width:1180px;margin:0 auto}
.ncard{background:#fff;border:1px solid #DCE1E6;border-radius:10px;overflow:hidden;display:flex;flex-direction:column;transition:box-shadow .2s,transform .2s;color:inherit;text-decoration:none}
.ncard:hover{box-shadow:0 10px 24px rgba(14,47,90,.12);transform:translateY(-2px)}
.ncard .nm{position:relative;aspect-ratio:16/10;background:#F0F2F4;overflow:hidden}.ncard .nm img{width:100%;height:100%;object-fit:cover;display:block}
.ncard .play{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:58px;height:58px;border-radius:50%;background:rgba(14,47,90,.78);color:#fff;display:grid;place-items:center;font-size:22px;padding-left:4px}
.ncard .nb{padding:16px 18px 18px;display:flex;flex-direction:column;flex:1}
.ncard .nmeta{margin:0 0 6px;color:#5F6B77;font-size:12.5px}.ncard .nmeta span{color:#1580BF;font-weight:700;text-transform:uppercase;letter-spacing:.03em}
.ncard h3{margin:0 0 8px;font-size:17px;line-height:1.4;color:#0E2F5A}.ncard p{margin:0 0 12px;color:#4A545E;font-size:14.5px;line-height:1.6}
.ncard .more{margin-top:auto;color:#F07C1B;font-weight:700;font-size:14px}
.nall{text-align:center;margin-top:26px}
.ncards.home{display:flex;flex-wrap:wrap;justify-content:center}.ncards.home .ncard{flex:0 1 calc((100% - 44px)/3)}
@media (max-width:900px){.ncards.home .ncard{flex-basis:calc((100% - 22px)/2)}}@media (max-width:600px){.ncards.home .ncard{flex-basis:100%}}
.art{max-width:860px;margin:0 auto 40px}.art h1{font-size:clamp(24px,3vw,32px);line-height:1.3;color:#0E2F5A;margin:6px 0 14px}
.art figure{margin:0 0 20px}.art figure img,.art figure video{width:100%;height:auto;display:block;border-radius:8px}.art figure video{background:#000}.art figure img{max-width:560px}
.art figure video.port{max-width:420px}.art p,.art li{color:#33404C;font-size:16px}.art ol,.art ul{padding-left:22px}
@media (max-width:900px){.ncards{grid-template-columns:1fr 1fr}}@media (max-width:600px){.ncards{grid-template-columns:1fr}}"""

def _slugify(t, n=80):
    t = unicodedata.normalize("NFD", t.replace("đ", "d").replace("Đ", "D"))
    t = "".join(c for c in t if unicodedata.category(c) != "Mn").lower()
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:n].strip("-")

def slug(n): return _slugify(n["title"]["vi"])
def url(n, lang): return f"{PRE[lang]}tin-tuc/{slug(n)}/"
def thumb(n): return n.get("thumb") or n["img"]

def summary(n, lang, k=190):
    t = re.sub(r"<[^>]+>", "", n["intro"][lang][0])
    if len(t) <= k: return t
    cut = t[:k]; sp = cut.rfind(" ")
    return (cut[:sp] if sp > 60 and lang != "zh" else cut).rstrip(" ,;:") + "…"

def card(n, lang):
    play = '<span class="play">▶</span>' if ("video" in n or "yt" in n) else ""
    return (f'<a class="ncard" href="{url(n, lang)}"><div class="nm"><img src="{thumb(n)}" alt="{n["title"][lang]}" loading="lazy">{play}</div>'
            f'<div class="nb"><p class="nmeta"><span>{n["tag"][lang]}</span> · {n["date"][lang]}</p><h3>{n["title"][lang]}</h3>'
            f'<p>{summary(n, lang)}</p><span class="more">{UI[lang]["more"]}</span></div></a>')

def cards(lang, items=None):
    return '<div class="ncards">' + "".join(card(n, lang) for n in (N if items is None else items)) + "</div>"

def article(n, lang):
    items = "".join((f"<li><b>{a}</b> – {b}</li>" if a else f"<li>{b}</li>") for a, b in n["items"][lang]) if "items" in n else ""
    if "video" in n:
        port = n.get("vh", 960) > n.get("vw", 540)
        fig = f'<video{" class=port" if port else ""} src="{n["video"]}" poster="{n["img"]}" controls playsinline preload="metadata" width="{n.get("vw",540)}" height="{n.get("vh",960)}"></video>'
    else:
        fig = f'<img src="{n["img"]}" alt="{n["title"][lang]}">'
    yt = (f'<div style="position:relative;padding-top:56.25%;border-radius:10px;overflow:hidden;background:#000;margin:6px 0 4px"><iframe src="https://www.youtube-nocookie.com/embed/{n["yt"]}" title="{n["ytcap"][lang]}" loading="lazy" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture; fullscreen" allowfullscreen style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe></div><p style="font-size:13.5px;color:#64748b">{n["ytcap"][lang]}</p>' if n.get("yt") else "")
    lst = (f'<ul>{items}</ul>' if n.get("bullets") else f'<ol>{items}</ol>') if items else ""
    btns = "".join(f'<a class="btn" href="{h}"' + (' target="_blank" rel="noopener"' if h.endswith(".pdf") else "") + f'>{t}</a>' for t, h in n.get("links", {}).get(lang, []))
    return (f'<article class="art"><p class="tag">{n["tag"][lang]} · {n["date"][lang]}</p><h1>{n["title"][lang]}</h1><figure>{fig}</figure>'
            + "".join(f"<p>{x}</p>" for x in n["intro"][lang]) + lst + f'<p>{n["outro"][lang]}</p>{yt}'
            + f'<div class="btns">{btns}<a class="btn cta" href="{PRE[lang]}#lien-he">{n["cta"][lang]}</a></div></article>')

def block(lang):
    return f"""<section id="tin-tuc"><div class="wrap">
  <style>{CSS}</style>
  <div class="title"><h2>{H[lang]}</h2></div>
  {cards(lang, N[:3]).replace('class="ncards"', 'class="ncards home"', 1)}
  <p class="nall"><a class="btn cta" href="{PRE[lang]}tin-tuc/">{UI[lang]["all"]}</a></p>
</div></section>"""
