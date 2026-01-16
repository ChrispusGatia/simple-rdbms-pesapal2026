# Pesapal Junior Developer Challenge 2026 - SimpleDB

> **🎯 Challenge Submission by Chris Mwangi**  
> Submitted: January 2026  
> Repository: [GitHub Link - Add your URL here after pushing]

A lightweight in-memory relational database system with a SQL-like interface and web-based CRUD interface.

---

## 📋 Challenge Requirements Checklist

- ✅ **Simple RDBMS** - In-memory relational database
- ✅ **Table Declarations** - Support for INT, TEXT, FLOAT types
- ✅ **CRUD Operations** - Full Create, Read, Update, Delete support
- ✅ **Basic Indexing** - Hash-based primary key indexes
- ✅ **Primary Keys** - Enforced with constraint validation
- ✅ **Unique Keys** - Column-level unique constraints
- ✅ **Joining** - INNER JOIN on equality conditions
- ✅ **SQL-like Interface** - Full SQL parser
- ✅ **Interactive REPL** - Command-line query interface
- ✅ **Web Application** - Flask-based CRUD demo with table creation

---

## Features

- **In-Memory Storage**: Fast data access using Python dictionaries and lists
- **SQL-Like Interface**: Support for common SQL operations
  - `CREATE TABLE` with column definitions
  - `INSERT` for adding records
  - `SELECT *` for retrieving all records
  - `SELECT WHERE` for filtered queries
  - `SELECT JOIN` for combining tables (INNER JOIN)
  - `UPDATE` for modifying records
  - `DELETE` for removing records
- **Primary Key Management**: Automatic primary key enforcement and indexing
- **Unique Constraints**: Column-level unique constraint validation
- **Hash Indexing**: Fast lookups using hash-based indexes on primary keys
- **REPL Interface**: Interactive command-line interface for running queries
- **Web Interface**: Flask-based web app for easy CRUD operations
- **Type Safety**: Basic data type validation

## Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Setup

1. Clone or download this repository:
```bash
cd pesapal-jdev26-chris
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### REPL Interface

Run the interactive command-line interface:

```bash
python repl.py
```

Example queries:
```sql
CREATE TABLE users (id INT PRIMARY KEY, name TEXT, email TEXT UNIQUE, age INT)
INSERT INTO users VALUES (1, 'John Doe', 'john@example.com', 30)
INSERT INTO users VALUES (2, 'Jane Smith', 'jane@example.com', 25)
SELECT * FROM users
SELECT * FROM users WHERE id = 1
UPDATE users SET age = 31 WHERE id = 1
DELETE FROM users WHERE id = 2

-- JOIN example
CREATE TABLE orders (id INT PRIMARY KEY, user_id INT, product TEXT)
INSERT INTO orders VALUES (101, 1, 'Laptop')
SELECT * FROM users JOIN orders ON users.id = orders.user_id
```

Type `exit` or `quit` to exit the REPL.

### Web Application

Start the Flask web server:

```bash
python -m web_app.app
```

Then open your browser to: `http://localhost:5000`

The web interface allows you to:
- View all tables in the database
- Browse records in each table
- Create new records via web forms
- Edit existing records
- Delete records

## Project Structure

```
pesapal-jdev26-chris/
├── README.md
├── requirements.txt
├── .gitignore
├── repl.py                  # Interactive REPL interface
├── src/
│   ├── __init__.py
│   ├── database.py          # Main SimpleDB class
│   ├── table.py             # Table class with row storage and indexing
│   ├── parser.py            # SQL-like query parser
│   └── types.py             # Data type validation helpers
├── web_app/
│   ├── __init__.py
│   ├── app.py               # Flask application
│   ├── templates/           # HTML templates
│   └── static/              # CSS and static files
└── tests/
    └── test_database.py     # Unit tests
```

## Running Tests

Execute the test suite:

```bash
python -m pytest tests/
```

Or run directly:

```bash
python -m unittest tests.test_database
```

Expected output: **20 tests passing** ✅

## Demo Walkthrough

### REPL Demo
```bash
python repl.py
```

Try these commands to see all features:
```sql
-- Create tables
CREATE TABLE customers (id INT PRIMARY KEY, name TEXT, email TEXT UNIQUE)
CREATE TABLE orders (id INT PRIMARY KEY, customer_id INT, product TEXT, amount FLOAT)

-- Insert data
INSERT INTO customers VALUES (1, 'Alice Brown', 'alice@email.com')
INSERT INTO customers VALUES (2, 'Bob Wilson', 'bob@email.com')
INSERT INTO orders VALUES (100, 1, 'Laptop', 1299.99)
INSERT INTO orders VALUES (101, 1, 'Mouse', 29.99)
INSERT INTO orders VALUES (102, 2, 'Keyboard', 89.99)

-- Query data
SELECT * FROM customers
SELECT * FROM orders WHERE customer_id = 1

-- JOIN tables
SELECT * FROM customers JOIN orders ON customers.id = orders.customer_id

-- Update and delete
UPDATE orders SET amount = 1199.99 WHERE id = 100
DELETE FROM orders WHERE id = 102
```

### Web App Demo
```bash
python -m web_app.app
```
Navigate to `http://localhost:5000` and:
1. View the 3 pre-populated tables (users, products, orders)
2. Click "Create New Table" to add a custom table
3. Browse, create, edit, and delete records via the web UI
4. See JOIN relationships in the sample data

## Known Limitations

- **In-Memory Only**: Data is lost when the program exits (no persistence)
- **Simple Parser**: Limited SQL syntax support (no subqueries, complex expressions)
- **INNER JOIN Only**: Only supports INNER JOIN on single column equality
- **No Transactions**: No ACID guarantees or rollback support
- **Single-Threaded**: Not designed for concurrent access
- **Limited Data Types**: Basic support for INT, TEXT, and FLOAT only
- **No NULL Support**: All columns are required (NOT NULL by default)
- **Simple Indexing**: Only hash indexes on primary keys

## Future Enhancements

- Add optional SQLite persistence
- Support for more SQL operations (LEFT/RIGHT JOIN, GROUP BY, ORDER BY, LIMIT)
- Support for subqueries and complex WHERE conditions
- Implement B-tree indexes for range queries
- Add transaction support
- Multi-threaded access with proper locking
- More comprehensive data type system
- NULL value support

## Credits

**Author**: Chris Mwangi  
**Challenge**: Pesapal Junior Developer Challenge 2026  
**Submission Date**: January 17, 2026

### AI Assistance Disclosure

This project was developed with the assistance of AI tools (GitHub Copilot, Claude) for:
- Initial project structure and scaffolding
- Code review and optimization suggestions
- Documentation formatting
- Test case generation
- Debugging assistance

All core logic, design decisions, and implementation approaches were directed by the developer. AI tools were used as productivity enhancers, similar to how one would use Stack Overflow, documentation, or a senior developer's guidance.

### Technologies Used

- **Python 3.13** - Core language
- **Flask 3.0.0** - Web framework
- **Regular Expressions** - SQL parser implementation
- **Hash Tables** - Primary key indexing
- **Tabulate** - REPL output formatting

## License

This project is created for educational purposes as part of the Pesapal Junior Developer Challenge 2026.

---

## 📧 Contact

For questions about this submission:  
**Email**: [Your email here]  
**GitHub**: [Your GitHub profile]

**Thank you for reviewing my submission! 🚀**
