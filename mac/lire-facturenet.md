LECTURE FACTURE.NET SEULE, lancée par le bouton « F » de l'écran « Suivi des factures » de l'iPad. Pas de Trello, pas de WhatsApp, pas de SSD : uniquement facture.net, le plus vite possible.

facture.net est la SEULE source des factures du Dashboard : ce qui y est « Encaissé » est payé, ce qui est « Finalisé » reste à toucher. Le cash n'y est pas et ne doit pas apparaître.

1. `git -C /Users/noamoudiz/ipad-dashboard pull --no-rebase` puis lis data/factures.json (l'ancien fichier).
2. Avec Claude in Chrome (tabs_context_mcp avec createIfEmpty), ouvre https://www.facture.net/418029/invoices dans l'onglet du groupe Claude déjà ouvert : ne crée jamais de nouvel onglet ni de nouveau groupe. Si Chrome ne répond pas du premier coup : arrête-toi, ne modifie aucun fichier, réponds « ERREUR : Chrome injoignable ».
2b. Si la page demande de se connecter (formulaire e-mail / mot de passe) : ne tape RIEN, ferme l'onglet et réponds « ERREUR : connecte-toi à facture.net dans Chrome sur le Mac ».
3. LECTURE SEULE : ne clique jamais sur Créer, Encaisser, Modifier, Envoyer, Supprimer, Télécharger ni sur un menu « ⋮ ». Seules navigations permises : passer d'une page de la liste à la suivante (pagination en bas : « 2 », « 3 »…) et ouvrir une facture pour lire son détail (étape 3b), puis revenir à la liste. Lis la liste avec get_page_text, TOUTES les pages. Chaque facture s'affiche ainsi :
   numéro (F26…) · éventuellement « R » · statut · client · montant (« 150,00 € ») · date de création · date de paiement (seulement si encaissée).
   - « Encaissé » = payée : la 2e date est la date de paiement.
   - « Finalisé » = envoyée, pas encore payée.
   - « Rectifié », « Provisoire », « Annulé », les avoirs et les montants à 0 € : ignore-les.
3b. PROJET (« detail ») : la liste ne donne que le client qui paie ; Noam doit savoir de quel projet il s'agit. Pour chaque facture qui ira dans "factures", et pour les "encaisses" du MOIS EN COURS seulement (étape 4) : si l'ancien data/factures.json a déjà la même facture (même id) avec un "detail", reprends-le sans rien ouvrir. Sinon ouvre la facture (find avec son numéro, ex. « F2600046 », puis clic sur ce numéro), descends jusqu'au tableau « Détail » de l'aperçu (c'est une image : screenshot / zoom) et lis la 1re ligne de « Description ». Résume-la en 2 à 5 mots : projet ou client final + ce qui a été fait, ex. « Clip « Onlyfan » · Ogynae », « Marla · 3 vidéos verticales », « Mika · Maison de santé ». Illisible → laisse "detail" vide. Puis reviens à la liste.
   Payeurs connus (le client facturé n'est pas toujours le projet) : ZENJI = Zack, qui paie aussi tous les projets Michalak, Paris Select (Astotel, Ladurée…) et Marie Claire (Grand Café) : detail « Michalak · … », « Paris Select · … », « Marie Claire · … » ou « Zack · … » selon la facture ; ENSEMBLE EXPERIENCE = projets « Ensemble … ». Sur Trello, une carte peut porter « 🧾 Facturé à : … ».
4. Écris data/factures.json avec l'outil Write (UTF-8, indentation 1) :
   {"updated": "vendredi 27 nov. à 15h20", "source": "facture.net",
    "factures": [ {"id": "F2600046", "projet": "RYL", "detail": "Marla · 3 vidéos verticales", "brut": 250, "reste": 250, "entree": "2026-11-05"}, … ],
    "encaisses": [ {"id": "F2600047", "projet": "PKM", "detail": "Le Barranco", "montant": 150, "date": "2026-11-24"}, … ]}
   - "factures" = TOUTES les factures « Finalisé » ; id = numéro ; projet = nom du client tel qu'affiché ; brut = reste = montant (nombre, sans €) ; entree = date de création (AAAA-MM-JJ). Triées de la plus ancienne à la plus récente.
   - "encaisses" = factures « Encaissé » dont la DATE DE PAIEMENT tombe dans le mois en cours ou le mois précédent (heure de Paris) ; montant = montant ; date = date de paiement. Plus récentes en haut.
   - "updated" = maintenant, heure de Paris (`TZ=Europe/Paris date`), au format de l'exemple.
   - Rien d'autre dans le fichier (pas de "masque", pas de Trello).
5. Ferme l'onglet ouvert (rien ne doit rester dans la barre d'onglets).
6. `git -C /Users/noamoudiz/ipad-dashboard add data/factures.json`, `git -C /Users/noamoudiz/ipad-dashboard commit -m "Factures : lecture facture.net (iPad)"`, `git -C /Users/noamoudiz/ipad-dashboard push` (si le push est refusé : pull --no-rebase puis push).
7. Réponds en une seule ligne, la toute dernière : « OK : <N> à toucher · <X> € encaissés en <mois> ». Si une étape a échoué (Chrome injoignable, pas connecté, push refusé…), ne fais rien de plus et réponds « ERREUR : <raison très courte, en français simple> ».
