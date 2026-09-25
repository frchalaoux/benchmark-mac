# Guide utilisateur

## Préparer une machine

L'installateur GitHub installe `uv` si nécessaire. `uv` installe ensuite sa
propre version de CPython 3.14.4 et isole `benchmark-mac` du Python du système.
Il n'est donc pas nécessaire d'installer Python séparément.

La version réellement exécutée se vérifie avec :

```bash
benchmark-mac --version
```

Avant une mesure :

1. brancher un portable sur secteur ;
2. sélectionner le même type de mode d'alimentation sur chaque machine
   (performances, équilibré, etc.) et désactiver l'économie d'énergie ;
3. terminer les mises à jour et synchronisations, fermer les navigateurs très
   chargés, jeux, encodages, rendus, machines virtuelles et outils de compilation ;
4. attendre quelques minutes après le démarrage ou une charge soutenue afin que
   l'activité de fond et la température se stabilisent ;
5. employer la même version de la suite, le même profil, le même nombre de
   passages et des conditions ambiantes aussi proches que possible.

Juste avant les tests, le programme échantillonne pendant une seconde la charge
CPU totale, la mémoire disponible, l'échange et les processus les plus actifs.
Il signale notamment un CPU occupé à au moins 15 %, moins de 20 % de mémoire
disponible, au moins 10 % d'échange utilisé ou un processus consommant au moins
10 % de CPU. La campagne continue afin de ne pas rendre l'outil fragile, mais
il est préférable de l'interrompre et de la recommencer au repos. L'observation
et ses avertissements sont enregistrés dans le rapport JSON.

Ce contrôle est un instantané, pas une certification : une tâche peut démarrer
après l'échantillon, et certains services protégés ne livrent pas tous leurs
détails. Les processus affichés sont une aide au diagnostic ; il ne faut pas
arrêter un processus système que l'on ne reconnaît pas.

## Choisir l'étendue

`benchmark-mac list` affiche les identifiants, groupes et profils disponibles.
`benchmark-mac describe IDENTIFIANT` donne le protocole détaillé, ses limites et
ses références bibliographiques.

- `benchmark-mac run` lance les 16 tests ;
- `benchmark-mac run --group cpu` lance le groupe CPU ;
- `benchmark-mac run --group gpu` lance les quatre mesures GPU hors écran ;
- `benchmark-mac run cpu.integer` lance un seul test ;
- plusieurs `--group` et plusieurs identifiants peuvent être réunis sans doublon.

### Machines équipées de plusieurs GPU

`benchmark-mac info` affiche les adaptateurs WebGPU avec un indice, leur nom,
leur type et le backend utilisé. Sans option, la sélection automatique préfère
un GPU dédié, puis un GPU intégré. Elle est affichée avant toute mesure GPU.

Un rapport ne mesure qu'un seul adaptateur afin que son interprétation reste
sans ambiguïté. Pour comparer les cartes d'une même machine ou forcer le GPU
intégré d'un portable hybride, exécuter deux campagnes distinctes :

```bash
benchmark-mac run --group gpu --gpu 0 --label "PC hybride — GPU 0"
benchmark-mac run --group gpu --gpu 1 --label "PC hybride — GPU 1"
```

Les indices sont propres à la machine : vérifier `benchmark-mac info` sur
chacune d'elles au lieu de supposer que `0` désigne toujours le GPU dédié.

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
`fichiers`, `base-de-donnees`, `creation` et `jeu-3d`. Sans réglage, ils ont le
même poids. Une pondération personnelle s'écrit ainsi :

```bash
benchmark-mac compare mac.json pc.json \
  --weight developpement=50 \
  --weight creation=30 \
  --weight quotidien=20 \
  --html comparaison.html
```

La moyenne géométrique des rapports évite qu'une seule valeur très élevée
domine artificiellement l'indice. Les mesures WebGPU rendent comparables des
charges communes sur Metal, Direct3D 12 et Vulkan ; elles ne remplacent pas un
test d'un logiciel créatif ou d'un jeu précis.
