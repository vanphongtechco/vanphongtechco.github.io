/* Nút "Nghe bài viết" – đọc nội dung bài bằng giọng đọc của trình duyệt (Web Speech API). */
(function () {
  var art = document.querySelector('article.art'); if (!art || !('speechSynthesis' in window)) return;
  var LG = (document.documentElement.lang || 'vi').slice(0, 2);
  var LC = { vi: 'vi-VN', en: 'en-US', zh: 'zh-CN' }[LG] || 'vi-VN';
  var T = {
    vi: { play: 'Nghe bài viết', pause: 'Tạm dừng', resume: 'Đọc tiếp', stop: 'Dừng', nov: 'Thiết bị này chưa có giọng đọc tiếng Việt. Hãy thử Chrome/Edge hoặc điện thoại.' },
    en: { play: 'Listen to this article', pause: 'Pause', resume: 'Resume', stop: 'Stop', nov: 'No English voice is available on this device.' },
    zh: { play: '收听本文', pause: '暂停', resume: '继续', stop: '停止', nov: '此设备没有中文语音。' }
  }[LG] || {};
  var ss = window.speechSynthesis, voice = null, queue = [], idx = 0, state = 'idle';
  function pickVoice() {
    var vs = ss.getVoices().filter(function (v) { return (v.lang || '').replace('_', '-').toLowerCase().indexOf(LC.slice(0, 2).toLowerCase()) === 0; });
    vs.sort(function (a, b) { var s = function (v) { return (/natural|online|neural|google/i.test(v.name) ? 2 : 0) + ((v.lang || '').replace('_', '-') === LC ? 1 : 0); }; return s(b) - s(a); });
    voice = vs[0] || null;
  }
  pickVoice(); if (ss.onvoiceschanged !== undefined) ss.onvoiceschanged = pickVoice;

  var css = '.tts{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:0 0 16px}.tts button{display:inline-flex;align-items:center;gap:6px;border:1px solid #1580BF;background:#fff;color:#0E2F5A;border-radius:20px;padding:8px 14px;font:600 14px/1 inherit;font-family:inherit;cursor:pointer}.tts button.on{background:#1580BF;color:#fff}.tts button[hidden]{display:none}.tts small{color:#6B7684}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);
  var bar = document.createElement('div'); bar.className = 'tts';
  bar.innerHTML = '<button type="button" data-a="play">🔊 <span>' + T.play + '</span></button><button type="button" data-a="stop" hidden>⏹ ' + T.stop + '</button><small></small>';
  var h1 = art.querySelector('h1'); h1.parentNode.insertBefore(bar, h1.nextSibling);
  var bP = bar.querySelector('[data-a=play]'), bS = bar.querySelector('[data-a=stop]'), note = bar.querySelector('small');

  function textOf() {
    var c = art.cloneNode(true);
    [].forEach.call(c.querySelectorAll('.tts,figure,.btns,iframe,video,script,style,.tag'), function (x) { x.remove(); });
    var parts = [h1.textContent];
    [].forEach.call(c.querySelectorAll('p,li'), function (x) { var t = x.textContent.replace(/\s+/g, ' ').trim(); if (t) parts.push(t); });
    var out = [];
    parts.forEach(function (p) {                    // cắt câu ngắn để trình duyệt không bỏ dở
      p.replace(/([.!?;:])\s+/g, '$1\n').replace(/([。！？；])/g, '$1\n').split('\n').forEach(function (s) { s = s.trim(); if (s) out.push(s); });
    });
    return out;
  }
  function ui() {
    bP.classList.toggle('on', state === 'play');
    bP.querySelector('span').textContent = state === 'play' ? T.pause : state === 'pause' ? T.resume : T.play;
    bS.hidden = state === 'idle';
  }
  function next() {
    if (state !== 'play') return;
    if (idx >= queue.length) { state = 'idle'; ui(); return; }
    var u = new SpeechSynthesisUtterance(queue[idx]); u.lang = LC; try { if (voice) u.voice = voice; } catch (e) {} u.rate = 1;
    u.onend = function () { idx++; next(); };
    u.onerror = function (e) { if (e.error !== 'interrupted' && e.error !== 'canceled') { idx++; next(); } };
    ss.speak(u);
  }
  bP.onclick = function () {
    if (!voice) { pickVoice(); if (!voice) { note.textContent = T.nov; } }
    if (state === 'idle') { ss.cancel(); queue = textOf(); idx = 0; state = 'play'; ui(); next(); }
    else if (state === 'play') { state = 'pause'; ss.cancel(); ui(); }      // cancel + đọc lại câu đang dở: ổn định hơn pause() trên Chrome
    else { state = 'play'; ui(); next(); }
  };
  bS.onclick = function () { state = 'idle'; ss.cancel(); idx = 0; ui(); };
  window.addEventListener('pagehide', function () { ss.cancel(); });
})();
