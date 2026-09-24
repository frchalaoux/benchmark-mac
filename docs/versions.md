# Versions disponibles et installation

La page GitHub [Tags](https://github.com/frchalaoux/benchmark-mac/tags) est la
liste de référence des versions publiées. Un tag fige le code et permet de
réinstaller exactement la même suite sur plusieurs machines.

La correction `v0.2.0.dev1` est actuellement en préparation. Elle rend les
installateurs cohérents avec leur propre version, mais elle ne doit pas être
considérée comme disponible avant d'apparaître dans la page **Tags**.

## Choisir une version

### `v0.2.0.dev0` — développement

[Consulter le code source de `v0.2.0.dev0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.0.dev0)

Cette version est destinée aux essais de la prochaine version stable. Elle
ajoute notamment :

- trois passages par benchmark par défaut, réglables de un à neuf ;
- médiane, valeurs brutes, minimum, maximum et dispersion dans le rapport JSON ;
- capture de l'alimentation et des conditions thermiques accessibles ;
- indices base 100, catégories techniques et six scénarios d'usage ;
- pondérations personnalisables et temps de travail équivalents ;
- comparaison de deux machines ou davantage ;
- rapport HTML autonome avec barres, carte thermique et chronologies.

Les formats JSON et l'interface peuvent encore évoluer. Tous les rapports à
comparer doivent employer la même version de la suite, le même profil et la
même version de Python.

### `v0.1.0` — stable

[Consulter le code source de `v0.1.0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.1.0)

Cette première version stable fournit :

- 12 benchmarks CPU, mémoire, stockage et applications ;
- les profils `quick`, `standard` et `thorough` ;
- l'exécution complète, par groupe ou par test ;
- l'inventaire matériel et les rapports JSON ;
- une comparaison tabulaire simple en valeurs et pourcentages.

Elle ne contient pas les répétitions automatiques, la dispersion, les scénarios
pondérés ni le rapport HTML de `v0.2.0.dev0`.

## Installer `v0.2.0.dev0`

Python n'a pas besoin d'être préinstallé. L'installateur récupère `uv`, puis
`uv` gère CPython 3.14.4 et l'outil isolé.

### macOS et Linux

Copier la commande entière, sans crochets ni parenthèses Markdown :

```bash
curl -LsSf https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.2.0.dev0/install.sh \
  | BENCHMARK_MAC_SOURCE="https://github.com/frchalaoux/benchmark-mac/archive/refs/tags/v0.2.0.dev0.tar.gz" sh
```

La variable `BENCHMARK_MAC_SOURCE` est indispensable pour ce tag : son
installateur cible encore `v0.1.0` lorsqu'aucune source n'est précisée.

### Windows PowerShell

```powershell
$env:BENCHMARK_MAC_SOURCE = "https://github.com/frchalaoux/benchmark-mac/archive/refs/tags/v0.2.0.dev0.tar.gz"
irm https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.2.0.dev0/install.ps1 | iex
Remove-Item Env:BENCHMARK_MAC_SOURCE
```

La dernière ligne retire la variable temporaire après l'installation.

## Installer `v0.1.0`

### macOS et Linux

```bash
curl -LsSf https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.1.0/install.sh | sh
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.1.0/install.ps1 | iex
```

## Vérifier la version installée

`uv tool list` affiche la version du paquet installé. Les deux commandes
suivantes vérifient ensuite que l'exécutable et le catalogue fonctionnent :

```bash
uv tool list
benchmark-mac list
benchmark-mac describe cpu.hash
```

La commande suivante permet de vérifier la comparaison. Dans la version de
développement, son aide doit notamment présenter les options `--html` et
`--weight` :

```bash
benchmark-mac compare --help
```

## Changer de version

Les installateurs utilisent `uv tool install --reinstall`. Il suffit donc de
lancer la commande complète de la version souhaitée. Conserver dans le nom des
rapports la version utilisée et ne pas comparer directement des rapports issus
de versions différentes.

## Portée des versions actuelles

Les deux versions utilisent CPython 3.14.4 afin de rendre les résultats plus
comparables. Elles prennent en charge macOS, Windows et Linux. Le GPU est
inventorié, mais n'est pas encore mesuré par un benchmark commun.
