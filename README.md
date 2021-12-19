Ceci est le README.md du groupe marron pour le challenge 1

le package grp-marron est composé de plusieurs répertoires


Tout d'abord le répertoire scripts contenant 4 .py

move.py et movebot.py sont quasi identiques seuls certains paremètres changent pour être mieux adapter à la simulation et l'autre le control du turtlebot
obstacle.py et obstaclebot.py sont également quasi identiques avec quelques paramètres différents.

Nous avons divisé cela en deux groupes de noeuds différents afin de pouvoir avoir des paramètres différents

Le répertoire launch qui contient les deux .launch demandés utilisant les 4 noeuds (quand on appelle les launch il faut préciser rviz:= True/False pour lancer rviz ou non)

Le répertoire rviz qui contient les configurations de rviz pour les deux launchs


Afin de faire en sorte que le robot parcourt la totalité de son environnement nous avons essayé différents stratégie mais la seule que nous avons réussi à implémenter
dans la simulation (pas dans le controle direct) et de faire en sorte que le robot fasse des virages assez violent pour qu'il ricoche sur les obstacles. Cela n'était pas possible
avec le controle direct car ces virages étant assez brusques, il faisait tomber le pc qui controlé le robot au dessus
