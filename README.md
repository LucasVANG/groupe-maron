# Challenge 3 groupe marron

Ceci est la branche du challenge 3 du groupe marron

Pour la vidéo explicative du projet : https://www.youtube.com/watch?v=CnUKza1t8ZE

## Installation et lancement

Une fois la branche récupérée, il faut effectuer catkin_make (et eventuellemet source).

Pour lancer la solution créée il faut lancer la commande

```bash
roslaunch grp-marron challenge3.launch
```

Pour lancer la simulation sans détection d'objet il faut faire la commande 

```bash
roslaunch grp-marrin challenge3_simulation.launch
```
    
    
Pour obtenir la liste des Bouteilles detectées il faut appeler le service `/Liste_Bouteille` avec la commande (seulement disponible avec challenge3.launch)

```bash
rosservice call /Liste_Bouteille 0
```
    
qui  retournera deux varaibles :
-Sucess qui retourne False si il n'y a pas de bouteille, ou True si une bouteille est présente
-Message qui retourne le texte `"Aucune bouteille presente"` ou retourne la liste des bouteilles detectées avec leur coordonnées en x et y sur la map.


## Composition

Le depôt est composé du package grp-marron et de ce README

### Package grp-marron

Ce package est composé de 3 répertoires et 2 fichiers textes :

- CmakeLists.txt et package.xml qui sont présents pour le bon fonctionnement du package

- scripts qui contient les quatres noeuds de ce package

- launch qui contient les deux launch du challenge 3

- rviz qui contient la configuration utilisé dans le launch de rviz

##### Composition du launch

Seulement challenge3.launch sera décrit car challenge3_simulation est le même avec 2 noeuds en moins et lancement d'une simulation plutôt que du robot

Le launch active d'abord le robot, la camera et le laser  avec ces 3 lignes:
	<include file="$(find turtlebot_bringup)/launch/minimal.launch"/>
	<include file="$(find realsense2_camera)/launch/rs_aligned_depth.launch"/>
	<node name="laser" pkg="urg_node" type="urg_node"/>

Il lance ensuite Rviz avec une configuration prédéfini et le gmapping avec :

	<node pkg="rviz" type="rviz" name="rviz" args="-d $(find grp-marron)/rviz/challengebot.rviz"/>
	<node name="gmapping" pkg="gmapping" type="slam_gmapping"/>

En même temps le launch définit la transformation static entre le repère du laser et du robot afin qu'on puisse positionner correctement ce que repère le laser par rapport au robot:

	<node name="base" pkg="tf" type="static_transform_publisher" args=" 0.1 0 0 0 0 0 base_footprint laser 100"/>
	
Ensuite on lance les 4 noeuds qui sont décrits juste après:

	<node name="obstaclelist" pkg="grp-marron" type="obstaclebot.py" output="screen"/>
	<node name="vision" pkg="grp-marron" type="vision.py"/>
    	<node name="marker" pkg="grp-marron" type="markerbottle.py"/>
    	<node name="move" pkg="grp-marron" type="movebot.py"/>
#### Composition de scripts


##### vision.py



Tout d'abord on lance le noeud et on le déinit en tant que publisher dans le topic `can` et on l'abonne aux deux topics de la caméra nécessaire (c'est à dire l'image et les niveaux de profondeur.
On définit le rate également afin d'éviter de traiter toutes les images mais un nombre réduit qui est suffisant.
On définit également lo et hi pour déterminer l'intervalle de détection HSV.

Les données de profondeurs sont sauvegardées dans une variable globable pour être utilisées dans le traitement de l'image avec :

```python
def distance(data):
	global disArr
	disArr=np.array(bridge.imgmsg_to_cv2(data,desired_encoding="passthrough"))
```

On effectue ensuite un seuillage par couleur sur l'image reçu pour seulement récupérer l'objet voulu.

Une fois fait on calcule les coordonnées de l'object detectés dans un repère cartésien avec la caméra comme origine du repère parallele au sol avec la fonction en récupérant la profondeur de l'objet:

```python
def Coor(x,pro):
	angle=43.55*(x-640)/640
	angle=angle*math.pi/180 # passage en radians
	return [math.cos(angle) * pro, math.sin( angle ) * pro-35]
```


Une fois fait on vérifie certaines conditions (la taille de l'objet et sa distance pour limiter les erreurs quand la caméra détecte des objets trop éloignés),on publie ensuite l'objet en tant que PoseStamped dans le topic `can`.



##### markerbottle.py



On inialise le noeud en tant que publisher dans le topic `/bottle` et on l'abonne au topic `can`

A chaque fois qu'il reçoit une position du topic il le transforme du repère de la caméra à celui de la map pour ensuite créer un marker correspondant à cette coordonnées dans la map:

```python
poseMap= tfListener.transformPose("map", data)
x=poseMap.pose.position.x
y=poseMap.pose.position.y
bouteille=initialize_marker(i,x,y)
```

Si il n'y a pas de bouteille sauvegarder on l'enregistre (même si il s'agit d'une erreur de détection cela sera réglé juste aprés)

Sinon
On vérifie si l'objet détecté est proche ou non d'une des bouteilles déjà placées sur la map. Si oui, on cosidère que c'est la même bouteille on additionne les nouvelles coordonnées aux anciennes multipliés par le nombre de détection puis on divise par le nombre de détection+1 pour qu'une valeur fausse ne décale pas le marker de manière exagérée. Sinon on place l'objet comme une nouvelle bouteille. On demande également un nombre minimal de détection pour considérer l'objet détecter comme une bouteille (ici 10 détections). Si cela n'est pas respecté on ne publie pas ce marker car c'est probablement une erreur.

Chaque nouvelle bouteille a ses coordonnées en x,y sauvegarder dans une variable contenant la liste des bouteilles. De plus on vérifie que dans cette liste et dans les markers, il n'y a pas de boublons pour avoir le bon compte de bouteille au final.


Ce noeud gère également le service de d'affichage de la liste des bouteilles cité au début de ce texte en utisant le service SetBool de std_srvs



##### obstaclebot.py



Ce noeud se charge de détecter les obstacles grâce au laser installé sur le robot et de déterminer le comportement à adopter.

Tout d'abord le noeud détermine quel est l'obstacle le plus proche sur la droite et sur la gauche. on récupère ainsi les coordonnées polaires de ces obstacles par rapport au robot:

```python
dis_gau,angle_gau,dis_dro,angle_dro=obs_plus_proches(data) 
```

Une fois cela récupéré on détermine lequel des deux est le plus proche.

Le noeud ensuite regarde la distance, si il est supérieur à 60cm on ignore l'obstacle et on continue a pleine vitesse. Sinon plus l'obstacle est proche, plus l'ordre de vitesse diminue (entre 60-45, entre 45-30 et en dessous de 30).

Quand un obstacle est proche on regarde si il est à droite ou à gauche pour déterminer dans quel sens tourner.


Ensuite le noeud regard si l'obstacle à droite et à gauche forment un coin. Si oui le noeud déterminera si il est possible de continuer dans cet espace réduit ou si il faut faire demi-tour car il n'y a pas assez de place pour le robot.

Le noeud envoie ensuite ses ordres dans un message sous forme de 2 int au noeud movebot



##### movebot.py



Ce noeud récupère les ordres de obstaclebot en tant que int et se contente de les diviser par 100 pour avoir la valeur voulue dans la vitesse linéaire et angulaire.

Ce noeud garde en mémoire également la vitesse linéaire et angulaire du robot. Lorsque qu'il reçoit des nouveaux ordres de vitesse, il adapte ses valeurs par incréments pour atteindre la vitesse voulue:

 ```python
 
def adapt_vit(data): #Pour incrémenter lentement la vitesse
    global vitesse 
    if(vitesse<data):
        vitesse+=0.04
    elif(vitesse>data):
        vitesse-=0.04
    return vitesse

def adapt_tourne(data):
    global angulaire
    if(angulaire<data):
        angulaire+=0.05
    elif(angulaire>data):
        angulaire-=0.05
    return angulaire
```
Cela permet d'avoir une navigation plus fluide du robot en évitant des changement brusque du à des changements de vitesse trop rapide. Une fois fait le noeud publie ses ordres de vitesses dans cmd_vel_mux/input/navi pour que le robot s'adapte à la vitesse voulue
    
