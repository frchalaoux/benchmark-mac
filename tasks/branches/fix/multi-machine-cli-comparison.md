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
- Aucun tag `v0.3.1.dev0` n'est encore créé ou publié.

# Next Concrete Action

Relire le commit de préparation, puis préparer la publication coordonnée de la
branche et du tag `v0.3.1.dev0` sans opération distante.

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
