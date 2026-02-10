# Ventry – Inventory Manager 📦

A modern desktop inventory management system built with Python and PyQt5.

## 🎯 Features

- ✅ **Stock Management** - Add, edit, and delete inventory items with automatic date tracking
- ✅ **Purchase & Sale Transactions** - Record purchases and sales with automatic bill number generation
- ✅ **Bill Viewing** - View and search all bills (purchases and sales) in one place
- ✅ **Stock Tracking** - Real-time stock updates with purchase/sale history
- ✅ **Dark Mode** - Toggle between light and dark themes
- ✅ **Export to CSV** - Export stock data and bills for external use
- ✅ **Auto-calculated Totals** - Automatic calculation of transaction totals
- ✅ **Search & Filter** - Search items and filter bills by type

## 📋 What's New in This Update

### 1. **Created Date Column** ✅
   - Added "Created Date" column in Stock Items table
   - Shows when each item was added to the system
   - Properly formatted date display (YYYY-MM-DD HH:MM)

### 2. **Bill Viewing System** ✅
   - New "View Bills" tab to see all transactions
   - Filter by Purchase/Sale or view all together
   - Search bills by bill number
   - Color-coded bill types (Green for purchases, Red for sales)
   - Summary statistics showing total purchases, sales, and net amount
   - Export bills to CSV

### 3. **Credits & Attribution** ✅
   - Updated About dialog with developer information
   - Added GitHub link: https://github.com/githubsantu
   - Added website link: https://imdevops.in
   - Support for custom logo in About dialog

### 4. **Logo Support** ✅
   - Application now supports custom icon and logo
   - Icon file: `assets/icon.ico` (for window title bar and taskbar)
   - Logo file: `assets/logo.png` (for About dialog)

## 🚀 Installation

### Method 1: Run from Source

1. **Install Python** (3.8 or higher)
   Download from: https://www.python.org/downloads/

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

### Method 2: Build Executable

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Build EXE**
   ```bash
   python build_exe.py
   ```

3. **Find Your EXE**
   - The executable will be in the `dist/` folder
   - File name: `Ventry.exe`
   - This is a standalone file - no installation needed!

### Method 3: Manual PyInstaller Build

```bash
pyinstaller Ventry.spec
```

## 📁 Project Structure

```
ventry/
│
├── main.py              # Main application file
├── database.py          # Database management
├── requirements.txt     # Python dependencies
├── build_exe.py         # Automated build script
├── Ventry.spec         # PyInstaller configuration
├── README.md           # This file
│
├── assets/             # Optional: App resources
│   ├── icon.ico       # Window icon (256x256 recommended)
│   └── logo.png       # About dialog logo (64x64 recommended)
│
└── ventry.db          # SQLite database (auto-created)
```

## 🎨 Adding Custom Logo/Icon

### For Application Icon:
1. Create or download a `.ico` file (256x256 pixels recommended)
2. Create an `assets` folder in the project directory
3. Save the icon as `assets/icon.ico`
4. Rebuild the EXE

### For About Dialog Logo:
1. Create or download a `.png` file (64x64 pixels recommended)
2. Save it as `assets/logo.png`
3. The logo will appear in the About dialog automatically

### Free Icon Resources:
- **Icons8**: https://icons8.com/
- **Flaticon**: https://www.flaticon.com/
- **Icon Archive**: https://iconarchive.com/

### Creating .ico from .png:
Use online tools like:
- https://convertio.co/png-ico/
- https://www.icoconverter.com/

## 💾 Database

The application uses SQLite for data storage:
- **File**: `ventry.db` (created automatically on first run)
- **Location**: Same folder as the executable
- **Backup**: Simply copy the `ventry.db` file to backup your data

### Database Tables:
- `items` - Inventory items
- `purchases` - Purchase transactions
- `sales` - Sale transactions
- `stock_log` - Stock change history

## 🎮 Usage

### Adding Items:
1. Go to "Stock Items" tab
2. Click "➕ Add Item"
3. Enter item name and prices
4. Click OK

### Recording Purchases:
1. Go to "Transactions" tab
2. Select "Purchase Entry"
3. Bill number is auto-generated
4. Select item, enter quantity and rate
5. Click "💾 Save Purchase"

### Recording Sales:
1. Go to "Transactions" tab
2. Select "Sale Entry"
3. Bill number is auto-generated
4. Select item, enter quantity and rate
5. Click "💾 Save Sale"
   - The system will check stock availability automatically

### Viewing Bills:
1. Go to "View Bills" tab
2. Use filters to show All Bills, Purchases Only, or Sales Only
3. Search by bill number
4. View summary statistics at the bottom
5. Export to CSV if needed

### Dark Mode:
- Press `Ctrl+D` or use View menu → Toggle Dark Mode

### Export Data:
- File menu → Export to CSV
- Or use the export button in View Bills tab

## ⌨️ Keyboard Shortcuts

- `Ctrl+E` - Export to CSV
- `Ctrl+D` - Toggle Dark Mode
- `F5` - Refresh Data
- `Ctrl+Q` - Quit Application

## 🐛 Troubleshooting

### "No items available" message:
- Add items first in the Stock Items tab
- Click "🔄 Refresh Items" in Transactions tab

### "Insufficient stock" error:
- Check current stock in Stock Items tab
- You can only sell items that are in stock

### Database errors:
- Make sure `ventry.db` file is not open in another program
- Check file permissions

### EXE build fails:
- Make sure all dependencies are installed
- Run `pip install -r requirements.txt` again
- Check if `assets` folder exists (create it if missing)

## 📊 Features in Detail

### Bill Number System:
- Purchase bills: P0001, P0002, P0003...
- Sale bills: S0001, S0002, S0003...
- Auto-increments with each transaction
- Can be searched in the View Bills tab

### Stock Tracking:
- Purchases automatically add to stock
- Sales automatically deduct from stock
- View total purchased and sold quantities
- Current stock shown in real-time

### Date Tracking:
- All items have creation timestamps
- All transactions have date records
- View Bills tab shows transaction dates
- Export includes all date information

## 👨‍💻 Developer

- GitHub: [@githubsantu](https://github.com/githubsantu)
- Website: [imdevops.in](https://imdevops.in)

## 📝 License

© 2026 Ventry. All rights reserved.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Visit: https://imdevops.in
3. Open an issue on GitHub: https://github.com/githubsantu

---

**Enjoy managing your inventory with Ventry! 🎉**
