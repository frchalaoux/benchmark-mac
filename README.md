# benchmark-mac

Suite locale pour comparer les performances de Mac et de PC avant un achat. Elle
utilise les mêmes scénarios, paramètres et version exacte de CPython sur macOS,
Windows et Linux, puis produit des rapports JSON portables.

## Versions publiées

Consulter [tous les tags disponibles](https://github.com/frchalaoux/benchmark-mac/tags)
ou choisir une version ci-dessous.

| Version | Canal | À choisir pour | État |
| --- | --- | --- | --- |
| [`v0.2.0.dev0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.0.dev0) | Développement | Tester les répétitions, les scénarios et le rapport HTML | Fonctionnelle, interface susceptible d'évoluer |
| [`v0.1.0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.1.0) | Stable | Exécuter les 12 benchmarks et produire des JSON simples | Première version stable |

La [fiche détaillée des versions](docs/versions.md) indique les différences,
les commandes d'installation pour chaque système et les précautions de mise à
jour. Le reste de ce README décrit la version de développement actuelle.

> La correction `v0.2.0.dev1` est en préparation sur la branche de
> développement, mais n'est pas encore un tag publié. Ne pas employer une URL
> `v0.2.0.dev1` avant son apparition dans la page **Tags**.

## Couverture actuelle

- **CPU** : entiers et flottants mono-cœur, SHA-256, compression zlib et calcul multicœur ;
- **mémoire** : bande passante de copie séquentielle ;
- **stockage** : lectures et écritures séquentielles et aléatoires de 4 Kio ;
- **applications** : traitement JSON et charge SQLite ;
- **inventaire** : modèle, OS, CPU, mémoire, GPU, disque et environnement Python.

Le GPU est inventorié mais pas encore scoré. Une comparaison GPU honnête entre
Metal, DirectX, CUDA et autres API nécessitera un moteur commun tel que Blender.

## Installation depuis GitHub

Python n'a pas besoin d'être installé. Le script installe `uv`, puis `uv`
télécharge et gère CPython 3.14.4 avant d'installer l'application.

### Version stable `v0.1.0`

Sur macOS ou Linux :

```bash
curl -LsSf https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.1.0/install.sh | sh
```

Sous Windows, dans PowerShell :

```powershell
irm https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.1.0/install.ps1 | iex
```

### Version de développement `v0.2.0.dev0`

Sur macOS ou Linux, utiliser cette commande complète. La variable est
nécessaire car l'installateur livré dans ce premier tag de développement cible
encore `v0.1.0` par défaut :

```bash
curl -LsSf https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.2.0.dev0/install.sh \
  | BENCHMARK_MAC_SOURCE="https://github.com/frchalaoux/benchmark-mac/archive/refs/tags/v0.2.0.dev0.tar.gz" sh
```

Sous Windows, dans PowerShell :

```powershell
$env:BENCHMARK_MAC_SOURCE = "https://github.com/frchalaoux/benchmark-mac/archive/refs/tags/v0.2.0.dev0.tar.gz"
irm https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.2.0.dev0/install.ps1 | iex
Remove-Item Env:BENCHMARK_MAC_SOURCE
```

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
