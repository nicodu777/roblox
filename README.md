# Studio Nico

Site vitrine de Studio Nico : création de sites web, à distance partout en France.

## Organisation

```
├── README.md      ce fichier
├── A_FAIRE.md     idées et tâches à venir
├── src/           les sources (c'est ici qu'on modifie le site)
│   ├── page.html    le site complet : textes, styles, animations
│   ├── fonts.css    déclaration des polices
│   └── build.py     génère le dossier site/
└── site/          le site prêt à mettre en ligne (généré, ne pas modifier à la main)
    ├── index.html
    ├── .htaccess    réglages Hostinger : HTTPS, compression, cache, sécurité
    ├── robots.txt
    ├── sitemap.xml
    ├── fonts/       polices hébergées sur le site (RGPD)
    └── img/         photos, icônes, image de partage
```

## Modifier le site

1. Modifier `src/page.html`.
2. Lancer `python3 src/build.py` : le dossier `site/` est régénéré.

Le jour où le nom de domaine est acheté, changer `SITE_URL` en haut de `src/build.py`, puis relancer la commande.

## Mettre en ligne sur Hostinger

Envoyer **le contenu** du dossier `site/` (pas le dossier lui-même) dans `public_html`, avec le gestionnaire de fichiers ou en FTP. Pensez à afficher les fichiers cachés pour ne pas oublier `.htaccess`.
