LECTURE TRELLO SEULE, lancée depuis le bouton « Lire Trello » de l'iPad. Pas de WhatsApp, pas de SSD : uniquement Trello, et le plus vite possible.

Règles complètes du planning (format, textes courts, une tâche par vidéo, priorités…) : lis ~/.claude/scheduled-tasks/planning-semaine/SKILL.md et applique-les, SAUF les parties WhatsApp et SSD que tu ignores.

1. `git -C /Users/noamoudiz/ipad-dashboard pull --no-rebase` puis lis semaine.json, data/production.json, data/factures.json et data/factures-etat.json (s'il existe).
2. Tableau « 🎬 Noam orga » = ari:cloud:trello::board/workspace/6aa7d13f1a28949c6ff323a5/6aa7d1be312c134671485c91. Lis son activité (trelloReadBoard, action list_activity) et ne garde que ce qui est plus récent que "trello_vu" de data/production.json. Rien de nouveau → ne touche à rien dans le planning (passe à l'étape 5 pour mettre l'heure à jour).
3. Pour chaque carte concernée seulement : ouvre-la (trelloReadCard get) et mets à jour data/production.json et les tâches de semaine.json (vidéo cochée = tâche faite, vidéo décochée = tâche à faire, carte qui change de liste, nouvelle carte en production = ses tâches). Respecte "perso", "supprimes" et l'ordre fixés par Noam.
4. Factures : relis la liste « 🧾 Solde en attente » et mets data/factures.json à jour comme dans les règles (y compris le déplacement des cartes payées, seule écriture Trello autorisée).
5. Mets "trello_vu" = maintenant (AAAA-MM-JJTHH:MM, UTC) dans data/production.json et "updated" de semaine.json au format « dimanche 15 nov. à 1h20 » (heure de Paris). Ne change PAS "whatsapp".
6. `git -C /Users/noamoudiz/ipad-dashboard add semaine.json data/production.json data/factures.json`, `commit -m "Planning : lecture Trello (iPad)"`, `push` (si le push est refusé : pull --no-rebase puis push).
7. Réponds en une ligne : ce qui a changé.
