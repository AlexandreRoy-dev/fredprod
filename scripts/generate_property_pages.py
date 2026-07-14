#!/usr/bin/env python3
"""Generate proprietes.html + SEO detail pages from data/properties.json."""

from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://fredroy.ca"
CENTRIS_AGENT_URL = (
    "https://www.centris.ca/fr/courtier-immobilier~frederic-roy~proprio-direct/j2971"
)
PROPRIO_AGENT_URL = "https://propriodirect.com/frederic-roy"


def load_registry() -> dict:
    return json.loads((ROOT / "data" / "properties.json").read_text(encoding="utf-8"))


def public_path(listing: dict) -> str:
    return listing.get("publicPath") or (
        f"/{listing['country']}/{listing['province']}/{listing['city']}/"
        f"{listing['sector']}/{listing['street']}/"
    )


def asset_prefix(depth: int) -> str:
    return "../" * depth if depth else ""


def _nav_link_class(active: str, key: str) -> str:
    if key == active:
        return "text-fred-gold transition-colors"
    return "hover:text-fred-gold transition-colors"


def site_chrome(active: str, depth: int = 0) -> tuple[str, str]:
    p = asset_prefix(depth)
    nav_cls = {
        "apropos": _nav_link_class(active, "apropos"),
        "proprietes": _nav_link_class(active, "proprietes"),
        "services": _nav_link_class(active, "services"),
        "temoignages": _nav_link_class(active, "temoignages"),
        "contact": _nav_link_class(active, "contact"),
    }

    header = f"""<nav class="bg-fred-blue sticky top-0 z-50 transition-all duration-300 shadow-md">
    <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <a href="{p}index.html" class="flex flex-col group drop-shadow-md w-max">
            <img src="{p}public/LOGO_FRED_ROY_blanc_gold.png" alt="Fred Roy" class="h-12 w-auto object-contain" />
            <span class="h-[2px] w-8 bg-fred-gold mt-2 group-hover:w-full transition-all duration-500 ease-out"></span>
        </a>

        <ul class="hidden md:flex items-center gap-12 text-white text-xs tracking-luxury font-semibold uppercase drop-shadow-md">
            <li><a href="{p}index.html#apropos" class="{nav_cls['apropos']}">À Propos</a></li>
            <li><a href="{p}proprietes.html" class="{nav_cls['proprietes']}">Propriétés</a></li>
            <li><a href="{p}index.html#services" class="{nav_cls['services']}">Services</a></li>
            <li><a href="{p}index.html#temoignages" class="{nav_cls['temoignages']}">Témoignages</a></li>
            <li>
                <a href="{p}index.html#contact" class="px-6 py-3 border border-white text-white hover:bg-white hover:text-fred-blue transition-all duration-300">
                    Me Contacter
                </a>
            </li>
        </ul>

        <button id="mobile-menu-btn" class="md:hidden text-white p-2 -m-2" type="button" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="mobile-menu">
            <svg id="menu-icon-open" class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 6h16M4 12h16M4 18h16"></path>
            </svg>
            <svg id="menu-icon-close" class="w-8 h-8 hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
        </button>
    </div>

    <div id="mobile-menu" class="md:hidden fixed inset-0 top-0 z-40 bg-fred-blue/98 backdrop-blur-sm pt-24 px-6 pb-8 hidden" aria-hidden="true">
        <ul class="flex flex-col gap-8 text-white text-sm tracking-luxury font-semibold uppercase">
            <li><a href="{p}index.html#apropos" class="block py-2 hover:text-fred-gold transition-colors mobile-menu-link">À Propos</a></li>
            <li><a href="{p}proprietes.html" class="block py-2 hover:text-fred-gold transition-colors mobile-menu-link">Propriétés</a></li>
            <li><a href="{p}index.html#services" class="block py-2 hover:text-fred-gold transition-colors mobile-menu-link">Services</a></li>
            <li><a href="{p}index.html#temoignages" class="block py-2 hover:text-fred-gold transition-colors mobile-menu-link">Témoignages</a></li>
            <li>
                <a href="{p}index.html#contact" class="inline-block px-6 py-3 border border-white text-white hover:bg-white hover:text-fred-blue transition-all duration-300 mobile-menu-link">
                    Me Contacter
                </a>
            </li>
        </ul>
    </div>
</nav>"""

    footer = f"""<footer class="bg-fred-blue text-white py-20">
    <div class="max-w-7xl mx-auto px-6 md:px-12 flex flex-col md:flex-row justify-between items-start gap-12">
        <div>
            <a href="{p}index.html" class="block mb-6 w-max">
                <img src="{p}public/LOGO_FRED_ROY_blanc_gold.png" alt="Fred Roy" class="h-16 w-auto object-contain" />
            </a>
            <p class="text-gray-400 text-sm font-light max-w-xs mb-8">
                Courtier Immobilier Résidentiel. <br>
                L'expertise au service de votre patrimoine.
            </p>
            <img src="{p}public/propriodirect.svg" alt="Proprio Direct" class="h-16 w-auto object-contain brightness-0 invert opacity-70 hover:opacity-100 transition-opacity duration-300" />
        </div>

        <div class="flex gap-8 text-xs uppercase tracking-widest text-gray-400">
            <a href="{p}index.html" class="hover:text-fred-gold transition-colors">Accueil</a>
            <a href="{p}proprietes.html" class="hover:text-fred-gold transition-colors">Propriétés</a>
            <a href="{p}index.html#contact" class="hover:text-fred-gold transition-colors">Contact</a>
        </div>

        <div class="text-xs text-gray-500 font-light">
            &copy; 2026 Fred Roy. Tous droits réservés.<br>
            <a href="{p}confidentialite.html" class="hover:text-white transition-colors">Politique de confidentialité</a><br>
            <span class="mt-2 block">Conception web par <a href="https://roymarketing.ca" target="_blank" rel="noopener noreferrer" class="hover:text-white transition-colors">Roy marketing</a></span>
            <p class="mt-4 text-gray-400">
                <a href="tel:+14388826840" class="hover:text-fred-gold transition-colors">(438) 882-6840</a>
                <span class="mx-2">·</span>
                <a href="mailto:info@fredroy.ca" class="hover:text-fred-gold transition-colors">info@fredroy.ca</a>
            </p>
        </div>
    </div>
</footer>
<script>
    (function() {{
        const btn = document.getElementById('mobile-menu-btn');
        const menu = document.getElementById('mobile-menu');
        const iconOpen = document.getElementById('menu-icon-open');
        const iconClose = document.getElementById('menu-icon-close');
        const links = document.querySelectorAll('.mobile-menu-link');

        function openMenu() {{
            menu.classList.remove('hidden');
            menu.setAttribute('aria-hidden', 'false');
            btn.setAttribute('aria-expanded', 'true');
            btn.setAttribute('aria-label', 'Fermer le menu');
            iconOpen.classList.add('hidden');
            iconClose.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        }}

        function closeMenu() {{
            menu.classList.add('hidden');
            menu.setAttribute('aria-hidden', 'true');
            btn.setAttribute('aria-expanded', 'false');
            btn.setAttribute('aria-label', 'Ouvrir le menu');
            iconOpen.classList.remove('hidden');
            iconClose.classList.add('hidden');
            document.body.style.overflow = '';
        }}

        function toggleMenu() {{
            const isOpen = !menu.classList.contains('hidden');
            if (isOpen) closeMenu(); else openMenu();
        }}

        if (btn && menu) {{
            btn.addEventListener('click', toggleMenu);
            links.forEach(function(link) {{
                link.addEventListener('click', closeMenu);
            }});
        }}
    }})();
</script>
<div id="cookie-banner" class="fixed bottom-0 left-0 right-0 md:bottom-8 md:left-8 md:right-auto md:max-w-sm z-[100] bg-white border-t-4 md:border-t-0 md:border-l-4 border-fred-gold shadow-2xl p-6 transform transition-transform duration-500 translate-y-full md:translate-y-[150%] hidden">
    <h3 class="text-lg font-bold text-fred-blue mb-2">Gestion des cookies</h3>
    <p class="text-sm text-gray-600 font-light leading-relaxed mb-6">
        Nous utilisons des cookies pour améliorer votre expérience sur notre site. En continuant à naviguer, vous acceptez notre <a href="{p}confidentialite.html" class="text-fred-gold hover:underline">politique de confidentialité</a>.
    </p>
    <div class="flex flex-col sm:flex-row gap-3">
        <button id="accept-cookies" class="flex-1 bg-fred-blue text-white py-3 px-4 text-xs font-bold uppercase tracking-wider hover:bg-fred-gold transition-colors duration-300 text-center shadow-md">
            Accepter
        </button>
        <button id="decline-cookies" class="flex-1 bg-fred-gray text-fred-blue py-3 px-4 text-xs font-bold uppercase tracking-wider hover:bg-gray-200 transition-colors duration-300 text-center">
            Refuser
        </button>
    </div>
</div>
<script>
    document.addEventListener("DOMContentLoaded", function() {{
        const banner = document.getElementById('cookie-banner');
        const acceptBtn = document.getElementById('accept-cookies');
        const declineBtn = document.getElementById('decline-cookies');
        if (!banner || !acceptBtn || !declineBtn) return;
        if (!localStorage.getItem('cookieConsent')) {{
            banner.classList.remove('hidden');
            setTimeout(() => {{
                banner.classList.remove('translate-y-full', 'md:translate-y-[150%]');
            }}, 100);
        }}
        function handleConsent(choice) {{
            localStorage.setItem('cookieConsent', choice);
            banner.classList.add('translate-y-full', 'md:translate-y-[150%]');
            setTimeout(() => {{
                banner.classList.add('hidden');
            }}, 500);
        }}
        acceptBtn.addEventListener('click', () => handleConsent('accepted'));
        declineBtn.addEventListener('click', () => handleConsent('declined'));
    }});
</script>"""

    return header, footer


def head_block(
    *,
    title: str,
    description: str,
    canonical: str,
    og_image: str,
    depth: int = 0,
    extra: str = "",
) -> str:
    p = asset_prefix(depth)
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <meta content="width=device-width, initial-scale=1.0" name="viewport">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <link rel="icon" type="image/png" sizes="32x32" href="{p}public/favicon.png">
  <link rel="icon" type="image/png" sizes="16x16" href="{p}public/favicon.png">
  <link rel="apple-touch-icon" sizes="180x180" href="{p}public/favicon.png">
  <link rel="shortcut icon" href="{p}public/favicon.ico">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;800&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          colors: {{
            fred: {{
              blue: '#282e64',
              gold: '#be9018',
              gray: '#F5F7FA',
            }}
          }},
          fontFamily: {{
            sans: ['Montserrat', 'sans-serif'],
          }},
          letterSpacing: {{
            luxury: '0.2em',
          }}
        }}
      }}
    }}
  </script>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
  <link href="{p}assets/css/properties.css" rel="stylesheet">
  <link rel="canonical" href="{escape(canonical)}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:image" content="{escape(og_image)}">
  <meta property="og:image:secure_url" content="{escape(og_image)}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:alt" content="{escape(title)}">
  <meta property="og:url" content="{escape(canonical)}">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="fr_CA">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(title)}">
  <meta name="twitter:description" content="{escape(description)}">
  <meta name="twitter:image" content="{escape(og_image)}">
  <meta name="twitter:image:alt" content="{escape(title)}">
  <style>
    html {{ scroll-behavior: smooth; }}
    ::selection {{ background-color: #be9018; color: white; }}
  </style>
{extra}
</head>"""


def listing_card_html(listing: dict, depth: int = 0) -> str:
    p = asset_prefix(depth)
    href = public_path(listing)
    img = f"{p}assets/img/proprietes/{listing['fallbackImage']}"
    badge = ""
    if listing.get("sold"):
        badge = '<span class="prop-badge sold">Vendu</span>'
    elif listing.get("isNew"):
        badge = '<span class="prop-badge new">Nouveauté</span>'

    meta_bits = []
    if listing.get("beds"):
        meta_bits.append(
            f'<span><i class="bi bi-door-closed"></i> {escape(str(listing["beds"]))} ch.</span>'
        )
    if listing.get("baths"):
        meta_bits.append(
            f'<span><i class="bi bi-droplet"></i> {escape(str(listing["baths"]))} sdb</span>'
        )
    size_value = listing.get("livingArea") or listing.get("size")
    if size_value:
        meta_bits.append(
            f'<span><i class="bi bi-bounding-box"></i> {escape(str(size_value))}</span>'
        )

    is_sold = bool(listing.get("sold"))
    price_html = (
        '<p class="prop-price prop-sold-label">Vendu</p>'
        if is_sold
        else f'<p class="prop-price">{escape(listing.get("price") or "")}</p>'
    )

    return f"""
        <article class="prop-card{" prop-card-sold" if is_sold else ""}">
          <a href="{escape(href)}" class="prop-card-media">
            <img src="{escape(img)}" alt="{escape(listing.get('title') or listing.get('address') or '')}" loading="lazy">
            {badge}
          </a>
          <div class="prop-card-body">
            <span class="prop-subtitle mb-1">{escape(listing.get('propertyType') or 'Propriété')}</span>
            {price_html}
            <h3 class="prop-address">{escape(listing.get('address') or '')}</h3>
            <p class="prop-city">{escape(listing.get('cityLabel') or '')}</p>
            <div class="prop-meta">{''.join(meta_bits)}</div>
            <a href="{escape(href)}" class="prop-cta">Voir la fiche <i class="bi bi-arrow-right ms-1"></i></a>
          </div>
        </article>"""


def generate_listings_page(registry: dict) -> None:
    header, footer = site_chrome("proprietes", depth=0)
    listings = registry.get("listings", [])
    active = [x for x in listings if not x.get("sold")]
    sold = [x for x in listings if x.get("sold")]
    ordered = active + sold

    cards = "\n".join(listing_card_html(item, depth=0) for item in ordered) or (
        '<p class="col-span-full text-center text-gray-500">Aucune propriété à afficher pour le moment.</p>'
    )

    description = (
        "Découvrez les propriétés en vigueur de Fred Roy, courtier immobilier "
        "résidentiel Proprio Direct."
    )
    og_image = f"{BASE_URL}/public/LOGO_FRED_ROY_blanc_gold.png"
    if ordered:
        og_image = (
            f"{BASE_URL}/assets/img/proprietes/{ordered[0]['uls']}/og-share.jpg"
        )

    html = f"""{head_block(
        title="Propriétés - Fred Roy, courtier immobilier",
        description=description,
        canonical=f"{BASE_URL}/proprietes.html",
        og_image=og_image,
        depth=0,
    )}
<body class="antialiased bg-fred-gray text-fred-blue font-sans selection:bg-fred-gold selection:text-white proprietes-page">
{header}
<main>
  <section class="properties-title-section">
    <div class="max-w-7xl mx-auto px-6 md:px-8 text-center">
      <div class="section-title-wrapper">
        <span class="prop-subtitle">Inscriptions</span>
        <h1 class="title-with-lines">Propriétés</h1>
        <p>Découvrez mes inscriptions actuelles et mes propriétés vendues.</p>
      </div>
    </div>
  </section>
  <section class="section properties-grid pt-0 pb-24">
    <div class="max-w-7xl mx-auto px-6 md:px-8">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8">
{cards}
      </div>
      <div class="text-center properties-external-link">
        <a href="{PROPRIO_AGENT_URL}" target="_blank" rel="noopener" class="btn-outline">
          Voir aussi sur Proprio Direct
        </a>
      </div>
    </div>
  </section>
</main>
{footer}
</body>
</html>
"""
    (ROOT / "proprietes.html").write_text(html, encoding="utf-8")
    print("wrote proprietes.html")


def kv_list_html(data: dict | None, empty_message: str = "") -> str:
    if not data:
        return (
            f'<p class="text-gray-500 mb-0">{escape(empty_message)}</p>'
            if empty_message
            else ""
        )
    rows = [
        f"<li><strong>{escape(str(key))}</strong><span>{escape(str(value))}</span></li>"
        for key, value in data.items()
    ]
    return f'<ul class="property-facts">{"".join(rows)}</ul>'


def rooms_table_html(rooms: list | None) -> str:
    if not rooms:
        return ""
    rows = []
    for room in rooms:
        rows.append(
            "<tr>"
            f"<td>{escape(str(room.get('name') or ''))}</td>"
            f"<td>{escape(str(room.get('level') or ''))}</td>"
            f"<td>{escape(str(room.get('dimensions') or ''))}</td>"
            f"<td>{escape(str(room.get('flooring') or ''))}</td>"
            "</tr>"
        )
    return (
        '<div class="property-rooms-table">'
        "<table>"
        "<thead><tr><th>Pièce</th><th>Étage</th><th>Dimensions</th><th>Plancher</th></tr></thead>"
        f"<tbody>{''.join(rows)}</tbody>"
        "</table></div>"
    )


def generate_detail_page(listing: dict) -> None:
    depth = 5  # /ca/qc/city/sector/street/index.html
    header, footer = site_chrome("proprietes", depth=depth)
    p = asset_prefix(depth)
    path = public_path(listing)
    canonical = BASE_URL + path
    og_image = f"{BASE_URL}/assets/img/proprietes/{listing['uls']}/og-share.jpg"
    fallback = f"{p}assets/img/proprietes/{listing['fallbackImage']}"
    description = listing.get("description") or listing.get("shareTitle") or listing.get("title")
    if len(description) > 300:
        description = description[:297].rstrip() + "…"

    badge = ""
    if listing.get("sold"):
        badge = '<span class="prop-badge sold">Vendu</span>'
    elif listing.get("isNew"):
        badge = '<span class="prop-badge new">Nouveauté</span>'

    meta_rows = []
    if listing.get("beds"):
        meta_rows.append(
            f"<li><strong>Chambres</strong><span>{escape(str(listing['beds']))}</span></li>"
        )
    if listing.get("baths"):
        meta_rows.append(
            f"<li><strong>Salles de bain</strong><span>{escape(str(listing['baths']))}</span></li>"
        )
    size_value = listing.get("livingArea") or listing.get("size")
    if size_value:
        meta_rows.append(
            f"<li><strong>Superficie</strong><span>{escape(str(size_value))}</span></li>"
        )
    if listing.get("yearBuilt"):
        meta_rows.append(
            f"<li><strong>Année</strong><span>{escape(str(listing['yearBuilt']))}</span></li>"
        )
    if listing.get("floorLevel"):
        meta_rows.append(
            f"<li><strong>Niveau</strong><span>{escape(str(listing['floorLevel']))}</span></li>"
        )
    if listing.get("condoFees"):
        meta_rows.append(
            f"<li><strong>Frais de condo</strong><span>{escape(str(listing['condoFees']))}</span></li>"
        )
    if listing.get("parking"):
        meta_rows.append(
            f"<li><strong>Stationnement</strong><span>{escape(str(listing['parking']))}</span></li>"
        )
    if listing.get("postalCode"):
        meta_rows.append(
            f"<li><strong>Code postal</strong><span>{escape(str(listing['postalCode']))}</span></li>"
        )
    meta_rows.append(
        f"<li><strong>Inscription</strong><span>{escape(str(listing['uls']))}</span></li>"
    )

    city_label = listing["city"].replace("-", " ").title()
    sector_label = listing["sector"].replace("-", " ").title()
    city_line = escape(listing.get("cityLabel") or "")
    if listing.get("postalCode"):
        city_line += f" · {escape(str(listing['postalCode']))}"

    is_sold = bool(listing.get("sold"))
    price_html = (
        '<p class="prop-price prop-sold-label">Vendu</p>'
        if is_sold
        else f'<p class="prop-price">{escape(listing.get("price") or "")}</p>'
    )
    actions_html = ""
    if is_sold:
        actions_html = f"""
            <div class="property-actions">
              <a class="btn-outline" href="{escape(listing.get('proprioUrl') or '#')}" target="_blank" rel="noopener">Voir sur Proprio Direct</a>
              <a class="btn-outline" href="{escape(listing.get('centrisUrl') or '#')}" target="_blank" rel="noopener">Voir sur Centris</a>
            </div>"""
    else:
        actions_html = f"""
            <div class="property-actions">
              <a class="btn-primary" href="{p}index.html#contact">Demander une visite</a>
              <a class="btn-outline" href="{escape(listing.get('proprioUrl') or '#')}" target="_blank" rel="noopener">Voir sur Proprio Direct</a>
              <a class="btn-outline" href="{escape(listing.get('centrisUrl') or '#')}" target="_blank" rel="noopener">Voir sur Centris</a>
            </div>"""

    highlights_html = ""
    if listing.get("highlights"):
        highlights_html = f"""
          <div class="property-panel">
            <span class="prop-subtitle">Aperçu</span>
            <h2>Points saillants</h2>
            {kv_list_html(listing.get("highlights"))}
          </div>"""

    details_html = ""
    if listing.get("details"):
        details_html = f"""
          <div class="property-panel">
            <span class="prop-subtitle">Caractéristiques</span>
            <h2>Détails de la propriété</h2>
            {kv_list_html(listing.get("details"))}
          </div>"""

    inclusions_html = ""
    if listing.get("inclusions"):
        inclusions_html = f"""
          <div class="property-panel">
            <span class="prop-subtitle">Ce qui est inclus</span>
            <h2>Inclusions</h2>
            <p>{escape(listing.get("inclusions") or "")}</p>
          </div>"""

    exclusions_html = ""
    if listing.get("exclusions"):
        exclusions_html = f"""
          <div class="property-panel">
            <span class="prop-subtitle">Non inclus</span>
            <h2>Exclusions</h2>
            <p>{escape(listing.get("exclusions") or "")}</p>
          </div>"""

    rooms_html = ""
    rooms_table = rooms_table_html(listing.get("rooms"))
    if rooms_table:
        rooms_html = f"""
          <div class="property-panel">
            <span class="prop-subtitle">Aménagement</span>
            <h2>Pièces</h2>
            {rooms_table}
          </div>"""

    taxes_html = ""
    if listing.get("taxes"):
        taxes_html = f"""
          <div class="property-panel">
            <span class="prop-subtitle">Finances</span>
            <h2>Taxes et évaluation</h2>
            {kv_list_html(listing.get("taxes"))}
          </div>"""

    additional_html = ""
    if listing.get("additionalInfo"):
        additional_html = f"""
          <div class="property-panel property-panel-muted">
            <span class="prop-subtitle">À noter</span>
            <h2>Information supplémentaire</h2>
            <p>{escape(listing.get("additionalInfo") or "")}</p>
          </div>"""

    body = f"""{head_block(
        title=listing.get("shareTitle") or listing.get("title") or "Propriété",
        description=description,
        canonical=canonical,
        og_image=og_image,
        depth=depth,
    )}
<body class="antialiased bg-fred-gray text-fred-blue font-sans selection:bg-fred-gold selection:text-white property-details-page">
{header}
<main>
  <section class="section property-detail">
    <div class="max-w-7xl mx-auto px-6 md:px-8">
      <nav class="prop-breadcrumb" aria-label="Fil d'Ariane">
        <a href="{p}proprietes.html">Propriétés</a>
        <span>/</span>
        <span>{escape(city_label)}</span>
        <span>/</span>
        <span>{escape(sector_label)}</span>
      </nav>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 lg:gap-8 items-start">
        <div class="lg:col-span-7">
          <section class="property-media"
            data-uls="{escape(listing['uls'])}"
            data-share-title="{escape(listing.get('shareTitle') or '')}"
            data-share-url="{escape(canonical)}"
            data-share-image="{escape(og_image)}"
            data-fallback-image="{escape(fallback)}"
            data-assets-base="{p}assets/img/proprietes/">
            <div class="property-gallery">
              <div class="gallery-main-wrap">
                <img id="property-gallery-main" src="{escape(fallback)}" alt="{escape(listing.get('title') or '')}">
                <button type="button" id="property-gallery-prev" aria-label="Photo précédente"><i class="bi bi-chevron-left"></i></button>
                <button type="button" id="property-gallery-next" aria-label="Photo suivante"><i class="bi bi-chevron-right"></i></button>
                <span id="property-gallery-counter">1 / 1</span>
                {badge}
              </div>
              <div id="property-gallery-thumbs" class="gallery-thumbs"></div>
            </div>
            <div class="property-share">
              <p>Partager cette propriété</p>
              <div id="property-share-buttons"></div>
            </div>
          </section>
        </div>
        <div class="lg:col-span-5">
          <div class="property-summary">
            <span class="prop-subtitle">{escape(listing.get('propertyType') or 'Propriété')}</span>
            {price_html}
            <h1>{escape(listing.get('address') or listing.get('title') or '')}</h1>
            <p class="prop-city">{city_line}</p>
            <ul class="property-facts">
              {''.join(meta_rows)}
            </ul>
            {actions_html}
          </div>
        </div>
      </div>

      <div class="mt-8 max-w-4xl">
          <div class="property-description">
            <span class="prop-subtitle">À propos</span>
            <h2>Description de la propriété</h2>
            <p>{escape(listing.get('description') or 'Description à venir.')}</p>
          </div>
          {highlights_html}
          {details_html}
          {inclusions_html}
          {exclusions_html}
          {rooms_html}
          {taxes_html}
          {additional_html}
      </div>
    </div>
  </section>
</main>
{footer}
<script src="{p}assets/js/property-gallery.js" defer></script>
<script src="{p}assets/js/property-share.js" defer></script>
</body>
</html>
"""

    dest_dir = (
        ROOT
        / listing["country"]
        / listing["province"]
        / listing["city"]
        / listing["sector"]
        / listing["street"]
    )
    dest_dir.mkdir(parents=True, exist_ok=True)
    (dest_dir / "index.html").write_text(body, encoding="utf-8")
    print(f"wrote {dest_dir.relative_to(ROOT) / 'index.html'}")


def prune_stale_detail_pages(registry: dict) -> None:
    active_paths = {
        (
            listing["country"],
            listing["province"],
            listing["city"],
            listing["sector"],
            listing["street"],
        )
        for listing in registry.get("listings", [])
    }
    ca_root = ROOT / "ca" / "qc"
    if not ca_root.exists():
        return
    for index in ca_root.rglob("index.html"):
        rel = index.relative_to(ROOT)
        parts = rel.parts
        if len(parts) != 6:
            continue
        key = parts[:5]
        if key not in active_paths:
            index.unlink()
            # clean empty parents
            parent = index.parent
            for _ in range(5):
                if parent.exists() and not any(parent.iterdir()):
                    parent.rmdir()
                    parent = parent.parent
                else:
                    break
            print(f"removed stale {rel}")


def update_nav_links() -> None:
    """Point nav/footer 'Propriétés' Centris links to the local listings page."""
    pattern = re.compile(
        r'<a href="'
        + re.escape(CENTRIS_AGENT_URL)
        + r'"(?:\s+target="_blank")?(?:\s+rel="noopener noreferrer")?',
        re.IGNORECASE,
    )
    for path in ROOT.glob("*.html"):
        if path.name == "proprietes.html":
            continue
        text = path.read_text(encoding="utf-8")
        updated = pattern.sub('<a href="proprietes.html"', text)
        if updated != text:
            path.write_text(updated, encoding="utf-8")
            print(f"updated Propriétés links in {path.name}")


def generate_all() -> None:
    registry = load_registry()
    generate_listings_page(registry)
    for listing in registry.get("listings", []):
        generate_detail_page(listing)
    prune_stale_detail_pages(registry)
    update_nav_links()


if __name__ == "__main__":
    generate_all()
