from datetime import date
transactions = []


def get_transaction_type():
    while True:
        transaction_type = (input('Transaction Type: ')).lower()
        if transaction_type not in ('income', 'i', 'expense', 'e'):
            print('please enter "income/i" or "expense/e".')
        else:
            if transaction_type in ('i', 'income'):
                return 'income'
            elif transaction_type in ('e', 'expense'):
                return 'expense'


def get_amount():
    valid = False
    while not valid:
        try:
            amount = float(input('Amount: '))
            if amount > 0:
                valid = True
                return amount
            else:
                print('Amount must be greater than zero! ')
        except ValueError:
            print('Please enter a valid number!')


def add_transaction():

    transaction_type = get_transaction_type()
    amount = get_amount()
    category = (input('Category: '))
    transaction_date = get_transaction_date()
    person = input('Person (press Enter if there is none): ').lower()

    if person:
        relationship = get_relationship()
    else:
        relationship = 'normal'
    description = input('Description (press Enter if there is none): ')

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
    print('Transaction added successfully!')


def get_relationship():
    while True:
        try:
            relationship = int(input('''Please choose the relationship:
1. Normal transaction
2. I lent money
3. I borrowed money
Choose an option: '''))
        except ValueError:
            print('Please enter 1, 2, or 3.')
            continue
        if relationship == 1:
            return 'normal'
        elif relationship == 2:
            return 'lent'
        elif relationship == 3:
            return 'borrowed'


def view_transactions(person=None):
    if not transactions:
        print('No transactions yet.')
    else:
        number = '#'
        date_header = 'DATE'
        type_header = 'TYPE'
        amount_header = 'AMOUNT'
        category_header = 'CATEGORY'
        person_header = 'PERSON'
        relationship_header = 'RELATIONSHIP'
        description_header = 'DESCRIPTION'
        print('_' * 147)
        print(
            f"{number:<4} | {date_header:^12} | {type_header:^10} | {amount_header:^20} | {category_header:^20} | {person_header:^20} | {relationship_header:^20} | {description_header:^20}")
        print('_' * 147)
        found_match = False
        for number, transaction in enumerate(transactions, start=1):
            if transaction['type'] == 'income':
                display_amount = f'+${transaction['amount']:,.2f}'
            elif transaction['type'] == 'expense':
                display_amount = f'-${transaction['amount']:,.2f}'
            if person is None or person == transaction['person']:
                found_match = True
                print(
                    f"{str(number) + '.':<4} | {str(transaction['date']):^12} | {transaction['type'].upper():^10} | {display_amount:>20} | {transaction['category']:^20} | {transaction['person']:^20} | {transaction['relationship']:^20} |{transaction['description']:^20}")
        if not found_match:
            print('No transaction found for this person.')


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
    2. View transaction
    3. View balance
    4. View person history
    5. View person balance
    6. Exit
''')


def get_transaction_date():
    while True:
        user_date = input(
            "Enter the date(YYYY-MM-DD) or press Enter for today's date: ")
        # if not user_date:
        if user_date == '':
            return date.today()
        try:
            user_date = date.fromisoformat(user_date)
            return user_date
        except ValueError:
            print('Please enter a valid date.')


def view_person_history():
    if not transactions:
        print('No transaction yet! Please add a transaction first.')
        return
    while True:
        person_name = input("Enter the person's name: ").lower()

        if person_name:
            break

        print("Please enter a person's name.")

    view_transactions(person=person_name)


def view_person_balance():
    if not transactions:
        print('No transaction yet! Please add a transaction first.')
        return

    while True:
        person_name = input("Enter the person's name: ").lower()

        if person_name:
            break

        print("Please enter a person's name.")

    print('PERSON BALANCE')
    print('-' * 22)
    total = 0
    found_person = False
    for transaction in transactions:
        if transaction['person'] == person_name:
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


continue_tracking = True
while continue_tracking:
    show_menu()
    try:
        option = int((input('Choose an option: ')))
        if option == 1:
            add_transaction()
        elif option == 2:
            view_transactions()
        elif option == 3:
            view_balance()
        elif option == 4:
            view_person_history()
        elif option == 5:
            view_person_balance()
        elif option == 6:
            continue_tracking = False
        else:
            print('Please enter a number from 1 to 6.')
    except ValueError:
        print('Please enter a number! (1, 2, 3, 4, 5, or 6.)')
