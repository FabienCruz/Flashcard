from model import Database, Card, Deck
from controller import Play
from view import Screen, Dealer, CardMat

def main():
    # création de la base de données
    db = Database()
    # charger les données
    deck = Deck(db)
    card = Card(db)
    play = Play(db, deck, card)
    # afficher l'écran
    screen = Screen(play)
    dealer = Dealer(screen)
    card_mat = CardMat(screen, dealer)
    # lancer l'application
    screen.run()
    # fermeture de la base de données
    db.close()

if __name__ == "__main__":
    main()