# src/view/fenetre_principale.py
import sys
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction
from src.view.composant_grille import ComposantGrille


class FenetrePrincipale(QMainWindow):
    """
    Cette classe représente la fenêtre principale de notre application Néonaure.
    En héritant de QMainWindow, nous bénéficions automatiquement d'une structure
    prête à l'emploi pour intégrer une barre de menus et un espace de travail central.
    """
    def __init__(self, controleur):
        super().__init__()

        # La vue ne connaît pas le modèle. Elle passe toujours par le contrôleur,
        # ce qui permet de respecter l'architecture MVC demandée dans la SAÉ.
        self.controleur = controleur

        self.setWindowTitle("Néonaure - SAÉ Graphes-IHM")
        self.resize(800, 600)
        self.setMinimumSize(600, 400)

        self.initialiser_menus()

        self.widget_central = QWidget()
        self.layout_central = QVBoxLayout()
        self.widget_central.setLayout(self.layout_central)
        self.setCentralWidget(self.widget_central)

        # Subtilité importante : avec la signature ComposantGrille(rows, cols, parent),
        # il ne faut pas écrire ComposantGrille(self), sinon self devient le nombre de lignes.
        self.composant_grille = ComposantGrille(parent=self)
        self.layout_central.addWidget(self.composant_grille)

        self.widget_central.setStyleSheet("background-color: #ecf0f1;")

    def initialiser_menus(self) -> None:
        """
        Construit toute la barre de menus.
        Les actions restent volontairement simples : elles délèguent au contrôleur.
        """
        barre_menu = self.menuBar()

        menu_fichier = barre_menu.addMenu("Fichier")

        action_charger = QAction("Charger une grille...", self)
        action_charger.triggered.connect(self.action_charger)
        menu_fichier.addAction(action_charger)

        action_sauvegarder = QAction("Sauvegarder", self)
        action_sauvegarder.triggered.connect(self.action_sauvegarder)
        menu_fichier.addAction(action_sauvegarder)

        menu_fichier.addSeparator()

        action_quitter = QAction("Quitter", self)
        action_quitter.triggered.connect(self.action_quitter)
        menu_fichier.addAction(action_quitter)

        menu_jeu = barre_menu.addMenu("Jeu")

        action_verifier = QAction("Vérifier", self)
        action_verifier.triggered.connect(self.action_verifier)
        menu_jeu.addAction(action_verifier)

        action_resoudre = QAction("Résoudre", self)
        action_resoudre.triggered.connect(self.action_resoudre)
        menu_jeu.addAction(action_resoudre)

        action_reinitialiser = QAction("Réinitialiser", self)
        action_reinitialiser.triggered.connect(self.action_reinitialiser)
        menu_jeu.addAction(action_reinitialiser)

        menu_aide = barre_menu.addMenu("Aide")

        action_regles = QAction("Règles du jeu", self)
        action_regles.triggered.connect(self.action_regles)
        menu_aide.addAction(action_regles)

    def _appeler_controleur(self, nom_methode: str, *args):
        """
        Appelle une méthode du contrôleur seulement si elle existe.
        C'est pratique pendant le développement, car toutes les méthodes d'Adel
        ne sont pas forcément encore branchées.
        """
        methode = getattr(self.controleur, nom_methode, None)

        if callable(methode):
            return methode(*args)

        QMessageBox.warning(
            self,
            "Fonction indisponible",
            f"La méthode du contrôleur '{nom_methode}' n'est pas encore disponible."
        )
        return None

    def action_charger(self) -> None:
        """
        Ouvre l'explorateur de fichiers.
        PyQt6 renvoie un tuple : le chemin du fichier et le filtre utilisé.
        Le filtre n'est pas utile ici, donc on le récupère avec _.
        """
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Charger une grille Néonaure",
            "",
            "Fichiers JSON (*.json);;Tous les fichiers (*)"
        )

        if filepath:
            self._appeler_controleur("charger_grille", filepath)

    def action_sauvegarder(self) -> None:
        """
        Demande où sauvegarder la partie.
        La vue ne crée pas le JSON elle-même : elle transmet le chemin au contrôleur.
        """
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Sauvegarder la grille",
            "",
            "Fichiers JSON (*.json)"
        )

        if filepath:
            self._appeler_controleur("sauvegarder_grille", filepath)

    def action_verifier(self) -> None:
        """
        Demande au contrôleur de vérifier la grille.
        Si le contrôleur renvoie True ou False, on affiche un retour simple.
        Sinon, on le laisse gérer l'affichage des erreurs directement dans la grille.
        """
        resultat = self._appeler_controleur("verifier_grille")

        if resultat is True:
            QMessageBox.information(self, "Vérification", "La grille est correcte.")
        elif resultat is False:
            QMessageBox.warning(self, "Vérification", "La grille contient encore des erreurs.")

    def action_resoudre(self) -> None:
        """Demande au contrôleur de lancer l'algorithme de résolution."""
        self._appeler_controleur("resoudre_grille")

    def action_reinitialiser(self) -> None:
        """
        Demande une confirmation avant de remettre la grille à zéro.
        Cela évite qu'un joueur perde sa progression par erreur.
        """
        reponse = QMessageBox.question(
            self,
            "Réinitialiser",
            "Voulez-vous vraiment réinitialiser la grille ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reponse == QMessageBox.StandardButton.Yes:
            self._appeler_controleur("reinitialiser_grille")

    def action_quitter(self) -> None:
        """
        Demande une confirmation avant de fermer l'application.
        C'est un contrôle explicite utile pour éviter les fermetures accidentelles.
        """
        reponse = QMessageBox.question(
            self,
            "Quitter",
            "Voulez-vous vraiment quitter le jeu ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reponse == QMessageBox.StandardButton.Yes:
            self.close()

    def action_regles(self) -> None:
        """Affiche les règles officielles du Néonaure dans une fenêtre d'aide."""
        regles = (
            "Règles du Néonaure :\n\n"
            "1. Un chiffre par case.\n"
            "2. Un chiffre doit être entouré de chiffres différents, y compris en diagonale.\n"
            "3. Un motif de N cases, repéré en traits gras, doit comporter tous les chiffres de 1 à N."
        )

        QMessageBox.information(self, "Règles du jeu", regles)