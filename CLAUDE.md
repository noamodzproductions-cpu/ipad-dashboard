# Dashboard Noam

Avant toute modif visuelle, respecter le style de accueil-bento.html et les contraintes iPad Air 1 / Safari 12.

## Contexte
- Web app pour iPad Air 1 (iOS 12.5, Safari 12), 1024×768 en paysage, publiée sur GitHub Pages.
- `index.html` = version normale (en service). `test/index.html` = version d'essai au style de `accueil-bento.html` (maquette de référence, look et disposition seulement).
- Ne jamais modifier la version normale quand on travaille sur `/test`.
- /test : PAS de fond d'écran (fond noir uni #000), cartes pleines gris foncé #1c1c1e (Devis : carte claire #E9E9EC). `bg.jpg`/`blur.jpg` ne sont plus utilisés.
- Écran Projets : bouton icône « Missions du jour » (à gauche de « + Projet ») qui ouvre la page Claude « Aujourd'hui » (https://claude.ai/artifact/Ff3ZbqjcB6FYCZBsdPyeoW), mise à jour 2×/jour par la routine Suivi. Ne pas supprimer.
- Accueil /test : en-tête (Bonjour/Bonsoir Noam, date, heure, engrenage) + disposition de accueil-bento.html : à gauche « Suivi des factures » en grande carte (remplace le Chrono, supprimé), à droite en haut Devis (carte claire) et Projets, à droite en bas la carte « Musique » (lance le live Lofi Girl sur le Mac via `mac/musique.py`, port 8765, LaunchAgent `com.noam.musique` ; si le Mac ne répond pas, propose d'ouvrir le live sur l'iPad). Juste nom + icône (sauf la tuile Factures). Le widget Projets ouvre la page interne « Projets » (écran `taches`, planning de la semaine), pas Safari : claude.ai interdit l'affichage intégré (frame-ancestors 'self') et ne s'affiche pas sur iOS 12. L'ancien écran Projets avec les montants n'est plus relié à l'accueil.
- /test : un seul mode (pas de mode nuit), pas d'effet « bounce » au toucher, le fond ne doit jamais bouger (touchmove bloqué hors des listes).
- Les mises en page doivent tenir aussi dans Safari avec barre d'adresse (~1024×690), pas seulement en plein écran (1024×768).
- `DESIGN.md` (style Mobbin) = ancienne piste, remplacée par `accueil-bento.html`.

## Suivi des factures (`data/factures.json`)
- Écrit par la routine planning-semaine-ipad (liste lue à chaque passage, reste de Trello 1×/jour) : cartes ouvertes de la liste « 🧾 Solde en attente ». Format : `{updated, factures:[{id, projet, brut, reste, entree:"AAAA-MM-JJ"}]}`.
- Tuile accueil : icône + total à toucher + « N à relancer » (violet) ; elle ouvre l'écran `factures` : cases À toucher / URSSAF 23,2 % / Net / Encaissé du mois (payés cochés sur l'iPad + cartes sorties de « Solde en attente », gardés 70 j dans facEtat.encaisses), puis une carte par facture (plus ancienne d'abord) avec, séparées par un trait, deux petites cases sans texte (titres « Relancé » / « Payé » une seule fois au-dessus) : Relancé cochée = violet tant que les 15 jours courent (re-toucher = retirer), Payé cochée = vert (re-toucher = décocher). Ligne d'état : « En attente depuis X j · relance dans Y j / à relancer », « Relancé il y a X j · prochaine relance dans Y j / à relancer de nouveau » (bord violet quand c'est à relancer). Payées : carte grisée en bas, montant barré. Toucher le nom ouvre le détail (historique des relances). Bandeau « Annuler » après chaque action.
- État iPad (`data.facEtat` = {relances:{id:[ms]}, payes:{id:ms}}) envoyé avec la clé GitHub dans `data/factures-etat.json` (écrit UNIQUEMENT par l'iPad). La routine lit ce fichier à chaque passage : déplace les payés dans « ✅ Payé & Archivé » et ajoute la tâche `relance-<6 car.>-<AAAAMMJJ>` le jour de l'échéance.
- Vérif : Clip Ogynae Onlyfan 400 €, Mika Maison de la Santé 450 €, Le Barranco 150 € → 1 000 € / URSSAF 232 € / net 768 €.

## Projets = planning de la semaine (`semaine.json` à la racine du repo)
- Source UNIQUE : écrit par le Claude du planning de la semaine (conversation sur le téléphone) à chaque mise à jour. Pas de copie intermédiaire.
- Format : `{updated, days:[{date:"AAAA-MM-JJ", jour:"Mercredi 11 novembre", tasks:[{id, client, text, done}]}]}`. `id` stable d'un jour à l'autre (sert aux coches). Texte commençant par « URGENT · » = tâche urgente.
- /test le lit en XMLHttpRequest (`../semaine.json`) à l'ouverture puis toutes les 5 min, cache hors ligne. Affiche UNIQUEMENT la journée (pas de flèches). Vue semaine = planning Claude de Noam sur iPhone (pas de page semaine ici).
- Gestes sur l'écran Projets : 1 appui = cocher, double appui = modifier (renommer, jour suivant, supprimer), glisser à gauche = supprimer (bandeau « Annuler » 5 s), appui long = déplacer plus haut/bas. Gardé sur l'iPad (`tEdits`) et, avec la clé GitHub, écrit dans semaine.json : `"supprimes":[ids]`, `"perso":true` (texte/jour fixés par Noam), ordre du jour. La routine planning-semaine-ipad les respecte.
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
- Devis /test : week-end = prix normal (pas de majoration) ; seul le jour férié est majoré (réglage « Jour férié », clé `weekend`, 30 %). Ex. 8 h un samedi = 990 € comme en semaine ; 8 h le 25 déc. = 1 140 €.
- Devis /test : pages épurées (pas de % ni de prix sous les boutons), bouton Exporter = texte ligne par ligne pour facture.net (désignation · 1 · prix, mention TVA 293 B).
