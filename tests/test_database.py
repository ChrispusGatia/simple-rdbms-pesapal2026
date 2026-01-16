"""
Unit tests for SimpleDB.

This module contains test cases for the database, table, and parser modules.
"""

import unittest
from src.database import SimpleDB
from src.table import Table
from src.parser import QueryParser


class TestSimpleDB(unittest.TestCase):
    """Test cases for SimpleDB class."""
    
    def setUp(self):
        """Set up test database before each test."""
        self.db = SimpleDB()
    
    def test_create_table(self):
        """Test table creation."""
        result = self.db.create_table(
            'users',
            [('id', 'INT'), ('name', 'TEXT'), ('email', 'TEXT')],
            'id',
            ['email']
        )
        
        self.assertTrue(result['success'])
        self.assertIn('users', self.db.tables)
        self.assertEqual(self.db.get_table('users').name, 'users')
    
    def test_create_duplicate_table(self):
        """Test that creating duplicate table fails."""
        self.db.create_table('users', [('id', 'INT')], 'id', [])
        result = self.db.create_table('users', [('id', 'INT')], 'id', [])
        
        self.assertFalse(result['success'])
        self.assertIn('already exists', result['message'])
    
    def test_create_table_invalid_primary_key(self):
        """Test that creating table with invalid primary key fails."""
        result = self.db.create_table(
            'users',
            [('id', 'INT'), ('name', 'TEXT')],
            'nonexistent_column',
            []
        )
        
        self.assertFalse(result['success'])
        self.assertIn('not found', result['message'])


class TestTable(unittest.TestCase):
    """Test cases for Table class."""
    
    def setUp(self):
        """Set up test table before each test."""
        self.table = Table(
            'users',
            [('id', 'INT'), ('name', 'TEXT'), ('email', 'TEXT'), ('age', 'INT')],
            'id',
            ['email']
        )
    
    def test_insert_valid_row(self):
        """Test inserting a valid row."""
        result = self.table.insert([1, 'John Doe', 'john@example.com', 30])
        
        self.assertTrue(result['success'])
        self.assertEqual(len(self.table.rows), 1)
        self.assertIn(1, self.table.primary_index)
    
    def test_insert_wrong_column_count(self):
        """Test that inserting wrong number of values fails."""
        result = self.table.insert([1, 'John Doe'])  # Missing columns
        
        self.assertFalse(result['success'])
        self.assertIn('Expected', result['message'])
    
    def test_insert_duplicate_primary_key(self):
        """Test that duplicate primary key insertion fails."""
        self.table.insert([1, 'John Doe', 'john@example.com', 30])
        result = self.table.insert([1, 'Jane Doe', 'jane@example.com', 25])
        
        self.assertFalse(result['success'])
        self.assertIn('Primary key violation', result['message'])
    
    def test_insert_duplicate_unique_column(self):
        """Test that duplicate unique column insertion fails."""
        self.table.insert([1, 'John Doe', 'john@example.com', 30])
        result = self.table.insert([2, 'Jane Doe', 'john@example.com', 25])
        
        self.assertFalse(result['success'])
        self.assertIn('Unique constraint violation', result['message'])
    
    def test_select_all(self):
        """Test selecting all rows."""
        self.table.insert([1, 'John Doe', 'john@example.com', 30])
        self.table.insert([2, 'Jane Smith', 'jane@example.com', 25])
        
        result = self.table.select()
        
        self.assertTrue(result['success'])
        self.assertEqual(len(result['data']), 2)
        self.assertEqual(result['columns'], ['id', 'name', 'email', 'age'])
    
    def test_select_with_where(self):
        """Test selecting with WHERE clause."""
        self.table.insert([1, 'John Doe', 'john@example.com', 30])
        self.table.insert([2, 'Jane Smith', 'jane@example.com', 25])
        
        result = self.table.select(where={'column': 'id', 'value': 1})
        
        self.assertTrue(result['success'])
        self.assertEqual(len(result['data']), 1)
        self.assertEqual(result['data'][0][0], 1)  # First column (id) should be 1
    
    def test_update_row(self):
        """Test updating a row."""
        self.table.insert([1, 'John Doe', 'john@example.com', 30])
        
        result = self.table.update(
            set_values={'age': 31, 'name': 'John Updated'},
            where={'column': 'id', 'value': 1}
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(self.table.rows[0]['age'], 31)
        self.assertEqual(self.table.rows[0]['name'], 'John Updated')
    
    def test_delete_row(self):
        """Test deleting a row."""
        self.table.insert([1, 'John Doe', 'john@example.com', 30])
        self.table.insert([2, 'Jane Smith', 'jane@example.com', 25])
        
        result = self.table.delete(where={'column': 'id', 'value': 1})
        
        self.assertTrue(result['success'])
        self.assertEqual(len(self.table.rows), 1)
        self.assertNotIn(1, self.table.primary_index)
        self.assertEqual(self.table.rows[0]['id'], 2)


class TestQueryParser(unittest.TestCase):
    """Test cases for QueryParser class."""
    
    def setUp(self):
        """Set up parser before each test."""
        self.parser = QueryParser()
    
    def test_parse_create_table(self):
        """Test parsing CREATE TABLE query."""
        query = "CREATE TABLE users (id INT PRIMARY KEY, name TEXT, email TEXT UNIQUE)"
        result = self.parser.parse(query)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['type'], 'CREATE_TABLE')
        self.assertEqual(result['table_name'], 'users')
        self.assertEqual(result['primary_key'], 'id')
        self.assertIn('email', result['unique_columns'])
    
    def test_parse_insert(self):
        """Test parsing INSERT query."""
        query = "INSERT INTO users VALUES (1, 'John Doe', 'john@example.com')"
        result = self.parser.parse(query)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['type'], 'INSERT')
        self.assertEqual(result['table_name'], 'users')
        self.assertEqual(result['values'], [1, 'John Doe', 'john@example.com'])
    
    def test_parse_select_all(self):
        """Test parsing SELECT * query."""
        query = "SELECT * FROM users"
        result = self.parser.parse(query)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['type'], 'SELECT')
        self.assertEqual(result['table_name'], 'users')
        self.assertEqual(result['columns'], ['*'])
    
    def test_parse_select_with_where(self):
        """Test parsing SELECT with WHERE clause."""
        query = "SELECT * FROM users WHERE id = 1"
        result = self.parser.parse(query)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['type'], 'SELECT')
        self.assertEqual(result['where']['column'], 'id')
        self.assertEqual(result['where']['value'], 1)
    
    def test_parse_update(self):
        """Test parsing UPDATE query."""
        query = "UPDATE users SET age = 31 WHERE id = 1"
        result = self.parser.parse(query)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['type'], 'UPDATE')
        self.assertEqual(result['table_name'], 'users')
        self.assertEqual(result['set_values']['age'], 31)
    
    def test_parse_delete(self):
        """Test parsing DELETE query."""
        query = "DELETE FROM users WHERE id = 1"
        result = self.parser.parse(query)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['type'], 'DELETE')
        self.assertEqual(result['table_name'], 'users')
        self.assertEqual(result['where']['column'], 'id')
    
    def test_parse_select_join(self):
        """Test parsing SELECT with JOIN."""
        query = "SELECT * FROM users INNER JOIN orders ON users.id = orders.user_id"
        result = self.parser.parse(query)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['type'], 'SELECT_JOIN')
        self.assertEqual(result['left_table'], 'users')
        self.assertEqual(result['right_table'], 'orders')
        self.assertEqual(result['join_condition']['left_column'], 'id')
        self.assertEqual(result['join_condition']['right_column'], 'user_id')


class TestEndToEnd(unittest.TestCase):
    """End-to-end integration tests."""
    
    def setUp(self):
        """Set up database before each test."""
        self.db = SimpleDB()
    
    def test_full_crud_workflow(self):
        """Test complete CRUD workflow."""
        # Create table
        result = self.db.execute(
            "CREATE TABLE users (id INT PRIMARY KEY, name TEXT, email TEXT UNIQUE)"
        )
        self.assertTrue(result['success'])
        
        # Insert rows
        result = self.db.execute("INSERT INTO users VALUES (1, 'John Doe', 'john@example.com')")
        self.assertTrue(result['success'])
        
        result = self.db.execute("INSERT INTO users VALUES (2, 'Jane Smith', 'jane@example.com')")
        self.assertTrue(result['success'])
        
        # Select all
        result = self.db.execute("SELECT * FROM users")
        self.assertTrue(result['success'])
        self.assertEqual(len(result['data']), 2)
        
        # Select with WHERE
        result = self.db.execute("SELECT * FROM users WHERE id = 1")
        self.assertTrue(result['success'])
        self.assertEqual(len(result['data']), 1)
        
        # Update
        result = self.db.execute("UPDATE users SET name = 'John Updated' WHERE id = 1")
        self.assertTrue(result['success'])
        
        # Verify update
        result = self.db.execute("SELECT * FROM users WHERE id = 1")
        self.assertTrue(result['success'])
        # Check if 'John Updated' is in the first row
        self.assertIn('John Updated', result['data'][0])
        
        # Delete
        result = self.db.execute("DELETE FROM users WHERE id = 2")
        self.assertTrue(result['success'])
        
        # Verify delete
        result = self.db.execute("SELECT * FROM users")
        self.assertTrue(result['success'])
        self.assertEqual(len(result['data']), 1)
    
    def test_join_query(self):
        """Test JOIN query."""
        # Create tables
        self.db.execute("CREATE TABLE users (id INT PRIMARY KEY, name TEXT)")
        self.db.execute("CREATE TABLE orders (id INT PRIMARY KEY, user_id INT, product TEXT)")
        
        # Insert data
        self.db.execute("INSERT INTO users VALUES (1, 'John Doe')")
        self.db.execute("INSERT INTO users VALUES (2, 'Jane Smith')")
        self.db.execute("INSERT INTO orders VALUES (101, 1, 'Laptop')")
        self.db.execute("INSERT INTO orders VALUES (102, 1, 'Mouse')")
        self.db.execute("INSERT INTO orders VALUES (103, 2, 'Keyboard')")
        
        # Test JOIN
        result = self.db.execute("SELECT * FROM users JOIN orders ON users.id = orders.user_id")
        
        self.assertTrue(result['success'])
        self.assertEqual(len(result['data']), 3)  # 3 matching rows
        
        # Verify columns have table prefixes
        self.assertIn('users.id', result['columns'])
        self.assertIn('orders.id', result['columns'])


if __name__ == '__main__':
    unittest.main()
