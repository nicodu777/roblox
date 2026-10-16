"""Génère index.html (site GitHub Pages, photos dans img/) et la version Artifact (photos intégrées).
Usage : python3 src/build.py [chemin_artifact.html]"""
import base64, pathlib, re, sys
# Adresse publique du site (à changer quand vous aurez votre nom de domaine, avec le / final)
SITE_URL = "https://nicodu777.github.io/roblox/"
TITLE = "Studio Nico · Création de sites web partout en France"
DESC = "Sites vitrines et boutiques en ligne sur mesure, partout en France (Paris, Lyon, Marseille, Toulouse…). Hébergement inclus, devis gratuit en 24 h."
root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "src" / "page.html").read_text(encoding="utf-8").replace("__SITE_URL__", SITE_URL)
imgs = {p.stem: p for p in (root / "img").glob("*.webp")}

def sub(html, fn):
    return re.sub(r"__IMG_(\w+)__", lambda m: fn(m.group(1)), html)

# Site autonome
head, rest = src.split("</style>", 1)
head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
# Polices hébergées localement (RGPD : aucune adresse IP transmise à Google)
import re as _re
head = _re.sub(r'<link rel="preconnect"[^>]*>\n', "", head)
fcss = (root / "fonts" / "fonts.css").read_text(encoding="utf-8").replace("url(", "url(fonts/")
pre = '<link rel="preload" href="fonts/bricolage-grotesque-normal-500.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="preload" href="fonts/instrument-sans-normal-400.woff2" as="font" type="font/woff2" crossorigin>\n'
head = _re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^"]*">', lambda m: pre + "<style>" + fcss + "</style>", head)
# Référencement et partage
head = head.replace("<title>Studio Nico</title>", f"<title>{TITLE}</title>", 1)
head = _re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', head, count=1)
meta = f"""<link rel="canonical" href="{SITE_URL}">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="img/apple-touch-icon.png">
<meta name="theme-color" content="#3B3FD1">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Studio Nico">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{SITE_URL}">
<meta property="og:image" content="{SITE_URL}img/og.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
"""
head = head.replace("<style>", meta + "<style>", 1)
(root / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
(root / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n  <url><loc>{SITE_URL}</loc><changefreq>monthly</changefreq><priority>1.0</priority></url>\n</urlset>\n', encoding="utf-8")
head = head.replace("*{box-sizing:border-box}", "*{box-sizing:border-box}\nbody{margin:0}\nimg{max-width:100%}\n[hidden]{display:none!important}\n:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}", 1)
site = ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + head + "</style>\n</head>\n<body>" + rest + "\n</body>\n</html>\n")
(root / "index.html").write_text(sub(site, lambda k: f"img/{k}.webp"), encoding="utf-8")

# Version Artifact
if len(sys.argv) > 1:
    uri = lambda k: "data:image/webp;base64," + base64.b64encode(imgs[k].read_bytes()).decode()
    pathlib.Path(sys.argv[1]).write_text(sub(src, uri), encoding="utf-8")
print("ok")
