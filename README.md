# benchmark-mac

Suite locale pour comparer les performances de Mac et de PC avant un achat. Elle
utilise les mêmes scénarios, paramètres et version exacte de CPython sur macOS,
Windows et Linux, puis produit des rapports JSON portables.

La branche de travail prépare `0.3.0.dev0` : elle ajoute quatre benchmarks GPU
WebGPU légers et un contrôle de l'état de la machine avant chaque campagne. Ce
numéro n'est pas présenté comme un tag disponible tant qu'il n'est pas publié.

## Versions publiées

Consulter [tous les tags disponibles](https://github.com/frchalaoux/benchmark-mac/tags)
ou choisir une version ci-dessous.

| Version | Canal | À choisir pour | État |
| --- | --- | --- | --- |
| [`v0.2.1`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.1) | Stable | Comparer des machines, notamment sous Windows | Version recommandée |
| [`v0.2.0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.0) | Stable antérieure | Reproduire une campagne existante | Échec SQLite possible sous Windows |
| [`v0.2.0.dev2`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.0.dev2) | Développement archivé | Reproduire une campagne de préversion | Base fonctionnelle de `v0.2.0` |
| [`v0.2.0.dev1`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.0.dev1) | Développement archivé | Reproduire une campagne existante | Comparaison multicœur trop stricte |
| [`v0.2.0.dev0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.0.dev0) | Développement obsolète | Reproduire une ancienne campagne | Installateur incorrect par défaut |
| [`v0.1.0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.1.0) | Stable antérieure | Reproduire les premiers rapports simples | Remplacée par `v0.2.1` |

La [fiche détaillée des versions](docs/versions.md) indique les différences,
les commandes d'installation pour chaque système et les précautions de mise à
jour. Les commandes GitHub ci-dessous ciblent la stable actuelle ; les sections
fonctionnelles décrivent la préparation `0.3.0.dev0` de cette branche.

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

`v0.2.0.dev0` reste téléchargeable pour la reproductibilité, mais son
installateur nécessite un contournement détaillé dans la
[fiche des versions](docs/versions.md#installer-lancienne-v020dev0).

Vérifier ensuite l'installation :

```bash
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
concluante.

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
