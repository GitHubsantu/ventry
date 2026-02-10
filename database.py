"""
Database Manager for Ventry Inventory Management System
Handles all SQLite database operations with proper transaction management
"""

import sqlite3
from datetime import datetime
from typing import List, Tuple, Optional


class DatabaseManager:
    """Manages all database operations for the inventory system"""
    
    def __init__(self, db_path: str = "ventry.db"):
        """Initialize database connection and create tables if needed"""
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establish database connection"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row  # Enable column access by name
        self.cursor = self.connection.cursor()
    
    def create_tables(self):
        """Create all required tables if they don't exist"""
        
        # Items table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL UNIQUE,
                current_stock REAL DEFAULT 0,
                purchase_price REAL DEFAULT 0,
                sale_price REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Purchases table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_no TEXT NOT NULL,
                date TEXT NOT NULL,
                item_id INTEGER NOT NULL,
                quantity REAL NOT NULL,
                rate REAL NOT NULL,
                total REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (item_id) REFERENCES items(id)
            )
        """)
        
        # Sales table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bill_no TEXT NOT NULL,
                date TEXT NOT NULL,
                item_id INTEGER NOT NULL,
                quantity REAL NOT NULL,
                rate REAL NOT NULL,
                total REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (item_id) REFERENCES items(id)
            )
        """)
        
        # Stock log table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                change_qty REAL NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('purchase', 'sale')),
                date TEXT NOT NULL,
                bill_no TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (item_id) REFERENCES items(id)
            )
        """)
        
        self.connection.commit()
    
    # ==================== ITEM OPERATIONS ====================
    
    def add_item(self, item_name: str, purchase_price: float = 0, 
                 sale_price: float = 0) -> bool:
        """Add a new item to inventory"""
        try:
            self.cursor.execute("""
                INSERT INTO items (item_name, purchase_price, sale_price)
                VALUES (?, ?, ?)
            """, (item_name, purchase_price, sale_price))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False  # Item already exists
    
    def update_item(self, item_id: int, item_name: str, 
                    purchase_price: float, sale_price: float) -> bool:
        """Update an existing item"""
        try:
            self.cursor.execute("""
                UPDATE items 
                SET item_name = ?, purchase_price = ?, sale_price = ?
                WHERE id = ?
            """, (item_name, purchase_price, sale_price, item_id))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def delete_item(self, item_id: int) -> bool:
        """Delete an item (only if no transactions exist)"""
        try:
            # Check if item has any transactions
            self.cursor.execute("""
                SELECT COUNT(*) FROM purchases WHERE item_id = ?
            """, (item_id,))
            purchase_count = self.cursor.fetchone()[0]
            
            self.cursor.execute("""
                SELECT COUNT(*) FROM sales WHERE item_id = ?
            """, (item_id,))
            sale_count = self.cursor.fetchone()[0]
            
            if purchase_count > 0 or sale_count > 0:
                return False  # Cannot delete item with transactions
            
            self.cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
            self.connection.commit()
            return True
        except:
            return False
    
    def get_all_items(self) -> List[Tuple]:
        """Get all items with calculated purchased and sold quantities"""
        self.cursor.execute("""
            SELECT 
                i.id,
                i.item_name,
                COALESCE(SUM(p.quantity), 0) as purchased_qty,
                COALESCE(SUM(s.quantity), 0) as sold_qty,
                i.current_stock,
                i.purchase_price,
                i.sale_price,
                i.created_at
            FROM items i
            LEFT JOIN purchases p ON i.id = p.item_id
            LEFT JOIN sales s ON i.id = s.item_id
            GROUP BY i.id
            ORDER BY i.item_name
        """)
        return self.cursor.fetchall()
    
    def get_item_by_id(self, item_id: int) -> Optional[sqlite3.Row]:
        """Get a single item by ID"""
        self.cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        return self.cursor.fetchone()
    
    def search_items(self, search_term: str) -> List[Tuple]:
        """Search items by name"""
        self.cursor.execute("""
            SELECT 
                i.id,
                i.item_name,
                COALESCE(SUM(p.quantity), 0) as purchased_qty,
                COALESCE(SUM(s.quantity), 0) as sold_qty,
                i.current_stock,
                i.purchase_price,
                i.sale_price,
                i.created_at
            FROM items i
            LEFT JOIN purchases p ON i.id = p.item_id
            LEFT JOIN sales s ON i.id = s.item_id
            WHERE i.item_name LIKE ?
            GROUP BY i.id
            ORDER BY i.item_name
        """, (f"%{search_term}%",))
        return self.cursor.fetchall()
    
    # ==================== PURCHASE OPERATIONS ====================
    
    def add_purchase(self, bill_no: str, date: str, item_id: int, 
                     quantity: float, rate: float) -> bool:
        """Add a purchase transaction and update stock"""
        try:
            self.connection.execute("BEGIN TRANSACTION")
            
            total = quantity * rate
            
            # Insert purchase record
            self.cursor.execute("""
                INSERT INTO purchases (bill_no, date, item_id, quantity, rate, total)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (bill_no, date, item_id, quantity, rate, total))
            
            # Update item stock
            self.cursor.execute("""
                UPDATE items 
                SET current_stock = current_stock + ?,
                    purchase_price = ?
                WHERE id = ?
            """, (quantity, rate, item_id))
            
            # Log stock change
            self.cursor.execute("""
                INSERT INTO stock_log (item_id, change_qty, type, date, bill_no)
                VALUES (?, ?, 'purchase', ?, ?)
            """, (item_id, quantity, date, bill_no))
            
            self.connection.commit()
            return True
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding purchase: {e}")
            return False
    
    def get_last_purchase_bill_no(self) -> str:
        """Get the last purchase bill number"""
        self.cursor.execute("""
            SELECT bill_no FROM purchases 
            ORDER BY id DESC LIMIT 1
        """)
        result = self.cursor.fetchone()
        return result[0] if result else "P0000"
    
    # ==================== SALE OPERATIONS ====================
    
    def add_sale(self, bill_no: str, date: str, item_id: int, 
                 quantity: float, rate: float) -> Tuple[bool, str]:
        """
        Add a sale transaction and update stock
        Returns: (success, error_message)
        """
        try:
            self.connection.execute("BEGIN TRANSACTION")
            
            # Check available stock
            self.cursor.execute("""
                SELECT current_stock FROM items WHERE id = ?
            """, (item_id,))
            result = self.cursor.fetchone()
            
            if not result:
                self.connection.rollback()
                return False, "Item not found"
            
            current_stock = result[0]
            if current_stock < quantity:
                self.connection.rollback()
                return False, f"Insufficient stock! Available: {current_stock}"
            
            total = quantity * rate
            
            # Insert sale record
            self.cursor.execute("""
                INSERT INTO sales (bill_no, date, item_id, quantity, rate, total)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (bill_no, date, item_id, quantity, rate, total))
            
            # Update item stock
            self.cursor.execute("""
                UPDATE items 
                SET current_stock = current_stock - ?,
                    sale_price = ?
                WHERE id = ?
            """, (quantity, rate, item_id))
            
            # Log stock change
            self.cursor.execute("""
                INSERT INTO stock_log (item_id, change_qty, type, date, bill_no)
                VALUES (?, ?, 'sale', ?, ?)
            """, (item_id, -quantity, date, bill_no))
            
            self.connection.commit()
            return True, "Success"
        except Exception as e:
            self.connection.rollback()
            print(f"Error adding sale: {e}")
            return False, str(e)
    
    def get_last_sale_bill_no(self) -> str:
        """Get the last sale bill number"""
        self.cursor.execute("""
            SELECT bill_no FROM sales 
            ORDER BY id DESC LIMIT 1
        """)
        result = self.cursor.fetchone()
        return result[0] if result else "S0000"
    
    # ==================== UTILITY OPERATIONS ====================
    
    def get_next_bill_no(self, prefix: str, last_bill: str) -> str:
        """Generate next bill number"""
        try:
            # Extract number from last bill (e.g., "P0001" -> 1)
            if last_bill and len(last_bill) > 1:
                number = int(last_bill[1:])
                return f"{prefix}{number + 1:04d}"
            else:
                return f"{prefix}0001"
        except:
            return f"{prefix}0001"
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()