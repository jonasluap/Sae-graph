# tests/test_case.py

import unittest
from src.model.case import Case


class TestCase(unittest.TestCase):
    """
    Tests unitaires de la classe Case.

    Vérifie :
    - la création des cases ;
    - la gestion des valeurs ;
    - la protection des cases fixées.
    """

    def test_creation_case_vide(self):
        """
        Vérifie qu'une case vide est correctement initialisée.
        """
        c = Case(1, 2)

        self.assertEqual(c.get_position(), (1, 2))
        self.assertIsNone(c.get_value())
        self.assertFalse(c.is_fixed())

    def test_creation_case_fixee(self):
        """
        Vérifie qu'une case préremplie conserve sa valeur
        et est marquée comme fixée.
        """
        c = Case(0, 0, valeur=5, fixee=True)

        self.assertEqual(c.get_value(), 5)
        self.assertTrue(c.is_fixed())

    def test_modification_case_libre(self):
        """
        Vérifie qu'une case libre peut être modifiée
        puis vidée.
        """
        c = Case(3, 3)

        c.set_value(4)
        self.assertEqual(c.get_value(), 4)

        c.set_value(None)
        self.assertIsNone(c.get_value())

    def test_protection_case_fixee(self):
        """
        Vérifie qu'une case fixée ne peut pas être modifiée.
        """
        c = Case(2, 2, valeur=8, fixee=True)

        c.set_value(3)

        # La valeur initiale doit rester inchangée
        self.assertEqual(c.get_value(), 8)


if __name__ == '__main__':
    # Exécution des tests du fichier
    unittest.main()