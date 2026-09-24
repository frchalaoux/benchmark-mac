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
- Candidate locale `0.2.0.dev1` : installateurs alignés sur leur version et
  protégés par des tests de non-régression ; aucun tag `dev1` encore publié.

## Prochaine action possible

Valider le rapport HTML avec les mesures réelles d'une deuxième machine, puis
ajouter un scénario GPU commun fondé sur une version figée de Blender.

## Point de vigilance

Ne pas publier de dépôt, tag, release ou modification distante sans demande
explicite, séparée et actuelle de l'utilisateur.
