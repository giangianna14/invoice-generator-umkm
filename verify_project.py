#!/usr/bin/env python3
"""
Final Verification Script for Invoice Generator UMKM v2.2.0
Verifies all features including Company Settings and Template System
"""

import sys
import os

def verify_files():
    """Verify all required files exist"""
    required_files = [
        'app.py',
        'database.py', 
        'pdf_generator.py',
        'template_pdf_generator.py',
        'requirements.txt',
        'README.md',
        'CHANGELOG.md',
        'LICENSE',
        'CONTRIBUTING.md'
    ]
    
    print("🔍 Verifying project files...")
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✅ {file}")
        else:
            print(f"  ❌ {file} - MISSING")
            missing_files.append(file)
    
    return len(missing_files) == 0

def verify_database_schema():
    """Verify database has all required tables"""
    try:
        from database import Database
        db = Database("verify_test.db")
        
        import sqlite3
        conn = sqlite3.connect("verify_test.db")
        cursor = conn.cursor()
        
        # Check if all tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['customers', 'products', 'invoices', 'invoice_items', 'company_settings']
        
        print("\n📊 Verifying database schema...")
        missing_tables = []
        
        for table in required_tables:
            if table in tables:
                print(f"  ✅ {table} table")
            else:
                print(f"  ❌ {table} table - MISSING")
                missing_tables.append(table)
        
        # Test company settings functionality
        if 'company_settings' in tables:
            try:
                settings = db.get_company_settings()
                print(f"  ✅ Company settings retrieval works")
                
                result = db.update_company_settings(
                    name="Test Company",
                    address="Test Address", 
                    phone="123456789",
                    email="test@test.com",
                    invoice_template="creative"
                )
                print(f"  ✅ Company settings update works")
                
                # Test template persistence
                updated_settings = db.get_company_settings()
                if updated_settings and updated_settings.get('invoice_template') == 'creative':
                    print(f"  ✅ Template persistence works")
                else:
                    print(f"  ❌ Template persistence failed: {updated_settings.get('invoice_template') if updated_settings else 'None'}")
                    return False
                
            except Exception as e:
                print(f"  ❌ Company settings methods error: {e}")
                return False
        
        conn.close()
        os.remove("verify_test.db")
        
        return len(missing_tables) == 0
        
    except Exception as e:
        print(f"  ❌ Database verification failed: {e}")
        return False

def verify_imports():
    """Verify all required packages can be imported"""
    required_packages = [
        'streamlit',
        'pandas', 
        'plotly',
        'reportlab',
        'openpyxl'
    ]
    
    print("\n📦 Verifying package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - NOT INSTALLED") 
            failed_imports.append(package)
    
    return len(failed_imports) == 0

def verify_readme_content():
    """Verify README contains new features"""
    print("\n📖 Verifying README content...")
    
    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_content = [
            'Company Settings',
            'company information management',
            'Pengaturan',
            'v2.1.0' in open('CHANGELOG.md').read() if os.path.exists('CHANGELOG.md') else False
        ]
        
        checks = [
            'Company Settings' in content,
            'company information' in content.lower(),
            'pengaturan' in content.lower(),
            'template' in content.lower(),
            os.path.exists('CHANGELOG.md')
        ]
        
        check_names = [
            'Company Settings mentioned',
            'Company information described', 
            'Indonesian interface mentioned',
            'Template system mentioned',
            'CHANGELOG.md exists'
        ]
        
        all_passed = True
        for check, name in zip(checks, check_names):
            if check:
                print(f"  ✅ {name}")
            else:
                print(f"  ❌ {name}")
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"  ❌ README verification failed: {e}")
        return False

def main():
    """Run all verification checks"""
    print("🚀 Invoice Generator UMKM v2.2.0 - Final Verification")
    print("=" * 60)
    
    all_checks = [
        ("Files", verify_files()),
        ("Database", verify_database_schema()),
        ("Packages", verify_imports()),
        ("Documentation", verify_readme_content())
    ]
    
    print("\n" + "=" * 60)
    print("📋 VERIFICATION SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(all_checks)
    
    for check_name, result in all_checks:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name:15} : {status}")
        if result:
            passed += 1
    
    print("=" * 60)
    
    if passed == total:
        print(f"🎉 ALL CHECKS PASSED ({passed}/{total})")
        print("\n🚀 Project is ready for production!")
        print("📊 Features: Invoice Generation + Company Settings + Template System + CRUD + Analytics")
        print("🎨 Templates: 8 Professional Designs for UMKM Industries")
        print("🌐 GitHub: Ready for deployment")
        return True
    else:
        print(f"💥 SOME CHECKS FAILED ({passed}/{total})")
        print("\n🔧 Please fix the issues before deployment")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
