"""
@file menu.py
@brief Gère l'affichage du menu principal de l'application Planning Poker.
@version 1.0
@author ldebret & mblanchon
@date 2024-12-08
"""

# Importation des bibliothèques
import pygame
from app.settings import run_settings
from app.utils import Button

"""
@brief Fonction principale du menu de l'application Planning Poker.
@details Cette fonction gère l'affichage du menu principal, avec les options "Démarrer une partie" et "Quitter l'application".
Elle attend l'interaction de l'utilisateur et lance l'action correspondante (démarrer le jeu ou quitter l'application).
@param screen L'écran Pygame sur lequel afficher le menu.
"""
def run_menu(screen):
    running = True
    font = pygame.font.Font(None, 36)
    screen_width, screen_height = screen.get_size()
    title_color = (34, 112, 147)  # Bleu 
    title_font = pygame.font.SysFont("Arial", 48, bold=True)  
    button_color = (188, 108, 37)  # Marron
    hover_color = (210, 140, 75)  #marron plus clair survol


    # Création des boutons "Démarrer une partie" et "Quitter l'application"
    button_width, button_height = 450, 110  # Nouveau taille pour le bouton plus gros
    start_button = Button((screen_width - button_width) // 2, 250, button_width, button_height, "Démarrer une partie", color=button_color, hover_color=hover_color)
    
    quit_button = Button((screen_width - button_width) // 2, 400, button_width, button_height, "Quitter l'application", color=button_color, hover_color=hover_color)
    
    




    while running:
        screen.fill((254, 250, 224)) 
        
        # Affiche le titre du menu
        title_text = title_font.render("Planning Poker - Menu Principal", True, title_color)
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 20))
        
        # Affiche les boutons
        start_button.draw(screen)
        quit_button.draw(screen)

        pygame.display.flip()
        
        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quitte l'application
                running = False
            if start_button.is_clicked(event):
                # Lance les paramètres du jeu
                run_settings(screen)
            if quit_button.is_clicked(event):
                # Quitte l'application
                running = False

        pygame.time.wait(100)
