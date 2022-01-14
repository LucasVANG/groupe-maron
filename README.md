# Challenge 2 groupe marron

Ceci est la branche du challenge 2 du groupe marron

## Installation

Une fois la branche récupérée, il faut effectuer catkin_make (et eventuellemet source).

Pour lancer la solution créée il faut lancer la commande `roslaunch grp-marron challenge2.launch`

Ce launch utilise l'horloge du rosbag lancée. Ainsi pour lancer le rosbag correctement il faut faire la commande `rosbag play --clock nom_rosbag`

## Composition

Le depôt est composé du package grp-marron et de ce README

### Package grp-marron

Ce package est composé de 3 répertoires et 2 fichiers textes :

>CmakeLists.txt et package.xml qui sont présents pour le bon fonctionnement du package
>scripts qui contient les deux noeuds de ce package
>launch qui contient le launch challenge2 
>rviz qui contient la configuration utilisé dans le launch de rviz
