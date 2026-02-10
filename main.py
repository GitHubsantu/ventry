"""
Main Application Window for Ventry Inventory Management System
Modern PyQt5 desktop application with Excel-inspired layout
"""

import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel, QLineEdit,
    QComboBox, QDateEdit, QMessageBox, QDialog, QFormLayout,
    QDialogButtonBox, QHeaderView, QTabWidget, QAction, QFileDialog,
    QMenuBar, QMenu, QStatusBar, QTextBrowser
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QIcon, QFont, QPixmap
from database import DatabaseManager
import csv
from datetime import datetime


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


class VentryMainWindow(QMainWindow):
    """Main application window with tabbed interface"""
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.dark_mode = False
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Ventry – Inventory Manager")
        self.setGeometry(100, 100, 1200, 700)
        
        # Set application icon - use resource_path for PyInstaller
        icon_path = resource_path("assets/ventry_icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Add tabs
        self.stock_tab = StockItemScreen(self.db)
        self.entry_tab = EntryScreen(self.db, self.stock_tab)
        self.bills_tab = BillsViewScreen(self.db)
        
        self.tabs.addTab(self.stock_tab, "📦 Stock Items")
        self.tabs.addTab(self.entry_tab, "📝 Transactions")
        self.tabs.addTab(self.bills_tab, "📄 View Bills")
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Apply default stylesheet
        self.apply_light_mode()
        
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("&File")
        
        export_action = QAction("Export to CSV", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.export_to_csv)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu("&View")
        
        dark_mode_action = QAction("Toggle Dark Mode", self)
        dark_mode_action.setShortcut("Ctrl+D")
        dark_mode_action.triggered.connect(self.toggle_dark_mode)
        view_menu.addAction(dark_mode_action)
        
        refresh_action = QAction("Refresh", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.refresh_all)
        view_menu.addAction(refresh_action)
        
        # Help menu
        help_menu = menubar.addMenu("&Help")
        
        about_action = QAction("About Ventry", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def export_to_csv(self):
        """Export current stock data to CSV"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export to CSV", "ventry_stock.csv", "CSV Files (*.csv)"
        )
        
        if filename:
            try:
                items = self.db.get_all_items()
                with open(filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([
                        "Item Name", "Purchased Qty", "Sold Qty", 
                        "Current Stock", "Purchase Price", "Sale Price", "Created Date"
                    ])
                    for item in items:
                        writer.writerow([
                            item[1], item[2], item[3], 
                            item[4], item[5], item[6], item[7]
                        ])
                QMessageBox.information(self, "Success", "Data exported successfully!")
                self.status_bar.showMessage(f"Exported to {filename}", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
    
    def toggle_dark_mode(self):
        """Toggle between light and dark mode"""
        self.dark_mode = not self.dark_mode
        if self.dark_mode:
            self.apply_dark_mode()
        else:
            self.apply_light_mode()
    
    def apply_light_mode(self):
        """Apply light mode stylesheet"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                color: #333333;
                padding: 8px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #1976D2;
                font-weight: bold;
            }
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QTableWidget {
                background-color: white;
                gridline-color: #e0e0e0;
                border: 1px solid #cccccc;
            }
            QHeaderView::section {
                background-color: #1976D2;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 6px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #1976D2;
            }
        """)
    
    def apply_dark_mode(self):
        """Apply dark mode stylesheet"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #e0e0e0;
            }
            QTabWidget::pane {
                border: 1px solid #3a3a3a;
                background-color: #2b2b2b;
            }
            QTabBar::tab {
                background-color: #3a3a3a;
                color: #e0e0e0;
                padding: 8px 20px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #2b2b2b;
                color: #64B5F6;
                font-weight: bold;
            }
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2196F3;
            }
            QTableWidget {
                background-color: #2b2b2b;
                color: #e0e0e0;
                gridline-color: #3a3a3a;
                border: 1px solid #3a3a3a;
            }
            QHeaderView::section {
                background-color: #1976D2;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QLineEdit, QComboBox, QDateEdit {
                padding: 6px;
                border: 1px solid #3a3a3a;
                border-radius: 4px;
                background-color: #2b2b2b;
                color: #e0e0e0;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus {
                border: 2px solid #1976D2;
            }
            QLabel {
                color: #e0e0e0;
            }
            QTextBrowser {
                background-color: #2b2b2b;
                color: #e0e0e0;
                border: 1px solid #3a3a3a;
            }
        """)
    
    def refresh_all(self):
        """Refresh all data in the application"""
        self.stock_tab.load_items()
        self.bills_tab.load_bills()
        self.status_bar.showMessage("Data refreshed", 2000)
    
    def show_about(self):
        """Show about dialog"""
        about_text = """
        <div style='text-align: center;'>
            <h2>Ventry – Inventory Manager</h2>
            <p><b>Version 1.0</b></p>
            <p>A modern desktop inventory management system</p>
            <p>Built with Python and PyQt5</p>
            <br>
            <p>© 2026 Ventry. All rights reserved.</p>
            <br>
            <p><b>GitHub:</b> <a href='https://github.com/githubsantu'>github.com/githubsantu</a></p>
            <p><b>Website:</b> <a href='https://imdevops.in'>imdevops.in</a></p>
        </div>
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle("About Ventry")
        msg.setTextFormat(Qt.RichText)
        msg.setText(about_text)
        msg.setStandardButtons(QMessageBox.Ok)
        
        # Add logo if it exists - use resource_path for PyInstaller
        logo_path = resource_path("assets/ventry_icon.png")
        if os.path.exists(logo_path):
            pixmap = QPixmap(logo_path)
            msg.setIconPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        msg.exec_()
    
    def closeEvent(self, event):
        """Handle application close event"""
        self.db.close()
        event.accept()


class StockItemScreen(QWidget):
    """Stock items management screen"""
    
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_items()
    
    def init_ui(self):
        """Initialize stock items UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Type to search items...")
        self.search_input.textChanged.connect(self.search_items)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addStretch()
        layout.addLayout(search_layout)
        
        # Table widget
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Item Name", "Purchased Qty", "Sold Qty", 
            "Current Stock", "Purchase Price", "Sale Price", "Created Date", "ID"
        ])
        self.table.hideColumn(7)  # Hide ID column
        
        # Make table read-only
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Auto-resize columns
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        for i in range(1, 7):
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("➕ Add Item")
        self.add_btn.clicked.connect(self.add_item)
        
        self.edit_btn = QPushButton("✏️ Edit Item")
        self.edit_btn.clicked.connect(self.edit_item)
        
        self.delete_btn = QPushButton("🗑️ Delete Item")
        self.delete_btn.clicked.connect(self.delete_item)
        
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.load_items)
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(button_layout)
    
    def load_items(self):
        """Load all items into the table"""
        items = self.db.get_all_items()
        self.populate_table(items)
    
    def populate_table(self, items):
        """Populate table with item data"""
        self.table.setRowCount(len(items))
        
        for row, item in enumerate(items):
            self.table.setItem(row, 0, QTableWidgetItem(item[1]))  # Name
            self.table.setItem(row, 1, QTableWidgetItem(f"{item[2]:.2f}"))  # Purchased
            self.table.setItem(row, 2, QTableWidgetItem(f"{item[3]:.2f}"))  # Sold
            self.table.setItem(row, 3, QTableWidgetItem(f"{item[4]:.2f}"))  # Stock
            self.table.setItem(row, 4, QTableWidgetItem(f"₹{item[5]:.2f}"))  # Purchase price
            self.table.setItem(row, 5, QTableWidgetItem(f"₹{item[6]:.2f}"))  # Sale price
            
            # Format created date
            created_date = item[7] if len(item) > 7 else ""
            if created_date:
                try:
                    # Parse the datetime and format it nicely
                    date_obj = datetime.fromisoformat(created_date)
                    formatted_date = date_obj.strftime("%Y-%m-%d %H:%M")
                except:
                    formatted_date = created_date
            else:
                formatted_date = "N/A"
            
            self.table.setItem(row, 6, QTableWidgetItem(formatted_date))  # Created date
            self.table.setItem(row, 7, QTableWidgetItem(str(item[0])))  # ID
            
            # Center align numeric columns
            for col in range(1, 7):
                self.table.item(row, col).setTextAlignment(Qt.AlignCenter)
    
    def search_items(self, text):
        """Search items by name"""
        if text:
            items = self.db.search_items(text)
        else:
            items = self.db.get_all_items()
        self.populate_table(items)
    
    def add_item(self):
        """Open dialog to add new item"""
        dialog = ItemDialog(self)
        if dialog.exec_():
            data = dialog.get_data()
            if self.db.add_item(data['name'], data['purchase_price'], data['sale_price']):
                QMessageBox.information(self, "Success", "Item added successfully!")
                self.load_items()
            else:
                QMessageBox.warning(self, "Error", "Item already exists or invalid data!")
    
    def edit_item(self):
        """Open dialog to edit selected item"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select an item to edit!")
            return
        
        item_id = int(self.table.item(current_row, 7).text())
        item = self.db.get_item_by_id(item_id)
        
        dialog = ItemDialog(self, item)
        if dialog.exec_():
            data = dialog.get_data()
            if self.db.update_item(item_id, data['name'], 
                                  data['purchase_price'], data['sale_price']):
                QMessageBox.information(self, "Success", "Item updated successfully!")
                self.load_items()
            else:
                QMessageBox.warning(self, "Error", "Failed to update item!")
    
    def delete_item(self):
        """Delete selected item"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select an item to delete!")
            return
        
        item_name = self.table.item(current_row, 0).text()
        item_id = int(self.table.item(current_row, 7).text())
        
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete '{item_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.db.delete_item(item_id):
                QMessageBox.information(self, "Success", "Item deleted successfully!")
                self.load_items()
            else:
                QMessageBox.warning(
                    self, "Error",
                    "Cannot delete item with existing transactions!"
                )


class ItemDialog(QDialog):
    """Dialog for adding/editing items"""
    
    def __init__(self, parent=None, item=None):
        super().__init__(parent)
        self.item = item
        self.init_ui()
        
        if item:
            self.setWindowTitle("Edit Item")
            self.name_input.setText(item['item_name'])
            self.purchase_price_input.setText(str(item['purchase_price']))
            self.sale_price_input.setText(str(item['sale_price']))
        else:
            self.setWindowTitle("Add New Item")
    
    def init_ui(self):
        """Initialize item dialog UI"""
        layout = QFormLayout()
        self.setLayout(layout)
        
        # Input fields
        self.name_input = QLineEdit()
        self.purchase_price_input = QLineEdit()
        self.purchase_price_input.setText("0.00")
        self.sale_price_input = QLineEdit()
        self.sale_price_input.setText("0.00")
        
        layout.addRow("Item Name:", self.name_input)
        layout.addRow("Purchase Price:", self.purchase_price_input)
        layout.addRow("Sale Price:", self.sale_price_input)
        
        # Buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
        self.resize(400, 150)
    
    def validate_and_accept(self):
        """Validate input before accepting"""
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Warning", "Item name cannot be empty!")
            return
        
        try:
            float(self.purchase_price_input.text())
            float(self.sale_price_input.text())
        except ValueError:
            QMessageBox.warning(self, "Warning", "Prices must be valid numbers!")
            return
        
        self.accept()
    
    def get_data(self):
        """Return dialog data"""
        return {
            'name': self.name_input.text().strip(),
            'purchase_price': float(self.purchase_price_input.text()),
            'sale_price': float(self.sale_price_input.text())
        }


class BillsViewScreen(QWidget):
    """Screen to view and search all bills (purchases and sales)"""
    
    def __init__(self, db: DatabaseManager):
        super().__init__()
        self.db = db
        self.init_ui()
        self.load_bills()
    
    def init_ui(self):
        """Initialize bills view UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Filter controls
        filter_layout = QHBoxLayout()
        
        # Bill type filter
        filter_layout.addWidget(QLabel("Bill Type:"))
        self.type_filter = QComboBox()
        self.type_filter.addItems(["All Bills", "Purchases Only", "Sales Only"])
        self.type_filter.currentIndexChanged.connect(self.load_bills)
        filter_layout.addWidget(self.type_filter)
        
        # Search by bill number
        filter_layout.addWidget(QLabel("Search Bill No:"))
        self.bill_search = QLineEdit()
        self.bill_search.setPlaceholderText("Enter bill number...")
        self.bill_search.textChanged.connect(self.load_bills)
        filter_layout.addWidget(self.bill_search)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Table widget
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Bill No", "Type", "Date", "Item Name", "Quantity", "Rate", "Total"
        ])
        
        # Make table read-only
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Auto-resize columns
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(3, QHeaderView.Stretch)
        for i in [0, 1, 2, 4, 5, 6]:
            header.setSectionResizeMode(i, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.table)
        
        # Summary label
        self.summary_label = QLabel()
        self.summary_label.setFont(QFont("Arial", 10, QFont.Bold))
        layout.addWidget(self.summary_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.load_bills)
        
        self.export_btn = QPushButton("📥 Export to CSV")
        self.export_btn.clicked.connect(self.export_bills)
        
        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.export_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
    
    def load_bills(self):
        """Load bills based on filters"""
        bill_type = self.type_filter.currentText()
        search_term = self.bill_search.text().strip()
        
        # Get purchases
        purchases = []
        if bill_type in ["All Bills", "Purchases Only"]:
            self.db.cursor.execute("""
                SELECT p.bill_no, p.date, i.item_name, p.quantity, p.rate, p.total
                FROM purchases p
                JOIN items i ON p.item_id = i.id
                WHERE p.bill_no LIKE ?
                ORDER BY p.date DESC, p.id DESC
            """, (f"%{search_term}%",))
            purchases = [("P", *row) for row in self.db.cursor.fetchall()]
        
        # Get sales
        sales = []
        if bill_type in ["All Bills", "Sales Only"]:
            self.db.cursor.execute("""
                SELECT s.bill_no, s.date, i.item_name, s.quantity, s.rate, s.total
                FROM sales s
                JOIN items i ON s.item_id = i.id
                WHERE s.bill_no LIKE ?
                ORDER BY s.date DESC, s.id DESC
            """, (f"%{search_term}%",))
            sales = [("S", *row) for row in self.db.cursor.fetchall()]
        
        # Combine and sort
        all_bills = purchases + sales
        all_bills.sort(key=lambda x: x[2], reverse=True)  # Sort by date
        
        self.populate_table(all_bills)
        self.update_summary(purchases, sales)
    
    def populate_table(self, bills):
        """Populate table with bill data"""
        self.table.setRowCount(len(bills))
        
        for row, bill in enumerate(bills):
            bill_type, bill_no, date, item_name, quantity, rate, total = bill
            
            # Bill number
            self.table.setItem(row, 0, QTableWidgetItem(bill_no))
            
            # Type with color
            type_item = QTableWidgetItem("Purchase" if bill_type == "P" else "Sale")
            if bill_type == "P":
                type_item.setForeground(Qt.darkGreen)
            else:
                type_item.setForeground(Qt.darkRed)
            self.table.setItem(row, 1, type_item)
            
            # Date
            self.table.setItem(row, 2, QTableWidgetItem(date))
            
            # Item name
            self.table.setItem(row, 3, QTableWidgetItem(item_name))
            
            # Quantity
            self.table.setItem(row, 4, QTableWidgetItem(f"{quantity:.2f}"))
            
            # Rate
            self.table.setItem(row, 5, QTableWidgetItem(f"₹{rate:.2f}"))
            
            # Total
            self.table.setItem(row, 6, QTableWidgetItem(f"₹{total:.2f}"))
            
            # Center align numeric columns
            for col in [1, 2, 4, 5, 6]:
                self.table.item(row, col).setTextAlignment(Qt.AlignCenter)
    
    def update_summary(self, purchases, sales):
        """Update summary statistics"""
        total_purchases = sum(bill[6] for bill in purchases)
        total_sales = sum(bill[6] for bill in sales)
        
        summary = f"📊 Summary: Purchases: ₹{total_purchases:,.2f} | Sales: ₹{total_sales:,.2f} | Net: ₹{total_sales - total_purchases:,.2f}"
        self.summary_label.setText(summary)
    
    def export_bills(self):
        """Export bills to CSV"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Bills to CSV", "ventry_bills.csv", "CSV Files (*.csv)"
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["Bill No", "Type", "Date", "Item Name", "Quantity", "Rate", "Total"])
                    
                    for row in range(self.table.rowCount()):
                        row_data = []
                        for col in range(7):
                            row_data.append(self.table.item(row, col).text())
                        writer.writerow(row_data)
                
                QMessageBox.information(self, "Success", "Bills exported successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")


class EntryScreen(QWidget):
    """Transaction entry screen (Purchase/Sale)"""
    
    def __init__(self, db: DatabaseManager, stock_screen: StockItemScreen):
        super().__init__()
        self.db = db
        self.stock_screen = stock_screen
        self.init_ui()
    
    def showEvent(self, event):
        """Refresh items when tab becomes visible"""
        super().showEvent(event)
        self.load_items_to_combo()
    
    def init_ui(self):
        """Initialize entry screen UI"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Entry type selector
        type_layout = QHBoxLayout()
        type_label = QLabel("Transaction Type:")
        type_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.entry_type = QComboBox()
        self.entry_type.addItems(["Purchase Entry", "Sale Entry"])
        self.entry_type.currentIndexChanged.connect(self.update_entry_form)
        
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.entry_type)
        type_layout.addStretch()
        layout.addLayout(type_layout)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Bill number
        self.bill_no_input = QLineEdit()
        form_layout.addRow("Bill No:", self.bill_no_input)
        
        # Date
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)
        self.date_input.setDate(QDate.currentDate())
        form_layout.addRow("Date:", self.date_input)
        
        # Item selection
        self.item_combo = QComboBox()
        form_layout.addRow("Item:", self.item_combo)
        
        # Quantity
        self.quantity_input = QLineEdit()
        self.quantity_input.setText("0")
        form_layout.addRow("Quantity:", self.quantity_input)
        
        # Rate
        self.rate_input = QLineEdit()
        self.rate_input.setText("0.00")
        form_layout.addRow("Rate:", self.rate_input)
        
        # Total (auto-calculated)
        self.total_label = QLabel("₹0.00")
        self.total_label.setFont(QFont("Arial", 12, QFont.Bold))
        form_layout.addRow("Total:", self.total_label)
        
        layout.addLayout(form_layout)
        
        # Calculate total on quantity/rate change
        self.quantity_input.textChanged.connect(self.calculate_total)
        self.rate_input.textChanged.connect(self.calculate_total)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("💾 Save Entry")
        self.save_btn.clicked.connect(self.save_entry)
        self.save_btn.setMinimumHeight(40)
        
        self.clear_btn = QPushButton("🗑️ Clear Form")
        self.clear_btn.clicked.connect(self.clear_form)
        
        self.refresh_items_btn = QPushButton("🔄 Refresh Items")
        self.refresh_items_btn.clicked.connect(self.load_items_to_combo)
        self.refresh_items_btn.setToolTip("Reload items from database")
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.refresh_items_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        # Initial setup
        self.load_items_to_combo()
        self.update_entry_form()
    
    def load_items_to_combo(self):
        """Load items into combo box"""
        # Store current selection if any
        current_item_id = self.item_combo.currentData()
        
        # Clear and reload
        self.item_combo.clear()
        items = self.db.get_all_items()
        
        if not items:
            # No items available - show a message in the combo
            self.item_combo.addItem("No items available - Add items first", None)
            return
        
        # Add all items
        for item in items:
            self.item_combo.addItem(item[1], item[0])  # Name, ID
        
        # Restore previous selection if it still exists
        if current_item_id:
            index = self.item_combo.findData(current_item_id)
            if index >= 0:
                self.item_combo.setCurrentIndex(index)
    
    def update_entry_form(self):
        """Update form based on entry type"""
        # Refresh items first to ensure dropdown is populated
        self.load_items_to_combo()
        
        entry_type = self.entry_type.currentText()
        
        if entry_type == "Purchase Entry":
            last_bill = self.db.get_last_purchase_bill_no()
            next_bill = self.db.get_next_bill_no("P", last_bill)
            self.save_btn.setText("💾 Save Purchase")
        else:
            last_bill = self.db.get_last_sale_bill_no()
            next_bill = self.db.get_next_bill_no("S", last_bill)
            self.save_btn.setText("💾 Save Sale")
        
        self.bill_no_input.setText(next_bill)
    
    def calculate_total(self):
        """Calculate and display total amount"""
        try:
            quantity = float(self.quantity_input.text())
            rate = float(self.rate_input.text())
            total = quantity * rate
            self.total_label.setText(f"₹{total:.2f}")
        except ValueError:
            self.total_label.setText("₹0.00")
    
    def save_entry(self):
        """Save purchase or sale entry"""
        try:
            # Validate inputs
            bill_no = self.bill_no_input.text().strip()
            if not bill_no:
                QMessageBox.warning(self, "Warning", "Bill number is required!")
                return
            
            # Check if any items exist
            if self.item_combo.count() == 0:
                QMessageBox.warning(
                    self, "Warning", 
                    "No items available!\nPlease add items first in the Stock Items tab."
                )
                return
            
            # Check if a valid item is selected
            if self.item_combo.currentData() is None:
                QMessageBox.warning(
                    self, "Warning", 
                    "No items available!\nPlease add items first in the Stock Items tab."
                )
                return
            
            if self.item_combo.currentIndex() < 0:
                QMessageBox.warning(self, "Warning", "Please select an item!")
                return
            
            item_id = self.item_combo.currentData()
            date = self.date_input.date().toString("yyyy-MM-dd")
            quantity = float(self.quantity_input.text())
            rate = float(self.rate_input.text())
            
            if quantity <= 0:
                QMessageBox.warning(self, "Warning", "Quantity must be greater than 0!")
                return
            
            if rate <= 0:
                QMessageBox.warning(self, "Warning", "Rate must be greater than 0!")
                return
            
            # Save based on entry type
            if self.entry_type.currentText() == "Purchase Entry":
                success = self.db.add_purchase(bill_no, date, item_id, quantity, rate)
                if success:
                    QMessageBox.information(self, "Success", "Purchase saved successfully!")
                    self.clear_form()
                    self.stock_screen.load_items()
                else:
                    QMessageBox.critical(self, "Error", "Failed to save purchase!")
            else:
                success, message = self.db.add_sale(bill_no, date, item_id, quantity, rate)
                if success:
                    QMessageBox.information(self, "Success", "Sale saved successfully!")
                    self.clear_form()
                    self.stock_screen.load_items()
                else:
                    QMessageBox.critical(self, "Error", f"Failed to save sale!\n{message}")
        
        except ValueError:
            QMessageBox.warning(self, "Warning", "Please enter valid numeric values!")
    
    def clear_form(self):
        """Clear all form inputs"""
        self.update_entry_form()  # This now includes refreshing items
        self.date_input.setDate(QDate.currentDate())
        self.quantity_input.setText("0")
        self.rate_input.setText("0.00")
        self.total_label.setText("₹0.00")


def main():
    """Main application entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Ventry")
    
    # Set application-wide font
    font = QFont("Arial", 10)
    app.setFont(font)
    
    # Set application icon - use resource_path for PyInstaller
    icon_path = resource_path("assets/ventry_icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Create and show main window
    window = VentryMainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()