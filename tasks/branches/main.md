# Objective

Comparer de manière reproductible les performances de Mac et PC envisagés pour
un achat.

# Current Status

La préversion `v0.3.1.dev0` est publiée et sa correction CLI est intégrée dans
`main`. La suite couvre 16 benchmarks CPU, mémoire,
stockage, applications et GPU WebGPU, avec contrôle préalable, sélection
d'adaptateur et comparaisons HTML multi-machines. Les rapports `0.3.0.dev1`,
`0.3.0.dev2` et `0.3.0` sont compatibles entre eux.

# Next Concrete Action

Finaliser et publier la stable `v0.3.1` depuis la branche `release/0.3.1`.

# Validation Snapshot

- CPython cible : 3.14.4 géré par `uv`.
- Stable actuelle : `v0.3.0`, publiée sur `3d50177` puis fusionnée dans `main`
  par la pull request nº 3 (`14cd225`).
- Préversion `v0.3.1.dev0` publiée sur `0e96ee5`; correction fusionnée par la
  pull request nº 5 (`f6022ac`).
- Ruff, format, 49 tests, source et wheel `0.3.0` validés.
- Validations fonctionnelles macOS, Windows 11 et Linux amd64 réalisées.

# Watchouts

- Employer exactement le même profil et des versions de protocole compatibles
  sur toutes les machines.
- Les lectures disque peuvent être influencées par les caches du système.
- Ne jamais déplacer ou recréer le tag stable `v0.3.0`.
- Ne rien publier à distance sans autorisation explicite actuelle.
