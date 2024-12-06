import re
import firebase_admin
from firebase_admin import credentials, firestore
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Text, Dict, List

import time 




# Initialize Firestore
cred = credentials.Certificate("../rasa-venv/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()




class ActionShowMenu(Action):
    def name(self) -> Text:
        return "action_show_menu"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Fetch menu items from Firestore
        menu_items = [doc.to_dict()['Name'] for doc in db.collection("Menu_Items").stream()]
        menu_text = "\n".join(f"- {item}" for item in menu_items)

        dispatcher.utter_message(text=f"Here is the menu: \n {menu_text} \n \n What would you like to order?")
        return []
    

class ActionAskFoodAndQuantity(Action):
    def name(self) -> Text:
        return "action_ask_food_and_quantity"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="How many of each item would you like?")
        return []


# class ActionShowAvailableTables(Action):
#     def name(self) -> Text:
#         return "action_show_available_tables"

#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         # Fetch available tables from Firestore
#         available_tables = [doc.id for doc in db.collection("Tables").where("Status", "==", "Available").stream()]
#         tables_text = ", ".join(available_tables)

#         print("Tables", tables_text)

#         dispatcher.utter_message(template="utter_ask_table_number", tables_names=tables_text)
#         return []


class ActionGenerateOrderAndReservation(Action):
    def name(self) -> Text:
        return "action_generate_order_and_reservation"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        raw_quantities = tracker.get_slot("quantity")

        # Get an available table dynamically from the database
        available_tables = [doc.id for doc in db.collection("Tables").where("Status", "==", "Available").stream()]
        if not available_tables:
            dispatcher.utter_message(text="Sorry, no tables are currently available for reservation.")
            return []
        table_number = available_tables[0]

        print("Raw Quantities:", raw_quantities)
        print("Selected Table Number:", table_number)

        # Parse the quantities to extract item names and their counts
        quantities = {}
        for entry in raw_quantities:
            match = re.match(r"(\d+)\s+(.+)", entry)
            if match:
                count, item_name = int(match.group(1)), match.group(2).strip().lower()
                quantities[item_name] = count

        print("Parsed Quantities:", quantities)

        # Map item names to their corresponding MenuItemID and fetch prices
        prices = {}
        menu_items = []

        for item_name, count in quantities.items():
            item_doc = db.collection("Menu_Items").where("Name", "==", item_name).stream()
            found = False
            for doc in item_doc:
                menu_item_id = doc.id
                item_data = doc.to_dict()
                prices[menu_item_id] = item_data.get("Price", 0)
                menu_items.append({"id": menu_item_id, "name": item_name, "quantity": count, "price": item_data.get("Price", 0)})
                found = True
                break
            if not found:
                dispatcher.utter_message(text=f"Error: Menu item '{item_name}' not found in the database.")
                return []

        # Calculate the total amount dynamically
        total_amount = sum(item["quantity"] * item["price"] for item in menu_items)

        # Generate unique IDs
        order_id = f"O{int(time.time())}"
        reservation_id = f"R{int(time.time())}"

        # Save order in Firestore
        order_data = {
            "OrderID": order_id,
            "OrderDate": firestore.SERVER_TIMESTAMP,
            "TotalAmount": total_amount,
            "Status": "Pending",
            "Items": [
                {"MenuItemID": item["id"], "quantity": item["quantity"], "price": item["price"]}
                for item in menu_items
            ]
        }
        db.collection("Orders").document(order_id).set(order_data)

        # Save reservation in Firestore
        reservation_data = {
            "ReservationID": reservation_id,
            "TableID": table_number,
            "ReservationDate": "Today",
            "ReservationTime": "7 PM",
            "Status": "Confirmed"
        }
        db.collection("Reservations").document(reservation_id).set(reservation_data)

        # Update table status to "Reserved"
        db.collection("Tables").document(table_number).update({"Status": "Reserved"})

        # Create order summary for response
        order_summary = "\n".join(
            f"- {item['quantity']} x {item['name'].title()} @ ${item['price']} each"
            for item in menu_items
        )

        # Respond to the user with order and reservation details
        dispatcher.utter_message(
            text=f"Your order has been placed!\n"
                 f"- Order:\n{order_summary}\n"
                 f"- Total: ${total_amount}\n"
                 f"- Reservation: Today at 7 PM\n"
                 f"- Assigned Table: Table {table_number}\n"
                 f"Order ID: {order_id}\n"
                 f"Reservation ID: {reservation_id}"
        )

        return []