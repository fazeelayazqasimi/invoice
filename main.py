import streamlit as st
import json
import os
from datetime import datetime
from generate_invoice import generate_pdf

st.set_page_config(page_title="Invoice Generator", layout="wide")
st.title("🧾 Invoice Generator")

invoice_file = "data/invoices.json"

# Load existing invoices
if os.path.exists(invoice_file):
    with open(invoice_file, "r") as f:
        all_invoices = json.load(f)
else:
    all_invoices = []

# Sidebar options
st.sidebar.header("📜 Invoice Options")
sidebar_option = st.sidebar.radio("Select an option", ["Generate Invoice", "Recent Invoices"])

if sidebar_option == "Generate Invoice":
    with st.form("invoice_form"):
        st.subheader("Enter Invoice Details")

        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date", datetime.now().date())
            platform = st.selectbox("Platform", ["Salamtec", "Alfamall", "Digimall", "Meezan Bank", "Faisal Takmeel", "Daraz", "Js Bank", "Bank al Falah"])
            name = st.text_input("Customer Name")
            order_number = st.text_input("Order Number")
            contact = st.text_input("Contact Number")
        with col2:
            address = st.text_area("Address")
            advance = st.number_input("Advance", min_value=0.0, step=1.0)
            cod = st.number_input("Cash on Delivery", min_value=0.0, step=1.0)
            num_products = st.number_input("Number of Products", min_value=1, step=1)

        # Product Inputs
        products = []
        for i in range(int(num_products)):
            st.markdown(f"### 📦 Product {i+1}")
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                product = st.text_input(f"Product {i+1}", key=f"product_{i}")
            with c2:
                imei = st.text_input(f"IMEI {i+1}", key=f"imei_{i}")
            with c3:
                qty = st.number_input(f"Qty {i+1}", min_value=1, step=1, key=f"qty_{i}")
            with c4:
                price = st.number_input(f"Price {i+1}", min_value=0.0, step=1.0, key=f"price_{i}")

            if product.strip():  # Only add if product name is not empty
                products.append({
                    "product": product.strip(),
                    "imei": imei.strip(),
                    "qty": qty,
                    "price": price
                })

        submitted = st.form_submit_button("💾 Save Invoice")

    if submitted:
        if not products:
            st.warning("⚠️ Please enter at least one product with a name.")
        else:
            total = sum(p["qty"] * p["price"] for p in products)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            invoice_data = {
                "date": str(date),
                "timestamp": timestamp,
                "platform": platform,
                "name": name,
                "order_number": order_number,
                "contact": contact,
                "address": address,
                "advance": advance,
                "cod": cod,
                "total": total,
                "products": products
            }

            all_invoices.append(invoice_data)
            os.makedirs("data", exist_ok=True)
            with open(invoice_file, "w") as f:
                json.dump(all_invoices, f, indent=2)

            st.success("✅ Invoice saved!")

            pdf = generate_pdf(invoice_data)
            st.download_button(
                "📥 Download Invoice PDF",
                data=pdf,
                file_name=f"invoice_{order_number}.pdf",
                mime="application/pdf"
            )

elif sidebar_option == "Recent Invoices":
    st.subheader("🔍 Recent Invoices")
    search_term = st.text_input("Search by Name, Date or Order Number").lower()
    filtered = [
        inv for inv in all_invoices
        if search_term in inv["name"].lower()
        or search_term in inv["order_number"].lower()
        or search_term in inv["date"].lower()
    ]

    st.write(f"Total Results: {len(filtered)}")

    for inv in filtered[::-1]:
       with st.expander(f"📄 {inv['order_number']} - {inv['name']} ({inv['date']})"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"📅 **Date/Time:** {inv['timestamp']}")
                st.write(f"🛒 **Platform:** {inv['platform']}")
                st.write(f"📞 **Contact:** {inv['contact']}")
            with col2:
                st.write(f"🏠 **Address:** {inv['address']}")
                st.write(f"💵 **Advance:** {inv['advance']} | **COD:** {inv['cod']}")
                st.write(f"🧮 **Total:** {inv['total']}")

            # Show products in table format
            if inv.get("products"):
                product_data = [{
                    "Product": p["product"],
                    "IMEI": p["imei"],
                    "Qty": p["qty"],
                    "Price": p["price"]
                } for p in inv["products"]]
                st.markdown("### 📦 Product Details")
                st.table(product_data)

            # Download button
            pdf = generate_pdf(inv)
            st.download_button(
                f"📥 Download Invoice PDF ({inv['order_number']})",
                data=pdf,
                file_name=f"invoice_{inv['order_number']}.pdf",
                mime="application/pdf"
            )
