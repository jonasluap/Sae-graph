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
        
        # Pour respecter strictement l'architecture MVC demandée par notre professeur, 
        # la vue doit ignorer le modèle. 
        # Nous stockons donc le contrôleur pour pouvoir lui déléguer toutes les actions métier.
        self.controleur = controleur
        
        self.setWindowTitle("Néonaure - SAÉ Graphes-IHM")
        self.resize(800, 600)
        self.setMinimumSize(600, 400)
        
        self.initialiser_menus()
        
        # 1. On crée d'abord le conteneur principal
        self.widget_central = QWidget()
        
        # 2. On crée le layout et on l'applique au conteneur AVANT d'y ajouter des éléments
        self.layout_central = QVBoxLayout()
        self.widget_central.setLayout(self.layout_central)
        self.setCentralWidget(self.widget_central)
        
        # 3. Maintenant que le layout existe, on peut y insérer le composant de la grille
        self.composant_grille = ComposantGrille(self)
        self.layout_central.addWidget(self.composant_grille)
        
        # J'ajoute une légère couleur de fond temporaire pour t'aider à visualiser cet espace.
        self.widget_central.setStyleSheet("background-color: #ecf0f1;")

    def initialiser_menus(self) -> None:
        """
        Nous construisons ici toute la barre de navigation supérieure. 
        L'appel à menuBar() génère automatiquement la barre si elle n'existe pas encore.
        """
        barre_menu = self.menuBar()
        
        # Nous commençons par construire le menu Fichier, qui regroupe les entrées et sorties.
        menu_fichier = barre_menu.addMenu("Fichier")
        
        # Chaque élément du menu est une QAction. Il suffit de la créer, puis de lier 
        # son signal "triggered" (qui s'active au clic) à la méthode correspondante.
        action_charger = QAction("Charger une grille...", self)
        action_charger.triggered.connect(self.action_charger)
        menu_fichier.addAction(action_charger)
        
        action_sauvegarder = QAction("Sauvegarder", self)
        action_sauvegarder.triggered.connect(self.action_sauvegarder)
        menu_fichier.addAction(action_sauvegarder)
        
        # L'ajout d'un séparateur est une bonne pratique ergonomique pour isoler l'action de fermeture.
        menu_fichier.addSeparator()
        
        action_quitter = QAction("Quitter", self)
        action_quitter.triggered.connect(self.action_quitter)
        menu_fichier.addAction(action_quitter)
        
        # Nous passons ensuite au menu Jeu, dédié aux interactions avec la partie en cours.
        menu_jeu = barre_menu.addMenu("Jeu")
        
        action_resoudre = QAction("Résoudre", self)
        action_resoudre.triggered.connect(self.action_resoudre)
        menu_jeu.addAction(action_resoudre)
        
        # Enfin, nous mettons en place le menu Aide pour guider l'utilisateur.
        menu_aide = barre_menu.addMenu("Aide")
        
        action_regles = QAction("Règles du jeu", self)
        action_regles.triggered.connect(self.action_regles)
        menu_aide.addAction(action_regles)

    def action_charger(self) -> None:
        """
        Cette méthode lance l'explorateur de fichiers natif du système d'exploitation.
        La subtilité avec PyQt6 est que la fonction renvoie un tuple contenant le chemin 
        du fichier et le filtre utilisé. Nous ignorons le filtre avec un simple tiret du bas.
        """
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Charger une grille Néonaure",
            "",
            "Fichiers JSON (*.json);;Tous les fichiers (*)"
        )
        
        # Si le joueur a bien sélectionné un fichier, nous transmettons ce chemin au contrôleur.
        # Encore une fois, la vue ne lit jamais le fichier d'elle-même.
        if filepath:
            self.controleur.charger_grille(filepath)

    def action_sauvegarder(self) -> None:
        """
        De la même manière que pour le chargement, nous demandons à l'utilisateur où il souhaite
        enregistrer sa partie, puis nous laissons le contrôleur gérer la sérialisation en JSON.
        """
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Sauvegarder la grille",
            "",
            "Fichiers JSON (*.json)"
        )
        if filepath:
            self.controleur.sauvegarder_grille(filepath)

    def action_resoudre(self) -> None:
        """
        Un simple relais vers le contrôleur pour lancer l'algorithme de résolution de la grille.
        """
        self.controleur.resoudre_grille()

    def action_quitter(self) -> None:
        """
        Pour garantir une bonne ergonomie et éviter les fermetures accidentelles, 
        nous affichons une boîte de dialogue demandant une confirmation explicite à l'utilisateur.
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
        """
        Affiche simplement les règles officielles du Néonaure dans une petite fenêtre d'information.
        """
        regles = (
            "Règles du Néonaure :\n\n"
            "1. Un chiffre par case.\n"
            "2. Un chiffre doit être entouré de chiffres différents (y compris en diagonale).\n"
            "3. Un motif de N cases (repéré en traits gras) doit comporter tous les chiffres de 1 à N."
        )
        QMessageBox.information(self, "Règles du jeu", regles)