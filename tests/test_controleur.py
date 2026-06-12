import pytest
from src.controller.controleur import Controleur

GRILLE1 = "Exemples de grille-20260609/grille1.json"


def test_charger_grille():
    c = Controleur()
    c.charger_grille(GRILLE1)
    assert c.grille is not None
    assert c.grille.nb_colonnes == 8
    assert c.grille.nb_lignes == 8


def test_verifier_grille_valide():
    c = Controleur()
    c.charger_grille(GRILLE1)
    assert c.verifier_grille() == True


def test_verifier_grille_invalide():
    c = Controleur()
    c.charger_grille(GRILLE1)
    c.grille.get_case(0, 0).valeur = 1
    c.grille.get_case(1, 0).valeur = 1
    assert c.verifier_grille() == False


def test_verifier_grille_sans_grille():
    c = Controleur()
    assert c.verifier_grille() is None


def test_reinitialiser_grille():
    c = Controleur()
    c.charger_grille(GRILLE1)
    c.grille.get_case(0, 0).valeur = 3
    c.reinitialiser_grille()
    assert c.grille.get_case(0, 0).valeur is None


def test_reinitialiser_ne_touche_pas_cases_fixees():
    c = Controleur()
    c.charger_grille(GRILLE1)
    case_fixee = c.grille.get_case(0, 7)  # valeur 3, fixée
    c.reinitialiser_grille()
    assert case_fixee.valeur == 3


def test_saisir_valeur():
    c = Controleur()
    c.charger_grille(GRILLE1)
    c.saisir_valeur(0, 0, 2)
    assert c.grille.get_case(0, 0).valeur == 2


def test_saisir_valeur_case_fixee():
    c = Controleur()
    c.charger_grille(GRILLE1)
    c.saisir_valeur(0, 7, 9)  # case fixée, ne doit pas changer
    assert c.grille.get_case(0, 7).valeur == 3
