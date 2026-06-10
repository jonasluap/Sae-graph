# tests/test_motif.py

import unittest
from src.model.motif import Motif
from src.model.case import Case


class TestMotif(unittest.TestCase):
    """
    Tests unitaires de la classe Motif.

    Vérifie :
    - la taille d'un motif ;
    - la complétude d'un motif ;
    - le respect des règles de validité ;
    - la détection des doublons ;
    - la détection des valeurs hors limites.
    """

    def setUp(self):
        """
        Prépare un motif de taille 3 avant chaque test.

        Valeurs autorisées :
        1, 2 et 3.
        """
        self.motif = Motif("test_motif")

        self.c1 = Case(0, 0)
        self.c2 = Case(0, 1)
        self.c3 = Case(1, 0)

        self.motif.add_case(self.c1)
        self.motif.add_case(self.c2)
        self.motif.add_case(self.c3)

    def test_taille_motif(self):
        """
        Vérifie que la taille du motif correspond
        au nombre de cases ajoutées.
        """
        self.assertEqual(self.motif.size(), 3)
        self.assertEqual(len(self.motif.get_cases()), 3)

    def test_motif_incomplet_mais_valide(self):
        """
        Vérifie qu'un motif partiellement rempli
        peut rester valide tant qu'il respecte les règles.
        """
        self.c1.set_value(1)
        self.c2.set_value(2)

        # c3 reste vide
        self.assertFalse(self.motif.is_complete())
        self.assertTrue(self.motif.is_valid())

    def test_motif_complet_et_valide(self):
        """
        Vérifie qu'un motif entièrement rempli
        avec les bonnes valeurs est valide.
        """
        self.c1.set_value(1)
        self.c2.set_value(2)
        self.c3.set_value(3)

        self.assertTrue(self.motif.is_complete())
        self.assertTrue(self.motif.is_valid())

    def test_motif_invalide_doublons(self):
        """
        Vérifie qu'un doublon rend le motif invalide.
        """
        self.c1.set_value(1)
        self.c2.set_value(1)  # Doublon

        self.assertFalse(self.motif.is_valid())

    def test_motif_invalide_hors_limites(self):
        """
        Vérifie qu'une valeur en dehors de l'intervalle
        [1, taille_du_motif] rend le motif invalide.
        """
        # Valeur supérieure à la taille du motif
        self.c1.set_value(4)
        self.assertFalse(self.motif.is_valid())

        # Valeur inférieure à 1
        self.c1.set_value(0)
        self.assertFalse(self.motif.is_valid())


if __name__ == '__main__':
    # Exécution directe des tests du fichier
    unittest.main()