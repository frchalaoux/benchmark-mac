# Handoff

## État actuel

- Branche locale : `feat/gpu-preflight`.
- Version préparée : `0.3.0.dev0` ; tag prévu : `v0.3.0.dev0`.
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
- Installateurs alignés sur `v0.3.0.dev0` et CPython 3.14.4 géré par `uv`.
- Si un ancien `uv` ne connaît pas CPython 3.14.4, les installateurs mettent
  automatiquement `uv` à niveau depuis la source officielle, puis réessaient.
- Documentation des quatre benchmarks GPU avec protocole, limites et références
  WebGPU, WGSL, `wgpu-py` et IEEE 754.

## Validations réalisées

- `uv run ruff check .` : réussi.
- `uv run pytest` : 46 tests réussis, dont la reprise après échec d'un ancien `uv`.
- `uv build` : source et wheel `0.3.0.dev0` construits.
- Exécution réelle des quatre benchmarks sur AMD Radeon Pro 560X via Metal.
- Détection réelle de deux GPU sur MacBook Pro : Radeon dédiée et Intel UHD 630.
- Sélection explicite et exécution réelle de `gpu.compute-fp32` sur l'Intel UHD 630.
- Contrôle préalable testé avec une machine au repos et avec un processus actif.
- Cause de l'échec Windows identifiée : `uv 0.5.1` (2024) ne connaît pas le
  téléchargement `cpython-3.14.4-windows-x86_64-none`.
- La validation fonctionnelle de la préversion complète reste à effectuer sous
  Windows et Linux après publication.

## Publication préparée

La documentation cible la future URL du tag `v0.3.0.dev0` et fournit les deux
commandes d'installation GitHub. Avant publication, refaire toutes les
validations, committer la documentation, puis demander une confirmation
impérative distincte.

Après confirmation seulement :

1. pousser `feat/gpu-preflight` sur `origin` ;
2. créer le tag annoté `v0.3.0.dev0` sur le commit final ;
3. pousser ce tag sur `origin` ;
4. vérifier que la branche et le tag sont visibles sur GitHub et que les deux
   URL `raw.githubusercontent.com` des installateurs répondent ;
5. ne pas fusionner dans `main` sans une nouvelle demande explicite.

## Points de vigilance

- Ne jamais effectuer d'opération distante sans confirmation explicite,
  impérative, séparée et actuelle de l'utilisateur.
- Toujours pousser la branche contenant le commit avant ou avec le tag.
- Ne pas présenter `v0.3.0.dev0` comme stable ; `v0.2.1` reste la stable
  recommandée.
- Un indice GPU est local à une machine : toujours consulter
  `benchmark-mac info` avant d'utiliser `--gpu`.
- Les mesures WebGPU sont synthétiques et ne remplacent pas Blender, un jeu, le
  ray tracing, les codecs vidéo matériels ou les accélérateurs IA.
