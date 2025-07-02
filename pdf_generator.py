from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from datetime import datetime
import io

class InvoicePDFGenerator:
    def __init__(self):
        self.page_size = A4
        self.styles = getSampleStyleSheet()
        
    def create_invoice_pdf(self, invoice_data, items_data, company_info=None):
        """Generate PDF invoice"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=self.page_size)
        
        # Default company info
        if not company_info:
            company_info = {
                'name': 'Nama Perusahaan Anda',
                'address': 'Alamat Perusahaan\nKota, Kode Pos',
                'phone': '+62 xxx-xxxx-xxxx',
                'email': 'email@perusahaan.com'
            }
        
        story = []
        
        # Header with company info
        header_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            textColor=colors.darkblue
        )
        
        company_style = ParagraphStyle(
            'Company',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=20
        )
        
        # Company Header
        story.append(Paragraph(company_info['name'], header_style))
        story.append(Paragraph(f"{company_info['address']}<br/>{company_info['phone']}<br/>{company_info['email']}", company_style))
        
        # Invoice Title
        invoice_title = ParagraphStyle(
            'InvoiceTitle',
            parent=self.styles['Heading2'],
            fontSize=18,
            spaceAfter=20,
            textColor=colors.darkred
        )
        story.append(Paragraph("INVOICE", invoice_title))
        
        # Invoice details table
        invoice_details = [
            ['Invoice Number:', str(invoice_data['invoice_number'])],
            ['Issue Date:', str(invoice_data['issue_date'])],
            ['Due Date:', str(invoice_data['due_date'])],
            ['Status:', str(invoice_data['status'])]
        ]
        
        invoice_table = Table(invoice_details, colWidths=[2*inch, 3*inch])
        invoice_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(invoice_table)
        story.append(Spacer(1, 20))
        
        # Customer info
        customer_style = ParagraphStyle(
            'Customer',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=20
        )
        
        customer_info = f"""
        <b>Bill To:</b><br/>
        {invoice_data['customer_name']}<br/>
        {invoice_data.get('address', '')}<br/>
        {invoice_data.get('phone', '')}<br/>
        {invoice_data.get('email', '')}
        """
        story.append(Paragraph(customer_info, customer_style))
        
        # Items table
        items_header = ['Item', 'Qty', 'Unit Price', 'Total']
        items_list = [items_header]
        
        for _, item in items_data.iterrows():
            items_list.append([
                str(item['product_name']),
                str(int(item['quantity'])),
                f"Rp {item['unit_price']:,.0f}",
                f"Rp {item['total_price']:,.0f}"
            ])
        
        # Summary rows
        subtotal = invoice_data['subtotal']
        tax_rate = invoice_data['tax_rate'] * 100
        tax_amount = invoice_data['tax_amount']
        total = invoice_data['total']
        
        items_list.extend([
            ['', '', 'Subtotal:', f"Rp {subtotal:,.0f}"],
            ['', '', f'Tax ({tax_rate:.0f}%):', f"Rp {tax_amount:,.0f}"],
            ['', '', 'TOTAL:', f"Rp {total:,.0f}"]
        ])
        
        items_table = Table(items_list, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
        items_table.setStyle(TableStyle([
            # Header style
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows
            ('FONTNAME', (0, 1), (-1, -4), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -4), 10),
            ('GRID', (0, 0), (-1, -4), 1, colors.black),
            
            # Summary section
            ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, -3), (-1, -1), 11),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('GRID', (2, -3), (-1, -1), 1, colors.black),
        ]))
        
        story.append(items_table)
        
        # Notes
        if invoice_data.get('notes'):
            story.append(Spacer(1, 20))
            notes_style = ParagraphStyle(
                'Notes',
                parent=self.styles['Normal'],
                fontSize=10,
                spaceAfter=20
            )
            story.append(Paragraph(f"<b>Notes:</b><br/>{invoice_data['notes']}", notes_style))
        
        # Footer
        story.append(Spacer(1, 30))
        footer_style = ParagraphStyle(
            'Footer',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.grey
        )
        story.append(Paragraph("Thank you for your business!", footer_style))
        
        # Build PDF
        doc.build(story)
        
        # Get PDF data
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data