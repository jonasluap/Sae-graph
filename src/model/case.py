class Case:
    """Stub temporaire — à remplacer par la version de Henry."""

    def __init__(self, col: int, ligne: int, valeur: int | None = None, fixee: bool = False):
        self.col = col
        self.ligne = ligne
        self.valeur = valeur
        self.fixee = fixee

    def __repr__(self):
        return f"Case({self.col},{self.ligne})={self.valeur}"
