"""
SQL-like query parser.

This module provides a simple parser for SQL-like queries using
regular expressions and string manipulation.
"""

import re
from typing import Dict, Any, Optional, List, Tuple


class QueryParser:
    """
    Simple SQL-like query parser.
    
    Supports: CREATE TABLE, INSERT, SELECT, UPDATE, DELETE
    """
    
    def __init__(self):
        """Initialize the parser."""
        pass
    
    def parse(self, query: str) -> Dict[str, Any]:
        """
        Parse a SQL-like query string.
        
        Args:
            query: SQL-like query string
            
        Returns:
            Dictionary with parsed query information
        """
        query = query.strip()
        
        # Determine query type
        query_upper = query.upper()
        
        if query_upper.startswith('CREATE TABLE'):
            return self._parse_create_table(query)
        elif query_upper.startswith('INSERT INTO'):
            return self._parse_insert(query)
        elif query_upper.startswith('SELECT'):
            return self._parse_select(query)
        elif query_upper.startswith('UPDATE'):
            return self._parse_update(query)
        elif query_upper.startswith('DELETE FROM'):
            return self._parse_delete(query)
        else:
            return {
                'success': False,
                'message': 'Unsupported query type'
            }
    
    def _parse_create_table(self, query: str) -> Dict[str, Any]:
        """
        Parse CREATE TABLE query.
        
        Example: CREATE TABLE users (id INT PRIMARY KEY, name TEXT, email TEXT UNIQUE)
        """
        # TODO: Implement CREATE TABLE parsing
        # Pattern: CREATE TABLE table_name (col1 type1 [PRIMARY KEY], col2 type2 [UNIQUE], ...)
        
        pattern = r'CREATE TABLE\s+(\w+)\s*\((.*)\)'
        match = re.match(pattern, query, re.IGNORECASE)
        
        if not match:
            return {
                'success': False,
                'message': 'Invalid CREATE TABLE syntax'
            }
        
        table_name = match.group(1)
        columns_str = match.group(2)
        
        # Parse columns
        columns = []
        primary_key = None
        unique_columns = []
        
        # Split by comma (but not within parentheses)
        col_defs = [c.strip() for c in columns_str.split(',')]
        
        for col_def in col_defs:
            parts = col_def.split()
            if len(parts) < 2:
                return {
                    'success': False,
                    'message': f'Invalid column definition: {col_def}'
                }
            
            col_name = parts[0]
            col_type = parts[1]
            
            # Check for PRIMARY KEY
            if 'PRIMARY' in col_def.upper() and 'KEY' in col_def.upper():
                primary_key = col_name
            
            # Check for UNIQUE
            if 'UNIQUE' in col_def.upper():
                unique_columns.append(col_name)
            
            columns.append((col_name, col_type.upper()))
        
        if not primary_key:
            return {
                'success': False,
                'message': 'No PRIMARY KEY specified'
            }
        
        return {
            'success': True,
            'type': 'CREATE_TABLE',
            'table_name': table_name,
            'columns': columns,
            'primary_key': primary_key,
            'unique_columns': unique_columns
        }
    
    def _parse_insert(self, query: str) -> Dict[str, Any]:
        """
        Parse INSERT query.
        
        Example: INSERT INTO users VALUES (1, 'John Doe', 'john@example.com')
        """
        # TODO: Implement INSERT parsing
        # Pattern: INSERT INTO table_name VALUES (val1, val2, ...)
        
        pattern = r'INSERT INTO\s+(\w+)\s+VALUES\s*\((.*)\)'
        match = re.match(pattern, query, re.IGNORECASE)
        
        if not match:
            return {
                'success': False,
                'message': 'Invalid INSERT syntax'
            }
        
        table_name = match.group(1)
        values_str = match.group(2)
        
        # Parse values (handle strings in quotes)
        values = self._parse_values(values_str)
        
        return {
            'success': True,
            'type': 'INSERT',
            'table_name': table_name,
            'values': values
        }
    
    def _parse_select(self, query: str) -> Dict[str, Any]:
        """
        Parse SELECT query.
        
        Examples:
            SELECT * FROM users
            SELECT * FROM users WHERE id = 1
            SELECT * FROM users INNER JOIN orders ON users.id = orders.user_id
        """
        # Check for JOIN
        if 'JOIN' in query.upper():
            return self._parse_select_with_join(query)
        
        # Regular SELECT without JOIN
        pattern = r'SELECT\s+(.*?)\s+FROM\s+(\w+)(?:\s+WHERE\s+(.*))?'
        match = re.match(pattern, query, re.IGNORECASE)
        
        if not match:
            return {
                'success': False,
                'message': 'Invalid SELECT syntax'
            }
        
        columns_str = match.group(1).strip()
        table_name = match.group(2)
        where_str = match.group(3)
        
        # Parse columns
        if columns_str == '*':
            columns = ['*']
        else:
            columns = [c.strip() for c in columns_str.split(',')]
        
        # Parse WHERE clause
        where = None
        if where_str:
            where = self._parse_where(where_str)
        
        return {
            'success': True,
            'type': 'SELECT',
            'table_name': table_name,
            'columns': columns,
            'where': where
        }
    
    def _parse_select_with_join(self, query: str) -> Dict[str, Any]:
        """
        Parse SELECT query with JOIN.
        
        Example: SELECT * FROM users INNER JOIN orders ON users.id = orders.user_id
        """
        # Pattern: SELECT columns FROM table1 [INNER] JOIN table2 ON table1.col = table2.col [WHERE condition]
        pattern = r'SELECT\s+(.*?)\s+FROM\s+(\w+)\s+(?:INNER\s+)?JOIN\s+(\w+)\s+ON\s+(\w+)\.(\w+)\s*=\s*(\w+)\.(\w+)(?:\s+WHERE\s+(.*))?'
        match = re.match(pattern, query, re.IGNORECASE)
        
        if not match:
            return {
                'success': False,
                'message': 'Invalid JOIN syntax. Expected: SELECT ... FROM table1 JOIN table2 ON table1.col = table2.col'
            }
        
        columns_str = match.group(1).strip()
        left_table = match.group(2)
        right_table = match.group(3)
        left_join_table = match.group(4)
        left_join_col = match.group(5)
        right_join_table = match.group(6)
        right_join_col = match.group(7)
        where_str = match.group(8)
        
        # Parse columns
        if columns_str == '*':
            columns = ['*']
        else:
            columns = [c.strip() for c in columns_str.split(',')]
        
        # Parse WHERE clause
        where = None
        if where_str:
            where = self._parse_where(where_str)
        
        return {
            'success': True,
            'type': 'SELECT_JOIN',
            'columns': columns,
            'left_table': left_table,
            'right_table': right_table,
            'join_condition': {
                'left_table': left_join_table,
                'left_column': left_join_col,
                'right_table': right_join_table,
                'right_column': right_join_col
            },
            'where': where
        }
    
    def _parse_update(self, query: str) -> Dict[str, Any]:
        """
        Parse UPDATE query.
        
        Example: UPDATE users SET age = 31 WHERE id = 1
        """
        # TODO: Implement UPDATE parsing
        # Pattern: UPDATE table_name SET col1=val1, col2=val2 WHERE condition
        
        pattern = r'UPDATE\s+(\w+)\s+SET\s+(.+?)(?:\s+WHERE\s+(.*))?$'
        match = re.match(pattern, query, re.IGNORECASE)
        
        if not match:
            return {
                'success': False,
                'message': 'Invalid UPDATE syntax'
            }
        
        table_name = match.group(1)
        set_str = match.group(2)
        where_str = match.group(3)
        
        # Parse SET clause
        set_values = {}
        set_parts = [s.strip() for s in set_str.split(',')]
        for part in set_parts:
            if '=' not in part:
                return {
                    'success': False,
                    'message': f'Invalid SET clause: {part}'
                }
            col, val = part.split('=', 1)
            col = col.strip()
            val = self._parse_single_value(val.strip())
            set_values[col] = val
        
        # Parse WHERE clause
        where = None
        if where_str:
            where = self._parse_where(where_str)
        
        return {
            'success': True,
            'type': 'UPDATE',
            'table_name': table_name,
            'set_values': set_values,
            'where': where
        }
    
    def _parse_delete(self, query: str) -> Dict[str, Any]:
        """
        Parse DELETE query.
        
        Example: DELETE FROM users WHERE id = 1
        """
        # TODO: Implement DELETE parsing
        # Pattern: DELETE FROM table_name WHERE condition
        
        pattern = r'DELETE FROM\s+(\w+)(?:\s+WHERE\s+(.*))?'
        match = re.match(pattern, query, re.IGNORECASE)
        
        if not match:
            return {
                'success': False,
                'message': 'Invalid DELETE syntax'
            }
        
        table_name = match.group(1)
        where_str = match.group(2)
        
        # Parse WHERE clause
        where = None
        if where_str:
            where = self._parse_where(where_str)
        
        return {
            'success': True,
            'type': 'DELETE',
            'table_name': table_name,
            'where': where
        }
    
    def _parse_select_with_join(self, query: str) -> Dict[str, Any]:
        """
        Parse SELECT query with JOIN.
        
        Example: SELECT * FROM users INNER JOIN orders ON users.id = orders.user_id
        """
        # Pattern: SELECT columns FROM table1 [INNER] JOIN table2 ON table1.col = table2.col [WHERE condition]
        pattern = r'SELECT\s+(.*?)\s+FROM\s+(\w+)\s+(?:INNER\s+)?JOIN\s+(\w+)\s+ON\s+(\w+)\.(\w+)\s*=\s*(\w+)\.(\w+)(?:\s+WHERE\s+(.*))?'
        match = re.match(pattern, query, re.IGNORECASE)
        
        if not match:
            return {
                'success': False,
                'message': 'Invalid JOIN syntax. Expected: SELECT ... FROM table1 JOIN table2 ON table1.col = table2.col'
            }
        
        columns_str = match.group(1).strip()
        left_table = match.group(2)
        right_table = match.group(3)
        left_join_table = match.group(4)
        left_join_col = match.group(5)
        right_join_table = match.group(6)
        right_join_col = match.group(7)
        where_str = match.group(8)
        
        # Parse columns
        if columns_str == '*':
            columns = ['*']
        else:
            columns = [c.strip() for c in columns_str.split(',')]
        
        # Parse WHERE clause
        where = None
        if where_str:
            where = self._parse_where(where_str)
        
        return {
            'success': True,
            'type': 'SELECT_JOIN',
            'columns': columns,
            'left_table': left_table,
            'right_table': right_table,
            'join_condition': {
                'left_table': left_join_table,
                'left_column': left_join_col,
                'right_table': right_join_table,
                'right_column': right_join_col
            },
            'where': where
        }
    
    def _parse_where(self, where_str: str) -> Optional[Dict[str, Any]]:
        """
        Parse WHERE clause (simple: column = value).
        
        Args:
            where_str: WHERE clause string
            
        Returns:
            Dictionary with column and value
        """
        # Simple WHERE: column = value
        match = re.match(r'(\w+)\s*=\s*(.+)', where_str.strip())
        if match:
            column = match.group(1)
            value = self._parse_single_value(match.group(2).strip())
            return {
                'column': column,
                'value': value
            }
        return None
    
    def _parse_values(self, values_str: str) -> List[Any]:
        """
        Parse comma-separated values, handling quoted strings.
        
        Args:
            values_str: String of comma-separated values
            
        Returns:
            List of parsed values
        """
        values = []
        current = ''
        in_quotes = False
        quote_char = None
        
        for char in values_str:
            if char in ('"', "'") and not in_quotes:
                in_quotes = True
                quote_char = char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
            elif char == ',' and not in_quotes:
                values.append(self._parse_single_value(current.strip()))
                current = ''
            else:
                current += char
        
        if current.strip():
            values.append(self._parse_single_value(current.strip()))
        
        return values
    
    def _parse_single_value(self, value_str: str) -> Any:
        """
        Parse a single value (int, float, or string).
        
        Args:
            value_str: String representation of value
            
        Returns:
            Parsed value
        """
        value_str = value_str.strip()
        
        # Remove quotes if present
        if (value_str.startswith('"') and value_str.endswith('"')) or \
           (value_str.startswith("'") and value_str.endswith("'")):
            return value_str[1:-1]
        
        # Try to parse as int
        try:
            return int(value_str)
        except ValueError:
            pass
        
        # Try to parse as float
        try:
            return float(value_str)
        except ValueError:
            pass
        
        # Return as string
        return value_str
