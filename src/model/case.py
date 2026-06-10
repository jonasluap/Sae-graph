# src/model/case.py

class Case:
    """
    Représente une cellule individuelle dans la grille de Néonaure.
    """

    def __init__(self, col: int, ligne: int, valeur: int = None, fixee: bool = False):
        self.col = col
        self.ligne = ligne
        self.valeur = valeur
        self.fixee = fixee

    def get_position(self) -> tuple[int, int]:
        return self.col, self.ligne

    def get_value(self) -> int | None:
        return self.valeur

    def set_value(self, valeur: int | None) -> None:
        if not self.fixee:
            self.valeur = valeur

    def is_fixed(self) -> bool:
        return self.fixee

    def __str__(self) -> str:
        etat = "Fixée" if self.fixee else "Libre"
        val = self.valeur if self.valeur is not None else "."
        return f"[{val}] ({etat})"

    def __repr__(self) -> str:
        return f"Case(col={self.col}, ligne={self.ligne}, valeur={self.valeur}, fixee={self.fixee})"