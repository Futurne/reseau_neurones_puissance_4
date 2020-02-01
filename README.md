# reseau_neurones_puissance_4
Premier essai avec les réseaux de neurones - Janvier 2019

Petit projet de 4 jours après la fin des partiels du 1er semestre.
Le but était de créer une IA pour un puissance 4 meilleur que l'IA développée par un ami. Ce projet a été réalisé avec ce même ami, le but était d'apprendre le fonctionnement global d'un réseau de neurones.

Le projet se divise alors en 2 parties, une première partie qui permet la génération et l'entraînement de notre propre réseau de neurones. La deuxième partie consiste à créer de la data d'entraînement pour le réseau.

Finalement, les données ne sont pas de grandes qualités donc on a pas réellement pu tester l'efficacité de notre réseau (c'est aussi possible que ce soit le réseau qui ne fonctionne pas correctement).

# Source principale pour le fonctionnement d'un réseau de neurones
3Blue1Brown a été notre principale source d'information pour la réalisation de notre propre réseau neuronal.
  - https://www.youtube.com/watch?v=aircAruvnKk
  - https://www.youtube.com/watch?v=IHZwWFHWa-w
  - https://www.youtube.com/watch?v=Ilg3gGewQ5U
  - https://www.youtube.com/watch?v=tIeHLnjs5U8
  
# Un mot sur la génération des données d'entraînement
Pour générer le dataset, on a utilisé l'IA de mon ami. Celle-ci était une IA assez basique (mais très efficace), qui regarde tous les coups possibles, avec 3 coups d'avance, et évalue le meilleur des coups. Pour générer une donnée, on mettait l'IA dans une situation de jeu, et on notait son coup. Pour aller plus loin, on lui donnait quelques situations initiales, puis on la faisait jouer contre elle-même et on enregistrait tous les coups.
