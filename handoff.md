# Handoff — PerfComparator et catalogue communautaire

État vérifié le 1er octobre 2026. Ce document est un point de reprise, pas une
source de vérité pour les branches, tags, releases ou pull requests : vérifier
leur état distant avant toute reprise ou publication.

## Objectif

Maintenir le parcours de contribution aux résultats communautaires :
PerfComparator produit un export public anonymisé, le catalogue valide les
rapports soumis par pull request, puis construit son index au déploiement et
permet leur consultation et leur téléchargement.

## Dépôts et état vérifié

- **PerfComparator** — [`frchalaoux/perfcomparator`](https://github.com/frchalaoux/perfcomparator), branche par défaut `main`, commit
  `ba962a033deb1af2c69652f02e013f6c2abfcc7f` (fusion de la PR #23). La stable
  publiée et marquée Latest est [`v0.4.0`](https://github.com/frchalaoux/perfcomparator/releases/tag/v0.4.0).
- **Catalogue** — [`frchalaoux/perfcomparator-results`](https://github.com/frchalaoux/perfcomparator-results), branche par défaut `main`, commit
  `d03e00dbe9f25f7e9a01e772a792c1cd44fa6960` (fusion de la PR #16). Le site est
  [frchalaoux.github.io/perfcomparator-results](https://frchalaoux.github.io/perfcomparator-results/).
- **Documentation source en cours** — PR #24, branche `docs/multiboot-readme`
  vers `main`, ouverte et indiquée `CLEAN` lors du contrôle. Elle clarifie le
  multiboot et documente la stratégie de publication. Actualiser son état avant
  toute action : elle peut avoir été fusionnée ou modifiée depuis ce relevé.

## Fonctionnement du catalogue

- Les rapports publics validés sous `reports/` sont la source de vérité ; ne
  pas réintroduire d'index versionné. Le déploiement génère l'index du site.
- Une contribution normale ajoute un rapport JSON par PR. L'automatisation
  valide le rapport et peut fusionner ce type précis de PR ; le workflow ne
  certifie pas les performances.
- Les rapports publiés sont publics et réputés non certifiés. Ne jamais y
  inclure un rapport privé, un numéro de série, un UUID matériel, un nom d'hôte,
  un chemin local ou toute autre donnée identifiante.
- Le dépôt catalogue possède son propre cycle de changements ; ne pas mélanger
  ses rapports ou sa documentation à une release du logiciel sans raison
  explicite.

## Reprise

1. Vérifier les arbres de travail et les branches dans les deux dépôts.
2. Vérifier sur GitHub les PR, tags, releases et déploiements concernés ; ce
   handoff peut être périmé.
3. Reprendre la prochaine tâche explicitement demandée. À l'état du présent
   relevé, la seule action distante connue est la revue de la PR #24 ; aucune
   action n'est implicitement autorisée par ce document.

Respecter les règles durables de publication dans `AGENTS.md` et la stratégie
détaillée dans [`docs/strategie-publication.md`](docs/strategie-publication.md).
Toute écriture distante requiert une confirmation explicite et actuelle après
annonce de ses cibles précises. Après confirmation, arrêter au premier échec ou
état inattendu.
