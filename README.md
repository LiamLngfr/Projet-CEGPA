# Projet-CEGPA 
Projet CEGPA Forcalquier 2024. 
Projet commandité par J-F Hangouët pendant le stage à Forcalquier de fin de 1ère année d'ingénieur à l'ENSG Géomatique.

Le projet consistait à approfondir la recherche autour de l’éco-conception de la photogrammétrie aérienne. Avec cet objectif, un des moyens que nous avons trouvé est la création d'un programme qui pourrait calculer les émissions de CO2 ainsi que la consommation énergétique en fonction des différents paramètres utilisés dans les orthophotos. Le but de l’application est essentiellement informatif, il pourrait servir de support pour communiquer sur le poids écologique parfois trop important des manipulations de données photogrammétriques aériennes, et de ce qu’elles impliquent.
Pour ce faire, nous avons développé une application de calcul global des paramètres minimaux de la prise d'orthophotos.
Il est bon de noter que ce sont des estimations avec des valeurs idéales, par exemple l'émission de CO2 ne prend pas en compte le décollage, l'aterrisage ou encore le chemin jusqu'à la zone de vol.
De plus, c'est un code fait par un étudiant en un peu plus d'une semaine, donc des erreurs et des bugs sont possibles. Pour les paramètres des acquisitions il est recommandé de vérifier les valeurs calculées.



# Utilisation 
Pour chaque version : Ouvrir la version voulue, aller dans le dossier du language désiré et exécuter le .exe correspondant. 
Les dossiers ressources contiennent les images explicatives des différentes variables.
La variable Hauteur maximale de terrain correspond à la hauteur maximale de terrain visible en stéréoscopie.
IMPORTANT : Jusqu'à la version 1.3 comprise, entre 2 calculs il est important de faire un reset, sinon certaines valeurs peuvent devenir biaisées.
Recommandé : Version 1.3 +, les versions antérieures contiennent des erreurs lors des calculs.

# Remerciments
Merci à tout les membres de mon groupe, notamment à A.Floch et G.Potel qui m'ont fournis les images, et merci à J-F Hangouët pour tout ses conseils et ses remarques durant toute la phase de préparation et de programmation.
