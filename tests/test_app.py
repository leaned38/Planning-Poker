"""
@file test_app.py
@brief Contient les tests unitaires pour les fonctions utilitaires et la classe Button de l'application Planning Poker.
@version 1.0
@author ldebret & mblanchon
@date 2024-12-08
"""

# Importation des bibliothèques nécessaires
import unittest
from unittest.mock import MagicMock, patch
from app.utils import load_backlog, save_backlog, calculate_rule_result, Button
import pygame
from unittest import TestCase
from unittest.mock import mock_open, patch
import json

"""
@brief Classe de tests unitaires pour les fonctions utilitaires.
@details Cette classe contient des tests unitaires pour les fonctions utilitaires telles que load_backlog, save_backlog et calculate_rule_result.
"""
class TestUtils(unittest.TestCase):

    """
    @brief Teste le chargement d'un backlog valide.
    @details Ce test vérifie que la fonction load_backlog charge correctement un backlog à partir d'un fichier valide.
    """
    def test_load_backlog_valid(self):
        with patch("builtins.open", unittest.mock.mock_open(read_data='{"Task1": 5, "Task2": 8}')):
            result = load_backlog("dummy_path")
            self.assertEqual(result, {"Task1": 5, "Task2": 8})

    """
    @brief Teste le chargement d'un backlog depuis un fichier inexistant.
    @details Ce test vérifie que load_backlog renvoie un dictionnaire vide lorsqu'il ne trouve pas le fichier.
    """
    def test_load_backlog_invalid_file(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            result = load_backlog("dummy_path")
            self.assertEqual(result, {})

    """
    @brief Teste le chargement d'un backlog avec un contenu JSON invalide.
    @details Ce test vérifie que load_backlog renvoie un dictionnaire vide lorsqu'il rencontre un problème de décodage JSON.
    """
    def test_load_backlog_invalid_json(self):
        with patch("builtins.open", unittest.mock.mock_open(read_data="{invalid_json")):
            result = load_backlog("dummy_path")
            self.assertEqual(result, {})

    """
    @brief Teste la sauvegarde d'un backlog dans un fichier.
    @details Ce test vérifie que la fonction save_backlog écrit correctement le backlog dans un fichier.
    """
    @patch('builtins.open', new_callable=mock_open)
    def test_save_backlog(self, mocked_file):
        backlog = {"Task1": 5}
        save_backlog('dummy_path', backlog)
        mocked_file().write.assert_called_once_with(json.dumps(backlog))

    """
    @brief Teste le calcul du résultat des votes avec la règle "Unanimité" lorsque tous les votes sont identiques.
    @details Ce test vérifie que la fonction calculate_rule_result renvoie le bon résultat lorsque tous les votes sont identiques.
    """
    def test_calculate_rule_result_unanimity_success(self):
        votes = {"Player1": 5, "Player2": 5}
        result = calculate_rule_result(votes, "Unanimité")
        self.assertEqual(result, 5)

    """
    @brief Teste le calcul du résultat des votes avec la règle "Unanimité" lorsque les votes sont différents.
    @details Ce test vérifie que la fonction calculate_rule_result renvoie -1 lorsque les votes ne sont pas unanimes.
    """
    def test_calculate_rule_result_unanimity_failure(self):
        votes = {"Player1": 5, "Player2": 8}
        result = calculate_rule_result(votes, "Unanimité")
        self.assertEqual(result, -1)

    """
    @brief Teste le calcul du résultat des votes avec la règle "Médiane".
    @details Ce test vérifie que la fonction calculate_rule_result renvoie la médiane des votes lorsqu'on utilise la règle "Médiane".
    """
    def test_calculate_rule_result_median(self):
        votes = {"Player1": 5, "Player2": 8, "Player3": 3}
        result = calculate_rule_result(votes, "Médiane")
        self.assertEqual(result, 5)

    """
    @brief Teste le calcul du résultat des votes avec la règle "Moyenne".
    @details Ce test vérifie que la fonction calculate_rule_result renvoie la moyenne des votes lorsqu'on utilise la règle "Moyenne".
    """
    def test_calculate_rule_result_average(self):
        votes = {"Player1": 5, "Player2": 8, "Player3": 3}
        result = calculate_rule_result(votes, "Moyenne")
        self.assertEqual(result, 5.33)

    """
    @brief Teste le calcul du résultat des votes avec un ensemble de votes vide.
    @details Ce test vérifie que la fonction calculate_rule_result renvoie -1 lorsqu'il n'y a pas de votes.
    """
    def test_calculate_rule_result_empty_votes(self):
        votes = {}
        result = calculate_rule_result(votes, "Unanimité")
        self.assertEqual(result, -1)


"""
@brief Classe de tests unitaires pour la classe Button.
@details Cette classe contient des tests unitaires pour la classe Button, vérifiant son affichage et sa fonctionnalité de détection de clic.
"""
class TestButton(unittest.TestCase):
    
    """
    @brief Initialise les tests pour le bouton.
    @details Cette méthode initialise Pygame et crée un bouton avant chaque test.
    """
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.button = Button(100, 100, 200, 50, "Test")

    """
    @brief Nettoie après les tests.
    @details Cette méthode ferme Pygame après chaque test.
    """
    def tearDown(self):
        pygame.quit()

    """
    @brief Teste l'affichage du bouton.
    @details Ce test vérifie que le bouton est correctement dessiné à l'écran.
    """
    def test_button_draw(self):
        self.button.draw(self.screen)
        pygame.display.flip()  # Rendu visuel (non validé ici programatiquement)

    """
    @brief Teste la méthode is_clicked avec un clic valide.
    @details Ce test vérifie que la méthode is_clicked renvoie True lorsque le bouton est cliqué.
    """
    def test_button_is_clicked_true(self):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (150, 125), "button": 1})
        self.assertTrue(self.button.is_clicked(event))

    """
    @brief Teste la méthode is_clicked avec un clic hors du bouton.
    @details Ce test vérifie que la méthode is_clicked renvoie False lorsque le clic est en dehors du bouton.
    """
    def test_button_is_clicked_false(self):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, {"pos": (50, 50), "button": 1})
        self.assertFalse(self.button.is_clicked(event))


if __name__ == "__main__":
    unittest.main()
