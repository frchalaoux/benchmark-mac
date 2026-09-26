# Objective

Rendre la sortie CLI correcte et lisible lorsque plus de deux machines sont
comparées, puis servir de branche de travail à la série `0.3.1`.

# Current Status

- Branche réintégrée avec `main` au commit `afae631` après publication et
  close-out de la stable `v0.3.0`.
- Chaque candidate affiche désormais son propre écart et sa propre conclusion
  dans le détail des benchmarks.
- La première machine est explicitement indiquée comme référence.
- Paquet, installateurs et documentation alignés localement sur `0.3.1.dev0`.
- `0.3.1.dev0` conserve le protocole de mesure de `0.3.0`.
- Branche et tag annoté `v0.3.1.dev0` publiés ensemble sur `0e96ee5`.
- Archive distante validée avec une comparaison CLI réelle de trois rapports
  complets et 16 benchmarks communs.
- Pull request nº 5 fusionnée dans `main` au commit `f6022ac`; correction
  stabilisée et publiée dans `v0.3.1`.

# Next Concrete Action

Aucune action requise; le travail est intégré et stabilisé dans `v0.3.1`.

# Validation Snapshot

- `uv run ruff check .` réussi.
- `uv run ruff format --check .` réussi.
- `uv run pytest` : 50 tests réussis sur `0.3.1.dev0`.
- Source et wheel `0.3.1.dev0` construites avec succès.
- Archive inspectée sans rapport HTML; wheel installée isolément et
  `benchmark-mac --version` vérifié à `0.3.1.dev0`.

# Key Files

- `src/benchmark_mac/cli.py`
- `tests/test_cli.py`
- `handoff.md`

# Watchouts

- Ne pas changer le protocole de mesure dans cette correction de rendu CLI.
- Ne créer ni pousser branche ou tag sans confirmation explicite actuelle.
- Les rapports HTML dans `data/results/` restent ignorés et locaux.
