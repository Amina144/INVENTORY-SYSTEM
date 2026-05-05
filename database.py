import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            quantity INTEGER DEFAULT 0,
            price REAL DEFAULT 0.0
        )
    ''')
    conn.commit()
    conn.close()

def add_item(name, category, quantity, price):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('INSERT INTO items (name, category, quantity, price) VALUES (?, ?, ?, ?)',
              (name, category, quantity, price))
    conn.commit()
    conn.close()

def get_items():
    conn = sqlite3.connect('inventory.db')
    df = pd.read_sql_query('SELECT * FROM items', conn)
    conn.close()
    return df

def update_item(item_id, name, category, quantity, price):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('''
        UPDATE items
        SET name = ?, category = ?, quantity = ?, price = ?
        WHERE id = ?
    ''', (name, category, quantity, price, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = sqlite3.connect('inventory.db')
    c = conn.cursor()
    c.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
