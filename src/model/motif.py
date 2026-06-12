from typing import List
from .case import Case


class Motif:
    """
    Représente un motif (une zone délimitée) contenant un ensemble de cases.

    Règle du jeu :
    Un motif de taille N doit contenir exactement les valeurs de 1 à N,
    sans doublons.
    """

    def __init__(self, nom: str, cases: List[Case] | None = None):
        """
        Initialise un motif.

        Args:
            nom: Nom identifiant le motif.
            cases: Liste initiale de cases appartenant au motif.
        """
        self.nom = nom

        # Si aucune liste n'est fournie, on crée une liste vide
        self._cases: List[Case] = cases if cases is not None else []

    @property
    def cases(self) -> List[Case]:
        """
        Retourne la liste des cases du motif.

        Alias utilisé par le reste du projet.
        """
        return self._cases

    @property
    def n(self) -> int:
        """
        Retourne la taille du motif.

        Alias utilisé par le reste du projet.
        """
        return len(self._cases)

    def add_case(self, case: Case) -> None:
        """
        Ajoute une case au motif.
        """
        self._cases.append(case)

    def get_cases(self) -> List[Case]:
        """
        Retourne la liste des cases appartenant au motif.
        """
        return self._cases

    def size(self) -> int:
        """
        Retourne le nombre total de cases du motif.
        """
        return len(self._cases)

    def get_values(self) -> List[int]:
        """
        Retourne toutes les valeurs actuellement présentes
        dans le motif en ignorant les cases vides.
        """
        return [
            case.get_value()
            for case in self._cases
            if case.get_value() is not None
        ]

    def is_complete(self) -> bool:
        """
        Vérifie que toutes les cases du motif sont remplies.
        """
        return len(self.get_values()) == self.size()

    def is_valid(self) -> bool:
        """
        Vérifie que le motif respecte les règles :

        - Chaque valeur doit être comprise entre 1 et N.
        - Aucune valeur ne doit apparaître plusieurs fois.

        Un motif partiellement rempli peut être valide.
        """
        valeurs = self.get_values()
        n = self.size()

        # Vérification des bornes autorisées
        for val in valeurs:
            if val < 1 or val > n:
                return False

        # Vérification de l'absence de doublons
        if len(valeurs) != len(set(valeurs)):
            return False

        return True

    # ==================================================
    # Aliases demandés pour assurer la compatibilité
    # avec le code d'Adel.
    # ==================================================

    def est_valide(self) -> bool:
        """
        Alias français de is_valid().
        """
        return self.is_valid()

    def est_complet(self) -> bool:
        """
        Alias français de is_complete().
        """
        return self.is_complete()

    def __repr__(self):
        """
        Représentation textuelle du motif pour le débogage.
        """
        return f"Motif({self.nom}, n={self.n})"