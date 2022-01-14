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

-CmakeLists.txt et package.xml qui sont présents pour le bon fonctionnement du package

-scripts qui contient les deux noeuds de ce package

-launch qui contient le launch challenge2 

-rviz qui contient la configuration utilisé dans le launch de rviz

####Composition du launch

Ce launch lance les différents noeuds nécessaires.

Tout d'abord il fixe l'horloge à celle du rosbag avec ` <param name="/use_sim_time" value="true" />`
Il lance ensuite rviz avec la configuration enregistrée avec `<node pkg="rviz" type="rviz" name="rviz" args="-d $(find grp-marron)/rviz/gmappingbot.rviz"/>
Puis le gmapping avec `<node name="gmapping" pkg="gmapping" type="slam_gmapping"/>`
Puis les deux noeuds du répertoire scripts

####Composition de scripts

#####vision.py

Tout d'abord on lance le noeud et on le déinit en tant que publisher dans le topic `can` et on l'abonne aux deux topics de la caméra nécessaire (c'est à dire l'image et les niveaux de profondeur.
On définit le rate également afin d'éviter de traiter toutes les images mais un nombre réduit qui est suffisant.
On définit également lo et hi pour déterminer l'intervalle de détection HSV.

Les données de profondeurs sont sauvegardées dans une variable globable pour être utilisées dans le traitement de l'image avec :
<br/>`def distance(data):`
    <br/>`global disArr`
    <br/>`disArr=np.array(bridge.imgmsg_to_cv2(data,desired_encoding="passthrough"))`




