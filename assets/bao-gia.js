/* Giỏ yêu cầu báo giá + tài khoản khách hàng (đăng nhập bằng mã gửi qua email, không mật khẩu).
   Backend: Google Apps Script – mã nguồn ở _tools/apps-script/Code.gs. Dán URL web app vào API bên dưới.
   Khi API để trống: yêu cầu báo giá được gửi bằng email (mailto) tới info@, phần lịch sử tạm ẩn. */
(function () {
  'use strict';
  var API = 'https://script.google.com/macros/s/AKfycbwCCPywMCCS0R01K6FAF3luI93BOHVzwc5vlfoPuXNgi0N5Qrr4M6J1N3n3SdR5tZo_/exec';
  var INFO = 'info@vanphongtechco.com.vn';
  var K_CART = 'vp_cart', K_TOK = 'vp_tok', K_PROF = 'vp_prof', K_HIST = 'vp_hist';

  var hl = (document.documentElement.lang || 'vi').toLowerCase();
  var LG = hl.indexOf('zh') === 0 ? 'zh' : hl.indexOf('en') === 0 ? 'en' : 'vi';
  var PRE = LG === 'vi' ? '/' : '/' + LG + '/';

  var S = {
    vi: {
      fab: 'Giỏ báo giá', hCart: 'Giỏ báo giá', hLogin: 'Đăng nhập', hAcc: 'Tài khoản', add: 'Thêm vào báo giá', added: 'Đã thêm ✓', qty: 'SL', qtyL: 'Số lượng',
      tCart: 'Giỏ báo giá', tAcc: 'Đăng nhập / Lịch sử',
      empty: 'Chưa có sản phẩm nào. Bấm “Thêm vào báo giá” ở sản phẩm cần hỏi giá.',
      browse: 'Xem danh mục sản phẩm', remove: 'Xóa',
      name: 'Họ tên', company: 'Đơn vị / Công ty', phone: 'Số điện thoại', email: 'Email', note: 'Ghi chú (yêu cầu kỹ thuật, nơi giao, thời gian…)',
      send: 'Gửi yêu cầu báo giá', sending: 'Đang gửi…',
      sentOk: 'Đã gửi yêu cầu {c}. Vân Phong sẽ phản hồi qua email/điện thoại trong giờ làm việc.',
      sentMail: 'Đã mở ứng dụng email với nội dung yêu cầu. Bấm Gửi trong email để hoàn tất.',
      track: 'Theo dõi yêu cầu này trong mục Tài khoản – chỉ cần nhập email.',
      need: 'Vui lòng nhập họ tên, số điện thoại và email hợp lệ.',
      accIntro: 'Đăng nhập không cần mật khẩu: nhập email, nhận mã 6 số và xem toàn bộ yêu cầu báo giá đã gửi.',
      getCode: 'Nhận mã đăng nhập', codeSent: 'Mã đã gửi tới {e} (kiểm tra cả Spam). Mã có hiệu lực 10 phút.',
      code: 'Mã 6 số', login: 'Đăng nhập', otherEmail: 'Đổi email', logout: 'Đăng xuất',
      hello: 'Đang đăng nhập: {e}', none: 'Chưa có yêu cầu báo giá nào.',
      items: 'mặt hàng', reorder: 'Hỏi giá lại', file: 'Tải báo giá', reply: 'Phản hồi',
      regIntro: 'Đăng ký bằng họ tên, số điện thoại, email và mật khẩu tự đặt – dùng ngay, không cần chờ duyệt. Lần sau đăng nhập bằng email hoặc số điện thoại.', reg: 'Đăng ký / Đăng nhập', regOk: 'Đăng ký thành công. Chọn sản phẩm và gửi yêu cầu báo giá, lịch sử sẽ hiện ở đây.', helloN: 'Xin chào {n}',
      tLogin: 'Đăng nhập', tReg: 'Đăng ký', idL: 'Email hoặc số điện thoại', pw: 'Mật khẩu', pw2: 'Nhập lại mật khẩu', pwNew: 'Mật khẩu mới', pwHint: 'Tối thiểu 6 ký tự',
      forgot: 'Quên mật khẩu?', forgotIntro: 'Nhập email hoặc số điện thoại đã đăng ký. Hệ thống sẽ gửi mật khẩu mới vào email của Quý khách.', forgotBtn: 'Gửi mật khẩu mới', forgotOk: 'Nếu thông tin đã đăng ký, mật khẩu mới đã được gửi tới email của Quý khách (kiểm tra cả Spam).', back: '← Quay lại đăng nhập',
      chg: 'Đổi mật khẩu', chgOk: 'Đã đổi mật khẩu.', noAcc: 'Chưa có tài khoản?', haveAcc: 'Đã có tài khoản?',
      errLogin: 'Sai email/số điện thoại hoặc mật khẩu.', errExists: 'Email hoặc số điện thoại này đã đăng ký. Vui lòng đăng nhập, hoặc bấm “Quên mật khẩu?” để nhận mật khẩu mới qua email.', errPw: 'Mật khẩu tối thiểu 6 ký tự và hai lần nhập phải giống nhau.',
      err: 'Có lỗi kết nối, vui lòng thử lại hoặc gọi 08.9999.0683.',
      errCode: 'Mã không đúng hoặc đã hết hạn.', errRate: 'Bạn thao tác quá nhanh, vui lòng thử lại sau ít phút.',
      expired: 'Phiên đăng nhập đã hết hạn, vui lòng đăng nhập lại.',
      st: { 'Mới': 'Đã nhận', 'Đang xử lý': 'Đang xử lý', 'Đã gửi báo giá': 'Đã gửi báo giá', 'Hoàn tất': 'Hoàn tất', 'Hủy': 'Đã hủy' },
      subj: 'Yêu cầu báo giá từ website', close: 'Đóng'
    },
    en: {
      fab: 'Quote cart', hCart: 'Quote cart', hLogin: 'Sign in', hAcc: 'Account', add: 'Add to quote', added: 'Added ✓', qty: 'Qty', qtyL: 'Quantity',
      tCart: 'Quote cart', tAcc: 'Sign in / History',
      empty: 'No products yet. Click “Add to quote” on the products you need prices for.',
      browse: 'Browse products', remove: 'Remove',
      name: 'Full name', company: 'Organisation / Company', phone: 'Phone', email: 'Email', note: 'Notes (technical requirements, delivery place, timing…)',
      send: 'Send quote request', sending: 'Sending…',
      sentOk: 'Request {c} sent. Van Phong will reply by email/phone during business hours.',
      sentMail: 'Your email app has been opened with the request. Press Send there to finish.',
      track: 'Track this request under Account – just enter your email.',
      need: 'Please enter your name, phone number and a valid email.',
      accIntro: 'No password needed: enter your email, receive a 6-digit code and see all quote requests you have sent.',
      getCode: 'Email me a sign-in code', codeSent: 'Code sent to {e} (check Spam too). Valid for 10 minutes.',
      code: '6-digit code', login: 'Sign in', otherEmail: 'Change email', logout: 'Sign out',
      hello: 'Signed in as {e}', none: 'No quote requests yet.',
      items: 'items', reorder: 'Request again', file: 'Download quotation', reply: 'Reply',
      regIntro: 'Sign up with your name, phone, email and a password of your choice – ready to use immediately. Next time, sign in with your email or phone number.', reg: 'Sign up / Sign in', regOk: 'You are signed up. Add products and send a quote request; your history will appear here.', helloN: 'Hello {n}',
      tLogin: 'Sign in', tReg: 'Sign up', idL: 'Email or phone number', pw: 'Password', pw2: 'Repeat password', pwNew: 'New password', pwHint: 'At least 6 characters',
      forgot: 'Forgot password?', forgotIntro: 'Enter the email or phone number you registered with. A new password will be sent to your email.', forgotBtn: 'Send new password', forgotOk: 'If the details are registered, a new password has been sent to your email (check Spam too).', back: '← Back to sign in',
      chg: 'Change password', chgOk: 'Password changed.', noAcc: 'No account yet?', haveAcc: 'Already have an account?',
      errLogin: 'Wrong email/phone number or password.', errExists: 'This email or phone number is already registered. Please sign in, or click “Forgot password?” to receive a new password by email.', errPw: 'Password must be at least 6 characters and both entries must match.',
      err: 'Connection error, please try again or call +84 899 990 683.',
      errCode: 'Wrong or expired code.', errRate: 'Too many attempts, please try again in a few minutes.',
      expired: 'Your session has expired, please sign in again.',
      st: { 'Mới': 'Received', 'Đang xử lý': 'In progress', 'Đã gửi báo giá': 'Quotation sent', 'Hoàn tất': 'Completed', 'Hủy': 'Cancelled' },
      subj: 'Quote request from website', close: 'Close'
    },
    zh: {
      fab: '询价单', hCart: '询价单', hLogin: '登录', hAcc: '账户', add: '加入询价单', added: '已加入 ✓', qty: '数量', qtyL: '数量',
      tCart: '询价单', tAcc: '登录 / 历史',
      empty: '询价单为空。请在需要报价的产品上点击“加入询价单”。',
      browse: '浏览产品', remove: '删除',
      name: '姓名', company: '单位 / 公司', phone: '电话', email: '邮箱', note: '备注（技术要求、交货地点、时间等）',
      send: '提交询价', sending: '提交中…',
      sentOk: '询价 {c} 已提交。Vân Phong 将在工作时间通过邮件/电话回复。',
      sentMail: '已打开邮件应用，请在邮件中点击发送完成。',
      track: '在“账户”中输入邮箱即可查看此询价。',
      need: '请填写姓名、电话和有效邮箱。',
      accIntro: '无需密码：输入邮箱，接收 6 位验证码，即可查看所有已提交的询价。',
      getCode: '发送登录验证码', codeSent: '验证码已发送至 {e}（请同时查看垃圾邮件），10 分钟内有效。',
      code: '6 位验证码', login: '登录', otherEmail: '更换邮箱', logout: '退出',
      hello: '已登录：{e}', none: '暂无询价记录。',
      items: '项', reorder: '再次询价', file: '下载报价单', reply: '回复',
      regIntro: '填写姓名、电话、邮箱并自设密码即可注册，立即使用。以后可用邮箱或手机号登录。', reg: '注册 / 登录', regOk: '注册成功。选择产品并提交询价，历史记录将显示在这里。', helloN: '您好，{n}',
      tLogin: '登录', tReg: '注册', idL: '邮箱或手机号', pw: '密码', pw2: '再次输入密码', pwNew: '新密码', pwHint: '至少 6 位',
      forgot: '忘记密码？', forgotIntro: '请输入注册时的邮箱或手机号，系统将把新密码发送到您的邮箱。', forgotBtn: '发送新密码', forgotOk: '如信息已注册，新密码已发送至您的邮箱（请同时查看垃圾邮件）。', back: '← 返回登录',
      chg: '修改密码', chgOk: '密码已修改。', noAcc: '还没有账户？', haveAcc: '已有账户？',
      errLogin: '邮箱/手机号或密码错误。', errExists: '该邮箱或手机号已注册。请直接登录，或点击“忘记密码？”通过邮箱获取新密码。', errPw: '密码至少 6 位，且两次输入须一致。',
      err: '连接错误，请重试或致电 +84 899 990 683。',
      errCode: '验证码错误或已过期。', errRate: '操作过于频繁，请稍后再试。',
      expired: '登录已过期，请重新登录。',
      st: { 'Mới': '已收到', 'Đang xử lý': '处理中', 'Đã gửi báo giá': '已报价', 'Hoàn tất': '已完成', 'Hủy': '已取消' },
      subj: '网站询价', close: '关闭'
    }
  }[LG];

  function $(s, r) { return (r || document).querySelector(s); }
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function fmt(s, o) { return s.replace(/\{(\w)\}/g, function (_, k) { return esc(o[k]); }); }
  function ld(k, d) { try { var v = JSON.parse(localStorage.getItem(k)); return v == null ? d : v; } catch (e) { return d; } }
  function sv(k, v) { try { v == null ? localStorage.removeItem(k) : localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} }
  function okEmail(s) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(s); }
  function api(d) {
    return fetch(API, { method: 'POST', body: JSON.stringify(d) }).then(function (r) { return r.json(); });
  }

  var cart = ld(K_CART, []);
  function saveCart() { sv(K_CART, cart); badge(); if (window.__vqhb) window.__vqhb(); }
  function count() { return cart.length; }
  function addItem(it, q) {
    q = Math.max(1, Math.min(9999, parseInt(q, 10) || 1));
    var f = cart.filter(function (x) { return x.s === it.s; })[0];
    if (f) f.q = Math.min(9999, f.q + q); else cart.push({ s: it.s, n: it.n, c: it.c || '', q: q });
    saveCart();
  }

  /* ---------- styles ---------- */
  var css = '.vq-fab{position:fixed;right:20px;bottom:20px;z-index:45;display:flex;align-items:center;gap:8px;background:#F07C1B;color:#fff;border:0;border-radius:24px;padding:11px 16px;font:600 14px/1 inherit;font-family:inherit;box-shadow:0 6px 18px rgba(0,0,0,.18);cursor:pointer}'
    + '.float-stack .vq-fab{position:static}.vq-fab b{background:#fff;color:#F07C1B;border-radius:12px;min-width:22px;padding:3px 6px;font-size:12px;text-align:center}'
    + '.vq-add{display:inline-flex;align-items:center;gap:6px;border:1px solid #F07C1B;color:#F07C1B;background:#fff;border-radius:6px;padding:6px 10px;font:600 13px/1.2 inherit;font-family:inherit;cursor:pointer}.vq-add:hover{background:#FFF4EA}.vq-add.ok{background:#F07C1B;color:#fff}'
    + '.vq-row{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:10px 0}.vq-row input{width:72px;padding:9px 8px;border:1px solid #D5DBE3;border-radius:6px;font:inherit}.vq-row .vq-add{padding:11px 16px;font-size:15px}'
    + '.card .foot .vq-add{margin-left:auto}'
    + '.vq-ov{position:fixed;inset:0;z-index:200;background:rgba(10,20,35,.55);display:none;justify-content:flex-end}.vq-ov.open{display:flex}'
    + '.vq-pn{background:#fff;width:min(460px,100%);height:100%;display:flex;flex-direction:column;font-size:15px;color:#1B2430}'
    + '.vq-hd{display:flex;align-items:center;border-bottom:1px solid #E3E8EE}.vq-hd button{flex:1;border:0;background:none;padding:15px 8px;font:600 15px inherit;font-family:inherit;color:#6B7684;cursor:pointer;border-bottom:3px solid transparent}.vq-hd button.on{color:#0E2F5A;border-color:#F07C1B}.vq-hd .vq-x{flex:0 0 48px;font-size:24px}'
    + '.vq-bd{flex:1;overflow:auto;padding:16px}.vq-bd label{display:block;font-size:13px;color:#6B7684;margin:10px 0 4px}.vq-bd input,.vq-bd textarea{width:100%;box-sizing:border-box;padding:10px;border:1px solid #D5DBE3;border-radius:6px;font:inherit}.vq-bd textarea{min-height:70px}'
    + '.vq-it{display:grid;grid-template-columns:1fr 70px 28px;gap:8px;align-items:center;padding:10px 0;border-bottom:1px solid #EEF1F5}.vq-it a{color:#0E2F5A;font-weight:600}.vq-it small{display:block;color:#6B7684}.vq-it input{padding:7px;text-align:center}.vq-it button{border:0;background:none;font-size:20px;color:#9AA4B1;cursor:pointer}'
    + '.vq-btn{display:block;width:100%;margin-top:14px;border:0;border-radius:6px;background:#F07C1B;color:#fff;padding:13px;font:700 15px inherit;font-family:inherit;cursor:pointer}.vq-btn[disabled]{opacity:.6}.vq-btn.sec{background:#fff;color:#0E2F5A;border:1px solid #D5DBE3}'
    + '.vq-msg{padding:10px 12px;border-radius:6px;background:#EEF5FF;color:#0E2F5A;margin:10px 0;font-size:14px}.vq-msg.bad{background:#FFF0F0;color:#A01818}.vq-mute{color:#6B7684;font-size:14px}.vq-hp{position:absolute;left:-9999px}'
    + '.vq-q{border:1px solid #E3E8EE;border-radius:8px;padding:12px;margin:10px 0}.vq-q h5{margin:0 0 4px;font-size:15px;display:flex;justify-content:space-between;gap:8px}.vq-q ul{margin:6px 0;padding-left:18px;font-size:14px}.vq-st{font-size:12px;font-weight:700;padding:3px 8px;border-radius:10px;background:#FFF4EA;color:#B85A0B;white-space:nowrap}.vq-st.s2,.vq-st.s3{background:#E9F7EF;color:#17733D}.vq-st.s4{background:#F1F2F4;color:#6B7684}'
    + '.vq-q .vq-a{display:flex;gap:12px;flex-wrap:wrap;font-size:14px}.vq-q .vq-a a,.vq-q .vq-a button{color:#2F6FB7;font-weight:600;background:none;border:0;padding:0;font:inherit;cursor:pointer}';
  css += '.vq-hb{display:flex;gap:8px;align-items:center;margin-left:12px;flex-shrink:0}.vq-hb button{display:inline-flex;align-items:center;gap:6px;border:1px solid #D5DBE3;background:#fff;color:#0E2F5A;border-radius:20px;padding:7px 12px;font:600 13px/1 inherit;font-family:inherit;cursor:pointer;white-space:nowrap}.vq-hb button:hover{border-color:#F07C1B;color:#F07C1B}.vq-hb .vq-hc{background:#F07C1B;border-color:#F07C1B;color:#fff}.vq-hb .vq-hc:hover{color:#fff;background:#D96A0E}.vq-hb b{background:#fff;color:#F07C1B;border-radius:10px;padding:2px 6px;font-size:11px}.vq-hb svg{width:16px;height:16px;fill:currentColor}'
    + '.vq-idx{align-self:center;margin:0 -4px 0 0;gap:6px}.vq-idx .t{display:none}.vq-idx button{padding:8px 10px}.vq-top{display:none}'
    + '@media (max-width:1100px){.vq-idx{display:none}.vq-top{display:flex}}@media (max-width:900px){.vq-top{margin:0 auto}}'
    + '@media (max-width:760px){.vq-hb:not(.vq-top){margin-left:auto;gap:6px}.vq-hb:not(.vq-top) button{padding:7px 9px}.vq-hb:not(.vq-top) .t{display:none}}';
  css += '.vq-av{display:inline-grid;place-items:center;width:22px;height:22px;border-radius:50%;background:#1580BF;color:#fff;font:700 12px/1 inherit;font-family:inherit;font-style:normal;margin:-3px 0 -3px -4px}.vq-hb .vq-hu.in{border-color:#1580BF}'
    + '.vq-tabs{display:flex;gap:6px;margin-bottom:6px}.vq-tabs button{flex:1;border:1px solid #D5DBE3;background:#fff;border-radius:6px;padding:9px;font:600 14px inherit;font-family:inherit;color:#6B7684;cursor:pointer}.vq-tabs button.on{background:#0E2F5A;border-color:#0E2F5A;color:#fff}'
    + '.vq-lnk{background:none;border:0;padding:0;color:#2F6FB7;font:600 14px inherit;font-family:inherit;cursor:pointer;margin-top:12px}.vq-me{display:flex;align-items:center;gap:12px;margin-bottom:8px}.vq-me .vq-av{width:44px;height:44px;font-size:20px;margin:0}.vq-me b{display:block;color:#0E2F5A;font-size:16px}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  /* ---------- floating button + panel ---------- */
  var fab = document.createElement('button');
  fab.type = 'button'; fab.className = 'vq-fab'; fab.setAttribute('aria-haspopup', 'dialog');
  function badge() { fab.innerHTML = '🧾 ' + esc(S.fab) + ' <b>' + count() + '</b>'; }
  badge();
  var HBS = [];
  function mkHb(cls) {
    var hb = document.createElement('div'); hb.className = 'vq-hb ' + (cls || '');
    hb.innerHTML = '<button type="button" class="vq-hc" title="' + esc(S.hCart) + '"><svg viewBox="0 0 24 24"><path d="M7 18a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm10 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4zM5.2 4H2V2h4.6l.9 2H22l-3.4 8.2a2 2 0 0 1-1.8 1.3H8.3l-1 1.8H20v2H4l2.6-4.6z"/></svg><span class="t">' + esc(S.hCart) + '</span> <b>0</b></button>'
      + '<button type="button" class="vq-hu" title="' + esc(S.hLogin) + ' / ' + esc(S.hAcc) + '"><svg viewBox="0 0 24 24"><path d="M12 12a5 5 0 1 0 0-10 5 5 0 0 0 0 10zm0 2c-4.4 0-9 2.2-9 5v3h18v-3c0-2.8-4.6-5-9-5z"/></svg><span class="t"></span></button>';
    hb.querySelector('.vq-hc').onclick = function () { open('cart'); };
    hb.querySelector('.vq-hu').onclick = function () { open('acc'); };
    HBS.push(hb); return hb;
  }
  var nm = document.querySelector('header nav.main'), top = document.querySelector('.top .wrap');
  if (nm) {                                   // trang chủ: nút trong thanh menu (desktop) + thanh xám trên cùng (mobile)
    nm.parentNode.insertBefore(mkHb('vq-idx'), nm.nextSibling);
    if (top) top.appendChild(mkHb('vq-top'));
  } else { var hn = document.querySelector('header nav'); if (hn) hn.insertBefore(mkHb(), hn.querySelector('.langs')); }
  function hbar() {
    var t = ld(K_TOK, null);
    var pf = ld(K_PROF, {}), nmF = (pf.name || '').trim(), first = t ? (nmF.split(/\s+/).pop() || t.e.split('@')[0]) : '';
    HBS.forEach(function (hb) {
      hb.querySelector('.vq-hc b').textContent = count();
      var u = hb.querySelector('.vq-hu'), sv0 = u.querySelector('svg'), av = u.querySelector('.vq-av');
      u.querySelector('.t').textContent = t ? first : S.hLogin;
      if (t) {
        if (!av) { av = document.createElement('i'); av.className = 'vq-av'; u.insertBefore(av, u.firstChild); }
        av.textContent = (first || '?').charAt(0).toUpperCase(); sv0.style.display = 'none'; u.classList.add('in');
        u.title = (nmF || t.e) + ' · ' + S.hAcc;
      } else { if (av) av.remove(); sv0.style.display = ''; u.classList.remove('in'); u.title = S.hLogin; }
    });
  }
  window.__vqhb = hbar; hbar();
  var stack = document.getElementById('fstack');
  if (stack) stack.insertBefore(fab, stack.firstChild); else document.body.appendChild(fab);

  var ov = document.createElement('div');
  ov.className = 'vq-ov'; ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true');
  ov.innerHTML = '<div class="vq-pn"><div class="vq-hd"><button type="button" data-tab="cart">' + esc(S.tCart) + '</button><button type="button" data-tab="acc">' + esc(S.tAcc) + '</button><button type="button" class="vq-x" aria-label="' + esc(S.close) + '">×</button></div><div class="vq-bd"></div></div>';
  document.body.appendChild(ov);
  var bd = $('.vq-bd', ov), tab = 'cart', note = '';
  function open(t) { tab = t || 'cart'; ov.classList.add('open'); document.body.style.overflow = 'hidden'; render(); }
  function close() { ov.classList.remove('open'); document.body.style.overflow = ''; note = ''; hbar(); }
  fab.onclick = function () { open('cart'); };
  ov.addEventListener('click', function (e) {
    if (e.target === ov || e.target.closest('.vq-x')) return close();
    var t = e.target.closest('[data-tab]'); if (t) { tab = t.dataset.tab; note = ''; render(); }
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && ov.classList.contains('open')) close(); });
  if (location.hash === '#bao-gia-cua-toi') setTimeout(function () { open('acc'); }, 50);

  function render() {
    [].forEach.call(ov.querySelectorAll('[data-tab]'), function (b) { b.classList.toggle('on', b.dataset.tab === tab); });
    tab === 'cart' ? renderCart() : renderAcc();
  }
  function msg() { return note ? '<div class="vq-msg' + (note.bad ? ' bad' : '') + '">' + note.h + '</div>' : ''; }
  function say(h, bad) { note = { h: h, bad: !!bad }; }

  function renderCart() {
    var p = ld(K_PROF, {}), tok = ld(K_TOK, null);
    if (!cart.length) { bd.innerHTML = msg() + '<p class="vq-mute">' + esc(S.empty) + '</p><a class="vq-btn sec" style="text-align:center;text-decoration:none" href="' + PRE + 'san-pham/">' + esc(S.browse) + '</a>'; return; }
    bd.innerHTML = msg() + cart.map(function (x, i) {
      return '<div class="vq-it"><div><a href="' + PRE + 'san-pham/' + encodeURIComponent(x.s) + '/">' + esc(x.n) + '</a>' + (x.c ? '<small>' + esc(x.c) + '</small>' : '') + '</div>'
        + '<input type="number" min="1" max="9999" value="' + x.q + '" data-i="' + i + '" aria-label="' + esc(S.qtyL) + '"><button type="button" data-rm="' + i + '" aria-label="' + esc(S.remove) + '">×</button></div>';
    }).join('')
      + '<form class="vq-f"><input class="vq-hp" name="hp" tabindex="-1" autocomplete="off">'
      + '<label>' + esc(S.name) + ' *</label><input name="name" required autocomplete="name" value="' + esc(p.name) + '">'
      + '<label>' + esc(S.company) + '</label><input name="company" autocomplete="organization" value="' + esc(p.company) + '">'
      + '<label>' + esc(S.phone) + ' *</label><input name="phone" type="tel" required autocomplete="tel" value="' + esc(p.phone) + '">'
      + '<label>' + esc(S.email) + ' *</label><input name="email" type="email" required autocomplete="email" value="' + esc(tok ? tok.e : p.email) + '"' + (tok ? ' readonly' : '') + '>'
      + '<label>' + esc(S.note) + '</label><textarea name="note"></textarea>'
      + '<button class="vq-btn" type="submit">' + esc(S.send) + '</button></form>';
    [].forEach.call(bd.querySelectorAll('[data-i]'), function (inp) {
      inp.onchange = function () { var v = Math.max(1, Math.min(9999, parseInt(inp.value, 10) || 1)); inp.value = v; cart[+inp.dataset.i].q = v; saveCart(); };
    });
    [].forEach.call(bd.querySelectorAll('[data-rm]'), function (b) { b.onclick = function () { cart.splice(+b.dataset.rm, 1); saveCart(); note = ''; renderCart(); }; });
    $('.vq-f', bd).onsubmit = submit;
  }

  function submit(e) {
    e.preventDefault();
    var f = e.target, g = function (n) { return (f.elements[n].value || '').trim(); };
    var d = { name: g('name'), company: g('company'), phone: g('phone'), email: g('email').toLowerCase(), note: g('note'), hp: g('hp') };
    if (!d.name || d.phone.replace(/\D/g, '').length < 8 || !okEmail(d.email)) { say(esc(S.need), 1); return renderCart(); }
    var prof = { name: d.name, company: d.company, phone: d.phone, email: d.email };
    sv(K_PROF, prof);
    var items = cart.map(function (x) { return { s: x.s, n: x.n, c: x.c, q: x.q }; });
    if (!API) {
      var body = S.tCart + ':\n' + items.map(function (x, i) { return (i + 1) + '. ' + x.n + (x.c && x.n.indexOf(x.c) < 0 ? ' (' + x.c + ')' : '') + ' – ' + S.qty + ': ' + x.q; }).join('\n')
        + '\n\n' + S.name + ': ' + d.name + (d.company ? '\n' + S.company + ': ' + d.company : '') + '\n' + S.phone + ': ' + d.phone + '\n' + S.email + ': ' + d.email + (d.note ? '\n\n' + d.note : '') + '\n\n' + location.href;
      var now = new Date(), p2 = function (n) { return ('0' + n).slice(-2); };
      var code = 'YC' + String(now.getFullYear()).slice(2) + p2(now.getMonth() + 1) + p2(now.getDate()) + '-' + p2(now.getHours()) + p2(now.getMinutes());
      var H = ld(K_HIST, {}); (H[d.email] = H[d.email] || []).unshift({ code: code, time: p2(now.getDate()) + '/' + p2(now.getMonth() + 1) + '/' + now.getFullYear() + ' ' + p2(now.getHours()) + ':' + p2(now.getMinutes()), status: 'Mới', items: items, note: d.note });
      sv(K_HIST, H);
      if (!ld(K_TOK, null)) sv(K_TOK, { t: '', e: d.email, local: 1 });
      location.href = 'mailto:' + INFO + '?subject=' + encodeURIComponent(S.subj + ' ' + code + ' – ' + d.name) + '&body=' + encodeURIComponent(code + '\n' + body);
      cart = []; saveCart(); hbar(); say(fmt(S.sentOk, { c: code }) + '<br>' + esc(S.sentMail)); return renderCart();
    }
    var btn = $('button[type=submit]', f); btn.disabled = true; btn.textContent = S.sending;
    var tok = ld(K_TOK, null);
    d.action = 'submitQuote'; d.items = items; d.lang = LG; d.page = location.href; if (tok) d.token = tok.t;
    api(d).then(function (r) {
      if (!r.ok) throw r;
      cart = []; saveCart();
      say(fmt(S.sentOk, { c: r.code }) + (tok ? '' : '<br>' + esc(S.track)));
      renderCart();
    }).catch(function (r) {
      say(esc(r && r.err === 'rate' ? S.errRate : S.err), 1); renderCart();
    });
  }

  /* ---------- account (email/SĐT + mật khẩu) ---------- */
  var amode = 'login';
  function pwField(n, l, ac) { return '<label>' + esc(l) + ' *</label><input name="' + n + '" type="password" required minlength="6" autocomplete="' + ac + '">'; }
  function busy(f) { var b = $('button[type=submit]', f); b.disabled = true; b.textContent = S.sending; }
  function errMsg(r) { var k = r && r.err; return esc(k === 'rate' ? S.errRate : k === 'login' ? S.errLogin : k === 'exists' ? S.errExists : k === 'pw' ? S.errPw : k === 'input' ? S.need : S.err); }
  function signedIn(r, em) {
    sv(K_TOK, { t: r.token, e: em });
    sv(K_PROF, Object.assign(ld(K_PROF, {}), r.profile || {}, { email: em }));
    hbar();
  }
  function renderAcc() {
    if (!API) return renderLocal();
    var tok = ld(K_TOK, null);
    if (tok && !tok.t) { sv(K_TOK, null); tok = null; }
    if (!tok) {
      var p0 = ld(K_PROF, {});
      var tabs = '<div class="vq-tabs"><button type="button" data-m="login" class="' + (amode === 'login' ? 'on' : '') + '">' + esc(S.tLogin) + '</button><button type="button" data-m="reg" class="' + (amode === 'reg' ? 'on' : '') + '">' + esc(S.tReg) + '</button></div>';
      if (amode === 'forgot') {
        bd.innerHTML = msg() + '<p class="vq-mute">' + esc(S.forgotIntro) + '</p><form class="vq-fg"><label>' + esc(S.idL) + '</label><input name="id" required autocomplete="username" value="' + esc(p0.email || p0.phone) + '"><button class="vq-btn" type="submit">' + esc(S.forgotBtn) + '</button></form><button type="button" class="vq-lnk" data-m="login">' + esc(S.back) + '</button>';
        $('.vq-fg', bd).onsubmit = function (e) {
          e.preventDefault(); var f = e.target; busy(f);
          api({ action: 'forgot', id: f.id.value.trim(), lang: LG }).then(function (r) {
            if (!r.ok) throw r; amode = 'login'; say(esc(S.forgotOk)); renderAcc();
          }).catch(function (r) { say(errMsg(r), 1); renderAcc(); });
        };
      } else if (amode === 'reg') {
        bd.innerHTML = tabs + msg() + '<p class="vq-mute">' + esc(S.regIntro) + '</p><form class="vq-r">'
          + '<label>' + esc(S.name) + ' *</label><input name="name" required autocomplete="name" value="' + esc(p0.name) + '">'
          + '<label>' + esc(S.phone) + ' *</label><input name="phone" type="tel" required autocomplete="tel" value="' + esc(p0.phone) + '">'
          + '<label>' + esc(S.email) + ' *</label><input name="email" type="email" required autocomplete="email" value="' + esc(p0.email) + '">'
          + '<label>' + esc(S.company) + '</label><input name="company" autocomplete="organization" value="' + esc(p0.company) + '">'
          + pwField('pw', S.pw + ' (' + S.pwHint + ')', 'new-password') + pwField('pw2', S.pw2, 'new-password')
          + '<input class="vq-hp" name="hp" tabindex="-1" autocomplete="off"><button class="vq-btn" type="submit">' + esc(S.tReg) + '</button></form>'
          + '<p class="vq-mute" style="margin-top:12px">' + esc(S.haveAcc) + ' <button type="button" class="vq-lnk" style="margin:0" data-m="login">' + esc(S.tLogin) + '</button></p>';
        $('.vq-r', bd).onsubmit = function (e) {
          e.preventDefault(); var f = e.target, g = function (n) { return f.elements[n].value.trim(); };
          var d = { action: 'register', name: g('name'), phone: g('phone'), email: g('email').toLowerCase(), company: g('company'), pw: f.pw.value, hp: g('hp'), lang: LG };
          if (!d.name || d.phone.replace(/\D/g, '').length < 8 || !okEmail(d.email)) { say(esc(S.need), 1); return renderAcc(); }
          if (d.pw.length < 6 || d.pw !== f.pw2.value) { say(esc(S.errPw), 1); return renderAcc(); }
          sv(K_PROF, { name: d.name, phone: d.phone, email: d.email, company: d.company });
          busy(f);
          api(d).then(function (r) {
            if (!r.ok) throw r; signedIn(r, d.email); say(esc(S.regOk)); renderAcc();
          }).catch(function (r) { if (r && r.err === 'exists') amode = 'login'; say(errMsg(r), 1); renderAcc(); });
        };
      } else {
        bd.innerHTML = tabs + msg() + '<form class="vq-l"><label>' + esc(S.idL) + '</label><input name="id" required autocomplete="username" value="' + esc(p0.email || p0.phone) + '">'
          + pwField('pw', S.pw, 'current-password') + '<button class="vq-btn" type="submit">' + esc(S.tLogin) + '</button></form>'
          + '<button type="button" class="vq-lnk" data-m="forgot">' + esc(S.forgot) + '</button>'
          + '<p class="vq-mute" style="margin-top:12px">' + esc(S.noAcc) + ' <button type="button" class="vq-lnk" style="margin:0" data-m="reg">' + esc(S.tReg) + '</button></p>';
        $('.vq-l', bd).onsubmit = function (e) {
          e.preventDefault(); var f = e.target, id = f.id.value.trim(); busy(f);
          api({ action: 'login', id: id, pw: f.pw.value }).then(function (r) {
            if (!r.ok) throw r; signedIn(r, (r.profile && r.profile.email || id).toLowerCase()); note = ''; renderAcc();
          }).catch(function (r) { say(errMsg(r), 1); renderAcc(); });
        };
      }
      [].forEach.call(bd.querySelectorAll('[data-m]'), function (b) { b.onclick = function () { amode = b.dataset.m; note = ''; renderAcc(); }; });
      return;
    }
    var pf = ld(K_PROF, {}), nmF = pf.name || tok.e, first = (pf.name || '').trim().split(/\s+/).pop() || tok.e;
    if (amode === 'chg') {
      bd.innerHTML = msg() + '<form class="vq-c">' + pwField('pw', S.pw, 'current-password') + pwField('npw', S.pwNew + ' (' + S.pwHint + ')', 'new-password') + pwField('npw2', S.pw2, 'new-password')
        + '<button class="vq-btn" type="submit">' + esc(S.chg) + '</button></form><button type="button" class="vq-lnk" data-back>' + esc(S.back.replace(/đăng nhập|sign in|登录/i, S.hAcc)) + '</button>';
      $('[data-back]', bd).onclick = function () { amode = 'login'; note = ''; renderAcc(); };
      $('.vq-c', bd).onsubmit = function (e) {
        e.preventDefault(); var f = e.target;
        if (f.npw.value.length < 6 || f.npw.value !== f.npw2.value) { say(esc(S.errPw), 1); return renderAcc(); }
        busy(f);
        api({ action: 'changePw', token: tok.t, pw: f.pw.value, npw: f.npw.value }).then(function (r) {
          if (!r.ok) { if (r.err === 'auth') { sv(K_TOK, null); hbar(); } throw r; } amode = 'login'; say(esc(S.chgOk)); renderAcc();
        }).catch(function (r) { say(r && r.err === 'auth' ? esc(S.expired) : errMsg(r), 1); renderAcc(); });
      };
      return;
    }
    bd.innerHTML = msg() + '<div class="vq-me"><i class="vq-av">' + esc(first.charAt(0).toUpperCase()) + '</i><div><b>' + esc(nmF) + '</b><span class="vq-mute">' + esc(tok.e) + (pf.phone ? ' · ' + esc(pf.phone) : '') + '</span></div></div>'
      + '<p class="vq-mute"><a href="#" data-chg>' + esc(S.chg) + '</a> · <a href="#" data-out>' + esc(S.logout) + '</a></p><div class="vq-list"><p class="vq-mute">…</p></div>';
    $('[data-out]', bd).onclick = function (e) { e.preventDefault(); sv(K_TOK, null); amode = 'login'; note = ''; hbar(); renderAcc(); };
    $('[data-chg]', bd).onclick = function (e) { e.preventDefault(); amode = 'chg'; note = ''; renderAcc(); };
    api({ action: 'myQuotes', token: tok.t }).then(function (r) {
      if (!r.ok) { if (r.err === 'auth') { sv(K_TOK, null); hbar(); say(esc(S.expired), 1); return renderAcc(); } throw r; }
      var L = $('.vq-list', bd); if (!L) return;
      L.innerHTML = quoteCards(r.quotes); bindReorder(L, r.quotes);
    }).catch(function () { var L = $('.vq-list', bd); if (L) L.innerHTML = '<div class="vq-msg bad">' + esc(S.err) + '</div>'; });
  }

  function quoteCards(list) {
    return list.length ? list.map(function (q, qi) {
      var k = ['Mới', 'Đang xử lý', 'Đã gửi báo giá', 'Hoàn tất', 'Hủy'].indexOf(q.status);
      return '<div class="vq-q"><h5><span>' + esc(q.code) + '</span><span class="vq-st s' + k + '">' + esc(S.st[q.status] || q.status || S.st['Mới']) + '</span></h5>'
        + '<div class="vq-mute">' + esc(q.time) + ' · ' + q.items.length + ' ' + esc(S.items) + '</div>'
        + '<ul>' + q.items.map(function (x) { return '<li>' + esc(x.n) + ' × ' + esc(x.q) + '</li>'; }).join('') + '</ul>'
        + (q.reply ? '<div class="vq-msg"><b>' + esc(S.reply) + ':</b> ' + esc(q.reply) + '</div>' : '')
        + '<div class="vq-a">' + (/^https:\/\//.test(q.file || '') ? '<a href="' + esc(q.file) + '" target="_blank" rel="noopener">' + esc(S.file) + '</a>' : '')
        + '<button type="button" data-re="' + qi + '">' + esc(S.reorder) + '</button></div></div>';
    }).join('') : '<p class="vq-mute">' + esc(S.none) + '</p>';
  }
  function bindReorder(root, list) {
    [].forEach.call(root.querySelectorAll('[data-re]'), function (b) {
      b.onclick = function () { list[+b.dataset.re].items.forEach(function (x) { if (x.s) addItem(x, x.q); }); note = ''; open('cart'); };
    });
  }
  // Tài khoản đơn giản (chưa có backend): đăng ký họ tên + SĐT + email là dùng được ngay, lịch sử lưu trên trình duyệt này.
  function renderLocal() {
    var tok = ld(K_TOK, null), p = ld(K_PROF, {});
    if (!tok) {
      bd.innerHTML = msg() + '<p class="vq-mute">' + esc(S.regIntro) + '</p><form class="vq-r">'
        + '<label>' + esc(S.name) + ' *</label><input name="name" required autocomplete="name" value="' + esc(p.name) + '">'
        + '<label>' + esc(S.phone) + ' *</label><input name="phone" type="tel" required autocomplete="tel" value="' + esc(p.phone) + '">'
        + '<label>' + esc(S.email) + ' *</label><input name="email" type="email" required autocomplete="email" value="' + esc(p.email) + '">'
        + '<label>' + esc(S.company) + '</label><input name="company" autocomplete="organization" value="' + esc(p.company) + '">'
        + '<button class="vq-btn" type="submit">' + esc(S.reg) + '</button></form>';
      $('.vq-r', bd).onsubmit = function (e) {
        e.preventDefault(); var f = e.target, g = function (n) { return f.elements[n].value.trim(); };
        var d = { name: g('name'), phone: g('phone'), email: g('email').toLowerCase(), company: g('company') };
        if (!d.name || d.phone.replace(/\D/g, '').length < 8 || !okEmail(d.email)) { say(esc(S.need), 1); return renderLocal(); }
        sv(K_PROF, d); sv(K_TOK, { t: '', e: d.email, local: 1 }); say(esc(S.regOk)); hbar(); renderLocal();
      };
      return;
    }
    var list = ld(K_HIST, {})[tok.e] || [];
    bd.innerHTML = msg() + '<p class="vq-mute">' + fmt(S.helloN, { n: p.name || tok.e }) + ' · ' + esc(tok.e) + (p.phone ? ' · ' + esc(p.phone) : '') + ' · <a href="#" data-out>' + esc(S.logout) + '</a></p><div class="vq-list">' + quoteCards(list) + '</div>';
    $('[data-out]', bd).onclick = function (e) { e.preventDefault(); sv(K_TOK, null); note = ''; hbar(); renderLocal(); };
    bindReorder(bd, list);
  }

  /* ---------- "Add to quote" buttons ---------- */
  function addBtn(it, getQ) {
    var b = document.createElement('button'); b.type = 'button'; b.className = 'vq-add'; b.textContent = '+ ' + S.add;
    b.onclick = function (e) {
      e.preventDefault(); addItem(it, getQ ? getQ() : 1);
      b.classList.add('ok'); b.textContent = S.added;
      setTimeout(function () { b.classList.remove('ok'); b.textContent = '+ ' + S.add; }, 1600);
    };
    return b;
  }
  function slugOf(href) { var m = /(?:^|\/)san-pham\/([^\/?#]+)\/?/.exec(href || ''); return m ? decodeURIComponent(m[1]) : ''; }

  // Product detail page
  var m = /\/san-pham\/([^\/]+)\/?$/.exec(location.pathname);
  var h1 = $('.pd h1');
  if (m && h1) {
    var cta = $('.pd .btn.cta'), dd = $('.pd dl dd');
    var it = { s: decodeURIComponent(m[1]), n: h1.textContent.trim(), c: dd && $('.pd dl dt') && /model|型号/i.test($('.pd dl dt').textContent) ? dd.textContent.trim() : '' };
    var row = document.createElement('div'); row.className = 'vq-row';
    var qi = document.createElement('input'); qi.type = 'number'; qi.min = 1; qi.max = 9999; qi.value = 1; qi.setAttribute('aria-label', S.qtyL);
    row.appendChild(qi); row.appendChild(addBtn(it, function () { return qi.value; }));
    var anchor = cta ? cta.parentNode : h1;
    anchor.parentNode.insertBefore(row, anchor.nextSibling);
  }

  // Homepage product grid (re-rendered on filter / paging)
  function decorate(root) {
    [].forEach.call((root || document).querySelectorAll('.card .foot'), function (ft) {
      if (ft.querySelector('.vq-add')) return;
      var card = ft.closest('.card'), a = card.querySelector('h4 a'); if (!a) return;
      var s = slugOf(a.getAttribute('href')); if (!s) return;
      var c = ft.querySelector('.code');
      ft.appendChild(addBtn({ s: s, n: a.textContent.trim(), c: c ? c.textContent.trim() : '' }));
    });
  }
  var grid = document.getElementById('grid');
  if (grid) { decorate(grid); new MutationObserver(function () { decorate(grid); }).observe(grid, { childList: true }); }

  window.addEventListener('storage', function (e) { if (e.key === K_CART) { cart = ld(K_CART, []); badge(); } hbar(); });
})();
