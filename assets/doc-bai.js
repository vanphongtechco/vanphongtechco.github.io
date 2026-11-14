/* Đọc to bằng giọng đọc của trình duyệt (Web Speech API):
   – trang bài tin tức: nút "Nghe bài viết" dưới tiêu đề;
   – trang chủ, mục Bài báo khoa học / Sáng chế: nút "Nghe tóm tắt" ở từng bài. */
(function () {
  if (!('speechSynthesis' in window)) return;
  var art = document.querySelector('article.art'), pubs = document.querySelectorAll('li.pub'), about = document.querySelector('.about');
  if (!art && !pubs.length && !about) return;
  var LG = (document.documentElement.lang || 'vi').slice(0, 2);
  var LC = { vi: 'vi-VN', en: 'en-US', zh: 'zh-CN' }[LG] || 'vi-VN';
  var T = {
    vi: { prod: 'Nghe giới thiệu', play: 'Nghe bài viết', abs: 'Nghe tóm tắt', pause: 'Tạm dừng', resume: 'Đọc tiếp', stop: 'Dừng', nov: 'Thiết bị này chưa có giọng đọc tiếng Việt. Hãy thử Chrome/Edge hoặc điện thoại.' },
    en: { prod: 'Listen to the introduction', play: 'Listen to this article', abs: 'Listen to abstract', pause: 'Pause', resume: 'Resume', stop: 'Stop', nov: 'No English voice is available on this device.' },
    zh: { prod: '收听产品介绍', play: '收听本文', abs: '收听摘要', pause: '暂停', resume: '继续', stop: '停止', nov: '此设备没有中文语音。' }
  }[LG] || {};
  var ss = window.speechSynthesis, voice = null;
  function pickVoice() {
    var vs = ss.getVoices().filter(function (v) { return (v.lang || '').replace('_', '-').toLowerCase().indexOf(LC.slice(0, 2).toLowerCase()) === 0; });
    vs.sort(function (a, b) { var s = function (v) { return (/natural|online|neural|google/i.test(v.name) ? 2 : 0) + ((v.lang || '').replace('_', '-') === LC ? 1 : 0); }; return s(b) - s(a); });
    voice = vs[0] || null;
  }
  pickVoice(); if (ss.onvoiceschanged !== undefined) ss.onvoiceschanged = pickVoice;
  function split(parts) {
    var out = [];
    parts.forEach(function (p) {
      p = String(p || '').replace(/\s+/g, ' ').trim(); if (!p) return;
      p.replace(/([.!?;:])\s+/g, '$1\n').replace(/([。！？；])/g, '$1\n').split('\n').forEach(function (s) { s = s.trim(); if (s) out.push(s); });
    });
    return out;
  }

  /* một trình đọc dùng chung: chỉ một đoạn được đọc tại một thời điểm */
  var cur = null; // { q, i, state, ui }
  function speakNext() {
    if (!cur || cur.state !== 'play') return;
    if (cur.i >= cur.q.length) { var c = cur; cur = null; c.state = 'idle'; c.ui(c); return; }
    var u = new SpeechSynthesisUtterance(cur.q[cur.i]); u.lang = LC; try { if (voice) u.voice = voice; } catch (e) {} u.rate = 1;
    var me = cur;
    u.onend = function () { if (cur === me) { me.i++; speakNext(); } };
    u.onerror = function (e) { if (cur === me && e.error !== 'interrupted' && e.error !== 'canceled') { me.i++; speakNext(); } };
    ss.speak(u);
  }
  function makePlayer(getText, ui) {
    var pl = { q: [], i: 0, state: 'idle', ui: ui };
    pl.toggle = function () {
      if (!voice) pickVoice();
      if (pl.state === 'idle') {
        if (cur && cur !== pl) { var o = cur; o.state = 'idle'; o.ui(o); }
        ss.cancel(); pl.q = split(getText()); pl.i = 0; pl.state = 'play'; cur = pl; ui(pl); speakNext();
      } else if (pl.state === 'play') { pl.state = 'pause'; ss.cancel(); ui(pl); }
      else { if (cur && cur !== pl) { var o2 = cur; o2.state = 'idle'; o2.ui(o2); } cur = pl; pl.state = 'play'; ui(pl); speakNext(); }
    };
    pl.stop = function () { pl.state = 'idle'; pl.i = 0; if (cur === pl) { cur = null; ss.cancel(); } ui(pl); };
    return pl;
  }

  var css = '.tts{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:0 0 16px}.tts button,.tts1{display:inline-flex;align-items:center;gap:6px;border:1px solid #1580BF;background:#fff;color:#0E2F5A;border-radius:20px;padding:8px 14px;font:600 14px/1 inherit;font-family:inherit;cursor:pointer}'
    + '.tts button.on,.tts1.on{background:#1580BF;color:#fff}.tts button[hidden]{display:none}.tts small,.tts1+small{color:#6B7684;font-size:13px}.tts1{padding:5px 11px;font-size:13px;margin:0 8px 0 0;vertical-align:middle}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  /* bài tin tức, hoặc trang sản phẩm có phần Giới thiệu */
  var box = art || about;
  if (box) {
    var h1 = art ? art.querySelector('h1') : document.querySelector('.pd h1, main h1, h1');
    var LBL = art ? T.play : T.prod;
    var bar = document.createElement('div'); bar.className = 'tts';
    bar.innerHTML = '<button type="button" data-a="play">🔊 <span>' + LBL + '</span></button><button type="button" data-a="stop" hidden>⏹ ' + T.stop + '</button><small></small>';
    if (art) h1.parentNode.insertBefore(bar, h1.nextSibling); else { var hh = about.querySelector('h2'); hh.parentNode.insertBefore(bar, hh.nextSibling); }
    var bP = bar.querySelector('[data-a=play]'), bS = bar.querySelector('[data-a=stop]'), note = bar.querySelector('small');
    var pa = makePlayer(function () {
      var c = box.cloneNode(true);
      [].forEach.call(c.querySelectorAll('.tts,figure,.btns,iframe,video,script,style,.tag,h2'), function (x) { x.remove(); });
      var parts = [h1 ? h1.textContent : ''];
      [].forEach.call(c.querySelectorAll('p,li'), function (x) { parts.push(x.textContent); });
      return parts;
    }, function (p) {
      bP.classList.toggle('on', p.state === 'play');
      bP.querySelector('span').textContent = p.state === 'play' ? T.pause : p.state === 'pause' ? T.resume : LBL;
      bS.hidden = p.state === 'idle';
      if (!voice && p.state !== 'idle') note.textContent = T.nov;
    });
    bP.onclick = pa.toggle; bS.onclick = pa.stop;
  }

  /* bài báo khoa học, sáng chế */
  [].forEach.call(pubs, function (li) {
    var abs = li.querySelector('details p'), dl = li.querySelector('.dl'); if (!abs || !dl) return;
    var b = document.createElement('button'); b.type = 'button'; b.className = 'tts1'; b.innerHTML = '🔊 <span>' + T.abs + '</span>';
    var nt = document.createElement('small');
    dl.insertBefore(nt, dl.firstChild); dl.insertBefore(b, dl.firstChild);
    var pl = makePlayer(function () { var h = li.querySelector('h4'); return [h ? h.textContent : '', abs.textContent]; }, function (p) {
      b.classList.toggle('on', p.state === 'play');
      b.querySelector('span').textContent = p.state === 'play' ? T.pause : p.state === 'pause' ? T.resume : T.abs;
      nt.textContent = (!voice && p.state !== 'idle') ? ' ' + T.nov + ' ' : '';
      if (p.state === 'play') { var d = li.querySelector('details'); if (d) d.open = true; }
    });
    b.onclick = pl.toggle;
  });
  window.addEventListener('pagehide', function () { ss.cancel(); });
})();
