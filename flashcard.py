from view import Screen

if __name__ == "__main__":
# boucle moteur faisant tourner l'application
window = tk.Tk()

# Instanciation de la classe Screen
screen = Screen(window)

# Instanciation des classes Thema et ActionThema
#thema_screen = Thema(screen)
#action_thema_screen = ActionThema(screen)
#card_mats = CardMat(screen)
#card_action = CardAction(screen)

window.mainloop()

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