# Guide développeur

Le paquet sépare les responsabilités :

- `models.py` définit le schéma versionné des rapports ;
- `system_info.py` collecte l'inventaire multiplateforme ;
- `benchmarks.py` contient profils, catalogue et charges ;
- `service.py` résout une sélection et isole les échecs ;
- `repository.py` persiste les rapports atomiquement ;
- `cli.py` expose les commandes et la comparaison.

Un benchmark reçoit un `BenchmarkContext` et retourne un `BenchmarkResult`. Il
doit employer des données déterministes, exclure sa préparation du chronométrage,
borner ses ressources avec le profil et nettoyer ses fichiers temporaires. Son
identifiant reste stable afin que les rapports puissent être comparés.

Chaque identifiant possède aussi une entrée dans `BENCHMARK_DOCUMENTATION`.
Méthode, limites et références sont embarquées dans le rapport JSON et exposées
par `benchmark-mac describe`.

Ajouter ensuite sa `BenchmarkDefinition` à `DEFINITIONS`. Les groupes et le
catalogue en découlent automatiquement. Toute évolution incompatible du JSON
doit incrémenter `schema_version`.

Les validations locales sont :

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv build
```
