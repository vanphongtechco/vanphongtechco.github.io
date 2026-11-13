/**
 * Vân Phong – backend cho giỏ yêu cầu báo giá và tài khoản khách hàng trên vanphongtechco.com.vn
 *
 * CÀI ĐẶT (một lần):
 *  1. Đăng nhập Google bằng info@vanphongtechco.com.vn → script.google.com → Dự án mới (hoặc Apps Script gắn với một Sheet).
 *  2. Dán toàn bộ file này vào Code.gs, bấm Lưu.
 *  3. Chọn hàm "setup" → Chạy → cấp quyền. Hàm tự tạo Google Sheet "Web – Yêu cầu báo giá và khách hàng" (link ở Nhật ký thực thi).
 *  4. Triển khai → Tùy chọn triển khai mới → loại "Ứng dụng web":
 *       Thực thi với tư cách: Tôi (info@…) · Người có quyền truy cập: Bất kỳ ai → Triển khai.
 *  5. Sao chép "URL ứng dụng web" (…/exec) gửi cho người quản trị web để dán vào assets/bao-gia.js (biến API).
 *  Khi sửa file này: Triển khai → Quản lý triển khai → ✎ → Phiên bản: Phiên bản mới → Triển khai (URL giữ nguyên).
 *
 * SỬ DỤNG:
 *  - Sheet "BaoGia": mỗi dòng là một yêu cầu. Nhân viên cập nhật cột "Trạng thái", "Phản hồi cho khách",
 *    "Link file báo giá" (link Drive/PDF chia sẻ cho người có link) – khách thấy ngay trong mục Tài khoản trên web.
 *  - Sheet "KhachHang": danh sách khách đã gửi yêu cầu / đăng nhập.
 */

var INFO = 'info@vanphongtechco.com.vn';
var CC = '';                       // thêm email nhận bản sao, ví dụ 'binh@…' (để trống nếu không cần)
var SITE = 'https://vanphongtechco.com.vn';
var TZ = 'Asia/Ho_Chi_Minh';
var STATUSES = ['Mới', 'Đang xử lý', 'Đã gửi báo giá', 'Hoàn tất', 'Hủy'];
var H_Q = ['Mã', 'Thời gian', 'Email', 'Họ tên', 'Công ty', 'Điện thoại', 'Ghi chú', 'Sản phẩm – số lượng', 'Số dòng',
  'Trạng thái', 'Phản hồi cho khách', 'Link file báo giá', 'Email đã xác thực', 'Ngôn ngữ', 'Trang gửi', 'Dữ liệu (JSON)'];
var H_C = ['Email', 'Họ tên', 'Công ty', 'Điện thoại', 'Ngày tạo', 'Lần cuối', 'Số yêu cầu', 'Mật khẩu (mã hóa)'];
var SESSION_DAYS = 180;

function SS() {
  var id = PropertiesService.getScriptProperties().getProperty('SHEET_ID');
  return id ? SpreadsheetApp.openById(id) : SpreadsheetApp.getActiveSpreadsheet();
}

function setup() {
  var p0 = PropertiesService.getScriptProperties();
  var ss = null;
  try { ss = SpreadsheetApp.getActiveSpreadsheet(); } catch (e) {}
  if (!ss && p0.getProperty('SHEET_ID')) ss = SpreadsheetApp.openById(p0.getProperty('SHEET_ID'));
  if (!ss) { ss = SpreadsheetApp.create('Web – Yêu cầu báo giá và khách hàng'); }
  p0.setProperty('SHEET_ID', ss.getId());
  var q = ss.getSheetByName('BaoGia') || ss.insertSheet('BaoGia');
  q.getRange(1, 1, 1, H_Q.length).setValues([H_Q]).setFontWeight('bold').setBackground('#0E2F5A').setFontColor('#fff');
  q.setFrozenRows(1);
  q.getRange('J2:J').setDataValidation(SpreadsheetApp.newDataValidation().requireValueInList(STATUSES, true).build());
  q.setColumnWidth(8, 420); q.setColumnWidth(7, 260); q.setColumnWidth(11, 260); q.hideColumns(16);
  var c = ss.getSheetByName('KhachHang') || ss.insertSheet('KhachHang');
  c.getRange(1, 1, 1, H_C.length).setValues([H_C]).setFontWeight('bold').setBackground('#0E2F5A').setFontColor('#fff');
  c.setFrozenRows(1);
  var s1 = ss.getSheetByName('Sheet1') || ss.getSheetByName('Trang tính1');
  if (s1 && s1.getLastRow() === 0 && ss.getSheets().length > 2) ss.deleteSheet(s1);
  var p = PropertiesService.getScriptProperties();
  if (!p.getProperty('SECRET')) p.setProperty('SECRET', Utilities.getUuid() + Utilities.getUuid());
  MailApp.getRemainingDailyQuota(); // xin quyền gửi mail ngay khi setup
  console.log('SHEET: ' + ss.getUrl());
}

function doGet() { return out({ ok: true, service: 'vanphong-quote' }); }

function doPost(e) {
  try {
    var d = JSON.parse(e.postData.contents || '{}');
    if (d.hp) return out({ ok: true, code: '—' });          // bẫy bot
    switch (d.action) {
      case 'register': return out(register(d));
      case 'login': return out(login(d));
      case 'forgot': return out(forgot(d));
      case 'changePw': return out(changePw(d));
      case 'requestCode': return out(requestCode(d));
      case 'verify': return out(verify(d));
      case 'submitQuote': return out(submitQuote(d));
      case 'myQuotes': return out(myQuotes(d));
    }
    return out({ ok: false, err: 'action' });
  } catch (err) {
    console.error(err);
    return out({ ok: false, err: 'server' });
  }
}

/* ---------- đăng nhập bằng mã email ---------- */
function requestCode(d) {
  var em = cleanEmail(d.email); if (!em) return { ok: false, err: 'email' };
  if (!limit('rc:' + em, 5, 3600) || !limit('rc:all', 300, 3600)) return { ok: false, err: 'rate' };
  var code = ('00000' + (parseInt(Utilities.getUuid().replace(/\D/g, '').slice(0, 9), 10) % 1000000)).slice(-6);
  CacheService.getScriptCache().put('otp:' + em, JSON.stringify({ c: code, n: 0 }), 600);
  var t = TX[d.lang] || TX.vi;
  MailApp.sendEmail({
    to: em, name: 'Vân Phong', subject: t.otpSubj + ' ' + code,
    htmlBody: wrap('<p>' + t.otpBody + '</p><p style="font-size:30px;font-weight:700;letter-spacing:6px;color:#0E2F5A">' + code + '</p><p style="color:#6B7684">' + t.otpNote + '</p>')
  });
  return { ok: true };
}

function verify(d) {
  var em = cleanEmail(d.email); if (!em) return { ok: false, err: 'email' };
  var cache = CacheService.getScriptCache(), key = 'otp:' + em, raw = cache.get(key);
  if (!raw) return { ok: false, err: 'code' };
  var o = JSON.parse(raw);
  if (o.n >= 5) { cache.remove(key); return { ok: false, err: 'rate' }; }
  if (String(d.code || '').trim() !== o.c) { o.n++; cache.put(key, JSON.stringify(o), 600); return { ok: false, err: 'code' }; }
  cache.remove(key);
  var prof = upsertCustomer(em, {}, false);
  return { ok: true, token: makeToken(em), profile: prof };
}

/* ---------- tài khoản: đăng ký / đăng nhập bằng email hoặc SĐT + mật khẩu ---------- */
function normPhone(x) { x = String(x || '').replace(/\D/g, ''); if (x.indexOf('84') === 0 && x.length >= 11) x = '0' + x.slice(2); return x; }
function custSheet() {
  var sh = SS().getSheetByName('KhachHang');
  if (sh.getRange(1, 8).getValue() !== H_C[7]) {
    sh.getRange(1, 1, 1, H_C.length).setValues([H_C]).setFontWeight('bold').setBackground('#0E2F5A').setFontColor('#fff');
    sh.hideColumns(8);
  }
  return sh;
}
function findCust(id) {
  var sh = custSheet(), last = sh.getLastRow(); if (last < 2) return null;
  var em = cleanEmail(id), ph = em ? '' : normPhone(id); if (!em && ph.length < 8) return null;
  var v = sh.getRange(2, 1, last - 1, H_C.length).getValues();
  for (var i = 0; i < v.length; i++) {
    if ((em && String(v[i][0]).toLowerCase() === em) || (ph && normPhone(v[i][3]) === ph)) return { sh: sh, row: i + 2, v: v[i] };
  }
  return null;
}
function hashPw(pw, salt) {
  salt = salt || Utilities.getUuid().replace(/-/g, '');
  var x = String(pw);
  for (var i = 0; i < 300; i++) x = b64(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, salt + x, Utilities.Charset.UTF_8));
  return salt + ':' + x;
}
function pwOk(pw, stored) { stored = String(stored || ''); var salt = stored.split(':')[0]; return !!salt && stored.indexOf(':') > 0 && hashPw(pw, salt) === stored; }
function profOf(v) { return { name: String(v[1]), company: String(v[2]), phone: String(v[3]).replace(/^'/, ''), email: String(v[0]) }; }
function tmpPw() { var a = 'abcdefghjkmnpqrstuvwxyz23456789', r = ''; for (var i = 0; i < 8; i++) r += a.charAt(Math.floor(Math.random() * a.length)); return r; }

function register(d) {
  var em = cleanEmail(d.email), name = str(d.name, 120), phone = str(d.phone, 40), company = str(d.company, 200), pw = String(d.pw || '');
  if (!em || !name || normPhone(phone).length < 8) return { ok: false, err: 'input' };
  if (pw.length < 6 || pw.length > 100) return { ok: false, err: 'pw' };
  if (!limit('rg:' + em, 5, 3600) || !limit('rg:all', 200, 3600)) return { ok: false, err: 'rate' };
  var lock = LockService.getScriptLock(); lock.waitLock(20000);
  try {
    if (findCust(em) || findCust(phone)) return { ok: false, err: 'exists' };
    upsertCustomer(em, { name: name, company: company, phone: phone }, false);
    var c = findCust(em); c.sh.getRange(c.row, 8).setValue(hashPw(pw));
  } finally { lock.releaseLock(); }
  try {
    MailApp.sendEmail({ to: INFO, cc: CC || undefined, replyTo: em, name: 'Website Vân Phong',
      subject: '[Web] Khách hàng mới đăng ký – ' + name + (company ? ' – ' + company : ''),
      htmlBody: wrap('<p>Khách hàng mới đăng ký tài khoản trên website:</p><p><b>' + h(name) + '</b>' + (company ? ' – ' + h(company) : '')
        + '<br>ĐT: ' + h(phone) + '<br>Email: ' + h(em) + '</p><p style="color:#6B7684">Danh sách đầy đủ trong Sheet "KhachHang".</p>') });
  } catch (e) { console.error(e); }
  return { ok: true, token: makeToken(em), profile: { name: name, company: company, phone: phone, email: em } };
}

function login(d) {
  var id = str(d.id, 120).toLowerCase();
  if (!limit('lg:' + id, 10, 900) || !limit('lg:all', 600, 3600)) return { ok: false, err: 'rate' };
  var c = findCust(id);
  if (!c || !c.v[7] || !pwOk(String(d.pw || ''), c.v[7])) return { ok: false, err: 'login' };
  c.sh.getRange(c.row, 6).setValue(Utilities.formatDate(new Date(), TZ, 'dd/MM/yyyy HH:mm'));
  return { ok: true, token: makeToken(String(c.v[0]).toLowerCase()), profile: profOf(c.v) };
}

function forgot(d) {
  var id = str(d.id, 120).toLowerCase();
  if (!limit('fg:' + id, 3, 3600) || !limit('fg:all', 100, 3600)) return { ok: false, err: 'rate' };
  var c = findCust(id);
  if (c) {
    var pw = tmpPw(), em = String(c.v[0]), t = TX[d.lang] || TX.vi;
    c.sh.getRange(c.row, 8).setValue(hashPw(pw));
    MailApp.sendEmail({ to: em, replyTo: INFO, name: 'Vân Phong', subject: t.pwSubj,
      htmlBody: wrap('<p>' + t.pwBody + '</p><p style="font-size:24px;font-weight:700;letter-spacing:2px;color:#0E2F5A">' + pw + '</p><p>' + t.pwNote + '</p>') });
  }
  return { ok: true };                     // không tiết lộ email/SĐT có tồn tại hay không
}

function changePw(d) {
  var em = checkToken(d.token); if (!em) return { ok: false, err: 'auth' };
  var c = findCust(em), npw = String(d.npw || '');
  if (!c || !pwOk(String(d.pw || ''), c.v[7])) return { ok: false, err: 'login' };
  if (npw.length < 6 || npw.length > 100) return { ok: false, err: 'pw' };
  c.sh.getRange(c.row, 8).setValue(hashPw(npw));
  return { ok: true };
}

/* ---------- yêu cầu báo giá ---------- */
function submitQuote(d) {
  var tokEmail = d.token ? checkToken(d.token) : null;
  var em = tokEmail || cleanEmail(d.email);
  var name = str(d.name, 120), phone = str(d.phone, 40), company = str(d.company, 200), note = str(d.note, 3000);
  if (!em || !name || phone.replace(/\D/g, '').length < 8) return { ok: false, err: 'input' };
  var items = (Array.isArray(d.items) ? d.items : []).slice(0, 100).map(function (x) {
    return { s: str(x.s, 200), n: str(x.n, 300), c: str(x.c, 120), q: Math.max(1, Math.min(9999, parseInt(x.q, 10) || 1)) };
  }).filter(function (x) { return x.n; });
  if (!items.length) return { ok: false, err: 'input' };
  if (!limit('sq:' + em, 10, 86400) || !limit('sq:all', 500, 86400)) return { ok: false, err: 'rate' };

  var lock = LockService.getScriptLock(); lock.waitLock(20000);
  try {
    var sh = SS().getSheetByName('BaoGia');
    var now = new Date(), day = Utilities.formatDate(now, TZ, 'yyMMdd');
    var n = 1, last = sh.getLastRow();
    if (last > 1) {
      var codes = sh.getRange(Math.max(2, last - 300), 1, Math.min(301, last - 1), 1).getValues();
      codes.forEach(function (r) { var m = /^YC(\d{6})-(\d+)$/.exec(r[0]); if (m && m[1] === day) n = Math.max(n, +m[2] + 1); });
    }
    var code = 'YC' + day + '-' + ('00' + n).slice(-3);
    var list = items.map(function (x, i) { return (i + 1) + '. ' + x.n + (x.c && x.n.indexOf(x.c) < 0 ? ' (' + x.c + ')' : '') + ' × ' + x.q; }).join('\n');
    sh.appendRow([code, Utilities.formatDate(now, TZ, 'dd/MM/yyyy HH:mm'), em, name, company, "'" + phone, note, list, items.length,
      'Mới', '', '', tokEmail ? 'Có' : 'Chưa', str(d.lang, 5), str(d.page, 500), JSON.stringify(items)]);
  } finally { lock.releaseLock(); }
  upsertCustomer(em, { name: name, company: company, phone: phone }, true);

  var rows = items.map(function (x, i) {
    return '<tr><td style="padding:6px;border:1px solid #ddd">' + (i + 1) + '</td><td style="padding:6px;border:1px solid #ddd">'
      + (x.s ? '<a href="' + SITE + '/san-pham/' + encodeURIComponent(x.s) + '/">' + h(x.n) + '</a>' : h(x.n))
      + '</td><td style="padding:6px;border:1px solid #ddd">' + h(x.c) + '</td><td style="padding:6px;border:1px solid #ddd;text-align:right">' + x.q + '</td></tr>';
  }).join('');
  var table = '<table style="border-collapse:collapse;font-size:14px"><tr style="background:#F3F5F8"><th style="padding:6px;border:1px solid #ddd">#</th><th style="padding:6px;border:1px solid #ddd">Sản phẩm</th><th style="padding:6px;border:1px solid #ddd">Model</th><th style="padding:6px;border:1px solid #ddd">SL</th></tr>' + rows + '</table>';

  MailApp.sendEmail({
    to: INFO, cc: CC || undefined, replyTo: em, name: 'Website Vân Phong',
    subject: '[Web] Yêu cầu báo giá ' + code + ' – ' + name + (company ? ' – ' + company : ''),
    htmlBody: wrap('<p><b>' + h(name) + '</b>' + (company ? ' – ' + h(company) : '') + '<br>ĐT: ' + h(phone) + ' · Email: ' + h(em)
      + (tokEmail ? ' (đã xác thực)' : ' (chưa xác thực)') + '</p>' + table + (note ? '<p><b>Ghi chú:</b><br>' + h(note).replace(/\n/g, '<br>') + '</p>' : '')
      + '<p style="color:#6B7684">Mã ' + code + ' · Cập nhật trạng thái/phản hồi trong Sheet "BaoGia" để khách xem trên web. Bấm Trả lời để email trực tiếp cho khách.</p>')
  });
  var t = TX[d.lang] || TX.vi;
  MailApp.sendEmail({
    to: em, replyTo: INFO, name: 'Vân Phong',
    subject: t.qSubj + ' ' + code,
    htmlBody: wrap('<p>' + t.qBody.replace('{c}', '<b>' + code + '</b>') + '</p>' + table
      + '<p>' + t.qTrack.replace('{u}', '<a href="' + SITE + (d.lang && d.lang !== 'vi' ? '/' + d.lang : '') + '/#bao-gia-cua-toi">vanphongtechco.com.vn</a>') + '</p>')
  });
  return { ok: true, code: code };
}

function myQuotes(d) {
  var em = checkToken(d.token); if (!em) return { ok: false, err: 'auth' };
  var sh = SS().getSheetByName('BaoGia'), last = sh.getLastRow(), res = [];
  if (last > 1) {
    var v = sh.getRange(2, 1, last - 1, H_Q.length).getDisplayValues();
    for (var i = v.length - 1; i >= 0 && res.length < 50; i--) {
      if (String(v[i][2]).toLowerCase() !== em) continue;
      var items; try { items = JSON.parse(v[i][15]); } catch (e) { items = [{ n: v[i][7], q: '' }]; }
      res.push({ code: v[i][0], time: v[i][1], status: v[i][9] || 'Mới', reply: v[i][10], file: v[i][11], items: items });
    }
  }
  return { ok: true, quotes: res };
}

/* ---------- tiện ích ---------- */
function upsertCustomer(em, p, isQuote) {
  var sh = custSheet(), last = sh.getLastRow();
  var now = Utilities.formatDate(new Date(), TZ, 'dd/MM/yyyy HH:mm');
  var emails = last > 1 ? sh.getRange(2, 1, last - 1, 1).getValues().map(function (r) { return String(r[0]).toLowerCase(); }) : [];
  var i = emails.indexOf(em);
  if (i < 0) {
    sh.appendRow([em, p.name || '', p.company || '', p.phone ? "'" + p.phone : '', now, now, isQuote ? 1 : 0, '']);
    return { name: p.name || '', company: p.company || '', phone: p.phone || '' };
  }
  var r = sh.getRange(i + 2, 1, 1, H_C.length), v = r.getValues()[0];
  if (p.name) v[1] = p.name; if (p.company) v[2] = p.company; if (p.phone) v[3] = "'" + p.phone;
  v[5] = now; if (isQuote) v[6] = (+v[6] || 0) + 1;
  r.setValues([v]);
  return { name: String(v[1]), company: String(v[2]), phone: String(v[3]).replace(/^'/, '') };
}

function makeToken(em) {
  var body = b64(em + '|' + (Date.now() + SESSION_DAYS * 864e5));
  return body + '.' + sig(body);
}
function checkToken(t) {
  var p = String(t || '').split('.'); if (p.length !== 2 || sig(p[0]) !== p[1]) return null;
  var s = Utilities.newBlob(Utilities.base64DecodeWebSafe(p[0])).getDataAsString().split('|');
  return +s[1] > Date.now() ? s[0] : null;
}
function sig(s) { return b64(Utilities.computeHmacSha256Signature(s, PropertiesService.getScriptProperties().getProperty('SECRET'))).slice(0, 43); }
function b64(x) { return Utilities.base64EncodeWebSafe(x).replace(/=+$/, ''); }
function limit(k, max, sec) {
  var c = CacheService.getScriptCache(), n = +(c.get('rl:' + k) || 0);
  if (n >= max) return false; c.put('rl:' + k, String(n + 1), sec); return true;
}
function cleanEmail(s) { s = String(s || '').trim().toLowerCase(); return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(s) && s.length < 120 ? s : null; }
function str(s, n) { return String(s == null ? '' : s).trim().slice(0, n); }
function h(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
function out(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }
function wrap(b) {
  return '<div style="font-family:Arial,sans-serif;font-size:15px;color:#1B2430;max-width:640px">' + b
    + '<hr style="border:0;border-top:1px solid #E3E8EE;margin:20px 0"><p style="font-size:13px;color:#6B7684">Công ty TNHH Kỹ thuật và Thương mại Vân Phong<br>'
    + 'Số 34, ngõ 36A, phố Trần Điền, Phường Phương Liệt, TP. Hà Nội<br>Hotline 08.9999.0683 · ' + INFO + ' · vanphongtechco.com.vn</p></div>';
}

var TX = {
  vi: {
    otpSubj: 'Mã đăng nhập Vân Phong:', otpBody: 'Mã đăng nhập tài khoản trên website Vân Phong của bạn là:',
    otpNote: 'Mã có hiệu lực 10 phút. Nếu bạn không yêu cầu, hãy bỏ qua email này.',
    qSubj: 'Vân Phong đã nhận yêu cầu báo giá', qBody: 'Cảm ơn Quý khách. Vân Phong đã nhận yêu cầu báo giá {c} gồm:',
    qTrack: 'Chúng tôi sẽ phản hồi trong giờ làm việc. Quý khách theo dõi trạng thái tại mục Tài khoản trên {u}.',
    pwSubj: 'Mật khẩu mới – tài khoản website Vân Phong', pwBody: 'Theo yêu cầu "Quên mật khẩu", mật khẩu mới cho tài khoản của Quý khách là:', pwNote: 'Đăng nhập bằng email hoặc số điện thoại cùng mật khẩu này, sau đó có thể đổi mật khẩu trong mục Tài khoản. Nếu Quý khách không yêu cầu, vui lòng liên hệ 08.9999.0683.'
  },
  en: {
    otpSubj: 'Van Phong sign-in code:', otpBody: 'Your sign-in code for the Van Phong website is:',
    otpNote: 'The code is valid for 10 minutes. If you did not request it, please ignore this email.',
    qSubj: 'Van Phong received your quote request', qBody: 'Thank you. Van Phong has received your quote request {c}:',
    qTrack: 'We will reply during business hours. Track its status under Account on {u}.',
    pwSubj: 'New password – Van Phong website account', pwBody: 'As requested via "Forgot password", the new password for your account is:', pwNote: 'Sign in with your email or phone number and this password; you can change it under Account. If you did not request this, please call +84 899 990 683.'
  },
  zh: {
    otpSubj: 'Vân Phong 登录验证码：', otpBody: '您在 Vân Phong 网站的登录验证码是：',
    otpNote: '验证码 10 分钟内有效。如非本人操作，请忽略此邮件。',
    qSubj: 'Vân Phong 已收到您的询价', qBody: '感谢您的询价。Vân Phong 已收到询价单 {c}：',
    qTrack: '我们将在工作时间回复。请在 {u} 的“账户”中查看进度。',
    pwSubj: '新密码 – Vân Phong 网站账户', pwBody: '根据您的“忘记密码”请求，您账户的新密码为：', pwNote: '请使用邮箱或手机号及此密码登录，登录后可在“账户”中修改密码。如非本人操作，请致电 +84 899 990 683。'
  }
};
