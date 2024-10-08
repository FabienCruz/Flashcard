import tkinter as tk
from tkinter import ttk

class Screen:
    def __init__(self, window):
        self.window = window
        self.window.title("Flashcards")
        
        # --- main frame contains other frames
        self.main_frm = ttk.Frame(master=self.window, padding=3) 
        self.main_frm.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.window.columnconfigure(0, weight=1, minsize=360)
        self.window.rowconfigure(0, weight=1, minsize=280)

# --- frame and widgets
class Thema(Screen):
    thema_test = ['histoire', 'italien', 'géographie']
    
    def __init__(self, window):
        super().__init__(window)  
        
        self.thema_frm = ttk.Frame(master=self.main_frm)
        self.thema_frm.grid(column=0, row=0, sticky=(tk.W, tk.N), padx=5, pady=5)
        
        self.thema_lbl = ttk.Label(self.thema_frm, text='Sélectionner:', font=('Helvetica', 12, 'bold'))
        self.thema_lbl.grid(sticky=tk.W, padx=5, pady=5)
        
        #--- variables to track the state of checkboxes
        self.check_vars = []
        
        #--- display list of themes with checkboxes
        for thema in self.thema_test:
            var = tk.IntVar()  # Variable to track the checkbox state (0 = unchecked, 1 = checked)
            self.check_vars.append(var)
            checkbox = ttk.Checkbutton(master=self.thema_frm, text=thema, variable=var)
            checkbox.grid(padx=3, pady=3, sticky=tk.W)
    
    # --- method to get the selected choices
    def get_selected_themes(self):
        selected = [self.thema_test[i] for i, var in enumerate(self.check_vars) if var.get() == 1]
        return selected

class ActionThema(Screen):
    def __init__(self, window):
        super().__init__(window)
    
        self.action_thema_frm = ttk.Frame(self.main_frm)
        self.action_thema_frm.grid(column=0, row=1, sticky=(tk.W, tk.S), padx=5, pady=5)
        
        self.action_thema_btn_modif = ttk.Button(self.action_thema_frm, text='modifier')
        self.action_thema_btn_modif.grid(column=0, row=0, padx=5, pady=5, sticky=(tk.W, tk.S))
        
        self.action_thema_btn_launch = ttk.Button(self.action_thema_frm, text='lancer FlashCard')
        self.action_thema_btn_launch.grid(column=1, row=0, padx=5, pady=5, sticky=(tk.W, tk.S))


# --- controller
window = tk.Tk()

# Instanciation des classes Thema et ActionThema
thema_screen = Thema(window)
action_thema_screen = ActionThema(window)

window.mainloop()
