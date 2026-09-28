# PerfComparator

PerfComparator, anciennement `benchmark-mac`, est une suite locale pour comparer
les performances de plusieurs machines avant un achat. Elle
utilise les mêmes scénarios, paramètres et version exacte de CPython sur macOS,
Windows et Linux, puis produit des rapports JSON portables.

La version stable `v0.3.2` mémorise le protocole de mesure indépendamment de la
version de la suite. Elle conserve les 16 benchmarks et le protocole `0.3.0` de
la stable précédente, ainsi que la comparaison CLI de plusieurs machines.

## Développement non publié `0.4.0.dev1`

L'arbre de développement prépare l'export anonymisé et la validation locale des
rapports destinés au catalogue communautaire. Cette version n'est pas encore
taguée : les installateurs continuent donc volontairement de cibler la
préversion publiée `v0.4.0.dev0`.

## Préversion publiée `v0.4.0.dev0`

La préversion `0.4.0.dev0` introduit le nom **PerfComparator**, le paquet
`perfcomparator` et la commande principale `perfcomparator`. La commande
`benchmark-mac` reste disponible comme alias pendant la transition. Le module
Python interne reste `benchmark_mac`, et le protocole de mesure reste `0.3.0` :
les rapports demeurent compatibles avec ceux de la famille `0.3.x` reconnue.
L'installateur remplace aussi l'ancien paquet enregistré par `uv`.

Ses installateurs sont :

```bash
curl -LsSf https://raw.githubusercontent.com/frchalaoux/perfcomparator/v0.4.0.dev0/install.sh | sh
```

```powershell
irm https://raw.githubusercontent.com/frchalaoux/perfcomparator/v0.4.0.dev0/install.ps1 | iex
```

## Versions publiées

Consulter [tous les tags disponibles](https://github.com/frchalaoux/perfcomparator/tags)
ou choisir une version ci-dessous.

| Version | Canal | À choisir pour | État |
| --- | --- | --- | --- |
| [`v0.4.0.dev0`](https://github.com/frchalaoux/perfcomparator/tree/v0.4.0.dev0) | Développement publié | Tester le changement de nom et la migration | Préversion |
| [`v0.3.2`](https://github.com/frchalaoux/perfcomparator/tree/v0.3.2) | Stable actuelle | Conserver et comparer explicitement les protocoles | Version recommandée |
| [`v0.3.2.dev0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.3.2.dev0) | Développement antérieur | Reproduire la validation du protocole mémorisé | Préversion publiée |
| [`v0.3.1`](https://github.com/frchalaoux/benchmark-mac/tree/v0.3.1) | Stable antérieure | Comparer clairement plusieurs machines | Remplacée par `v0.3.2` |
| [`v0.3.1.dev0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.3.1.dev0) | Développement antérieur | Reproduire la validation de la correction CLI | Préversion publiée |
| [`v0.3.0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.3.0) | Stable antérieure | Comparer CPU, mémoire, stockage, applications et GPU | Remplacée par `v0.3.1` |
| [`v0.3.0.dev2`](https://github.com/frchalaoux/benchmark-mac/tree/v0.3.0.dev2) | Développement antérieur | Reproduire les validations de la stable | Convention des tags explicitée |
| [`v0.3.0.dev1`](https://github.com/frchalaoux/benchmark-mac/tree/v0.3.0.dev1) | Développement antérieur | Tester les corrections Windows | Corrige l'installation et le PID 0 sous Windows |
| [`v0.3.0.dev0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.3.0.dev0) | Développement antérieur | Reproduire une campagne existante | Problèmes d'installation et de contrôle préalable sous Windows |
| [`v0.2.1`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.1) | Stable antérieure | Reproduire une campagne sans GPU | Remplacée par `v0.3.0` |
| [`v0.2.0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.0) | Stable antérieure | Reproduire une campagne existante | Échec SQLite possible sous Windows |
| [`v0.2.0.dev2`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.0.dev2) | Développement archivé | Reproduire une campagne de préversion | Base fonctionnelle de `v0.2.0` |
| [`v0.2.0.dev1`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.0.dev1) | Développement archivé | Reproduire une campagne existante | Comparaison multicœur trop stricte |
| [`v0.2.0.dev0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.0.dev0) | Développement obsolète | Reproduire une ancienne campagne | Installateur incorrect par défaut |
| [`v0.1.0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.1.0) | Stable antérieure | Reproduire les premiers rapports simples | Remplacée par `v0.2.1` |

La [fiche détaillée des versions](docs/versions.md) indique les différences,
les commandes d'installation pour chaque système et les précautions de mise à
jour. Les fonctionnalités décrites ci-dessous correspondent à la série `0.3` ;
les différences avec la stable sont signalées explicitement.

## Version stable `v0.3.2`

`v0.3.2` mémorise séparément `suite_version` et `protocol_version` dans les
nouveaux rapports. Elle conserve le protocole de mesure `0.3.0` et reste
compatible avec les rapports historiques reconnus de cette famille.

Sur macOS ou Linux :

```bash
curl -LsSf https://raw.githubusercontent.com/frchalaoux/perfcomparator/v0.3.2/install.sh | sh
```

Sous Windows, dans PowerShell :

```powershell
irm https://raw.githubusercontent.com/frchalaoux/perfcomparator/v0.3.2/install.ps1 | iex
```

Le contrôle `benchmark-mac --version` doit afficher `benchmark-mac 0.3.2`.

## Couverture actuelle

- **CPU** : entiers et flottants mono-cœur, SHA-256, compression zlib et calcul multicœur ;
- **mémoire** : bande passante de copie séquentielle ;
- **stockage** : lectures et écritures séquentielles et aléatoires de 4 Kio ;
- **applications** : traitement JSON et charge SQLite ;
- **GPU** : calcul FP32, bande passante, filtre d'image et rendu raster hors écran ;
- **inventaire** : modèle, OS, CPU, mémoire, GPU, disque et environnement Python.

Les mesures GPU utilisent `wgpu-py`, une petite couche WebGPU qui choisit Metal,
Direct3D 12 ou Vulkan selon le système. Elles ne nécessitent ni Blender, ni
fenêtre graphique, ni scène externe.

Une machine peut exposer plusieurs GPU. `perfcomparator info` les numérote ; par
défaut, la suite choisit d'abord un GPU dédié, puis un GPU intégré. Pour mesurer
chaque carte séparément, produire un rapport par indice :

```bash
perfcomparator run --group gpu --gpu 0 --label "Portable — GPU 0"
perfcomparator run --group gpu --gpu 1 --label "Portable — GPU 1"
```

Le GPU effectivement choisi est annoncé avant la campagne et enregistré dans
chaque résultat GPU.

Dans une machine virtuelle sans accélération graphique transmise, WebGPU peut
n'exposer que `Microsoft Basic Render Driver`, classé `CPU`. Ce moteur logiciel
est signalé et refusé pour éviter de présenter un score CPU comme une performance
GPU. Les douze autres benchmarks continuent normalement.

## Installation depuis GitHub

Python n'a pas besoin d'être installé. Le script installe `uv`, puis `uv`
télécharge et gère CPython 3.14.4 avant d'installer l'application.

### Préversion antérieure `v0.3.1.dev0`

Cette préversion affiche, pour chaque machine candidate, son propre écart et sa
propre conclusion dans le détail CLI. La première machine reste explicitement
la référence 100.

Sur macOS ou Linux :

```bash
curl -LsSf https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.3.1.dev0/install.sh | sh
```

Sous Windows, dans PowerShell :

```powershell
irm https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.3.1.dev0/install.ps1 | iex
```

Le contrôle `benchmark-mac --version` doit afficher
`benchmark-mac 0.3.1.dev0`.

### Version stable `v0.3.1`

Sur macOS ou Linux :

```bash
curl -LsSf https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.3.1/install.sh | sh
```

Sous Windows, dans PowerShell :

```powershell
irm https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.3.1/install.ps1 | iex
```

Cette version installe CPython 3.14.4, met automatiquement à niveau un ancien
`uv` si nécessaire et remplace toute version précédente de l'outil. Vérifier
l'installation avec `benchmark-mac --version`, qui doit afficher
`benchmark-mac 0.3.1`.

### Préversion antérieure `v0.3.0.dev2`

Cette préversion reste disponible pour reproduire les campagnes de validation
de la stable. Sous Windows, la mise à niveau de `uv` s'exécute dans un processus
enfant et le pseudo-processus PID 0 est ignoré.

> **Convention des préversions :** les tags suivent la forme `vX.Y.Z.devK`.
> Ce tag s'écrit donc exactement `v0.3.0.dev2`. Les points font partie
> du nom Git et doivent être conservés dans les URL et les commandes.

Sur macOS ou Linux :

```bash
curl -LsSf https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.3.0.dev2/install.sh | sh
```

Sous Windows, dans PowerShell :

```powershell
irm https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.3.0.dev2/install.ps1 | iex
```

L'installateur emploie `uv tool install --reinstall` : la même commande permet
donc aussi de passer d'une version antérieure à cette préversion. Vérifier le
résultat avec `benchmark-mac --version`, qui doit afficher
`benchmark-mac 0.3.0.dev2`.

`v0.2.0.dev0` reste téléchargeable pour la reproductibilité, mais son
installateur nécessite un contournement détaillé dans la
[fiche des versions](docs/versions.md#installer-lancienne-v020dev0).

Vérifier ensuite l'installation :

```bash
perfcomparator --version
uv tool list
perfcomparator list
perfcomparator compare --help
```

Avec une version `0.3.x`, employer l'ancienne commande `benchmark-mac`.

## Installation depuis le dossier de développement

```bash
./install.sh
```

ou simplement :

```bash
uv sync
uv run perfcomparator list
```

## Lancer les benchmarks

Avant de lancer une campagne comparable :

1. brancher le portable au secteur et sélectionner le mode de performances à
   utiliser sur toutes les machines ;
2. fermer navigateurs, synchronisations, mises à jour, jeux, rendus, machines
   virtuelles et autres tâches lourdes ;
3. attendre quelques minutes après le démarrage ou une charge importante, dans
   une pièce aux conditions aussi proches que possible ;
4. conserver le même profil, le même nombre de passages et, pour le stockage,
   le même type d'emplacement `--work-dir`.

Au démarrage, PerfComparator observe pendant une seconde la charge CPU, la
mémoire, l'échange et les processus actifs. Il affiche un avertissement si le
point de départ paraît éloigné du repos, puis poursuit la mesure. Ce contrôle
ponctuel aide à repérer une mauvaise campagne ; il ne peut pas prouver que la
machine a atteint son potentiel maximal.

Toute la suite, avec le profil standard :

```bash
perfcomparator run --label "MacBook Pro M4 Pro"
```

Chaque test est exécuté trois fois par défaut et le rapport conserve la médiane,
le minimum, le maximum et la dispersion. Le nombre de passages est réglable :

```bash
perfcomparator run --repeat 5 --profile thorough
```

Un groupe ou plusieurs groupes :

```bash
perfcomparator run --group cpu
perfcomparator run --group memory --group storage --profile thorough
perfcomparator run --group gpu --profile standard
```

Un ou plusieurs tests individuels :

```bash
perfcomparator run cpu.integer
perfcomparator run cpu.hash memory.copy application.sqlite --profile quick
```

Le catalogue complet est fourni par `perfcomparator list`. La commande
`perfcomparator describe cpu.hash` affiche le protocole, les limites et les
références d'un test. Les profils `quick`, `standard` et `thorough` augmentent
progressivement les durées et volumes.

## Exporter un rapport public

Cette commande appartient au développement non publié `0.4.0.dev1`.

Un rapport de campagne privé contient des informations de diagnostic qui ne
doivent pas être publiées directement. La commande `export-public` reconstruit
un fichier distinct depuis une liste blanche, localement et sans envoi réseau :

```bash
perfcomparator export-public data/results/benchmark_….json \
  --output rapport-public.json \
  --accept-cc0
```

`--accept-cc0` confirme que les données exportées pourront être diffusées sous
licence CC0 1.0. L'export retire notamment le label libre, la date précise, les
chemins, processus, PID, messages d'échec, versions détaillées du système et
informations de disque. Il porte un identifiant de contenu déterministe et la
mention `community-unverified` : l'anonymisation et la validation du format ne
certifient jamais les performances déclarées.

Le [contrat complet du format public](docs/format-rapport-public.md) précise les
données conservées et les limites de confidentialité.

Un fichier reçu se contrôle localement avant toute utilisation :

```bash
perfcomparator validate-public rapport-public.json
```

Cette validation borne la taille à 2 Mio, refuse les champs inconnus et vérifie
le protocole, les unités, paramètres, échantillons, dispersions et l'identifiant
de contenu. Elle ne constitue pas une certification des scores.

## Comparer plusieurs machines

Copier les rapports JSON dans un même dossier, puis utiliser le premier comme
référence :

```bash
perfcomparator compare mac-m4.json pc-ryzen.json
```

Pour obtenir le rapport visuel autonome et adapter le résultat à ses usages :

```bash
perfcomparator compare mac-m4.json pc-ryzen.json pc-intel.json \
  --weight developpement=50 \
  --weight creation=30 \
  --weight quotidien=20 \
  --html comparaison.html
```

Le premier rapport est la référence 100. Le HTML traduit les rapports en
indices, écarts qualitatifs et temps équivalents. Il contient des barres, un
graphique d'écart pour deux machines, une carte thermique pour plusieurs
machines, des chronologies et un résumé en langage courant.

La comparaison exige des versions de protocole compatibles, le même profil et
la même version de Python. `0.3.0.dev1`, `0.3.0.dev2`, `0.3.0`, `0.3.1.dev0`,
`0.3.1`, `0.3.2.dev0`, `0.3.2`, `0.4.0.dev0` et `0.4.0.dev1` sont compatibles
entre elles. Les rapports sont
enregistrés dans `data/results/` par défaut. Les nouvelles campagnes conservent
séparément la version exacte de la suite (`suite_version`) et celle du protocole
de mesure (`protocol_version`). Deux versions différentes de la suite restent
donc comparables lorsqu'elles déclarent le même protocole. Pour les anciens
rapports sans ce champ, la table de compatibilité historique reste appliquée.
Une différence dont les plages min–max se chevauchent est signalée comme non
concluante. Les rapports `0.2.x` et `0.3.x` ne sont pas directement comparables,
car le catalogue, les scénarios et le schéma JSON ont évolué.

## Développement

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv build
```

Consulter la [documentation](DOCUMENTATION.md) pour le protocole de mesure et
l'architecture du projet.
