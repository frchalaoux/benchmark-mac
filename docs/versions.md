# Versions disponibles et installation

La page GitHub [Tags](https://github.com/frchalaoux/benchmark-mac/tags) est la
liste de référence des versions publiées. Un tag fige le code et permet de
réinstaller exactement la même suite sur plusieurs machines.

## Choisir une version

### `v0.3.0` — stable actuelle

[Consulter le code source de `v0.3.0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.3.0)

Cette version stable reprend les quatre benchmarks GPU WebGPU, la sélection
d'adaptateur, le contrôle préalable de la machine et les corrections Windows
validés dans les préversions `dev1` et `dev2`. Elle refuse les moteurs WebGPU
logiciels afin de ne pas présenter un score CPU comme une performance GPU.

Les rapports `0.3.0.dev1`, `0.3.0.dev2` et `0.3.0` emploient le même protocole
de mesure et peuvent être comparés entre eux. `0.3.0.dev0` reste exclue de ce
groupe de compatibilité.

### `v0.3.0.dev2` — développement antérieur

[Consulter le code source de `v0.3.0.dev2`](https://github.com/frchalaoux/benchmark-mac/tree/v0.3.0.dev2)

Cette candidate conserve les fonctionnalités GPU de `dev0` et corrige la mise
à niveau automatique de `uv` sous Windows. Le script officiel est téléchargé
dans un fichier temporaire puis exécuté dans un processus PowerShell enfant :
son éventuel `exit` ne peut plus fermer la console principale. Elle ignore
également le pseudo-processus Windows PID 0 pendant le contrôle préalable et
refuse les moteurs WebGPU logiciels classés `CPU`, tels que
`Microsoft Basic Render Driver`.

Cette révision explicite aussi la convention durable `vX.Y.Z.devK` dans les
instructions du projet, le README et les guides.

### `v0.3.0.dev1` — développement antérieur

[Consulter le code source de `v0.3.0.dev1`](https://github.com/frchalaoux/benchmark-mac/tree/v0.3.0.dev1)

Cette préversion introduit les corrections Windows reprises dans `dev2` : mise
à niveau de `uv` dans un processus PowerShell enfant, exclusion du PID 0 et
refus des moteurs WebGPU logiciels classés `CPU`.

### `v0.3.0.dev0` — développement publié

[Consulter le code source de `v0.3.0.dev0`](https://github.com/frchalaoux/benchmark-mac/tree/v0.3.0.dev0)

Cette préversion ajoute :

- quatre mesures GPU WebGPU sans Blender : FP32, mémoire, filtre d'image et raster ;
- la sélection d'un adaptateur sur les machines multi-GPU avec `--gpu INDEX` ;
- un contrôle préalable du CPU, de la mémoire, de l'échange et des processus actifs ;
- la conservation de cet état initial et de ses avertissements dans le JSON ;
- le scénario `jeu-3d` et l'intégration du GPU aux scénarios de comparaison ;
- le titre HTML « Ce que ces performances changent au quotidien » ;
- l'option globale `benchmark-mac --version` ;
- la mise à niveau automatique d'un `uv` trop ancien pour CPython 3.14.4 ;
- le schéma JSON 4.

Elle doit être validée sur plusieurs configurations macOS, Windows et Linux
avant de devenir stable. Les rapports `0.2.x` et `0.3.x` ne doivent pas être
mélangés dans une comparaison.

Sous Windows, la reprise automatique de `dev0` présente toutefois un défaut :
elle injecte l'installateur officiel de `uv` dans la session en cours. Si celui-ci
appelle `exit`, la console peut se fermer avant la reprise de `benchmark-mac`.
Mettre `uv` à niveau séparément ou utiliser `v0.3.0.dev2`.

Pour reproduire malgré tout une campagne `dev0`, après mise à niveau préalable
de `uv` sous Windows :

```bash
curl -LsSf https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.3.0.dev0/install.sh | sh
```

```powershell
irm https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.3.0.dev0/install.ps1 | iex
```

### `v0.2.1` — stable antérieure

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

Tous les rapports à comparer doivent employer des versions de protocole
compatibles, le même profil et la même version de Python.

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

## Installer `v0.3.0`

Python n'a pas besoin d'être préinstallé. L'installateur récupère `uv` si
nécessaire, puis `uv` gère CPython 3.14.4 et remplace la version de
`benchmark-mac` éventuellement installée. Si un ancien `uv` ne connaît pas ce
Python, l'installateur met automatiquement `uv` à niveau et réessaie.

### macOS et Linux

```bash
curl -LsSf https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.3.0/install.sh | sh
```

### Windows PowerShell

```powershell
irm https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.3.0/install.ps1 | iex
```

Le contrôle suivant doit afficher `benchmark-mac 0.3.0` :

```bash
benchmark-mac --version
```

## Installer la stable `v0.2.1`

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

### Ancien `uv` sous Windows

L'installateur historique de `v0.2.1` réutilise le `uv` présent sans vérifier
s'il connaît CPython 3.14.4. Avec une version ancienne telle que `uv 0.5.1`, la
commande peut échouer avec `No download found`. Mettre alors `uv` à niveau et
placer sa version officielle en tête du `PATH` pour la session :

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
$env:Path = "$HOME\.local\bin;$env:Path"
uv --version
irm https://raw.githubusercontent.com/frchalaoux/benchmark-mac/v0.2.1/install.ps1 | iex
```

`v0.3.0.dev2` automatise cette reprise sans exécuter l'installateur tiers dans
la console principale.

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

## Portée des versions

Toutes ces versions utilisent CPython 3.14.4 afin de rendre les résultats plus
comparables et prennent en charge macOS, Windows et Linux. Jusqu'à `v0.2.1`, le
GPU est seulement inventorié. La série `0.3` ajoute les mesures WebGPU communes,
mais ne couvre pas le ray tracing, les unités IA, les codecs vidéo matériels ou
un moteur de jeu complet.
