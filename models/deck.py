import sqlite3

class Deck:
    """
    Classe gérant les opérations sur les decks de cartes.
    """
    def __init__(self, db):
        """
        Initialise la gestion des decks.
        
        Args:
            db (Database): Instance de la classe Database
        """
        self.connexion = db.connexion
        self.create_table()

    def create_table(self):
        """Crée la table des decks si elle n'existe pas."""
        try:
            with self.connexion:
                self.connexion.execute("""
                    CREATE TABLE IF NOT EXISTS decks (
                        deck_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        thema TEXT NOT NULL UNIQUE
                    );
                """)
        except sqlite3.Error as e:
            print(f"Erreur lors de la création de la table 'decks' : {e}")

    def add_deck(self, thema):
        """
        Ajoute un nouveau deck.
        
        Args:
            thema (str): Le thème du deck
            
        Returns:
            bool: True si l'ajout a réussi, False sinon
        """
        try:
            with self.connexion:
                self.connexion.execute(
                    "INSERT INTO decks (thema) VALUES (?);", 
                    (thema,)
                )
                return True
        except sqlite3.Error as e:
            print(f"Erreur lors de l'ajout du deck : {e}")
            return False

    def get_all_decks(self):
        """
        Récupère tous les decks de la base de données.
        
        Returns:
            list: Liste de tuples (deck_id, thema)
        """
        try:
            cur = self.connexion.cursor()
            cur.execute("SELECT deck_id, thema FROM decks ORDER BY deck_id;")
            return cur.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des decks : {e}")
            return []

    def get_deck_by_id(self, deck_id):
        """
        Récupère un deck spécifique par son ID.
        
        Args:
            deck_id (int): L'ID du deck à récupérer
            
        Returns:
            tuple: (deck_id, thema) ou None si non trouvé
        """
        try:
            cur = self.connexion.cursor()
            cur.execute(
                "SELECT deck_id, thema FROM decks WHERE deck_id = ?;",
                (deck_id,)
            )
            return cur.fetchone()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération du deck {deck_id} : {e}")
            return None
        
    def update_deck(self, deck_id, new_thema):
        """
        Met à jour le thème d'un deck.
        
        Args:
            deck_id (int): L'ID du deck à modifier
            new_thema (str): Le nouveau thème
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            with self.connexion:
                cur = self.connexion.cursor()
                cur.execute(
                    "UPDATE decks SET thema = ? WHERE deck_id = ?;",
                    (new_thema, deck_id)
                )
                return cur.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour du deck {deck_id} : {e}")
            return False
    
    def delete_deck(self, deck_id):
        """
        Supprime un deck de la base de données.
        
        Args:
            deck_id (int): L'ID du deck à supprimer
            
        Returns:
            bool: True si la suppression a réussi, False sinon
        """
        try:
            with self.connexion:
                cur = self.connexion.cursor()
                cur.execute(
                    "DELETE FROM decks WHERE deck_id = ?;",
                    (deck_id,)
                )
                return cur.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erreur lors de la suppression du deck {deck_id} : {e}")
            return False
