from fpdf import FPDF
from io import BytesIO

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Customer Invoice", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(invoice):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", "", 12)

    # Basic info
    pdf.cell(100, 10, f"Date: {invoice.get('date', '')}", ln=True)
    pdf.cell(100, 10, f"Platform: {invoice.get('platform', '')}", ln=True)
    pdf.cell(100, 10, f"Order #: {invoice.get('order_number', '')}", ln=True)
    pdf.cell(100, 10, f"Customer Name: {invoice.get('name', '')}", ln=True)
    pdf.cell(100, 10, f"Contact: {invoice.get('contact', '')}", ln=True)
    pdf.multi_cell(0, 10, f"Address: {invoice.get('address', '')}")
    pdf.ln(5)

    # Table headers
    pdf.set_fill_color(200, 220, 255)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(10, 10, "No", border=1, fill=True)
    pdf.cell(60, 10, "Product", border=1, fill=True)
    pdf.cell(40, 10, "IMEI", border=1, fill=True)
    pdf.cell(20, 10, "Qty", border=1, fill=True)
    pdf.cell(30, 10, "Price", border=1, fill=True)
    pdf.cell(30, 10, "Total", border=1, ln=True, fill=True)

    # Reset font
    pdf.set_font("Arial", "", 12)

    # Get product list (ensure backward compatibility)
    products = invoice.get("products")
    if not isinstance(products, list):
        products = [{
            "product": invoice.get("product", ""),
            "imei": invoice.get("imei", ""),
            "qty": invoice.get("qty", 1),
            "price": invoice.get("price", 0.0),
        }]

    # Table rows
    for idx, item in enumerate(products, start=1):
        product = item.get("product", "")
        imei = item.get("imei", "")
        qty = item.get("qty", 1)
        price = item.get("price", 0.0)
        total_price = price * qty

        pdf.cell(10, 10, str(idx), border=1)
        pdf.cell(60, 10, product, border=1)
        pdf.cell(40, 10, imei, border=1)
        pdf.cell(20, 10, str(qty), border=1)
        pdf.cell(30, 10, f"{price:.2f}", border=1)
        pdf.cell(30, 10, f"{total_price:.2f}", border=1, ln=True)

    # Final Summary
    pdf.ln(5)
    advance = invoice.get("advance", 0.0)
    cod = invoice.get("cod", 0.0)
    total = sum(p.get("price", 0.0) * p.get("qty", 1) for p in products)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(100, 10, f"Advance Paid: {advance:.2f}", ln=True)
    pdf.cell(100, 10, f"Cash on Delivery: {cod:.2f}", ln=True)
    pdf.cell(100, 10, f"Total Amount: {total:.2f}", ln=True)

    # Output as PDF
    pdf_output = BytesIO()
    return pdf.output(dest='S').encode('latin1')

