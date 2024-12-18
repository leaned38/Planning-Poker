# Planning-Poker

## Description
Ce projet est une application développée en Python, avec Pygame permettant d’estimer les coûts de tâches dans un projet, de façon ludique et collaborative. 

## Fonctionnalités principales de l'application 
- **Gestion du backlog** : importer un backlog, format JSON, et afficher les tâches à estimer. 
-   **Moment d’estimation** : chaque joueur peut estimer, le coût d’une tâche, selon ses propres critères. Ensuite, le consensus est automatiquement calculé. 
-   **Modes de jeu** : il y a plusieurs modes de jeu disponibles : « Unanimité », « Médiane », « Moyenne » 
-   **Interface utilisateur** : l’interface est simple, minimaliste et interactive, ce qui permet une prise en main facile.

## Pré-requis 
Pour le bon déroulement, assurez-vous d’avoir installé sur votre machine : 
-   **Python**
-   **La bibliothèque pygame**
Pour installer pygame, vous pouvez exécuter cette commande dans votre terminal :
```bash
pip install pygame
```

## Lancement de l'application
- **ETAPE 1 : Cloner le projet**
Pour cela, vous pouvez exécuter ces commandes dans le terminal :
```bash
git clone https://github.com/leaned38/Planning-Poker.git
cd Planning-Poker
```
- **ETAPE 2 : Lancer l’application**
Pour lancer l’application, vous pouvez exécuter cette commande :
```bash
python main.py
```
- **ETAPE 3 : Naviguer dans l’application**
Pour naviguer dans l’application, il vous suffit de suivre les instructions affichées dans la fenêtre. Il faut d’abord commencer une partie. Ensuite, chargez un backlog puis renseignez les noms des joueurs. Vous pouvez choisir le mode de jeu. Enfin, pour débuter la partie, cliquez sur « commencer la partie ». 
La partie est lancée. Attendez votre tour et choisissez la carte adaptée selon vous à la tâche indiquée. Pour le mode Unanimité, tant que l’unanimité ne l’emporte pas, la tâche sera remise en jeu. Une fois l’unanimité trouvée, une nouvelle tâche vous est proposée et à vous de voter à nouveau en fonction.

## Tests unitaires
Les tests sont définis dans le dossier tests. Pour les exécuter : python –m unittest discover –s tests
