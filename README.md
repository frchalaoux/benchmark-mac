# benchmark-mac

Suite locale pour comparer les performances de Mac et de PC avant un achat. Elle
utilise les mêmes scénarios, paramètres et version exacte de CPython sur macOS,
Windows et Linux, puis produit des rapports JSON portables.

La préversion `v0.3.0.dev1` ajoute quatre benchmarks GPU WebGPU légers et un
contrôle de l'état de la machine avant chaque campagne. Elle corrige aussi
l'installation et le contrôle préalable sous Windows. La stable recommandée
reste `v0.2.1`.

## Versions publiées

Consulter [tous les tags disponibles](https://github.com/frchalaoux/benchmark-mac/tags)
ou choisir une version ci-dessous.

| Version | Canal | À choisir pour | État |
| --- | --- | --- | --- |
| [`v0.3.0.dev1`](https://github.com/frchalaoux/benchmark-mac/tree/v0.3.0.dev1) | Développement actuel | Tester les GPU et le contrôle préalable | Corrige l'installation et le PID 0 sous Windows |
| [`v0.3.0.dev0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.3.0.dev0) | Développement antérieur | Reproduire une campagne existante | Problèmes d'installation et de contrôle préalable sous Windows |
| [`v0.2.1`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.1) | Stable | Comparer des machines, notamment sous Windows | Version recommandée |
| [`v0.2.0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.0) | Stable antérieure | Reproduire une campagne existante | Échec SQLite possible sous Windows |
| [`v0.2.0.dev2`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.0.dev2) | Développement archivé | Reproduire une campagne de préversion | Base fonctionnelle de `v0.2.0` |
| [`v0.2.0.dev1`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.0.dev1) | Développement archivé | Reproduire une campagne existante | Comparaison multicœur trop stricte |
| [`v0.2.0.dev0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.0.dev0) | Développement obsolète | Reproduire une ancienne campagne | Installateur incorrect par défaut |
| [`v0.1.0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.1.0) | Stable antérieure | Reproduire les premiers rapports simples | Remplacée par `v0.2.1` |

La [fiche détaillée des versions](docs/versions.md) indique les différences,
les commandes d'installation pour chaque système et les précautions de mise à
jour. Les fonctionnalités décrites ci-dessous correspondent à la série `0.3` ;
les différences avec la stable sont signalées explicitement.

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

Une machine peut exposer plusieurs GPU. `benchmark-mac info` les numérote ; par
défaut, la suite choisit d'abord un GPU dédié, puis un GPU intégré. Pour mesurer
chaque carte séparément, produire un rapport par indice :

```bash
benchmark-mac run --group gpu --gpu 0 --label "Portable — GPU 0"
benchmark-mac run --group gpu --gpu 1 --label "Portable — GPU 1"
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

### Version stable `v0.2.1`

Sur macOS ou Linux :

```bash
curl -LsSf https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.2.1/install.sh | sh
```

Sous Windows, dans PowerShell :

```powershell
irm https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.2.1/install.ps1 | iex
```

Cette version corrige l'échec `WinError 32` du benchmark SQLite sous Windows en
fermant explicitement la base avant la suppression du répertoire temporaire.

Si Windows possède encore un ancien `uv` qui ne connaît pas CPython 3.14.4,
mettre d'abord `uv` à niveau avec la procédure indiquée dans la
[fiche des versions](docs/versions.md#ancien-uv-sous-windows), puis relancer
l'installation de `v0.2.1`.

### Version de développement `v0.3.0.dev1`

Cette préversion est destinée à valider les nouveaux tests GPU et le contrôle
de l'état initial avant une future stable. Sous Windows, la mise à niveau de
`uv` s'exécute dans un processus enfant et le pseudo-processus PID 0 est ignoré.

Sur macOS ou Linux :

```bash
curl -LsSf https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.3.0.dev1/install.sh | sh
```

Sous Windows, dans PowerShell :

```powershell
irm https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.3.0.dev1/install.ps1 | iex
```

L'installateur emploie `uv tool install --reinstall` : la même commande permet
donc aussi de passer d'une version antérieure à cette préversion. Vérifier le
résultat avec `benchmark-mac --version`, qui doit afficher
`benchmark-mac 0.3.0.dev1`.

`v0.2.0.dev0` reste téléchargeable pour la reproductibilité, mais son
installateur nécessite un contournement détaillé dans la
[fiche des versions](docs/versions.md#installer-lancienne-v020dev0).

Vérifier ensuite l'installation :

```bash
benchmark-mac --version
uv tool list
benchmark-mac list
benchmark-mac compare --help
```

## Installation depuis le dossier de développement

```bash
./install.sh
```

ou simplement :

```bash
uv sync
uv run benchmark-mac list
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

Au démarrage, `benchmark-mac` observe pendant une seconde la charge CPU, la
mémoire, l'échange et les processus actifs. Il affiche un avertissement si le
point de départ paraît éloigné du repos, puis poursuit la mesure. Ce contrôle
ponctuel aide à repérer une mauvaise campagne ; il ne peut pas prouver que la
machine a atteint son potentiel maximal.

Toute la suite, avec le profil standard :

```bash
benchmark-mac run --label "MacBook Pro M4 Pro"
```

Chaque test est exécuté trois fois par défaut et le rapport conserve la médiane,
le minimum, le maximum et la dispersion. Le nombre de passages est réglable :

```bash
benchmark-mac run --repeat 5 --profile thorough
```

Un groupe ou plusieurs groupes :

```bash
benchmark-mac run --group cpu
benchmark-mac run --group memory --group storage --profile thorough
benchmark-mac run --group gpu --profile standard
```

Un ou plusieurs tests individuels :

```bash
benchmark-mac run cpu.integer
benchmark-mac run cpu.hash memory.copy application.sqlite --profile quick
```

Le catalogue complet est fourni par `benchmark-mac list`. La commande
`benchmark-mac describe cpu.hash` affiche le protocole, les limites et les
références d'un test. Les profils `quick`, `standard` et `thorough` augmentent
progressivement les durées et volumes.

## Comparer plusieurs machines

Copier les rapports JSON dans un même dossier, puis utiliser le premier comme
référence :

```bash
benchmark-mac compare mac-m4.json pc-ryzen.json
```

Pour obtenir le rapport visuel autonome et adapter le résultat à ses usages :

```bash
benchmark-mac compare mac-m4.json pc-ryzen.json pc-intel.json \
  --weight developpement=50 \
  --weight creation=30 \
  --weight quotidien=20 \
  --html comparaison.html
```

Le premier rapport est la référence 100. Le HTML traduit les rapports en
indices, écarts qualitatifs et temps équivalents. Il contient des barres, un
graphique d'écart pour deux machines, une carte thermique pour plusieurs
machines, des chronologies et un résumé en langage courant.

La comparaison exige la même version de la suite, le même profil et la même
version de Python. Les rapports sont enregistrés dans `data/results/` par défaut.
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
