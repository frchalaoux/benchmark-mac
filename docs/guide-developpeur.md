# Guide développeur

Le paquet sépare les responsabilités :

- `models.py` définit le schéma versionné des rapports ;
- `system_info.py` collecte l'inventaire multiplateforme ;
- `benchmarks.py` contient profils, catalogue et charges ;
- `gpu_benchmarks.py` contient les pipelines WebGPU hors écran ;
- `service.py` résout une sélection et isole les échecs ;
- `repository.py` persiste les rapports atomiquement ;
- `comparison.py` calcule indices, scénarios, incertitudes et formulations ;
- `html_report.py` produit un document autonome sans ressource distante ;
- `cli.py` expose les commandes, pondérations et formats de comparaison.

Un benchmark reçoit un `BenchmarkContext` et retourne un `BenchmarkResult`. Il
doit employer des données déterministes, exclure sa préparation du chronométrage,
borner ses ressources avec le profil et nettoyer ses fichiers temporaires. Son
identifiant reste stable afin que les rapports puissent être comparés.

Le service répète chaque runner séparément, puis stocke la médiane comme
`value`. Les valeurs brutes ne doivent jamais être supprimées : l'analyse en a
besoin pour signaler les plages min–max chevauchantes.

Chaque identifiant possède aussi une entrée dans `BENCHMARK_DOCUMENTATION`.
Méthode, limites et références sont embarquées dans le rapport JSON et exposées
par `benchmark-mac describe`.

Ajouter ensuite sa `BenchmarkDefinition` à `DEFINITIONS`. Les groupes et le
catalogue en découlent automatiquement. Toute évolution incompatible du JSON
doit incrémenter `schema_version`.

Le contrôle préalable repose sur `psutil`. Il ne bloque jamais une campagne :
il produit un `ReadinessSnapshot`, affiché par la CLI, persisté dans le schéma 4
et repris par l'analyse comparative. Toute évolution des seuils doit rester
documentée dans la méthodologie et testée sans attente réelle.

Les validations locales sont :

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv build
```
