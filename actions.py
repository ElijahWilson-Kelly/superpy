import csv
import datetime

from util_functions import find_closest_expiration_date, get_next_id, string_to_date, get_internal_date, convert_date, remove_last_entry

FIELDNAMES = {
    "bought": ["id", "product_name", "buy_date", "buy_price", "expiration_date"],
    "sold": ["id", "product_name", "bought_id", "sell_date", "sell_price"],
    "inventory": ["product_name", "buy_prices", "bought_ids", "count"],
    "history": ["action"]
}

def buy_item(item):
    id_num = get_next_id("./data/bought.csv")
    date = convert_date("today")
    item["expiration_date"] = convert_date(item["expiration_date"])

    with open("./data/bought.csv", "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES["bought"])
        writer.writerow({
            "id": id_num,
            "product_name": item["product_name"],
            "buy_date": date,
            "buy_price": item["price"],
            "expiration_date": item["expiration_date"],
        })
    add_action_to_history("buy")
    update_inventory()

def sell_item(item):
    date = "15/5/2023"
    bought_ids = None
    with open("./data/inventory.csv", newline="") as csvfile:
        entries_inventory = csv.DictReader(csvfile)
        for entry in entries_inventory:
            if entry["product_name"] == item["product_name"]:
                bought_ids = entry["bought_ids"]
        if bought_ids == None:
            print("Item not Available")
            return
    id_num = get_next_id("./data/sold.csv")
    item_to_sell = find_closest_expiration_date(bought_ids) 
    with open("./data/sold.csv", "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES["sold"])
        writer.writerow({
            "id": id_num, 
            "product_name": item["product_name"],
            "bought_id": item_to_sell["id"], 
            "sell_date": date,
            "sell_price": item["price"]
        })
    add_action_to_history("sell")
    update_inventory()

def update_inventory():
    date = datetime.date(2010, 5, 12)
    bought_ids_product_sold = []
    with open("./data/sold.csv", newline="") as csvfile:
        entries_sold = csv.DictReader(csvfile)
        for entry in  entries_sold:
            bought_ids_product_sold.append(entry["bought_id"])

    inventory = {}
    with open("./data/bought.csv", newline="") as csvfile:
        entries_bought = csv.DictReader(csvfile)
        for entry in entries_bought:
            expiration_date = string_to_date(entry["expiration_date"])
            if expiration_date < date:
                continue
            if entry["id"] in bought_ids_product_sold:
                continue
            if entry["product_name"] not in inventory:
                inventory[entry["product_name"]] = {
                    "product_name": entry["product_name"],
                    "buy_prices": [entry["buy_price"]],
                    "bought_ids": [entry["id"]],
                    "count": 1
                }
            else:
                inventory[entry["product_name"]]["buy_prices"].append(entry["buy_price"])
                inventory[entry["product_name"]]["bought_ids"].append(entry["id"])
                inventory[entry["product_name"]]["count"] += 1

    with open("./data/inventory.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES["inventory"])
        writer.writeheader()
        writer.writerows(inventory.values())

def show_inventory():
    with open("./data/inventory.csv") as csvfile:
        entries_inventory = csv.DictReader(csvfile)
        for entry in entries_inventory:
            print(entry)

def undo():
    action = None
    rows = []
    with open("./data/history.txt") as txt_file:
        rows = txt_file.read().split("\n")
        action = rows.pop(len(rows) - 2)
    with open("./data/history.txt", "w") as txt_file:
        txt_file.write("\n".join(rows))
    if action == "buy":
        remove_last_entry("./data/bought.csv")
    elif action == "sell":
        remove_last_entry("./data/sold.csv")
    update_inventory()
    

def add_action_to_history(action):
    with open("./data/history.txt", "a") as txt_file:
        txt_file.write(action)
        txt_file.write("\n")

def reset():
    with open("./data/bought.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES["bought"])
        writer.writeheader()
    with open("./data/sold.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES["sold"])
        writer.writeheader()
    with open("./data/history.txt", "w", newline="") as txt_file:
        txt_file.write("")
    update_inventory()

