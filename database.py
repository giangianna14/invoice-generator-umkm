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
    
    def check_product_exists(self, name):
        """Check if product with same name already exists"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, price FROM products 
            WHERE LOWER(name) = LOWER(?)
        ''', (name,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'exists': True,
                'id': result[0],
                'name': result[1],
                'price': result[2]
            }
        else:
            return {'exists': False}
    
    def add_product(self, name, price, description=""):
        """Add new product with duplicate checking"""
        # Check if product already exists
        existing = self.check_product_exists(name)
        if existing['exists']:
            return {
                'success': False,
                'message': f"Produk '{name}' sudah ada di database dengan harga Rp {existing['price']:,.0f}",
                'existing_product': existing
            }
        
        # Add new product
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO products (name, price, description)
                VALUES (?, ?, ?)
            ''', (name, price, description))
            
            product_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'message': f"Produk '{name}' berhasil disimpan ke master data!",
                'product_id': product_id
            }
        except Exception as e:
            conn.rollback()
            conn.close()
            return {
                'success': False,
                'message': f"Error menyimpan produk: {str(e)}"
            }
    
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
    
    def update_customer(self, customer_id, name, email="", phone="", address=""):
        """Update existing customer"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE customers 
                SET name = ?, email = ?, phone = ?, address = ?
                WHERE id = ?
            ''', (name, email, phone, address, customer_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                conn.close()
                return {
                    'success': True,
                    'message': f"Customer '{name}' berhasil diupdate!"
                }
            else:
                conn.close()
                return {
                    'success': False,
                    'message': "Customer tidak ditemukan"
                }
        except Exception as e:
            conn.rollback()
            conn.close()
            return {
                'success': False,
                'message': f"Error updating customer: {str(e)}"
            }
    
    def delete_customer(self, customer_id):
        """Delete customer if not used in invoices"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            # Check if customer is used in invoices
            cursor.execute('SELECT COUNT(*) FROM invoices WHERE customer_id = ?', (customer_id,))
            invoice_count = cursor.fetchone()[0]
            
            if invoice_count > 0:
                conn.close()
                return {
                    'success': False,
                    'message': f"Customer tidak dapat dihapus karena sudah digunakan dalam {invoice_count} invoice"
                }
            
            # Get customer name for message
            cursor.execute('SELECT name FROM customers WHERE id = ?', (customer_id,))
            result = cursor.fetchone()
            if not result:
                conn.close()
                return {
                    'success': False,
                    'message': "Customer tidak ditemukan"
                }
            
            customer_name = result[0]
            
            # Delete customer
            cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'message': f"Customer '{customer_name}' berhasil dihapus!"
            }
            
        except Exception as e:
            conn.rollback()
            conn.close()
            return {
                'success': False,
                'message': f"Error deleting customer: {str(e)}"
            }
    
    def get_customer_by_id(self, customer_id):
        """Get customer details by ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'name': result[1],
                'email': result[2],
                'phone': result[3],
                'address': result[4],
                'created_at': result[5]
            }
        return None
    
    def update_product(self, product_id, name, price, description=""):
        """Update existing product"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                UPDATE products 
                SET name = ?, price = ?, description = ?
                WHERE id = ?
            ''', (name, price, description, product_id))
            
            if cursor.rowcount > 0:
                conn.commit()
                conn.close()
                return {
                    'success': True,
                    'message': f"Produk '{name}' berhasil diupdate!"
                }
            else:
                conn.close()
                return {
                    'success': False,
                    'message': "Produk tidak ditemukan"
                }
        except Exception as e:
            conn.rollback()
            conn.close()
            return {
                'success': False,
                'message': f"Error updating product: {str(e)}"
            }
    
    def delete_product(self, product_id):
        """Delete product if not used in invoices"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            # Get product name first
            cursor.execute('SELECT name FROM products WHERE id = ?', (product_id,))
            result = cursor.fetchone()
            if not result:
                conn.close()
                return {
                    'success': False,
                    'message': "Produk tidak ditemukan"
                }
            
            product_name = result[0]
            
            # Check if product is used in invoice items (by name matching)
            cursor.execute('SELECT COUNT(*) FROM invoice_items WHERE product_name = ?', (product_name,))
            usage_count = cursor.fetchone()[0]
            
            if usage_count > 0:
                conn.close()
                return {
                    'success': False,
                    'message': f"Produk '{product_name}' tidak dapat dihapus karena sudah digunakan dalam {usage_count} invoice"
                }
            
            # Delete product
            cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
            conn.commit()
            conn.close()
            
            return {
                'success': True,
                'message': f"Produk '{product_name}' berhasil dihapus!"
            }
            
        except Exception as e:
            conn.rollback()
            conn.close()
            return {
                'success': False,
                'message': f"Error deleting product: {str(e)}"
            }
    
    def get_product_by_id(self, product_id):
        """Get product details by ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'name': result[1],
                'price': result[2],
                'description': result[3],
                'created_at': result[4]
            }
        return None