"""
@file utils.py
@brief Contient des fonctions utilitaires pour charger et sauvegarder des données (backlog, cartes) et calculer les résultats des votes.
@version 1.0
@author ldebret & mblanchon
@date 2024-12-08
"""

# Importation des bibliothèques nécessaires
import json
import statistics
import pygame

def load_backlog(filepath="backlog_json/backlog_exemple.json"):
    """
    @brief Charge un backlog depuis un fichier JSON.
    @details Cette fonction tente de charger un fichier JSON contenant un backlog. Si le fichier n'est pas trouvé ou si une erreur de décodage se produit, un dictionnaire vide est retourné.
    @param filepath Le chemin d'accès au fichier JSON contenant le backlog (par défaut, "backlog_json/backlog_exemple.json").
    @return Un dictionnaire représentant le backlog chargé, ou un dictionnaire vide en cas d'erreur.
    """
    try:
        print(f"Tentative de chargement du fichier : {filepath}")
        with open(filepath, "r", encoding='utf-8') as file:
            data = json.load(file)
            print(f"Fichier chargé avec succès. Contenu : {data}")
            return data
    except FileNotFoundError:
        print(f"Fichier non trouvé : {filepath}")
        return {}
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON : {e}")
        return {}

def save_backlog(file_path, backlog):
    """
    @brief Sauvegarde un backlog dans un fichier JSON.
    @details Cette fonction prend un dictionnaire représentant un backlog et l'enregistre sous forme de chaîne JSON dans un fichier.
    @param file_path Le chemin d'accès du fichier où sauvegarder le backlog.
    @param backlog Le dictionnaire représentant le backlog à sauvegarder.
    """
    with open(file_path, 'w') as f:
        json_data = json.dumps(backlog)
        f.write(json_data)


def load_cards(filepath):
    """
    @brief Charge les cartes depuis un fichier JSON.
    @details Cette fonction tente de charger un fichier JSON contenant les cartes. Si le fichier est introuvable ou invalide, un jeu de cartes par défaut est retourné.
    @param filepath Le chemin d'accès du dossier contenant le fichier JSON des cartes.
    @return La liste des cartes, ou un jeu de cartes par défaut si le fichier est introuvable ou invalide.
    """
    try:
        with open(f"{filepath}/cards.json", "r") as file:
            data = json.load(file)
            return data.get("cards", ["0", "1", "2", "3", "5", "8", "13", "20", "40", "100", "café", "intero"])
    except FileNotFoundError:
        print("Cartes introuvables, utilisation des cartes par défaut.")
        return ["0", "1", "2", "3", "5", "8", "13", "20", "40", "100", "café", "intero"]

def calculate_rule_result(votes, rule):
    """
    @brief Calcule le résultat des votes en fonction de la règle choisie.
    @details Cette fonction évalue les votes des joueurs selon une règle spécifiée ("Unanimité", "Médiane", "Moyenne") et renvoie le résultat.
    @param votes Un dictionnaire contenant les votes des joueurs, où la clé est le nom du joueur et la valeur est le vote (un entier ou une chaîne).
    @param rule La règle à appliquer pour calculer le résultat ("Unanimité", "Médiane", "Moyenne").
    @return Le résultat calculé en fonction de la règle. Si aucune règle ne correspond, retourne -1.
    """
    values = [v for v in votes.values() if isinstance(v, int)]
    if not values:
        return -1  # No valid votes
    if rule == "Unanimité":
        return values[0] if len(set(values)) == 1 else -1
    elif rule == "Médiane":
        return statistics.median(values)
    elif rule == "Moyenne":
        return round(sum(values) / len(values), 2)
    return -1


# --- Classe Button ---

class Button:
    """
    @class Button
    @brief Classe représentant un bouton dans l'interface utilisateur à afficher à l'écran.
    @details Cette classe gère l'affichage d'un bouton ainsi que les interactions de l'utilisateur (clics).
    """
    
    def __init__(self, x, y, width, height, text, color=(0, 128, 0), hover_color=(0, 255, 0), text_color=(255, 255, 255)):
        """
        @brief Initialise un bouton avec des propriétés de position, taille et texte.
        @param x La coordonnée x du coin supérieur gauche du bouton.
        @param y La coordonnée y du coin supérieur gauche du bouton.
        @param width La largeur du bouton.
        @param height La hauteur du bouton.
        @param text Le texte à afficher sur le bouton.
        @param color La couleur de base du bouton (par défaut, vert).
        @param hover_color La couleur du bouton lorsque la souris survole celui-ci (par défaut, vert clair).
        @param text_color La couleur du texte sur le bouton (par défaut, blanc).
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        """
        @brief Dessine le bouton à l'écran.
        @param screen L'écran Pygame sur lequel dessiner le bouton.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        # Dessin du texte
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        """
        @brief Vérifie si le bouton a été cliqué.
        @param event L'événement de la souris à analyser.
        @return True si le bouton a été cliqué, sinon False.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic gauche
            return self.rect.collidepoint(event.pos)
        return False
