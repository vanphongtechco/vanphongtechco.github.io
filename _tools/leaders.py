# -*- coding: utf-8 -*-
# Leadership section (Ban lãnh đạo) — international-style profile, no employment history / personal data.
L = {
 "vi": dict(
  h="Ban lãnh đạo",
  name="TS. Lê Thanh Bình", role="Trợ lý Tổng Giám đốc",
  bio=["TS. Lê Thanh Bình là Trợ lý Tổng Giám đốc Công ty TNHH Kỹ thuật và Thương mại Vân Phong. Ông có 20 năm kinh nghiệm trong lĩnh vực nghiên cứu khoa học và công nghệ, công nghệ vật liệu, tư vấn xây dựng, thí nghiệm – kiểm định, thiết kế – chế tạo thiết bị cơ khí phục vụ ngành mỏ và công nghiệp, thương mại xuất – nhập khẩu vật tư – thiết bị công nghiệp, y tế, phòng thí nghiệm và giáo dục.",
       "Tại Vân Phong, ông hỗ trợ Tổng Giám đốc về chuyên môn kỹ thuật, tư vấn đầu tư xây dựng, thiết kế, tính toán, lựa chọn giải pháp thiết bị cho chủ đầu tư và phát triển hợp tác với các đối tác trong và ngoài nước."],
  edu_h="Học vấn",
  edu=["Tiến sĩ chuyên ngành Máy mỏ – Trường Đại học Mỏ Saint Petersburg, Liên bang Nga",
       "Thạc sĩ Khoa học và Kỹ thuật vật liệu – Đại học Bách khoa Hà Nội (2013)",
       "Kỹ sư Vật liệu học và Nhiệt luyện – Đại học Bách khoa Hà Nội (2006)"],
  exp_h="Lĩnh vực chuyên môn",
  exp=["Máy và thiết bị mỏ, công nghiệp, y tế, phòng thí nghiệm và giáo dục", "Công nghệ vật liệu", "Thí nghiệm – kiểm định", "Tư vấn xây dựng", "Nghiên cứu và phát triển khoa học công nghệ, đổi mới sáng tạo và chuyển đổi số", "Phát triển thị trường sản phẩm kỹ thuật"],
  lang_h="Ngoại ngữ", lang="Tiếng Anh, tiếng Nga"),
 "en": dict(
  h="Leadership",
  name="Dr. Le Thanh Binh", role="Assistant to the General Director",
  bio=["Dr. Le Thanh Binh is Assistant to the General Director of Van Phong Technical and Trading Co., Ltd. He has 20 years of experience in science and technology research, materials technology, construction consulting, testing and inspection, design and manufacture of mechanical equipment for the mining and industrial sectors, and the import–export trade of materials and equipment for industry, healthcare, laboratories and education.",
       "At Van Phong, he supports the General Director on technical matters, construction investment consulting, design, engineering calculations and the selection of equipment solutions for project owners, and develops cooperation with domestic and international partners."],
  edu_h="Education",
  edu=["PhD in Mining Machinery – Saint Petersburg Mining University, Russian Federation",
       "MSc in Materials Science and Engineering – Hanoi University of Science and Technology (2013)",
       "BEng in Materials Science and Heat Treatment – Hanoi University of Science and Technology (2006)"],
  exp_h="Areas of expertise",
  exp=["Machinery and equipment for mining, industry, healthcare, laboratories and education", "Materials technology", "Testing and inspection", "Construction consulting", "Science &amp; technology R&amp;D, innovation and digital transformation", "Market development for engineering products"],
  lang_h="Languages", lang="English, Russian"),
 "zh": dict(
  h="管理团队",
  name="黎清平 博士（Le Thanh Binh）", role="总经理助理",
  bio=["黎清平博士现任 Van Phong 技术与贸易有限公司总经理助理，在科技研究、材料技术、建设咨询、试验检测、矿山及工业机械设备设计制造，以及工业、医疗、实验室和教育用物资设备进出口贸易等领域拥有 20 年经验。",
       "在 Van Phong，他协助总经理处理技术事务，为业主提供建设投资咨询、设计、计算及设备方案选型，并负责拓展与国内外合作伙伴的合作。"],
  edu_h="教育背景",
  edu=["矿山机械专业博士 – 俄罗斯圣彼得堡矿业大学",
       "材料科学与工程硕士 – 河内百科大学（2013）",
       "材料学与热处理工程学士 – 河内百科大学（2006）"],
  exp_h="专业领域",
  exp=["矿山、工业、医疗、实验室及教育机械设备", "材料技术", "试验与检测", "建设咨询", "科技研发、创新与数字化转型", "工程产品市场开发"],
  lang_h="外语", lang="英语、俄语"),
}

CHAIR = {"vi": ("Bà Trần Hoàng Phương", "Chủ tịch Công ty"),
         "en": ("Ms. Tran Hoang Phuong", "Chairperson"),
         "zh": ("陈黄芳 女士（Tran Hoang Phuong）", "董事长")}

GD = {"vi": ("Bà Nguyễn Thị Tám", "Tổng Giám đốc"),
      "en": ("Ms. Nguyen Thi Tam", "General Director"),
      "zh": ("Nguyen Thi Tam 女士", "总经理")}

def block(lang):
    t = L[lang]
    li = lambda xs: "".join(f"<li>{x}</li>" for x in xs)
    return f"""<section id="ban-lanh-dao"><div class="wrap">
  <div class="title"><h2>{t['h']}</h2></div>
  <article class="leader chair">
    <figure><img src="/lanh-dao/tran-hoang-phuong.jpg?v=2" alt="{CHAIR[lang][0]}" width="600" height="600" loading="lazy"></figure>
    <div class="lbody"><h3>{CHAIR[lang][0]}</h3><p class="role">{CHAIR[lang][1]}</p></div>
  </article>
  <article class="leader chair">
    <figure><img src="/lanh-dao/nguyen-thi-tam.jpg?v=2" alt="{GD[lang][0]}" width="600" height="600" loading="lazy"></figure>
    <div class="lbody"><h3>{GD[lang][0]}</h3><p class="role">{GD[lang][1]}</p></div>
  </article>
  <article class="leader">
    <figure><img src="/lanh-dao/le-thanh-binh.jpg?v=3" alt="{t['name']}" width="600" height="600" loading="lazy"></figure>
    <div class="lbody">
      <h3>{t['name']}</h3><p class="role">{t['role']}</p>
      {''.join(f'<p>{p}</p>' for p in t['bio'])}
      <div class="lcols">
        <div><h4>{t['edu_h']}</h4><ul>{li(t['edu'])}</ul></div>
        <div><h4>{t['exp_h']}</h4><ul>{li(t['exp'])}</ul><h4>{t['lang_h']}</h4><p>{t['lang']}</p></div>
      </div>
    </div>
  </article>
</div></section>"""
