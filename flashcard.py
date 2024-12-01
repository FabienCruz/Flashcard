from model import Database, Card, Deck
from controller import ManageDB, ManageDeck, ManageCard
from view import Screen, Dealer, CardMat, DeckManagerScreen

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
    # afficher les écrans
    screen = Screen(manage_db)
    dealer = Dealer(screen, manage_deck)
    card_mat = CardMat(screen, dealer, manage_card)
    # lancer l'application
    screen.run()
    # fermeture de la base de données
    db.close()

if __name__ == "__main__":
    main()