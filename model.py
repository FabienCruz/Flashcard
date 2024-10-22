import sqlite3

class Database:
    def __init__(self, db_name="flashcards.db"):
        self.connexion = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        # Création des tables "decks" et "cards"
        try:
            with self.connexion:
                self.connexion.execute("""
                    CREATE TABLE IF NOT EXISTS decks (
                        deck_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        thema TEXT NOT NULL
                    );
                """)
                self.connexion.execute("""
                    CREATE TABLE IF NOT EXISTS cards (
                        card_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        question TEXT NOT NULL,
                        answer TEXT NOT NULL,
                        priority INTEGER DEFAULT 1,
                        deck_id INTEGER,
                        FOREIGN KEY(deck_id) REFERENCES decks(deck_id) ON DELETE CASCADE
                    );
                """)
        except sqlite3.Error as e:
            print(f"Erreur lors de la création des tables : {e}")

    def close(self):
        # Méthode pour fermer la connexion à la base de données
        self.connexion.close()

class Deck:
    def __init__(self, db):
        self.connexion = db.connexion

    def add_deck(self, thema):
        try:
            with self.connexion:
                self.connexion.execute("INSERT INTO decks (thema) VALUES (?);", (thema,))
        except sqlite3.Error as e:
            print(f"Erreur lors de l'ajout du deck : {e}")

    def delete_deck(self, deck_id):
        try:
            with self.connexion:
                self.connexion.execute("DELETE FROM decks WHERE deck_id = ?;", (deck_id,))
        except sqlite3.Error as e:
            print(f"Erreur lors de la suppression du deck : {e}")

    def get_deck(self, deck_id):
        try:
            cur = self.connexion.cursor()
            cur.execute("SELECT * FROM decks WHERE deck_id = ?;", (deck_id,))
            return cur.fetchone()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération du deck : {e}")
            return None

    def get_all_decks(self):
        try:
            cur = self.connexion.cursor()
            cur.execute("SELECT * FROM decks;")
            return cur.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des decks : {e}")
            return []

class Card:
    def __init__(self, db):
        self.connexion = db.connexion

    def add_card(self, question, answer, priority, deck_id):
        try:
            with self.connexion:
                self.connexion.execute("""
                    INSERT INTO cards (question, answer, priority, deck_id)
                    VALUES (?, ?, ?, ?);
                """, (question, answer, priority, deck_id))
        except sqlite3.Error as e:
            print(f"Erreur lors de l'ajout de la carte : {e}")

    def delete_card(self, card_id):
        try:
            with self.connexion:
                self.connexion.execute("DELETE FROM cards WHERE card_id = ?;", (card_id,))
        except sqlite3.Error as e:
            print(f"Erreur lors de la suppression de la carte : {e}")

    def get_card(self, card_id):
        try:
            cur = self.connexion.cursor()
            cur.execute("SELECT * FROM cards WHERE card_id = ?;", (card_id,))
            return cur.fetchone()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération de la carte : {e}")
            return None

    def get_all_cards(self):
        try:
            cur = self.connexion.cursor()
            cur.execute("SELECT * FROM cards;")
            return cur.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des cartes : {e}")
            return []

    def get_cards_by_deck(self, deck_id):
        try:
            cur = self.connexion.cursor()
            cur.execute("SELECT * FROM cards WHERE deck_id = ?;", (deck_id,))
            return cur.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des cartes par deck : {e}")
            return []
