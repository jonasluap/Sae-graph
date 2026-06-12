import pytest
import os
import tempfile
from src.model.grille import Grille
from src.model.solveur import resoudre

GRILLE1 = "Exemples de grille-20260609/grille1.json"
GRILLE9 = "Exemples de grille-20260609/grille9.json"

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
    
    
def test_est_valide_conflit_voisins():
    g = Grille()
    g.charger_json(GRILLE1)
    # Mettre la même valeur sur deux cases voisines
    g.get_case(0, 0).valeur = 1
    g.get_case(1, 0).valeur = 1  # voisin direct de (0,0)
    assert g.est_valide() == False
    
def test_est_valide():
    g = Grille()
    g.charger_json(GRILLE1)
    assert g.est_valide() == True
    
    
    
def test_solveur_grille1():
    g = Grille()
    g.charger_json(GRILLE1)
    resultat = resoudre(g)
    assert resultat == True
    assert g.est_complete() == True
    
    
def test_chargement_grille9():
    g = Grille()
    g.charger_json(GRILLE9)
    assert g.nb_colonnes == 5
    assert g.nb_lignes == 13


def test_sauvegarder_json():
    g = Grille()
    g.charger_json(GRILLE1)
    g.get_case(0, 0).valeur = 2

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        chemin = f.name

    try:
        g.sauvegarder_json(chemin)
        g2 = Grille()
        g2.charger_json(chemin)
        assert g2.nb_colonnes == 8
        assert g2.nb_lignes == 8
        assert g2.get_case(0, 0).valeur == 2
        assert g2.get_case(0, 7).valeur == 3
    finally:
        os.remove(chemin)
