# 🧾 Invoice Generator UMKM

> **Professional Invoice Management System untuk UMKM Indonesia** 🇮🇩

Invoice Generator adalah aplikasi lengkap untuk UMKM Indonesia yang dibuat dengan Python dan Streamlit. Aplikasi ini membantu usaha kecil dan menengah untuk membuat invoice professional, mengelola customer, tracking penjualan, dan analytics bisnis dengan fitur CRUD yang lengkap.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![UMKM](https://img.shields.io/badge/Made%20for-UMKM%20Indonesia-red.svg)](https://github.com)

## 📸 Screenshots

> **Coming Soon!** Screenshots dan demo video akan ditambahkan untuk showcase UI/UX aplikasi.

## 🚀 Quick Demo

Coba aplikasi dalam 3 langkah mudah:

```bash
# 1. Clone & setup
git clone https://github.com/username/invoice-generator-umkm.git
cd invoice-generator-umkm && pip install -r requirements.txt

# 2. Run aplikasi  
streamlit run app.py

# 3. Buka browser ke http://localhost:8501
```

> **🎯 Pro Tip**: Setup selesai dalam 2-3 menit!

## ✨ Features

### 🧾 Invoice Management
- ✅ **Generate Invoice PDF** - Format profesional dengan logo perusahaan
- ✅ **Professional PDF Layout** - Template bisnis yang rapi dan modern
- ✅ **Multiple Invoice Templates** - 8 template design sesuai industri UMKM
- ✅ **Auto Invoice Numbering** - Format INV-YYYYMMDD-HHMMSS
- ✅ **Tax Calculation** - Perhitungan pajak otomatis (default 11%)
- ✅ **Multi-Currency Format** - Format Rupiah yang rapi
- ✅ **Invoice Status Tracking** - Draft, Paid, Overdue status
- ✅ **Company Settings** - Atur informasi perusahaan untuk header invoice

### 👥 Customer Management (Full CRUD)
- ✅ **Add Customers** - Tambah customer dengan data lengkap
- ✅ **Search Customers** - Pencarian real-time berdasarkan nama
- ✅ **Edit Customer Data** - Update informasi customer inline
- ✅ **Delete Customers** - Hapus customer dengan validasi usage
- ✅ **Customer Profiles** - Name, email, phone, address
- ✅ **Usage Protection** - Prevent delete jika sudah digunakan di invoice

### 📦 Product Management (Full CRUD)
- ✅ **Master Data Products** - Database produk/jasa lengkap
- ✅ **Search & Sort Products** - Cari dan urutkan berdasarkan nama/harga/tanggal
- ✅ **Edit Product Details** - Update nama, harga, deskripsi
- ✅ **Delete Products** - Hapus produk dengan validasi usage
- ✅ **Duplicate Detection** - Cegah produk dengan nama sama
- ✅ **Product Statistics** - Total, rata-rata, min/max harga
- ✅ **Auto-save to Master** - Simpan produk baru dari invoice ke master data

### 📊 Sales Analytics & Reports
- ✅ **Interactive Dashboard** - Overview bisnis dengan metrics penting
- ✅ **Revenue Tracking** - Total penjualan dan rata-rata invoice
- ✅ **Visual Charts** - Line chart revenue bulanan, pie chart status
- ✅ **Date Range Reports** - Filter laporan berdasarkan periode
- ✅ **Excel Export** - Export laporan ke Excel untuk analisis lanjut
- ✅ **Real-time Analytics** - Update otomatis saat ada invoice baru

### 🚀 Advanced Features
- ✅ **Master Data Integration** - Pilih produk dari database atau input manual
- ✅ **Smart Product Selection** - Tab untuk master data vs manual input
- ✅ **Duplicate Product Handling** - Warning dan opsi gunakan existing
- ✅ **Company Information Management** - Atur info perusahaan (nama, alamat, kontak, NPWP)
- ✅ **Multiple Invoice Templates** - 8 template design profesional sesuai industri
- ✅ **Template Persistence** - Template selection tersimpan permanen (FIXED v1.2.1)
- ✅ **Template Preview System** - Preview sample invoice dengan template pilihan
- ✅ **Industry-Specific Design** - Template khusus retail, F&B, tech, service, dll
- ✅ **Customizable Business Settings** - Default tax rate dan due date settings
- ✅ **Professional PDF Branding** - Header perusahaan otomatis di setiap invoice
- ✅ **Responsive Design** - Akses optimal dari desktop dan mobile
- ✅ **Session Management** - State management yang robust
- ✅ **Error Handling** - Comprehensive error handling dan validation
- ✅ **Data Integrity** - Referential integrity protection
- ✅ **Professional UI/UX** - Clean interface dengan icons dan styling

## 🎯 User Experience Highlights

### 📱 Intuitive Interface
- 🎨 **Modern UI** - Clean design dengan icons dan color coding
- 📱 **Mobile Responsive** - Optimal experience di semua device
- 🔍 **Real-time Search** - Instant search untuk customer dan produk
- � **Visual Feedback** - Progress indicators dan status notifications

### ⚡ Workflow Efficiency
- 🚀 **Quick Product Add** - Pilih dari master data atau input manual
- 💾 **Auto-save Options** - Simpan produk baru ke master data otomatis
- � **Smart Validation** - Prevent errors dengan validation yang cerdas
- 📋 **Bulk Operations** - Efficient data management

### 🛡️ Data Protection
- 🔒 **Safe Delete** - Validasi usage sebelum hapus data
- 📊 **Usage Tracking** - Monitor penggunaan customer/produk di invoice
- 💾 **Data Integrity** - Consistent data dengan foreign key protection
- 🔄 **Auto-backup** - Session state management untuk prevent data loss

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

1. **Clone repository**
```bash
git clone https://github.com/username/invoice-generator-umkm.git
cd invoice-generator-umkm
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau
venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run application**
```bash
streamlit run app.py
```

5. **Open browser**
```
🌐 http://localhost:8501
```

> **💡 Tip**: Bookmark URL untuk akses cepat ke aplikasi!

### 🔧 Development Setup

Untuk developer yang ingin berkontribusi:

```bash
# Clone repository
git clone https://github.com/username/invoice-generator-umkm.git
cd invoice-generator-umkm

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# atau venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run in development mode
streamlit run app.py --server.runOnSave true
```

> **📂 Files**: Lihat [GITHUB_UPLOAD_INSTRUCTIONS.md](GITHUB_UPLOAD_INSTRUCTIONS.md) untuk setup GitHub dan deployment.

## 📁 Project Structure

```
invoice_generator/
├── 📄 app.py               # Main Streamlit application
├── 🗄️ database.py          # Database operations & CRUD
├── 📋 pdf_generator.py     # Professional PDF generation
├── 📦 requirements.txt     # Python dependencies
├── 📖 README.md           # Documentation (this file)
├── ⚙️ .gitignore          # Git ignore rules
├── 📄 LICENSE             # MIT License
├── 🤝 CONTRIBUTING.md     # Contribution guidelines
├── 📤 GITHUB_UPLOAD_INSTRUCTIONS.md  # GitHub setup guide
└── 🗃️ invoice_system.db   # SQLite database (auto-created)
```

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| **Backend** | Python 3.8+ | Core application logic |
| **Web Framework** | Streamlit | Interactive web interface |
| **Database** | SQLite | Lightweight data storage |
| **PDF Generation** | ReportLab | Professional invoice PDFs |
| **Data Processing** | Pandas | Data manipulation & analysis |
| **Visualization** | Plotly | Interactive charts & graphs |
| **Excel Export** | OpenPyXL | Report generation |
| **UI Components** | Streamlit Native | Modern responsive design |

## 📋 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| **streamlit** | 1.28.1 | Web framework & UI |
| **pandas** | 2.1.3 | Data processing |
| **reportlab** | 4.0.7 | PDF generation |
| **openpyxl** | 3.1.2 | Excel export |
| **plotly** | 5.17.0 | Interactive charts |
| **pillow** | 10.1.0 | Image processing |
| **python-dateutil** | 2.8.2 | Date utilities |

> **💾 Auto Install**: Jalankan `pip install -r requirements.txt` untuk install semua dependencies.

## 📖 How to Use

### 1. **Setup Master Data**
#### Company Settings (Enhanced!)
- **Setup Company Info**: Menu "Pengaturan" → Isi informasi perusahaan lengkap
- **Company Details**: Nama perusahaan, alamat, telepon, email (wajib)
- **Additional Info**: Website, NPWP (opsional untuk compliance)
- **Business Settings**: Default tax rate (%) dan due date (hari)
- **Invoice Template Selection**: Pilih dari 8 template design profesional
- **Template Preview**: Generate sample invoice untuk preview template
- **Real-time Preview**: Lihat preview info yang akan muncul di PDF
- **Professional PDF Header**: Info perusahaan otomatis tampil di semua invoice

#### Available Invoice Templates
1. **🏛️ Klasik Profesional** - Traditional business style, cocok untuk semua industri
2. **🎯 Modern Minimalis** - Clean contemporary design, cocok untuk tech/startup
3. **🎨 Kreatif & Colorful** - Eye-catching design untuk industri kreatif
4. **🏢 Corporate Formal** - Professional dengan emphasis pada credibility
5. **💻 Tech & Digital** - Modern tech-focused design untuk IT/software
6. **🛍️ Retail & Fashion** - Stylish dan trendy untuk fashion/retail
7. **🍽️ Food & Beverage** - Warm design untuk restaurant/catering
8. **🔧 Jasa & Konsultasi** - Professional service-oriented design

#### Customer Management
- **Add**: Tambah customer baru dengan nama, email, phone, alamat
- **Search**: Gunakan search box untuk cari customer cepat
- **Edit**: Click "✏️ Edit" untuk update data customer
- **Delete**: Click "🗑️ Hapus" (dengan validasi usage protection)

#### Product Management  
- **Add**: Tambah produk/jasa dengan nama, harga, deskripsi
- **Search & Sort**: Cari produk dan urutkan by nama/harga/tanggal
- **Edit**: Click "✏️ Edit" untuk update produk details
- **Delete**: Click "🗑️ Hapus" (dengan usage validation)
- **Statistics**: Lihat overview total produk, harga rata-rata, min/max

### 2. **Create Professional Invoices**
#### Method 1: Master Data (Recommended)
- Pilih tab "📦 Pilih dari Master Data"
- Select produk dari dropdown (nama + harga auto-fill)
- Set quantity dan click "➕ Tambah dari Master"

#### Method 2: Manual Input
- Pilih tab "✏️ Input Manual"
- Input nama produk, quantity, harga manual
- Click "➕ Tambah Manual"
- **Optional**: Click "💾 Simpan ke Master Data" untuk future use

#### Complete Invoice
- Pilih customer dari dropdown
- Set tanggal invoice dan due date
- Adjust tax rate (default 11%)
- Add notes jika diperlukan
- Click "🧾 Buat Invoice"
- Download PDF invoice yang professional

### 3. **Monitor & Analyze Business**
#### Dashboard Overview
- 📊 **Key Metrics**: Total invoice, revenue, rata-rata invoice
- 📈 **Visual Charts**: Revenue trends dan status distribution
- 📋 **Recent Invoices**: 10 invoice terbaru dengan details

#### Advanced Reports
- 📅 **Date Range Filter**: Pilih periode custom
- 📊 **Sales Analytics**: Detail penjualan harian
- 📈 **Performance Metrics**: Total penjualan, average per invoice
- 📋 **Excel Export**: Download laporan untuk analisis lanjut

### 4. **Data Management Best Practices**
#### Customer Data
- 🔍 **Use Search**: Cari customer dengan nama
- ✏️ **Keep Updated**: Update info customer secara berkala
- 🛡️ **Safe Operations**: System protect dari accidental delete

#### Product Catalog
- 📦 **Build Master Data**: Simpan produk yang sering dijual
- 🔄 **Consistent Pricing**: Update harga di master data
- 📊 **Monitor Performance**: Track produk dengan statistics
- 🔍 **Easy Management**: Search dan sort untuk efficiency

## 🎯 Target Users

- **UMKM** - Usaha kecil dan menengah
- **Freelancer** - Pekerja lepas yang butuh invoice
- **Small Business** - Bisnis kecil dengan pencatatan sederhana
- **Startup** - Tim yang butuh invoicing system cepat

## 💰 Business Model

### Freemium Model
- **Free**: 10 invoice/bulan
- **Premium**: Unlimited invoice (Rp 149K-299K/bulan)

### Premium Features
- Unlimited invoices
- Custom branding PDF
- Advanced analytics
- Multi-user access
- Cloud backup
- WhatsApp integration
- Payment gateway integration

## 🚀 Roadmap

### ✅ Phase 1 (Completed)
- ✅ Complete invoice generation system
- ✅ Customer & product CRUD operations
- ✅ Professional PDF export with branding
- ✅ Company information management with customizable settings
- ✅ Multiple invoice templates (8 professional designs)
- ✅ Template preview and selection system
- ✅ Industry-specific invoice designs
- ✅ Advanced dashboard with analytics
- ✅ Master data integration with smart selection
- ✅ Search, sort, and filter functionality
- ✅ Duplicate detection and validation
- ✅ Excel reporting with custom date ranges
- ✅ Responsive UI with modern design
- ✅ Data integrity protection
- ✅ Real-time company settings with PDF integration

### 🚧 Phase 2 (In Progress)
- 💳 Payment integration (Midtrans/QRIS)
- 📱 WhatsApp integration for invoice delivery
- 🔄 Recurring invoices untuk subscription business
- 👥 Multi-user support dengan role management
- 📊 Advanced analytics dengan AI insights

### 🔮 Phase 3 (Future)
- 📦 Inventory management integration
- 🏪 E-commerce integration (Shopee, Tokopedia)
- 🤖 AI-powered business insights
- ☁️ Cloud sync dan backup
- 📱 Mobile app (React Native)
- 🌐 Multi-language support

## 💡 Key Differentiators

### 🇮🇩 Indonesia-Focused
- **Rupiah Currency**: Native Indonesian currency formatting
- **Tax Integration**: PPN 11% calculation built-in
- **Local Business Needs**: Designed specifically for UMKM workflow
- **Bahasa Indonesia**: Full Indonesian language interface

### 🚀 Technical Excellence
- **Modern Tech Stack**: Python + Streamlit + SQLite
- **Responsive Design**: Works perfectly on mobile devices
- **Real-time Updates**: Instant search and data synchronization
- **Professional Output**: High-quality PDF generation

### 💼 Business Ready
- **Complete CRUD**: Full data management capabilities
- **Data Protection**: Usage validation and referential integrity
- **Scalable Architecture**: Handle growing business needs
- **Professional UI**: Enterprise-grade user interface

## 📊 Performance Features

### ⚡ Speed Optimizations
- **Fast Search**: Real-time filtering dengan minimal latency
- **Efficient Queries**: Optimized database operations
- **Smart Caching**: Session state management for better UX
- **Lazy Loading**: Load data only when needed

### 🛡️ Security & Reliability
- **Input Validation**: Comprehensive data validation
- **Error Handling**: Robust error management
- **Data Backup**: Session state protection
- **Safe Operations**: Prevent accidental data loss

## 🤝 Contributing

Kami welcome kontribusi dari developer Indonesia! 🇮🇩

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** changes (`git commit -m 'Add AmazingFeature'`)
4. **Push** to branch (`git push origin feature/AmazingFeature`)
5. **Open** Pull Request

Lihat [CONTRIBUTING.md](CONTRIBUTING.md) untuk guidelines lengkap.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support & Community

Butuh bantuan atau punya pertanyaan? Kami siap membantu! 

| Channel | Contact | Purpose |
|---------|---------|---------|
| 📧 **Email** | support@invoicegenerator.com | General support |
| 💬 **WhatsApp** | +62 xxx-xxxx-xxxx | Quick assistance |
| 🐛 **Issues** | [GitHub Issues](https://github.com/username/invoice-generator-umkm/issues) | Bug reports & features |
| 📖 **Docs** | [GITHUB_UPLOAD_INSTRUCTIONS.md](GITHUB_UPLOAD_INSTRUCTIONS.md) | Setup guide |

## 🌟 Star History

Jika aplikasi ini membantu bisnis Anda, berikan ⭐ di GitHub!

## 📈 Stats

- ✅ **100%** CRUD functionality
- ✅ **22+** core features implemented  
- ✅ **8** professional invoice templates
- ✅ **15+** advanced features ready
- ✅ **0** known critical bugs
- ✅ **NEW:** Multiple invoice templates system
- ✅ **FIXED:** Template persistence bug (v1.2.1)

## 📋 Recent Updates

### v1.2.1 (July 3, 2025) - Template Persistence Fix
- 🐛 **Fixed**: Template selection now properly persists after saving settings
- 🔧 **Improved**: Database column indexing for template storage
- ⚡ **Enhanced**: Session state synchronization for better user experience
- ✅ **Resolved**: Issue where template would revert to 'classic' after form submission
- 🧪 **Added**: Test scripts for template persistence verification

### v1.2.0 (July 2, 2025) - Multi-Template System
- 🎨 **Added**: 8 professional invoice templates (Classic, Modern, Creative, Corporate, Tech, Retail, Food, Service)
- 📄 **Enhanced**: Template preview and sample PDF generation
- 🏢 **Improved**: Company settings management with template selection
- 🎯 **Optimized**: Industry-specific template designs for UMKM needs

## 🙏 Acknowledgments

- Streamlit untuk framework yang amazing
- ReportLab untuk PDF generation
- Plotly untuk visualization yang beautiful
- UMKM Indonesia untuk inspirasi dan feedback

---

**Made with ❤️ for UMKM Indonesia** 🇮🇩
