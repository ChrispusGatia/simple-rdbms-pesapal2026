"""
Table module - Core table implementation.

This module contains the Table class which manages rows, columns,
indexes, and constraints for a single database table.
"""

from typing import Dict, Any, List, Optional, Tuple
from src.types import validate_type, convert_value


class Table:
    """
    Represents a single database table with rows, columns, and indexes.
    """
    
    def __init__(self, name: str, columns: List[Tuple[str, str]], 
                 primary_key: str, unique_columns: List[str]):
        """
        Initialize a new table.
        
        Args:
            name: Table name
            columns: List of (column_name, column_type) tuples
            primary_key: Name of the primary key column
            unique_columns: List of columns with UNIQUE constraint
        """
        self.name = name
        self.columns = columns  # [(name, type), ...]
        self.column_names = [col[0] for col in columns]
        self.column_types = {col[0]: col[1] for col in columns}
        self.primary_key = primary_key
        self.unique_columns = set(unique_columns)
        
        # Storage
        self.rows: List[Dict[str, Any]] = []
        
        # Indexes - hash index on primary key
        self.primary_index: Dict[Any, int] = {}  # pk_value -> row_index
        
        # Unique indexes for unique columns
        self.unique_indexes: Dict[str, Dict[Any, int]] = {}
        for col in self.unique_columns:
            self.unique_indexes[col] = {}
    
    def insert(self, values: List[Any]) -> Dict[str, Any]:
        """
        Insert a new row into the table.
        
        Args:
            values: List of values matching column order
            
        Returns:
            Result dictionary
        """
        # TODO: Implement insertion logic
        # - Validate value count matches column count
        # - Validate types
        # - Check primary key doesn't already exist
        # - Check unique constraints
        # - Add to rows list
        # - Update indexes
        
        if len(values) != len(self.columns):
            return {
                'success': False,
                'message': f"Expected {len(self.columns)} values, got {len(values)}"
            }
        
        # Create row dictionary
        row = {}
        for i, (col_name, col_type) in enumerate(self.columns):
            try:
                row[col_name] = convert_value(values[i], col_type)
            except ValueError as e:
                return {
                    'success': False,
                    'message': f"Type error for column '{col_name}': {str(e)}"
                }
        
        # Check primary key constraint
        pk_value = row[self.primary_key]
        if pk_value in self.primary_index:
            return {
                'success': False,
                'message': f"Primary key violation: '{pk_value}' already exists"
            }
        
        # Check unique constraints
        for col in self.unique_columns:
            col_value = row[col]
            if col_value in self.unique_indexes[col]:
                return {
                    'success': False,
                    'message': f"Unique constraint violation: '{col}' = '{col_value}' already exists"
                }
        
        # Insert the row
        row_index = len(self.rows)
        self.rows.append(row)
        
        # Update primary index
        self.primary_index[pk_value] = row_index
        
        # Update unique indexes
        for col in self.unique_columns:
            self.unique_indexes[col][row[col]] = row_index
        
        return {
            'success': True,
            'message': f"Inserted 1 row into '{self.name}'"
        }
    
    def select(self, columns: List[str] = None, 
               where: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Select rows from the table.
        
        Args:
            columns: List of column names to select (or ['*'] for all)
            where: Optional WHERE clause as dict {'column': value}
            
        Returns:
            Result dictionary with data
        """
        # TODO: Implement SELECT logic
        # - If WHERE clause, filter rows
        # - Use index for primary key lookups
        # - Return matching rows with selected columns
        
        if not columns or columns == ['*']:
            columns = self.column_names
        
        # Filter rows based on WHERE clause
        filtered_rows = []
        if where:
            # Simple WHERE: column = value
            where_col = where.get('column')
            where_val = where.get('value')
            
            if where_col == self.primary_key:
                # Use primary key index for fast lookup
                row_idx = self.primary_index.get(where_val)
                if row_idx is not None:
                    filtered_rows = [self.rows[row_idx]]
            else:
                # Linear scan
                for row in self.rows:
                    if row.get(where_col) == where_val:
                        filtered_rows.append(row)
        else:
            filtered_rows = self.rows
        
        # Extract selected columns
        result_data = []
        for row in filtered_rows:
            result_row = [row.get(col) for col in columns]
            result_data.append(result_row)
        
        return {
            'success': True,
            'message': f"Selected {len(result_data)} row(s)",
            'columns': columns,
            'data': result_data
        }
    
    def update(self, set_values: Dict[str, Any], 
               where: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Update rows in the table.
        
        Args:
            set_values: Dictionary of {column: new_value}
            where: Optional WHERE clause
            
        Returns:
            Result dictionary
        """
        # TODO: Implement UPDATE logic
        # - Find matching rows
        # - Validate new values
        # - Check constraints (can't update PK if it creates duplicate)
        # - Update rows and indexes
        
        if not where:
            return {
                'success': False,
                'message': "UPDATE without WHERE clause is not supported"
            }
        
        where_col = where.get('column')
        where_val = where.get('value')
        
        # Find matching rows
        rows_to_update = []
        for idx, row in enumerate(self.rows):
            if row.get(where_col) == where_val:
                rows_to_update.append(idx)
        
        if not rows_to_update:
            return {
                'success': True,
                'message': "Updated 0 row(s)"
            }
        
        # Update rows
        for idx in rows_to_update:
            for col, new_val in set_values.items():
                if col in self.column_names:
                    # Validate type
                    try:
                        converted = convert_value(new_val, self.column_types[col])
                        self.rows[idx][col] = converted
                    except ValueError as e:
                        return {
                            'success': False,
                            'message': f"Type error: {str(e)}"
                        }
        
        return {
            'success': True,
            'message': f"Updated {len(rows_to_update)} row(s)"
        }
    
    def delete(self, where: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Delete rows from the table.
        
        Args:
            where: Optional WHERE clause
            
        Returns:
            Result dictionary
        """
        # TODO: Implement DELETE logic
        # - Find matching rows
        # - Remove from rows list
        # - Update indexes
        
        if not where:
            return {
                'success': False,
                'message': "DELETE without WHERE clause is not supported"
            }
        
        where_col = where.get('column')
        where_val = where.get('value')
        
        # Find matching rows
        rows_to_delete = []
        for idx, row in enumerate(self.rows):
            if row.get(where_col) == where_val:
                rows_to_delete.append(idx)
        
        if not rows_to_delete:
            return {
                'success': True,
                'message': "Deleted 0 row(s)"
            }
        
        # Delete rows (in reverse order to maintain indices)
        for idx in sorted(rows_to_delete, reverse=True):
            row = self.rows.pop(idx)
            
            # Remove from primary index
            pk_val = row[self.primary_key]
            if pk_val in self.primary_index:
                del self.primary_index[pk_val]
            
            # Remove from unique indexes
            for col in self.unique_columns:
                col_val = row[col]
                if col_val in self.unique_indexes[col]:
                    del self.unique_indexes[col][col_val]
        
        # Rebuild indexes since row indices changed
        self._rebuild_indexes()
        
        return {
            'success': True,
            'message': f"Deleted {len(rows_to_delete)} row(s)"
        }
    
    def _rebuild_indexes(self):
        """Rebuild all indexes after row deletion."""
        self.primary_index.clear()
        for col in self.unique_columns:
            self.unique_indexes[col].clear()
        
        for idx, row in enumerate(self.rows):
            # Rebuild primary index
            self.primary_index[row[self.primary_key]] = idx
            
            # Rebuild unique indexes
            for col in self.unique_columns:
                self.unique_indexes[col][row[col]] = idx
