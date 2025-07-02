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
        ["Dashboard", "Buat Invoice", "Data Customer", "Data Produk", "Laporan"]
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
        
        # Recent invoices
        st.subheader("Invoice Terbaru")
        recent_invoices = invoices_df.head(10)[['invoice_number', 'customer_name', 'issue_date', 'total', 'status']]
        st.dataframe(recent_invoices, use_container_width=True)
        
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
                        try:
                            st.session_state.db.add_product(product_name, unit_price, "Ditambah dari invoice")
                            st.success(f"✅ '{product_name}' berhasil disimpan ke master data!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                
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
                    pdf_data = st.session_state.pdf_generator.create_invoice_pdf(invoice_data, items_data)
                    
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
    
    # Display customers
    customers_df = st.session_state.db.get_customers()
    if len(customers_df) > 0:
        st.subheader("Daftar Customer")
        st.dataframe(customers_df, use_container_width=True)
    else:
        st.info("Belum ada customer yang terdaftar")

def product_management():
    st.header("📦 Data Produk")
    
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
                    st.session_state.db.add_product(name, price, description)
                    st.success("Produk berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.error("Nama dan harga produk wajib diisi")
    
    # Display products
    products_df = st.session_state.db.get_products()
    if len(products_df) > 0:
        st.subheader("Daftar Produk")
        st.dataframe(products_df, use_container_width=True)
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

if __name__ == "__main__":
    main()