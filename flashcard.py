from model import Database

def main():
    # création de la base de données
    db = Database()
    # lancer controller sur jeu
    # lancer écran 
    # fermeture de la base de données
    db.close()

if __name__ == "__main__":
    main()

"""
# main.py
from model import TaskModel
from view import TaskView
from controller import TaskController

def main():
    # Initialisation du modèle
    model = TaskModel()

    # Initialisation du contrôleur
    controller = TaskController(model)

    # Création de la fenêtre principale Tkinter à l'intérieur de TaskView
    app = TaskView(controller=controller)

    # Lancer la boucle principale Tkinter
    app.mainloop()

    # Fermer la connexion à la base de données
    model.close()

if __name__ == "__main__":
    main()

"""