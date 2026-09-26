# Handoff

## État actuel

- Branche locale : `release/0.3.0`, créée depuis `main` au commit `8dc7a53`.
- Périmètre fonctionnel de `v0.3.0` figé : GPU WebGPU, contrôle préalable,
  corrections Windows et documentation associée déjà présents sur `main`.
- La correction CLI multi-machine du commit `6d4c5dd` est explicitement exclue
  de `v0.3.0` et reste réservée à la série `0.3.1`.
- Préversions publiées : `v0.3.0.dev0` sur `73c7d53`, `v0.3.0.dev1` sur
  `57bf438` et `v0.3.0.dev2` sur `41da9e3`.
- `main` pointe sur `8dc7a53`; la dernière version stable publiée reste
  `v0.2.1` (`c7ffdce`).
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

## Validations réalisées

- `uv run ruff check .` : réussi.
- `uv run pytest` : 49 tests réussis, dont la reprise après échec d'un ancien `uv`,
  l'exclusion du PID 0, le refus d'un moteur graphique logiciel et la
  compatibilité contrôlée entre `0.3.0.dev1`, `0.3.0.dev2` et `0.3.0`.
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
- Aucune fusion dans `main` et aucune release GitHub effectuées.

## Prochaine étape possible

Relire le commit de préparation stable, puis préparer son intégration dans
`main` et le tag annoté `v0.3.0`. Aucun ajout fonctionnel ne doit entrer dans
cette branche.

## Points de vigilance

- Ne jamais effectuer d'opération distante sans confirmation explicite,
  impérative, séparée et actuelle de l'utilisateur.
- Toujours pousser la branche contenant le commit avant ou avec le tag.
- Tant que `v0.3.0` n'est pas publié, `v0.2.1` reste la dernière stable
  réellement disponible sur GitHub.
- Un indice GPU est local à une machine : toujours consulter
  `benchmark-mac info` avant d'utiliser `--gpu`.
- Les mesures WebGPU sont synthétiques et ne remplacent pas Blender, un jeu, le
  ray tracing, les codecs vidéo matériels ou les accélérateurs IA.
