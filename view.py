import tkinter as tk
from tkinter import ttk, messagebox

class Screen:
    def __init__(self, controller):
        self.window = tk.Tk()
        self.window.title("Flashcards")
        self.controller = controller
        
        # frame (up-left) to select thema
        self.dealer_frm = ttk.Frame(master=self.window)
        self.dealer_frm.grid(column=0, row=0, padx=5, pady=5, sticky=(tk.W, tk.N))

        # frame (down-left) to activate
        self.dealer_frm_action = ttk.Frame(master=self.window)
        self.dealer_frm_action.grid(column=0, row=1, padx=5, pady=5, sticky=(tk.W, tk.S))

        # frame (up-right) to display cards (card mats)
        self.card_mat_frm = ttk.Frame(master=self.window)
        self.card_mat_frm.grid(column=1, row=0, padx=5, pady=5, sticky=(tk.E, tk.N))

        # frame (down-right) to act
        self.card_frm_action = ttk.Frame(master=self.window)
        self.card_frm_action.grid(column=1, row=1, padx=5, pady=5, sticky=(tk.E, tk.S))

    def run(self):
        self.window.protocol("WM_DELETE_WINDOW", self.stop)
        self.window.mainloop()
    
    def stop(self):
        print("fermeture de l'application")
        self.window.destroy()
        self.controller.close_database()


class Dealer:
    
    def __init__(self, screen):
        self.screen = screen
        self.decks = screen.controller.get_decks()
        self.selected_decks = []

        # section with selection of dealer's menu
        self.deck_lbl = ttk.Label(self.screen.dealer_frm, text='Sélectionner:', font=('Helvetica', 12, 'bold'))
        self.deck_lbl.grid(sticky=tk.W, padx=5, pady=5)
        
        #--- variables to track the state of checkboxes
        self.check_vars = []
        
        #--- display list of themes with checkboxes
        for deck in self.decks:
            var = tk.IntVar()  # Variable to track the checkbox state (0 = unchecked, 1 = checked)
            self.check_vars.append(var)
            checkbox = ttk.Checkbutton(
                master=self.screen.dealer_frm, 
                text=deck, 
                variable=var,
                command=self.update_selected_decks
                )
            checkbox.grid(padx=3, pady=3, sticky=tk.W)
    
    def update_selected_decks(self):
        self.selected_decks = self.screen.controller.on_deck_selection(self.check_vars, self.decks)

    def get_selected_decks(self):
        return self.selected_decks
    
    def draw_card(self):
        selected_decks = self.get_selected_decks()
        if selected_decks:
            card = self.screen.controller.pick_a_card(selected_decks)
            return card
        else:
            print("No decks selected")
            return None

class CardMat:
    def __init__(self, screen, dealer):
        self.screen = screen
        self.dealer = dealer

        # bouton pour tirer une carte
        self.dealer_btn_draw = ttk.Button(master=self.screen.dealer_frm_action, text='tirer carte', command=lambda: self.deal_a_card(question=True))
        self.dealer_btn_draw.grid(column=0, row=1, padx=5, pady=5, sticky=(tk.W, tk.S))

        # affichage de la carte
        self.card_title_lbl = ttk.Label(master=self.screen.card_mat_frm, text='Carte:', font=('Helvetica', 12, 'bold'))
        self.card_title_lbl.grid(padx=5, pady=5)

        # Utilisation d'un widget Text pour afficher le contenu de la carte
        self.card_content_txt = tk.Text(master=self.screen.card_mat_frm, wrap=tk.WORD, font=('Helvetica', 18), height=10, width=50)
        self.card_content_txt.grid(padx=5, pady=5)
        self.card_content_txt.config(state=tk.DISABLED)  # Désactiver l'édition par l'utilisateur

    def deal_a_card(self, question):
        card = self.dealer.draw_card()
        self.display_card(card, question)
        
    def display_card(self, card, question):
        self.card_content_txt.config(state=tk.NORMAL)  # Activer l'édition pour mettre à jour le texte
        self.card_content_txt.delete(1.0, tk.END)  # Effacer le contenu précédent
        if card:
            if question:
                card_text = f"Question: {card[1]}"
                self.btn_see_answer()
            else: 
                card_text= f"Answer: {card[2]}"
                self.btn_good_answer(card)
            self.card_content_txt.insert(tk.END, card_text)
        else:
            self.card_content_txt.insert(tk.END, "No card available")
        self.card_content_txt.config(state=tk.DISABLED)  # Désactiver l'édition après mise à jour

    def btn_see_answer(self):
        # Effacer le contenu de self.screen.card_frm_action
        for widget in self.screen.card_frm_action.winfo_children():
            widget.destroy()
            
        # bouton pour voir la réponse
        self.card_btn_see_answer = ttk.Button(master=self.screen.card_frm_action, text='voir la réponse', command=lambda: self.deal_a_card(question=False))
        self.card_btn_see_answer.grid(padx=5, pady=5)

    def btn_good_answer(self, card):
        # Effacer le contenu de self.screen.card_frm_action
        for widget in self.screen.card_frm_action.winfo_children():
            widget.destroy()
    
        # bouton "Bonne réponse ?"
        self.btn_good = ttk.Button(master=self.screen.card_frm_action, text='Bonne réponse ?', command=lambda: self.update_priority(card, answer=True))
        self.btn_good.grid(column=0, row=0, padx=5, pady=5)

        # bouton "Mauvaise réponse ?"
        self.btn_bad = ttk.Button(master=self.screen.card_frm_action, text='Mauvaise réponse ?', command=lambda: self.update_priority(card, answer=False))
        self.btn_bad.grid(column=1, row=0, padx=5, pady=5)

    def update_priority(self, card, answer):
        # Appeler la méthode du contrôleur pour mettre à jour la priorité de la carte
        print(f"card: {card}")
        print(f"answer: {answer}")
        self.screen.controller.update_card_priority(card_id=card[0], priority=card[3], answer=answer)
        # Afficher la prochaine carte ou un message de confirmation
        #self.deal_a_card(question=True)
        messagebox.showinfo("Confirmation", "La priorité de la carte a été mise à jour.")