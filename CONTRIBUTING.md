# 🤝 Contributing to Invoice Generator UMKM

Terima kasih atas interest Anda untuk berkontribusi! Setiap kontribusi sangat dihargai.

## 📋 How to Contribute

### 🐛 Bug Reports
Jika menemukan bug, silakan buat issue dengan:
- **Bug description** yang jelas
- **Steps to reproduce** 
- **Expected vs actual behavior**
- **Screenshots** (jika applicable)
- **Environment details** (OS, Python version, dll)

### ✨ Feature Requests  
Untuk request fitur baru:
- **Feature description** yang detail
- **Use case** atau problem yang diselesaikan
- **Mockups** atau wireframes (jika ada)
- **Priority level** (nice-to-have vs must-have)

### 🔧 Code Contributions

#### 1. **Fork & Clone**
```bash
# Fork repository di GitHub
git clone https://github.com/giangianna14/invoice-generator-umkm.git
cd invoice-generator-umkm
```

#### 2. **Setup Development Environment**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install black flake8 pytest
```

#### 3. **Create Feature Branch**
```bash
git checkout -b feature/your-feature-name
# atau
git checkout -b bugfix/bug-description
```

#### 4. **Development Guidelines**

**Code Style:**
- Gunakan **Python 3.8+**
- Follow **PEP 8** style guide
- Use **Black** untuk formatting
- Add **docstrings** untuk functions
- Write **meaningful variable names**

**Commit Messages:**
```bash
# Good commit messages
git commit -m "✨ Add WhatsApp integration feature"
git commit -m "🐛 Fix PDF generation encoding issue"  
git commit -m "📚 Update documentation for installation"
git commit -m "🔧 Improve database connection handling"
```

**Testing:**
```bash
# Run tests before committing
python -m pytest tests/
```

#### 5. **Submit Pull Request**
- **Clear title** dan description
- **Link related issues** (#123)
- **Screenshots** untuk UI changes
- **Test coverage** untuk new features

## 🎯 Development Priorities

### 🔥 High Priority
1. **Payment Integration** (Midtrans/QRIS)
2. **WhatsApp Integration** 
3. **Mobile Responsiveness**
4. **Data Export Improvements**

### 🔄 Medium Priority  
1. **Multi-user Support**
2. **Inventory Management**
3. **Advanced Reporting**
4. **Email Integration**

### 💡 Nice to Have
1. **AI-powered Insights**
2. **Mobile App (React Native)**
3. **Marketplace Integration**
4. **Advanced Customization**

## 📁 Project Structure

```
invoice_generator/
├── app.py                 # Main Streamlit application
├── database.py           # Database operations & models
├── pdf_generator.py      # PDF generation logic
├── requirements.txt      # Python dependencies
├── tests/               # Test files
│   ├── test_database.py
│   ├── test_pdf.py
│   └── test_app.py
├── docs/               # Documentation
├── .github/           # GitHub templates
│   ├── ISSUE_TEMPLATE/
│   └── pull_request_template.md
└── assets/           # Static assets (images, etc)
```

## 🧪 Testing Guidelines

### Unit Tests
```bash
# Test database operations
python -m pytest tests/test_database.py

# Test PDF generation  
python -m pytest tests/test_pdf.py

# Test Streamlit app
python -m pytest tests/test_app.py
```

### Manual Testing
1. **Invoice Creation** - End-to-end flow
2. **PDF Generation** - Various scenarios
3. **Data Import/Export** - Excel compatibility
4. **Browser Compatibility** - Chrome, Firefox, Safari
5. **Mobile Testing** - Responsive design

## 🔒 Security Guidelines

- **No hardcoded secrets** - Use environment variables
- **Validate user input** - Prevent SQL injection
- **Sanitize file uploads** - Check file types
- **Secure database** - Use parameterized queries
- **HTTPS only** - For production deployment

## 📚 Documentation Standards

### Code Documentation
```python
def create_invoice(customer_id: int, items: List[dict], 
                  issue_date: date, due_date: date) -> Tuple[int, str]:
    """
    Create new invoice with items.
    
    Args:
        customer_id: ID of the customer
        items: List of invoice items with quantity and price
        issue_date: Invoice issue date
        due_date: Payment due date
        
    Returns:
        Tuple of (invoice_id, invoice_number)
        
    Raises:
        ValueError: If customer_id is invalid
        DatabaseError: If database operation fails
    """
```

### README Updates
- Keep **installation steps** updated
- Add **screenshots** untuk new features  
- Update **feature list** saat ada additions
- Include **troubleshooting** section

## 🏆 Recognition

Contributors akan mendapat recognition melalui:
- **GitHub Contributors** list
- **CHANGELOG.md** mentions
- **Social media** shoutouts
- **LinkedIn** recommendations (jika applicable)

## 💬 Communication

- **GitHub Issues** - For bugs and features
- **GitHub Discussions** - For general questions
- **Email** - giangianna14@outlook.com untuk urgent matters

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Happy Contributing! 🎉**

Together we can make the best invoice generator for Indonesian SMEs! 🇮🇩
