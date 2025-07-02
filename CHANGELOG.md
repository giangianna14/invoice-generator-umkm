# Changelog

All notable changes to Invoice Generator UMKM project will be documented in this file.

## [v2.2.1] - 2025-07-03

### 🐛 Bug Fixes - Template Persistence
- **Fixed Template Selection Bug** - Template selection now properly persists after saving settings
- **Database Column Index Fix** - Corrected template column reading in `get_company_settings()`
  - Fixed index position from 9 to 10 for `invoice_template` field
  - Resolved issue where template value was incorrectly read from `updated_at` timestamp
- **Session State Synchronization** - Improved session state management for template selection
  - Always sync `temp_selected_template` with database value on page load
  - Removed conflicting conditional logic that caused state mismatches
- **Form Submission Flow** - Optimized form submission behavior
  - Removed unnecessary `st.rerun()` that caused form reset issues
  - Template selection UI now reflects saved state immediately after submit

### 🧪 Testing & Validation
- Added comprehensive test script (`test_template_fix_clean.py`)
- Verified template persistence across all 8 template types
- Confirmed database storage and retrieval functionality
- Validated UI state synchronization with database

### 🔧 Technical Details
- Updated `database.py`: Fixed column indexing in row result parsing
- Updated `app.py`: Simplified session state synchronization logic
- Improved error handling for backward compatibility
- Enhanced form validation and user feedback

### 📝 Impact
- **User Experience**: Template selection now works as expected
- **Data Integrity**: Template preferences reliably saved and restored
- **System Stability**: Eliminated form reset issues and state conflicts
- **Business Continuity**: Users can consistently use their preferred invoice templates

---

## [v2.2.0] - 2025-07-02

### ✨ Added - Multiple Invoice Templates
- **8 Professional Invoice Templates** - Industry-specific designs for different UMKM needs
  - 🏛️ Klasik Profesional - Traditional business style
  - 🎯 Modern Minimalis - Clean contemporary design  
  - 🎨 Kreatif & Colorful - Eye-catching for creative industries
  - 🏢 Corporate Formal - Professional with credibility emphasis
  - 💻 Tech & Digital - Modern tech-focused design
  - 🛍️ Retail & Fashion - Stylish and trendy
  - 🍽️ Food & Beverage - Warm restaurant/catering design
  - 🔧 Jasa & Konsultasi - Professional service-oriented
- **Template Selection System** - Easy template picker in company settings
- **Template Preview** - Generate sample invoices to preview templates
- **Template Showcase** - Visual overview of all available templates
- **Database Integration** - Template preference stored and applied automatically

### 🛠️ Technical Improvements
- Created `TemplatedInvoicePDFGenerator` class with modular template system
- Enhanced database schema with `invoice_template` field in company settings
- Updated PDF generation pipeline to use selected templates
- Added comprehensive template preview and selection UI
- Implemented template-specific styling and layouts

### 🎨 Design Features
- **Industry-Specific Colors** - Each template uses appropriate color schemes
- **Professional Layouts** - Different header styles, info placement, and branding
- **Enhanced Typography** - Template-specific fonts and sizing
- **Visual Differentiation** - Unique design elements for each template
- **Brand Consistency** - Company info integration across all templates

### 📖 Documentation
- Updated README with template feature documentation
- Added template selection guide and usage instructions
- Enhanced feature list with template capabilities
- Updated project roadmap and statistics

---

## [v2.1.0] - 2025-07-02

### ✨ Added
- **Company Settings Management** - Complete company information setup
  - Company details form (name, address, phone, email)
  - Additional business info (website, NPWP) 
  - Default business settings (tax rate %, due days)
  - Real-time preview of company information
  - Professional PDF header integration
- **Enhanced PDF Branding** - Company info automatically appears in invoice headers
- **Business Configuration** - Customizable default tax rates and due date settings
- **Data Persistence** - Company settings stored in database and used across sessions

### 🛠️ Technical Improvements  
- Added `company_settings` table to database schema
- Implemented `get_company_settings()` and `update_company_settings()` methods
- Enhanced PDF generator to accept and format company information
- Integrated settings page with form validation and error handling
- Added comprehensive testing for end-to-end company settings workflow

### 📖 Documentation
- Updated README with company settings feature documentation
- Added usage instructions for company information setup
- Enhanced feature list with new capabilities
- Updated project stats and roadmap

---

## [v2.0.0] - 2025-07-01

### 🚀 Major Features
- Complete CRUD operations for customers and products
- Advanced search, sort, and filtering capabilities
- Professional PDF invoice generation
- Interactive dashboard with analytics
- Master data integration with smart product selection
- Excel export functionality
- Responsive mobile-friendly UI

### 🧾 Invoice Management
- Auto invoice numbering with timestamp format
- Tax calculation with customizable rates
- Multi-status tracking (Draft, Paid, Overdue)
- Professional PDF layout with business branding

### 👥 Customer Management
- Full CRUD with inline editing
- Real-time search and filtering
- Usage protection (prevent delete if used in invoices)
- Comprehensive customer profiles

### 📦 Product Management  
- Master data catalog with pricing
- Duplicate detection and validation
- Bulk operations and statistics
- Auto-save from invoice to master data

### 📊 Analytics & Reporting
- Interactive dashboard with key metrics
- Visual charts for revenue trends
- Date range filtering
- Excel export for detailed analysis

---

## [v1.0.0] - 2025-06-30

### 🎯 Initial Release
- Basic invoice generation system
- SQLite database integration
- Streamlit web interface
- PDF export functionality
- Core customer and product management

---

**Legend:**
- ✨ New features
- 🛠️ Improvements
- 🐛 Bug fixes
- 📖 Documentation
- 🔒 Security
- 🚀 Performance
