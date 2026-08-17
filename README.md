# Financial Tracker

A beginner-to-intermediate Python command-line financial tracker built from scratch.

This project started as a simple transaction tracker and gradually grew into a more structured application for managing income, expenses, personal transactions, lending, borrowing, and balances.

The goal wasn't just to make the program work. Throughout development, I focused on understanding **why** the code works, improving the user experience, validating input, and designing the data model around real-world financial situations.

> **Current version: v1.0 — In-memory financial tracker**

---

## Features

### Transaction Management

- Add income and expense transactions
- Enter transaction amounts with validation
- Support decimal amounts and large values
- Add categories
- Add descriptions
- Assign dates manually or use today's date
- Optionally associate transactions with a person
- Display transactions in a formatted terminal table

<img width="1488" height="499" alt="Screenshot 2026-08-17 225514" src="https://github.com/user-attachments/assets/ca4604e4-b36a-4af7-8e29-4465dc046c8c" />

### Person Tracking

Transactions can optionally be associated with a person.

For example:

- Dad
- Brother
- Friend
- Roommate

The tracker can then:

- View all transactions involving a specific person
- Calculate the balance associated with that person
- Determine whether I am the **creditor** or **debtor**
- Detect when the balance is **settled**

### Lending & Borrowing

When a person is attached to a transaction, the user can specify:

1. Normal transaction
2. I lent money
3. I borrowed money

The application uses these relationships to calculate person-specific balances.

For example:

```text
I lend Dad $500
→ Dad owes me $500
→ Creditor: +$500.00

Dad pays me back $200
→ Balance becomes +$300.00

Dad pays the remaining $300
→ Balance becomes $0.00
→ Settled
```

<img width="791" height="839" alt="Screenshot 2026-08-17 203814" src="https://github.com/user-attachments/assets/a1283a60-0c2b-4704-85af-bd0ca8d9ff79" />

The sign of the person balance represents the financial relationship from my perspective:

```text
+ amount → I am the creditor
- amount → I am the debtor
$0.00    → Settled
```

---

## Input Validation

The program validates several types of user input instead of assuming everything entered is correct.

Examples include:

- Invalid transaction types
- Invalid numeric amounts
- Zero or negative amounts
- Invalid dates
- Invalid menu choices
- Invalid relationship choices
- Empty person names when a person-specific feature is selected

The program uses loops to let the user correct invalid input instead of terminating.

---

## Terminal Interface

Transactions are displayed in a structured table with aligned columns:

```text
___________________________________________________________________________________________________________________________________________________
#    |     DATE     |    TYPE    |        AMOUNT        |       CATEGORY       |        PERSON        |     RELATIONSHIP     |    DESCRIPTION
___________________________________________________________________________________________________________________________________________________
1.   | 2026-08-17   |   INCOME   |             +$500.00 |        allowance     |          dad         |       borrowed      | ...
```

Python's formatted string syntax is used extensively for:

- left alignment
- centered headers
- right-aligned monetary values
- fixed-width columns
- thousands separators
- two decimal places
- positive/negative display signs

One interesting formatting lesson from the project was learning how datetime.date objects behave when displayed and formatted in f-strings, which led me to explicitly convert dates to strings for consistent terminal output.

---

## Main Menu

```text
=====================
  FINANCIAL TRACKER
=====================
1. Add transaction
2. View transaction
3. View balance
4. View person history
5. View person balance
6. Exit
```

---

## Project Structure

The current version is intentionally kept as a single Python file while the application is still being developed.

The program is divided into functions with specific responsibilities, including:

```text
get_transaction_type()
get_amount()
get_relationship()
get_transaction_date()

add_transaction()

view_transactions()
view_balance()
view_person_history()
view_person_balance()

show_menu()
```

The project began with simpler logic and gradually evolved into smaller functions as new responsibilities appeared.

---

## Data Model

Each transaction is currently represented as a Python dictionary:

```python
transaction = {
    'type': transaction_type,
    'amount': amount,
    'category': category,
    'person': person,
    'relationship': relationship,
    'description': description,
    'date': transaction_date
}
```

All transactions are stored in a list:

```python
transactions = []
```

This structure makes it possible to filter and calculate information across transactions.

For example, person history can search for transactions where:

```python
transaction['person'] == person_name
```

and person balance can use:

```python
transaction['relationship']
```

to determine whether money should increase or decrease the person's balance.

---

## What I Learned

This project taught me considerably more than simply writing a collection of Python statements.

### Python fundamentals

- Variables and data types
- Lists
- Dictionaries
- Functions
- Parameters and arguments
- Return values
- Conditional statements
- `for` loops
- `while` loops
- `break`
- `continue`
- `try` / `except`
- Boolean flags
- String methods
- F-strings
- String alignment and formatting
- The `datetime.date` type
- `date.fromisoformat()`

### Control Flow

One of the most useful patterns I learned was:

```python
while True:
    value = input(...)

    if value_is_valid:
        break

    print("Invalid input.")
```

I learned that an `else` block is not always necessary after an `if`. If the valid condition uses `break`, the loop exits immediately; otherwise Python naturally continues to the next statement.

This made my input-validation logic considerably cleaner.

### Function Design

I learned to separate responsibilities between functions.

For example:

```text
view_person_history()
        ↓
asks for and validates a person
        ↓
view_transactions(person=name)
        ↓
filters and displays matching transactions
```

Instead of making one function responsible for everything, the functions cooperate with each other.

This also introduced me to the idea of **DRY (Don't Repeat Yourself)** and helped me recognize when code should be reused rather than duplicated.

### Default Parameters

I learned how a function such as:

```python
def view_transactions(person=None):
```

can provide two behaviors:

```python
view_transactions()
```

→ display all transactions

and:

```python
view_transactions(person="dad")
```

→ display only Dad's transactions.

Understanding why the function still needs an explicit condition such as:

```python
if person is None or person == transaction['person']:
```

was an important lesson in how function parameters actually work.

### Data Modeling

One of the biggest lessons was realizing that a transaction's **type** and its **relationship to another person** are different concepts.

For example:

```text
type         → income / expense
relationship → normal / lent / borrowed
```

Separating these concepts made person-specific balance calculations possible.

It also exposed real-world design questions, such as how a loan repayment should be represented. Those questions helped me think about the meaning of data rather than only the syntax used to store it.

---

## Design Decisions

The project was influenced by a real-world family financial tracking system.

A particularly useful idea was tracking transactions with people rather than maintaining a completely separate "loan" system.

This allows the application to show the complete history of transactions involving a person, while also calculating the current amount owed.

The result is closer to a personal ledger than a simple income/expense calculator.

---

## Current Limitations

This is intentionally **v1.0**, so there are several things that are not implemented yet.

### No persistent storage

Transactions currently exist only while the program is running:

```python
transactions = []
```

Closing the application clears the data.

### No database

The current version uses Python lists and dictionaries instead of a database.

### No editing or deleting transactions

Once a transaction is added, it cannot currently be modified or removed.

### No advanced filtering

There is currently no filtering by:

- date range
- category
- transaction type
- amount
- multiple people

### No automated tests

The current version has been tested manually through the command-line interface.

These limitations are intentional opportunities for future versions.


### Learning to Refactor

One of the biggest things I noticed while building this project was that some functions were becoming too busy. Even when the code worked, I started recognizing that a function shouldn't have to handle every little responsibility itself. I learned to move separate pieces of logic into their own functions and let functions work together instead of making one function do everything. For example, I separated input and validation into functions like `get_amount()`, `get_transaction_date()`, and `get_relationship()`, while `view_person_history()` simply collects the person's name and passes it to `view_transactions()`. This taught me that clean code isn't just about making something work—it's also about making the code easier to understand, maintain, and improve.

<img width="1811" height="714" alt="Screenshot 2026-08-17 233800" src="https://github.com/user-attachments/assets/5d9ce5f3-7144-42c4-a02a-d6b6aee785cd" />

---

## Planned Improvements

Possible future development includes:

### v2.0 — Persistent Storage

Learn and implement JSON storage so transactions survive between program sessions.

```text
Python data
    ↓
JSON file
    ↓
Program closes
    ↓
Program starts
    ↓
JSON file
    ↓
Python data
```

### Future improvements

- Refactor repeated formatting logic
- Separate the application into multiple modules
- Add transaction editing
- Add transaction deletion
- Add search and filtering
- Add category summaries
- Add date-based reports
- Add automated tests
- Improve terminal UI
- Add CSV export
- Eventually explore SQLite for database-backed storage

---

## Why I Built This

I wanted to build something practical rather than another isolated syntax exercise.

Financial tracking gave me an opportunity to combine many Python concepts into one program while also encountering problems that don't have a single obvious answer.

Some of the most valuable parts of the project were the moments where the code technically worked but the **design didn't quite make sense yet**.

For example:

- How should lending and borrowing affect a balance?
- Should a person's history display every transaction or only loans?
- Where should input validation happen?
- Should a function ask for input or receive it as an argument?
- When should a function return versus continue looping?
- How should positive and negative balances communicate creditor/debtor status?
- Which information belongs in the transaction itself and which should be calculated later?

Working through those questions helped me move from thinking about individual lines of code toward thinking about **program structure and data design**.

---

## Development Philosophy

This project was developed incrementally.

Instead of trying to design the entire application before writing code, I built a working feature, tested it, encountered a problem, investigated the behavior, and then improved the design.

That process led to several important discoveries about:

- control flow
- function responsibilities
- reusable functions
- validation
- formatting
- data modeling
- user experience
- edge cases

The code is therefore not presented as a claim of perfect architecture. It represents a genuine learning progression toward more structured Python programming.

---

## Tech Stack

- **Python 3**
- Python standard library
- `datetime`
- Command-line interface
- No external dependencies

---

## How to Run

Clone the repository or download the Python file.

Run:

```bash
python financial_tracker.py
```

Follow the numbered menu options to add and inspect transactions.

---

## Project Status

**v1.0 — Working**

The core financial tracking functionality is implemented and manually tested.

The next major milestone is persistent storage using JSON.

---

Built from scratch as a Python learning project.

This project is part of my progression from beginner Python programming toward intermediate software development, with an emphasis on understanding the reasoning behind the code rather than simply making the program run.
