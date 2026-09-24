# Méthodologie

## Reproductibilité

Chaque rapport conserve la version de la suite, le profil, la version et le
chemin de Python, l'OS et l'inventaire matériel. L'installation officielle doit
utiliser CPython 3.14.4 géré par `uv` afin d'éviter qu'un Python système différent
modifie les scores.

Réaliser idéalement trois passages du profil `standard`, dans les mêmes
conditions d'alimentation et de refroidissement. Le premier passage peut servir
à chauffer la machine ; comparer ensuite la médiane des passages suivants.

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
