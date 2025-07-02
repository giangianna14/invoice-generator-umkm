# Changelog

All notable changes to Invoice Generator UMKM project will be documented in this file.

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
