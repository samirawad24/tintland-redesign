(function () {
  var d = document;
  d.documentElement.classList.add('js');
  var PHONE = '14077232809';

  // mobile menu
  var menu = d.querySelector('.menu'), nav = d.querySelector('.nav');
  if (menu && nav) {
    menu.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      menu.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // reveal on scroll
  var rv = d.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px' });
    rv.forEach(function (el) { io.observe(el); });
  } else {
    rv.forEach(function (el) { el.classList.add('in'); });
  }

  // gallery lightbox
  var dlg = d.querySelector('#lightbox');
  if (dlg && dlg.showModal) {
    var big = dlg.querySelector('img');
    d.querySelectorAll('.gal a').forEach(function (a) {
      a.addEventListener('click', function (e) {
        e.preventDefault();
        big.src = a.href;
        big.alt = a.querySelector('img').alt;
        dlg.showModal();
      });
    });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
  }

  // tint simulator
  var LEVELS = [
    { v: null, op: 0, desc: 'Bare glass, the way most front doors leave the factory.' },
    { v: 70, op: 0.22, desc: 'Close to clear. You get the heat and UV protection without changing the look.' },
    { v: 50, op: 0.40, desc: 'A light smoke. People can still see in.' },
    { v: 35, op: 0.56, desc: 'The middle ground. Real privacy, and still easy to see out at night.' },
    { v: 20, op: 0.74, desc: 'Dark. Hard to see in during the day.' },
    { v: 15, op: 0.82, desc: 'Very dark. Daytime privacy is close to total.' },
    { v: 5, op: 0.94, desc: 'Limo tint. Nobody sees in, and you see less at night.' }
  ];
  d.querySelectorAll('.sim').forEach(function (sim) {
    var range = sim.querySelector('input[type=range]'), tint = sim.querySelector('.tint'),
        num = sim.querySelector('.sim-num'), cap = sim.querySelector('.sim-cap'), desc = sim.querySelector('.sim-desc'),
        ticks = sim.querySelectorAll('.ticks button'), rows = sim.querySelectorAll('.legal b');
    var LIMITS = [28, 15, 6];
    function set(i) {
      var L = LEVELS[i];
      range.value = i;
      tint.style.opacity = L.op;
      num.textContent = L.v === null ? 'None' : L.v + '%';
      cap.textContent = L.v === null ? 'no film on the glass' : 'of visible light gets through';
      desc.textContent = L.desc;
      range.setAttribute('aria-valuetext', L.v === null ? 'No tint' : L.v + ' percent');
      ticks.forEach(function (b, k) { b.setAttribute('aria-pressed', k === i ? 'true' : 'false'); });
      rows.forEach(function (b, k) {
        var ok = L.v === null || L.v >= LIMITS[k];
        b.textContent = ok ? 'Legal in Florida' : 'Too dark for Florida';
        b.className = ok ? 'ok' : 'no';
      });
    }
    range.addEventListener('input', function () { set(parseInt(range.value, 10)); });
    ticks.forEach(function (b, k) { b.addEventListener('click', function () { set(k); }); });
    set(parseInt(range.value, 10));
  });

  function send(kind, text) {
    var url = kind === 'wa'
      ? 'https://wa.me/' + PHONE + '?text=' + encodeURIComponent(text)
      : 'sms:+' + PHONE + '?&body=' + encodeURIComponent(text);
    window.location.href = url;
  }
  var money = function (n) { return '$' + n.toLocaleString('en-US'); };

  // price builder
  var pf = d.querySelector('#price-form');
  if (pf) {
    var P = window.TL_PRICES;
    var VEH = { two: '2-door car', four: '4-door sedan', suv: 'SUV or pickup' };
    var FILM = { cs: 'Prime CS', hp: 'Prime HP', xr: 'Prime XR ceramic', xrp: 'Prime XR Plus ceramic' };
    var out = d.querySelector('#q-total'), list = d.querySelector('#q-lines'), last = '';
    function calc() {
      var f = new FormData(pf), v = f.get('vehicle'), film = f.get('film'), ws = f.get('windshield');
      var lines = [[VEH[v] + ', ' + FILM[film], P.base[v][film]]];
      if (ws === 'visor') lines.push(['Visor strip, ' + FILM[film], P.visor[film]]);
      if (ws === 'xr') lines.push(['Full windshield, Prime XR ceramic', P.windshield.xr]);
      if (ws === 'xrp') lines.push(['Full windshield, Prime XR Plus ceramic', P.windshield.xrp]);
      var total = lines.reduce(function (s, l) { return s + l[1]; }, 0);
      out.textContent = money(total);
      list.innerHTML = '';
      lines.forEach(function (l) {
        var li = d.createElement('li'), a = d.createElement('span'), b = d.createElement('b');
        a.textContent = l[0]; b.textContent = money(l[1]); li.appendChild(a); li.appendChild(b); list.appendChild(li);
      });
      last = 'Hi Tintland, I priced a tint job on your site.\n' +
        lines.map(function (l) { return l[0] + ': ' + money(l[1]); }).join('\n') +
        '\nTotal: ' + money(total) + '\nMy car (year, make, model): ';
    }
    pf.addEventListener('change', calc);
    pf.addEventListener('submit', function (e) { e.preventDefault(); });
    d.querySelector('#q-wa').addEventListener('click', function () { send('wa', last); });
    d.querySelector('#q-sms').addEventListener('click', function () { send('sms', last); });
    calc();
  }

  // estimate form
  var ef = d.querySelector('#est-form');
  if (ef) {
    var carBox = d.querySelector('#est-car'), placeBox = d.querySelector('#est-place'), err = d.querySelector('#est-err');
    function mode() {
      var car = new FormData(ef).get('kind') === 'Car';
      carBox.hidden = !car; placeBox.hidden = car;
    }
    ef.addEventListener('change', mode);
    ef.addEventListener('submit', function (e) { e.preventDefault(); });
    function build() {
      var f = new FormData(ef), kind = f.get('kind'), g = function (k) { return (f.get(k) || '').toString().trim(); };
      var miss = !g('name') || (kind === 'Car' ? (!g('year') || !g('make') || !g('model')) : !g('address'));
      if (miss) {
        err.textContent = kind === 'Car' ? 'Add your name and the year, make and model of the car.' : 'Add your name and the address of the property.';
        return null;
      }
      err.textContent = '';
      var t = 'Hi Tintland, I would like a free estimate.\nName: ' + g('name') + '\nJob: ' + kind + ' tint';
      if (kind === 'Car') t += '\nCar: ' + g('year') + ' ' + g('make') + ' ' + g('model') + (g('film') ? '\nFilm: ' + g('film') : '');
      else t += '\nAddress: ' + g('address');
      if (g('notes')) t += '\nNotes: ' + g('notes');
      return t;
    }
    d.querySelector('#est-wa').addEventListener('click', function () { var t = build(); if (t) send('wa', t); });
    d.querySelector('#est-sms').addEventListener('click', function () { var t = build(); if (t) send('sms', t); });
    mode();
  }
})();
