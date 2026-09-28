# Handoff — catalogue communautaire PerfComparator

## Objectif unique de la prochaine session

Concevoir la première version sobre d'un catalogue communautaire de rapports
PerfComparator hébergé sur GitHub et affiché avec GitHub Pages.

Le site reste statique : les contributions passent par des pull requests, puis
une automatisation valide les JSON et régénère l'index. Aucun serveur payant,
compte utilisateur ou base de données n'est prévu pour cette première version.

Commencer par l'export public anonymisé dans le CLI. Ne pas créer le dépôt
communautaire distant avant d'avoir défini et testé ce format.

## État du projet source

- Dépôt : `https://github.com/frchalaoux/perfcomparator`.
- Branche distante par défaut : `main` au commit `a11eab9`.
- Branche locale préparée pour ce chantier : `feat/community-report-catalog`.
- Stable actuelle : `v0.3.2`, marquée `Latest`.
- Préversion du changement de nom : `v0.4.0.dev0`, taguée sur `d4fee69`.
- Version locale du chantier catalogue : `0.4.0.dev1`, non taguée et non publiée.
- Nom public et commande principale : `PerfComparator` / `perfcomparator`.
- Alias conservé pendant la transition : `benchmark-mac`.
- Module Python interne conservé : `benchmark_mac`.
- Protocole de mesure : `0.3.0` ; schéma JSON : `4`.
- Le changement de nom a été validé sous macOS, Ubuntu 24.04 et Windows 10.
- Aucune pull request n'est ouverte.

## État local du chantier

Le premier livrable est enregistré dans le commit local `9b11ae1` :

- le modèle fermé `perfcomparator-public-report` version 1 ;
- un export fondé sur une liste blanche et un identifiant SHA-256 déterministe ;
- la commande locale `perfcomparator export-public SOURCE --output DESTINATION
  --accept-cc0` ;
- le consentement explicite à la licence de données `CC0-1.0` ;
- le marquage obligatoire `community-unverified` ;
- la validation du schéma privé 4, du protocole 0.3.0, des unités, paramètres,
  passages, résultats et échecs ;
- la documentation de la politique de confidentialité et de ses limites ;
- des tests de non-divulgation des labels, dates, chemins, PID, processus,
  avertissements, messages d'échec et détails système privés.

La seconde tranche locale non encore committée ajoute :

- `perfcomparator validate-public SOURCE` ;
- une limite de 2 Mio avant lecture ;
- la validation sémantique complète des systèmes, benchmarks, unités,
  paramètres, répétitions, échantillons, médianes, bornes et dispersions ;
- le recalcul et la vérification de l'identifiant de contenu ;
- le refus des chemins privés et des données non canoniques.

Validations acquises sur cet arbre : Ruff réussi, 73 tests réussis, export puis
validation des 12 rapports locaux macOS/Windows compatibles, et campagne Linux
x86_64 réelle sous CPython 3.14.4 avec export puis validation réussis. Les
rapports Linux privé et public sont restés dans un répertoire temporaire hors
Git. Aucun fichier privé n'a été publié ou versionné.

## Travail PyPI différé

La publication PyPI est volontairement mise de côté. Elle n'est pas nécessaire
au catalogue ni aux installateurs GitHub.

Le travail préparatoire reste sauvegardé localement sur
`chore/pypi-trusted-publishing` :

- `27b8a5a` — workflow Trusted Publishing ;
- `8d142bf` — ancien handoff PyPI.

Cette branche n'a pas été poussée. Ne pas la fusionner ni reprendre PyPI sans
une nouvelle demande explicite de l'utilisateur.

## Architecture recommandée

Un dépôt séparé local, nom de travail `perfcomparator-results`, a été créé dans
`../perfcomparator-results` afin de ne pas alourdir le dépôt du logiciel. Ses
étapes sont conservées dans son propre historique Git ; aucun remote n'est
configuré.

```text
perfcomparator-results/
├── reports/
│   └── protocol-0.3.0/
│       └── <identifiant-sha256>.json
├── catalog/
│   └── index.json
├── scripts/
│   └── build_catalog.py
└── tests/
```

Le rangement plat par protocole et identifiant évite de classer arbitrairement
les machines combinant plusieurs fabricants. Le nom du dépôt reste à vérifier
avant toute création distante.

Le dépôt local délègue la validation sémantique à `perfcomparator
validate-public`, contrôle l'emplacement, le nom et l'unicité des rapports, puis
génère un index minimal et déterministe. Ruff, 4 tests, la validation du
catalogue vide et le contrôle de son index réussissent.

Les commits locaux suivants ajoutent une première page statique sans framework,
un artefact Pages autonome et deux workflows préparés mais non publiés :
validation des pull requests en lecture seule et déploiement depuis `main`.
Recherche, filtres, compteurs, téléchargements et avertissement « rapports
communautaires non certifiés » sont couverts par quatre tests JavaScript. Un
smoke test HTTP a confirmé la page, le CSS, les modules et l'index.

Fonctionnement visé :

1. `perfcomparator export-public` produit un JSON anonymisé.
2. L'utilisateur ajoute ce fichier au dépôt communautaire par une pull request.
3. Un workflow vérifie le rapport sans secret et avec un jeton en lecture seule.
4. Après fusion, l'index et le site GitHub Pages sont régénérés.
5. Chacun recherche et télécharge seulement les rapports qui l'intéressent.
6. Les rapports téléchargés restent comparables localement avec sa machine.

GitHub Pages héberge des fichiers HTML, CSS et JavaScript statiques et peut les
déployer par GitHub Actions :
https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages

## Première étape indispensable : export public anonymisé

Les rapports actuels ne doivent pas être publiés tels quels. Ils peuvent
contenir des informations identifiantes ou trop détaillées :

- `python_executable`, dont le chemin peut révéler un nom d'utilisateur ;
- PID et noms des processus actifs ;
- label libre fourni par l'utilisateur ;
- date et heure précises ;
- détails du système non nécessaires à la comparaison.

Créer un format public fondé sur une **liste blanche**, jamais sur une liste de
champs à retirer. Conserver uniquement ce qui est nécessaire :

- identifiant et version du format public ;
- `protocol_version`, `schema_version` et `suite_version` ;
- processeur, mémoire, GPU et système sous une forme normalisée ;
- profil, répétitions et paramètres comparatifs utiles ;
- résultats, unités, valeurs brutes ou dispersion nécessaires à l'analyse ;
- état global de la campagne et échecs de benchmarks, sans processus ni chemin.

À décider explicitement avant implémentation :

- précision temporelle conservée, éventuellement mois seul ou aucune date ;
- génération d'un identifiant de rapport non traçant ;
- traitement du label libre : suppression, remplacement ou validation stricte ;
- informations exactes sur le système et le matériel autorisées ;
- licence associée au rapport public et consentement explicite de l'auteur.

Ajouter des tests de non-divulgation : un chemin utilisateur, un PID, un nom de
processus et un label sensible injectés dans un rapport privé ne doivent jamais
apparaître dans l'export public.

## Validation automatique des contributions

Le workflow du futur dépôt doit contrôler au minimum :

- schéma et version du format public ;
- protocole reconnu ;
- cohérence des benchmarks, unités, paramètres et répétitions ;
- absence de champs privés ou inconnus ;
- taille maximale du fichier ;
- unicité de l'identifiant et du contenu ;
- conditions de mesure et avertissements ;
- résultats manquants ou en échec ;
- nom et emplacement normalisés du fichier.

Pour les contributions issues de forks, utiliser `pull_request`, sans secret et
avec des permissions en lecture seule. Ne pas utiliser `pull_request_target`
pour exécuter du contenu non fiable :
https://docs.github.com/en/actions/reference/security/secure-use

Le workflow valide mais ne certifie pas les performances. Un rapport peut être
falsifié. Le site doit afficher « rapport communautaire non certifié », garder
le lien vers la pull request d'origine et ne jamais présenter le catalogue
comme un classement officiel.

## Catalogue et distribution sobres

Le site statique pourra charger `catalog/index.json`, filtrer localement les
machines et proposer le téléchargement direct des JSON.

Évolution CLI envisagée, hors première étape :

```text
perfcomparator catalog search "Mac mini M4"
perfcomparator catalog download ID
perfcomparator compare mon-rapport.json rapport-communautaire.json
```

Le CLI doit télécharger uniquement l'index léger puis les rapports sélectionnés,
jamais cloner toute la base.

Ne pas utiliser les artefacts GitHub Actions comme stockage permanent : leur
durée de conservation est limitée. Les rapports acceptés doivent être des
fichiers Git normaux au début :
https://docs.github.com/en/actions/how-tos/manage-workflow-runs/download-workflow-artifacts

GitHub recommande de limiter la taille des dépôts et GitHub Pages recommande un
site et une source sous 1 Go. Si le volume devient important, déplacer les JSON
vers un stockage d'objets et conserver seulement l'index sur GitHub :

- https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits
- https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits

## Prochaine action concrète

Préparer le workflow `pull_request` en lecture seule dès qu'une révision
publiquement installable de PerfComparator contient `validate-public`, puis le
déploiement GitHub Pages. Ne créer aucun dépôt, aucune branche distante et aucun
déploiement sans confirmation explicite actuelle.

## Critères d'acceptation du premier livrable

- Aucun chemin utilisateur, PID, processus actif ou label libre non validé.
- Format public versionné et documenté.
- Protocole et données comparatives suffisants pour réutiliser le moteur actuel.
- Export déterministe à partir du même rapport source.
- Refus clair d'un rapport invalide ou trop ancien pour être exporté sûrement.
- Tests couvrant explicitement les données sensibles.
- Aucun envoi réseau effectué par `export-public`.

## Fichiers clés

- `src/benchmark_mac/models.py` : schéma privé actuel.
- `src/benchmark_mac/cli.py` : future commande `export-public`.
- `src/benchmark_mac/comparison.py` : données requises pour comparer.
- `src/benchmark_mac/repository.py` : lecture et écriture atomique des JSON.
- `tests/` : tests de schéma, CLI et non-divulgation à ajouter.
- `data/results/` : rapports locaux privés, ignorés et à ne jamais versionner.

## Points de vigilance

- Aucune opération distante sans annonce précise puis confirmation explicite et
  actuelle de l'utilisateur.
- Ne jamais publier les rapports locaux existants ni les HTML de comparaison.
- Ne jamais considérer une validation de schéma comme une preuve d'authenticité.
- Ne pas collecter d'adresse IP, compte, télémétrie ou identifiant matériel.
- Ne pas réutiliser de mémoire ou de conventions SMB dans ce projet.
- Préserver la compatibilité des rapports et le protocole `0.3.0` pendant ce
  chantier ; le format public possède sa propre version.
