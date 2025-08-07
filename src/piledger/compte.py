from piledger.transaction import Transaction


class Account:
    """
    Represents an  account with a name and associated transactions.

    This class stores transactions related to the account and provides
    methods to calculate the account balance and display its transactions.

    Attributes:
        name (str): The name of the account.
        transactions (List[Transaction]): A list of Transaction objects associated with the account.

    Methods:
        calculate_balance(): Computes and prints the total balance by summing transaction amounts.
        display_transactions(): Prints a list of all transactions for the account, or a message if none exist.
    """

    def __init__(self, name, transactions):
        self.name = name
        self.transactions = transactions

    def calculate_balance(self):
        balance = 0.0
        for txn in self.transactions:
            balance += txn.montant
        print(f"\nSolde du compte '{self.name}': {balance}$")

    def display_transactions(self):
        print(f"\n=== TRANSACTIONS POUR LE COMPTE '{self.name}' ===")

        if len(self.transactions) < 1:
            print(f"Aucune transaction trouvée pour le compte '{self.name}'")
        else:
            for txn in self.transactions:
                print(txn)
