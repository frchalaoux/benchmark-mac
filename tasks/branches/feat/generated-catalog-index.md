# Objective

Livrer l'index du catalogue généré au déploiement plutôt que versionné dans Git.

# Current Status

Objectif atteint. Le commit `c0a1ea6…` est publié sous `v0.4.0.dev6` et fusionné
dans `main` par la PR #22. Le catalogue génère son index pendant le déploiement
Pages. La stable `v0.4.0` est depuis publiée et intégrée dans `main` par la PR
#23.

# Next Concrete Action

Aucune action restante sur cette branche terminée.

# Validation Snapshot

- Source : Ruff, format et 92 tests réussis.
- Installation publique isolée de `v0.4.0.dev6` réussie.
- Catalogue : 13 tests Python, 5 tests JavaScript et construction Pages réussis.
- Le catalogue public contient maintenant un rapport ajouté par la PR #14.

# Key Files

- `src/benchmark_mac/contribution.py`
- `src/benchmark_mac/cli.py`
- `docs/tutoriel-catalogue.md`
- `docs/versions.md`
- `README.md`
- `../perfcomparator-results/scripts/build_catalog.py`
- `../perfcomparator-results/scripts/build_site.py`
- `../perfcomparator-results/scripts/auto_merge.py`

# Watchouts

- Le tag `v0.4.0.dev6` pointe sur `c0a1ea6…` et ne doit pas être déplacé.
- La branche locale actuelle est déjà fusionnée ; repartir de `origin/main` pour
  tout nouveau changement.
- L'index reste généré au déploiement ; ne pas le réintroduire dans les commits.
- Aucune opération distante sans confirmation explicite actuelle.
