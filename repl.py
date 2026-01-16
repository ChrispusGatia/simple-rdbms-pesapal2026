"""
REPL (Read-Eval-Print Loop) interface for SimpleDB.

This module provides an interactive command-line interface for executing
SQL-like queries against the in-memory database.
"""

from tabulate import tabulate
from src.database import SimpleDB


def print_result(result):
    """
    Print query results in a nicely formatted table.
    
    Args:
        result: Query result from database execution
    """
    if isinstance(result, dict):
        if result.get('success'):
            print(f"✓ {result.get('message', 'Success')}")
            
            # If there's data to display (SELECT query)
            if 'data' in result and result['data']:
                headers = result.get('columns', [])
                rows = result['data']
                print(tabulate(rows, headers=headers, tablefmt='grid'))
            elif 'data' in result and not result['data']:
                print("No rows returned.")
        else:
            print(f"✗ Error: {result.get('message', 'Unknown error')}")
    else:
        print(result)


def main():
    """Main REPL loop."""
    db = SimpleDB()
    
    print("=" * 60)
    print("SimpleDB REPL - Pesapal Junior Developer Challenge 2026")
    print("=" * 60)
    print("Type SQL-like queries or 'exit'/'quit' to exit.")
    print("Example: CREATE TABLE users (id INT PRIMARY KEY, name TEXT)")
    print("=" * 60)
    print()
    
    while True:
        try:
            # Read input
            query = input("SimpleDB> ").strip()
            
            # Check for exit commands
            if query.lower() in ['exit', 'quit', 'q']:
                print("Goodbye!")
                break
            
            # Skip empty queries
            if not query:
                continue
            
            # Execute query
            result = db.execute(query)
            
            # Print result
            print_result(result)
            print()
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            print()


if __name__ == "__main__":
    main()
