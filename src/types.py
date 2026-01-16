"""
Data type validation and conversion utilities.

This module provides helpers for validating and converting values
to appropriate Python types based on SQL-like type specifications.
"""

from typing import Any


def validate_type(value: Any, type_name: str) -> bool:
    """
    Validate that a value matches the expected type.
    
    Args:
        value: Value to validate
        type_name: Type name (INT, TEXT, FLOAT, etc.)
        
    Returns:
        True if valid, False otherwise
    """
    type_name = type_name.upper()
    
    if type_name == 'INT':
        return isinstance(value, int)
    elif type_name in ('TEXT', 'VARCHAR', 'CHAR', 'STRING'):
        return isinstance(value, str)
    elif type_name in ('FLOAT', 'REAL', 'DOUBLE'):
        return isinstance(value, (int, float))
    else:
        # Unknown type - accept anything
        return True


def convert_value(value: Any, type_name: str) -> Any:
    """
    Convert a value to the appropriate Python type.
    
    Args:
        value: Value to convert
        type_name: Target type name (INT, TEXT, FLOAT, etc.)
        
    Returns:
        Converted value
        
    Raises:
        ValueError: If conversion fails
    """
    type_name = type_name.upper()
    
    try:
        if type_name == 'INT':
            return int(value)
        elif type_name in ('TEXT', 'VARCHAR', 'CHAR', 'STRING'):
            return str(value)
        elif type_name in ('FLOAT', 'REAL', 'DOUBLE'):
            return float(value)
        else:
            # Unknown type - return as-is
            return value
    except (ValueError, TypeError) as e:
        raise ValueError(f"Cannot convert '{value}' to {type_name}: {str(e)}")


def get_python_type(type_name: str) -> type:
    """
    Get the Python type corresponding to a SQL-like type name.
    
    Args:
        type_name: SQL-like type name
        
    Returns:
        Python type class
    """
    type_name = type_name.upper()
    
    if type_name == 'INT':
        return int
    elif type_name in ('TEXT', 'VARCHAR', 'CHAR', 'STRING'):
        return str
    elif type_name in ('FLOAT', 'REAL', 'DOUBLE'):
        return float
    else:
        return object
