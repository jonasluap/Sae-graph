import sys
from PyQt6.QtWidgets import QApplication

from src.controller.controleur import Controleur
from src.view.fenetre_principale import FenetrePrincipale


if __name__ == "__main__":
    app = QApplication(sys.argv)

    controleur = Controleur()
    fenetre = FenetrePrincipale(controleur)
    fenetre.show()

    sys.exit(app.exec())