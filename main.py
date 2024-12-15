"""
@file main.py
@brief Programme principal de l'application Planning Poker.
@version 1.0
@author ldebret & mblanchon
@date 2024-12-08
"""

# Importation des bibliothèques
import pygame
from app.menu import run_menu
from app.utils import save_backlog

# Initialisation de Pygame
pygame.init()

# Taille de la fenêtre de l'application
WINDOW_SIZE = (1400, 800)
# Création de la fenêtre de l'application avec la taille spécifiée
screen = pygame.display.set_mode(WINDOW_SIZE)
# Définition du titre de la fenêtre
pygame.display.set_caption("Planning Poker")

"""
@brief Fonction principale exécutant l'application.
@details Cette fonction gère le menu principal du jeu et capture les interruptions clavier (Ctrl+C).
En cas de fermeture, Pygame est correctement quitté.
"""
def main():
    try:
        # Exécution du menu principal de l'application
        run_menu(screen)
    except KeyboardInterrupt:
        # Capture de l'interruption clavier (Ctrl+C)
        print("Fin de l'application.")
    finally:
        # Fermeture de Pygame après la fin du programme
        pygame.quit()

# Condition pour exécuter le programme si ce fichier est le principal
if __name__ == "__main__":
    # Appel de la fonction principale
    main()
