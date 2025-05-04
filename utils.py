import json
import os

def load_invoices(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)

def save_invoice(invoice, path):
    invoices = load_invoices(path)
    invoices.append(invoice)
    with open(path, "w") as f:
        json.dump(invoices, f, indent=4)

def update_invoice(updated, path):
    invoices = load_invoices(path)
    for i, inv in enumerate(invoices):
        if inv["order_number"] == updated["order_number"]:
            invoices[i] = updated
            break
    with open(path, "w") as f:
        json.dump(invoices, f, indent=4)

def search_invoices(invoices, term, date=None):
    term = term.lower()
    results = []
    for inv in invoices:
        if term in inv["name"].lower() or term in inv["order_number"].lower():
            if date:
                if inv["date"] == str(date):
                    results.append(inv)
            else:
                results.append(inv)
    return results
