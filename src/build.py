"""Génère index.html (site GitHub Pages, photos dans img/) et la version Artifact (photos intégrées).
Usage : python3 src/build.py [chemin_artifact.html]"""
import base64, pathlib, re, sys
root = pathlib.Path(__file__).resolve().parent.parent
src = (root / "src" / "page.html").read_text(encoding="utf-8")
imgs = {p.stem: p for p in (root / "img").glob("*.jpg")}

def sub(html, fn):
    return re.sub(r"__IMG_(\w+)__", lambda m: fn(m.group(1)), html)

# Site autonome
head, rest = src.split("</style>", 1)
head = head.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
# Polices hébergées localement (RGPD : aucune adresse IP transmise à Google)
import re as _re
head = _re.sub(r'<link rel="preconnect"[^>]*>\n', "", head)
head = _re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^"]*">', '<link rel="stylesheet" href="fonts/fonts.css">', head)
head = head.replace("*{box-sizing:border-box}", "*{box-sizing:border-box}\nbody{margin:0}\nimg{max-width:100%}\n[hidden]{display:none!important}\n:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}", 1)
site = ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + head + "</style>\n</head>\n<body>" + rest + "\n</body>\n</html>\n")
(root / "index.html").write_text(sub(site, lambda k: f"img/{k}.jpg"), encoding="utf-8")

# Version Artifact
if len(sys.argv) > 1:
    uri = lambda k: "data:image/jpeg;base64," + base64.b64encode(imgs[k].read_bytes()).decode()
    pathlib.Path(sys.argv[1]).write_text(sub(src, uri), encoding="utf-8")
print("ok")
