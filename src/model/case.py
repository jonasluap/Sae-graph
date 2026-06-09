# src/model/case.py

class Case:
    """
    Représente une cellule individuelle dans la grille de Néonaure.
    """
    def __init__(self, ligne: int, colonne: int, valeur: int = None, fixee: bool = False):
        self._ligne = ligne
        self._colonne = colonne
        self._valeur = valeur
        self._fixee = fixee

    def get_position(self) -> tuple[int, int]:
        """Retourne les coordonnées de la case sous forme de tuple (ligne, colonne)."""
        return self._ligne, self._colonne

    def get_value(self) -> int | None:
        """Retourne la valeur actuelle de la case, ou None si elle est vide."""
        return self._valeur

    def set_value(self, valeur: int | None) -> None:
        """
        Modifie la valeur de la case.
        Si la case est fixée (préremplie), la modification est ignorée.
        """
        if not self._fixee:
            self._valeur = valeur

    def is_fixed(self) -> bool:
        """Retourne True si la case est préremplie et non modifiable."""
        return self._fixee

    def __str__(self) -> str:
        etat = "Fixée" if self._fixee else "Libre"
        val = self._valeur if self._valeur is not None else "."
        return f"[{val}] ({etat})"

    def __repr__(self) -> str:
        return f"Case(ligne={self._ligne}, col={self._colonne}, valeur={self._valeur}, fixee={self._fixee})"