from models import Database, Card, Deck
from controllers import ManageDB, ManageDeck, ManageCard, ManageScreen
from views import Screen, Dealer, CardMat, DeckManagerScreen, CardManagerScreen, ReturnButton

def main():
    
    # création de la base de données
    db = Database()
    
    # charger les données
    deck = Deck(db)
    card = Card(db)
    
    # initialiser les contrôleurs
    manage_db = ManageDB(db)
    manage_deck = ManageDeck(db, deck)
    manage_card = ManageCard(db, card)
    manage_screen = ManageScreen(manage_db, manage_deck, manage_card)
    
    # instancie les écrans (accueil)
    screen = Screen(manage_screen)
    manage_screen.set_screen(screen)
    
    # instancie les écrans (gestion)
    deck_screen = DeckManagerScreen(screen, manage_screen)
    card_screen = CardManagerScreen(screen, manage_screen)
    return_button = ReturnButton(screen, manage_screen)
    screen.set_managers(deck_screen, card_screen, return_button)

    # instancie les écrans (jeu)
    dealer = Dealer(screen, manage_screen)
    card_mat = CardMat(screen, manage_screen)
    screen.set_game(dealer, card_mat)
    
    # lancer l'application, boucle principale Tkinter (mainloop)
    screen.after(0, manage_screen.show_game_screen)
    screen.run()
    
    # fermeture de la base de données
    db.close()

if __name__ == "__main__":
    main()