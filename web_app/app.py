"""
Flask web application for SimpleDB.

Provides a web interface for CRUD operations on database tables.
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from src.database import SimpleDB


app = Flask(__name__)
app.secret_key = 'simpledb_secret_key_change_in_production'

# Initialize database
db = SimpleDB()

# Create sample tables for demonstration with JOIN capability
db.execute("CREATE TABLE users (id INT PRIMARY KEY, name TEXT, email TEXT UNIQUE, age INT)")
db.execute("CREATE TABLE products (id INT PRIMARY KEY, name TEXT, price FLOAT, stock INT)")
db.execute("CREATE TABLE orders (id INT PRIMARY KEY, user_id INT, product_id INT, quantity INT)")

# Add sample data to demonstrate JOIN
db.execute("INSERT INTO users VALUES (1, 'John Doe', 'john@example.com', 30)")
db.execute("INSERT INTO users VALUES (2, 'Jane Smith', 'jane@example.com', 25)")
db.execute("INSERT INTO products VALUES (1, 'Laptop', 999.99, 10)")
db.execute("INSERT INTO products VALUES (2, 'Mouse', 25.50, 50)")
db.execute("INSERT INTO orders VALUES (1, 1, 1, 2)")
db.execute("INSERT INTO orders VALUES (2, 2, 2, 1)")


@app.route('/')
def index():
    """
    Home page - show list of all tables.
    """
    tables = db.list_tables()
    return render_template('index.html', tables=tables)


@app.route('/create-table', methods=['GET', 'POST'])
def create_table():
    """
    Create a new table via web interface.
    """
    if request.method == 'POST':
        try:
            # Get form data
            table_name = request.form.get('table_name', '').strip()
            columns_input = request.form.get('columns', '').strip()
            
            if not table_name or not columns_input:
                flash('Table name and columns are required', 'error')
                return redirect(url_for('create_table'))
            
            # Build CREATE TABLE query
            # Expected format: "id INT PRIMARY KEY, name TEXT, email TEXT UNIQUE"
            query = f"CREATE TABLE {table_name} ({columns_input})"
            
            # Execute query
            result = db.execute(query)
            
            if result['success']:
                flash(result['message'], 'success')
                return redirect(url_for('index'))
            else:
                flash(result['message'], 'error')
        except Exception as e:
            flash(f'Error creating table: {str(e)}', 'error')
    
    return render_template('create_table.html')


@app.route('/table/<table_name>')
def view_table(table_name):
    """
    View all records in a specific table.
    
    Args:
        table_name: Name of the table to view
    """
    table = db.get_table(table_name)
    
    if not table:
        flash(f"Table '{table_name}' not found", "error")
        return redirect(url_for('index'))
    
    # Get all records
    result = table.select()
    
    return render_template(
        'view_table.html',
        table_name=table_name,
        columns=result.get('columns', []),
        rows=result.get('data', []),
        primary_key=table.primary_key
    )


@app.route('/table/<table_name>/create', methods=['GET', 'POST'])
def create_record(table_name):
    """
    Create a new record in a table.
    
    Args:
        table_name: Name of the table
    """
    table = db.get_table(table_name)
    
    if not table:
        flash(f"Table '{table_name}' not found", "error")
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Get values from form
        values = []
        for col_name, col_type in table.columns:
            value = request.form.get(col_name)
            values.append(value)
        
        # Insert into table
        result = table.insert(values)
        
        if result['success']:
            flash(result['message'], "success")
            return redirect(url_for('view_table', table_name=table_name))
        else:
            flash(result['message'], "error")
    
    return render_template(
        'create.html',
        table_name=table_name,
        columns=table.columns
    )


@app.route('/table/<table_name>/edit/<pk_value>', methods=['GET', 'POST'])
def edit_record(table_name, pk_value):
    """
    Edit an existing record.
    
    Args:
        table_name: Name of the table
        pk_value: Primary key value of the record to edit
    """
    table = db.get_table(table_name)
    
    if not table:
        flash(f"Table '{table_name}' not found", "error")
        return redirect(url_for('index'))
    
    # Convert pk_value to appropriate type
    try:
        pk_type = table.column_types[table.primary_key]
        if pk_type == 'INT':
            pk_value = int(pk_value)
    except (ValueError, KeyError):
        flash("Invalid primary key value", "error")
        return redirect(url_for('view_table', table_name=table_name))
    
    if request.method == 'POST':
        # Get updated values from form
        set_values = {}
        for col_name, col_type in table.columns:
            if col_name != table.primary_key:  # Don't update primary key
                value = request.form.get(col_name)
                set_values[col_name] = value
        
        # Update the record
        result = table.update(
            set_values=set_values,
            where={'column': table.primary_key, 'value': pk_value}
        )
        
        if result['success']:
            flash(result['message'], "success")
            return redirect(url_for('view_table', table_name=table_name))
        else:
            flash(result['message'], "error")
    
    # Get current record
    result = table.select(where={'column': table.primary_key, 'value': pk_value})
    
    if not result['data']:
        flash("Record not found", "error")
        return redirect(url_for('view_table', table_name=table_name))
    
    # Convert row data to dictionary
    current_data = {}
    for i, col_name in enumerate(result['columns']):
        current_data[col_name] = result['data'][0][i]
    
    return render_template(
        'edit.html',
        table_name=table_name,
        columns=table.columns,
        current_data=current_data,
        primary_key=table.primary_key,
        pk_value=pk_value
    )


@app.route('/table/<table_name>/delete/<pk_value>', methods=['POST'])
def delete_record(table_name, pk_value):
    """
    Delete a record from a table.
    
    Args:
        table_name: Name of the table
        pk_value: Primary key value of the record to delete
    """
    table = db.get_table(table_name)
    
    if not table:
        flash(f"Table '{table_name}' not found", "error")
        return redirect(url_for('index'))
    
    # Convert pk_value to appropriate type
    try:
        pk_type = table.column_types[table.primary_key]
        if pk_type == 'INT':
            pk_value = int(pk_value)
    except (ValueError, KeyError):
        flash("Invalid primary key value", "error")
        return redirect(url_for('view_table', table_name=table_name))
    
    # Delete the record
    result = table.delete(where={'column': table.primary_key, 'value': pk_value})
    
    if result['success']:
        flash(result['message'], "success")
    else:
        flash(result['message'], "error")
    
    return redirect(url_for('view_table', table_name=table_name))


if __name__ == '__main__':
    print("Starting SimpleDB Web Application...")
    print("Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
