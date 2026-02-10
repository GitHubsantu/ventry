"""
Build Script for Ventry - Creates Standalone EXE
Automatically installs PyInstaller and creates executable
"""

import subprocess
import sys
import os

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    print("=" * 60)
    print("Installing PyInstaller...")
    print("=" * 60)
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    print("✓ PyInstaller installed successfully!\n")

def build_exe():
    """Build the executable using PyInstaller"""
    print("=" * 60)
    print("Building Ventry Executable...")
    print("=" * 60)
    print()
    
    # Check if assets folder exists
    if not os.path.exists('assets'):
        print("✗ Assets folder not found!")
        print("  Please run create_icon.py first to generate icons")
        return False
    
    # Build using spec file
    if os.path.exists('ventry.spec'):
        print("Building from ventry.spec...")
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "--clean",  # Clean PyInstaller cache
            "ventry.spec"
        ])
    else:
        # Build with command line options
        print("Building with auto-generated spec...")
        subprocess.check_call([
            sys.executable, "-m", "PyInstaller",
            "--name=Ventry",
            "--onefile",  # Single file executable
            "--windowed",  # No console window
            "--icon=assets/ventry_icon.ico",
            "--add-data=assets/ventry_icon.ico;assets",
            "--add-data=assets;assets",
            "--noconsole",
            "main.py"
        ])
    
    print()
    print("=" * 60)
    print("✓ Build completed successfully!")
    print("=" * 60)
    print()
    print("Executable location:")
    print("  → dist/Ventry.exe (Windows)")
    print("  → dist/Ventry (Linux/Mac)")
    print()
    print("Notes:")
    print("  - The exe is standalone and includes all dependencies")
    print("  - Database (ventry.db) will be created on first run")
    print("  - Keep the exe in a folder with write permissions")
    print()
    return True

def main():
    """Main build process"""
    print()
    print("╔════════════════════════════════════════════════════════╗")
    print("║       Ventry EXE Builder - Standalone Package         ║")
    print("╚════════════════════════════════════════════════════════╝")
    print()
    
    try:
        # Step 1: Install PyInstaller
        install_pyinstaller()
        
        # Step 2: Build executable
        if build_exe():
            print("╔════════════════════════════════════════════════════════╗")
            print("║              Build Process Completed!                  ║")
            print("╚════════════════════════════════════════════════════════╝")
        else:
            print("Build failed. Please check the errors above.")
            sys.exit(1)
            
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error during build: {e}")
        print("\nTroubleshooting:")
        print("  1. Ensure Python and pip are properly installed")
        print("  2. Check that all required files exist:")
        print("     - main.py")
        print("     - database.py")
        print("     - assets/ventry_icon.ico")
        print("  3. Try running: pip install pyinstaller")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
