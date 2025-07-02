# 🧾 Invoice Generator UMKM

Invoice Generator aplikasi untuk UMKM Indonesia yang dibuat dengan Python dan Streamlit. Aplikasi ini membantu usaha kecil dan menengah untuk membuat invoice professional, mengelola customer, dan tracking penjualan.

## ✨ Features

### Core Features
- ✅ **Generate Invoice PDF** - Format profesional dengan logo perusahaan
- ✅ **Customer Database** - Simpan data customer dengan lengkap
- ✅ **Product Management** - Kelola produk/jasa dengan harga
- ✅ **Sales Tracking** - Track semua invoice dan status
- ✅ **Financial Reports** - Dashboard dengan metrik penting
- ✅ **Export to Excel** - Export laporan ke format Excel

### Advanced Features
- 📦 **Master Data Integration** - Pilih produk dari database atau input manual
- 📊 **Dashboard Analytics** - Visualisasi data dengan charts
- 💾 **Auto-save Products** - Simpan produk baru ke master data
- 📱 **Responsive Design** - Akses dari desktop atau mobile
- 🎨 **Professional PDF** - Invoice dengan layout bisnis yang rapi

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
http://localhost:8501
```

## 📁 Project Structure

```
invoice_generator/
├── app.py              # Main Streamlit application
├── database.py         # Database operations
├── pdf_generator.py    # PDF generation logic
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── invoice_system.db  # SQLite database (auto-created)
```

## 🛠️ Tech Stack

- **Backend**: Python
- **Web Framework**: Streamlit
- **Database**: SQLite
- **PDF Generation**: ReportLab
- **Data Processing**: Pandas
- **Visualization**: Plotly
- **Excel Export**: OpenPyXL

## 📋 Dependencies

```
streamlit==1.28.1
pandas==2.1.3
reportlab==4.0.7
openpyxl==3.1.2
plotly==5.17.0
pillow==10.1.0
python-dateutil==2.8.2
```

## 📖 How to Use

### 1. **Setup Data Master**
- Tambah customer di menu "Data Customer"
- Tambah produk/jasa di menu "Data Produk"

### 2. **Buat Invoice**
- Pilih menu "Buat Invoice"
- Tambah item dari master data atau input manual
- Isi detail invoice (customer, tanggal, pajak)
- Generate dan download PDF

### 3. **Monitor Business**
- Lihat dashboard untuk overview bisnis
- Check laporan penjualan berkala
- Export data ke Excel untuk analisis lanjut

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

### Phase 1 (Current)
- ✅ Basic invoice generation
- ✅ Customer & product management
- ✅ PDF export
- ✅ Basic reporting

### Phase 2 (Next)
- 💳 Payment integration (Midtrans/QRIS)
- 📱 WhatsApp integration
- 🔄 Recurring invoices
- 👥 Multi-user support

### Phase 3 (Future)
- 📦 Inventory management
- 🏪 E-commerce integration
- 🤖 AI-powered insights
- ☁️ Cloud sync

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

Jika ada pertanyaan atau butuh bantuan:
- 📧 Email: support@invoicegenerator.com
- 💬 WhatsApp: +62 xxx-xxxx-xxxx
- 🐛 Issues: [GitHub Issues](https://github.com/username/invoice-generator-umkm/issues)

## 🙏 Acknowledgments

- Streamlit untuk framework yang amazing
- ReportLab untuk PDF generation
- Plotly untuk visualization yang beautiful
- UMKM Indonesia untuk inspirasi dan feedback

---

**Made with ❤️ for UMKM Indonesia** 🇮🇩
