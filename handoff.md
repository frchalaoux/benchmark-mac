# Handoff — transition progressive du nom du projet

## Objectif unique de la prochaine session

Remplacer progressivement le nom public `benchmark-mac` par un nom réellement
multiplateforme, sans casser les installations existantes ni la compatibilité
des rapports JSON.

Ne traiter aucun autre chantier pendant cette session : ni catalogue public de
rapports, ni nouveaux benchmarks, ni CI générale, ni changement de protocole.

## État de départ

- Branche de travail : `feat/project-rename`, créée depuis `main` au commit
  `77e97cf`.
- Stable publiée : `v0.3.2`, taguée sur `57c7598` et marquée `Latest`.
- Dépôt actuel : `https://github.com/frchalaoux/benchmark-mac`.
- Paquet installable : `benchmark-mac`.
- Commande actuelle : `benchmark-mac`.
- Module Python interne : `benchmark_mac`.
- La suite fonctionne sous macOS, Windows et Linux; son nom actuel est donc
  devenu trop restrictif.
- Aucun changement de nom n'a encore été effectué.

## Décisions déjà prises

1. Procéder par transition douce, vraisemblablement dans la série `0.4.0`.
2. Choisir et vérifier le nouveau nom avant toute modification de code ou
   opération distante.
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

## Prochaine action concrète

Proposer une courte liste de noms multiplateformes, puis vérifier pour chaque
candidat :

- disponibilité du dépôt GitHub;
- disponibilité et éventuels conflits sur PyPI;
- collisions évidentes avec une marque ou un logiciel existant;
- lisibilité comme commande de terminal;
- capacité à nommer aussi un futur catalogue communautaire de rapports.

Présenter ensuite les résultats à l'utilisateur et attendre son choix. Poursuivre
ensuite la migration sur la branche `feat/project-rename` déjà créée.

## Stratégie de migration à appliquer après le choix

- Ajouter la nouvelle commande tout en conservant l'alias `benchmark-mac`.
- Adapter le nom du paquet, les installateurs, les messages CLI, les rapports
  HTML, les tests et la documentation.
- Mettre à jour les URL GitHub et le remote local au moment approprié.
- Vérifier les installations nouvelle et historique avec un seul parcours de
  validation automatisé et idempotent.
- Préparer une publication coordonnée, puis demander une confirmation unique
  couvrant exactement les opérations distantes annoncées.

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
- Les tests, la construction des distributions et un unique smoke test distant
  réussissent.

## Points de vigilance

- Le renommage du dépôt GitHub est une opération distante et exige une
  confirmation explicite.
- Ne pas confondre nom du dépôt, nom de distribution Python, commande CLI et
  module importable.
- Vérifier l'aide réelle des commandes avant les tests; ne pas deviner leurs
  options.
- Éviter une pull request documentaire de close-out : conserver dans Git
  uniquement les informations durables.
