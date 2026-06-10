# tests/test_motif.py
import unittest
from src.model.motif import Motif
from src.model.case import Case

class TestMotif(unittest.TestCase):
    
    def setUp(self):
        self.motif = Motif("test_motif")
        self.c1 = Case(0, 0)
        self.c2 = Case(0, 1)
        self.c3 = Case(1, 0)
        
        self.motif.add_case(self.c1)
        self.motif.add_case(self.c2)
        self.motif.add_case(self.c3)
        # Taille du motif = 3 (valeurs valides: 1, 2, 3)

    def test_taille_motif(self):
        self.assertEqual(self.motif.size(), 3)
        self.assertEqual(len(self.motif.get_cases()), 3)

    def test_motif_incomplet_mais_valide(self):
        self.c1.set_value(1)
        self.c2.set_value(2)
        # c3 est vide (None)
        self.assertFalse(self.motif.is_complete())
        self.assertTrue(self.motif.is_valid())

    def test_motif_complet_et_valide(self):
        self.c1.set_value(1)
        self.c2.set_value(2)
        self.c3.set_value(3)
        self.assertTrue(self.motif.is_complete())
        self.assertTrue(self.motif.is_valid())

    def test_motif_invalide_doublons(self):
        self.c1.set_value(1)
        self.c2.set_value(1) # Doublon
        self.assertFalse(self.motif.is_valid())

    def test_motif_invalide_hors_limites(self):
        self.c1.set_value(4) # 4 est > à la taille du motif (3)
        self.assertFalse(self.motif.is_valid())
        
        self.c1.set_value(0) # 0 est < 1
        self.assertFalse(self.motif.is_valid())

if __name__ == '__main__':
    unittest.main()