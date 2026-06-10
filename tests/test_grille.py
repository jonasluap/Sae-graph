import pytest
from src.model.grille import Grille

GRILLE1 = "Exemples de grille-20260609/grille1.json"


# --- tests à écrire ---

def test_chargement_dimensions():
    g = Grille()
    g.charger_json(GRILLE1)
    assert g.nb_colonnes == 8
    assert g.nb_lignes == 8
    assert len(g.motifs) == 15
    
def test_get_case():
    g = Grille()
    g.charger_json(GRILLE1)
    case = g.get_case(0, 7)
    assert case.valeur == 3
    assert case.fixee == True;
    
    
def test_case_vide():
    g = Grille()
    g.charger_json(GRILLE1)
    case = g.get_case(0,0)
    assert case.valeur == None
    assert case.fixee == False

def test_get_voisins_coin():
    g = Grille()
    g.charger_json(GRILLE1)
    voisins = g.get_voisins(0, 0)
    assert len(voisins) == 3
    
def test_get_voisins_milieu():
    g = Grille()
    g.charger_json(GRILLE1)
    voisins = g.get_voisins(3, 3)
    assert len(voisins) == 8