import tkinter as tk
from tkinter import ttk

class Screen:
    def __init__(self, window):
        self.window = window
        self.window.title("Flashcards")
        
        # frame (up-left) to select thema
        self.thema_frm = ttk.Frame(master=self.window)
        self.thema_frm.grid(column=0, row=0, padx=5, pady=5, sticky=(tk.W, tk.N))

        # frame (down-left) to activate
        self.action_thema_frm = ttk.Frame(master=self.window)
        self.action_thema_frm.grid(column=0, row=1, padx=5, pady=5, sticky=(tk.W, tk.S))

        # frame (up-right) to display cards (card mats)
        self.card_mats_frm = ttk.Frame(master=self.window)
        self.card_mats_frm.grid(column=1, row=0, padx=5, pady=5, sticky=(tk.E, tk.N))

        # frame (down-right) to act
        self.card_action_frm = ttk.Frame(master=self.window)
        self.card_action_frm.grid(column=1, row=1, padx=5, pady=5, sticky=(tk.E, tk.S))

class Thema:
    thema_test = ['histoire', 'italien', 'géographie']
    
    def __init__(self, screen):
        self.screen = screen

        # section with selecion of thema
        self.thema_lbl = ttk.Label(self.screen.thema_frm, text='Sélectionner:', font=('Helvetica', 12, 'bold'))
        self.thema_lbl.grid(sticky=tk.W, padx=5, pady=5)
               
        #--- variables to track the state of checkboxes
        self.check_vars = []
        
        #--- display list of themes with checkboxes
        for thema in self.thema_test:
            var = tk.IntVar()  # Variable to track the checkbox state (0 = unchecked, 1 = checked)
            self.check_vars.append(var)
            checkbox = ttk.Checkbutton(master=self.screen.thema_frm, text=thema, variable=var)
            checkbox.grid(padx=3, pady=3, sticky=tk.W)
    
    # --- method to get the selected choices
    def get_selected_themes(self):
        selected = [self.thema_test[i] for i, var in enumerate(self.check_vars) if var.get() == 1]
        return selected
    
class ActionThema:
    def __init__(self, screen):
        self.screen = screen

        # button to modify
        self.action_thema_btn_modif = ttk.Button(master=self.screen.action_thema_frm, text='modifier')
        self.action_thema_btn_modif.grid(column=0, row=0, padx=5, pady=5, sticky=(tk.W, tk.S))
        
        # button "pick a card"
        self.action_thema_btn_launch = ttk.Button(master=self.screen.action_thema_frm, text='tirer carte')
        self.action_thema_btn_launch.grid(column=0, row=1, padx=5, pady=5, sticky=(tk.W, tk.S))

class CardMat:
    def __init__(self, screen):
        self.screen = screen
    
        self.card_title_lbl = ttk.Label(master=self.screen.card_mats_frm, text='Question:', font=('Helvetica', 12))
        self.card_title_lbl.grid(padx=5, pady=5)
        self.card_content_lbl = ttk.Label(master=self.screen.card_mats_frm, text='Lorem ipsum dolor sit amet.', font=('Helvetica', 18))
        self.card_content_lbl.grid(padx=5, pady=5)

class CardAction:
    def __init__(self, screen):
        self.screen = screen

        self.card_action_btn_1 = ttk.Button(master=self.screen.card_action_frm, text='choix 1')
        self.card_action_btn_1.grid(column=0, row=0, padx=5, pady=5)
        self.card_action_btn_2 = ttk.Button(master=self.screen.card_action_frm, text='choix 2')
        self.card_action_btn_2.grid(column=1, row=0, padx=5, pady=5)

# --- controller
window = tk.Tk()

# Instanciation de la classe Screen
screen = Screen(window)

# Instanciation des classes Thema et ActionThema
thema_screen = Thema(screen)
action_thema_screen = ActionThema(screen)
card_mats = CardMat(screen)
card_action = CardAction(screen)

window.mainloop()
