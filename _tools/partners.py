# -*- coding: utf-8 -*-
# Partner tiles: (monogram, color, {lang: (name, work)})
P = [
 ("VD","#0E5C3A",{"vi":("Công ty CP Than Vàng Danh – Vinacomin","Lắp đặt hệ thống cam hãm tự động dùng khí nén (đề tài KH&amp;CN cấp TKV); tư vấn sàng đĩa đan xen CRS350-15"),
                  "en":("Vang Danh Coal JSC – Vinacomin","Installation of an automatic pneumatic mine-car retarder system (Vinacomin R&amp;D project); CRS350-15 disc screen consulting"),
                  "zh":("Vang Danh 煤炭股份公司 – Vinacomin","安装气动自动阻车系统（TKV 级科研项目）；CRS350-15 交叉筛方案咨询")}),
 ("IEMM","#0E2F5A",{"vi":("Viện Cơ khí Năng lượng và Mỏ – Vinacomin","Dịch vụ kỹ thuật; mua bán vật tư, thiết bị"),
                   "en":("Institute of Energy and Mining Mechanical Engineering – Vinacomin (IEMM)","Technical services; supply of materials and equipment"),
                   "zh":("能源与矿山机械研究院 – Vinacomin（IEMM）","技术服务；物资、设备供应")}),
 ("ĐD","#1580BF",{"vi":("Công ty TNHH Cơ điện Đại Dương","Mua bán vật tư, thiết bị các loại, trong đó có sàng đĩa đan xen CRS1414"),
                  "en":("Dai Duong Electromechanical Co., Ltd.","Supply of various materials and equipment, including the CRS1414 disc screen"),
                  "zh":("Dai Duong 机电有限责任公司","各类物资、设备供应，包括 CRS1414 交叉筛")}),
 ("GB","#B3261E",{"vi":("Gongbei Heavy Machinery (Thạch Gia Trang, Trung Quốc)","Hãng sản xuất sàng đĩa đan xen CRS1414, CRS350-15"),
                  "en":("Shijiazhuang Gongbei Heavy Machinery (China)","Manufacturer of CRS1414 and CRS350-15 disc screens"),
                  "zh":("石家庄功倍重型机械有限公司","CRS1414、CRS350-15 交叉筛制造商")}),
 ("TT","#0F7C8C",{"vi":("Công ty Tư vấn Thủy điện Thủy lợi Thăng Long","Tư vấn thẩm tra Báo cáo NCKT Hồ bùn đỏ số 2 – Tổ hợp Bauxit – Nhôm Lâm Đồng"),
                  "en":("Thang Long Hydropower &amp; Irrigation Consulting","Verification of the feasibility study for Red Mud Pond No. 2 – Lam Dong Bauxite – Alumina Complex"),
                  "zh":("Thang Long 水电水利咨询公司","林同铝土矿 – 氧化铝联合体2号赤泥库可研报告审查咨询")}),
 ("CFT","#D35400",{"vi":("Công ty CP Công nghiệp CFTSHOP","Cung cấp tủ cấy vi sinh BIOBASE BKCB-V900"),
                   "en":("CFTSHOP Industrial JSC","Supply of BIOBASE BKCB-V900 clean bench"),
                   "zh":("CFTSHOP 工业股份公司","供应 BIOBASE BKCB-V900 超净工作台")}),
 ("ĐHH","#7A1F3D",{"vi":("Trường Đại học Sư phạm – Đại học Huế","Cung cấp thiết bị thí nghiệm cho Khoa Hóa học"),
                   "en":("University of Education – Hue University","Laboratory equipment for the Faculty of Chemistry"),
                   "zh":("顺化大学师范大学","为化学系供应实验室设备")}),
 ("DW","#C8102E",{"vi":("Chongqing Drawell Instrument (Trung Quốc)","x"),"en":("Chongqing Drawell Instrument Co., Ltd. (China)","x"),"zh":("重庆德瑞沃仪器有限公司（Drawell）","x")}),
 ("BIO","#1D2F6F",{"vi":("BIOBASE Group (Trung Quốc)","x"),"en":("BIOBASE Group (China)","x"),"zh":("博科集团（BIOBASE）","x")}),
]
LOGO = {"VD":"than-vang-danh.png","IEMM":"iemm.png","BQL":"vinacomin.png","NLĐ":"vinacomin.png","GB":"gongbei.png?v=2","ĐD":"co-dien-dai-duong.png?v=2","ĐHH":"dhsp-hue.png","BIO":"biobase.png","DW":"drawell.png"}
def block(lang):
    out=[]
    for m,c,d in P:
        name=d[lang][0]
        if m in LOGO:
            lg=f'<div class="lg img"><img src="/logo-doi-tac/{LOGO[m]}" alt="" loading="lazy"></div>'
        else:
            lg=f'<div class="lg" style="--c:{c}">{m}</div>'
        out.append(f'    <div class="pt">{lg}<b>{name}</b></div>')
    return "\n".join(out)
