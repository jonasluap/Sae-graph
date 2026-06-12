# src/model/case.py

class Case:
    """
    Représente une cellule individuelle dans la grille de Néonaure.

    Une case possède :
    - une position (colonne, ligne),
    - une valeur (ou None si elle est vide),
    - un état indiquant si elle est fixée ou modifiable.
    """

    def __init__(self, col: int, ligne: int, valeur: int = None, fixee: bool = False):
        # Coordonnées de la case dans la grille
        self.col = col
        self.ligne = ligne

        # Valeur actuellement contenue dans la case
        # None signifie que la case est vide
        self.valeur = valeur

        # True si la case fait partie des indices initiaux du puzzle
        self.fixee = fixee

    def get_position(self) -> tuple[int, int]:
        """
        Retourne la position de la case sous la forme (colonne, ligne).
        """
        return self.col, self.ligne

    def get_value(self) -> int | None:
        """
        Retourne la valeur actuellement stockée dans la case.
        """
        return self.valeur

    def set_value(self, valeur: int | None) -> None:
        """
        Modifie la valeur de la case uniquement si celle-ci n'est pas fixée.
        """
        if not self.fixee:
            self.valeur = valeur

    def is_fixed(self) -> bool:
        """
        Indique si la case est fixée (non modifiable).
        """
        return self.fixee

    def __str__(self) -> str:
        """
        Représentation lisible de la case pour l'affichage.
        """
        etat = "Fixée" if self.fixee else "Libre"
        val = self.valeur if self.valeur is not None else "."
        return f"[{val}] ({etat})"

    def __repr__(self) -> str:
        """
        Représentation détaillée de la case, utile pour le débogage.
        """
        return f"Case(col={self.col}, ligne={self.ligne}, valeur={self.valeur}, fixee={self.fixee})"