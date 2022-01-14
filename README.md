# Challenge 2 groupe marron

Ceci est la branche du challenge 2 du groupe marron

## Installation et lancement

Une fois la branche récupérée, il faut effectuer catkin_make (et eventuellemet source).

Pour lancer la solution créée il faut lancer la commande    `roslaunch grp-marron challenge2.launch`

Ce launch utilise l'horloge du rosbag lancée. Ainsi pour lancer le rosbag correctement il faut faire la commande `rosbag play --clock nom_rosbag`

Pour obtenir la liste des Bouteilles detectées il faut appeler le service `/Liste_Bouteille` avec la commande `rosservice call /Liste_Bouteille 0` qui  retournera deux varaibles :
-Sucess qui retourne False si il n'y a pas de bouteille, ou True si une bouteille est présente
-Message qui retourne le texte `"Aucune bouteille presente"` ou retourne la liste des bouteilles detectées avec leur coordonnées en x et y sur la map.


## Composition

    Le depôt est composé du package grp-marron et de ce README

### Package grp-marron

    Ce package est composé de 3 répertoires et 2 fichiers textes :

    -CmakeLists.txt et package.xml qui sont présents pour le bon fonctionnement du package

    -scripts qui contient les deux noeuds de ce package

    -launch qui contient le launch challenge2 

    -rviz qui contient la configuration utilisé dans le launch de rviz

##### Composition du launch

    Ce launch lance les différents noeuds nécessaires.

    Tout d'abord il fixe l'horloge à celle du rosbag avec ` <param name="/use_sim_time" value="true" />`
    Il lance ensuite rviz avec la configuration enregistrée avec `<node pkg="rviz" type="rviz" name="rviz" args="-d $(find grp-marron)/rviz/gmappingbot.rviz"/>
    Puis le gmapping avec `<node name="gmapping" pkg="gmapping" type="slam_gmapping"/>`
    Puis les deux noeuds du répertoire scripts

#### Composition de scripts

##### vision.py

    Tout d'abord on lance le noeud et on le déinit en tant que publisher dans le topic `can` et on l'abonne aux deux topics de la caméra nécessaire (c'est à dire l'image et les niveaux de profondeur.
    On définit le rate également afin d'éviter de traiter toutes les images mais un nombre réduit qui est suffisant.
    On définit également lo et hi pour déterminer l'intervalle de détection HSV.

    Les données de profondeurs sont sauvegardées dans une variable globable pour être utilisées dans le traitement de l'image avec :
    <br/>`def distance(data):`
        <br/>`global disArr`
        <br/>`disArr=np.array(bridge.imgmsg_to_cv2(data,desired_encoding="passthrough"))`

    On effectue ensuite un seuillage par couleur sur l'image reçu pour seulement récupérer l'objet voulu.

    Une fois fait on calcule les coordonnées de l'object detectés dans un repère cartésien avec la caméra comme origine du repère parallele au sol avec la fonction en récupérant la profondeur de l'objet:
    <br/>`def Coor(x,pro):`
        <br/>`angle=43.55*(x-640)/640`
        <br/>`angle=angle*math.pi/180 # passage en radians`
        <br/>`return [math.cos(angle) * pro, math.sin( angle ) * pro-35] ` 


    Une fois fait on vérifie certaines conditions (la taille de l'objet et sa distance pour limiter les erreurs quand la caméra détecte des objets trop éloignés),on publie ensuite l'objet en tant que PoseStamped dans le topic `can`.

##### markerbottle.py

    On inialise le noeud en tant que publisher dans le topic `/bottle` et on l'abonne au topic `can`

    A chaque fois qu'il reçoit une position du topic il le transforme du repère de la caméra à celui de la map pour ensuite créer un marker correspondant à cette coordonnées dans la map:
    <br/>`poseMap= tfListener.transformPose("map", data)`
    <br/>`x=poseMap.pose.position.x`
    <br/>`y=poseMap.pose.position.y`
    <br/>`bouteille=initialize_marker(i,x,y)`

    Si il n'y a pas de bouteille sauvegarder on l'enregistre (même si il s'agit d'une erreur de détection cela sera réglé juste aprés)

    Sinon
    On vérifie si l'objet détecté est proch ou non d'une des bouteilles déjà placées sur la map. Si oui, on cosidère que c'est la même bouteille et on fait la moyenne de leur coordonnées pour avoir une position plus précise. Sinon on place l'objet comme une nouvelle bouteille. On demande également un nombre minimal de détection pour considérer l'objet détecter comme une bouteille (ici 10 détections). Si cela n'est pas respecté on ne publie pas ce marker car c'est probablement une erreur.

    Chaque nouvelle bouteille a ses coordonnées en x,y sauvegarder dans une variable contenant la liste des bouteilles. De plus on vérifie que dans cette liste et dans les markers, il n'y a pas de boublons pour avoir le bon compte de bouteille au final.


    Ce noeud gère également le service de d'affichage de la liste des bouteilles cité au début de ce texte en utisant le service SetBool de std_srvs
    
  







