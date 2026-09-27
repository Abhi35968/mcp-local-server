import random
from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

mcp= FastMCP(name="Demo Server")

def init_db():
    """Initialize the database and create the expenses table if it doesn't exist."""
    with sqlite3.connect(DB_PATH) as cnn:
        cnn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )    
        """)

init_db()

@mcp.tool
def add_expense(date, amount, category, subcategory='', note=''):
    """Add a new expense to the database."""
    with sqlite3.connect(DB_PATH) as cnn:
        cnn.execute(
            "INSERT INTO expenses (date, amount, category, subcategory, note) VALUES (?, ?, ?, ?, ?)",
            (date, amount, category, subcategory, note)
        )
        return {"status": "success", "message": "Expense added successfully."}

@mcp.tool
def list_expenses(start_date, end_date):
    """List all expenses in the database."""
    with sqlite3.connect(DB_PATH) as cnn:
        curr=cnn.execute("SELECT id, date, amount, category, subcategory, note FROM expenses WHERE date BETWEEN ? AND ? ORDER BY id ASC", (start_date, end_date))
        cols= [d[0] for d in curr.description]
        return [dict(zip(cols, row)) for row in curr.fetchall()]
    
@mcp.tool
def summerize(start_date, end_date,category=None):
    """Summarize expenses by category and subcategory."""
    with sqlite3.connect(DB_PATH) as cnn:
        query = (
            """
            SELECT category,SUM(amount) as total_amount FROM expenses WHERE date BETWEEN ? AND ?
            """
        )
        params = [start_date, end_date]
        if category:
            query += " AND category = ?"
            params.append(category)
        query += " GROUP BY category ORDER BY category ASC"
        
        curr=cnn.execute(query, params)
        cols= [d[0] for d in curr.description]
        return [dict(zip(cols, row)) for row in curr.fetchall()]
@mcp.resource("config://categories")
def categories():
    #Read fresh each time so you can edit the file without restarting
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()
    
    
def main() -> None:
    mcp.run(transport="http", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()