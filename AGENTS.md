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

## Intégration entre branches

Privilégier une pull request documentée pour intégrer une branche de travail,
notamment vers `staging`, puis de `staging` vers `main`. Cette préférence ne
constitue pas une autorisation permanente d'effectuer une opération distante.
