/* Giỏ yêu cầu báo giá + tài khoản khách hàng (đăng nhập bằng mã gửi qua email, không mật khẩu).
   Backend: Google Apps Script – mã nguồn ở _tools/apps-script/Code.gs. Dán URL web app vào API bên dưới.
   Khi API để trống: yêu cầu báo giá được gửi bằng email (mailto) tới info@, phần lịch sử tạm ẩn. */
(function () {
  'use strict';
  var API = '';
  var INFO = 'info@vanphongtechco.com.vn';
  var K_CART = 'vp_cart', K_TOK = 'vp_tok', K_PROF = 'vp_prof';

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
      offline: 'Tính năng tài khoản đang được kích hoạt. Trong lúc chờ, vui lòng gọi 08.9999.0683 hoặc email ' + INFO + '.',
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
      offline: 'Accounts are being activated. Meanwhile please call +84 899 990 683 or email ' + INFO + '.',
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
      offline: '账户功能正在开通。请致电 +84 899 990 683 或发邮件至 ' + INFO + '。',
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
    HBS.forEach(function (hb) { hb.querySelector('.vq-hc b').textContent = count(); hb.querySelector('.vq-hu .t').textContent = t ? t.e.split('@')[0] : S.hLogin; });
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
      location.href = 'mailto:' + INFO + '?subject=' + encodeURIComponent(S.subj + ' – ' + d.name) + '&body=' + encodeURIComponent(body);
      cart = []; saveCart(); say(esc(S.sentMail)); return renderCart();
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

  /* ---------- account ---------- */
  var pend = null; // email awaiting code
  function renderAcc() {
    if (!API) { bd.innerHTML = '<div class="vq-msg">' + esc(S.offline) + '</div>'; return; }
    var tok = ld(K_TOK, null);
    if (!tok) {
      if (!pend) {
        bd.innerHTML = msg() + '<p class="vq-mute">' + esc(S.accIntro) + '</p><form class="vq-l"><label>' + esc(S.email) + '</label><input name="email" type="email" required autocomplete="email" value="' + esc(ld(K_PROF, {}).email) + '"><input class="vq-hp" name="hp" tabindex="-1" autocomplete="off"><button class="vq-btn" type="submit">' + esc(S.getCode) + '</button></form>';
        $('.vq-l', bd).onsubmit = function (e) {
          e.preventDefault(); var em = e.target.email.value.trim().toLowerCase(); if (!okEmail(em)) return;
          var b = $('button', e.target); b.disabled = true; b.textContent = S.sending;
          api({ action: 'requestCode', email: em, lang: LG, hp: e.target.hp.value }).then(function (r) {
            if (!r.ok) throw r; pend = em; say(fmt(S.codeSent, { e: em })); renderAcc();
          }).catch(function (r) { say(esc(r && r.err === 'rate' ? S.errRate : S.err), 1); renderAcc(); });
        };
      } else {
        bd.innerHTML = msg() + '<form class="vq-v"><label>' + esc(S.code) + '</label><input name="code" inputmode="numeric" autocomplete="one-time-code" maxlength="6" pattern="[0-9]{6}" required><button class="vq-btn" type="submit">' + esc(S.login) + '</button><button class="vq-btn sec" type="button" data-other>' + esc(S.otherEmail) + '</button></form>';
        $('[data-other]', bd).onclick = function () { pend = null; note = ''; renderAcc(); };
        var ci = $('input', bd); ci.focus();
        $('.vq-v', bd).onsubmit = function (e) {
          e.preventDefault(); var b = $('button', e.target); b.disabled = true;
          api({ action: 'verify', email: pend, code: ci.value.trim() }).then(function (r) {
            if (!r.ok) throw r;
            sv(K_TOK, { t: r.token, e: pend });
            if (r.profile) sv(K_PROF, Object.assign(ld(K_PROF, {}), r.profile, { email: pend }));
            pend = null; note = ''; hbar(); renderAcc();
          }).catch(function (r) { say(esc(r && r.err === 'code' ? S.errCode : r && r.err === 'rate' ? S.errRate : S.err), 1); renderAcc(); });
        };
      }
      return;
    }
    bd.innerHTML = '<p class="vq-mute">' + fmt(S.hello, { e: tok.e }) + ' · <a href="#" data-out>' + esc(S.logout) + '</a></p><div class="vq-list"><p class="vq-mute">…</p></div>';
    $('[data-out]', bd).onclick = function (e) { e.preventDefault(); sv(K_TOK, null); note = ''; hbar(); renderAcc(); };
    api({ action: 'myQuotes', token: tok.t }).then(function (r) {
      if (!r.ok) { if (r.err === 'auth') { sv(K_TOK, null); say(esc(S.expired), 1); return renderAcc(); } throw r; }
      var L = $('.vq-list', bd); if (!L) return;
      L.innerHTML = r.quotes.length ? r.quotes.map(function (q, qi) {
        var k = ['Mới', 'Đang xử lý', 'Đã gửi báo giá', 'Hoàn tất', 'Hủy'].indexOf(q.status);
        return '<div class="vq-q"><h5><span>' + esc(q.code) + '</span><span class="vq-st s' + k + '">' + esc(S.st[q.status] || q.status || S.st['Mới']) + '</span></h5>'
          + '<div class="vq-mute">' + esc(q.time) + ' · ' + q.items.length + ' ' + esc(S.items) + '</div>'
          + '<ul>' + q.items.map(function (x) { return '<li>' + esc(x.n) + ' × ' + esc(x.q) + '</li>'; }).join('') + '</ul>'
          + (q.reply ? '<div class="vq-msg"><b>' + esc(S.reply) + ':</b> ' + esc(q.reply) + '</div>' : '')
          + '<div class="vq-a">' + (/^https:\/\//.test(q.file || '') ? '<a href="' + esc(q.file) + '" target="_blank" rel="noopener">' + esc(S.file) + '</a>' : '')
          + '<button type="button" data-re="' + qi + '">' + esc(S.reorder) + '</button></div></div>';
      }).join('') : '<p class="vq-mute">' + esc(S.none) + '</p>';
      [].forEach.call(L.querySelectorAll('[data-re]'), function (b) {
        b.onclick = function () { r.quotes[+b.dataset.re].items.forEach(function (x) { if (x.s) addItem(x, x.q); }); note = ''; open('cart'); };
      });
    }).catch(function () { var L = $('.vq-list', bd); if (L) L.innerHTML = '<div class="vq-msg bad">' + esc(S.err) + '</div>'; });
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
