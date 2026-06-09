class Motif:
    """Stub temporaire — à remplacer par la version de Henry."""

    def __init__(self, nom: str, cases: list):
        self.nom = nom
        self.cases = cases  # liste de Case

    @property
    def n(self) -> int:
        """Nombre de cases = valeurs attendues de 1 à n."""
        return len(self.cases)

    def est_valide(self) -> bool:
        """Pas de doublon parmi les cases remplies."""
        valeurs = [c.valeur for c in self.cases if c.valeur is not None]
        return len(valeurs) == len(set(valeurs))

    def est_complet(self) -> bool:
        """Le motif contient exactement les chiffres 1 à n."""
        valeurs = [c.valeur for c in self.cases if c.valeur is not None]
        return sorted(valeurs) == list(range(1, self.n + 1))

    def __repr__(self):
        return f"Motif({self.nom}, n={self.n})"
