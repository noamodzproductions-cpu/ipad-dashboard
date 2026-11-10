# Dashboard Noam

Avant toute modif visuelle, lire DESIGN.md et respecter les contraintes iPad Air 1 / Safari 12.

## Contexte
- Web app pour iPad Air 1 (iOS 12.5, Safari 12), 1024×768 en paysage, publiée sur GitHub Pages.
- `index.html` = version normale (en service). `test/index.html` = version d'essai du style DESIGN.md.
- Ne jamais modifier la version normale quand on travaille sur `/test`.

## Contraintes Safari 12
- Un seul fichier HTML/CSS/JS vanilla, sans framework, sans dépendance, sans police web (police système -apple-system).
- Interdit : `?.`, `??`, flex `gap`, `aspect-ratio`, `:is`/`:where`, `inset`, `backdrop-filter`/flou, animations CSS en boucle.
- Cibles tactiles ≥ 70 px, textes lisibles à 1 m, tout tient en 1024×768 sans scroller (sauf les listes).
- Données en localStorage (`noamdash` pour la version normale, `noamdash-test` pour `/test`).

## Vérification
- Devis : 1 journée + 6 h de montage + 1 trajet → brut 990 €, URSSAF 238 €, frais 30 €, net 722 €.
