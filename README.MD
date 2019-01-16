# PyTable

Bienvenue sur le dépot de PyTable, un éditeur pour l'environement du robot :)

## Getting started

### 1. Installation des outils nécessaires

Pour installer python avec les bonnes librairies, tapez la commande suivante :

```
sudo apt-get install python3 python3-pip python3-tk python3-pil.imagetk
```

Clonez ensuite le repository sur votre machine

```
git clone https://github.com/ClubRobotInsat/pytable.git
```

Enfin, pour installer toutes les dépendances nécessaires au projet :

```
cd pytable/
pip3 install -r requirements.txt
```

### 2. Lancer l'application

Vous pouvez lancer l'éditeur pytable simplement avec la commande suivante (à executer dans le dossier qui contient le repository) :

```
python3 -m pytable
```

### 3. Lancer les tests unitaires

Pour lancer les tests unitaires, il suffit de lancer la commande :

```
python3 -m unittest tests
```
