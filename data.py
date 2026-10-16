# -*- coding: utf-8 -*-
"""Banque de questions : (question, bonne pratique, poids 1-3, drapeau)
Drapeau : "C" = impact direct sur les comptes, "L" = limitation de l'étendue des travaux, "" = autre
"""

DOMAINS = ["Banque", "Négoce", "Usine (industrie)", "ONG humanitaire", "ONG agricole"]

COMMON = {
    "1. Gouvernance et organisation": [
        ("Existe-t-il un organigramme à jour avec des responsabilités clairement définies ?",
         "Organigramme validé et diffusé, fiches de poste, délégations de pouvoir écrites.", 2, ""),
        ("Un manuel de procédures écrit et approuvé est-il en vigueur ?",
         "Manuel couvrant tous les cycles, approuvé par la direction, revu au moins une fois par an.", 2, ""),
        ("Les organes de gouvernance (conseil, assemblée, comité d'audit) se réunissent-ils avec des PV formalisés ?",
         "Calendrier annuel de réunions, PV signés, suivi des décisions.", 2, ""),
        ("Existe-t-il un code d'éthique, une politique anti-fraude et un dispositif d'alerte ?",
         "Code de conduite signé par le personnel, ligne d'alerte confidentielle, déclaration annuelle des conflits d'intérêts.", 3, ""),
        ("Une cartographie des risques est-elle établie et mise à jour ?",
         "Cartographie annuelle (probabilité x impact), plans de traitement et propriétaires de risques désignés.", 2, ""),
        ("Une fonction d'audit/contrôle interne existe-t-elle et rend-elle compte à la direction ?",
         "Plan d'audit annuel basé sur les risques, rapports suivis, indépendance vis-à-vis des opérationnels.", 2, ""),
    ],
    "2. Comptabilité et information financière": [
        ("La comptabilité est-elle tenue à jour (retard maximum d'un mois) selon le référentiel applicable (SYSCOHADA, IFRS, PCG...) ?",
         "Saisie continue, calendrier de clôture mensuelle, référentiel comptable documenté.", 3, "C"),
        ("Les rapprochements bancaires sont-ils réalisés et revus chaque mois par une personne indépendante ?",
         "Rapprochement mensuel signé, éléments en suspens justifiés et apurés sous 30 jours.", 3, "C"),
        ("Les écritures manuelles sont-elles justifiées, approuvées et séparées de la saisie ?",
         "Pièce justificative systématique, validation par un responsable, journal des écritures manuelles revu.", 3, "C"),
        ("Les soldes des comptes de bilan sont-ils justifiés (balances auxiliaires, états de rapprochement) à la clôture ?",
         "Dossier de justification de chaque compte significatif, revu et signé.", 3, "C"),
        ("Les provisions, charges à payer et produits constatés d'avance sont-ils estimés selon une méthode documentée ?",
         "Procédure de cut-off, méthode de provisionnement écrite, revue par la direction financière.", 2, "C"),
        ("Un inventaire physique des immobilisations est-il fait annuellement et rapproché de la comptabilité ?",
         "Inventaire annuel contradictoire, étiquetage, traitement des écarts et des mises au rebut.", 2, "C"),
        ("Les parties liées et engagements hors bilan sont-ils recensés et présentés en annexe ?",
         "Registre des parties liées, circularisation des avocats/banques, annexe complète.", 2, "C"),
        ("Les états financiers sont-ils arrêtés dans les délais légaux et approuvés par les organes compétents ?",
         "Arrêté des comptes dans les 3-6 mois, approbation formelle, dépôt réglementaire.", 2, "C"),
        ("L'auditeur a-t-il eu accès à tous les documents, registres et interlocuteurs demandés ?",
         "Aucune restriction d'accès ; lettre d'affirmation signée par la direction.", 3, "L"),
    ],
    "3. Trésorerie": [
        ("Les comptes bancaires sont-ils ouverts et fermés sur autorisation formelle, avec double signature ?",
         "Liste des comptes et signataires tenue à jour, double signature au-delà d'un seuil.", 3, "C"),
        ("La caisse est-elle plafonnée, comptée régulièrement et contrôlée de façon inopinée ?",
         "Plafond de caisse, comptage hebdomadaire contradictoire, PV de caisse.", 3, "C"),
        ("Existe-t-il un plan de trésorerie prévisionnel suivi mensuellement ?",
         "Prévisionnel à 3-12 mois, analyse des écarts, alertes de liquidité.", 1, ""),
        ("Les paiements sont-ils effectués uniquement sur pièces approuvées (bon à payer) ?",
         "Triple rapprochement (commande, réception, facture), approbation selon délégations.", 3, "C"),
    ],
    "4. Achats et dépenses": [
        ("Les achats sont-ils soumis à des seuils d'approbation et à une mise en concurrence (devis/appels d'offres) ?",
         "Politique d'achat écrite, trois devis au-delà d'un seuil, comité d'ouverture des offres.", 3, ""),
        ("Les fonctions de commande, réception et paiement sont-elles séparées ?",
         "Séparation des tâches, accès système cloisonnés.", 3, "C"),
        ("Les fournisseurs sont-ils référencés et vérifiés avant création en base ?",
         "Procédure de référencement, contrôle d'existence, revue périodique du fichier fournisseurs.", 2, ""),
        ("Les dettes fournisseurs sont-elles rapprochées des relevés fournisseurs ?",
         "Rapprochement périodique, analyse de l'antériorité, traitement des litiges.", 2, "C"),
    ],
    "5. Ressources humaines et paie": [
        ("Les dossiers du personnel sont-ils complets (contrat, pièces d'identité, diplômes) ?",
         "Dossier standardisé, archivage sécurisé, revue annuelle.", 1, ""),
        ("La paie est-elle calculée, contrôlée et validée par des personnes différentes ?",
         "Séparation RH/paie/paiement, revue des états de paie, contrôle de l'existence réelle des employés.", 3, "C"),
        ("Les cotisations sociales et impôts sur salaires sont-ils déclarés et payés dans les délais ?",
         "Calendrier de conformité, rapprochement paie/déclarations/comptabilité.", 2, "C"),
    ],
    "6. Systèmes d'information": [
        ("Les droits d'accès aux logiciels (comptable, paie, stocks) sont-ils attribués selon les fonctions et revus ?",
         "Matrice des droits, revue semestrielle, désactivation immédiate des départs.", 2, ""),
        ("Des sauvegardes régulières sont-elles réalisées, externalisées et testées ?",
         "Sauvegarde quotidienne, copie hors site, test de restauration annuel.", 2, ""),
        ("Existe-t-il un plan de continuité / reprise d'activité testé ?",
         "PCA/PRA écrit, testé chaque année, responsables identifiés.", 1, ""),
    ],
    "7. Conformité fiscale, sociale et juridique": [
        ("Les déclarations fiscales (TVA, impôt sur les sociétés/bénéfices, retenues) sont-elles déposées dans les délais ?",
         "Calendrier fiscal, revue de cohérence avec la comptabilité, suivi des contrôles fiscaux.", 3, "C"),
        ("Les litiges et contentieux sont-ils recensés et provisionnés si nécessaire ?",
         "Registre des litiges, avis des conseils juridiques, provision selon le risque estimé.", 2, "C"),
        ("Les autorisations, licences et agréments nécessaires à l'activité sont-ils à jour ?",
         "Registre des licences avec dates d'échéance et responsable de renouvellement.", 2, ""),
    ],
}

SPECIFIC = {
    "Banque": {
        "8. Spécificités bancaires": [
            ("Les ratios prudentiels (solvabilité, liquidité, division des risques) sont-ils calculés et respectés ?",
             "Calcul mensuel, tableau de bord, plan d'action en cas de dépassement, déclaration à l'autorité de supervision.", 3, "C"),
            ("Le dispositif KYC / LCB-FT (lutte contre le blanchiment) est-il appliqué à l'ouverture et en cours de relation ?",
             "Identification et vérification des clients, profilage du risque, filtrage des listes de sanctions, déclarations de soupçon.", 3, ""),
            ("Les crédits sont-ils octroyés après analyse documentée et décision d'un comité selon des délégations ?",
             "Dossier de crédit complet, notation interne, comité de crédit, garanties valorisées et inscrites.", 3, ""),
            ("Les créances sont-elles classées (saines, douteuses, contentieuses) et provisionnées selon la réglementation ?",
             "Revue trimestrielle du portefeuille, déclassement automatique selon l'impayé, provisions IFRS 9/réglementaires.", 3, "C"),
            ("Les fonctions front-office, back-office et contrôle des risques sont-elles séparées ?",
             "Organisation indépendante, limites de trading/engagement, reporting direct au comité des risques.", 3, ""),
            ("Les comptes de liaison, nostro/vostro et comptes d'attente sont-ils rapprochés et apurés ?",
             "Rapprochement quotidien/hebdomadaire, apurement sous 30 jours, revue des suspens anciens.", 3, "C"),
            ("Les intérêts et commissions sont-ils calculés par le système et vérifiés par sondage ? Le taux effectif global respecte-t-il le taux d'usure ?",
             "Paramétrage contrôlé, tests périodiques, revue du TEG.", 2, "C"),
            ("Les fonctions de conformité et d'audit interne rendent-elles compte au conseil d'administration ?",
             "Rapports trimestriels, plan annuel validé, suivi des recommandations de la supervision.", 2, ""),
        ]},
    "Négoce": {
        "8. Spécificités négoce": [
            ("Les contrats d'achat et de vente sont-ils écrits, approuvés et enregistrés avant exécution ?",
             "Contrat signé selon délégations, registre des contrats, revue juridique.", 3, ""),
            ("Les stocks sont-ils inventoriés physiquement (contrôle qualité/quantité par un tiers si nécessaire) et valorisés au coût ou à la valeur nette de réalisation ?",
             "Inventaire contradictoire, contrôle d'un surveillant indépendant, dépréciation des stocks lents.", 3, "C"),
            ("Les limites de crédit clients sont-elles fixées, suivies et les créances anciennes relancées/dépréciées ?",
             "Étude de solvabilité, assurance-crédit/lettre de crédit, balance âgée mensuelle, provisions.", 3, "C"),
            ("Le risque de change et de variation des prix est-il identifié et couvert selon une politique approuvée ?",
             "Politique de couverture écrite, position suivie quotidiennement, limites approuvées.", 2, "C"),
            ("Les documents d'import/export (connaissements, déclarations en douane, incoterms) sont-ils contrôlés et archivés ?",
             "Dossier par opération, rapprochement avec les factures, suivi des droits et taxes.", 2, "C"),
            ("Le chiffre d'affaires est-il comptabilisé au transfert effectif de propriété/risques (séparation des exercices) ?",
             "Contrôle de cut-off à la clôture selon les incoterms, revue des livraisons proches de la clôture.", 3, "C"),
            ("Les contreparties (clients, fournisseurs, intermédiaires) font-elles l'objet d'une vérification d'intégrité et de sanctions ?",
             "Due diligence, filtrage des listes de sanctions, clauses anticorruption.", 2, ""),
        ]},
    "Usine (industrie)": {
        "8. Spécificités industrielles": [
            ("Existe-t-il une comptabilité analytique donnant le coût de revient par produit ?",
             "Nomenclatures et gammes à jour, coûts standards revus, analyse mensuelle des écarts.", 3, "C"),
            ("Les stocks (matières, en-cours, produits finis) sont-ils inventoriés régulièrement et valorisés selon une méthode documentée (CMP, FIFO) ?",
             "Inventaire tournant et annuel, valorisation documentée, dépréciation des obsolètes.", 3, "C"),
            ("Les rendements, pertes et rebuts de production sont-ils mesurés et analysés ?",
             "Suivi des taux de rendement par ligne, seuils d'alerte, enquête sur les écarts.", 2, "C"),
            ("Une maintenance préventive planifiée est-elle appliquée aux équipements critiques ?",
             "Plan de maintenance, GMAO, historique des pannes, stock de pièces critiques.", 2, ""),
            ("Les amortissements reflètent-ils la durée d'utilité réelle et les immobilisations en cours sont-elles suivies ?",
             "Tableau d'immobilisations, revue annuelle des durées, test de dépréciation si indice de perte de valeur.", 2, "C"),
            ("Un système de contrôle qualité (normes ISO, laboratoire, traçabilité des lots) est-il en place ?",
             "Procédures de contrôle à réception/production/expédition, traçabilité par lot, gestion des non-conformités.", 2, ""),
            ("Les règles d'hygiène, sécurité et environnement (HSE) sont-elles appliquées et les déchets gérés ?",
             "Registre des accidents, formations, EPI, plan de gestion des déchets, conformité environnementale.", 2, ""),
        ]},
    "ONG humanitaire": {
        "8. Spécificités ONG humanitaire": [
            ("La comptabilité est-elle tenue par projet/bailleur avec des codes analytiques distincts ?",
             "Plan analytique par bailleur et projet, rapprochement budget/réalisé, rapports financiers conformes aux exigences des bailleurs.", 3, "C"),
            ("Les fonds restreints (affectés) sont-ils distingués des fonds non affectés et les produits constatés selon les conditions des accords ?",
             "Suivi des fonds dédiés, reconnaissance des produits selon les conventions, fonds non utilisés correctement reportés/restitués.", 3, "C"),
            ("Les achats respectent-ils les règles de passation de marchés des bailleurs (seuils, comité, dossiers complets) ?",
             "Manuel d'achats aligné sur les règles des bailleurs, comparaison d'offres, justification des marchés de gré à gré.", 3, ""),
            ("Les bénéficiaires sont-ils ciblés selon des critères écrits, listés et vérifiés avant distribution ?",
             "Listes validées par la communauté, vérification d'identité, émargement, contrôle post-distribution.", 3, ""),
            ("Les transferts monétaires et la gestion du cash (paiements en espèces, mobile money) sont-ils sécurisés et rapprochés ?",
             "Prestataire financier agréé, contrôle des listes de paiement, rapprochement, plafonds de caisse terrain.", 3, "C"),
            ("Les stocks de biens humanitaires sont-ils suivis (entrées, sorties, inventaires) avec bons de livraison signés ?",
             "Fiches de stock, inventaire périodique, traçabilité jusqu'au point de distribution, pertes déclarées.", 2, "C"),
            ("Existe-t-il une politique de protection contre l'exploitation et les abus sexuels (PSEAH) et un mécanisme de plaintes ?",
             "Politique signée, formation obligatoire, canal de plaintes accessible, enquêtes documentées.", 3, ""),
            ("Les coûts indirects (frais de structure) sont-ils imputés selon une clé de répartition approuvée par les bailleurs ?",
             "Clé de répartition documentée, plafonds respectés, justificatifs conservés.", 2, "C"),
            ("Un plan de sécurité du personnel et des actifs en zones à risque existe-t-il ?",
             "Analyse de contexte, procédures d'évacuation, assurance, point de sécurité régulier.", 2, ""),
        ]},
    "ONG agricole": {
        "8. Spécificités ONG agricole": [
            ("La comptabilité est-elle tenue par projet/bailleur avec suivi des subventions reçues et consommées ?",
             "Plan analytique par projet, états de rapprochement avec le budget du bailleur, rapports financiers périodiques.", 3, "C"),
            ("Les intrants distribués (semences, engrais, outils) sont-ils suivis en stock, avec listes de bénéficiaires émargées ?",
             "Fiches de stock, bons de sortie, listes de producteurs signées, contrôle terrain par sondage.", 3, "C"),
            ("Les relations avec les coopératives et producteurs sont-elles encadrées par des conventions écrites ?",
             "Conventions signées, engagements réciproques, suivi des obligations de chaque partie.", 2, ""),
            ("Les crédits ou avances aux producteurs sont-ils suivis, recouvrés et dépréciés si nécessaire ?",
             "Échéancier de remboursement, relances, provisions sur impayés, analyse du risque de la campagne.", 3, "C"),
            ("Les équipements agricoles et actifs du projet sont-ils inventoriés, immatriculés et leur affectation suivie ?",
             "Registre des immobilisations par projet, étiquetage, traitement des actifs en fin de projet selon le bailleur.", 2, "C"),
            ("Un système de suivi-évaluation mesure-t-il les résultats (rendements, revenus, surfaces) par rapport au cadre logique ?",
             "Indicateurs de base et cibles, collecte fiable, rapports d'avancement vérifiés.", 2, ""),
            ("Les récoltes ou produits commercialisés sont-ils tracés (pesée, qualité, stockage, vente) ?",
             "Bons de pesée, magasins sécurisés, registres de stock, inventaire contradictoire, contrats de vente.", 3, "C"),
            ("Les impacts environnementaux (eau, pesticides, sols) sont-ils évalués et des mesures de protection appliquées ?",
             "Étude d'impact, utilisation encadrée des produits phytosanitaires, formation des producteurs.", 2, ""),
            ("La saisonnalité des activités est-elle prise en compte dans la planification de trésorerie et des décaissements ?",
             "Calendrier cultural, prévision de trésorerie par saison, décaissements anticipés pour les intrants.", 1, ""),
        ]},
}


def build_questionnaire(domain):
    """Retourne une liste de sections [(nom, [questions])] avec identifiants uniques."""
    sections = {}
    sections.update(COMMON)
    sections.update(SPECIFIC.get(domain, {}))
    result, n = [], 0
    for name in sorted(sections.keys(), key=lambda s: int(s.split(".")[0])):
        qs = []
        for text, practice, weight, flag in sections[name]:
            n += 1
            qs.append({"id": f"Q{n:03d}", "text": text, "practice": practice,
                       "weight": weight, "flag": flag, "answer": "", "comment": ""})
        result.append((name, qs))
    return result
