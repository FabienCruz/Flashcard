import tkinter as tk
from tkinter import ttk, messagebox

class CardMat:
    """

    La classe CardMat est responsable de l'affichage du 'tapis de jeu'.
    Elle affiche les cartes, face question, face réponse, les boutons d'actions.

    """

    def __init__(self, screen, manage_screen):
        self.screen = screen
        self.decks = manage_screen.manage_deck
        self.cards = manage_screen.manage_card

    def initialize_card_mat(self):
        # efface le contenu des cadres
        self.screen.clear_frm_up_right()
        self.screen.clear_frm_down_right()

        # affichage bouton pour tirer une carte
        self.btn_draw = ttk.Button(master=self.screen.frm_down_right, text='tirer carte', command=lambda: self.deal_a_card(is_question=True))
        self.btn_draw.grid(column=0, row=0, padx=5, pady=5, sticky=(tk.E, tk.S))

        # affichage de la carte
        self.card_title_lbl = ttk.Label(master=self.screen.frm_up_right, text='Carte:', font=('Helvetica', 12, 'bold'))
        self.card_title_lbl.grid(padx=5, pady=5)

        # Utilisation d'un widget Text pour afficher le contenu de la carte
        self.card_content_txt = tk.Text(master=self.screen.frm_up_right, wrap=tk.WORD, font=('Helvetica', 18), height=10, width=50, padx=10, pady=10)
        self.card_content_txt.grid(padx=5, pady=5)
        self.card_content_txt.config(state=tk.DISABLED)  # Désactiver l'édition par l'utilisateur
        # montre une carte
        self.deal_a_card(is_question=True)    


    def deal_a_card(self, is_question):
        card = self.draw_card()
        self.display_card(card, is_question)
        
    def draw_card(self):
        selected_decks = self.decks.get_selected_decks()
        if selected_decks:
            card = self.cards.pick_a_card(selected_decks)
            return card
        else:
            return None
        
    def display_card(self, card, is_question):
        self.card_content_txt.config(state=tk.NORMAL)  # Activer l'édition pour mettre à jour le texte
        self.card_content_txt.delete(1.0, tk.END)  # Effacer le contenu précédent
        if card:
            if is_question:
                card_text = f"Question:\n\n{card[1]}"
                self.btn_see_answer(card)
            else: 
                card_text= f"Réponse:\n\n{card[2]}"
                self.btn_is_good_answer(card)
            self.card_content_txt.insert(tk.END, card_text)
        else:
            self.card_content_txt.insert(tk.END, "Sélectionnez un ou plusieurs thèmes pour tirer une carte")
        self.card_content_txt.config(state=tk.DISABLED)  # Désactiver l'édition après mise à jour

    def btn_see_answer(self, card):
        # Effacer le contenu de self.screen.frm_down_right
        for widget in self.screen.frm_down_right.winfo_children():
            widget.destroy()
            
        # bouton pour voir la réponse
        self.card_btn_see_answer = ttk.Button(master=self.screen.frm_down_right, text='voir la réponse', command=lambda: self.display_card(card ,is_question=False))
        self.card_btn_see_answer.grid(padx=5, pady=5)

    def btn_is_good_answer(self, card):
        # Effacer le contenu de self.screen.frm_down_right
        for widget in self.screen.frm_down_right.winfo_children():
            widget.destroy()
    
        # bouton "Bonne réponse ?"
        self.btn_good = ttk.Button(master=self.screen.frm_down_right, text='Bonne réponse ?', command=lambda: self.update_priority(card, is_good_answer=True))
        self.btn_good.grid(column=0, row=0, padx=5, pady=5)

        # bouton "Mauvaise réponse ?"
        self.btn_bad = ttk.Button(master=self.screen.frm_down_right, text='Mauvaise réponse ?', command=lambda: self.update_priority(card, is_good_answer=False))
        self.btn_bad.grid(column=1, row=0, padx=5, pady=5)

    def update_priority(self, card, is_good_answer):
        # Appeler la méthode du contrôleur pour mettre à jour la priorité de la carte
        self.cards.update_card_priority(card_id=card[0], current_priority=card[3], is_good_answer=is_good_answer)
        # Afficher la prochaine carte ou un message de confirmation
        messagebox.showinfo("Réponse", "Votre réponse est enregistrée")
        self.initialize_card_mat()
