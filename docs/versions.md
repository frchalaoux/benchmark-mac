# Versions disponibles et installation

La page GitHub [Tags](https://github.com/frchalaoux/benchmark-mac/tags) est la
liste de référence des versions publiées. Un tag fige le code et permet de
réinstaller exactement la même suite sur plusieurs machines.

## Choisir une version

### `0.3.0.dev0` — préparation locale, non publiée

La branche de travail ajoute quatre mesures GPU WebGPU, un contrôle préalable
des processus et de la charge, un septième scénario `jeu-3d` et le schéma JSON
4. Les machines hybrides peuvent sélectionner un adaptateur avec `--gpu INDEX`.
Elle ne figure pas encore dans la liste des tags GitHub : il n'existe donc
pas encore de commande d'installation distante fiable pour cette version.
Depuis son dossier de travail, elle s'installe avec `./install.sh` sur macOS ou
Linux et `./install.ps1` dans PowerShell.

### `v0.2.1` — stable actuelle

[Consulter le code source de `v0.2.1`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.1)

Cette version reprend toutes les fonctions de `v0.2.0` et corrige l'échec
`WinError 32` de `application.sqlite` sous Windows. La connexion SQLite est
désormais fermée explicitement avant la suppression du répertoire temporaire.

### `v0.2.0` — stable antérieure

[Consulter le code source de `v0.2.0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.0)

Cette version stable ajoute notamment :

- trois passages par benchmark par défaut, réglables de un à neuf ;
- médiane, valeurs brutes, minimum, maximum et dispersion dans le rapport JSON ;
- capture de l'alimentation et des conditions thermiques accessibles ;
- indices base 100, catégories techniques et six scénarios d'usage ;
- pondérations personnalisables et temps de travail équivalents ;
- comparaison de deux machines ou davantage ;
- rapport HTML autonome avec barres, carte thermique et chronologies.

Tous les rapports à comparer doivent employer la même version de la suite, le
même profil et la même version de Python.

Cette révision corrige la comparaison `cpu.multicore` : le nombre de processus
peut varier selon les processeurs logiques disponibles sur chaque machine, sans
relâcher la vérification des autres paramètres du protocole.

Sous Windows, `application.sqlite` peut néanmoins échouer avec `WinError 32`
pendant le nettoyage. Utiliser `v0.2.1` pour toute nouvelle campagne.

### `v0.2.0.dev2` — développement archivé

[Consulter le code source de `v0.2.0.dev2`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.0.dev2)

Cette préversion contient les fonctions et la correction multicœur reprises
dans `v0.2.0`. Préférer `v0.2.1` pour toute nouvelle campagne.

### `v0.2.0.dev1` — développement antérieur

[Consulter le code source de `v0.2.0.dev1`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.0.dev1)

Cette version corrige les installateurs de `dev0`, mais refuse la comparaison
`cpu.multicore` lorsque les machines possèdent un nombre différent de
processeurs logiques. Préférer `v0.2.1` pour une nouvelle campagne.

### `v0.2.0.dev0` — développement obsolète

[Consulter le code source de `v0.2.0.dev0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.2.0.dev0)

Cette version contient les mêmes grandes fonctions expérimentales, mais son
README et ses installateurs ciblent `v0.1.0` par défaut. Elle reste disponible
pour reproduire une ancienne campagne ; toute nouvelle installation doit
préférer `v0.2.1`.

### `v0.1.0` — stable antérieure

[Consulter le code source de `v0.1.0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.1.0)

Cette première version stable fournit :

- 12 benchmarks CPU, mémoire, stockage et applications ;
- les profils `quick`, `standard` et `thorough` ;
- l'exécution complète, par groupe ou par test ;
- l'inventaire matériel et les rapports JSON ;
- une comparaison tabulaire simple en valeurs et pourcentages.

Elle ne contient pas les répétitions automatiques, la dispersion, les scénarios
pondérés ni le rapport HTML de `v0.2.1`.

## Installer `v0.2.1`

Python n'a pas besoin d'être préinstallé. L'installateur récupère `uv`, puis
`uv` gère CPython 3.14.4 et l'outil isolé.

### macOS et Linux

Copier la commande entière, sans crochets ni parenthèses Markdown :

```bash
curl -LsSf https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.2.1/install.sh | sh
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.2.1/install.ps1 | iex
```

## Installer l'ancienne `v0.2.0`

Cette version est conservée pour reproduire une campagne existante. Sous
Windows, son benchmark SQLite peut échouer pendant le nettoyage ; préférer
`v0.2.1`.

### macOS et Linux

```bash
curl -LsSf https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.2.0/install.sh | sh
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.2.0/install.ps1 | iex
```

## Installer l'ancienne `v0.2.0.dev2`

Ces commandes servent uniquement à reproduire une campagne de préversion. Pour
une nouvelle comparaison, utiliser `v0.2.1`.

### macOS et Linux

```bash
curl -LsSf https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.2.0.dev2/install.sh | sh
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.2.0.dev2/install.ps1 | iex
```

## Installer l'ancienne `v0.2.0.dev1`

Ces commandes servent à reproduire une campagne existante. Pour une nouvelle
comparaison entre machines, utiliser `v0.2.1`.

### macOS et Linux

```bash
curl -LsSf https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.2.0.dev1/install.sh | sh
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.2.0.dev1/install.ps1 | iex
```

## Installer l'ancienne `v0.2.0.dev0`

Cette procédure sert uniquement à reproduire une campagne existante. La source
doit être imposée explicitement pour contourner l'erreur de son installateur.

### macOS et Linux

```bash
curl -LsSf https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.2.0.dev0/install.sh \
  | BENCHMARK_MAC_SOURCE="https://github.com/frchalaoux/benchmark-mac/archive/refs/tags/v0.2.0.dev0.tar.gz" sh
```

### Windows PowerShell

```powershell
$env:BENCHMARK_MAC_SOURCE = "https://github.com/frchalaoux/benchmark-mac/archive/refs/tags/v0.2.0.dev0.tar.gz"
irm https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.2.0.dev0/install.ps1 | iex
Remove-Item Env:BENCHMARK_MAC_SOURCE
```

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
benchmark-mac --version
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

## Portée des versions publiées

Les versions publiées jusqu'à `v0.2.1` utilisent CPython 3.14.4 afin de rendre
les résultats plus comparables. Elles prennent en charge macOS, Windows et
Linux. Le GPU y est inventorié, mais n'y est pas encore mesuré par un benchmark
commun. Cette limite est levée dans la préparation locale `0.3.0.dev0` décrite
ci-dessus.
