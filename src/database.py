"""
SimpleDB - Main database module.

This module contains the SimpleDB class which manages all tables
and provides the main interface for executing SQL-like queries.
"""

from typing import Dict, Any, Optional
from src.table import Table
from src.parser import QueryParser


class SimpleDB:
    """
    Main in-memory database class.
    
    Manages multiple tables and provides SQL-like query execution interface.
    """
    
    def __init__(self):
        """Initialize an empty database."""
        self.tables: Dict[str, Table] = {}
        self.parser = QueryParser()
    
    def create_table(self, name: str, columns: list, primary_key: str, 
                     unique_columns: Optional[list] = None) -> Dict[str, Any]:
        """
        Create a new table in the database.
        
        Args:
            name: Table name
            columns: List of column definitions [(name, type), ...]
            primary_key: Name of the primary key column
            unique_columns: Optional list of columns with UNIQUE constraint
            
        Returns:
            Result dictionary with success status and message
        """
        # TODO: Implement table creation logic
        # - Check if table already exists
        # - Validate primary key exists in columns
        # - Create Table instance
        # - Add to self.tables dictionary
        
        if name in self.tables:
            return {
                'success': False,
                'message': f"Table '{name}' already exists"
            }
        
        # Validate primary key is in columns
        column_names = [col[0] for col in columns]
        if primary_key not in column_names:
            return {
                'success': False,
                'message': f"Primary key '{primary_key}' not found in columns"
            }
        
        # Create the table
        self.tables[name] = Table(name, columns, primary_key, unique_columns or [])
        
        return {
            'success': True,
            'message': f"Table '{name}' created successfully"
        }
    
    def get_table(self, name: str) -> Optional[Table]:
        """
        Get a table by name.
        
        Args:
            name: Table name
            
        Returns:
            Table instance or None if not found
        """
        return self.tables.get(name)
    
    def list_tables(self) -> list:
        """
        Get list of all table names.
        
        Returns:
            List of table names
        """
        return list(self.tables.keys())
    
    def execute(self, query: str) -> Dict[str, Any]:
        """
        Execute a SQL-like query.
        
        Args:
            query: SQL-like query string
            
        Returns:
            Result dictionary with success, message, and optional data
        """
        try:
            # Parse the query
            parsed = self.parser.parse(query)
            
            if not parsed or not parsed.get('success'):
                return {
                    'success': False,
                    'message': parsed.get('message', 'Failed to parse query')
                }
            
            query_type = parsed['type']
            
            # Route to appropriate handler
            if query_type == 'CREATE_TABLE':
                return self._handle_create_table(parsed)
            elif query_type == 'INSERT':
                return self._handle_insert(parsed)
            elif query_type == 'SELECT':
                return self._handle_select(parsed)
            elif query_type == 'SELECT_JOIN':
                return self._handle_select_join(parsed)
            elif query_type == 'UPDATE':
                return self._handle_update(parsed)
            elif query_type == 'DELETE':
                return self._handle_delete(parsed)
            else:
                return {
                    'success': False,
                    'message': f"Unsupported query type: {query_type}"
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f"Error executing query: {str(e)}"
            }
    
    def _handle_create_table(self, parsed: dict) -> Dict[str, Any]:
        """Handle CREATE TABLE query."""
        return self.create_table(
            parsed['table_name'],
            parsed['columns'],
            parsed['primary_key'],
            parsed.get('unique_columns', [])
        )
    
    def _handle_insert(self, parsed: dict) -> Dict[str, Any]:
        """Handle INSERT query."""
        table = self.get_table(parsed['table_name'])
        if not table:
            return {
                'success': False,
                'message': f"Table '{parsed['table_name']}' does not exist"
            }
        
        return table.insert(parsed['values'])
    
    def _handle_select(self, parsed: dict) -> Dict[str, Any]:
        """Handle SELECT query."""
        table = self.get_table(parsed['table_name'])
        if not table:
            return {
                'success': False,
                'message': f"Table '{parsed['table_name']}' does not exist"
            }
        
        return table.select(
            columns=parsed.get('columns', ['*']),
            where=parsed.get('where')
        )
    
    def _handle_select_join(self, parsed: dict) -> Dict[str, Any]:
        """Handle SELECT with JOIN query."""
        left_table = self.get_table(parsed['left_table'])
        right_table = self.get_table(parsed['right_table'])
        
        if not left_table:
            return {
                'success': False,
                'message': f"Table '{parsed['left_table']}' does not exist"
            }
        
        if not right_table:
            return {
                'success': False,
                'message': f"Table '{parsed['right_table']}' does not exist"
            }
        
        # Perform INNER JOIN
        join_condition = parsed['join_condition']
        left_col = join_condition['left_column']
        right_col = join_condition['right_column']
        
        # Validate columns exist
        if left_col not in left_table.column_names:
            return {
                'success': False,
                'message': f"Column '{left_col}' not found in table '{parsed['left_table']}'"
            }
        
        if right_col not in right_table.column_names:
            return {
                'success': False,
                'message': f"Column '{right_col}' not found in table '{parsed['right_table']}'"
            }
        
        # Build joined result
        joined_rows = []
        
        for left_row in left_table.rows:
            left_val = left_row[left_col]
            
            # Find matching rows in right table
            for right_row in right_table.rows:
                right_val = right_row[right_col]
                
                if left_val == right_val:
                    # Merge rows
                    merged_row = {}
                    
                    # Add left table columns with table prefix
                    for col in left_table.column_names:
                        merged_row[f"{parsed['left_table']}.{col}"] = left_row[col]
                    
                    # Add right table columns with table prefix
                    for col in right_table.column_names:
                        merged_row[f"{parsed['right_table']}.{col}"] = right_row[col]
                    
                    joined_rows.append(merged_row)
        
        # Apply WHERE filter if specified
        if parsed.get('where'):
            where_col = parsed['where']['column']
            where_val = parsed['where']['value']
            joined_rows = [row for row in joined_rows if row.get(where_col) == where_val]
        
        # Determine output columns
        if parsed['columns'] == ['*']:
            # All columns from both tables
            all_columns = []
            for col in left_table.column_names:
                all_columns.append(f"{parsed['left_table']}.{col}")
            for col in right_table.column_names:
                all_columns.append(f"{parsed['right_table']}.{col}")
            output_columns = all_columns
        else:
            output_columns = parsed['columns']
        
        # Extract data for output
        result_data = []
        for row in joined_rows:
            result_row = [row.get(col) for col in output_columns]
            result_data.append(result_row)
        
        return {
            'success': True,
            'message': f"Selected {len(result_data)} row(s) from JOIN",
            'columns': output_columns,
            'data': result_data
        }
    
    def _handle_update(self, parsed: dict) -> Dict[str, Any]:
        """Handle UPDATE query."""
        table = self.get_table(parsed['table_name'])
        if not table:
            return {
                'success': False,
                'message': f"Table '{parsed['table_name']}' does not exist"
            }
        
        return table.update(
            set_values=parsed['set_values'],
            where=parsed.get('where')
        )
    
    def _handle_delete(self, parsed: dict) -> Dict[str, Any]:
        """Handle DELETE query."""
        table = self.get_table(parsed['table_name'])
        if not table:
            return {
                'success': False,
                'message': f"Table '{parsed['table_name']}' does not exist"
            }
        
        return table.delete(where=parsed.get('where'))
