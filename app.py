import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
from database import Database
from pdf_generator import InvoicePDFGenerator

# Initialize
if 'db' not in st.session_state:
    st.session_state.db = Database()

if 'pdf_generator' not in st.session_state:
    st.session_state.pdf_generator = InvoicePDFGenerator()

# Page config
st.set_page_config(
    page_title="Invoice Generator UMKM",
    page_icon="🧾",
    layout="wide"
)

def main():
    st.title("🧾 Invoice Generator untuk UMKM")
    st.markdown("---")
    
    # Sidebar navigation
    st.sidebar.title("Menu")
    page = st.sidebar.selectbox(
        "Pilih Halaman",
        ["Dashboard", "Buat Invoice", "Data Customer", "Data Produk", "Laporan", "Pengaturan"]
    )
    
    if page == "Dashboard":
        show_dashboard()
    elif page == "Buat Invoice":
        create_invoice_page()
    elif page == "Data Customer":
        customer_management()
    elif page == "Data Produk":
        product_management()
    elif page == "Laporan":
        reports_page()
    elif page == "Pengaturan":
        company_settings_page()

def show_dashboard():
    st.header("📊 Dashboard")
    
    # Get summary data
    invoices_df = st.session_state.db.get_invoices()
    
    if len(invoices_df) > 0:
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_invoices = len(invoices_df)
            st.metric("Total Invoice", total_invoices)
        
        with col2:
            total_revenue = invoices_df['total'].sum()
            st.metric("Total Revenue", f"Rp {total_revenue:,.0f}")
        
        with col3:
            pending_invoices = len(invoices_df[invoices_df['status'] == 'Draft'])
            st.metric("Invoice Draft", pending_invoices)
        
        with col4:
            avg_invoice = invoices_df['total'].mean()
            st.metric("Rata-rata Invoice", f"Rp {avg_invoice:,.0f}")
        
        # Recent invoices with pagination
        st.subheader("Invoice Terbaru")
        
        # Initialize pagination for dashboard
        if 'dashboard_invoice_page' not in st.session_state:
            st.session_state.dashboard_invoice_page = 0
        if 'dashboard_invoices_per_page' not in st.session_state:
            st.session_state.dashboard_invoices_per_page = 10
        
        # Pagination controls for recent invoices
        total_invoices_count = len(invoices_df)
        invoices_per_page = st.selectbox("Invoices per halaman", [5, 10, 20], 
                                       index=[5, 10, 20].index(st.session_state.dashboard_invoices_per_page),
                                       key="dashboard_invoices_per_page_select")
        
        if invoices_per_page != st.session_state.dashboard_invoices_per_page:
            st.session_state.dashboard_invoices_per_page = invoices_per_page
            st.session_state.dashboard_invoice_page = 0
            st.rerun()
        
        total_pages = (total_invoices_count - 1) // st.session_state.dashboard_invoices_per_page + 1 if total_invoices_count > 0 else 1
        
        # Ensure current page is valid
        if st.session_state.dashboard_invoice_page >= total_pages:
            st.session_state.dashboard_invoice_page = max(0, total_pages - 1)
        
        start_idx = st.session_state.dashboard_invoice_page * st.session_state.dashboard_invoices_per_page
        end_idx = min(start_idx + st.session_state.dashboard_invoices_per_page, total_invoices_count)
        
        # Display paginated invoices
        page_invoices = invoices_df.iloc[start_idx:end_idx][['invoice_number', 'customer_name', 'issue_date', 'total', 'status']]
        st.dataframe(page_invoices, use_container_width=True)
        
        # Pagination controls at bottom
        if total_invoices_count > st.session_state.dashboard_invoices_per_page:
            st.markdown("---")
            # Display pagination info
            st.write(f"Menampilkan {start_idx + 1}-{end_idx} dari {total_invoices_count} invoice")
            
            col_nav1, col_nav2, col_nav3, col_nav4, col_nav5 = st.columns([1, 1, 2, 1, 1])
            with col_nav1:
                if st.button("⏮️ First", disabled=st.session_state.dashboard_invoice_page == 0, key="dashboard_first", use_container_width=True):
                    st.session_state.dashboard_invoice_page = 0
                    st.rerun()
            with col_nav2:
                if st.button("◀️ Prev", disabled=st.session_state.dashboard_invoice_page == 0, key="dashboard_prev", use_container_width=True):
                    st.session_state.dashboard_invoice_page -= 1
                    st.rerun()
            with col_nav3:
                st.markdown(f"<div style='text-align: center; padding: 8px;'><strong>Page {st.session_state.dashboard_invoice_page + 1} of {total_pages}</strong></div>", unsafe_allow_html=True)
            with col_nav4:
                if st.button("▶️ Next", disabled=st.session_state.dashboard_invoice_page >= total_pages - 1, key="dashboard_next", use_container_width=True):
                    st.session_state.dashboard_invoice_page += 1
                    st.rerun()
            with col_nav5:
                if st.button("⏭️ Last", disabled=st.session_state.dashboard_invoice_page >= total_pages - 1, key="dashboard_last", use_container_width=True):
                    st.session_state.dashboard_invoice_page = total_pages - 1
                    st.rerun()
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Monthly revenue chart
            invoices_df['issue_date'] = pd.to_datetime(invoices_df['issue_date'])
            invoices_df['month'] = invoices_df['issue_date'].dt.to_period('M')
            monthly_revenue = invoices_df.groupby('month')['total'].sum().reset_index()
            monthly_revenue['month'] = monthly_revenue['month'].astype(str)
            
            fig_revenue = px.line(monthly_revenue, x='month', y='total', 
                                title='Revenue Bulanan')
            st.plotly_chart(fig_revenue, use_container_width=True)
        
        with col2:
            # Status distribution
            status_dist = invoices_df['status'].value_counts()
            fig_status = px.pie(values=status_dist.values, names=status_dist.index,
                              title='Status Invoice')
            st.plotly_chart(fig_status, use_container_width=True)
    
    else:
        st.info("Belum ada data invoice. Silakan buat invoice pertama Anda!")

def create_invoice_page():
    st.header("📝 Buat Invoice Baru")
    
    # Initialize items in session state
    if 'invoice_items' not in st.session_state:
        st.session_state.invoice_items = []
    
    # Initialize created invoice state
    if 'created_invoice_pdf' not in st.session_state:
        st.session_state.created_invoice_pdf = None
        st.session_state.created_invoice_number = None
    
    # Section 1: Add Items (Outside of form)
    st.subheader("Tambah Item Invoice")
    with st.expander("Tambah Item Baru", expanded=True):
        # Get products from database
        products_df = st.session_state.db.get_products()
        
        # Tab for choosing input method
        tab1, tab2 = st.tabs(["📦 Pilih dari Master Data", "✏️ Input Manual"])
        
        with tab1:
            if len(products_df) > 0:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    # Create options for selectbox
                    product_options = {}
                    for _, product in products_df.iterrows():
                        display_name = f"{product['name']} - Rp {product['price']:,.0f}"
                        product_options[display_name] = {
                            'name': product['name'],
                            'price': product['price']
                        }
                    
                    selected_product_display = st.selectbox(
                        "Pilih Produk", 
                        options=list(product_options.keys()),
                        key="selected_product"
                    )
                    
                    if selected_product_display:
                        selected_product = product_options[selected_product_display]
                        product_name_master = selected_product['name']
                        unit_price_master = selected_product['price']
                    else:
                        product_name_master = ""
                        unit_price_master = 0.0
                
                with col2:
                    quantity_master = st.number_input("Jumlah", min_value=1, value=1, key="quantity_master")
                
                with col3:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("➕ Tambah dari Master", type="secondary"):
                        if product_name_master and quantity_master > 0 and unit_price_master > 0:
                            st.session_state.invoice_items.append({
                                'product_name': product_name_master,
                                'quantity': quantity_master,
                                'unit_price': unit_price_master
                            })
                            st.success(f"✅ {product_name_master} berhasil ditambahkan!")
                            st.rerun()
                        else:
                            st.error("Pilih produk yang valid")
            else:
                st.info("💡 Belum ada produk di master data. Silakan tambah produk di menu 'Data Produk' atau gunakan input manual.")
        
        with tab2:
            col1, col2, col3, col4 = st.columns([3, 1, 2, 1])
            
            with col1:
                product_name = st.text_input("Nama Produk/Jasa", key="new_product_name")
            with col2:
                quantity = st.number_input("Jumlah", min_value=1, value=1, key="new_quantity")
            with col3:
                unit_price = st.number_input("Harga Satuan", min_value=0.0, value=0.0, key="new_unit_price")
            with col4:
                st.markdown("<br>", unsafe_allow_html=True)  # Add space
                if st.button("➕ Tambah Manual", type="secondary"):
                    if product_name and quantity > 0 and unit_price > 0:
                        st.session_state.invoice_items.append({
                            'product_name': product_name,
                            'quantity': quantity,
                            'unit_price': unit_price
                        })
                        st.success("✅ Item berhasil ditambahkan!")
                        # Clear the inputs by rerunning
                        st.rerun()
                    else:
                        st.error("Semua field harus diisi dengan nilai yang valid")
            
            # Option to save to master data
            if product_name and unit_price > 0:
                st.markdown("---")
                col_save, col_info = st.columns([1, 3])
                with col_save:
                    if st.button("💾 Simpan ke Master Data", type="secondary", use_container_width=True):
                        result = st.session_state.db.add_product(product_name, unit_price, "Ditambah dari invoice")
                        
                        if result['success']:
                            st.success(result['message'])
                            st.rerun()
                        else:
                            if 'existing_product' in result:
                                # Show warning for duplicate with existing product info
                                existing = result['existing_product']
                                st.warning(f"⚠️ {result['message']}")
                                
                                # Show option to use existing product
                                if st.button("📦 Gunakan Produk yang Ada", type="secondary", key="use_existing"):
                                    st.session_state.invoice_items.append({
                                        'product_name': existing['name'],
                                        'quantity': quantity,
                                        'unit_price': existing['price']
                                    })
                                    st.success(f"✅ {existing['name']} (dari master data) berhasil ditambahkan!")
                                    st.rerun()
                            else:
                                st.error(result['message'])
                
                with col_info:
                    st.info("💡 Simpan produk ini ke master data untuk memudahkan penggunaan di invoice selanjutnya")
    
    # Display current items
    if st.session_state.invoice_items:
        st.subheader("Item yang Ditambahkan")
        items_df = pd.DataFrame(st.session_state.invoice_items)
        items_df['Total'] = items_df['quantity'] * items_df['unit_price']
        
        # Format for display
        display_df = items_df.copy()
        display_df['unit_price'] = display_df['unit_price'].apply(lambda x: f"Rp {x:,.0f}")
        display_df['Total'] = display_df['Total'].apply(lambda x: f"Rp {x:,.0f}")
        display_df.columns = ['Nama Produk', 'Jumlah', 'Harga Satuan', 'Total']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns([1, 6])
        with col1:
            if st.button("🗑️ Hapus Semua", type="secondary"):
                st.session_state.invoice_items = []
                st.rerun()
        
        # Show subtotal
        subtotal = items_df['Total'].sum()
        st.metric("Subtotal", f"Rp {subtotal:,.0f}")
    
    # Section 2: Invoice Details Form
    st.subheader("Detail Invoice")
    with st.form("invoice_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            # Customer selection
            customers_df = st.session_state.db.get_customers()
            if len(customers_df) > 0:
                customer_options = dict(zip(customers_df['name'], customers_df['id']))
                selected_customer = st.selectbox("Pilih Customer", options=list(customer_options.keys()))
                customer_id = customer_options[selected_customer]
            else:
                st.warning("Belum ada customer. Silakan tambah customer terlebih dahulu.")
                customer_id = None
            
            # Dates
            issue_date = st.date_input("Tanggal Invoice", datetime.now())
            due_date = st.date_input("Tanggal Jatuh Tempo", datetime.now() + timedelta(days=30))
        
        with col2:
            # Tax rate
            tax_rate = st.number_input("Pajak (%)", min_value=0.0, max_value=100.0, value=11.0) / 100
            
            # Notes
            notes = st.text_area("Catatan")
        
        # Submit button
        submitted = st.form_submit_button("🧾 Buat Invoice", type="primary", use_container_width=True)
        
        if submitted:
            if not customer_id:
                st.error("Silakan pilih customer")
            elif not st.session_state.invoice_items:
                st.error("Silakan tambahkan minimal 1 item")
            else:
                try:
                    invoice_id, invoice_number = st.session_state.db.create_invoice(
                        customer_id=customer_id,
                        items=st.session_state.invoice_items,
                        issue_date=issue_date,
                        due_date=due_date,
                        tax_rate=tax_rate,
                        notes=notes
                    )
                    
                    st.success(f"✅ Invoice {invoice_number} berhasil dibuat!")
                    
                    # Generate PDF
                    invoice_data, items_data = st.session_state.db.get_invoice_details(invoice_id)
                    company_settings = st.session_state.db.get_company_settings()
                    pdf_data = st.session_state.pdf_generator.create_invoice_pdf(invoice_data, items_data, company_settings)
                    
                    # Store PDF data in session state
                    st.session_state.created_invoice_pdf = pdf_data
                    st.session_state.created_invoice_number = invoice_number
                    
                    # Clear items after successful creation
                    st.session_state.invoice_items = []
                    
                    # Force rerun to show download button
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # Download button (outside of form)
    if st.session_state.created_invoice_pdf is not None:
        st.markdown("---")
        st.subheader("📄 Download Invoice")
        
        st.download_button(
            label="📄 Download PDF Invoice",
            data=st.session_state.created_invoice_pdf,
            file_name=f"{st.session_state.created_invoice_number}.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )
        
        # Option to clear the PDF data
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("✨ Buat Invoice Baru", type="secondary", use_container_width=True):
                st.session_state.created_invoice_pdf = None
                st.session_state.created_invoice_number = None
                st.rerun()
        
        with col2:
            if st.button("📊 Lihat Dashboard", type="secondary", use_container_width=True):
                st.session_state.created_invoice_pdf = None
                st.session_state.created_invoice_number = None
                # This would need to change the page, but since we're using selectbox, 
                # we'll just clear the state
                st.info("Silakan pilih 'Dashboard' di menu sidebar")

def customer_management():
    st.header("👥 Data Customer")
    
    # Initialize pagination states
    if 'customer_page' not in st.session_state:
        st.session_state.customer_page = 0
    if 'customers_per_page' not in st.session_state:
        st.session_state.customers_per_page = 5
    
    # Add new customer
    with st.expander("Tambah Customer Baru"):
        with st.form("customer_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Nama Customer*", key="customer_name")
                email = st.text_input("Email", key="customer_email")
            with col2:
                phone = st.text_input("Telepon", key="customer_phone")
                address = st.text_area("Alamat", key="customer_address")
            
            if st.form_submit_button("Tambah Customer"):
                if name:
                    st.session_state.db.add_customer(name, email, phone, address)
                    st.success("Customer berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.error("Nama customer wajib diisi")
    
    # Display customers with CRUD actions
    customers_df = st.session_state.db.get_customers()
    if len(customers_df) > 0:
        st.subheader("Daftar Customer")
        
        # Controls row
        col_search, col_per_page = st.columns([3, 1])
        with col_search:
            search_term = st.text_input("🔍 Cari Customer", placeholder="Masukkan nama customer...")
        with col_per_page:
            customers_per_page = st.selectbox("Item per halaman", [5, 10, 20, 50], 
                                            index=[5, 10, 20, 50].index(st.session_state.customers_per_page))
            if customers_per_page != st.session_state.customers_per_page:
                st.session_state.customers_per_page = customers_per_page
                st.session_state.customer_page = 0  # Reset to first page
                st.rerun()
        
        # Apply search filter
        if search_term:
            filtered_customers = customers_df[customers_df['name'].str.contains(search_term, case=False, na=False)]
        else:
            filtered_customers = customers_df
        
        # Pagination logic
        total_customers = len(filtered_customers)
        total_pages = (total_customers - 1) // st.session_state.customers_per_page + 1 if total_customers > 0 else 1
        
        # Ensure current page is valid
        if st.session_state.customer_page >= total_pages:
            st.session_state.customer_page = max(0, total_pages - 1)
        
        start_idx = st.session_state.customer_page * st.session_state.customers_per_page
        end_idx = min(start_idx + st.session_state.customers_per_page, total_customers)
        
        # Display current page customers
        page_customers = filtered_customers.iloc[start_idx:end_idx]
        
        # Display customers table with action buttons
        for _, customer in page_customers.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                
                with col1:
                    st.write(f"**{customer['name']}**")
                    if customer['email']:
                        st.write(f"📧 {customer['email']}")
                    if customer['phone']:
                        st.write(f"📱 {customer['phone']}")
                
                with col2:
                    if customer['address']:
                        st.write(f"📍 {customer['address']}")
                
                with col3:
                    if st.button("✏️ Edit", key=f"edit_customer_{customer['id']}", type="secondary"):
                        st.session_state.edit_customer_id = customer['id']
                        st.rerun()
                
                with col4:
                    if st.button("🗑️ Hapus", key=f"delete_customer_{customer['id']}", type="secondary"):
                        st.session_state.delete_customer_confirm = True
                        st.session_state.delete_customer_id = customer['id']
                        st.rerun()
                
                # Show edit form directly below selected customer
                if hasattr(st.session_state, 'edit_customer_id') and st.session_state.edit_customer_id == customer['id']:
                    with st.expander(f"✏️ Edit Customer: {customer['name']}", expanded=True):
                        with st.form(f"edit_customer_form_{customer['id']}"):
                            col1_edit, col2_edit = st.columns(2)
                            with col1_edit:
                                edit_name = st.text_input("Nama Customer*", value=customer['name'])
                                edit_email = st.text_input("Email", value=customer['email'] or "")
                            with col2_edit:
                                edit_phone = st.text_input("Telepon", value=customer['phone'] or "")
                                edit_address = st.text_area("Alamat", value=customer['address'] or "")
                            
                            col_update, col_cancel = st.columns(2)
                            with col_update:
                                if st.form_submit_button("✏️ Update Customer", type="primary", use_container_width=True):
                                    if edit_name:
                                        result = st.session_state.db.update_customer(
                                            customer['id'], edit_name, edit_email, edit_phone, edit_address
                                        )
                                        if result['success']:
                                            st.success(result['message'])
                                            del st.session_state.edit_customer_id
                                            st.rerun()
                                        else:
                                            st.error(result['message'])
                                    else:
                                        st.error("Nama customer wajib diisi")
                            
                            with col_cancel:
                                if st.form_submit_button("❌ Batal", use_container_width=True):
                                    del st.session_state.edit_customer_id
                                    st.rerun()
                
                # Show delete confirmation directly below selected customer
                if hasattr(st.session_state, 'delete_customer_confirm') and st.session_state.delete_customer_confirm and hasattr(st.session_state, 'delete_customer_id') and st.session_state.delete_customer_id == customer['id']:
                    with st.expander(f"⚠️ Konfirmasi Hapus Customer: {customer['name']}", expanded=True):
                        st.warning(f"Apakah Anda yakin ingin menghapus customer **{customer['name']}**?")
                        st.write("Tindakan ini tidak dapat dibatalkan!")
                        
                        col_confirm, col_cancel = st.columns(2)
                        with col_confirm:
                            if st.button("🗑️ Ya, Hapus", type="primary", use_container_width=True, key=f"confirm_delete_customer_{customer['id']}"):
                                result = st.session_state.db.delete_customer(customer['id'])
                                if result['success']:
                                    st.success(result['message'])
                                else:
                                    st.error(result['message'])
                                del st.session_state.delete_customer_confirm
                                del st.session_state.delete_customer_id
                                st.rerun()
                        with col_cancel:
                            if st.button("❌ Batal", use_container_width=True, key=f"cancel_delete_customer_{customer['id']}"):
                                del st.session_state.delete_customer_confirm
                                del st.session_state.delete_customer_id
                                st.rerun()
                
                st.divider()
        
        # Pagination controls at bottom
        if total_customers > st.session_state.customers_per_page:
            st.markdown("---")
            # Display pagination info
            st.write(f"Menampilkan {start_idx + 1}-{end_idx} dari {total_customers} customer")
            
            col_nav1, col_nav2, col_nav3, col_nav4, col_nav5 = st.columns([1, 1, 2, 1, 1])
            with col_nav1:
                if st.button("⏮️ First", disabled=st.session_state.customer_page == 0, use_container_width=True):
                    st.session_state.customer_page = 0
                    st.rerun()
            with col_nav2:
                if st.button("◀️ Prev", disabled=st.session_state.customer_page == 0, use_container_width=True):
                    st.session_state.customer_page -= 1
                    st.rerun()
            with col_nav3:
                st.markdown(f"<div style='text-align: center; padding: 8px;'><strong>Page {st.session_state.customer_page + 1} of {total_pages}</strong></div>", unsafe_allow_html=True)
            with col_nav4:
                if st.button("▶️ Next", disabled=st.session_state.customer_page >= total_pages - 1, use_container_width=True):
                    st.session_state.customer_page += 1
                    st.rerun()
            with col_nav5:
                if st.button("⏭️ Last", disabled=st.session_state.customer_page >= total_pages - 1, use_container_width=True):
                    st.session_state.customer_page = total_pages - 1
                    st.rerun()
    else:
        st.info("Belum ada customer yang terdaftar")

def product_management():
    st.header("📦 Data Produk")
    
    # Initialize pagination states
    if 'product_page' not in st.session_state:
        st.session_state.product_page = 0
    if 'products_per_page' not in st.session_state:
        st.session_state.products_per_page = 5
    
    # Add new product
    with st.expander("Tambah Produk Baru"):
        with st.form("product_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Nama Produk*")
                price = st.number_input("Harga*", min_value=0.0)
            with col2:
                description = st.text_area("Deskripsi")
            
            if st.form_submit_button("Tambah Produk"):
                if name and price > 0:
                    result = st.session_state.db.add_product(name, price, description)
                    
                    if result['success']:
                        st.success(result['message'])
                        st.rerun()
                    else:
                        if 'existing_product' in result:
                            st.warning(f"⚠️ {result['message']}")
                        else:
                            st.error(result['message'])
                else:
                    st.error("Nama dan harga produk wajib diisi")
    
    # Display products with CRUD actions
    products_df = st.session_state.db.get_products()
    if len(products_df) > 0:
        st.subheader("Daftar Produk")
        
        # Controls row
        col_search, col_per_page = st.columns([3, 1])
        with col_search:
            search_term = st.text_input("🔍 Cari Produk", placeholder="Masukkan nama produk...")
        with col_per_page:
            products_per_page = st.selectbox("Item per halaman", [5, 10, 20, 50], 
                                           index=[5, 10, 20, 50].index(st.session_state.products_per_page),
                                           key="products_per_page_select")
            if products_per_page != st.session_state.products_per_page:
                st.session_state.products_per_page = products_per_page
                st.session_state.product_page = 0  # Reset to first page
                st.rerun()
        
        # Apply search filter
        if search_term:
            filtered_products = products_df[products_df['name'].str.contains(search_term, case=False, na=False)]
        else:
            filtered_products = products_df
        
        # Sort options
        col_sort, col_order = st.columns(2)
        with col_sort:
            sort_by = st.selectbox("Urutkan berdasarkan", ["name", "price", "created_at"], index=0)
        with col_order:
            sort_order = st.selectbox("Urutan", ["Ascending", "Descending"], index=0)
        
        ascending = sort_order == "Ascending"
        filtered_products = filtered_products.sort_values(by=sort_by, ascending=ascending)
        
        # Pagination logic
        total_products = len(filtered_products)
        total_pages = (total_products - 1) // st.session_state.products_per_page + 1 if total_products > 0 else 1
        
        # Ensure current page is valid
        if st.session_state.product_page >= total_pages:
            st.session_state.product_page = max(0, total_pages - 1)
        
        start_idx = st.session_state.product_page * st.session_state.products_per_page
        end_idx = min(start_idx + st.session_state.products_per_page, total_products)
        
        # Display current page products
        page_products = filtered_products.iloc[start_idx:end_idx]
        
        # Display products table with action buttons
        for _, product in page_products.iterrows():
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                
                with col1:
                    st.write(f"**{product['name']}**")
                    if product['description']:
                        st.write(f"📝 {product['description']}")
                
                with col2:
                    st.write(f"💰 **Rp {product['price']:,.0f}**")
                    st.write(f"📅 {product['created_at'][:10]}")
                
                with col3:
                    if st.button("✏️ Edit", key=f"edit_product_{product['id']}", type="secondary"):
                        st.session_state.edit_product_id = product['id']
                        st.rerun()
                
                with col4:
                    if st.button("🗑️ Hapus", key=f"delete_product_{product['id']}", type="secondary"):
                        st.session_state.delete_product_confirm = True
                        st.session_state.delete_product_id = product['id']
                        st.rerun()
                
                # Show edit form directly below selected product
                if hasattr(st.session_state, 'edit_product_id') and st.session_state.edit_product_id == product['id']:
                    with st.expander(f"✏️ Edit Produk: {product['name']}", expanded=True):
                        with st.form(f"edit_product_form_{product['id']}"):
                            col1_edit, col2_edit = st.columns(2)
                            with col1_edit:
                                edit_name = st.text_input("Nama Produk*", value=product['name'])
                                edit_price = st.number_input("Harga*", min_value=0.0, value=float(product['price']))
                            with col2_edit:
                                edit_description = st.text_area("Deskripsi", value=product['description'] or "")
                            
                            col_update, col_cancel = st.columns(2)
                            with col_update:
                                if st.form_submit_button("✏️ Update Produk", type="primary", use_container_width=True):
                                    if edit_name and edit_price > 0:
                                        result = st.session_state.db.update_product(
                                            product['id'], edit_name, edit_price, edit_description
                                        )
                                        if result['success']:
                                            st.success(result['message'])
                                            del st.session_state.edit_product_id
                                            st.rerun()
                                        else:
                                            st.error(result['message'])
                                    else:
                                        st.error("Nama dan harga produk wajib diisi")
                            
                            with col_cancel:
                                if st.form_submit_button("❌ Batal", use_container_width=True):
                                    del st.session_state.edit_product_id
                                    st.rerun()
                
                # Show delete confirmation directly below selected product
                if hasattr(st.session_state, 'delete_product_confirm') and st.session_state.delete_product_confirm and hasattr(st.session_state, 'delete_product_id') and st.session_state.delete_product_id == product['id']:
                    with st.expander(f"⚠️ Konfirmasi Hapus Produk: {product['name']}", expanded=True):
                        st.warning(f"Apakah Anda yakin ingin menghapus produk **{product['name']}**?")
                        st.write("Tindakan ini tidak dapat dibatalkan!")
                        
                        col_confirm, col_cancel = st.columns(2)
                        with col_confirm:
                            if st.button("🗑️ Ya, Hapus", type="primary", use_container_width=True, key=f"confirm_delete_product_{product['id']}"):
                                result = st.session_state.db.delete_product(product['id'])
                                if result['success']:
                                    st.success(result['message'])
                                else:
                                    st.error(result['message'])
                                del st.session_state.delete_product_confirm
                                del st.session_state.delete_product_id
                                st.rerun()
                        with col_cancel:
                            if st.button("❌ Batal", use_container_width=True, key=f"cancel_delete_product_{product['id']}"):
                                del st.session_state.delete_product_confirm
                                del st.session_state.delete_product_id
                                st.rerun()
                
                st.divider()
        
        # Pagination controls at bottom
        if total_products > st.session_state.products_per_page:
            st.markdown("---")
            # Display pagination info
            st.write(f"Menampilkan {start_idx + 1}-{end_idx} dari {total_products} produk")
            
            col_nav1, col_nav2, col_nav3, col_nav4, col_nav5 = st.columns([1, 1, 2, 1, 1])
            with col_nav1:
                if st.button("⏮️ First", disabled=st.session_state.product_page == 0, key="product_first", use_container_width=True):
                    st.session_state.product_page = 0
                    st.rerun()
            with col_nav2:
                if st.button("◀️ Prev", disabled=st.session_state.product_page == 0, key="product_prev", use_container_width=True):
                    st.session_state.product_page -= 1
                    st.rerun()
            with col_nav3:
                st.markdown(f"<div style='text-align: center; padding: 8px;'><strong>Page {st.session_state.product_page + 1} of {total_pages}</strong></div>", unsafe_allow_html=True)
            with col_nav4:
                if st.button("▶️ Next", disabled=st.session_state.product_page >= total_pages - 1, key="product_next", use_container_width=True):
                    st.session_state.product_page += 1
                    st.rerun()
            with col_nav5:
                if st.button("⏭️ Last", disabled=st.session_state.product_page >= total_pages - 1, key="product_last", use_container_width=True):
                    st.session_state.product_page = total_pages - 1
                    st.rerun()
        
        # Statistics
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Produk", len(products_df))
        with col2:
            avg_price = products_df['price'].mean()
            st.metric("Harga Rata-rata", f"Rp {avg_price:,.0f}")
        with col3:
            max_price = products_df['price'].max()
            st.metric("Harga Tertinggi", f"Rp {max_price:,.0f}")
        with col4:
            min_price = products_df['price'].min()
            st.metric("Harga Terendah", f"Rp {min_price:,.0f}")
            
    else:
        st.info("Belum ada produk yang terdaftar")

def reports_page():
    st.header("📈 Laporan")
    
    # Date range filter
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Dari Tanggal", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("Sampai Tanggal", datetime.now())
    
    # Get sales summary
    sales_df = st.session_state.db.get_sales_summary(start_date, end_date)
    
    if len(sales_df) > 0:
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_sales = sales_df['total_sales'].sum()
            st.metric("Total Penjualan", f"Rp {total_sales:,.0f}")
        
        with col2:
            total_invoices = sales_df['invoice_count'].sum()
            st.metric("Total Invoice", int(total_invoices))
        
        with col3:
            avg_per_invoice = total_sales / total_invoices if total_invoices > 0 else 0
            st.metric("Rata-rata per Invoice", f"Rp {avg_per_invoice:,.0f}")
        
        with col4:
            total_tax = sales_df['total_tax'].sum()
            st.metric("Total Pajak", f"Rp {total_tax:,.0f}")
        
        # Charts
        fig = px.bar(sales_df, x='date', y='total_sales', 
                    title='Penjualan Harian')
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed table
        st.subheader("Detail Laporan")
        st.dataframe(sales_df, use_container_width=True)
        
        # Export to Excel (outside of any form)
        if st.button("Export ke Excel"):
            try:
                # Create Excel file in memory
                import io
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    sales_df.to_excel(writer, index=False, sheet_name='Laporan Penjualan')
                
                excel_data = output.getvalue()
                st.download_button(
                    label="📊 Download Excel",
                    data=excel_data,
                    file_name=f"laporan_penjualan_{start_date}_to_{end_date}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            except Exception as e:
                st.error(f"Error creating Excel file: {str(e)}")
    
    else:
        st.info("Tidak ada data untuk periode yang dipilih")

def company_settings_page():
    st.header("⚙️ Pengaturan Perusahaan")
    
    # Get current company settings
    company_info = st.session_state.db.get_company_settings()
    
    with st.form("company_settings_form"):
        st.subheader("Informasi Perusahaan")
        st.write("Informasi ini akan muncul di PDF invoice yang dihasilkan.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            company_name = st.text_input(
                "Nama Perusahaan*", 
                value=company_info.get('name', 'Nama Perusahaan Anda'),
                help="Nama perusahaan yang akan muncul di header invoice"
            )
            
            phone = st.text_input(
                "Telepon", 
                value=company_info.get('phone', '+62 xxx-xxxx-xxxx'),
                help="Nomor telepon perusahaan"
            )
            
            email = st.text_input(
                "Email", 
                value=company_info.get('email', 'email@perusahaan.com'),
                help="Email perusahaan"
            )
        
        with col2:
            address = st.text_area(
                "Alamat Perusahaan", 
                value=company_info.get('address', 'Alamat Perusahaan\nKota, Kode Pos'),
                height=100,
                help="Alamat lengkap perusahaan"
            )
            
            website = st.text_input(
                "Website (Opsional)", 
                value=company_info.get('website', ''),
                help="Website perusahaan (opsional)"
            )
            
            npwp = st.text_input(
                "NPWP (Opsional)", 
                value=company_info.get('npwp', ''),
                help="Nomor NPWP perusahaan (opsional)"
            )
        
        # Additional settings
        st.subheader("Pengaturan Tambahan")
        
        col3, col4 = st.columns(2)
        
        with col3:
            default_tax_rate = st.number_input(
                "Rate Pajak Default (%)", 
                min_value=0.0, 
                max_value=100.0, 
                value=company_info.get('default_tax_rate', 11.0),
                step=0.1,
                help="Rate pajak default untuk invoice baru"
            )
        
        with col4:
            default_due_days = st.number_input(
                "Jatuh Tempo Default (Hari)", 
                min_value=1, 
                max_value=365, 
                value=company_info.get('default_due_days', 30),
                help="Jumlah hari default untuk jatuh tempo invoice"
            )
        
        # Submit button
        submitted = st.form_submit_button("💾 Simpan Pengaturan", type="primary", use_container_width=True)
        
        if submitted:
            if company_name:
                result = st.session_state.db.update_company_settings(
                    name=company_name,
                    address=address,
                    phone=phone,
                    email=email,
                    website=website,
                    npwp=npwp,
                    default_tax_rate=default_tax_rate,
                    default_due_days=default_due_days
                )
                if result['success']:
                    st.success("✅ Pengaturan perusahaan berhasil disimpan!")
                    st.rerun()
                else:
                    st.error(f"❌ Error: {result['message']}")
            else:
                st.error("Nama perusahaan wajib diisi")
    
    # Preview section
    st.markdown("---")
    st.subheader("👁️ Preview Informasi Perusahaan")
    
    col_preview1, col_preview2 = st.columns(2)
    
    with col_preview1:
        st.write("**Informasi yang akan muncul di PDF:**")
        preview_info = f"""
        **{company_info.get('name', 'Nama Perusahaan Anda')}**  
        📍 {company_info.get('address', 'Alamat Perusahaan')}  
        📞 {company_info.get('phone', '+62 xxx-xxxx-xxxx')}  
        📧 {company_info.get('email', 'email@perusahaan.com')}
        """
        if company_info.get('website'):
            preview_info += f"  \n🌐 {company_info['website']}"
        if company_info.get('npwp'):
            preview_info += f"  \n🆔 NPWP: {company_info['npwp']}"
        
        st.markdown(preview_info)
    
    with col_preview2:
        st.write("**Pengaturan Default:**")
        st.write(f"💰 Rate Pajak: {company_info.get('default_tax_rate', 11.0)}%")
        st.write(f"📅 Jatuh Tempo: {company_info.get('default_due_days', 30)} hari")

if __name__ == "__main__":
    main()