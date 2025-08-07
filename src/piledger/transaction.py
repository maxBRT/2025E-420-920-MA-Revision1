class Transaction:
    """
    Represents a transaction.

    Attributes:
        no_txn (int or str): The unique transaction number or ID.
        date (str): The date of the transaction (YYYY-MM-DD).
        compte (str): The account associated with the transaction.
        montant (float): The amount of the transaction.
        commentaire (str): Optional comment or description about the transaction.

    Methods:
        __str__(): Returns a readable string representation of the transaction.
    """

    def __init__(self, no_txn, date, compte, montant, commentaire):
        self.no_txn = no_txn
        self.date = date
        self.compte = compte
        self.montant = montant
        self.commentaire = commentaire

    def __str__(self):
        result = (
            f"Transaction #{self.no_txn} | "
            f"Date: {self.date} | "
            f"Compte: {self.compte} | "
            f"Montant: {self.montant}"
        )

        if self.commentaire:
            result += f" | Commentaire: {self.commentaire}"

        return result
