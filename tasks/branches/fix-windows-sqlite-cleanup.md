# Objective

Éviter l'échec `WinError 32` du benchmark `application.sqlite` sous Windows.

# Current Status

- La connexion SQLite est fermée explicitement avant le nettoyage du dossier
  temporaire.
- Un test de non-régression vérifie l'appel à `close()`.
- Ruff, formatage, 36 tests et construction du paquet sont validés.
- La version corrective préparée est `0.2.1`.

# Next Concrete Action

Exécuter `benchmark-mac run application.sqlite` sur Windows et vérifier que
trois passages se terminent sans échec.

# Watchouts

- Le correctif n'est pas encore publié.
- Une validation Windows réelle reste nécessaire, car POSIX autorise la
  suppression de certains fichiers encore ouverts.
