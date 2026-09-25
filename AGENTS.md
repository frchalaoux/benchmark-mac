# Instructions durables du projet

## Publications

Directive utilisateur prioritaire : **keep cool**.

**Je n'effectuerai aucune opération distante sans validation explicite.**

Ne jamais créer, déplacer, pousser, publier ou supprimer un tag Git, une
branche distante, une release GitHub, ni aucune autre mise à jour distante sans
une confirmation impérative, séparée et actuelle de l'utilisateur, donnée
après l'annonce précise de l'opération envisagée.

Une question ou une formulation exploratoire telle que « peux-tu publier ? »,
une discussion, une approbation antérieure ou une demande ambiguë ne constitue
jamais une autorisation d'exécution. Préparer, tester et proposer une
publication est autorisé ; s'arrêter immédiatement avant toute opération
distante, décrire exactement celle-ci et attendre une confirmation explicite
telle que « publie maintenant » ou « pousse ce tag ».

Lorsqu'une publication distante a été explicitement confirmée, toujours
publier également la branche contenant le commit concerné avant ou avec le tag,
afin que le commit appartienne à une branche distante et puisse faire l'objet
d'une pull request. Annoncer précisément la branche et le tag concernés avant
l'opération. Cette règle de cohérence ne remplace jamais l'obligation d'obtenir
la confirmation explicite préalable.

## Documentation des versions

Le `README.md` à la racine doit contenir, dans une section visible près du
début, un lien permanent vers la page GitHub qui liste tous les tags du dépôt.
Il doit aussi fournir des liens directs vers les versions stable et de
développement actuellement publiées, lorsqu'elles existent.

À chaque préparation de tag, vérifier et mettre à jour ces liens. Vérifier aussi
que les commandes d'installation documentées installent réellement la version
annoncée : récupérer un installateur depuis un tag ne doit jamais installer en
silence une autre version. Un tag ne doit être présenté comme disponible que si
son code source est effectivement accessible depuis GitHub.

## Convention des préversions

Les tags de préversion suivent durablement la forme `vX.Y.Z.devK`, avec un
point avant `dev` ; par exemple `v0.3.0.dev1`. Employer exactement la même
forme dans la version du paquet (sans le `v`), les installateurs, le README, la
documentation et les liens GitHub.

## Intégration entre branches

Privilégier une pull request documentée pour intégrer une branche de travail,
notamment vers `staging`, puis de `staging` vers `main`. Cette préférence ne
constitue pas une autorisation permanente d'effectuer une opération distante.
