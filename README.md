# benchmark-mac

Suite locale pour comparer les performances de Mac et de PC avant un achat. Elle
utilise les mêmes scénarios, paramètres et version exacte de CPython sur macOS,
Windows et Linux, puis produit des rapports JSON portables.

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

Sur macOS ou Linux :

```bash
curl -LsSf https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.1.0/install.sh | sh
```

Sous Windows, dans PowerShell :

```powershell
irm https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.1.0/install.ps1 | iex
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

La comparaison exige la même version de la suite, le même profil et la même
version de Python. Les rapports sont enregistrés dans `data/results/` par défaut.

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
