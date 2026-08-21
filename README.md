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

### Person Tracking

Transactions can optionally be associated with a person.

For example:

- Dad
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

The sign of the person balance represents the financial relationship from my perspective:

```text
+ amount → I am the creditor
- amount → I am the debtor
$0.00    → Settled
```

<img width="791" height="839" alt="view-person-balance-refactored" src="https://github.com/user-attachments/assets/0a82a0d5-82ce-4049-8773-8403253b8e20" />

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

One interesting formatting lesson from the project was discovering that `datetime.date` objects behave differently from strings when formatting them, which led me to explicitly convert dates to strings for terminal formatting.

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


__________________________________________________________________________________________________________________________________________________________________

# Financial Tracker V2

A beginner-to-intermediate Python command-line financial tracker built from scratch.

This project started as a simple transaction tracker and gradually grew into a more structured application for managing income, expenses, personal transactions, lending, borrowing, and balances.

V2 builds directly on the limitations of the first version. The biggest change is persistent storage, but I also expanded the application with transaction editing, deletion, stronger input validation, custom exception handling, and more complete transaction management.

The goal is still the same: not just making the program work, but understanding why it works, how the data should be structured, and how the program should respond to different user situations.

> **Current version: v2.0 — JSON-backed financial tracker**

---

## Features

### Transaction Management

* Add income and expense transactions
* Enter and validate transaction amounts
* Support decimal amounts and large values
* Add categories and descriptions
* Assign dates manually or use today's date
* Optionally associate transactions with a person
* View transactions in a formatted terminal table
* Edit existing transactions
* Delete transactions with confirmation
* Cancel an operation at any point where cancellation is supported

<img width="1363" height="626" alt="Transaction-Deletion" src="https://github.com/user-attachments/assets/8b0848e5-4bd1-4cc3-91fb-951f99fc8d3e" />


### Persistent Storage

Unlike V1, transactions are no longer lost when the program closes.

V2 stores transaction data in:

```text
transactions.json
```

The program loads existing transactions when it starts and saves changes when transactions are added, edited, or deleted.

It also handles a missing file and detects corrupted JSON data instead of immediately terminating.

The current data is still represented using Python lists and dictionaries. JSON is being used as the storage layer rather than a database.

---

## Person Tracking

Transactions can optionally be associated with a person.

For example:

```text
Dad
Brother
Friend
Roommate
```

The tracker can then:

* View transactions involving a specific person
* Calculate the balance associated with that person
* Determine whether I am the creditor or debtor
* Detect when the balance is settled

The person balance is calculated from the relationship attached to each transaction.

---

## Lending & Borrowing

When a person is attached to a transaction, the user can specify:

```text
1. Normal transaction
2. I lent money
3. I borrowed money
```

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

The sign of the person balance represents the financial relationship from my perspective:

```text
+ amount → I am the creditor
- amount → I am the debtor
$0.00    → Settled
```

This was one of the main design ideas carried forward from V1. Rather than creating a completely separate loan system, lending and borrowing are represented as relationships attached to normal transactions.

This allows the application to keep a person's transaction history while also calculating the current balance.

---

## Input Validation

The program validates several types of user input instead of assuming everything entered is correct.

Examples include:

* Invalid transaction types
* Invalid numeric amounts
* Zero or negative amounts
* Invalid dates
* Invalid menu choices
* Invalid transaction numbers
* Invalid relationship choices
* Invalid edit choices

The program uses loops to allow the user to correct invalid input instead of terminating.

V2 also introduces a custom `TransactionCancelled` exception, which provides a consistent way to exit operations such as adding, editing, or deleting a transaction.

---

## Financial Calculations

The tracker can calculate:

```text
Total income
Total expenses
Balance
```

Income and expenses are calculated from the stored transactions, with the current balance being the difference between the two.

---

## Main Menu

```text
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
```

The menu expanded from V1 as new responsibilities were added to the application.

---

## Data Model

Each transaction is represented as a Python dictionary:

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

All transactions are stored in a list before being serialized to JSON.

One of the important design decisions in the project is keeping the transaction's **type** separate from its **relationship**:

```text
type
→ income / expense

relationship
→ normal / lent / borrowed
```

This separation makes it possible to calculate normal financial balances and person-specific balances using different pieces of information.

It also reflects one of the main lessons from V1: data modeling becomes more important as the application starts representing real-world situations.

---

## V1 → V2

V2 was built around the limitations of the first version.

### V1

The first version focused on:

* Building the core transaction system
* Working with lists and dictionaries
* Input validation
* Person tracking
* Lending and borrowing logic
* Terminal formatting
* Function design and program structure

However, the data only existed while the program was running. There was also no way to edit or delete an existing transaction.

### V2

V2 adds:

* Persistent JSON storage
* Loading saved transactions
* Saving changes to disk
* Editing transactions
* Deleting transactions
* Deletion confirmation
* Custom exception handling
* More complete cancellation flows
* Improved transaction management

The main progression wasn't just adding more features.

It was moving from a program that could **record data** toward one that can **manage data throughout its lifecycle**.

---

## What I Learned

This project has taught me more than simply writing Python syntax.

Some of the main areas I have worked with include:

* Lists and dictionaries
* Functions and parameters
* Return values
* Conditional statements
* `for` and `while` loops
* `try` / `except`
* Custom exceptions
* File handling
* JSON serialization
* Date handling
* Input validation
* CRUD operations
* Data persistence
* Data modeling
* String formatting
* Basic application state

One of the most useful lessons has been learning to separate responsibilities between functions.

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

Instead of making one function responsible for everything, different functions handle different parts of the process.

Another important lesson has been that a program can work technically while still having design problems. Adding new features often raises questions that cannot be solved by syntax alone:

* Where should validation happen?
* What information belongs in the transaction?
* What should be calculated instead of stored?
* What should happen when the user cancels?
* How should lending and borrowing affect a balance?
* What should happen when existing data is edited or deleted?

Those questions have been a major part of my progression from learning individual Python concepts toward thinking more about application design.

<img width="601" height="611" alt="class-TransactionCancellation" src="https://github.com/user-attachments/assets/7acac47b-eb04-4e2f-98db-ae2280b4391b" />

---

## Current Limitations

V2 is still a learning project, so there are several areas that I want to improve.

### Single Python File

The application is still contained in one Python file.

As the project grows, separating responsibilities into multiple modules should make the code easier to maintain.

### JSON Instead of a Database

JSON works well for the current size of the project, but it is not intended to be the final storage solution.

SQLite would be a next step.

### No Automated Tests

The application has primarily been tested manually through the command-line interface.

Adding unit tests would make it easier to verify calculations and edge cases as the project becomes more complex.

### Limited Reporting

The current version provides overall balances and person-specific balances, but does not yet include more advanced reporting such as:

* Category summaries
* Monthly spending
* Date-range filtering
* Spending trends
* Financial reports

These are possible directions for future versions.

---

## Future Improvements

Some of the improvements I would like to explore are:

* Refactor the application into multiple modules
* Introduce a dedicated transaction model
* Add automated tests
* Add transaction search and filtering
* Add category summaries
* Add monthly and yearly reports
* Add CSV import/export
* Move from JSON to SQLite
* Improve the terminal interface
* Eventually explore a graphical or web interface

---

## Development Approach

The project has been developed incrementally.

I did not try to design the entire application before writing it. Instead, I built a feature, tested it, encountered a problem, investigated the behavior, and then changed the design where necessary.

That process has led to most of the improvements between V1 and V2.

The project is therefore not meant to represent perfect architecture or production-ready software. It represents a practical learning progression where each version introduces a new problem to solve.

---

## Tech Stack

* **Python 3**
* Python standard library
* `json`
* `datetime`
* Command-line interface
* JSON file storage
* No external dependencies

---

## How to Run

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
```

Navigate to the project:

```bash
cd YOUR-REPOSITORY
```

Run the application:

```bash
python financial_tracker.py
```

The application will create or use `transactions.json` for persistent transaction storage.

---

## Project Status

**Version:** v2.0
**Status:** Working
**Type:** Personal learning project
**Language:** Python
**Storage:** JSON
**Interface:** Command line

V2 is another step in my progression from learning Python fundamentals toward building more structured applications.

The next version will focus less on simply adding features and more on improving architecture, testing, maintainability, and scalability.

---

Built from scratch as a Python learning project.

The purpose of this project is not to present a finished financial application, but to document my progression as I learn how to turn Python fundamentals into increasingly structured and practical software.

