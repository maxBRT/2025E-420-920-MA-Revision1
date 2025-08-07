import os
from piledger.load_data import read_data_file, get_all_accounts
from piledger.handler import (
    handle_balance_inquiry,
    handle_date_search,
    handle_display_all_transactions,
    handle_display_summary,
    handle_export,
    handle_get_transactions_by_accounts,
    handle_statistics,
)

DATA_PATH = "data.csv"


def display_menu():
    print("\n" + "=" * 50)
    print("SYSTÈME DE GESTION COMPTABLE PERSONNEL")
    print("=" * 50)
    print("1. Afficher le solde d'un compte")
    print("2. Afficher toutes les transactions")
    print("3. Afficher les transactions d'un compte")
    print("4. Afficher le résumé de tous les comptes")
    print("5. Afficher les statistiques")
    print("6. Exporter les écritures d'un compte")
    print("7. Rechercher par période")
    print("0. Quitter")
    print("=" * 50)


def main():
    # Load the handlers as callable in a dictionnairy
    choice_dict = {
        "1": lambda: handle_balance_inquiry(accounts),
        "2": lambda: handle_display_all_transactions(transactions),
        "3": lambda: handle_get_transactions_by_accounts(accounts),
        "4": lambda: handle_display_summary(accounts),
        "5": lambda: handle_statistics(transactions, accounts),
        "6": lambda: handle_export(transactions, accounts),
        "7": lambda: handle_date_search(transactions),
    }

    print("Chargement des données...")

    # Initializing data
    transactions = read_data_file(DATA_PATH)
    accounts = get_all_accounts(transactions)

    print(f"✅ {len(transactions)} transactions chargées avec succès!")

    # Main program loop
    running = True
    while running:
        display_menu()
        choice = input("\nVotre choix: ").strip()

        if choice == "exit" or choice == "quit" or choice == "0":
            print("\nMerci d'avoir utilisé le système de gestion comptable!")
            print("\nAu revoir!")
            running = False

        # Call the corresponding handler from the dictionnairy
        elif choice in choice_dict:
            choice_dict[choice]()

        else:
            print("❌ Choix invalide! Veuillez sélectionner une option valide.")

        if running:
            input("\nAppuyez sur Entrée pour continuer...")


if __name__ == "__main__":
    main()
