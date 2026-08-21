import json
from datetime import date

transactions = []


def save_transactions():
    with open('transactions.json', 'w') as file:
        json.dump(transactions, file)


def load_transactions():
    global transactions
    try:
        with open('transactions.json', 'r') as file:
            transactions = json.load(file)
    except FileNotFoundError:
        transactions = []
    except json.JSONDecodeError:
        print('Warning: transactions.json is corrupted.')
        transactions = []


class TransactionCancelled(Exception):
    pass


def check_for_cancel(value):
    if value.lower() == 'cancel':
        raise TransactionCancelled


def get_transaction_type():
    while True:
        transaction_type = input('Transaction Type: ').strip().lower()

        check_for_cancel(transaction_type)

        if transaction_type in ('income', 'i'):
            return 'income'
        elif transaction_type in ('expense', 'e'):
            return 'expense'
        else:
            print('Please enter "income/i", "expense/e" or "cancel".')


def get_amount():
    while True:
        amount_input = input('Amount: ').strip()

        check_for_cancel(amount_input)

        try:
            amount = float(amount_input)
        except ValueError:
            print('Please enter a valid number!')
            continue
        if amount <= 0:
            print('Amount must be greater than zero!')
            continue
        return amount


def add_transaction():
    print('=' * 15)
    print('ADD TRANSACTION')
    print('=' * 15)
    print('You can cancel at any time by typing "cancel".')
    print('Press Enter to leave optional fields empty.')

    try:
        transaction_type = get_transaction_type()
        amount = get_amount()
        category = get_category()
        transaction_date = get_transaction_date()
        person = get_person()

        if person:
            relationship = get_relationship()
        else:
            relationship = 'normal'
        description = get_description()
        transaction = {
            'type': transaction_type,
            'amount': amount,
            'category': category,
            'person': person,
            'relationship': relationship,
            'description': description,
            'date': transaction_date
        }
        transactions.append(transaction)
        save_transactions()
        print('Transaction added successfully!')
    except TransactionCancelled:
        print('Transaction cancelled.')


def get_optional_input(prompt):
    value = input(prompt).strip()

    check_for_cancel(value)
    return value


def get_category():
    return get_optional_input('Category (optional): ')


def get_person():
    return get_optional_input('Person (optional): ')


def get_description():
    return get_optional_input('Description (optional): ')


def get_relationship():
    while True:
        relationship_input = input('''Please choose the relationship:
1. Normal transaction
2. I lent money
3. I borrowed money
4. Cancel

Choose an option: ''').strip()

        check_for_cancel(relationship_input)

        try:
            relationship = int(relationship_input)
        except ValueError:
            print('Please enter 1, 2, 3, or 4.')
            continue

        if relationship == 1:
            return 'normal'
        elif relationship == 2:
            return 'lent'
        elif relationship == 3:
            return 'borrowed'
        elif relationship == 4:
            raise TransactionCancelled
        else:
            print('Please choose 1, 2, 3, or 4.')


def view_transactions(person=None):
    if not transactions:
        print('No transactions yet.')
        return

    number_header = '#'
    date_header = 'DATE'
    type_header = 'TYPE'
    amount_header = 'AMOUNT'
    category_header = 'CATEGORY'
    person_header = 'PERSON'
    relationship_header = 'RELATIONSHIP'
    description_header = 'DESCRIPTION'

    print('_' * 147)
    print(
        f"{number_header:<4} | "
        f"{date_header:^12} | "
        f"{type_header:^10} | "
        f"{amount_header:^20} | "
        f"{category_header:^20} | "
        f"{person_header:^20} | "
        f"{relationship_header:^20} | "
        f"{description_header:^20}"
    )
    print('_' * 147)

    found_match = False
    for number, transaction in enumerate(transactions, start=1):
        if transaction['type'] == 'income':
            display_amount = f'+${transaction['amount']:,.2f}'
        elif transaction['type'] == 'expense':
            display_amount = f'-${transaction['amount']:,.2f}'

        if (
            person is None
            or person.strip().lower()
            == transaction['person'].strip().lower()
        ):
            found_match = True
            print(
                f"{str(number) + '.':<4} | "
                f"{str(transaction['date']):^12} | "
                f"{transaction['type'].upper():^10} | "
                f"{display_amount:>20} | "
                f"{transaction['category']:^20} | "
                f"{transaction['person']:^20} | "
                f"{transaction['relationship']:^20} | "
                f"{transaction['description']:^20}"
            )

    if not found_match:
        print('No transaction found for this person.')


def get_transaction_number(action):
    while True:
        transaction_number = input(
            f'Choose the number of the transaction to {action}: ').strip()

        check_for_cancel(transaction_number)

        try:
            transaction_number = int(transaction_number)
        except ValueError:
            print('Invalid number.')
            continue
        if transaction_number == 0:
            raise TransactionCancelled

        if not 1 <= transaction_number <= len(transactions):
            print('Please choose a number within the transaction numbers. ')
            continue

        return transaction_number


def delete_transaction():
    print('=' * 18)
    print('DELETE TRANSACTION')
    print('=' * 18)
    print('You will be asked to confirm the deletion after selecting a transaction.')
    print('Enter 0 or type "cancel" to cancel.')

    if not transactions:
        print('There is no transaction to delete.')
        return

    view_transactions()

    try:
        transaction_number = get_transaction_number('delete')

        while True:
            confirm_deletion = input(
                'Delete this transaction? (y/n): ').strip().lower()

            if confirm_deletion in ('y', 'yes'):
                transactions.pop(transaction_number - 1)
                save_transactions()
                print('Transaction deleted successfully!')
                return
            elif confirm_deletion in ('n', 'no'):
                print('Deletion cancelled.')
                return
            else:
                print('Please enter yes/y or no/n.')

    except TransactionCancelled:
        print('Deletion cancelled.')


def edit_transaction():
    if not transactions:
        print('There is no transaction to edit.')
        return

    print('=' * 18)
    print('EDIT TRANSACTION')
    print('=' * 18)
    print('You can cancel at any time by typing "cancel".')

    view_transactions()

    try:
        transaction_number = get_transaction_number('edit')
    except TransactionCancelled:
        print('Editing cancelled.')
        return

    transaction = transactions[transaction_number - 1]

    while True:
        edit_input = input('''Choose what to edit:
1. Transaction Type
2. Amount
3. Category
4. Date
5. Person
6. Relationship
7. Description
8. Cancel Edit 

Choose an option: ''').strip()

        try:
            check_for_cancel(edit_input)
        except TransactionCancelled:
            print('Editing cancelled.')
            return

        try:
            edit = int(edit_input)
        except ValueError:
            print('Please enter a valid number or type "cancel".')
            continue

        if not 1 <= edit <= 8:
            print('Please enter a number from 1 to 8.')
            continue
        try:
            if edit == 1:
                transaction['type'] = get_transaction_type()
            elif edit == 2:
                transaction['amount'] = get_amount()
            elif edit == 3:
                transaction['category'] = get_category()
            elif edit == 4:
                transaction['date'] = get_transaction_date()
            elif edit == 5:
                new_person = get_person()

                if not new_person:
                    transaction['person'] = ''
                    transaction['relationship'] = 'normal'
                else:
                    while True:
                        changing_relationship = input(
                            'Do you want to change the relationship? (y/n)').strip().lower()

                        if changing_relationship in ('y', 'yes'):
                            transaction['relationship'] = get_relationship()
                            break

                        elif changing_relationship in ('n', 'no'):
                            break

                        else:
                            print('Please enter y/yes or n/no.')

                transaction['person'] = new_person

            elif edit == 6:
                transaction['relationship'] = get_relationship()
            elif edit == 7:
                transaction['description'] = get_description()
            elif edit == 8:
                print('Editing cancelled!')
                return

            save_transactions()
            print('Transaction updated successfully!')
        except TransactionCancelled:
            print('Editing cancelled.')
            return


def view_balance():
    total_income = 0
    total_expense = 0

    for transaction in transactions:
        if transaction['type'] == 'income':
            total_income += transaction['amount']
        elif transaction['type'] == 'expense':
            total_expense += transaction['amount']
    balance = total_income - total_expense

    print('Total income: ', f"${total_income:,.2f}")
    print('Total expenses: ', f"${total_expense:,.2f}")
    print('Balance: ', f"${balance:,.2f}")


def show_menu():
    print('''
    =====================
      FINANCIAL TRACKER
    =====================
    1. Add transaction
    2. View transactions
    3. View balance
    4. View person history
    5. View person balance
    6. Delete transaction
    7. Edit transaction
    8. Exit
''')


def get_transaction_date():
    while True:
        user_date = input(
            "Enter the date(YYYY-MM-DD) or press Enter for today's date: ").strip()

        check_for_cancel(user_date)

        # if not user_date:
        if user_date == '':
            return str(date.today())

        try:
            user_date = date.fromisoformat(user_date)
            return str(user_date)
        except ValueError:
            print('Please enter a valid date.')


def view_person_history():
    if not transactions:
        print('No transaction yet! Please add a transaction first.')
        return

    while True:
        person_name = input("Enter the person's name: ").strip()

        check_for_cancel(person_name)

        if person_name:
            break

        print("Please enter a person's name.")

    view_transactions(person=person_name)


def view_person_balance():
    if not transactions:
        print('No transaction yet! Please add a transaction first.')
        return

    while True:
        person_name = input("Enter the person's name: ").strip()

        check_for_cancel(person_name)

        if person_name:
            break

        print("Please enter a person's name.")

    print('PERSON BALANCE')
    print('-' * 22)

    total = 0
    found_person = False

    for transaction in transactions:
        if transaction['person'].strip().lower() == person_name.strip().lower():
            found_person = True
            if transaction['relationship'] == 'lent':
                total += transaction['amount']
            elif transaction['relationship'] == 'borrowed':
                total -= transaction['amount']
    if not found_person:
        print("No transaction found for this person.")
        return
    if total > 0:
        print('Person:', person_name)
        print('Status: Creditor')
        print('Balance:', f'+${total:,.2f}')
    elif total < 0:
        print('Person:', person_name)
        print('Status: Debtor')
        print('Balance:', f'-${abs(total):,.2f}')
    else:
        print('Person:', person_name)
        print('Status: Settled')
        print('Balance: $0.00')


load_transactions()

continue_tracking = True
while continue_tracking:
    show_menu()
    try:
        option = int(input('Choose an option: ').strip())
        if option == 1:
            add_transaction()
        elif option == 2:
            view_transactions()
        elif option == 3:
            view_balance()
        elif option == 4:
            try:
                view_person_history()
            except TransactionCancelled:
                print('Viewing person history cancelled.')

        elif option == 5:
            try:
                view_person_balance()
            except TransactionCancelled:
                print('Viewing person balance cancelled.')

        elif option == 6:
            delete_transaction()
        elif option == 7:
            edit_transaction()
        elif option == 8:
            continue_tracking = False
        else:
            print('Please enter a number from 1 to 8.')
    except ValueError:
        print('Please enter a number! (1, 2, 3, 4, 5, 6, 7, or 8.)')

save_transactions()
