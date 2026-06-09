# src/model/motif.py
from typing import List
from .case import Case

class Motif:
    """
    Représente un motif (une zone délimitée) contenant un ensemble de cases.
    Règle : un motif de taille N doit contenir exactement les chiffres de 1 à N.
    """
    def __init__(self, nom: str):
        self.nom = nom
        self._cases: List[Case] = []

    def add_case(self, case: Case) -> None:
        """Ajoute une instance de Case au motif."""
        self._cases.append(case)

    def get_cases(self) -> List[Case]:
        """Retourne la liste des cases appartenant au motif."""
        return self._cases

    def size(self) -> int:
        """Retourne la taille N du motif (nombre total de cases)."""
        return len(self._cases)

    def get_values(self) -> List[int]:
        """Retourne la liste des valeurs actuellement remplies dans le motif."""
        return [case.get_value() for case in self._cases if case.get_value() is not None]

    def is_complete(self) -> bool:
        """
        Vérifie si toutes les cases du motif sont remplies.
        """
        return len(self.get_values()) == self.size()

    def is_valid(self) -> bool:
        """
        Vérifie si le motif est valide selon les règles du jeu :
        - Aucune valeur en dehors de l'intervalle [1, N]
        - Aucun doublon
        Un motif partiellement rempli peut être valide s'il respecte ces règles.
        """
        valeurs = self.get_values()
        n = self.size()
        
        # Vérification des bornes
        for val in valeurs:
            if val < 1 or val > n:
                return False
                
        # Vérification des doublons
        if len(valeurs) != len(set(valeurs)):
            return False
            
        return True