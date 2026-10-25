/* Project HORIZON · Data Analyst lab guides · site.js
   Everything here is progressive enhancement: the guides read fine without it.
   State (steps done, guesses, gut score, collected cards) lives in this browser
   only, under one localStorage key, and every read/write is wrapped. */
(function () {
  'use strict';

  var KEY = 'pmi-da-labs:v1';
  var PAGE = document.documentElement.getAttribute('data-page') || 'x';
  var REDUCED = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.documentElement.classList.remove('no-js');
  if (/[?&]shot\b/.test(location.search)) { document.documentElement.classList.add('shot'); REDUCED = true; }
  if (/[?&]og\b/.test(location.search)) { document.documentElement.classList.add('og', 'shot'); REDUCED = true; }

  /* ------------------------------------------------------------ storage */
  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; }
  }
  var S = load();
  ['steps', 'guesses', 'gut', 'cards', 'inputs', 'picks'].forEach(function (k) { if (!S[k] || typeof S[k] !== 'object') S[k] = {}; });
  function save() { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) { /* private mode: fine */ } }
  function $(sel, root) { return (root || document).querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function fmt(n) { return n.toLocaleString('en-US'); }

  /* ------------------------------------------------------------ theme */
  var themeBtn = $('#theme');
  function effectiveDark() {
    var t = document.documentElement.getAttribute('data-theme');
    if (t) return t === 'dark';
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  }
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var next = effectiveDark() ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('pmi-da-theme', next); } catch (e) {}
      themeBtn.setAttribute('aria-label', next === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
      document.dispatchEvent(new CustomEvent('themechange'));
    });
  }

  /* ------------------------------------------------------------ top bar, read progress, menu */
  var bar = $('.topbar'), readbar = $('#readbar');
  function onScroll() {
    var y = window.scrollY || 0;
    if (bar) bar.classList.toggle('solid', y > 40);
    if (readbar) {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      readbar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, y / h) : 0) + ')';
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  var menuBtn = $('.menu-btn'), nav = $('.nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) { if (e.target.closest('a')) nav.classList.remove('open'); });
  }

  /* ------------------------------------------------------------ copy buttons */
  $$('.code .copy').forEach(function (btn) {
    var box = btn.closest('.code');
    var pre = box && box.querySelector('pre');
    if (!pre) return;
    var label = btn.querySelector('span');
    function done(t) {
      if (label) label.textContent = t;
      btn.classList.add('done');
      setTimeout(function () { if (label) label.textContent = 'Copy'; btn.classList.remove('done'); }, 1700);
    }
    function fallback() {
      try {
        var r = document.createRange(); r.selectNodeContents(pre);
        var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
        done('Press Ctrl+C');
      } catch (e) { done('Select it'); }
    }
    btn.addEventListener('click', function () {
      var text = pre.textContent.replace(/\s+$/, '') + '\n';
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { done('Copied'); }, fallback);
      } else fallback();
    });
  });
  /* X-ray toggles */
  $$('.xray').forEach(function (x) {
    var b = x.querySelector('.xray-toggle button');
    if (!b) return;
    b.addEventListener('click', function () {
      var on = x.classList.toggle('on');
      b.textContent = on ? 'Back to the prompt' : 'X-ray this prompt';
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  });

  /* ------------------------------------------------------------ steps done + progress */
  var pageSteps = S.steps[PAGE] || (S.steps[PAGE] = {});
  var stepBtns = $$('.donebtn[data-step]');
  function refreshProgress() {
    var total = stepBtns.length, n = 0;
    stepBtns.forEach(function (b) {
      var id = b.getAttribute('data-step');
      var on = !!pageSteps[id];
      if (on) n++;
      b.setAttribute('aria-pressed', on ? 'true' : 'false');
      var lbl = b.querySelector('.t'); if (lbl) lbl.textContent = on ? 'Done' : 'Mark done';
      var head = b.closest('.step'); if (head) head.classList.toggle('done', on);
      $$('.toc a[href="#' + id + '"]').forEach(function (a) { a.classList.toggle('complete', on); });
      $$('.route li[data-step="' + id + '"]').forEach(function (li) { li.classList.toggle('done', on); });
    });
    var fill = $('.toc-prog .bar i'), txt = $('.toc-prog .txt .c');
    if (fill) fill.style.width = (total ? (100 * n / total) : 0) + '%';
    if (txt) txt.textContent = n + ' of ' + total + ' steps';
    S.cards = S.cards || {};
  }
  stepBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      var id = b.getAttribute('data-step');
      if (pageSteps[id]) delete pageSteps[id]; else pageSteps[id] = true;
      save(); refreshProgress();
    });
  });
  refreshProgress();

  /* ------------------------------------------------------------ TOC highlight */
  var toc = $('.toc');
  if (toc && 'IntersectionObserver' in window) {
    var links = {}, targets = [], visible = {}, current = null;
    $$('a[href^="#"]', toc).forEach(function (a) {
      var id = decodeURIComponent(a.getAttribute('href').slice(1));
      var el = id && document.getElementById(id);
      if (el && !links[id]) { links[id] = a; targets.push(el); }
    });
    var pick = function () {
      var next = null;
      for (var i = 0; i < targets.length; i++) if (visible[targets[i].id]) { next = links[targets[i].id]; break; }
      if (!next || next === current) return;
      if (current) { current.classList.remove('on'); current.removeAttribute('aria-current'); }
      current = next; current.classList.add('on'); current.setAttribute('aria-current', 'true');
    };
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { visible[en.target.id] = en.isIntersecting; });
      pick();
    }, { rootMargin: '-10% 0px -72% 0px', threshold: 0 });
    targets.forEach(function (t) { io.observe(t); });
  }
  if (toc && window.innerWidth <= 1100) toc.removeAttribute('open');

  /* ------------------------------------------------------------ gut vs ground truth */
  function scoreChip() {
    var g = 0, t = 0;
    Object.keys(S.gut).forEach(function (k) { if (S.gut[k] === true) g++; else if (S.gut[k] === false) t++; });
    $$('.gut-chip').forEach(function (c) {
      var gg = c.querySelector('.g b'), tt = c.querySelector('.t b');
      if (gg) gg.textContent = g; if (tt) tt.textContent = t;
    });
    $$('[data-score="gut"]').forEach(function (e) { e.textContent = g; });
    $$('[data-score="truth"]').forEach(function (e) { e.textContent = t; });
  }
  scoreChip();

  function showGuess(id) {
    $$('details.reveal[data-p="' + id + '"] .yourguess').forEach(function (y) {
      var v = S.guesses[id];
      y.textContent = '';
      if (v) { y.appendChild(document.createTextNode('Your guess: ')); var b = document.createElement('b'); b.textContent = v; y.appendChild(b); }
    });
  }
  $$('.predict[data-p]').forEach(function (box) {
    var id = box.getAttribute('data-p');
    var inp = box.querySelector('input');
    var btn = box.querySelector('.guess button');
    var opts = $$('.opts button', box);
    var lockedTxt = box.querySelector('.locked span');
    function lock(v) {
      v = (v || '').trim();
      if (!v) { if (inp) inp.focus(); return; }
      S.guesses[id] = v.slice(0, 60); save();
      box.classList.add('is-locked');
      if (lockedTxt) lockedTxt.textContent = 'Locked in: ' + S.guesses[id];
      opts.forEach(function (o) { o.setAttribute('aria-pressed', o.getAttribute('data-v') === S.guesses[id] ? 'true' : 'false'); });
      showGuess(id);
    }
    if (btn) btn.addEventListener('click', function () { lock(inp && inp.value); });
    if (inp) inp.addEventListener('keydown', function (e) { if (e.key === 'Enter') { e.preventDefault(); lock(inp.value); } });
    opts.forEach(function (o) { o.addEventListener('click', function () { lock(o.getAttribute('data-v')); }); });
    if (S.guesses[id]) { if (inp) inp.value = S.guesses[id]; lock(S.guesses[id]); }
  });
  $$('details.reveal[data-p]').forEach(function (d) {
    var id = d.getAttribute('data-p');
    showGuess(id);
    var body = d.querySelector('.reveal-b');
    if (!body || d.hasAttribute('data-nogut')) return;
    var gc = document.createElement('div');
    gc.className = 'gutcheck';
    gc.innerHTML = '<span class="gq">Did your gut get it?<small></small></span>' +
      '<button type="button" class="y" aria-pressed="false">Yes: point to Gut</button>' +
      '<button type="button" class="n" aria-pressed="false">No: point to Ground Truth</button>' +
      '<span class="res"></span>';
    body.insertBefore(gc, body.firstChild);
    var y = gc.querySelector('.y'), n = gc.querySelector('.n'), res = gc.querySelector('.res'), sm = gc.querySelector('small');
    function paint() {
      var v = S.gut[id];
      y.setAttribute('aria-pressed', v === true ? 'true' : 'false');
      n.setAttribute('aria-pressed', v === false ? 'true' : 'false');
      res.textContent = v === true ? 'Gut +1' : v === false ? 'Ground Truth +1' : '';
      sm.textContent = S.guesses[id] ? 'you said ' + S.guesses[id] : '';
    }
    y.addEventListener('click', function () { S.gut[id] = true; save(); paint(); scoreChip(); });
    n.addEventListener('click', function () { S.gut[id] = false; save(); paint(); scoreChip(); });
    d.addEventListener('toggle', paint);
    paint();
  });

  /* ------------------------------------------------------------ in-view: rise, charts, steps, count-up */
  function countUp(el) {
    var to = parseFloat(el.getAttribute('data-count'));
    var dec = (el.getAttribute('data-count').split('.')[1] || '').length;
    var pre = el.getAttribute('data-pre') || '', suf = el.getAttribute('data-suf') || '';
    if (REDUCED || isNaN(to)) { el.textContent = pre + (isNaN(to) ? el.textContent : fmtN(to, dec)) + suf; return; }
    var from = parseFloat(el.getAttribute('data-from') || '0'), t0 = null, dur = 1300;
    function fmtN(v, d) { return d ? v.toFixed(d) : fmt(Math.round(v)); }
    function step(ts) {
      if (!t0) t0 = ts;
      var p = Math.min(1, (ts - t0) / dur), e = 1 - Math.pow(1 - p, 3);
      el.textContent = pre + fmtN(from + (to - from) * e, dec) + suf;
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  function fmtN(v, d) { return d ? v.toFixed(d) : fmt(Math.round(v)); }
  var inviewEls = $$('.rise, .anim, .step, [data-count]');
  if ('IntersectionObserver' in window && !REDUCED) {
    var vio = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target;
        el.classList.add('in');
        if (el.hasAttribute('data-count')) countUp(el);
        vio.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
    inviewEls.forEach(function (el) { vio.observe(el); });
  } else {
    inviewEls.forEach(function (el) { el.classList.add('in'); if (el.hasAttribute('data-count')) countUp(el); });
  }
  /* charts inside closed reveals animate when the reveal opens */
  $$('details.reveal').forEach(function (d) {
    d.addEventListener('toggle', function () {
      if (!d.open) return;
      $$('.anim', d).forEach(function (a) { a.classList.remove('in'); void a.offsetWidth; requestAnimationFrame(function () { a.classList.add('in'); }); });
      $$('[data-count]', d).forEach(countUp);
      document.dispatchEvent(new CustomEvent('revealopen', { detail: d }));
    });
  });

  /* ------------------------------------------------------------ tooltips (charts) */
  var tip = $('#tip');
  function tipShow(el, x, y) {
    var raw = el.getAttribute('data-tip') || '';
    var parts = raw.split('|');
    tip.textContent = '';
    var b = document.createElement('b'); b.textContent = parts[0]; tip.appendChild(b);
    if (parts[1]) { var s = document.createElement('span'); s.textContent = parts[1]; tip.appendChild(s); }
    var w = tip.offsetWidth || 160, h = tip.offsetHeight || 40;
    var left = Math.min(window.innerWidth - w - 10, Math.max(10, x - w / 2));
    var top = y - h - 14; if (top < 70) top = y + 18;
    tip.style.left = left + 'px'; tip.style.top = top + 'px';
    tip.classList.add('on');
  }
  if (tip) {
    document.addEventListener('pointermove', function (e) {
      var el = e.target.closest && e.target.closest('[data-tip]');
      if (el) tipShow(el, e.clientX, e.clientY); else tip.classList.remove('on');
    });
    document.addEventListener('focusin', function (e) {
      var el = e.target.closest && e.target.closest('[data-tip]');
      if (el) { var r = el.getBoundingClientRect(); tipShow(el, r.left + r.width / 2, r.top); }
    });
    document.addEventListener('focusout', function () { tip.classList.remove('on'); });
    window.addEventListener('scroll', function () { tip.classList.remove('on'); }, { passive: true });
  }

  /* ------------------------------------------------------------ hero parallax */
  var par = $$('.parallax');
  if (par.length && !REDUCED && window.matchMedia('(pointer: fine)').matches) {
    var mast = $('.mast');
    mast && mast.addEventListener('pointermove', function (e) {
      var r = mast.getBoundingClientRect();
      var dx = (e.clientX - r.left) / r.width - .5, dy = (e.clientY - r.top) / r.height - .5;
      par.forEach(function (p) {
        var d = parseFloat(p.getAttribute('data-depth') || '12');
        p.style.transform = 'translate3d(' + (-dx * d).toFixed(1) + 'px,' + (-dy * d).toFixed(1) + 'px,0)';
      });
    });
  }

  /* ------------------------------------------------------------ hero particle field */
  function fx(canvas) {
    var kind = canvas.getAttribute('data-fx');
    var ctx = canvas.getContext('2d');
    var W = 0, H = 0, dpr = Math.min(2, window.devicePixelRatio || 1), parts = [], running = false, raf = 0;
    var palette = {
      tokens: { c: '255,138,76', glyphs: ['?', 'timeframe?', 'adoption = ?', 'which table?', 'consent?', '?', '?', 'NULL?', 'Q3?', '18-24?'] },
      rows: { c: '0,201,167', glyphs: ['0', '1', 'SYN-JP', '73.1', '83.3', '100', '13', '30', 'true', 'false', '45', '0.70'] },
      percent: { c: '232,163,32', glyphs: ['%', '+20%', '?', 'vs ?', '%', 'pts', 'baseline?', '%', '?'] },
      stars: { c: '200,215,255', glyphs: null },
      embers: { c: '255,179,71', glyphs: null }
    }[kind] || { c: '255,255,255', glyphs: null };
    function size() {
      var r = canvas.getBoundingClientRect();
      W = r.width; H = r.height;
      canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = palette.glyphs ? Math.round(W * H / 42000) : Math.round(W * H / 5200);
      parts = [];
      for (var i = 0; i < n; i++) parts.push(spawn(true));
    }
    function spawn(any) {
      var p = {
        x: Math.random() * W,
        y: any ? Math.random() * H : (kind === 'rows' ? -20 : H + 20),
        s: palette.glyphs ? 11 + Math.random() * 9 : 0.4 + Math.random() * 1.5,
        v: (kind === 'rows' ? 1 : -1) * (0.08 + Math.random() * 0.28),
        a: palette.glyphs ? 0.03 + Math.random() * 0.09 : 0.05 + Math.random() * 0.7,
        tw: Math.random() * Math.PI * 2,
        g: palette.glyphs ? palette.glyphs[(Math.random() * palette.glyphs.length) | 0] : null
      };
      return p;
    }
    var shoot = null, t = 0;
    function frame() {
      t++;
      ctx.clearRect(0, 0, W, H);
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i];
        if (kind === 'stars' || kind === 'embers') {
          var tw = 0.55 + 0.45 * Math.sin(p.tw + t * 0.02 * (0.5 + p.s));
          ctx.fillStyle = 'rgba(' + palette.c + ',' + (p.a * tw).toFixed(3) + ')';
          ctx.beginPath(); ctx.arc(p.x, p.y, p.s, 0, 6.283); ctx.fill();
          if (kind === 'embers') { p.y += p.v * 0.6; if (p.y < -10) parts[i] = spawn(false); }
        } else {
          p.y += p.v;
          ctx.font = '500 ' + p.s.toFixed(0) + 'px "DM Mono", monospace';
          ctx.fillStyle = 'rgba(' + palette.c + ',' + p.a.toFixed(3) + ')';
          ctx.fillText(p.g, p.x, p.y);
          if ((p.v < 0 && p.y < -30) || (p.v > 0 && p.y > H + 30)) parts[i] = spawn(false);
        }
      }
      if (kind === 'stars') {
        if (!shoot && Math.random() < 0.004) shoot = { x: Math.random() * W * 0.7, y: Math.random() * H * 0.35, l: 0 };
        if (shoot) {
          shoot.l += 1;
          var len = 90, sx = shoot.x + shoot.l * 9, sy = shoot.y + shoot.l * 3.2;
          var g = ctx.createLinearGradient(sx, sy, sx - len, sy - len * 0.36);
          g.addColorStop(0, 'rgba(255,255,255,.85)'); g.addColorStop(1, 'rgba(255,255,255,0)');
          ctx.strokeStyle = g; ctx.lineWidth = 1.4;
          ctx.beginPath(); ctx.moveTo(sx, sy); ctx.lineTo(sx - len, sy - len * 0.36); ctx.stroke();
          if (shoot.l > 40) shoot = null;
        }
      }
      if (running) raf = requestAnimationFrame(frame);
    }
    size();
    window.addEventListener('resize', function () { size(); if (!running) frame(); });
    if (REDUCED) { frame(); return; }
    var io2 = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (en.isIntersecting && !running) { running = true; raf = requestAnimationFrame(frame); }
        else if (!en.isIntersecting && running) { running = false; cancelAnimationFrame(raf); }
      });
    });
    io2.observe(canvas);
  }
  $$('canvas[data-fx]').forEach(fx);

  /* ------------------------------------------------------------ S1: next-token sampler */
  $$('[data-widget="sampler"]').forEach(function (w) {
    var cands = JSON.parse(w.getAttribute('data-cands'));
    var rows = w.querySelector('.rows'), temp = w.querySelector('input[type=range]'), tv = w.querySelector('.tval');
    var draws = w.querySelector('.draws'), btn = w.querySelector('.sample'), stemOut = w.querySelector('.stem .pick');
    cands.forEach(function (c) {
      var r = document.createElement('div'); r.className = 'row';
      r.innerHTML = '<span class="w"></span><span class="track"><span class="fill"></span></span><span class="p"></span>';
      r.querySelector('.w').textContent = c[0];
      rows.appendChild(r);
    });
    function probs() {
      var T = parseFloat(temp.value);
      if (T < 0.05) { var mx = 0; cands.forEach(function (c, i) { if (c[1] > cands[mx][1]) mx = i; }); return cands.map(function (c, i) { return i === mx ? 1 : 0; }); }
      var ex = cands.map(function (c) { return Math.exp(c[1] / T); });
      var sum = ex.reduce(function (a, b) { return a + b; }, 0);
      return ex.map(function (e) { return e / sum; });
    }
    function paint(pick) {
      var p = probs(), T = parseFloat(temp.value);
      tv.textContent = T.toFixed(1);
      $$('.row', rows).forEach(function (r, i) {
        r.querySelector('.fill').style.width = (p[i] * 100).toFixed(1) + '%';
        r.querySelector('.p').textContent = (p[i] * 100).toFixed(0) + '%';
        r.classList.toggle('pick', i === pick);
      });
    }
    function sample() {
      var p = probs(), out = [];
      draws.textContent = '';
      for (var k = 0; k < 10; k++) {
        var r = Math.random(), acc = 0, i = 0;
        for (; i < p.length; i++) { acc += p[i]; if (r <= acc) break; }
        i = Math.min(i, p.length - 1);
        out.push(i);
        (function (idx, delay) {
          setTimeout(function () {
            var s = document.createElement('span'); s.textContent = cands[idx][0]; draws.appendChild(s);
          }, REDUCED ? 0 : delay);
        })(i, k * 70);
      }
      paint(out[0]);
      if (stemOut) stemOut.textContent = ' ' + cands[out[0]][0];
    }
    temp.addEventListener('input', function () { paint(-1); });
    btn.addEventListener('click', sample);
    paint(-1);
  });

  /* ------------------------------------------------------------ S1: age-gate dots */
  $$('[data-widget="agegate"]').forEach(function (w) {
    var field = w.querySelector('.dots'), total = +w.getAttribute('data-total'), u = +w.getAttribute('data-u25');
    var count = w.querySelector('.dots-count .v'), btn = w.querySelector('button.apply');
    var idx = [];
    for (var i = 0; i < total; i++) idx.push(i);
    // spread the under-25s through the field deterministically
    var marks = {}; for (var k = 0; k < u; k++) marks[Math.round((k + 0.5) * total / u + (k % 3) - 1)] = true;
    idx.forEach(function (i) { var d = document.createElement('i'); if (marks[i]) d.className = 'u25'; d.setAttribute('aria-hidden', 'true'); field.appendChild(d); });
    var on = false;
    function animTo(a, b) {
      if (REDUCED) { count.textContent = b; return; }
      var t0 = null;
      function st(ts) { if (!t0) t0 = ts; var p = Math.min(1, (ts - t0) / 700); count.textContent = Math.round(a + (b - a) * p); if (p < 1) requestAnimationFrame(st); }
      requestAnimationFrame(st);
    }
    btn.addEventListener('click', function () {
      on = !on;
      field.classList.toggle('gated', on);
      btn.textContent = on ? 'Remove the rules again' : 'Apply the age-gate';
      animTo(on ? total : total - u, on ? total - u : total);
      w.querySelector('.after').hidden = !on;
    });
  });

  /* ------------------------------------------------------------ S1: the NULL lab */
  $$('[data-widget="nullab"]').forEach(function (w) {
    var sets = JSON.parse(w.getAttribute('data-sets'));
    var tbody = w.querySelector('tbody'), verdict = w.querySelector('.verdict');
    var cur = { set: 'mixed', f: 'ne' };
    function truth(v, f) {
      if (f === 'ne') return v === null ? 'u' : (v !== 4 ? 't' : 'f');
      if (f === 'idf') return v === 4 ? 'f' : 't';
      if (f === 'or') return v === null ? 't' : (v !== 4 ? 't' : 'f');
    }
    var label = { t: 'TRUE', f: 'FALSE', u: 'UNKNOWN' };
    function paint() {
      var rows = sets[cur.set].rows;
      tbody.textContent = '';
      var kept = 0;
      rows.forEach(function (r) {
        var tv = truth(r[1], cur.f), tr = document.createElement('tr');
        tr.className = tv === 't' ? 'keep' : 'drop';
        if (tv === 't') kept++;
        var c0 = document.createElement('td'); c0.textContent = r[0];
        var c1 = document.createElement('td'); c1.textContent = r[1] === null ? 'NULL' : r[1];
        var c2 = document.createElement('td'); var sp = document.createElement('span'); sp.className = 'tv ' + tv; sp.textContent = label[tv]; c2.appendChild(sp);
        var c3 = document.createElement('td'); c3.textContent = tv === 't' ? 'kept' : 'dropped';
        tr.appendChild(c0); tr.appendChild(c1); tr.appendChild(c2); tr.appendChild(c3);
        tbody.appendChild(tr);
      });
      var s = sets[cur.set];
      var keptAll = s.scale ? (kept === rows.length ? s.scale : 0) : kept;
      var totalAll = s.scale || rows.length;
      verdict.className = 'verdict ' + ((keptAll === 0 || (!s.scale && cur.f === 'ne')) ? 'bad' : 'good');
      verdict.textContent = s.scale
        ? ('Kept ' + fmt(keptAll) + ' of ' + fmt(totalAll) + ' Indonesia events' + (keptAll === 0 ? '. No error. "Nobody adopted VEEV."' : '. Nothing lost: campaign 4 never had an event.'))
        : ('Kept ' + kept + ' of ' + rows.length + ' rows' + (cur.f === 'ne' ? '. Every NULL row vanished.' : '. Only campaign 4 is gone.'));
      var hd = w.querySelector('.filter-sql'); if (hd) hd.textContent = { ne: 'campaign_id <> 4', idf: 'campaign_id IS DISTINCT FROM 4', or: 'campaign_id IS NULL OR campaign_id <> 4' }[cur.f];
    }
    $$('.seg', w).forEach(function (seg) {
      var key = seg.getAttribute('data-k');
      $$('button', seg).forEach(function (b) {
        b.addEventListener('click', function () {
          cur[key] = b.getAttribute('data-v');
          $$('button', seg).forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
          paint();
        });
      });
    });
    paint();
  });

  /* ------------------------------------------------------------ S1: template, two markets */
  $$('[data-widget="tpl"]').forEach(function (w) {
    var vals = JSON.parse(w.getAttribute('data-vals'));
    var seg = w.querySelector('.seg');
    function paint(m, flash) {
      $$('dd[data-k]', w).forEach(function (dd) {
        var v = vals[m][dd.getAttribute('data-k')];
        if (dd.textContent !== v) { dd.textContent = v; if (flash) { dd.classList.remove('flash'); void dd.offsetWidth; dd.classList.add('flash'); } }
      });
    }
    $$('button', seg).forEach(function (b) {
      b.addEventListener('click', function () {
        $$('button', seg).forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
        paint(b.getAttribute('data-v'), true);
      });
    });
    paint('ID', false);
  });

  /* ------------------------------------------------------------ S2: two faces, real | synthetic */
  $$('[data-widget="face"]').forEach(function (cv) {
    var dots = JSON.parse(cv.getAttribute('data-dots') || '[]');
    var FW = 680, FH = 610, STEP = 8.5;
    var ctx = cv.getContext('2d'), dpr = Math.min(2, window.devicePixelRatio || 1);
    var A, B, W, H, k, raf = 0, running = false, t0 = performance.now(), hot = 0;
    function build() {
      W = cv.getBoundingClientRect().width || 560; H = W * FH / FW; k = W / FW;
      cv.style.height = H + 'px';
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
      A = document.createElement('canvas'); B = document.createElement('canvas');
      [A, B].forEach(function (c) { c.width = cv.width; c.height = cv.height; });
      var a = A.getContext('2d'), b = B.getContext('2d');
      a.setTransform(dpr * k, 0, 0, dpr * k, 0, 0); b.setTransform(dpr * k, 0, 0, dpr * k, 0, 0);
      var seed = 11;
      function rnd() { seed = (seed * 16807) % 2147483647; return seed / 2147483647; }
      dots.forEach(function (d) {
        var x = d[0], y = d[1], r = d[2], al = Math.min(1, 0.4 + r / STEP);
        a.fillStyle = 'rgba(0,201,167,' + al.toFixed(2) + ')';
        a.beginPath(); a.arc(x, y, r, 0, 6.283); a.fill();
        var s = 2 * r * 0.92 * (1 + (rnd() - 0.5) * 0.25), g = 90 + Math.round(70 * Math.min(1, r / (STEP * 0.52)));
        b.fillStyle = 'rgba(255,' + g + ',20,' + al.toFixed(2) + ')';
        b.fillRect(FW - x - s / 2, y - s / 2, s, s);
      });
    }
    function frame(now) {
      var t = (now - t0) / 1000;
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.clearRect(0, 0, cv.width, cv.height);
      ctx.drawImage(A, 0, 0);
      ctx.drawImage(B, 0, 0);
      var half = Math.round(cv.width / 2);
      var beam = ((t % 6) / 6) * cv.height * 1.2 - cv.height * 0.1;
      // glitch slices on the synthetic face: always near the beam, sometimes elsewhere
      var slices = [[beam - 14 * dpr, 10 * dpr, 1], [beam + 6 * dpr, 6 * dpr, -1]];
      for (var i = 0; i < 3; i++) {
        var ph = Math.sin(t * (2.3 + i) + i * 2.1);
        if (ph > 0.7 - hot * 0.5) slices.push([((Math.sin(t * 0.7 + i * 5.3) + 1) / 2) * cv.height, (6 + i * 7) * dpr, i % 2 ? 1 : -1]);
      }
      slices.forEach(function (s) {
        var y = Math.max(0, Math.round(s[0])), h = Math.round(s[1]);
        if (y + h > cv.height) return;
        var dx = Math.round((10 + 16 * Math.abs(Math.sin(t * 7 + s[0]))) * dpr * (1 + hot)) * s[2];
        ctx.clearRect(half, y, cv.width - half, h);
        ctx.drawImage(B, half, y, cv.width - half, h, half + dx, y, cv.width - half, h);
      });
      // the scan beam
      var g = ctx.createLinearGradient(0, beam - 30 * dpr, 0, beam + 30 * dpr);
      g.addColorStop(0, 'rgba(255,255,255,0)'); g.addColorStop(0.5, 'rgba(255,255,255,.10)'); g.addColorStop(1, 'rgba(255,255,255,0)');
      ctx.fillStyle = g; ctx.fillRect(0, beam - 30 * dpr, cv.width, 60 * dpr);
      ctx.fillStyle = 'rgba(255,255,255,.45)'; ctx.fillRect(0, beam, cv.width, dpr);
      hot = Math.max(0, hot - 0.02);
      if (running) raf = requestAnimationFrame(frame);
    }
    cv.addEventListener('pointermove', function () { hot = Math.min(1, hot + 0.15); });
    build();
    window.addEventListener('resize', function () { build(); if (!running) frame(performance.now()); });
    if (REDUCED) { frame(t0 + 2500); return; }
    new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (en.isIntersecting && !running) { running = true; raf = requestAnimationFrame(frame); }
        else if (!en.isIntersecting && running) { running = false; cancelAnimationFrame(raf); }
      });
    }).observe(cv);
  });

  /* ------------------------------------------------------------ S2: cost calculator */
  $$('[data-widget="cost"]').forEach(function (w) {
    var P = { opusOut: 20, haikuOut: 0.5 };            // $ per million output tokens (Anthropic API, Oct 2026)
    var PLAN = 800, PER_ROW = 50;                       // output tokens: the blueprint, and per generated row
    var rowsIn = w.querySelector('[name=rows]'), runsIn = w.querySelector('[name=runs]');
    var stops = [100, 1000, 10000, 100000];
    function money(v) { return v < 0.1 ? '$' + v.toFixed(3) : v < 100 ? '$' + v.toFixed(2) : '$' + fmt(Math.round(v)); }
    function paint() {
      var rows = stops[+rowsIn.value], runs = +runsIn.value;
      w.querySelector('.rows-v').textContent = fmt(rows);
      w.querySelector('.runs-v').textContent = runs;
      var plan = PLAN * P.opusOut / 1e6, opusRows = rows * PER_ROW * P.opusOut / 1e6, haikuRows = rows * PER_ROW * P.haikuOut / 1e6;
      var all = (plan + opusRows) * runs, split = (plan + haikuRows) * runs;
      var max = all;
      w.querySelector('.all .op').style.width = (100 * all / max) + '%';
      w.querySelector('.split .op').style.width = Math.max(0.6, 100 * plan * runs / max) + '%';
      w.querySelector('.split .hk').style.width = Math.max(0.6, 100 * haikuRows * runs / max) + '%';
      w.querySelector('.all .cost').textContent = money(all);
      w.querySelector('.split .cost').textContent = money(split);
      w.querySelector('.verdict .x').textContent = (all / split).toFixed(1) + '×';
      w.querySelector('.verdict .per').textContent = runs === 1 ? 'for one run' : 'per week, ' + runs + ' runs';
    }
    rowsIn.addEventListener('input', paint); runsIn.addEventListener('input', paint);
    paint();
  });

  /* ------------------------------------------------------------ S2: divergence board */
  $$('[data-widget="diverge"]').forEach(function (w) {
    $$('input[data-k]', w).forEach(function (inp) {
      var k = inp.getAttribute('data-k');
      if (S.inputs[k]) inp.value = S.inputs[k];
      inp.addEventListener('input', function () { S.inputs[k] = inp.value.slice(0, 120); save(); });
    });
    $$('.dv-w[data-after]', w).forEach(function (cell) {
      var id = cell.getAttribute('data-after');
      function open() { cell.classList.remove('hidden'); cell.removeAttribute('tabindex'); cell.removeAttribute('role'); }
      var d = document.querySelector('details.reveal[data-p="' + id + '"]');
      if (d && d.open) open();
      document.addEventListener('revealopen', function (e) { if (e.detail === d) open(); });
      cell.addEventListener('click', open);
      cell.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
    });
  });

  /* ------------------------------------------------------------ S3: three blanks */
  $$('[data-widget="blanks"]').forEach(function (w) {
    $$('.blank', w).forEach(function (b) {
      b.addEventListener('click', function () {
        var card = w.querySelector('.bcard[data-k="' + b.getAttribute('data-k') + '"]');
        var on = b.getAttribute('aria-expanded') !== 'true';
        b.setAttribute('aria-expanded', on ? 'true' : 'false');
        if (card) card.classList.toggle('open', on);
      });
    });
  });

  /* ------------------------------------------------------------ S3: percent vs points */
  $$('[data-widget="pvp"]').forEach(function (w) {
    var h = w.querySelector('.headline'), sub = w.querySelector('.sub');
    var txt = JSON.parse(w.getAttribute('data-txt'));
    $$('.seg button', w).forEach(function (b) {
      b.addEventListener('click', function () {
        $$('.seg button', w).forEach(function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
        var t = txt[b.getAttribute('data-v')];
        h.innerHTML = t[0]; sub.textContent = t[1];
      });
    });
  });

  /* ------------------------------------------------------------ S3: confidence picker */
  $$('[data-widget="conf"]').forEach(function (w) {
    var id = w.getAttribute('data-id'), out = w.parentNode.querySelector('.conf-out');
    var btns = $$('button', w);
    function paint() {
      var v = S.picks[id];
      w.classList.toggle('picked', !!v);
      btns.forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-v') === v ? 'true' : 'false'); });
      if (out) out.innerHTML = v ? 'Locked in: <b>' + v + '/5</b>. Now open the model answer below and compare.' : '';
    }
    btns.forEach(function (b) { b.addEventListener('click', function () { S.picks[id] = b.getAttribute('data-v'); S.guesses[id] = b.getAttribute('data-v') + '/5'; save(); paint(); showGuess(id); }); });
    paint();
  });

  /* ------------------------------------------------------------ S4: verdict board */
  $$('[data-widget="verdicts"]').forEach(function (w) {
    var claims = $$('.claim', w), score = w.querySelector('.score');
    function tally() {
      var right = 0, done = 0;
      claims.forEach(function (c) { var v = S.picks['v-' + c.getAttribute('data-id')]; if (v) { done++; if (v === c.getAttribute('data-correct')) right++; } });
      score.textContent = done ? ('Your calls match the evidence on ' + right + ' of ' + done + (done < claims.length ? ' so far' : '') + '.') : 'Make a call on each claim.';
    }
    claims.forEach(function (c) {
      var id = 'v-' + c.getAttribute('data-id'), correct = c.getAttribute('data-correct'), fb = c.querySelector('.fb');
      function paint() {
        var v = S.picks[id];
        $$('button', c).forEach(function (b) { b.setAttribute('aria-pressed', b.getAttribute('data-v') === v ? 'true' : 'false'); });
        c.classList.toggle('answered', !!v);
        if (v) {
          fb.className = 'fb ' + (v === correct ? 'right' : 'wrong');
          var head = v === correct ? 'Same call as the evidence. ' : 'The evidence says ' + correct + '. ';
          fb.innerHTML = '<b>' + head + '</b>' + c.getAttribute('data-why');
        }
      }
      $$('button', c).forEach(function (b) { b.addEventListener('click', function () { S.picks[id] = b.getAttribute('data-v'); save(); paint(); tally(); }); });
      paint();
    });
    tally();
  });

  /* ------------------------------------------------------------ S4: exhibit highlights */
  $$('.exhibit mark').forEach(function (m, i) {
    var k = 'mark-' + PAGE + '-' + i;
    if (S.picks[k]) m.classList.add('on');
    m.setAttribute('tabindex', '0');
    m.setAttribute('role', 'button');
    m.setAttribute('title', 'Click to flag this claim as suspicious');
    function t() { var on = m.classList.toggle('on'); if (on) S.picks[k] = 1; else delete S.picks[k]; save(); }
    m.addEventListener('click', t);
    m.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); t(); } });
  });

  /* ------------------------------------------------------------ S4: 3,000-consumer waffle */
  $$('[data-widget="waffle"]').forEach(function (cv) {
    var total = +cv.getAttribute('data-total'), dev = +cv.getAttribute('data-dev'), claim = +cv.getAttribute('data-claim');
    var cols = 75, rowsN = Math.ceil(total / cols), ctx = cv.getContext('2d'), dpr = Math.min(2, window.devicePixelRatio || 1);
    var shown = REDUCED ? total : 0, started = false;
    function col(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim() || '#3B6BC4'; }
    function draw() {
      var W = cv.getBoundingClientRect().width, cell = W / cols, H = cell * rowsN + 34;
      cv.style.height = H + 'px'; cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var cMain = col('--c-main'), cDim = col('--c-dim'), cBad = col('--bad'), ink = col('--muted');
      for (var i = 0; i < total; i++) {
        var r = Math.floor(i / cols), c = i % cols;
        ctx.fillStyle = i < Math.min(shown, total) ? (i < dev ? cMain : cDim) : 'rgba(128,140,160,.12)';
        var s = cell * 0.72;
        ctx.beginPath();
        ctx.arc(c * cell + cell / 2, r * cell + cell / 2, s / 2, 0, 6.283);
        ctx.fill();
      }
      // the 94% claim: where it would end
      var cr = Math.floor(claim / cols), cc = claim % cols;
      ctx.strokeStyle = cBad; ctx.lineWidth = 2; ctx.setLineDash([5, 4]);
      ctx.beginPath();
      ctx.moveTo(cc * cell, cr * cell); ctx.lineTo(cc * cell, (cr + 1) * cell); ctx.lineTo(cols * cell, (cr + 1) * cell);
      ctx.moveTo(0, (cr + 1) * cell); ctx.lineTo(0, (cr + 1) * cell);
      ctx.stroke();
      ctx.beginPath(); ctx.moveTo(0, cr * cell); ctx.lineTo(cc * cell, cr * cell); ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = cBad; ctx.font = '500 12px "DM Mono", monospace';
      ctx.fillText('94% claimed ends here (2,820)', Math.min(cc * cell + 6, W - 210), rowsN * cell + 22);
      var dr = Math.floor(dev / cols), dc = dev % cols;
      ctx.fillStyle = ink;
      ctx.fillText('devices end at 2,391 (79.7%)', 0, rowsN * cell + 22);
    }
    function grow() {
      if (started) return; started = true;
      if (REDUCED) { shown = total; draw(); return; }
      var t0 = null;
      function st(ts) { if (!t0) t0 = ts; var p = Math.min(1, (ts - t0) / 1600); shown = Math.round(total * (1 - Math.pow(1 - p, 3))); draw(); if (p < 1) requestAnimationFrame(st); }
      requestAnimationFrame(st);
    }
    draw();
    window.addEventListener('resize', draw);
    document.addEventListener('themechange', draw);
    var d = cv.closest('details');
    if (d) d.addEventListener('toggle', function () { if (d.open) { draw(); grow(); } });
    else if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { if (es[0].isIntersecting) grow(); }).observe(cv);
    else grow();
  });

  /* QA helper: ?open opens every reveal and flips every card (for screenshots) */
  if (/[?&]open\b/.test(location.search)) {
    $$('details.reveal').forEach(function (d) { d.open = true; d.dispatchEvent(new Event('toggle')); });
    setTimeout(function () { $$('.card3d').forEach(function (c) { c.classList.add('flipped'); }); $$('.xray').forEach(function (x) { x.classList.add('on'); }); $$('[data-widget="agegate"] button.apply').forEach(function (b) { b.click(); }); }, 50);
  }

  /* ------------------------------------------------------------ collectible card */
  $$('.card3d[data-card]').forEach(function (c) {
    var id = c.getAttribute('data-card');
    if (S.cards[id]) c.classList.add('flipped');
    c.setAttribute('aria-pressed', S.cards[id] ? 'true' : 'false');
    c.addEventListener('click', function () {
      var on = c.classList.toggle('flipped');
      c.setAttribute('aria-pressed', on ? 'true' : 'false');
      if (on) S.cards[id] = true;
      save(); markCollected();
    });
  });
  function markCollected() {
    $$('[data-collect]').forEach(function (el) {
      var on = !!S.cards[el.getAttribute('data-collect')];
      el.classList.toggle('collected', on);
      el.classList.toggle('got', on && el.classList.contains('slot'));
    });
    var n = Object.keys(S.cards).filter(function (k) { return S.cards[k]; }).length;
    $$('[data-score="cards"]').forEach(function (e) { e.textContent = n; });
    $$('.nav a[data-collect]').forEach(function (a) {
      var m = a.querySelector('.done-mark'); if (m) m.hidden = !S.cards[a.getAttribute('data-collect')];
    });
  }
  markCollected();

  /* ------------------------------------------------------------ pre-flight checklist */
  $$('.checks input[data-k]').forEach(function (cb) {
    var k = cb.getAttribute('data-k');
    cb.checked = !!S.picks[k];
    cb.addEventListener('change', function () { if (cb.checked) S.picks[k] = 1; else delete S.picks[k]; save(); });
  });

  /* ------------------------------------------------------------ reset */
  $$('[data-reset]').forEach(function (b) {
    b.addEventListener('click', function () {
      if (!window.confirm('Clear your guesses, score, progress and cards in this browser?')) return;
      try { localStorage.removeItem(KEY); } catch (e) {}
      location.reload();
    });
  });

  /* ------------------------------------------------------------ glossary filter */
  var q = $('#glossary-search');
  if (q) {
    var groups = $$('.gloss-group'), count = $('#glossary-count'), empty = $('#glossary-empty');
    var all = $$('.gloss .term');
    function filter() {
      var term = q.value.trim().toLowerCase(), shown = 0;
      all.forEach(function (t) { var hit = !term || t.textContent.toLowerCase().indexOf(term) !== -1; t.hidden = !hit; if (hit) shown++; });
      groups.forEach(function (g) { g.hidden = !$$('.term', g).some(function (t) { return !t.hidden; }); });
      if (count) count.textContent = shown + ' of ' + all.length + ' terms';
      if (empty) empty.hidden = shown !== 0;
    }
    q.addEventListener('input', filter);
    filter();
  }
})();
