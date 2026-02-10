"""
Sample Data Generator for Ventry
Creates sample inventory items and transactions for testing
"""

from database import DatabaseManager
from datetime import datetime, timedelta
import random


def generate_sample_data():
    """Generate sample inventory data for testing"""
    
    print("=" * 60)
    print("Ventry - Sample Data Generator")
    print("=" * 60)
    print()
    
    # Connect to database
    db = DatabaseManager()
    
    # Sample items
    items = [
        ("Laptop Dell Inspiron", 45000, 52000),
        ("Mouse Logitech Wireless", 800, 1200),
        ("Keyboard Mechanical", 2500, 3500),
        ("Monitor 24 inch LED", 8000, 10500),
        ("USB Cable Type-C", 150, 250),
        ("Headphones Sony", 1500, 2200),
        ("Webcam HD 1080p", 2800, 3800),
        ("External HDD 1TB", 3500, 4500),
        ("Printer HP LaserJet", 12000, 15000),
        ("Router WiFi Dual Band", 1800, 2500),
    ]
    
    print("Adding sample items...")
    item_ids = []
    for item_name, purchase_price, sale_price in items:
        if db.add_item(item_name, purchase_price, sale_price):
            # Get the item ID
            all_items = db.get_all_items()
            for item in all_items:
                if item[1] == item_name:
                    item_ids.append(item[0])
                    print(f"  ✓ Added: {item_name}")
                    break
    
    print(f"\nAdded {len(item_ids)} items successfully!")
    
    # Generate sample purchases
    print("\nGenerating sample purchases...")
    purchase_count = 0
    base_date = datetime.now() - timedelta(days=30)
    
    for i, item_id in enumerate(item_ids):
        # Get item details
        item = db.get_item_by_id(item_id)
        
        # Random number of purchases (1-3 per item)
        num_purchases = random.randint(1, 3)
        
        for p in range(num_purchases):
            bill_no = f"P{purchase_count + 1:04d}"
            date = (base_date + timedelta(days=random.randint(0, 25))).strftime("%Y-%m-%d")
            quantity = random.randint(5, 20)
            rate = item['purchase_price']
            
            if db.add_purchase(bill_no, date, item_id, quantity, rate):
                purchase_count += 1
    
    print(f"  ✓ Generated {purchase_count} purchase transactions")
    
    # Generate sample sales
    print("\nGenerating sample sales...")
    sale_count = 0
    
    for i, item_id in enumerate(item_ids):
        # Get item details
        item = db.get_item_by_id(item_id)
        
        # Check current stock
        if item['current_stock'] > 0:
            # Random number of sales (1-2 per item)
            num_sales = random.randint(1, 2)
            
            for s in range(num_sales):
                # Ensure we don't oversell
                available_stock = db.get_item_by_id(item_id)['current_stock']
                if available_stock > 0:
                    bill_no = f"S{sale_count + 1:04d}"
                    date = (base_date + timedelta(days=random.randint(5, 30))).strftime("%Y-%m-%d")
                    quantity = min(random.randint(1, 10), available_stock)
                    rate = item['sale_price']
                    
                    success, message = db.add_sale(bill_no, date, item_id, quantity, rate)
                    if success:
                        sale_count += 1
    
    print(f"  ✓ Generated {sale_count} sale transactions")
    
    # Display summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total Items Created: {len(item_ids)}")
    print(f"Total Purchases: {purchase_count}")
    print(f"Total Sales: {sale_count}")
    print()
    
    # Display current stock levels
    print("Current Stock Levels:")
    print("-" * 60)
    all_items = db.get_all_items()
    for item in all_items:
        print(f"  {item[1]:<30} Stock: {item[4]:>6.0f} units")
    
    print("\n" + "=" * 60)
    print("Sample data generated successfully!")
    print("You can now launch the Ventry application to see the data.")
    print("=" * 60)
    
    db.close()


if __name__ == "__main__":
    response = input("This will create sample data in your database. Continue? (y/n): ")
    if response.lower() == 'y':
        generate_sample_data()
    else:
        print("Cancelled.")
