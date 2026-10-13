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
VER = hashlib.md5((ROOT / "assets/site.css").read_bytes() + (ROOT / "assets/site.js").read_bytes()).hexdigest()[:8]

PRICES = dict(
    base=dict(two=dict(cs=190, hp=240, xr=300, xrp=500), four=dict(cs=200, hp=250, xr=320, xrp=520),
              suv=dict(cs=220, hp=260, xr=340, xrp=540)),
    windshield=dict(xr=180, xrp=220), visor=dict(cs=30, hp=40, xr=50, xrp=80),
)


def icon(name):
    svg = (Path(__file__).parent / f"{name}.svg").read_text(encoding="utf-8")
    path = svg[svg.index("<path"):svg.index("</svg>")]
    return f'<svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor" aria-hidden="true">{path}</svg>'


SOCIAL = "".join(f'<a href="{u}" rel="noopener" aria-label="Tintland Orlando on {n}">{icon(n.lower())}</a>' for n, u in [
    ("Instagram", "https://www.instagram.com/tintlandorlando/"), ("Facebook", "https://www.facebook.com/tintlandorlando")])


def pic(slug, alt, sizes="(max-width:860px) 100vw, 50vw", eager=False):
    w, h = Image.open(IMG / f"{slug}.webp").size
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img src="assets/img/{slug}-800.webp" srcset="assets/img/{slug}-800.webp 800w, assets/img/{slug}.webp {w}w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{alt}" {load}>')


NAV = [("tint-simulator.html", "Tint simulator"), ("prices.html", "Prices"), ("gallery.html", "Gallery"), ("about.html", "About")]


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
<meta name="theme-color" content="#f5f6f8">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="assets/img/og.jpg">
<meta property="og:type" content="website">
<link rel="preload" href="assets/fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/figtree.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/site.css?v={VER}">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="hdr">
  <div class="wrap">
    <a class="brand" href="index.html" aria-label="Tintland Orlando, home"><img src="assets/img/tintland-logo.png" width="211" height="62" alt="Tintland Orlando"></a>
    <button class="menu" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
    <nav class="nav" id="nav" aria-label="Main">{nav}<a class="btn btn-p" href="estimate.html">Free estimate</a></nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="ftr">
  <div class="wrap">
    <div class="ftr-grid">
      <div>
        <span class="logo"><img src="assets/img/tintland-logo.png" width="640" height="188" alt="Tintland Orlando" loading="lazy"></span>
        <p>Tintland Window Tinting LLC. XPEL window film for cars, homes and offices in Orlando since 2020.</p>
        <div class="social">{SOCIAL}</div>
      </div>
      <div>
        <h3>Visit or call</h3>
        <ul>
          <li>{ADDR1}<br>{ADDR2}</li>
          <li><a href="{TEL}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        </ul>
      </div>
      <div>
        <h3>Site</h3>
        <ul>
          <li><a href="tint-simulator.html">Tint simulator</a></li>
          <li><a href="prices.html">Prices</a></li>
          <li><a href="gallery.html">Gallery</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="estimate.html">Free estimate</a></li>
        </ul>
      </div>
    </div>
    <div class="note">
      <span>Tintland confirms your price before the job starts.</span>
      <span>Concept redesign by <a href="https://madebyawad.com" rel="noopener">Made by Awad</a>. Not the official Tintland site.</span>
    </div>
  </div>
</footer>
<div class="bar">
  <a class="btn btn-s" href="{TEL}">Call</a>
  <a class="btn btn-p" href="estimate.html">Free estimate</a>
</div>
{scripts}<script src="assets/site.js?v={VER}" defer></script>
</body>
</html>
"""
    assert "—" not in html and "–" not in html, f"dash in {fname}"
    (ROOT / fname).write_text(html, encoding="utf-8", newline="\n")
    print("built", fname)


def sim():
    cw, ch = Image.open(IMG / "sim-car.webp").size
    ticks = "".join(f'<button type="button" aria-pressed="false">{t}</button>' for t in ["None", "70%", "50%", "35%", "20%", "15%", "5%"])
    return f"""
    <div class="sim">
      <div class="stage">
        <img src="assets/img/sim-car-900.webp" srcset="assets/img/sim-car-900.webp 900w, assets/img/sim-car.webp {cw}w" sizes="(max-width:1100px) 92vw, 1000px" width="{cw}" height="{ch}" alt="White SUV seen from the side">
        <img class="tint" src="assets/img/sim-tint-900.webp" srcset="assets/img/sim-tint-900.webp 900w, assets/img/sim-tint.webp {cw}w" sizes="(max-width:1100px) 92vw, 1000px" width="{cw}" height="{ch}" alt="" aria-hidden="true">
      </div>
      <div class="sim-ctl">
        <input type="range" min="0" max="6" step="1" value="3" aria-label="Tint level, from no tint to 5 percent">
        <div class="ticks">{ticks}</div>
      </div>
      <div class="sim-row">
        <div><div class="sim-num" aria-live="polite">35%</div><div class="sim-cap">of visible light gets through</div></div>
        <p class="sim-desc">The middle ground. Real privacy, and still easy to see out at night.</p>
      </div>
      <div class="legal">
        <div><span>Front doors</span><b class="ok">Legal in Florida</b></div>
        <div><span>Back windows, sedan or coupe</span><b class="ok">Legal in Florida</b></div>
        <div><span>Back windows, SUV or van</span><b class="ok">Legal in Florida</b></div>
      </div>
      <p class="sim-note">Florida's limits are 28% on front doors, 15% on the back of sedans and coupes, and 6% on the back of SUVs and vans. The law counts the glass and the film together, and factory glass carries some tint of its own. The back glass on this SUV is factory privacy glass, so it starts darker than the front. Your screen is a guide, so see the samples at the shop before you choose. Car photo: <a href="https://commons.wikimedia.org/wiki/File:Audi_Q4_e-tron_2021-1_seitenansicht.jpg" rel="noopener">Sestmedia, CC BY-SA 4.0</a>, edited.</p>
    </div>"""


def price_table():
    rows = [("2-door car", "two"), ("4-door sedan", "four"), ("SUV or pickup truck", "suv")]
    body = "".join(f'<tr><th scope="row">{n}</th>' + "".join(f'<td class="n">${PRICES["base"][k][f]}</td>' for f in ("cs", "hp", "xr", "xrp")) + "</tr>" for n, k in rows)
    return f"""<div class="tbl-wrap"><table>
      <thead><tr><th scope="col">Vehicle</th><th scope="col" class="n">Prime CS</th><th scope="col" class="n">Prime HP</th><th scope="col" class="n">Prime XR</th><th scope="col" class="n">Prime XR Plus</th></tr></thead>
      <tbody>{body}</tbody></table></div>"""


def visit(h="Come by the shop"):
    return f"""
<section class="sec white" id="visit">
  <div class="wrap visit">
    <div>
      <h2>{h}</h2>
      <dl>
        <div><dt>Address</dt><dd>{ADDR1}<br>{ADDR2}</dd></div>
        <div><dt>Call or text</dt><dd><a href="{TEL}">{PHONE}</a></dd></div>
        <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
      </dl>
      <div class="btns">
        <a class="btn btn-p" href="estimate.html">Free estimate</a>
        <a class="btn btn-s" href="https://www.google.com/maps/search/?api=1&query={MAPQ}" rel="noopener">Directions</a>
      </div>
    </div>
    <iframe title="Map showing Tintland Orlando on N Goldenrod Rd" loading="lazy" src="https://www.google.com/maps?q={MAPQ}&output=embed"></iframe>
  </div>
</section>"""


END = f"""
<section class="sec end">
  <div class="wrap">
    <h2>Tell us your car. We'll send you a price.</h2>
    <div class="btns">
      <a class="btn btn-p" href="estimate.html">Free estimate</a>
      <a class="btn btn-s" href="{TEL}">Call {PHONE}</a>
    </div>
  </div>
</section>"""

# ---------------------------------------------------------------- home
home = f"""
<section class="hero">
  <div class="wrap">
    <div>
      <h1>Orlando window tint, at our shop or your home.</h1>
      <p>XPEL film, cut by computer, with a lifetime warranty that transfers with the car. Prices start at $190.</p>
      <div class="btns">
        <a class="btn btn-p" href="estimate.html">Free estimate</a>
        <a class="btn btn-s" href="#tint">Try the tint simulator</a>
      </div>
    </div>
    <div class="hero-img">{pic('shop-front', 'Yellow Lamborghini parked outside the Tintland Orlando shop', '(max-width:860px) 100vw, 40vw', eager=True)}</div>
  </div>
</section>

<section class="sec white" id="tint">
  <div class="wrap">
    <h2>See the shade before you pick it.</h2>
    <p class="lead">Drag the slider from clear glass to limo tint. The panel under the car tells you which windows that shade is legal on in Florida.</p>
    {sim()}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="facts rv">
      <div><b>XPEL film</b>Prime for cars, Vision for homes and offices</div>
      <div><b>Lifetime warranty</b>Nationwide, and it transfers to the next owner</div>
      <div><b>Computer cut</b>Patterns cut to your exact vehicle</div>
      <div><b>Free estimates</b>By text, by phone or in person</div>
    </div>
    <h2 class="rv" style="margin-top:clamp(56px,8vw,96px)">Four films. Every price up front.</h2>
    <p class="lead rv">Prices are per vehicle. Pick the film by how much heat you want to keep out.</p>
    <div class="rv">{price_table()}</div>
    <p class="sec-foot rv"><a class="tlink" href="prices.html">Build your price, with windshield options</a></p>
  </div>
</section>

<section class="sec white">
  <div class="wrap">
    <h2 class="rv">Fresh out of our bay.</h2>
    <div class="mosaic rv">
      <a href="gallery.html">{pic('supra-red', 'Red Toyota Supra in the Tintland bay', '(max-width:700px) 100vw, 66vw')}</a>
      <a href="gallery.html">{pic('telluride-black', 'Black Kia Telluride in the Tintland bay', '(max-width:700px) 50vw, 33vw')}</a>
      <a href="gallery.html">{pic('porsche-red', 'Red Porsche convertible in the Tintland bay', '(max-width:700px) 50vw, 33vw')}</a>
    </div>
    <p class="sec-foot rv"><a class="tlink" href="gallery.html">See the gallery</a></p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <h2 class="rv">How a job goes</h2>
    <div class="steps rv">
      <div><h3>Send us your car</h3><p>Text or WhatsApp the year, make and model. We reply with a price. For a home or office, we come out and measure for free.</p></div>
      <div><h3>We cut the film</h3><p>A computer cuts each piece to the pattern for your exact vehicle, so each piece matches your glass.</p></div>
      <div><h3>We install it</h3><p>Bring the car to the shop on Goldenrod Road, or have us do the same work at your home or office.</p></div>
    </div>
  </div>
</section>

<section class="sec white">
  <div class="wrap split">
    <div class="rv">{pic('suv-side-glass', 'Side windows of a dark SUV after tint at Tintland')}</div>
    <div class="stack rv">
      <h2>Run by a tinter, since 2020.</h2>
      <p class="mute">John Uzcategui opened Tintland Window Tinting in 2020, after more than 10 years in the automotive and tinting trade. The goal is simple: be the best choice for window tint in the Orlando area.</p>
      <p><a class="tlink" href="about.html">About Tintland</a></p>
    </div>
  </div>
</section>
{visit().replace('class="sec white"', 'class="sec"')}
{END}"""
page("index.html", "Tintland Orlando | Window Tinting for Cars, Homes and Offices",
     "XPEL window tint in Orlando from $190. Computer cut, lifetime transferable warranty, free estimates. At our Goldenrod Rd shop or at your home.", home)

# ---------------------------------------------------------------- simulator
simp = f"""
<section class="phead">
  <div class="wrap">
    <h1>Tint simulator</h1>
    <p class="lead">Drag the slider to see each shade on a car, and check it against Florida law as you go.</p>
  </div>
</section>
<section class="sec tight">
  <div class="wrap">
    <div style="margin-top:-36px">{sim()}</div>
  </div>
</section>

<section class="sec white">
  <div class="wrap">
    <h2 class="rv">Florida tint law, in four lines</h2>
    <p class="lead rv">The number is the share of visible light that gets through the glass and film together. A lower number is darker.</p>
    <div class="tbl-wrap rv">
      <table>
        <thead><tr><th scope="col">Glass</th><th scope="col" class="n">Sedans and coupes</th><th scope="col" class="n">SUVs, vans and other multipurpose vehicles</th></tr></thead>
        <tbody>
          <tr><th scope="row">Front doors</th><td class="n">28% or lighter</td><td class="n">28% or lighter</td></tr>
          <tr><th scope="row">Back doors</th><td class="n">15% or lighter</td><td class="n">6% or lighter</td></tr>
          <tr><th scope="row">Rear window</th><td class="n">15% or lighter</td><td class="n">6% or lighter</td></tr>
          <tr><th scope="row">Windshield</th><td class="n">Above the AS-1 line only</td><td class="n">Above the AS-1 line only</td></tr>
        </tbody>
      </table>
    </div>
    <p class="sec-foot mute small rv">This is a summary, not legal advice. Florida Statutes 316.2951 to 316.2957 hold the full rules, and the state grants medical exemptions for darker tint.</p>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <h2 class="rv">Shade and film are two choices</h2>
    <div class="rows rv">
      <div><b>Shade</b><span>How dark the glass looks. That is what the slider shows.</span></div>
      <div><b>Film</b><span>How much heat the glass keeps out. A light ceramic film can reject more heat than a dark dyed one.</span></div>
      <div><b>Price</b><span>Set by the film and the size of your vehicle. <a class="tlink" href="prices.html">See prices</a></span></div>
    </div>
  </div>
</section>
{END}"""
page("tint-simulator.html", "Tint Simulator | Tintland Orlando",
     "See 70%, 50%, 35%, 20%, 15% and 5% window tint on a car and check each shade against Florida tint law.", simp)

# ---------------------------------------------------------------- prices
prices = f"""
<section class="phead">
  <div class="wrap">
    <h1>Window tint prices</h1>
    <p class="lead">Pick your vehicle and film. The total updates as you go, and one tap sends it to us.</p>
  </div>
</section>
<section class="sec tight" id="price">
  <div class="wrap builder">
    <form id="price-form">
      <fieldset>
        <legend>Your vehicle</legend>
        <p class="hint">Prices are per vehicle.</p>
        <div class="opts c3">
          <label class="opt"><input type="radio" name="vehicle" value="two"><span><b>2-door car</b><small>Coupes and convertibles</small></span></label>
          <label class="opt"><input type="radio" name="vehicle" value="four" checked><span><b>4-door sedan</b><small>Four doors and a trunk</small></span></label>
          <label class="opt"><input type="radio" name="vehicle" value="suv"><span><b>SUV or pickup</b><small>Trucks included</small></span></label>
        </div>
      </fieldset>
      <fieldset>
        <legend>Your film</legend>
        <p class="hint">All four are XPEL Prime films with a lifetime warranty.</p>
        <div class="opts c4">
          <label class="opt"><input type="radio" name="film" value="cs"><span><b>Prime CS</b><small>Dyed film</small></span></label>
          <label class="opt"><input type="radio" name="film" value="hp"><span><b>Prime HP</b><small>Metalized film</small></span></label>
          <label class="opt"><input type="radio" name="film" value="xr" checked><span><b>Prime XR</b><small>Ceramic film</small></span></label>
          <label class="opt"><input type="radio" name="film" value="xrp"><span><b>Prime XR Plus</b><small>Top ceramic film</small></span></label>
        </div>
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
      <button class="btn btn-p" id="q-wa" type="button">Send by WhatsApp</button>
      <button class="btn btn-s" id="q-sms" type="button">Send by text</button>
      <a class="btn btn-s" href="{TEL}">Call {PHONE}</a>
      <p class="fine">Tintland confirms your price before the job starts.</p>
    </aside>
  </div>
</section>

<section class="sec white">
  <div class="wrap">
    <h2 class="rv">The full list</h2>
    <div class="rv">{price_table()}</div>
    <div class="tbl-wrap rv">
      <table>
        <thead><tr><th scope="col">Windshield</th><th scope="col" class="n">Prime CS</th><th scope="col" class="n">Prime HP</th><th scope="col" class="n">Prime XR</th><th scope="col" class="n">Prime XR Plus</th></tr></thead>
        <tbody>
          <tr><th scope="row">Visor strip only</th><td class="n">$30</td><td class="n">$40</td><td class="n">$50</td><td class="n">$80</td></tr>
          <tr><th scope="row">Full windshield</th><td class="n mute">n/a</td><td class="n mute">n/a</td><td class="n">$180</td><td class="n">$220</td></tr>
        </tbody>
      </table>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <h2 class="rv">Which film is which</h2>
    <p class="lead rv">All four come from XPEL's Prime line and carry a lifetime warranty that is good nationwide and transfers to the next owner.</p>
    <div class="rows rv">
      <div><b>Prime CS</b><span>Color-stable dyed film. The lowest price, for a darker look and UV protection.</span></div>
      <div><b>Prime HP</b><span>Dyed film with a metalized layer, which reflects more of the sun's heat than dyed film alone.</span></div>
      <div><b>Prime XR</b><span>Ceramic film. It rejects heat without metal, so it doesn't get in the way of phone, GPS or radio signals.</span></div>
      <div><b>Prime XR Plus</b><span>XPEL's top ceramic film for heat. The one to pick if your car sits in a Florida parking lot all day.</span></div>
    </div>
    <p class="sec-foot rv"><a class="tlink" href="tint-simulator.html">Not sure how dark to go? Try the tint simulator</a></p>
  </div>
</section>

<section class="sec white">
  <div class="wrap split">
    <div class="stack rv">
      <h2>Homes and offices</h2>
      <p class="mute">We install XPEL Vision film on house and office windows. The film is priced by the square foot, and the labor depends on the type and condition of each window.</p>
      <p class="mute">Send us the address and we'll come out, measure and give you a free estimate in person.</p>
      <div class="btns"><a class="btn btn-p" href="estimate.html">Free estimate</a></div>
    </div>
    <div class="rv">{pic('shop-front', 'The Tintland Orlando shop front with a yellow Lamborghini outside')}</div>
  </div>
</section>
{END}"""
page("prices.html", "Window Tint Prices | Tintland Orlando",
     "Tintland Orlando tint prices: XPEL Prime CS from $190, HP from $240, XR ceramic from $300, XR Plus from $500. Build your total and send it in one tap.",
     prices, f"<script>window.TL_PRICES={json.dumps(PRICES)};</script>\n")

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
    <h1>Gallery</h1>
    <p class="lead">Cars tinted at our shop on Goldenrod Road. Tap a photo to see it larger.</p>
  </div>
</section>
<section class="sec tight">
  <div class="wrap"><div class="gal">{gal}</div></div>
</section>
<dialog id="lightbox" aria-label="Photo">
  <form method="dialog"><button class="btn btn-s">Close</button></form>
  <img src="" alt="">
</dialog>
{END}"""
page("gallery.html", "Gallery | Tintland Orlando", "Photos of cars tinted with XPEL film at Tintland Orlando.", gallery)

# ---------------------------------------------------------------- about
about = f"""
<section class="phead">
  <div class="wrap">
    <h1>Service you can trust</h1>
    <p class="lead">We want every customer to leave with more than they expected.</p>
  </div>
</section>
<section class="sec tight">
  <div class="wrap split">
    <div>{pic('porsche-red', 'Red Porsche convertible in the Tintland bay', eager=True)}</div>
    <div class="stack">
      <h2>Opened in 2020 by John Uzcategui</h2>
      <p class="mute">John started Tintland Window Tinting LLC in 2020. He brought more than 10 years in the automotive and tinting trade with him.</p>
      <p class="mute">We set out to be the best choice for window tint in the Orlando area. You get the same work wherever you need it: at our shop, at your home or at your office.</p>
    </div>
  </div>
</section>
<section class="sec white">
  <div class="wrap">
    <h2 class="rv">What you get with every job</h2>
    <div class="rows rv">
      <div><b>Experienced installers</b><span>Technicians who tint for a living, on everything from daily drivers to exotics.</span></div>
      <div><b>XPEL film</b><span>Prime film on cars and Vision film on buildings, cut by computer to fit.</span></div>
      <div><b>A lifetime warranty</b><span>Good nationwide, and it transfers to the next owner if you sell the car.</span></div>
      <div><b>A free estimate</b><span>By text or WhatsApp for cars. In person for homes and offices.</span></div>
    </div>
  </div>
</section>
{visit().replace('class="sec white"', 'class="sec"')}
{END}"""
page("about.html", "About | Tintland Orlando",
     "Tintland Window Tinting LLC opened in Orlando in 2020. Founder John Uzcategui has more than 10 years in the automotive and tinting trade.", about)

# ---------------------------------------------------------------- estimate
est = f"""
<section class="phead">
  <div class="wrap">
    <h1>Free estimate</h1>
    <p class="lead">Fill this in and send it by WhatsApp or text. We answer with a price for cars, or a time to come measure your home or office.</p>
  </div>
</section>
<section class="sec tight">
  <div class="wrap builder">
    <form id="est-form" novalidate>
      <fieldset>
        <legend>What are we tinting?</legend>
        <div class="opts c3" style="margin-top:10px">
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
          <select id="f-film" name="film"><option value="">Not sure yet</option><option>Prime CS</option><option>Prime HP</option><option>Prime XR ceramic</option><option>Prime XR Plus ceramic</option></select></div>
      </div>
      <div id="est-place" hidden>
        <div class="field"><label for="f-addr">Address of the property</label><input id="f-addr" name="address" autocomplete="street-address">
          <p class="help">We use it to schedule the free in-person estimate.</p></div>
      </div>
      <div class="field"><label for="f-notes">Anything else we should know?</label><textarea id="f-notes" name="notes"></textarea></div>
      <p class="err" id="est-err" role="alert"></p>
    </form>
    <aside class="quote">
      <div class="cap">Send your request</div>
      <p style="margin:10px 0 18px;font-size:1.05rem">Your message opens ready to send. Nothing goes out until you press send.</p>
      <button class="btn btn-p" id="est-wa" type="button">Send by WhatsApp</button>
      <button class="btn btn-s" id="est-sms" type="button">Send by text</button>
      <a class="btn btn-s" href="{TEL}">Call {PHONE}</a>
      <p class="fine">Prefer email? Write to <a href="mailto:{EMAIL}" style="color:#fff">{EMAIL}</a>.</p>
    </aside>
  </div>
</section>
{visit("Or come by the shop")}"""
page("estimate.html", "Free Estimate | Tintland Orlando",
     "Get a free window tint estimate from Tintland Orlando by WhatsApp, text or phone. Cars, homes and offices.", est)

(ROOT / ".nojekyll").write_text("", encoding="utf-8")
