# Objective

Comparer de manière reproductible les performances de Mac et PC envisagés pour
un achat.

# Current Status

La stable `v0.3.1` est publiée et marquée `Latest`. La suite couvre 16
benchmarks CPU, mémoire,
stockage, applications et GPU WebGPU, avec contrôle préalable, sélection
d'adaptateur et comparaisons HTML multi-machines. Les rapports `0.3.0.dev1`,
`0.3.0.dev2`, `0.3.0`, `0.3.1.dev0` et `0.3.1` sont compatibles entre eux.
Son close-out documentaire est intégré par la pull request nº 7 (`d2bc4e8`).
La préversion `v0.3.2.dev0` mémorise désormais le protocole de mesure dans les
nouveaux JSON; sa fonctionnalité est intégrée par la pull request nº 9
(`ff307fd`).

# Next Concrete Action

Préparer la branche stable `release/0.3.2`.

# Validation Snapshot

- CPython cible : 3.14.4 géré par `uv`.
- Stable antérieure : `v0.3.0`, publiée sur `3d50177` puis fusionnée dans `main`
  par la pull request nº 3 (`14cd225`).
- Préversion `v0.3.1.dev0` publiée sur `0e96ee5`; correction fusionnée par la
  pull request nº 5 (`f6022ac`).
- Stable `v0.3.1` publiée sur `9045884`; pull request nº 6 fusionnée dans
  `main` au commit `a3debdd`; GitHub Release marquée `Latest`.
- Préversion `v0.3.2.dev0` publiée sur `5bffb42`; fonctionnalité fusionnée par
  la pull request nº 9 (`ff307fd`).
- Comparaison mixte distante réussie entre `0.3.0.dev2`, `0.3.1` et
  `0.3.2.dev0`, avec 16 benchmarks communs et le protocole déclaré `0.3.0`.
- Smoke test Ubuntu 24.04 Docker réussi depuis le tag distant `v0.3.2.dev0` :
  installation complète, catalogue de 16 tests et JSON Linux conforme après
  une exécution rapide de `cpu.integer`.
- Ruff, format, 50 tests, source et wheel `0.3.1` validés.
- Validations fonctionnelles macOS, Windows 11 et Linux amd64 réalisées.

# Watchouts

- Employer exactement le même profil et des versions de protocole compatibles
  sur toutes les machines.
- Les lectures disque peuvent être influencées par les caches du système.
- Ne jamais déplacer ou recréer le tag stable `v0.3.0`.
- Ne jamais déplacer ou recréer le tag stable `v0.3.1`.
- Ne rien publier à distance sans autorisation explicite actuelle.
