from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
from datetime import datetime
import io

class TemplatedInvoicePDFGenerator:
    def __init__(self):
        self.page_size = A4
        self.styles = getSampleStyleSheet()
        self.templates = {
            'classic': 'Template Klasik Profesional',
            'modern': 'Template Modern Minimalis',
            'creative': 'Template Kreatif & Colorful',
            'corporate': 'Template Corporate Formal',
            'tech': 'Template Tech & Digital',
            'retail': 'Template Retail & Fashion',
            'food': 'Template Food & Beverage',
            'service': 'Template Jasa & Konsultasi'
        }
    
    def get_available_templates(self):
        """Get list of available templates"""
        return self.templates
    
    def create_invoice_pdf(self, invoice_data, items_data, company_info=None, template='classic'):
        """Generate PDF invoice with selected template"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=self.page_size, 
                               topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Format company info
        company_info = self._format_company_info(company_info)
        
        # Generate story based on template
        if template == 'classic':
            story = self._create_classic_template(invoice_data, items_data, company_info)
        elif template == 'modern':
            story = self._create_modern_template(invoice_data, items_data, company_info)
        elif template == 'creative':
            story = self._create_creative_template(invoice_data, items_data, company_info)
        elif template == 'corporate':
            story = self._create_corporate_template(invoice_data, items_data, company_info)
        elif template == 'tech':
            story = self._create_tech_template(invoice_data, items_data, company_info)
        elif template == 'retail':
            story = self._create_retail_template(invoice_data, items_data, company_info)
        elif template == 'food':
            story = self._create_food_template(invoice_data, items_data, company_info)
        elif template == 'service':
            story = self._create_service_template(invoice_data, items_data, company_info)
        else:
            story = self._create_classic_template(invoice_data, items_data, company_info)
        
        # Build PDF
        doc.build(story)
        
        # Get PDF data
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return pdf_data
    
    def _format_company_info(self, company_info):
        """Format company info with defaults"""
        if not company_info:
            return {
                'name': 'Nama Perusahaan Anda',
                'address': 'Alamat Perusahaan\nKota, Kode Pos',
                'phone': '+62 xxx-xxxx-xxxx',
                'email': 'email@perusahaan.com'
            }
        
        formatted_info = {
            'name': company_info.get('name', 'Nama Perusahaan Anda'),
            'address': company_info.get('address', 'Alamat Perusahaan\nKota, Kode Pos'),
            'phone': company_info.get('phone', '+62 xxx-xxxx-xxxx'),
            'email': company_info.get('email', 'email@perusahaan.com')
        }
        
        if company_info.get('website'):
            formatted_info['website'] = company_info['website']
        if company_info.get('npwp'):
            formatted_info['npwp'] = company_info['npwp']
            
        return formatted_info
    
    def _create_classic_template(self, invoice_data, items_data, company_info):
        """Classic Professional Template - Traditional business style"""
        story = []
        
        # Header
        header_style = ParagraphStyle(
            'ClassicHeader',
            parent=self.styles['Heading1'],
            fontSize=28,
            textColor=colors.darkblue,
            spaceAfter=20,
            alignment=1  # Center
        )
        
        company_style = ParagraphStyle(
            'ClassicCompany',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=30,
            alignment=1  # Center
        )
        
        # Company Header
        story.append(Paragraph(company_info['name'], header_style))
        company_details = f"{company_info['address']}<br/>{company_info['phone']}<br/>{company_info['email']}"
        if company_info.get('website'):
            company_details += f"<br/>{company_info['website']}"
        if company_info.get('npwp'):
            company_details += f"<br/>NPWP: {company_info['npwp']}"
        story.append(Paragraph(company_details, company_style))
        
        # Invoice Title
        invoice_title_style = ParagraphStyle(
            'ClassicInvoiceTitle',
            parent=self.styles['Heading2'],
            fontSize=24,
            textColor=colors.darkred,
            spaceAfter=30,
            alignment=1
        )
        story.append(Paragraph("INVOICE", invoice_title_style))
        
        # Invoice and Customer Info in Table
        info_data = [
            ['Invoice Number:', str(invoice_data['invoice_number']), 'Bill To:', str(invoice_data['customer_name'])],
            ['Issue Date:', str(invoice_data['issue_date']), 'Address:', str(invoice_data.get('address', ''))],
            ['Due Date:', str(invoice_data['due_date']), 'Phone:', str(invoice_data.get('phone', ''))],
            ['Status:', str(invoice_data['status']), 'Email:', str(invoice_data.get('email', ''))]
        ]
        
        info_table = Table(info_data, colWidths=[1.5*inch, 2*inch, 1*inch, 2.5*inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (1, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (3, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 30))
        
        # Items table
        story.extend(self._create_items_table(invoice_data, items_data, 'classic'))
        
        # Footer
        story.append(Spacer(1, 30))
        footer_style = ParagraphStyle(
            'ClassicFooter',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.grey,
            alignment=1
        )
        story.append(Paragraph("Thank you for your business!", footer_style))
        
        return story
    
    def _create_modern_template(self, invoice_data, items_data, company_info):
        """Modern Minimalist Template - Clean and contemporary"""
        story = []
        
        # Header with line separator
        header_style = ParagraphStyle(
            'ModernHeader',
            parent=self.styles['Heading1'],
            fontSize=32,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=10,
            leftIndent=0
        )
        
        # Company name
        story.append(Paragraph(company_info['name'], header_style))
        
        # Separator line
        line_table = Table([['', '']], colWidths=[6*inch, 1*inch])
        line_table.setStyle(TableStyle([
            ('LINEBELOW', (0, 0), (0, 0), 3, colors.HexColor('#3498DB')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(line_table)
        story.append(Spacer(1, 20))
        
        # Invoice title and company info side by side
        header_data = [
            [Paragraph("INVOICE", ParagraphStyle('ModernInvoiceTitle', parent=self.styles['Heading1'], 
                                               fontSize=28, textColor=colors.HexColor('#E74C3C'))),
             Paragraph(f"{company_info['address']}<br/>{company_info['phone']}<br/>{company_info['email']}" + 
                      (f"<br/>{company_info['website']}" if company_info.get('website') else ""),
                      ParagraphStyle('ModernCompanyInfo', parent=self.styles['Normal'], 
                                   fontSize=10, alignment=2))]
        ]
        
        header_table = Table(header_data, colWidths=[3.5*inch, 3.5*inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 30))
        
        # Modern info cards
        info_card_data = [
            ['INVOICE #', 'DATE', 'DUE DATE', 'STATUS'],
            [str(invoice_data['invoice_number']), str(invoice_data['issue_date']), 
             str(invoice_data['due_date']), str(invoice_data['status'])]
        ]
        
        info_card_table = Table(info_card_data, colWidths=[1.75*inch, 1.75*inch, 1.75*inch, 1.75*inch])
        info_card_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ECF0F1')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#2C3E50')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white]),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(info_card_table)
        story.append(Spacer(1, 20))
        
        # Customer info
        customer_style = ParagraphStyle(
            'ModernCustomer',
            parent=self.styles['Normal'],
            fontSize=11,
            spaceAfter=20,
            leftIndent=0
        )
        
        customer_info = f"""
        <b>BILL TO:</b><br/>
        <b>{invoice_data['customer_name']}</b><br/>
        {invoice_data.get('address', '')}<br/>
        {invoice_data.get('phone', '')}<br/>
        {invoice_data.get('email', '')}
        """
        story.append(Paragraph(customer_info, customer_style))
        
        # Items table
        story.extend(self._create_items_table(invoice_data, items_data, 'modern'))
        
        return story
    
    def _create_creative_template(self, invoice_data, items_data, company_info):
        """Creative Colorful Template - For creative industries"""
        story = []
        
        # Creative header with gradient-like effect
        header_style = ParagraphStyle(
            'CreativeHeader',
            parent=self.styles['Heading1'],
            fontSize=30,
            textColor=colors.HexColor('#8E44AD'),
            spaceAfter=15,
            alignment=1
        )
        
        # Creative border effect
        border_table = Table([['', company_info['name'], '']], colWidths=[0.5*inch, 6*inch, 0.5*inch])
        border_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#E67E22')),
            ('BACKGROUND', (2, 0), (2, 0), colors.HexColor('#E67E22')),
            ('FONTNAME', (1, 0), (1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (1, 0), (1, 0), 30),
            ('TEXTCOLOR', (1, 0), (1, 0), colors.HexColor('#8E44AD')),
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (1, 0), (1, 0), [colors.HexColor('#F8F9FA')])
        ]))
        story.append(border_table)
        story.append(Spacer(1, 20))
        
        # Company info in colorful box
        company_details = f"{company_info['address']} | {company_info['phone']} | {company_info['email']}"
        if company_info.get('website'):
            company_details += f" | {company_info['website']}"
        
        company_table = Table([[company_details]], colWidths=[7*inch])
        company_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(company_table)
        story.append(Spacer(1, 30))
        
        # Creative invoice title
        invoice_title_style = ParagraphStyle(
            'CreativeInvoiceTitle',
            parent=self.styles['Heading2'],
            fontSize=26,
            textColor=colors.HexColor('#E74C3C'),
            spaceAfter=20,
            alignment=1
        )
        story.append(Paragraph("✨ INVOICE ✨", invoice_title_style))
        
        # Colorful info sections
        info_sections = [
            [
                Table([['INVOICE INFO']], colWidths=[2*inch]),
                Table([['CUSTOMER INFO']], colWidths=[3*inch])
            ],
            [
                Table([
                    ['Number:', str(invoice_data['invoice_number'])],
                    ['Date:', str(invoice_data['issue_date'])],
                    ['Due:', str(invoice_data['due_date'])],
                    ['Status:', str(invoice_data['status'])]
                ], colWidths=[0.8*inch, 1.2*inch]),
                Table([
                    ['Name:', str(invoice_data['customer_name'])],
                    ['Address:', str(invoice_data.get('address', ''))[:30] + '...' if len(str(invoice_data.get('address', ''))) > 30 else str(invoice_data.get('address', ''))],
                    ['Phone:', str(invoice_data.get('phone', ''))],
                    ['Email:', str(invoice_data.get('email', ''))]
                ], colWidths=[0.8*inch, 2.2*inch])
            ]
        ]
        
        # Style the info sections
        for section in info_sections:
            section_table = Table([section], colWidths=[2.5*inch, 3.5*inch])
            
            # Style headers
            if section == info_sections[0]:
                section[0].setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#9B59B6')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ]))
                section[1].setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#E67E22')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ]))
            else:
                section[0].setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ]))
                section[1].setStyle(TableStyle([
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ]))
            
            story.append(section_table)
            story.append(Spacer(1, 10))
        
        story.append(Spacer(1, 20))
        
        # Items table
        story.extend(self._create_items_table(invoice_data, items_data, 'creative'))
        
        return story
    
    def _create_items_table(self, invoice_data, items_data, template_style='classic'):
        """Create items table based on template style"""
        story = []
        
        # Items header and data
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
        
        # Style based on template
        if template_style == 'classic':
            items_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -4), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -4), 10),
                ('GRID', (0, 0), (-1, -4), 1, colors.black),
                ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                ('GRID', (2, -3), (-1, -1), 1, colors.black),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ]))
        elif template_style == 'modern':
            items_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -4), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -4), 10),
                ('GRID', (0, 0), (-1, -4), 1, colors.HexColor('#BDC3C7')),
                ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#3498DB')),
                ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
                ('GRID', (2, -3), (-1, -1), 1, colors.HexColor('#BDC3C7')),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ]))
        elif template_style == 'creative':
            items_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8E44AD')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (-1, -4), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -4), 10),
                ('GRID', (0, 0), (-1, -4), 2, colors.HexColor('#9B59B6')),
                ('FONTNAME', (0, -3), (-1, -1), 'Helvetica-Bold'),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#E74C3C')),
                ('TEXTCOLOR', (0, -1), (-1, -1), colors.white),
                ('GRID', (2, -3), (-1, -1), 2, colors.HexColor('#C0392B')),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ]))
        
        story.append(items_table)
        
        # Notes if available
        if invoice_data.get('notes'):
            story.append(Spacer(1, 20))
            notes_style = ParagraphStyle(
                'Notes',
                parent=self.styles['Normal'],
                fontSize=10,
                spaceAfter=20
            )
            story.append(Paragraph(f"<b>Notes:</b><br/>{invoice_data['notes']}", notes_style))
        
        return story

    # Continue with other template methods...
    def _create_corporate_template(self, invoice_data, items_data, company_info):
        """Corporate template implementation"""
        # Similar structure but with corporate styling
        return self._create_classic_template(invoice_data, items_data, company_info)
    
    def _create_tech_template(self, invoice_data, items_data, company_info):
        """Tech template implementation"""
        return self._create_modern_template(invoice_data, items_data, company_info)
    
    def _create_retail_template(self, invoice_data, items_data, company_info):
        """Retail template implementation"""
        return self._create_creative_template(invoice_data, items_data, company_info)
    
    def _create_food_template(self, invoice_data, items_data, company_info):
        """Food & Beverage template implementation"""
        return self._create_creative_template(invoice_data, items_data, company_info)
    
    def _create_service_template(self, invoice_data, items_data, company_info):
        """Service template implementation"""
        return self._create_classic_template(invoice_data, items_data, company_info)
