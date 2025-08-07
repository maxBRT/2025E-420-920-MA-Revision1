from typing import List
from piledger.compte import Account
from piledger.transaction import Transaction


def handle_balance_inquiry(accounts: List[Account]):
    """Get user input to find the Account and print its balance"""
    print("\n--- Consultation de solde ---")
    print("Comptes disponibles:")

    for a in accounts:
        print(f"  - {a.name}")

    account_input = input("\nEntrez le nom du compte: ").strip()

    if not account_input:
        print("Nom de compte invalide!")
        return
    try:
        a = _find_account(accounts, account_input)
    except ValueError:
        print(f"Compte '{account_input}' introuvable!")
        print("Vérifiez l'orthographe ou choisissez un compte dans la liste.")
        return

    a.calculate_balance()


def handle_statistics(data: List[Transaction], accounts: List[Account]):
    """
    Fetch statistics: total income, total expense, net_worth and largers expense
    """
    print("\n=== STATISTIQUES FINANCIÈRES ===")

    total_income = _find_total_income(data)
    total_expenses = _find_total_expenses(data)
    net_worth = total_income - total_expenses

    print(f"Revenus totaux: {total_income:.2f}$")
    print(f"Dépenses totales: {total_expenses:.2f}$")
    print(f"Situation nette: {net_worth:.2f}$")

    if net_worth > 0:
        print("📈 Situation financière positive")
    elif net_worth < 0:
        print("📉 Situation financière négative")
    else:
        print("⚖️  Situation financière équilibrée")

    largest_expense = _find_largest_expense(data)
    if largest_expense:
        print(
            f"\nPlus grosse dépense: {largest_expense.montant:.2f}$ ({largest_expense.compte})"
        )
        if largest_expense.commentaire:
            print(f"Commentaire: {largest_expense.commentaire}")

    for a in accounts:
        if a.name == "Compte courant":
            a.calculate_balance()


def handle_date_search(data: List[Transaction]):
    """Get user input and find transactions for the given period"""
    print("\n--- Recherche par période ---")
    start_date = input("Date de début (YYYY-MM-DD): ").strip()
    end_date = input("Date de fin (YYYY-MM-DD): ").strip()

    if not start_date or not end_date:
        print("Dates invalides!")
        return

    filtered_data = _get_transactions_by_date_range(data, start_date, end_date)

    if len(filtered_data) == 0:
        print(f"Aucune transaction trouvée entre {start_date} et {end_date}")
    else:
        print(
            f"\n{len(filtered_data)} écritures(s) trouvée(s) entre {start_date} et {end_date}:"
        )
        for t in filtered_data:
            print(t)


def handle_export(data, accounts):
    """Get user input to select an account and export its details in a csv file"""
    print("\n--- Exportation ---")
    print("Comptes disponibles:")
    for a in accounts:
        print(f"- {a.name}")

    account_input = input("\nEntrez le nom du compte à exporter: ").strip()

    if not account_input:
        print("Nom de compte invalide!")
        return

    try:
        a = _find_account(accounts, account_input)
    except ValueError:
        print(f"Compte '{account_input}' introuvable!")
        print("Vérifiez l'orthographe ou choisissez un compte dans la liste.")

    filename = input("Nom du fichier de sortie (ex: export.csv): ").strip()
    if not filename:
        filename = f"export_{a.name.replace(' ', '_').lower()}.csv"
    _export_account_postings(a, filename)


def handle_get_transactions_by_accounts(accounts: List[Account]):
    """Get user input to fetch all transactions for one accounts"""
    print("\n--- Transactions par compte ---")
    print("Comptes disponibles:")

    for a in accounts:
        print(f"- {a.name}")

    account_input = input("\nEntrez le nom du compte: ").strip()

    if account_input:
        try:
            a = _find_account(accounts, account_input)
            a.display_transactions()
        except ValueError as e:
            print(e)


def handle_display_all_transactions(data: List[Transaction]):
    """Print the given list of Transaction"""
    print("\n=== TOUTES LES TRANSACTIONS ===")
    for t in data:
        print(t)


def handle_display_summary(accounts: List[Account]):
    """Print the balance of all Account in the given list"""
    print("\n=== RÉSUMÉ DES COMPTES ===")
    for a in accounts:
        a.calculate_balance()


def _export_account_postings(a: Account, filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("No txn,Date,Compte,Montant,Commentaire\n")
        for t in a.transactions:
            f.write(f"{t.no_txn}, {t.date}, {t.compte}, {t.montant}, {t.commentaire}")
    print(f"Écritures exportées vers {filename}")


def _find_account(accounts, input) -> Account:
    for a in accounts:
        if a.name.lower().strip() == input.lower():
            return a
    raise ValueError(f"Compte '{input}' introuvable")


def _get_transactions_by_date_range(data, start_date, end_date):
    filtered_transactions = []
    for t in data:
        if start_date <= t.date <= end_date:
            filtered_transactions.append(t)
    return filtered_transactions


def _find_largest_expense(data: List[Transaction]) -> Transaction:
    largest_expense = None
    max_amount = 0
    for t in data:
        if (
            t.compte != "Compte courant"
            and t.compte != "Revenu"
            and t.montant > max_amount
        ):
            largest_expense = t
        else:
            continue

    return largest_expense


def _find_total_income(data: List[Transaction]) -> float:
    total = 0
    for t in data:
        if t.compte == "Revenu":
            total += abs(t.montant)
    return total


def _find_total_expenses(data: List[Transaction]) -> float:
    total = sum(
        t.montant
        for t in data
        if t.compte != "Compte courant" and t.compte != "Revenu" and t.montant > 0
    )
    return total
