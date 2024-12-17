import sqlite3

class Card:
    """
    Classe gérant les opérations sur les cartes.
    """
    def __init__(self, db):
        """
        Initialise la gestion des cartes.
        
        Args:
            db (Database): Instance de la classe Database
        """
        self.connexion = db.connexion
        self.create_table()

    def create_table(self):
        """Crée la table des cartes si elle n'existe pas."""
        try:
            with self.connexion:
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
            print(f"Erreur lors de la création de la table 'cards' : {e}")

    def add_card(self, question, answer, priority, deck_id):
        """
        Ajoute une nouvelle carte dans la base de données.
        
        Args:
            question (str): La question de la carte
            answer (str): La réponse de la carte
            priority (int): La priorité de la carte
            deck_id (int): L'ID du deck auquel appartient la carte
            
        Returns:
            bool: True si l'ajout a réussi, False sinon
        """
        try:
            with self.connexion:
                # Vérifier que le deck existe
                cur = self.connexion.cursor()
                cur.execute("SELECT deck_id FROM decks WHERE deck_id = ?;", (deck_id,))
                if not cur.fetchone():
                    print(f"Erreur : le deck_id {deck_id} n'existe pas")
                    return False
                
                # Ajouter la carte
                cur.execute("""
                    INSERT INTO cards (question, answer, priority, deck_id)
                    VALUES (?, ?, ?, ?);
                """, (question, answer, priority, deck_id))
                return True
        except sqlite3.Error as e:
            print(f"Erreur lors de l'ajout de la carte : {e}")
            return False

    def get_all_cards(self):
        """
        Récupère toutes les cartes de la base de données.
        
        Returns:
            list: Liste de tuples (card_id, question, answer, priority, deck_id)
        """
        try:
            cur = self.connexion.cursor()
            cur.execute("""
                SELECT card_id, question, answer, priority, deck_id 
                FROM cards 
                ORDER BY priority DESC;
            """)
            return cur.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des cartes : {e}")
            return []

    def get_cards_by_decks(self, deck_ids):
        """
        Récupère les cartes correspondant aux decks sélectionnés.
        
        Args:
            deck_ids (list): Liste des deck_id sélectionnés
            
        Returns:
            list: Liste de tuples (card_id, question, answer, priority, deck_id, thema)
        """
        try:
            cur = self.connexion.cursor()
            placeholders = ','.join('?' * len(deck_ids))
            query = f"""
                SELECT c.card_id, c.question, c.answer, c.priority, c.deck_id, d.thema
                FROM cards c
                JOIN decks d ON c.deck_id = d.deck_id
                WHERE c.deck_id IN ({placeholders})
                ORDER BY c.priority ASC;
            """
            cur.execute(query, deck_ids)
            return cur.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des cartes par deck : {e}")
            return []

    def get_card_by_id(self, card_id):
        """
        Récupère une carte spécifique par son ID.
        
        Args:
            card_id (int): L'ID de la carte à récupérer
            
        Returns:
            tuple: (card_id, question, answer, priority, deck_id) ou None si non trouvé
        """
        try:
            cur = self.connexion.cursor()
            cur.execute(
                "SELECT card_id, question, answer, priority, deck_id FROM cards WHERE card_id = ?;",
                (card_id,)
            )
            return cur.fetchone()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération de la carte {card_id} : {e}")
            return None
    
    def get_cards_by_deck_id(self, deck_id):
        """
        Récupère les cartes d'un deck spécifique.
        
        Args:
            deck_id (int): L'ID du deck
        
        Returns:
            list: Liste de tuples (card_id, question, answer, priority, deck_id)
        """
        try:
            cur = self.connexion.cursor()
            cur.execute("""
                SELECT card_id, question, answer, priority, deck_id 
                FROM cards 
                WHERE deck_id = ? 
                ORDER BY priority DESC;
            """, (deck_id,))
            return cur.fetchall()
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des cartes du deck {deck_id} : {e}")
            return []


    def update_card_priority(self, card_id, new_priority):
        """
        Met à jour la priorité d'une carte.
        
        Args:
            card_id (int): L'ID de la carte à modifier
            new_priority (int): La nouvelle priorité
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            with self.connexion:
                cur = self.connexion.cursor()
                cur.execute("""
                    UPDATE cards 
                    SET priority = ? 
                    WHERE card_id = ?;
                """, (new_priority, card_id))
                return cur.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour de la priorité : {e}")
            return False
    
    def update_card(self, card_id, new_question, new_answer):
        """
        Met à jour une carte.
        
        Args:
            card_id (int): L'ID de la carte à modifier
            new_question (str): La nouvelle question
            new_answer (str): La nouvelle réponse
            
        Returns:
            bool: True si la mise à jour a réussi, False sinon
        """
        try:
            with self.connexion:
                cur = self.connexion.cursor()
                cur.execute("""
                    UPDATE cards 
                    SET question = ?, answer = ? 
                    WHERE card_id = ?;
                """, (new_question, new_answer, card_id))
                return cur.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erreur lors de la mise à jour de la carte {card_id} : {e}")
            return False
    
    def delete_card(self, card_id):
        """
        Supprime une carte de la base de données.
        
        Args:
            card_id (int): L'ID de la carte à supprimer
            
        Returns:
            bool: True si la suppression a réussi, False sinon
        """
        try:
            with self.connexion:
                cur = self.connexion.cursor()
                cur.execute(
                    "DELETE FROM cards WHERE card_id = ?;",
                    (card_id,)
                )
                return cur.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erreur lors de la suppression de la carte {card_id} : {e}")
            return False