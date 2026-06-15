import sys
from PyQt6.QtWidgets import QApplication

# Il faut bien sûr adapter cet import selon le nom de ton dossier
from src.view.fenetre_principale import FenetrePrincipale


class FauxControleur:
    """
    Un contrôleur 'bouchon' temporaire pour permettre à Jonas 
    de tester sa vue sans que l'application ne plante.
    """
    def charger_grille(self, filepath):
        print(f"[TEST] Le contrôleur simule le chargement du fichier : {filepath}")

    def sauvegarder_grille(self, filepath):
        print(f"[TEST] Le contrôleur simule la sauvegarde dans : {filepath}")

    def resoudre_grille(self):
        print("[TEST] Le contrôleur simule le lancement de l'algorithme de résolution...")


if __name__ == "__main__":
    # 1. Création de l'application PyQt6
    app = QApplication(sys.argv)
    
    # 2. Instanciation de notre faux contrôleur
    controleur_test = FauxControleur()
    
    # 3. Création et affichage de ta fenêtre en lui passant le contrôleur
    ma_fenetre = FenetrePrincipale(controleur_test)
    ma_fenetre.show()
    
    # 4. Lancement de la boucle d'événements
    sys.exit(app.exec())