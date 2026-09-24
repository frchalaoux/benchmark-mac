# Objective

Comparer de manière reproductible les performances de Mac et PC envisagés pour
un achat.

# Current Status

La suite couvre CPU, mémoire, stockage, JSON et SQLite. Chaque test est
exécutable seul ou en groupe, avec trois profils. Les rapports JSON incluent
l'inventaire et peuvent être comparés localement.

# Next Concrete Action

Valider le protocole sur une deuxième machine, puis choisir un moteur GPU commun.

# Validation Snapshot

- CPython cible : 3.14.4 géré par `uv`.
- Version initiale : `v0.1.0`.
- Ruff, format, 21 tests et construction du paquet au vert avant publication.

# Watchouts

- Employer exactement le même profil et la même version sur toutes les machines.
- Les lectures disque peuvent être influencées par les caches du système.
- Ne rien publier à distance sans autorisation explicite actuelle.
