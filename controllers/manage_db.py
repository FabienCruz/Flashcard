
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