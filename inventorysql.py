import pyodbc

class Item:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

class Inventory:
    def __init__(self, server, database):
        self.connection = pyodbc.connect(f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database}")
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def add_item(self, item):
        query = f"INSERT INTO inventory (name, price, quantity) VALUES ('{item.name}', {item.price}, {item.quantity})"
        self.cursor.execute(query)
        self.connection.commit()

    def get_items(self):
        query = "SELECT * FROM inventory"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        if len(rows) == 0:
            print("No items found")
        else:
            for i, row in enumerate(rows):
                print(f"{i + 1}. {row.name} - Price: {row.price} - Quantity: {row.quantity}")

    def remove_item(self, item_id):
        query = f"DELETE FROM inventory WHERE id={item_id}"
        self.cursor.execute(query)
        self.connection.commit()

    def update_quantity(self, item_id, quantity):
        query = f"UPDATE inventory SET quantity={quantity} WHERE id={item_id}"
        self.cursor.execute(query)
        self.connection.commit()

    def generate_report(self):
        query = "SELECT * FROM inventory WHERE quantity < 5"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        if len(rows) == 0:
            print("No items need to be restocked")
        else:
            for i, row in enumerate(rows):
                print(f"{i + 1}. {row.name} - Quantity: {row.quantity}")

def main():
    server = "(localdb)\LocalDB"
    database = "inventory"


    inventory = Inventory(server, database)

    while True:
        print("\nInventory Management System")
        print("1. Add Item")
        print("2. View Items")
        print("3. Remove Item")
        print("4. Check Items Need to be Restocked")
        print("5. Update Quantity")
        print("6. Exit")

        choice = int(input("Please enter your choice (1-6): "))

        if choice == 1:
            name = input("Enter item name: ")
            price = float(input("Enter item price: "))
            quantity = int(input("Enter item quantity: "))
            item = Item(name, price, quantity)
            inventory.add_item(item)
            print("Item added to inventory")
        elif choice == 2:
            inventory.get_items()
        elif choice == 3:
            item_id = int(input("Enter item id to remove: "))
            inventory.remove_item(item_id)
            print("Item removed from inventory")
        elif choice == 4:
            inventory.generate_report()
        elif choice == 5:
            item_id = int(input("Enter item id to update: "))
            quantity = int(input("Enter the new quantity: "))
            inventory.update_quantity(item_id, quantity)
            print("Quantity updated")
        elif choice == 6:
            print("Exiting Inventory Management System")
            break
        else:
            print("Invalid choice")

if __name__ == '__main__':
    main()
