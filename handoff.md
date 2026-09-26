# Handoff

## État actuel

- Branche locale : `fix/multi-machine-cli-comparison`, réintégrée avec `main`
  après le close-out complet de `v0.3.0`.
- La correction CLI multi-machine du commit `6d4c5dd` ouvre la série `0.3.1`.
- Préversions publiées : `v0.3.0.dev0` sur `73c7d53`, `v0.3.0.dev1` sur
  `57bf438` et `v0.3.0.dev2` sur `41da9e3`.
- `main` et `origin/main` pointent sur `afae631`; la stable publiée actuelle est
  `v0.3.0`, taguée sur `3d50177`.
- 16 benchmarks exécutables ensemble, par groupe ou individuellement.
- Quatre benchmarks GPU hors écran fondés sur `wgpu 0.32.0` : calcul FP32,
  bande passante, filtre d'image et remplissage raster.
- Adaptateurs WebGPU listés par `benchmark-mac info`. Sélection automatique du
  premier GPU dédié, puis intégré, ou sélection explicite avec `--gpu INDEX`.
- Un seul GPU est mesuré par rapport ; utiliser un rapport par adaptateur sur
  les machines hybrides.
- Contrôle préalable d'une seconde avec `psutil 7.1.0` : CPU, mémoire disponible,
  échange et processus actifs. Les avertissements restent non bloquants, sont
  enregistrés dans le JSON et remontent dans les comparaisons.
- Schéma JSON 4. Les rapports `0.2.x` et `0.3.x` ne sont pas comparables.
- Sept scénarios, dont `jeu-3d`; GPU intégré à `calcul-intensif` et `creation`.
- Rapport HTML intitulé « Ce que ces performances changent au quotidien ».
- `benchmark-mac --version` affiche la version réellement exécutée.
- Version stable `0.3.0` préparée localement dans le paquet et les
  installateurs, avec CPython 3.14.4 géré par `uv`.
- Les rapports `0.3.0.dev1`, `0.3.0.dev2` et `0.3.0` sont explicitement
  reconnus comme compatibles; `0.3.0.dev0` reste refusée.
- Si un ancien `uv` ne connaît pas CPython 3.14.4, les installateurs mettent
  automatiquement `uv` à niveau depuis la source officielle, puis réessaient.
- Sous Windows, à partir de `dev1`, l'installateur télécharge la mise à niveau
  officielle de `uv` dans un fichier
  temporaire et l'exécute dans un processus PowerShell enfant. Son éventuel
  `exit` ne peut donc plus fermer la console principale.
- Documentation des quatre benchmarks GPU avec protocole, limites et références
  WebGPU, WGSL, `wgpu-py` et IEEE 754.
- La sortie CLI des comparaisons multi-machines associe désormais à chaque
  candidate son propre écart et sa propre conclusion; la première machine est
  explicitement affichée comme référence.
- Paquet, installateurs et documentation alignés localement sur la candidate
  `v0.3.1.dev0`, sans tag ni publication distante à ce stade.
- `0.3.1.dev0` conserve le protocole de mesure `0.3.0` et reste compatible avec
  `0.3.0.dev1`, `0.3.0.dev2` et `0.3.0`.

## Validations réalisées

- `uv run ruff check .` : réussi.
- `uv run pytest` : 49 tests réussis sur la stable, dont la reprise après échec
  d'un ancien `uv`,
  l'exclusion du PID 0, le refus d'un moteur graphique logiciel et la
  compatibilité contrôlée entre `0.3.0.dev1`, `0.3.0.dev2` et `0.3.0`.
- Test CLI ajouté sur la branche `0.3.1` avec trois machines, dont une plus
  rapide et une plus lente que la référence.
- Candidate `0.3.1.dev0` : 50 tests réussis, source et wheel construites,
  archive inspectée et wheel exécutée dans un environnement isolé avec la
  version attendue.
- `uv build` : source et wheel `0.3.0` construites; la wheel installée dans un
  environnement isolé affiche bien `benchmark-mac 0.3.0`.
- L'archive source exclut explicitement le rapport utilisateur racine
  `comparaison.html`.
- Exécution réelle des quatre benchmarks sur AMD Radeon Pro 560X via Metal.
- Détection réelle de deux GPU sur MacBook Pro : Radeon dédiée et Intel UHD 630.
- Sélection explicite et exécution réelle de `gpu.compute-fp32` sur l'Intel UHD 630.
- Contrôle préalable testé avec une machine au repos et avec un processus actif.
- Cause de l'échec Windows identifiée : `uv 0.5.1` (2024) ne connaît pas le
  téléchargement `cpython-3.14.4-windows-x86_64-none`.
- Second défaut identifié dans `dev0` : l'exécution imbriquée de
  `irm https://astral.sh/uv/install.ps1 | iex` permet au script tiers de fermer
  la session PowerShell appelante avec `exit`.
- Troisième défaut Windows identifié dans `dev0` : le pseudo-processus PID 0
  provoque une erreur de validation `ProcessLoad` avant les benchmarks.
- Une VM Windows 10 sans GPU transmis expose `Microsoft Basic Render Driver`
  comme adaptateur WebGPU de type `CPU`; `dev1` le signale et refuse les scores
  GPU logiciels sans interrompre les autres groupes.
- Windows 11 : campagne `standard` complète de 16 benchmarks réussie avec un
  état initial déclaré convenable.
- macOS Intel : campagne `quick` complète de 16 benchmarks réussie le
  26 septembre 2026 sur Radeon Pro 560X, sans échange utilisé et avec un état
  initial déclaré convenable. Les scores GPU de cette campagne restent trop
  dispersés pour servir de référence de performance stable.
- Linux amd64 sous Docker : l'installateur a correctement remplacé un ancien
  `uv 0.9.30` par `uv 0.12.19`, installé CPython 3.14.4 et exécuté les 12
  benchmarks CPU, mémoire, stockage et applications sans échec.
- Linux sans GPU transmis : `llvmpipe` est détecté comme moteur WebGPU de type
  `CPU` et les quatre scores GPU logiciels sont explicitement refusés. La voie
  Linux avec GPU matériel n'a pas pu être testée dans ce conteneur.

## Publication effectuée

- Branche `feat/gpu-preflight` publiée sur `origin`.
- Tag annoté `v0.3.0.dev0` publié sur le commit `73c7d53`.
- Tag annoté `v0.3.0.dev1` publié sur le commit `57bf438`.
- Tag annoté `v0.3.0.dev2` publié sur le commit `41da9e3`.
- Branche, tag, archive et page GitHub vérifiés après publication.
- Les installateurs `install.sh` et `install.ps1` de `v0.3.0.dev2` répondent
  depuis `raw.githubusercontent.com`, ciblent le bon tag avec CPython 3.14.4 et
  contiennent la reprise PowerShell isolée.
- Branche `release/0.3.0` et tag annoté `v0.3.0` publiés ensemble sur le commit
  `3d50177`.
- Pull request GitHub nº 3 fusionnée dans `main` au commit `14cd225`.
- GitHub Release stable `benchmark-mac v0.3.0` publiée et marquée `Latest` :
  https://github.com/frchalaoux/benchmark-mac/releases/tag/v0.3.0
- Installateurs bruts et métadonnées de version revérifiés après publication.
- Pull request documentaire nº 4 fusionnée dans `main` au commit `afae631`.

## Prochaine étape possible

Relire le commit de préparation de `0.3.1.dev0`, puis préparer la publication
coordonnée de la branche et du tag sans aucune opération distante avant
confirmation explicite.

## Points de vigilance

- Ne jamais effectuer d'opération distante sans confirmation explicite,
  impérative, séparée et actuelle de l'utilisateur.
- Toujours pousser la branche contenant le commit avant ou avec le tag.
- Ne jamais déplacer ou recréer le tag stable publié `v0.3.0`.
- Un indice GPU est local à une machine : toujours consulter
  `benchmark-mac info` avant d'utiliser `--gpu`.
- Les mesures WebGPU sont synthétiques et ne remplacent pas Blender, un jeu, le
  ray tracing, les codecs vidéo matériels ou les accélérateurs IA.
