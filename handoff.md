# Handoff — transition progressive du nom du projet

## Objectif

Remplacer progressivement le nom public `benchmark-mac` par `PerfComparator`,
un nom réellement multiplateforme, sans casser les installations existantes ni la compatibilité
des rapports JSON.

Ne traiter aucun autre chantier pendant cette session : ni catalogue public de
rapports, ni nouveaux benchmarks, ni CI générale, ni changement de protocole.

## État courant

- Branche de travail : `feat/project-rename`, créée depuis `main` au commit
  `77e97cf`.
- Stable publiée : `v0.3.2`, taguée sur `57c7598` et marquée `Latest`.
- Dépôt actuel : `https://github.com/frchalaoux/benchmark-mac`.
- Candidate locale : `0.4.0.dev0`.
- Paquet candidat : `perfcomparator`.
- Commande principale candidate : `perfcomparator`.
- Alias de transition : `benchmark-mac`.
- Module Python interne : `benchmark_mac`.
- La suite fonctionne sous macOS, Windows et Linux; son nom actuel est donc
  devenu trop restrictif.
- Nom retenu et appliqué localement : `PerfComparator`; dépôt, paquet et commande
  cibles : `perfcomparator`.
- Le dépôt distant porte encore le nom `benchmark-mac`; aucune opération
  distante liée au renommage n'a été effectuée.

## Décisions déjà prises

1. Procéder par transition douce dans la série `0.4.0`, en commençant par
   `0.4.0.dev0`.
2. Le nom `PerfComparator` a été vérifié comme disponible sur PyPI, dans
   l'espace GitHub du projet et en `.com`; aucune réservation n'a été faite.
3. Renommer l'identité publique, le dépôt, le paquet et la commande de façon
   coordonnée.
4. Conserver temporairement `benchmark-mac` comme alias de commande afin de ne
   pas casser les usages existants.
5. Garder dans un premier temps le module interne `benchmark_mac`; son renommage
   apporterait peu de valeur et augmenterait fortement le risque.
6. Ne modifier ni `protocol_version` (`0.3.0`) ni `schema_version` (`4`) pour un
   simple changement de nom.
7. Préserver tous les anciens tags et vérifier que leurs installateurs restent
   utilisables après le renommage du dépôt.
8. Ne réaliser aucune opération distante sans annoncer toute la séquence et
   obtenir une confirmation explicite actuelle.

## Travail local réalisé

- identité publique, distribution et commande principale renommées ;
- alias `benchmark-mac` conservé et module `benchmark_mac` inchangé ;
- version portée à `0.4.0.dev0`, sans changement du protocole `0.3.0` ni du
  schéma 4 ;
- installateurs adaptés au nouveau dépôt et capables de remplacer proprement
  l'ancien outil enregistré par `uv` ;
- CLI, rapports HTML, documentation, tests et verrou adaptés ;
- rapports historiques et liens des versions `0.3.x` préservés.

## Validations acquises

- `ruff format --check` et `ruff check` réussis ;
- 54 tests réussis ;
- wheel et archive source `perfcomparator-0.4.0.dev0` construites et inspectées ;
- les deux commandes sont présentes dans la wheel ;
- aucun rapport utilisateur n'est inclus dans les distributions ;
- migration réelle isolée depuis l'archive distante `v0.3.2` réussie sur macOS :
  un seul outil `perfcomparator 0.4.0.dev0` enregistré, avec les commandes
  `perfcomparator` et `benchmark-mac` fonctionnelles ;
- installateur PowerShell vérifié par tests statiques, faute de PowerShell local.

## Prochaine action concrète

Après le commit local, annoncer précisément la séquence distante proposée
(publication de la branche, pull request, renommage du dépôt et future
préversion) puis attendre une confirmation explicite actuelle. Mettre à jour le
remote local et les liens publiés seulement au moment coordonné du renommage.

## Critères d'acceptation

- La nouvelle commande installe et exécute toute la suite.
- `benchmark-mac` continue de fonctionner comme alias pendant la transition.
- Les anciens rapports restent comparables avec les nouveaux lorsque leur
  protocole est compatible.
- Les anciens tags ne sont ni déplacés ni recréés.
- Les installateurs macOS/Linux et Windows utilisent le bon dépôt et la bonne
  version.
- Le README indique clairement le nouveau nom et la période de compatibilité de
  l'ancien nom.
- Les tests, la construction des distributions et le smoke test de migration
  depuis la stable distante réussissent.

## Points de vigilance

- Le renommage du dépôt GitHub est une opération distante et exige une
  confirmation explicite.
- Ne pas confondre nom du dépôt, nom de distribution Python, commande CLI et
  module importable.
- Vérifier l'aide réelle des commandes avant les tests; ne pas deviner leurs
  options.
- Éviter une pull request documentaire de close-out : conserver dans Git
  uniquement les informations durables.
