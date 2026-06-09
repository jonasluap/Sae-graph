from src.model.grille import Grille
from src.model.case import Case


def resoudre(grille: Grille) -> bool:
    """Remplit la grille par backtracking récursif.

    Retourne True si une solution est trouvée, False sinon.
    Modifie la grille en place.
    """
    case = _trouver_case_vide(grille)
    if case is None:
        return True  # plus aucune case vide = solution trouvée

    motif = grille.get_motif_de(case)
    valeurs_possibles = range(1, motif.n + 1)

    for val in valeurs_possibles:
        if _peut_placer(grille, case, val):
            case.valeur = val
            if resoudre(grille):
                return True
            case.valeur = None  # backtrack : on annule et on essaie la valeur suivante

    return False  # aucune valeur ne fonctionne ici → on remonte


def _trouver_case_vide(grille: Grille) -> Case | None:
    """Retourne la première case sans valeur, ou None si la grille est complète."""
    for case in grille._cases.values():
        if case.valeur is None:
            return case
    return None


def _peut_placer(grille: Grille, case: Case, val: int) -> bool:
    """Vérifie si val peut être placée dans case sans violer les contraintes.

    Contrainte 1 — adjacence : aucun voisin (8 directions) ne doit déjà valoir val.
    Contrainte 2 — motif : val ne doit pas déjà être présente dans le motif.
    """
    # Contrainte 1 : voisins du graphe roi
    for voisin in grille.get_voisins(case.col, case.ligne):
        if voisin.valeur == val:
            return False

    # Contrainte 2 : unicité dans le motif
    motif = grille.get_motif_de(case)
    for c in motif.cases:
        if c is not case and c.valeur == val:
            return False

    return True
