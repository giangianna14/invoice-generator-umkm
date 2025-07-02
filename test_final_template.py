#!/usr/bin/env python3
"""
Final test untuk memverifikasi template persistence fix
"""

from database import Database

def test_final_template_persistence():
    """Final test untuk template persistence"""
    print("🔍 Final Template Persistence Test...")
    print("=" * 50)
    
    db = Database()
    
    # Test current template
    settings = db.get_company_settings()
    if settings:
        current_template = settings.get('invoice_template', 'TIDAK ADA')
        print(f"✅ Current template in database: {current_template}")
        
        # Test changing template and verifying persistence
        test_template = 'creative'
        print(f"\n🔄 Testing template change to: {test_template}")
        
        result = db.update_company_settings(
            name=settings['name'],
            address=settings['address'],
            phone=settings['phone'],
            email=settings['email'],
            website=settings.get('website', ''),
            npwp=settings.get('npwp', ''),
            default_tax_rate=settings.get('default_tax_rate', 11.0),
            default_due_days=settings.get('default_due_days', 30),
            invoice_template=test_template
        )
        
        if result['success']:
            # Verify it was saved
            updated_settings = db.get_company_settings()
            saved_template = updated_settings.get('invoice_template', 'TIDAK ADA')
            
            if saved_template == test_template:
                print(f"✅ Template {test_template} saved and verified successfully")
                
                # Restore original template
                restore_result = db.update_company_settings(
                    name=settings['name'],
                    address=settings['address'],
                    phone=settings['phone'],
                    email=settings['email'],
                    website=settings.get('website', ''),
                    npwp=settings.get('npwp', ''),
                    default_tax_rate=settings.get('default_tax_rate', 11.0),
                    default_due_days=settings.get('default_due_days', 30),
                    invoice_template=current_template
                )
                
                if restore_result['success']:
                    print(f"✅ Original template {current_template} restored")
                    print(f"\n🎉 TEMPLATE PERSISTENCE BUG IS FIXED!")
                    return True
                else:
                    print(f"❌ Failed to restore original template")
                    return False
            else:
                print(f"❌ Template not saved correctly. Expected: {test_template}, Got: {saved_template}")
                return False
        else:
            print(f"❌ Failed to save template: {result['message']}")
            return False
    else:
        print("❌ No company settings found")
        return False

if __name__ == "__main__":
    success = test_final_template_persistence()
    print("=" * 50)
    if success:
        print("✅ ALL TESTS PASSED - Template persistence working correctly!")
    else:
        print("❌ TESTS FAILED - Template persistence still has issues")
    exit(0 if success else 1)
