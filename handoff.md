# Handoff

## État actuel

- Suite multiplateforme de 12 benchmarks, exécutables tous ensemble, par groupe ou individuellement.
- Profils `quick`, `standard` et `thorough`.
- Rapports JSON portables avec inventaire matériel et comparaison en pourcentage.
- CPython 3.14.4 figé ; installateurs autonomes `uv` pour macOS/Linux et Windows.
- Publication initiale publique `v0.1.0` sur `frchalaoux/benchmark-mac`.
- Branche locale `feat/human-comparison-report` : répétitions, médiane,
  dispersion, indices base 100, scénarios pondérables, temps équivalents,
  conclusions prudentes et rapport HTML autonome.
- Version `0.2.0.dev1` : installateurs alignés sur leur version et protégés par
  des tests de non-régression.
- Version `0.2.0.dev2` : corrige la comparaison `cpu.multicore` entre
  machines ayant un nombre différent de processeurs logiques.
- Version stable `0.2.0` préparée pour intégration dans `main`.
- Branche locale `fix/windows-sqlite-cleanup` : fermeture explicite de la
  connexion SQLite avant suppression du répertoire temporaire, avec test de
  non-régression multiplateforme.

## Prochaine action possible

Confirmer le correctif SQLite sur Windows, puis examiner le rapport HTML produit
à partir de deux machines réelles.

## Point de vigilance

Ne pas publier de dépôt, tag, release ou modification distante sans demande
explicite, séparée et actuelle de l'utilisateur.
