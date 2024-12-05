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
        self.selected_decks = []

    def get_decks(self):
        return self.deck.get_all_decks()

    def on_deck_selection(self, check_vars, thema_list):
        selected_themes = [thema_list[i] for i, var in enumerate(check_vars) if var.get() == 1]
        return selected_themes
    
    def update_selected_decks(self, check_vars):
        thema_list = self.get_decks()
        self.selected_decks = self.on_deck_selection(check_vars, thema_list)

    def get_selected_decks(self):
        return self.selected_decks
    
    def add_deck(self, deck_name):
        return self.deck.add_deck(deck_name)
    
    def update_deck(self, deck_id, deck_new_name):
        return self.deck.update_deck(deck_id, deck_new_name)
    
    def delete_deck(self, deck_id):
        return self.deck.delete_deck(deck_id)

class ManageCard(ManageDB):
    def __init__(self, db, card):
        super().__init__(db)
        self.card = card
    
    def get_cards_by_deck(self, selected_decks):
        selected_themes_ids = [theme[0] for theme in selected_decks]
        return self.card.get_cards_by_decks(selected_themes_ids)
    
    def get_cards_by_deck_id(self, deck_id):
        return self.card.get_cards_by_deck_id(deck_id)
    
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

class ManageScreen:
    def __init__(self, manage_db, manage_deck, manage_card):
        self.manage_db = manage_db
        self.manage_deck = manage_deck
        self.manage_card = manage_card
        self.screen = None
    
    def set_screen(self, screen):
        self.screen = screen
    
    def show_game_screen(self):
        """Coordonne l'affichage de l'écran de jeu"""
        if self.screen:
            self.screen.show_game()

    def show_manager_screen(self):
        """Coordonne l'affichage des écrans de gestion des paquets et des cartes"""
        if self.screen:
            self.screen.show_deck_manager()
            self.screen.show_card_manager()
    
    def update_card_manager(self, deck_id):
        """Met à jour l'écran de gestion des cartes"""
        if self.screen and self.screen.card_screen:
            self.screen.card_screen.load_cards(deck_id)
    
    
