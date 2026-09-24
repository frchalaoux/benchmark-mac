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

Chaque benchmark est répété trois fois par défaut. `--repeat 5` demande cinq
passages, dans la limite de neuf. Le score principal est la médiane ; le rapport
conserve aussi toutes les valeurs, le minimum, le maximum et l'étendue relative.

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

## Rapport visuel et priorités

Le rapport HTML fonctionne hors ligne et n'envoie aucune donnée :

```bash
benchmark-mac compare rapports/mac.json rapports/pc.json \
  --html comparaison.html
```

Il présente une référence 100, des indices par catégorie et scénario, les temps
équivalents pour des tâches de 10 secondes, 2 minutes, 30 minutes et 4 heures,
ainsi que les dispersions et conclusions prudentes.

Les scénarios disponibles sont `quotidien`, `developpement`, `calcul-intensif`,
`fichiers`, `base-de-donnees` et `creation`. Sans réglage, ils ont le même poids.
Une pondération personnelle s'écrit ainsi :

```bash
benchmark-mac compare mac.json pc.json \
  --weight developpement=50 \
  --weight creation=30 \
  --weight quotidien=20 \
  --html comparaison.html
```

La moyenne géométrique des rapports évite qu'une seule valeur très élevée
domine artificiellement l'indice. Le scénario création reste marqué « hors
GPU » tant qu'un moteur graphique commun n'est pas intégré.
