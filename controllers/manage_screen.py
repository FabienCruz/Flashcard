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
            self.screen.show_return_button()
    
    def update_card_manager(self, deck_id):
        """Met à jour l'écran de gestion des cartes"""
        if self.screen and self.screen.card_screen:
            self.screen.card_screen.load_cards(deck_id)