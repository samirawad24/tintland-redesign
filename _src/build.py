"""Builds the Tintland Orlando concept site. Run: python _src/build.py"""
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
PHONE = "407-723-2809"
TEL = "tel:+14077232809"
EMAIL = "tintlandorlando@gmail.com"
ADDR1, ADDR2 = "1710 N Goldenrod Rd, Ste 2F", "Orlando, FL 32807"
MAPQ = "Tintland+Window+Tinting,+1710+N+Goldenrod+Rd+STE+2F,+Orlando,+FL+32807"
MAPS = f"https://www.google.com/maps/search/?api=1&query={MAPQ}"
VER = hashlib.md5((ROOT / "assets/site.css").read_bytes() + (ROOT / "assets/site.js").read_bytes()).hexdigest()[:8]

PRICES = dict(
    base=dict(two=dict(cs=190, hp=240, xr=300, xrp=500), four=dict(cs=200, hp=250, xr=320, xrp=520),
              suv=dict(cs=220, hp=260, xr=340, xrp=540)),
    windshield=dict(xr=180, xrp=220), visor=dict(cs=30, hp=40, xr=50, xrp=80),
)
PRICE_JS = f"<script>window.TL_PRICES={json.dumps(PRICES)};</script>\n"
FILMS = [
    ("cs", "Prime CS", "Dyed film", "Color-stable dyed film. The lowest price, for a darker look and UV protection."),
    ("hp", "Prime HP", "Metalized film", "Dyed film with a metalized layer, which reflects more of the sun's heat than dyed film alone."),
    ("xr", "Prime XR", "Ceramic film", "Ceramic film. It rejects heat without metal, so it doesn't get in the way of phone, GPS or radio signals."),
    ("xrp", "Prime XR Plus", "Top ceramic film", "XPEL's top ceramic film for heat. The one to pick if your car sits in a Florida parking lot all day."),
]
SWATCH = ["#b0c0ce", "#8b98a3", "#6d7780", "#525a61", "#34393e", "#262a2e", "#121417"]
STOPS = ["Off", "70", "50", "35", "20", "15", "5"]


def icon(name):
    svg = (Path(__file__).parent / f"{name}.svg").read_text(encoding="utf-8")
    path = svg[svg.index("<path"):svg.index("</svg>")]
    return f'<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true">{path}</svg>'


SOCIAL = "".join(f'<a href="{u}" rel="noopener" aria-label="Tintland Orlando on {n}">{icon(n.lower())}</a>' for n, u in [
    ("Instagram", "https://www.instagram.com/tintlandorlando/"), ("Facebook", "https://www.facebook.com/tintlandorlando")])


def btn(kind, href, label, extra=""):
    return f'<a class="btn btn-{kind}" href="{href}"{extra}><span>{label}</span></a>'


def pic(slug, alt, sizes="(max-width:860px) 100vw, 50vw", eager=False):
    w, h = Image.open(IMG / f"{slug}.webp").size
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img src="assets/img/{slug}-800.webp" srcset="assets/img/{slug}-800.webp 800w, assets/img/{slug}.webp {w}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{alt}" {load}>')


NAV = [("tint-simulator.html", "Simulator"), ("prices.html", "Prices"), ("gallery.html", "Gallery"), ("about.html", "About")]


def page(fname, title, desc, body, scripts=""):
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == fname else ""}>{t}</a>' for h, t in NAV)
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0c0c0d">
<meta name="color-scheme" content="dark">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="assets/img/og.jpg">
<meta property="og:type" content="website">
<link rel="preload" href="assets/fonts/barlow-condensed-800-italic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/barlow-400-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css?v={VER}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hdr">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Tintland Orlando, home"><img src="assets/img/tintland-logo.png" width="197" height="58" alt="Tintland Orlando"></a>
    <button class="menu" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main">{nav}{btn('p', 'estimate.html', 'Free estimate')}</nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="ftr">
  <div class="wrap">
    <img src="assets/img/tintland-logo.png" width="640" height="188" alt="Tintland Orlando" loading="lazy">
    <nav aria-label="Footer">
      <a href="tint-simulator.html">Simulator</a><a href="prices.html">Prices</a><a href="gallery.html">Gallery</a><a href="about.html">About</a><a href="estimate.html">Free estimate</a>
    </nav>
    <div class="social">{SOCIAL}</div>
    <div class="note">
      <span>Tintland Window Tinting LLC, {ADDR1}, {ADDR2}. Tintland confirms your price before the job starts.</span>
      <span>Concept redesign by <a href="https://madebyawad.com" rel="noopener">Made by Awad</a>. Not the official Tintland site.</span>
    </div>
  </div>
</footer>
<div class="bar">
  {btn('s', TEL, 'Call')}
  {btn('p', 'estimate.html', 'Free estimate')}
</div>
{scripts}<script src="assets/site.js?v={VER}" defer></script>
</body>
</html>
"""
    assert "—" not in html and "–" not in html, f"dash in {fname}"
    (ROOT / fname).write_text(html, encoding="utf-8", newline="\n")
    print("built", fname)


def simhero(h1, sub, second):
    cw, ch = Image.open(IMG / "sim-car.webp").size
    sw = "".join(f'<div class="sw{" on" if i == 3 else ""}" style="background:{c}"></div>' for i, c in enumerate(SWATCH))
    lb = "".join(f'<span{" class=\"on\"" if i == 3 else ""}>{s}</span>' for i, s in enumerate(STOPS))
    return f"""
<section class="simhero">
  <div class="wrap">
    <div class="sh-copy">
      <h1>{h1}</h1>
      <p>{sub}</p>
      <div class="btns">{btn('p', 'estimate.html', 'Free estimate')}{second}</div>
    </div>
    <div class="sh-num" aria-live="polite">35%</div>
    <div class="sh-stage">
      <img src="assets/img/sim-car-900.webp" srcset="assets/img/sim-car-900.webp 900w, assets/img/sim-car.webp {cw}w" sizes="(max-width:1000px) 92vw, 960px" width="{cw}" height="{ch}" alt="White SUV seen from the side" fetchpriority="high">
      <img class="tint" src="assets/img/sim-tint-900.webp" srcset="assets/img/sim-tint-900.webp 900w, assets/img/sim-tint.webp {cw}w" sizes="(max-width:1000px) 92vw, 960px" width="{cw}" height="{ch}" alt="" aria-hidden="true">
    </div>
    <div class="sim-ctl">
      <input class="sr" type="range" min="0" max="6" step="1" value="3" aria-label="Tint level, from no tint to 5 percent">
      <div class="swatches" aria-hidden="true">{sw}</div>
      <div class="sw-l" aria-hidden="true">{lb}</div>
    </div>
    <div class="sim-out">
      <p class="sim-desc">The middle ground. Real privacy, and still easy to see out at night.</p>
      <div class="legal">
        <div><span>Front doors</span><b>Legal</b></div>
        <div><span>Back glass, sedan</span><b>Legal</b></div>
        <div><span>Back glass, SUV or van</span><b>Legal</b></div>
      </div>
    </div>
    <p class="credit">Numbers are the share of light that gets through. Legal status follows Florida law. Your screen is a guide, so see the samples at the shop. Car photo: <a href="https://commons.wikimedia.org/wiki/File:Audi_Q4_e-tron_2021-1_seitenansicht.jpg" rel="noopener">Sestmedia, CC BY-SA 4.0</a>, edited.</p>
  </div>
</section>"""


def visit(h="Run by a tinter since 2020.", top0=True):
    st = ' style="padding-top:0"' if top0 else ""
    return f"""
<section class="sec" id="visit"{st}>
  <div class="wrap shop">
    <div class="shop-img rv">{pic('shop-front', 'Yellow Lamborghini parked outside the Tintland Orlando shop', '(max-width:860px) 100vw, 40vw')}</div>
    <div class="rv">
      <h2>{h}</h2>
      <p>John Uzcategui opened Tintland Window Tinting in 2020, after more than 10 years in the automotive and tinting trade. Bring the car to Goldenrod Road, or have us do the same work at your home or office.</p>
      <dl class="facts">
        <div><dt>Shop</dt><dd>{ADDR1}<br>{ADDR2}</dd></div>
        <div><dt>Call or text</dt><dd><a href="{TEL}">{PHONE}</a></dd></div>
        <div><dt>Email</dt><dd class="plain"><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
      </dl>
      <div class="btns">{btn('s', MAPS, 'Directions', ' rel="noopener"')}</div>
    </div>
  </div>
  <div class="map rv"><iframe title="Map showing Tintland Orlando on N Goldenrod Rd" loading="lazy" src="https://www.google.com/maps?q={MAPQ}&output=embed"></iframe></div>
</section>"""


END = f"""
<section class="sec end">
  <div class="wrap">
    <h2 class="rv">Tell us your car. We'll send a price.</h2>
    <a class="tel rv" href="{TEL}">{PHONE}</a>
    <div class="btns rv">{btn('p', 'estimate.html', 'Free estimate')}</div>
  </div>
</section>"""

BAND = """
<section class="band">
  <div class="wrap">
    <div><b>XPEL film</b>Prime on cars, Vision on homes and offices</div>
    <div><b>Lifetime warranty</b>Nationwide, and it transfers to the next owner</div>
    <div><b>Computer cut</b>Patterns cut to your exact vehicle</div>
    <div><b>Free estimates</b>By text, by phone or in person</div>
  </div>
</section>"""

# ---------------------------------------------------------------- home
board = "".join(f"""
      <li>
        <div class="nm">{n}<small>{t}</small></div>
        <p class="ds">{d}</p>
        <div class="pr" data-film="{k}">${PRICES['base']['four'][k]}</div>
      </li>""" for k, n, t, d in FILMS)
STRIP = [('supra-red', 'Red Toyota Supra in the Tintland bay', 'Toyota Supra'), ('telluride-black', 'Black Kia Telluride in the Tintland bay', 'Kia Telluride'),
         ('porsche-red', 'Red Porsche convertible in the Tintland bay', 'Porsche'), ('altima-white', 'White Nissan Altima with a tinted rear window', 'Nissan Altima'),
         ('suv-side-glass', 'Side windows of a dark SUV after tint', 'Side glass, after'), ('toyota-blue', 'Blue Toyota sedan with a tinted rear window', 'Toyota')]
strip = "".join(f'<figure>{pic(s, a, "(max-width:700px) 80vw, 46vw")}<figcaption>{c}</figcaption></figure>' for s, a, c in STRIP)
home = f"""
{simhero('Pick your shade.', 'Tap a swatch to tint the glass. XPEL film in Orlando from $190, computer cut, with a lifetime warranty.', btn('s', 'prices.html', 'See prices'))}
{BAND}

<section class="sec">
  <div class="wrap">
    <h2 class="rv">Four films. Every price up front.</h2>
    <div class="seg rv" role="group" aria-label="Vehicle type">
      <button type="button" data-veh="two" aria-pressed="false"><span>2-door</span></button>
      <button type="button" data-veh="four" aria-pressed="true"><span>4-door sedan</span></button>
      <button type="button" data-veh="suv" aria-pressed="false"><span>SUV or pickup</span></button>
    </div>
    <ol class="board rv">{board}
    </ol>
    <p class="sec-foot rv"><a class="tlink" href="prices.html">Add a windshield and send us the total</a></p>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap strip-head">
    <h2 class="rv">Fresh out of the bay.</h2>
    <div class="strip-nav rv">
      <button class="btn btn-s" type="button" data-strip="-1" aria-label="Previous photos"><span>Prev</span></button>
      <button class="btn btn-s" type="button" data-strip="1" aria-label="Next photos"><span>Next</span></button>
    </div>
  </div>
  <div class="strip rv" tabindex="0" aria-label="Photos of cars tinted at Tintland">{strip}</div>
  <div class="wrap"><p class="sec-foot"><a class="tlink" href="gallery.html">Open the gallery</a></p></div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <h2 class="rv">How a job goes.</h2>
    <div class="proc rv">
      <div><b>Send</b><p>Text or WhatsApp the year, make and model. We reply with a price. For a home or office, we come out and measure for free.</p></div>
      <div><b>Cut</b><p>A computer cuts each piece to the pattern for your exact vehicle, so each piece matches your glass.</p></div>
      <div><b>Install</b><p>Bring the car to the shop on Goldenrod Road, or have us do the same work at your home or office.</p></div>
    </div>
  </div>
</section>
{visit()}
{END}"""
page("index.html", "Tintland Orlando | Window Tinting for Cars, Homes and Offices",
     "XPEL window tint in Orlando from $190. Computer cut, lifetime transferable warranty, free estimates. At our Goldenrod Rd shop or at your home.", home, PRICE_JS)

# ---------------------------------------------------------------- simulator
simp = f"""
{simhero('Tint simulator.', 'Tap a swatch to see each shade on a car, and check it against Florida law as you go.', btn('s', '#law', 'Florida limits'))}

<section class="sec" id="law">
  <div class="wrap">
    <h2 class="rv">Florida tint law in four lines.</h2>
    <p class="lead rv">The number is the share of visible light that gets through the glass and film together. A lower number is darker.</p>
    <div class="tbl-wrap rv">
      <table>
        <thead><tr><th scope="col">Glass</th><th scope="col" class="n">Sedans and coupes</th><th scope="col" class="n">SUVs, vans, other multipurpose vehicles</th></tr></thead>
        <tbody>
          <tr><th scope="row">Front doors</th><td class="n">28% or lighter</td><td class="n">28% or lighter</td></tr>
          <tr><th scope="row">Back doors</th><td class="n">15% or lighter</td><td class="n">6% or lighter</td></tr>
          <tr><th scope="row">Rear window</th><td class="n">15% or lighter</td><td class="n">6% or lighter</td></tr>
          <tr><th scope="row">Windshield</th><td class="n">Above the AS-1 line</td><td class="n">Above the AS-1 line</td></tr>
        </tbody>
      </table>
    </div>
    <p class="sec-foot mute small rv">Factory glass carries some tint of its own, and the law counts glass and film together. The back glass on the SUV above is factory privacy glass, so it starts darker than the front. This is a summary, not legal advice. Florida Statutes 316.2951 to 316.2957 hold the full rules, and the state grants medical exemptions for darker tint.</p>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <h2 class="rv">Shade and film are two choices.</h2>
    <div class="rows rv">
      <div><b>Shade</b><span>How dark the glass looks. That is what the swatches show.</span></div>
      <div><b>Film</b><span>How much heat the glass keeps out. A light ceramic film can reject more heat than a dark dyed one.</span></div>
      <div><b>Price</b><span>Set by the film and the size of your vehicle. <a class="ilink" href="prices.html">See prices</a></span></div>
    </div>
  </div>
</section>
{END}"""
page("tint-simulator.html", "Tint Simulator | Tintland Orlando",
     "See 70%, 50%, 35%, 20%, 15% and 5% window tint on a car and check each shade against Florida tint law.", simp)

# ---------------------------------------------------------------- prices
film_opts = "".join(f'<label class="opt"><input type="radio" name="film" value="{k}"{" checked" if k == "xr" else ""}><span><b>{n}</b><small>{t}</small></span></label>' for k, n, t, d in FILMS)
film_rows = "".join(f"<div><b>{n}</b><span>{d}</span></div>" for k, n, t, d in FILMS)
prices = f"""
<section class="phead">
  <div class="wrap">
    <h1>Build your price.</h1>
    <p class="lead">Pick your vehicle and film. The total updates as you go, and one tap sends it to us.</p>
  </div>
</section>
<section class="sec" id="price" style="padding-top:24px">
  <div class="wrap builder">
    <form id="price-form">
      <fieldset>
        <legend>Your vehicle</legend>
        <p class="hint">Prices are per vehicle.</p>
        <div class="opts c3">
          <label class="opt"><input type="radio" name="vehicle" value="two"><span><b>2-door</b><small>Coupes and convertibles</small></span></label>
          <label class="opt"><input type="radio" name="vehicle" value="four" checked><span><b>4-door sedan</b><small>Four doors and a trunk</small></span></label>
          <label class="opt"><input type="radio" name="vehicle" value="suv"><span><b>SUV or pickup</b><small>Trucks included</small></span></label>
        </div>
      </fieldset>
      <fieldset>
        <legend>Your film</legend>
        <p class="hint">All four are XPEL Prime films with a lifetime warranty.</p>
        <div class="opts c4">{film_opts}</div>
      </fieldset>
      <fieldset>
        <legend>Windshield</legend>
        <p class="hint">Full windshields come in ceramic film only. Florida allows tint below the AS-1 line only with a medical exemption.</p>
        <div class="opts c4">
          <label class="opt"><input type="radio" name="windshield" value="none" checked><span><b>None</b><small>Leave it as is</small></span></label>
          <label class="opt"><input type="radio" name="windshield" value="visor"><span><b>Visor strip</b><small>In the film you picked</small></span></label>
          <label class="opt"><input type="radio" name="windshield" value="xr"><span><b>Full, XR</b><small>$180</small></span></label>
          <label class="opt"><input type="radio" name="windshield" value="xrp"><span><b>Full, XR Plus</b><small>$220</small></span></label>
        </div>
      </fieldset>
    </form>
    <aside class="quote" aria-live="polite">
      <div class="cap">Your total</div>
      <div class="tot" id="q-total">$320</div>
      <ul id="q-lines"><li><span>4-door sedan, Prime XR ceramic</span><b>$320</b></li></ul>
      <div class="acts">
        <button class="btn btn-k" id="q-wa" type="button"><span>Send by WhatsApp</span></button>
        <button class="btn btn-s" id="q-sms" type="button"><span>Send by text</span></button>
        {btn('s', TEL, 'Call ' + PHONE)}
      </div>
      <p class="fine">Tintland confirms your price before the job starts.</p>
    </aside>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap">
    <h2 class="rv">Which film is which.</h2>
    <p class="lead rv">All four come from XPEL's Prime line. The lifetime warranty is good nationwide and transfers to the next owner.</p>
    <div class="rows rv">{film_rows}</div>
    <p class="sec-foot rv"><a class="tlink" href="tint-simulator.html">Not sure how dark to go? Open the simulator</a></p>
  </div>
</section>

<section class="sec" style="padding-top:0">
  <div class="wrap split">
    <div class="rv">{pic('telluride-black', 'Black Kia Telluride in the Tintland bay')}</div>
    <div class="rv">
      <h2>Homes and offices.</h2>
      <p>We install XPEL Vision film on house and office windows. The film is priced by the square foot, and the labor depends on the type and condition of each window.</p>
      <p>Send us the address and we'll come out, measure and give you a free estimate in person.</p>
      <div class="btns" style="margin-top:30px">{btn('p', 'estimate.html', 'Free estimate')}</div>
    </div>
  </div>
</section>
{END}"""
page("prices.html", "Window Tint Prices | Tintland Orlando",
     "Tintland Orlando tint prices: XPEL Prime CS from $190, HP from $240, XR ceramic from $300, XR Plus from $500. Build your total and send it in one tap.",
     prices, PRICE_JS)

# ---------------------------------------------------------------- gallery
G = [('supra-red', 'Red Toyota Supra in the Tintland bay'), ('shop-front', 'Yellow Lamborghini outside the Tintland shop'),
     ('telluride-black', 'Black Kia Telluride in the Tintland bay'), ('porsche-red', 'Red Porsche convertible in the Tintland bay'),
     ('altima-white', 'White Nissan Altima with a tinted rear window'), ('suv-side-glass', 'Side windows of a dark SUV after tint'),
     ('toyota-blue', 'Blue Toyota sedan with a tinted rear window'), ('honda-rear-glass', 'Rear window of a Honda after tint'),
     ('convertible-red', 'Red convertible with a tinted rear window'), ('rear-glass-red-coupe', 'Rear window of a red coupe after tint')]
gal = "".join(f'<a href="assets/img/{s}.webp">{pic(s, a, "(max-width:480px) 100vw, (max-width:860px) 50vw, 33vw", eager=i < 3)}</a>' for i, (s, a) in enumerate(G))
gallery = f"""
<section class="phead">
  <div class="wrap">
    <h1>Fresh out of the bay.</h1>
    <p class="lead">Cars tinted at our shop on Goldenrod Road. Tap a photo to see it larger.</p>
  </div>
</section>
<section class="sec" style="padding-top:24px">
  <div class="wrap"><div class="gal">{gal}</div></div>
</section>
<dialog id="lightbox" aria-label="Photo">
  <form method="dialog"><button class="btn btn-s"><span>Close</span></button></form>
  <img src="" alt="">
</dialog>
{END}"""
page("gallery.html", "Gallery | Tintland Orlando", "Photos of cars tinted with XPEL film at Tintland Orlando.", gallery)

# ---------------------------------------------------------------- about
about = f"""
<section class="phead">
  <div class="wrap split">
    <div>
      <h1>Service you can trust.</h1>
      <p>John Uzcategui started Tintland Window Tinting LLC in 2020. He brought more than 10 years in the automotive and tinting trade with him.</p>
      <p>We set out to be the best choice for window tint in the Orlando area, and we want every customer to leave with more than they expected.</p>
    </div>
    <div>{pic('porsche-red', 'Red Porsche convertible in the Tintland bay', eager=True)}</div>
  </div>
</section>
{BAND}
<section class="sec">
  <div class="wrap">
    <h2 class="rv">What comes with every job.</h2>
    <div class="rows rv">
      <div><b>Installers</b><span>Technicians who tint for a living, on everything from daily drivers to exotics.</span></div>
      <div><b>Film</b><span>XPEL Prime on cars and XPEL Vision on buildings, cut by computer to fit.</span></div>
      <div><b>Warranty</b><span>Lifetime, good nationwide, and it transfers to the next owner if you sell the car.</span></div>
      <div><b>Estimate</b><span>Free. By text or WhatsApp for cars, in person for homes and offices.</span></div>
      <div><b>Where</b><span>The same work at our shop, at your home or at your office.</span></div>
    </div>
  </div>
</section>
{visit('Come by the shop.')}
{END}"""
page("about.html", "About | Tintland Orlando",
     "Tintland Window Tinting LLC opened in Orlando in 2020. Founder John Uzcategui has more than 10 years in the automotive and tinting trade.", about)

# ---------------------------------------------------------------- estimate
film_select = "".join(f"<option>{n}</option>" for k, n, t, d in FILMS)
est = f"""
<section class="phead">
  <div class="wrap">
    <h1>Free estimate.</h1>
    <p class="lead">Fill this in and send it by WhatsApp or text. We answer with a price for cars, or a time to come measure your home or office.</p>
  </div>
</section>
<section class="sec" style="padding-top:24px">
  <div class="wrap builder">
    <form id="est-form" novalidate>
      <fieldset>
        <legend>What are we tinting?</legend>
        <div class="opts c3" style="margin-top:14px">
          <label class="opt"><input type="radio" name="kind" value="Car" checked><span><b>Car</b><small>Any vehicle</small></span></label>
          <label class="opt"><input type="radio" name="kind" value="Home"><span><b>Home</b><small>Free visit to measure</small></span></label>
          <label class="opt"><input type="radio" name="kind" value="Office"><span><b>Office</b><small>Free visit to measure</small></span></label>
        </div>
      </fieldset>
      <div class="field"><label for="f-name">Your name</label><input id="f-name" name="name" autocomplete="name"></div>
      <div id="est-car">
        <div class="grid3">
          <div class="field"><label for="f-year">Year</label><input id="f-year" name="year" inputmode="numeric" maxlength="4"></div>
          <div class="field"><label for="f-make">Make</label><input id="f-make" name="make"></div>
          <div class="field"><label for="f-model">Model</label><input id="f-model" name="model"></div>
        </div>
        <div class="field"><label for="f-film">Film you're leaning toward</label>
          <select id="f-film" name="film"><option value="">Not sure yet</option>{film_select}</select></div>
      </div>
      <div id="est-place" hidden>
        <div class="field"><label for="f-addr">Address of the property</label><input id="f-addr" name="address" autocomplete="street-address">
          <p class="help">We use it to schedule the free in-person estimate.</p></div>
      </div>
      <div class="field"><label for="f-notes">Anything else we should know?</label><textarea id="f-notes" name="notes"></textarea></div>
      <p class="err" id="est-err" role="alert"></p>
    </form>
    <aside class="quote">
      <div class="big">Send it your way.</div>
      <p style="font-weight:600">Your message opens ready to go. Nothing leaves your phone until you press send.</p>
      <div class="acts">
        <button class="btn btn-k" id="est-wa" type="button"><span>Send by WhatsApp</span></button>
        <button class="btn btn-s" id="est-sms" type="button"><span>Send by text</span></button>
        {btn('s', TEL, 'Call ' + PHONE)}
      </div>
      <p class="fine">Prefer email? Write to <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </aside>
  </div>
</section>
{visit('Or come by the shop.')}"""
page("estimate.html", "Free Estimate | Tintland Orlando",
     "Get a free window tint estimate from Tintland Orlando by WhatsApp, text or phone. Cars, homes and offices.", est)

(ROOT / ".nojekyll").write_text("", encoding="utf-8")
