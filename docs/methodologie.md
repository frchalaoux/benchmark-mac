# Méthodologie

## Reproductibilité

Chaque rapport conserve la version de la suite, le profil, la version et le
chemin de Python, l'OS et l'inventaire matériel. L'installation officielle doit
utiliser CPython 3.14.4 géré par `uv` afin d'éviter qu'un Python système différent
modifie les scores.

Le logiciel réalise trois passages par défaut et retient leur médiane. Il
conserve les valeurs individuelles, le minimum, le maximum et l'étendue relative.
Pour une étude importante, demander cinq passages du profil `standard`, dans les
mêmes conditions d'alimentation et de refroidissement.

La suite capture aussi, lorsque le système l'expose sans privilège, la source
d'alimentation, la limitation thermique du CPU et une température avant/après.
Elle avertit en cas de batterie, changement d'alimentation, limitation de
fréquence, hausse d'au moins 10 °C ou température finale d'au moins 85 °C. Ces
informations restent indisponibles sur certaines machines.

Le benchmark `cpu.multicore` mesure volontairement le débit agrégé avec un
processus par processeur logique disponible. Son paramètre `workers` décrit donc
la machine et peut différer entre deux rapports. Les autres paramètres de
protocole doivent rester identiques.

Une différence est déclarée non concluante lorsque les plages min–max de deux
machines se chevauchent. Les termes « équivalent », « légère », « nette »,
« importante » et « changement de catégorie » correspondent respectivement aux
seuils 5 %, 15 %, 30 % et 60 %. Ce vocabulaire facilite la lecture ; il ne
constitue pas une loi générale de perception humaine.

## Agrégation et temps équivalents

Chaque score est divisé par celui de la première machine, qui devient l'indice
100. Les scénarios combinent ensuite leurs rapports par moyenne géométrique
pondérée. L'utilisateur peut pondérer les scénarios ; aucune pondération n'est
présentée comme universelle.

Pour une métrique de débit, le temps équivalent est calculé par
`temps référence / rapport de performance`. Il illustre une quantité de travail
identique, mais ne prédit pas exactement la durée d'une application réelle.

## Ce que mesurent les groupes

Le groupe CPU mélange du Python pur et des bibliothèques natives afin de couvrir
la réactivité de l'interpréteur, les flottants, la cryptographie, la compression
et la montée en charge multicœur. Le test mémoire mesure une copie séquentielle.
Le stockage utilise des fichiers temporaires sur le chemin choisi, avec
synchronisation des écritures. JSON et SQLite représentent des traitements
applicatifs fréquents.

## Limites

Les caches du système peuvent augmenter le résultat de lecture disque. Les
scores Python ne remplacent pas les outils spécialisés pour le GPU, l'encodage
vidéo matériel, les moteurs 3D, l'autonomie ou les performances thermiques
prolongées. Ces dimensions doivent être ajoutées comme scénarios optionnels avec
une dépendance et une version figées.
