"""
Pre-submission verification script for Pesapal Challenge 2026.
Run this to verify your setup is complete and ready for submission.
"""

import sys
import subprocess
from pathlib import Path

def print_status(message, status):
    """Print colored status message."""
    symbol = "✅" if status else "❌"
    print(f"{symbol} {message}")
    return status

def check_files_exist():
    """Check all required files exist."""
    print("\n📁 Checking required files...")
    required_files = [
        "README.md",
        "requirements.txt",
        ".gitignore",
        "repl.py",
        "src/__init__.py",
        "src/database.py",
        "src/table.py",
        "src/parser.py",
        "src/types.py",
        "web_app/__init__.py",
        "web_app/app.py",
        "web_app/templates/base.html",
        "web_app/templates/index.html",
        "web_app/templates/create.html",
        "web_app/templates/edit.html",
        "web_app/templates/view_table.html",
        "web_app/templates/create_table.html",
        "tests/test_database.py"
    ]
    
    all_exist = True
    for file in required_files:
        exists = Path(file).exists()
        if not exists:
            print_status(f"Missing: {file}", False)
            all_exist = False
    
    if all_exist:
        print_status(f"All {len(required_files)} required files present", True)
    return all_exist

def check_dependencies():
    """Check if dependencies are installed."""
    print("\n📦 Checking dependencies...")
    try:
        import flask
        import tabulate
        print_status("Flask installed", True)
        print_status("Tabulate installed", True)
        return True
    except ImportError as e:
        print_status(f"Missing dependency: {e}", False)
        print("   Run: pip install -r requirements.txt")
        return False

def run_tests():
    """Run unit tests."""
    print("\n🧪 Running unit tests...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "tests.test_database", "-v"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            # Count tests
            if "Ran" in result.stderr:
                test_line = [line for line in result.stderr.split('\n') if 'Ran' in line][0]
                print_status(f"Unit tests passed - {test_line}", True)
                return True
        else:
            print_status("Unit tests failed", False)
            print(result.stderr)
            return False
    except Exception as e:
        print_status(f"Error running tests: {e}", False)
        return False

def check_imports():
    """Check if core modules can be imported."""
    print("\n🐍 Checking module imports...")
    try:
        from src.database import SimpleDB
        from src.table import Table
        from src.parser import QueryParser
        from src.types import validate_type, convert_value
        print_status("All core modules import successfully", True)
        return True
    except Exception as e:
        print_status(f"Import error: {e}", False)
        return False

def check_basic_functionality():
    """Test basic database operations."""
    print("\n⚙️  Testing basic functionality...")
    try:
        from src.database import SimpleDB
        
        db = SimpleDB()
        
        # Test CREATE
        result = db.execute("CREATE TABLE test (id INT PRIMARY KEY, name TEXT)")
        if not result['success']:
            print_status("CREATE TABLE failed", False)
            return False
        
        # Test INSERT
        result = db.execute("INSERT INTO test VALUES (1, 'Test')")
        if not result['success']:
            print_status("INSERT failed", False)
            return False
        
        # Test SELECT
        result = db.execute("SELECT * FROM test")
        if not result['success'] or len(result['data']) != 1:
            print_status("SELECT failed", False)
            return False
        
        # Test JOIN
        db.execute("CREATE TABLE test2 (id INT PRIMARY KEY, test_id INT)")
        db.execute("INSERT INTO test2 VALUES (1, 1)")
        result = db.execute("SELECT * FROM test JOIN test2 ON test.id = test2.test_id")
        if not result['success'] or len(result['data']) != 1:
            print_status("JOIN failed", False)
            return False
        
        print_status("All CRUD + JOIN operations working", True)
        return True
    except Exception as e:
        print_status(f"Functionality test error: {e}", False)
        return False

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("🎯 Pesapal Challenge 2026 - Pre-Submission Verification")
    print("=" * 60)
    
    checks = [
        ("Files", check_files_exist),
        ("Dependencies", check_dependencies),
        ("Imports", check_imports),
        ("Basic Functionality", check_basic_functionality),
        ("Unit Tests", run_tests),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            results.append(check_func())
        except Exception as e:
            print_status(f"{name} check crashed: {e}", False)
            results.append(False)
    
    print("\n" + "=" * 60)
    if all(results):
        print("✅ ALL CHECKS PASSED - Ready for submission!")
        print("\nNext steps:")
        print("1. Push code to GitHub (make repo public)")
        print("2. Update README.md with your GitHub repo URL")
        print("3. Add your email/contact info in README.md")
        print("4. Submit application with repo link before deadline")
        print("=" * 60)
        return 0
    else:
        print("❌ SOME CHECKS FAILED - Fix issues before submitting")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
