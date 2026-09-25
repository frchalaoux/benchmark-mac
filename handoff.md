# Handoff

## État actuel

- Branche locale : `feat/gpu-preflight`.
- Préversion publiée : `v0.3.0.dev0`, pointant sur le commit `73c7d53`.
- Correctif prêt pour publication : `v0.3.0.dev1`.
- Base : `main` au tag stable `v0.2.1` (`c7ffdce`).
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
- Installateurs alignés sur la candidate `v0.3.0.dev1` et CPython 3.14.4
  géré par `uv`.
- Si un ancien `uv` ne connaît pas CPython 3.14.4, les installateurs mettent
  automatiquement `uv` à niveau depuis la source officielle, puis réessaient.
- Sous Windows, `dev1` télécharge l'installateur officiel dans un fichier
  temporaire et l'exécute dans un processus PowerShell enfant. Son éventuel
  `exit` ne peut donc plus fermer la console principale.
- Documentation des quatre benchmarks GPU avec protocole, limites et références
  WebGPU, WGSL, `wgpu-py` et IEEE 754.

## Validations réalisées

- `uv run ruff check .` : réussi.
- `uv run pytest` : 47 tests réussis, dont la reprise après échec d'un ancien `uv`,
  l'exclusion du PID 0 et le refus d'un moteur graphique logiciel.
- `uv build` : source et wheel `0.3.0.dev1` construits.
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
- La validation fonctionnelle de la préversion complète reste à effectuer sous
  Windows et Linux après publication.

## Publication effectuée

- Branche `feat/gpu-preflight` publiée sur `origin`.
- Tag annoté `v0.3.0.dev0` publié sur le commit `73c7d53`.
- Branche, tag et page GitHub vérifiés après publication.
- Les installateurs `install.sh` et `install.ps1` du tag répondent depuis
  `raw.githubusercontent.com` et ciblent bien `v0.3.0.dev0` avec CPython 3.14.4.
- Aucune fusion dans `main` et aucune release GitHub effectuées.

## Prochaine étape possible

Publier `v0.3.0.dev1` après une nouvelle confirmation explicite, puis l'installer
sur le Windows 10 qui possède encore `uv 0.5.1` afin de confirmer
que la mise à niveau automatique ne ferme plus la console. Exécuter ensuite au
minimum `benchmark-mac --version`, `benchmark-mac info` et
`benchmark-mac run --group gpu --profile quick`.

## Points de vigilance

- Ne jamais effectuer d'opération distante sans confirmation explicite,
  impérative, séparée et actuelle de l'utilisateur.
- Toujours pousser la branche contenant le commit avant ou avec le tag.
- Ne pas présenter `v0.3.0.dev1` comme stable ; `v0.2.1` reste la stable
  recommandée.
- Un indice GPU est local à une machine : toujours consulter
  `benchmark-mac info` avant d'utiliser `--gpu`.
- Les mesures WebGPU sont synthétiques et ne remplacent pas Blender, un jeu, le
  ray tracing, les codecs vidéo matériels ou les accélérateurs IA.
