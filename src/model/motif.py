from typing import List
from .case import Case

class Motif:
    """
    Représente un motif (une zone délimitée) contenant un ensemble de cases.
    Règle : un motif de taille N doit contenir exactement les chiffres de 1 à N.
    """

    def __init__(self, nom: str, cases: List[Case] | None = None):
        self.nom = nom
        self._cases: List[Case] = cases if cases is not None else []

    @property
    def cases(self) -> List[Case]:
        """Alias utilisé par le reste du projet."""
        return self._cases

    @property
    def n(self) -> int:
        """Alias utilisé par le reste du projet."""
        return len(self._cases)

    def add_case(self, case: Case) -> None:
        self._cases.append(case)

    def get_cases(self) -> List[Case]:
        return self._cases

    def size(self) -> int:
        return len(self._cases)

    def get_values(self) -> List[int]:
        return [
            case.get_value()
            for case in self._cases
            if case.get_value() is not None
        ]

    def is_complete(self) -> bool:
        return len(self.get_values()) == self.size()

    def is_valid(self) -> bool:
        valeurs = self.get_values()
        n = self.size()

        for val in valeurs:
            if val < 1 or val > n:
                return False

        if len(valeurs) != len(set(valeurs)):
            return False

        return True

    # ===== Aliases demandés par Adel =====

    def est_valide(self) -> bool:
        return self.is_valid()

    def est_complet(self) -> bool:
        return self.is_complete()

    def __repr__(self):
        return f"Motif({self.nom}, n={self.n})"