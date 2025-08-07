import collections
import csv
import os
import sys
from typing import List
from piledger.compte import Account
from piledger.transaction import Transaction


def read_data_file(filepath: str) -> List[Transaction]:
    """Reads transactions from a CSV file and returns a list of Transaction objects."""
    if not os.path.exists(filepath):
        print(f"ERREUR: Le fichier '{filepath}' est introuvable!")
        print("Assurez-vous que le fichier se trouve à la racine du répertoire.")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        transactions = [
            Transaction(
                no_txn=row["No txn"],
                date=row["Date"],
                compte=row["Compte"],
                montant=float(row["Montant"]),
                commentaire=row["Commentaire"],
            )
            for row in reader
        ]

    if not transactions:
        print("ERREUR: Aucune donnée n'a pu être chargée!")
        print(f"Vérifiez le contenu de {filepath}")
        sys.exit(1)

    return transactions


def get_all_accounts(transactions: List[Transaction]) -> List[Account]:
    """Get all unique accounts form a list of Transaction and return a list of Account"""
    accounts: List[Account] = []
    d = collections.defaultdict(list)
    for t in transactions:
        d[t.compte].append(t)
    accounts.extend([Account(name=k, transactions=v) for k, v in d.items()])
    return accounts
