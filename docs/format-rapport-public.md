# Format des rapports publics

## Portée

Le format `perfcomparator-public-report`, version `1`, est le seul format prévu
pour le futur catalogue communautaire. Il est construit depuis un rapport privé
par `perfcomparator export-public`; le fichier privé ne doit jamais être ajouté
au catalogue.

Cette première version accepte uniquement le schéma privé `4` et le protocole
de mesure `0.3.0`. Un format inconnu, un protocole incompatible, un benchmark
inconnu, un résultat dupliqué ou un rapport sans résultat est refusé plutôt que
d'être exporté avec une anonymisation incertaine.

## Liste blanche

Le fichier public conserve seulement :

- l'identifiant et la version du format public ;
- la licence `CC0-1.0` et l'état `community-unverified` ;
- les versions du schéma source, de la suite et du protocole ;
- le profil, le nombre de passages et les benchmarks demandés ;
- la famille du système, l'architecture, le processeur, les nombres de cœurs,
  la quantité de mémoire, les GPU et l'environnement Python ;
- le booléen indiquant si le contrôle initial était satisfaisant ;
- les scores, unités, paramètres comparatifs, échantillons et dispersions ;
- les identifiants des benchmarks en échec, sans leur message libre.

Tout champ non déclaré est interdit par le schéma public. Les intitulés des
benchmarks sont repris du catalogue de la suite, et non du texte potentiellement
modifié dans le rapport source.

Sont notamment absents :

- le label libre et la date de la campagne ;
- le chemin de l'exécutable Python ;
- les PID, noms de processus et métriques de charge détaillées ;
- les avertissements et messages d'erreur libres ;
- la version détaillée du système et du noyau ;
- les capacités totale et libre du disque ;
- les instantanés d'alimentation et de température.

## Identifiant déterministe

`report_id` est la somme SHA-256 du contenu public canonique, préfixée par
`sha256:`. Elle sert à détecter les doublons et change si une donnée comparative
change. Elle n'est dérivée d'aucun compte, adresse réseau, numéro de série ou
identifiant matériel. Le même rapport source produit donc exactement le même
export et le même identifiant.

## Licence, consentement et authenticité

L'export exige `--accept-cc0`. Cette confirmation indique que l'auteur accepte
la diffusion des données exportées sous [CC0 1.0](https://creativecommons.org/publicdomain/zero/1.0/).
La commande écrit uniquement le chemin demandé et n'effectue aucune connexion
réseau.

Le matériel et les scores restent naturellement descriptifs d'une configuration.
L'export retire les données locales inutiles, mais ne promet pas l'anonymat face
à une combinaison matérielle rare. Il faut relire le JSON avant publication.

Enfin, un rapport conforme peut être falsifié. `community-unverified` signifie
que le schéma est exploitable, pas que les performances ou la machine ont été
certifiées.
