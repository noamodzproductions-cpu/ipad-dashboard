# Dashboard Noam

Avant toute modif visuelle, respecter le style de accueil-bento.html et les contraintes iPad Air 1 / Safari 12.

## Contexte
- Web app pour iPad Air 1 (iOS 12.5, Safari 12), 1024×768 en paysage, publiée sur GitHub Pages.
- `index.html` = version normale (en service). `test/index.html` = version d'essai au style de `accueil-bento.html` (maquette de référence, look et disposition seulement).
- Ne jamais modifier la version normale quand on travaille sur `/test`.
- /test : PAS de fond d'écran (fond noir uni #000), cartes pleines gris foncé #1c1c1e (Devis : carte claire #E9E9EC). `bg.jpg`/`blur.jpg` ne sont plus utilisés.
- Écran Projets : bouton icône « Missions du jour » (à gauche de « + Projet ») qui ouvre la page Claude « Aujourd'hui » (https://claude.ai/artifact/Ff3ZbqjcB6FYCZBsdPyeoW), mise à jour 2×/jour par la routine Suivi. Ne pas supprimer.
- Accueil /test : en-tête (Bonjour/Bonsoir Noam, date, heure, engrenage) + disposition de accueil-bento.html : à gauche Chrono en grande carte (anneau + temps + interrupteur), à droite en haut Devis (carte claire) et Projets, à droite en bas une carte VIDE (temporaire, rien d'écrit). Juste nom + icône. Pas d'infos en plus (pas d'argent, pas d'URSSAF). Le widget Projets ouvre la page interne « Projets » (écran `taches`, planning de la semaine), pas Safari : claude.ai interdit l'affichage intégré (frame-ancestors 'self') et ne s'affiche pas sur iOS 12. L'ancien écran Projets avec les montants n'est plus relié à l'accueil.
- /test : un seul mode (pas de mode nuit), pas d'effet « bounce » au toucher, le fond ne doit jamais bouger (touchmove bloqué hors des listes).
- Les mises en page doivent tenir aussi dans Safari avec barre d'adresse (~1024×690), pas seulement en plein écran (1024×768).
- `DESIGN.md` (style Mobbin) = ancienne piste, remplacée par `accueil-bento.html`.

## Projets = planning de la semaine (`semaine.json` à la racine du repo)
- Source UNIQUE : écrit par le Claude du planning de la semaine (conversation sur le téléphone) à chaque mise à jour. Pas de copie intermédiaire.
- Format : `{updated, days:[{date:"AAAA-MM-JJ", jour:"Mercredi 11 novembre", tasks:[{id, client, text, done}]}]}`. `id` stable d'un jour à l'autre (sert aux coches). Texte commençant par « URGENT · » = tâche urgente.
- /test le lit en XMLHttpRequest (`../semaine.json`) à l'ouverture puis toutes les 5 min, cache hors ligne. Affiche UNIQUEMENT la journée (pas de flèches). Vue semaine = planning Claude de Noam sur iPhone (pas de page semaine ici).
- Coches locales à l'iPad, ou partagées dans semaine.json si une clé GitHub est collée dans Réglages (clé stockée à part, jamais exportée). Journée finie → « Journée terminée ✓ » et les tâches pas faites du/des jour(s) suivant(s) remontent en « En avance ».
- Le fichier est PUBLIC (GitHub Pages) : noms de clients visibles. Chiffrement possible plus tard.

## Contraintes Safari 12 / iPad Air 1
- Un seul fichier HTML/CSS/JS vanilla, sans framework, sans dépendance, sans police web (police système -apple-system).
- Interdit : `backdrop-filter`, `filter`, `blur()`, grosses ombres, animations CSS en boucle, `?.`, `??`, flex `gap` (grid-gap OK), `aspect-ratio`, `:is`/`:where`/`:has`, `inset`.
- Transitions uniquement sur `transform` et `opacity`. L'heure et le chrono ne mettent à jour que leur texte et la poignée.
- Couleurs : noir, blanc, gris + vert #4ade80 et violet #A78BFA, rien d'autre.
- Cibles tactiles ≥ 70 px, textes lisibles à 1 m, tout tient en 1024×768 sans scroller (sauf les listes).
- Données en localStorage (`noamdash` pour la version normale, `noamdash-test` pour `/test`).

## Vérification
- Devis : 1 journée + 6 h de montage + 1 trajet → brut 990 €, URSSAF 238 €, frais 30 €, net 722 €.
- /test : tournage saisi en HEURES par jour (1-3 h = h × 80 €, 4 h = demi-journée 300 €, puis +50 € par heure : 8 h = journée 500 €). Montage affiché avec son prix à l'heure (taux × (1 + retours)). Exemple /test : 8 h + 6 h de montage + 1 trajet → 990 / 238 / 30 / 722.
- Devis /test : pages épurées (pas de % ni de prix sous les boutons), bouton Exporter = texte ligne par ligne pour facture.net (désignation · 1 · prix, mention TVA 293 B).
