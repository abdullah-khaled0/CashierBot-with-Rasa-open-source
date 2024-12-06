import firebase_admin
from firebase_admin import credentials, firestore



# Initialize Firestore
cred = credentials.Certificate("../rasa-venv/serviceAccountKey.json")  # Update with your service account key file
firebase_admin.initialize_app(cred)
db = firestore.client()

# Add mock data to the Firestore database

# 1. Customers Collection
customers = [
    {"CustomerID": "C001", "Name": "John Doe", "Phone": "1234567890", "Email": "john@example.com", "Address": "123 Main St"},
    {"CustomerID": "C002", "Name": "Jane Smith", "Phone": "0987654321", "Email": "jane@example.com", "Address": "456 Elm St"},
]

for customer in customers:
    db.collection("Customers").document(customer["CustomerID"]).set(customer)

# # 2. Employees Collection
# employees = [
#     {"EmployeeID": "E001", "Name": "Alice Johnson", "Role": "Waiter", "Phone": "1112223333", "Email": "alice@example.com"},
#     {"EmployeeID": "E002", "Name": "Bob Brown", "Role": "Chef", "Phone": "4445556666", "Email": "bob@example.com"},
# ]

# for employee in employees:
#     db.collection("Employees").document(employee["EmployeeID"]).set(employee)

# 3. Menu_Items Collection
menu_items = [
    {"MenuItemID": "M001", "Name": "Pizza", "Description": "Cheese Pizza", "Price": 100, "Category": "Main Course"},
    {"MenuItemID": "M002", "Name": "Pasta", "Description": "Creamy Pasta", "Price": 80, "Category": "Main Course"},
]

for menu_item in menu_items:
    db.collection("Menu_Items").document(menu_item["MenuItemID"]).set(menu_item)

# # 4. Orders Collection
# orders = [
#     {
#         "OrderID": "O001",
#         "CustomerID": "C001",
#         "EmployeeID": "E001",
#         "OrderDate": "2024-11-25",
#         "TotalAmount": 180,
#         "Status": "Completed",
#     },
# ]

# for order in orders:
#     db.collection("Orders").document(order["OrderID"]).set(order)

# # 5. Order_Details Collection (Junction Table for Orders and Menu Items)
# order_details = [
#     {"OrderDetailID": "OD001", "OrderID": "O001", "MenuItemID": "M001", "Quantity": 1, "Price": 100},
#     {"OrderDetailID": "OD002", "OrderID": "O001", "MenuItemID": "M002", "Quantity": 1, "Price": 80},
# ]

# for detail in order_details:
#     db.collection("Order_Details").document(detail["OrderDetailID"]).set(detail)

# 6. Tables Collection
tables = [
    {"TableID": "T001", "TableNumber": "1", "Capacity": 4, "Status": "Available"},
    {"TableID": "T002", "TableNumber": "2", "Capacity": 6, "Status": "Occupied"},
]

for table in tables:
    db.collection("Tables").document(table["TableNumber"]).set(table)

# # 7. Reservations Collection
# reservations = [
#     {
#         "ReservationID": "R001",
#         "CustomerID": "C002",
#         "TableID": "T001",
#         "ReservationDate": "2024-11-26",
#         "ReservationTime": "19:00",
#         "Status": "Confirmed",
#     }
# ]

# for reservation in reservations:
#     db.collection("Reservations").document(reservation["ReservationID"]).set(reservation)

print("Mock data added to Firestore!")
