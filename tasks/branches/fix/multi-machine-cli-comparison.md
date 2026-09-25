# Objective

Rendre la sortie CLI correcte et lisible lorsque plus de deux machines sont
comparées, puis servir de branche de travail à la série `0.3.1`.

# Current Status

- Branche créée depuis `main` local après intégration fast-forward de
  `feat/gpu-preflight`.
- Chaque candidate affiche désormais son propre écart et sa propre conclusion
  dans le détail des benchmarks.
- La première machine est explicitement indiquée comme référence.
- Aucun tag `0.3.1` n'est encore préparé ou publié.

# Next Concrete Action

Après publication confirmée de `main` et de la branche, préparer
`v0.3.1.dev0` en alignant version du paquet, installateurs, README et fiche des
versions.

# Validation Snapshot

- `uv run ruff check .` réussi.
- `uv run ruff format --check .` réussi.
- `uv run pytest` : 48 tests réussis.

# Key Files

- `src/benchmark_mac/cli.py`
- `tests/test_cli.py`
- `handoff.md`

# Watchouts

- `origin/main` n'a pas encore reçu l'intégration locale.
- Ne créer ni pousser branche ou tag sans confirmation explicite actuelle.
- La modification locale de `.gitignore` est antérieure et reste hors du
  commit de correction.
