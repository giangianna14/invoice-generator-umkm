import sqlite3
import pandas as pd
from datetime import datetime
import os

class Database:
    def __init__(self, db_name="invoice_system.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Invoices table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT UNIQUE NOT NULL,
                customer_id INTEGER,
                issue_date DATE,
                due_date DATE,
                subtotal REAL,
                tax_rate REAL DEFAULT 0,
                tax_amount REAL,
                total REAL,
                status TEXT DEFAULT 'Draft',
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (customer_id) REFERENCES customers (id)
            )
        ''')
        
        # Invoice items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS invoice_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_id INTEGER,
                product_name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_price REAL NOT NULL,
                FOREIGN KEY (invoice_id) REFERENCES invoices (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_customer(self, name, email="", phone="", address=""):
        """Add new customer"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO customers (name, email, phone, address)
            VALUES (?, ?, ?, ?)
        ''', (name, email, phone, address))
        
        customer_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return customer_id
    
    def get_customers(self):
        """Get all customers"""
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query("SELECT * FROM customers ORDER BY name", conn)
        conn.close()
        return df
    
    def add_product(self, name, price, description=""):
        """Add new product"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO products (name, price, description)
            VALUES (?, ?, ?)
        ''', (name, price, description))
        
        product_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return product_id
    
    def get_products(self):
        """Get all products"""
        conn = sqlite3.connect(self.db_name)
        df = pd.read_sql_query("SELECT * FROM products ORDER BY name", conn)
        conn.close()
        return df
    
    def create_invoice(self, customer_id, items, issue_date, due_date, 
                      tax_rate=0.11, notes=""):
        """Create new invoice with items"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Generate invoice number
        invoice_number = f"INV-{datetime.now().strftime('%Y%m%d')}-{datetime.now().strftime('%H%M%S')}"
        
        # Calculate totals
        subtotal = sum(item['quantity'] * item['unit_price'] for item in items)
        tax_amount = subtotal * tax_rate
        total = subtotal + tax_amount
        
        # Insert invoice
        cursor.execute('''
            INSERT INTO invoices (invoice_number, customer_id, issue_date, due_date,
                                subtotal, tax_rate, tax_amount, total, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (invoice_number, customer_id, issue_date, due_date, 
              subtotal, tax_rate, tax_amount, total, notes))
        
        invoice_id = cursor.lastrowid
        
        # Insert invoice items
        for item in items:
            total_price = item['quantity'] * item['unit_price']
            cursor.execute('''
                INSERT INTO invoice_items (invoice_id, product_name, quantity, unit_price, total_price)
                VALUES (?, ?, ?, ?, ?)
            ''', (invoice_id, item['product_name'], item['quantity'], 
                  item['unit_price'], total_price))
        
        conn.commit()
        conn.close()
        return invoice_id, invoice_number
    
    def get_invoices(self):
        """Get all invoices with customer info"""
        conn = sqlite3.connect(self.db_name)
        query = '''
            SELECT i.*, c.name as customer_name 
            FROM invoices i
            LEFT JOIN customers c ON i.customer_id = c.id
            ORDER BY i.created_at DESC
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_invoice_details(self, invoice_id):
        """Get invoice with items and customer details"""
        conn = sqlite3.connect(self.db_name)
        
        # Get invoice info
        invoice_query = '''
            SELECT i.*, c.name as customer_name, c.email, c.phone, c.address
            FROM invoices i
            LEFT JOIN customers c ON i.customer_id = c.id
            WHERE i.id = ?
        '''
        invoice_df = pd.read_sql_query(invoice_query, conn, params=(invoice_id,))
        
        # Get invoice items
        items_query = '''
            SELECT * FROM invoice_items WHERE invoice_id = ?
        '''
        items_df = pd.read_sql_query(items_query, conn, params=(invoice_id,))
        
        conn.close()
        return invoice_df.iloc[0] if len(invoice_df) > 0 else None, items_df
    
    def get_sales_summary(self, start_date=None, end_date=None):
        """Get sales summary for reporting"""
        conn = sqlite3.connect(self.db_name)
        
        query = '''
            SELECT 
                DATE(issue_date) as date,
                COUNT(*) as invoice_count,
                SUM(total) as total_sales,
                SUM(tax_amount) as total_tax
            FROM invoices
            WHERE 1=1
        '''
        
        params = []
        if start_date:
            query += " AND issue_date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND issue_date <= ?"
            params.append(end_date)
            
        query += " GROUP BY DATE(issue_date) ORDER BY date DESC"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df