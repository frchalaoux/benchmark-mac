# Objective

Transformer les scores techniques en comparaison compréhensible et sensible
entre deux machines ou plus.

# Current Status

- Trois répétitions par défaut, médiane et dispersion conservées dans le JSON.
- Première machine ramenée à l'indice 100.
- Catégories et six scénarios d'usage agrégés par moyenne géométrique.
- Pondérations personnalisables avec `--weight scenario=nombre`.
- Temps équivalents, seuils qualitatifs et chevauchement min–max.
- Rapport HTML autonome avec barres, dumbbell, carte thermique et chronologies.
- Candidate `0.2.0.dev1` préparée avec des installateurs alignés sur leur propre
  version et des tests de non-régression dédiés.
- Candidate `0.2.0.dev2` : comparaison multicœur autorisée entre machines dont
  le nombre de processeurs logiques diffère.

# Next Concrete Action

Tester la comparaison avec des rapports complets issus de deux machines réelles.

# Validation Snapshot

- CPython 3.14.4 géré par `uv`.
- `ruff check` et `ruff format --check` réussis.
- 35 tests réussis.
- Source distribution et wheel `0.2.0.dev2` construites avec succès.
- Syntaxe de l'installateur POSIX validée.

# Watchouts

- Les temps équivalents sont des illustrations relatives, pas des prédictions applicatives.
- Le scénario création n'inclut pas encore le GPU.
- Ne pas publier la branche sans demande explicite, séparée et actuelle.
