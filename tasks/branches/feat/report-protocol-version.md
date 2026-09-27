# Objective

Enregistrer la version du protocole de mesure indépendamment de la version de
la suite afin de comparer automatiquement des rapports produits par des
versions logicielles différentes mais compatibles.

# Current Status

Implémentation locale terminée sur `feat/report-protocol-version`. Les nouvelles
campagnes `0.3.2.dev0` écrivent `protocol_version: "0.3.0"`; les anciens
rapports restent comparables par la table historique. La branche et le tag
annoté `v0.3.2.dev0` sont publiés sur `5bffb42`; la pull request nº 9 est ouverte
vers `main`.

# Next Concrete Action

Relire puis fusionner la pull request nº 9 après confirmation explicite.

# Validation Snapshot

- Les rapports historiques restent pris en charge par une table de repli.
- La wheel isolée produit un rapport avec `suite_version: "0.3.2.dev0"`,
  `protocol_version: "0.3.0"`, `schema_version: 4`, un résultat et zéro échec.
- Une comparaison réelle de trois archives `0.3.0.dev2` produit encore les 16
  benchmarks détaillés.
- `uv run ruff format --check .` et `uv run ruff check .` réussissent.
- Les 53 tests réussissent, notamment le cas mixte ancien/nouveau.
- La source et la wheel `0.3.2.dev0` se construisent avec le nouveau champ;
  aucun rapport HTML n'est embarqué.
- L'archive distante du tag installe bien `benchmark-mac 0.3.2.dev0`; les deux
  installateurs bruts sont accessibles et ciblent le bon tag.

# Key Files

- `src/benchmark_mac/models.py`
- `src/benchmark_mac/service.py`
- `src/benchmark_mac/comparison.py`
- `tests/test_comparison.py`
- `tests/test_service.py`

# Watchouts

- Ne jamais réécrire `suite_version` dans un rapport existant.
- `0.3.0.dev0` doit rester exclue du groupe historique compatible.
- Ne rien publier à distance sans confirmation explicite actuelle.
