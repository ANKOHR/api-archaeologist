"""SYNTHETIC acme-orders code remains. Never contact a real API."""
import requests
requests.get("https://acme-orders.invalid/orders/101")
requests.post("https://acme-orders.invalid/orders", json={"sku": "FICTIONAL-B", "quantity": 1})
