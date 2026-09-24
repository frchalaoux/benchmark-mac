# Guide utilisateur

## Préparer une machine

L'installateur GitHub installe `uv` si nécessaire. `uv` installe ensuite sa
propre version de CPython 3.14.4 et isole `benchmark-mac` du Python du système.
Il n'est donc pas nécessaire d'installer Python séparément.

Avant une mesure, brancher un portable sur secteur, désactiver son mode économie
d'énergie, fermer les charges lourdes et attendre que sa température se
stabilise. Employer exactement la même version de la suite et le même profil sur
toutes les machines.

## Choisir l'étendue

`benchmark-mac list` affiche les identifiants, groupes et profils disponibles.
`benchmark-mac describe IDENTIFIANT` donne le protocole détaillé, ses limites et
ses références bibliographiques.

- `benchmark-mac run` lance les 12 tests ;
- `benchmark-mac run --group cpu` lance le groupe CPU ;
- `benchmark-mac run cpu.integer` lance un seul test ;
- plusieurs `--group` et plusieurs identifiants peuvent être réunis sans doublon.

Les profils sont :

- `quick` pour vérifier rapidement une machine ;
- `standard` pour une comparaison courante ;
- `thorough` pour des mesures plus longues et des fichiers disque plus grands.

Le répertoire passé à `--work-dir` désigne le disque à tester. Les fichiers
temporaires sont supprimés après chaque mesure, y compris en cas d'erreur.

## Produire et comparer des rapports

Nommer clairement chaque configuration :

```bash
benchmark-mac run --profile standard --label "Mac mini M4 16 Go"
benchmark-mac history
```

Copier ensuite les JSON produits vers la machine qui fera la comparaison :

```bash
benchmark-mac compare rapports/mac-mini.json rapports/pc-ryzen.json
```

Le pourcentage est calculé par rapport au premier fichier. Tous les scores
actuels suivent la règle « plus haut est meilleur ».
