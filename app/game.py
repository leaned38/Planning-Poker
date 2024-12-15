"""
@file game.py
@brief Gère le déroulement du jeu de Planning Poker.
@version 1.1 (amélioré)
@date 2024-12-08
"""

# Importation des bibliothèques
import pygame
from app.utils import save_backlog, calculate_rule_result, Button

"""
@brief Fonction principale qui gère l'exécution du jeu de Planning Poker.
@details Cette fonction initialise le jeu, affiche les cartes et permet aux joueurs de voter. 
Elle gère également les événements liés à l'affichage des résultats et à la navigation entre les tâches.
@param screen L'écran Pygame sur lequel afficher l'interface du jeu.
@param backlog Liste des tâches à estimer.
@param players Liste des joueurs participant au jeu.
@param rule La règle utilisée pour calculer les résultats des votes.
"""
def run_game(screen, backlog, players, rule):
    pygame.init()

    # Polices basiques
    roboto_clsq = "assets/fonts/Roboto/Roboto-Medium.ttf"
    roboto_itlq = "assets/fonts/Roboto/Roboto-Italic.ttf"
    roboto_carte = "assets/fonts/Roboto/Roboto-MediumItalic.ttf"
    title_font = pygame.font.SysFont("Arial", 48, bold=True)  
    text_font = pygame.font.Font(roboto_clsq, 32)  
    text_font_itlq = pygame.font.Font(roboto_itlq, 32)  
    text_font_carte = pygame.font.Font(roboto_carte, 35) 
    player_text_font = pygame.font.SysFont("Arial", 32, bold=True)  

    running = True
    show_pause_message = False
    screen_width, screen_height = screen.get_size()


    # Charger les images des cartes
    card_values = ["0", "1", "2", "3", "5", "8", "13", "20", "40", "100", "cafe", "intero"]
    card_images = {value: pygame.image.load(f"assets/cards/{value}.png") for value in card_values}

    # Positionner les cartes sur deux lignes
    card_positions = {}
    x_offset = 150
    y_offset_top = 300
    y_offset_bottom = 450
    card_width, card_height = 80, 120  # Taille des cartes

    # Répartir les cartes sur deux lignes
    for i, value in enumerate(card_values):
        if i < len(card_values) // 2:
            card_positions[value] = (x_offset + i * (card_width + 100), y_offset_top)
        else:
            card_positions[value] = (x_offset + (i - len(card_values) // 2) * (card_width + 100), y_offset_bottom)

    tasks = list(backlog.keys())
    current_task_index = 0
    votes = {}
    current_player_index = 0

    # Couleurs et styles
    title_color = (34, 112, 147)  # Bleu 
    player_color = (188, 108, 37)  # Marron 
    text_color = (221, 161, 94)   # Orange 

    # Création des boutons "Révéler les cartes" et "Suivant"
    reveal_button = Button((screen_width - 300) // 2, 600, 300, 80, "Révéler les cartes")
    next_button = Button(600, 700, 200, 50, "Suivant")
    all_voted = False
    cards_revealed = False
    show_pause_message = False

    while running:
        screen.fill((254, 250, 224))  # Couleur de fond FEFAE0
        
        # Affiche le titre centré
        title_text = title_font.render("Planning Poker", True, title_color)
        screen.blit(title_text, (screen.get_width() // 2 - title_text.get_width() // 2, 20))

        # Affiche la tâche actuelle
        task = tasks[current_task_index]
        task_text = text_font.render(f"Tâche: {task}", True, text_color)
        screen.blit(task_text, (50, 100))

        # Affiche le joueur actuel
        current_player = players[current_player_index] if current_player_index < len(players) else "Tous ont voté"
        player_text = player_text_font.render(f"Joueur actuel: {current_player}", True, player_color)
        screen.blit(player_text, (screen.get_width() // 2 - player_text.get_width() // 2, 230))

        # Affiche les cartes disponibles si tous n'ont pas voté
        if not all_voted:
            for value, position in card_positions.items():
                screen.blit(card_images[value], position)

        # Affiche les votes déjà enregistrés ou dévoilés
        for i, player in enumerate(players):
            if cards_revealed:
                vote = votes.get(player, "Pas encore voté")
                vote_text = text_font_carte.render(f"{player} a choisi la carte {vote}", True, title_color)
                screen.blit(vote_text, (screen.get_width() // 2 - vote_text.get_width() // 2, 280 + i * 40))
            else: 
                vote = "?"
                vote_text = text_font_itlq.render(f"{player}: {vote}", True, text_color)
                screen.blit(vote_text, (50, 150 + i * 30))
            
            
        # for i, player in enumerate(players):
        #     vote = votes.get(player, "Pas encore voté") if cards_revealed else "?"
        #     vote_text = text_font_itlq.render(f"{player}: {vote}", True, text_color)
        #     screen.blit(vote_text, (700, 350 + i * 30)) if cards_revealed else screen.blit(vote_text, (50, 150 + i * 30))

        # Affiche les boutons
        if all_voted and not cards_revealed:
            reveal_button.draw(screen)
        if all_voted and cards_revealed and not show_pause_message:
            next_button.draw(screen)

        # Affiche le message de pause café si nécessaire
        if show_pause_message:
            pause_font = pygame.font.SysFont("Arial", 48)
            pause_text = pause_font.render("Pause Café !", True, (255, 0, 0))
            screen.blit(pause_text, (screen.get_width() // 2 - pause_text.get_width() // 2, 150))

        pygame.display.flip()

        # Gestion des événements
                # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Sauvegarde le backlog avant la fermeture du jeu
                save_backlog(backlog=backlog)
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos

                # Enregistre les votes si c'est le tour des joueurs
                if not all_voted:
                    # On récupère la position de la souris à chaque clic
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Reset le curseur à la flèche
                    for value, position in card_positions.items():
                        x, y = position
                        if x <= mouse_x <= x + card_width and y <= mouse_y <= y + card_height:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Changer le curseur en main
                            votes[current_player] = "Café" if value == "cafe" else "Intero" if value == "intero" else int(value)
                            current_player_index += 1

                            # Vérifie si tous les joueurs ont voté
                            if current_player_index >= len(players):
                                all_voted = True
                            break

                # Bouton "Révéler les cartes"
                if all_voted and not cards_revealed and reveal_button.is_clicked(event):
                    cards_revealed = True

                # Bouton "Suivant"
                if all_voted and cards_revealed and next_button.is_clicked(event):
                    result = calculate_rule_result(votes, rule)
                    if result == -1:
                        # Réinitialiser les votes et l'index des joueurs
                        votes = {}
                        current_player_index = 0
                        all_voted = False
                        cards_revealed = False
                    elif any(v == "Café" for v in votes.values()):
                        show_pause_message = True
                        pygame.time.set_timer(pygame.USEREVENT, 3000)  # Afficher le message pendant 3 secondes
                    else:
                        backlog[task] = result
                        current_task_index += 1
                        votes = {}
                        current_player_index = 0
                        all_voted = False
                        cards_revealed = False

                        # Vérifie si toutes les tâches sont terminées
                        if current_task_index >= len(tasks):
                            save_backlog(backlog=backlog)
                            running = False

            elif event.type == pygame.USEREVENT and show_pause_message:
                # Masquer le message de pause café après 3 secondes
                show_pause_message = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_backlog(backlog=backlog)
                    running = False

        # Changer le curseur à chaque itération pour gérer le survol
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Reset le curseur à la flèche
        for value, position in card_positions.items():
            x, y = position
            if x <= mouse_x <= x + card_width and y <= mouse_y <= y + card_height:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Change le curseur en main quand il survole une carte
                break
    
    
    
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Planning Poker")
    run_game(screen, {"Tâche 1": None, "Tâche 2": None}, ["Alice", "Bob"], "Médiane")
    pygame.quit()
