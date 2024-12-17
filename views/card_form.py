from tkinter import messagebox, Toplevel, Text, Button, Label
from tkinter.scrolledtext import ScrolledText


class CardForm(Toplevel):
    def __init__(self, parent, manage_card, deck_id=None, card=None, callback=None):
        super().__init__(parent)
        self.title("Ajouter une carte" if card is None else "Modifier une carte")
        self.manage_card = manage_card
        self.card = card
        self.deck_id = deck_id
        self.callback = callback
        self.geometry("400x320")

        # Champ "question"
        Label(self, text="Question (150 caractères max):").pack(pady=5)
        self.question_text = Text(self, height=3, width=40)
        self.question_text.pack(pady=5)
        self.question_text.bind("<KeyRelease>", self.limit_question_length)
        
        # Champ "réponse"
        Label(self, text="Réponse:").pack(pady=5)
        self.answer_text = ScrolledText(self, height=10, width=40)
        self.answer_text.pack(pady=5)
        
        # Pré-remplir les champs si une carte est fournie
        if card:
            """
            insère le texte de la question et de la réponse dans les champs correspondants
            card est un tuple (id, question, answer, priority, deck_id)
            """
            self.question_text.insert("1.0", card[1])
            self.answer_text.insert("1.0", card[2])
        
        # Bouton "Enregistrer"
        Button(self, text="Enregistrer", command=self.save_card).pack(pady=10)
    
    def limit_question_length(self, event):
        """Limite la longueur du texte dans le champ question à 150 caractères."""
        if len(self.question_text.get("1.0", "end-1c")) > 150:
            self.question_text.delete("1.0 + 150c", "end")
    
    def save_card(self):
        """Enregistre la carte."""
        deck_id = self.deck_id
        question = self.question_text.get("1.0", "end-1c").strip()
        answer = self.answer_text.get("1.0", "end-1c").strip()
        priority = 1
        
        if not question or not answer:
            messagebox.showwarning("Avertissement", "Les champs question et réponse ne peuvent pas être vides.")
            return
        
        if self.card:
            # Modifier la carte existante
            """
            la méthode update_card attend trois arguments:
                - card_id : int
                - question : str
                - answer : str
            card est un tuple (id, question, answer, priority, deck_id)
            """
            self.manage_card.update_card(self.card[0], question, answer)
            messagebox.showinfo("Information", "Carte modifiée avec succès.")
        else:
            # Ajouter une nouvelle carte
            self.manage_card.add_card(question, answer, priority, deck_id)
            messagebox.showinfo("Information", "Carte ajoutée avec succès.")
        
        # appeler le callback si fourni
        if self.callback:
            self.callback()

        self.destroy()