class ManageDB:
    def __init__(self, db):
        """Initialize the ManageDB controller.
        
        Initializes the controller with the given database, deck, and card.

        Args:
            db: The database instance to be used by the controller.
        """
        self.db = db
    
    def close_database(self):
        self.db.close()

class ManageDeck(ManageDB):
    def __init__(self, db, deck):
        super().__init__(db)
        self.deck = deck

    def get_decks(self):
        return self.deck.get_all_decks()

    def on_deck_selection(self, check_vars, thema_list):
        selected_themes = [thema_list[i] for i, var in enumerate(check_vars) if var.get() == 1]
        return selected_themes
    
    def add_deck(self, deck_name):
        return self.deck.add_deck(deck_name)
    
    def update_deck(self, deck_id, deck_name):
        return self.deck.update_deck(deck_id, deck_name)
    
    def delete_deck(self, deck_id):
        return self.deck.delete_deck(deck_id)

class ManageCard(ManageDB):
    def __init__(self, db, card):
        super().__init__(db)
        self.card = card
    
    def get_cards_by_deck(self, selected_decks):
        selected_themes_ids = [theme[0] for theme in selected_decks]
        return self.card.get_cards_by_decks(selected_themes_ids)
    
    def pick_a_card(self, selected_decks_id):
        if not selected_decks_id:
            return None
        # sélectionne les cartes avec les paquets sélectionnés
        cards = self.get_cards_by_deck(selected_decks_id)
        # retourne la première carte
        return cards[0]
      
    def update_card_priority(self, card_id, current_priority, is_good_answer):
        new_priority = current_priority + 1 if is_good_answer else 1
        return self.card.update_card_priority(card_id, new_priority)

    def add_card(self, deck_id, question, answer):
        return self.card.add_card(deck_id, question, answer)

    def update_card(self, card_id, question, answer):
        return self.card.update_card(card_id, question, answer)

    def delete_card(self, card_id):
        return self.card.delete_card(card_id)   