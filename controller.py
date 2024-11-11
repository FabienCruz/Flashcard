class Play:
    def __init__(self, db, deck, card):
        self.db = db
        self.deck = deck
        self.card = card
    
    def get_decks(self):
        return self.deck.get_all_decks()
    
    def close_database(self):
        self.db.close()

    def on_deck_selection(self, check_vars, thema_list):
        selected_themes = [thema_list[i] for i, var in enumerate(check_vars) if var.get() == 1]
        return selected_themes

    def get_cards_by_deck(self, selected_decks):
        selected_themes_ids = [theme[0] for theme in selected_decks]
        return self.card.get_cards_by_decks(selected_themes_ids)
    
    def pick_a_card(self, selected_decks_id):
        print("pick a card", selected_decks_id)
        cards = self.card.get_cards_by_decks(selected_decks_id)
        # les cartes doivent être classées par priorité
        return print("cards", cards)  

    def show_question():
        pass

    def show_answer():
        pass

class ManageCards:
    pass

class ManageDecks:
    pass

"""
# controller.py
class TaskController:
    def __init__(self, model):
        self.model = model

    def add_task(self, description):
        self.model.add_task(description)

    def show_tasks(self):
        return self.model.get_tasks()
"""