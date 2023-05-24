import csv
import datetime
import re
from rich.table import Table
from rich.console import Console

from util_functions import find_closest_expiration_date, get_next_id, get_internal_date, convert_string_to_date, remove_last_entry, is_valid_name, display_success_message

FIELDNAMES = {
    "bought": ["id", "product_name", "buy_date", "buy_price", "expiration_date"],
    "sold": ["id", "product_name", "bought_id", "sell_date", "sell_price"],
    "inventory": ["product_name", "bought_prices", "bought_ids", "count"],
}

console = Console()

def buy_item(item):
    expiration_date = convert_string_to_date(item["expiration_date"]) # Convert date to insure is a valid date
    item["expiration_date"] = expiration_date.isoformat()

    is_valid_name(item["product_name"]) # Verify is a valid name if not function will raise an exception

    id_num = get_next_id("./data/bought.csv")
    date_current = convert_string_to_date("today")
    with open("./data/bought.csv", "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES["bought"])
        writer.writerow({
            "id": id_num,
            "product_name": item["product_name"],
            "buy_date": date_current.isoformat(),
            "buy_price": item["price"],
            "expiration_date": item["expiration_date"],
        })
    add_action_to_history("buy")
    update_inventory()

def sell_item(item):
    date_current = convert_string_to_date("today")
    bought_ids = None
    with open("./data/inventory.csv", newline="") as csvfile:
        entries_inventory = csv.DictReader(csvfile)
        for entry in entries_inventory:
            if entry["product_name"] == item["product_name"]:
                bought_ids = entry["bought_ids"]
    if bought_ids == None:
        raise Exception("Item not in stock")
    
    id_num = get_next_id("./data/sold.csv")
    item_to_sell = find_closest_expiration_date(bought_ids) 
    with open("./data/sold.csv", "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES["sold"])
        writer.writerow({
            "id": id_num, 
            "product_name": item["product_name"],
            "bought_id": item_to_sell["id"], 
            "sell_date": date_current.isoformat(),
            "sell_price": item["price"]
        })
    add_action_to_history("sell")
    display_success_message(f"You sold a {item['product_name']} for {item['price']}")
    update_inventory()


def update_inventory():
    date_current = convert_string_to_date("today")
    bought_ids_product_sold = [] # Get all bought_ids from products sold
    with open("./data/sold.csv", newline="") as csvfile:
        entries_sold = csv.DictReader(csvfile)
        for entry in entries_sold:
            date_sold = convert_string_to_date(entry["sell_date"])
            if date_sold > date_current:
                # Sold after current date
                continue
            bought_ids_product_sold.append(entry["bought_id"])

    inventory = {}
    with open("./data/bought.csv", newline="") as csvfile:
        entries_bought = csv.DictReader(csvfile)
        for entry in entries_bought:
            expiration_date = convert_string_to_date(entry["expiration_date"])
            bought_date = convert_string_to_date(entry["buy_date"])
            if expiration_date <= date_current:
                # Item has expired
                continue
            if bought_date > date_current:
                # Item has not been purchased yet
                continue
            if entry["id"] in bought_ids_product_sold:
                # Item has been sold
                continue
            product_name = entry["product_name"]
            if product_name not in inventory:
                inventory[entry["product_name"]] = {
                    "product_name": entry["product_name"],
                    "bought_prices": [entry["buy_price"]],
                    "bought_ids": [entry["id"]],
                    "count": 1
                }
            else:
                inventory[product_name]["bought_prices"].append(entry["buy_price"])
                inventory[product_name]["bought_ids"].append(entry["id"])
                inventory[product_name]["count"] += 1

    with open("./data/inventory.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES["inventory"])
        writer.writeheader()
        writer.writerows(inventory.values())


def show_inventory():
    items = []
    with open("./data/inventory.csv") as csvfile:
        entries_inventory = csv.DictReader(csvfile)
        for entry in entries_inventory:
            items.append(entry)
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Product", style="dim", width=16)
    table.add_column("Number of Items", style="dim", width=16)
    table.add_column("Avg Purchase Price", style="dim", width=16)
    table.add_column("Nearest Expiration Date", style="dim", width=16)

    for item in items:
        avg_price = 0
        prices = re.findall("\d+", item["bought_prices"])
        for price in prices:
            avg_price += int(price)
        avg_price = round(avg_price/len(prices), 2)
        bought_ids = re.findall("\d+", item["bought_ids"])
        nearest_expiry_item = find_closest_expiration_date(bought_ids)
        
        table.add_row(
            item["product_name"],
            item["count"],
            str(avg_price),
            nearest_expiry_item["expiration_date"]
        )
    console.print(table)


def change_date(new_date):
    # new_date {string} - Either an integer representing the numbers of days to change by or another date to change to
    if re.fullmatch("-?\d+", new_date):
        # Change current day by number of days specified
        num_of_days = int(new_date)
        difference = datetime.timedelta(days=num_of_days)
        date_current = get_internal_date()
        new_date = date_current + difference
    else:
        # Change the date to the date specified
        new_date = convert_string_to_date(new_date)
    
    with open("./date.txt", "w") as date_file:
        date_file.write(new_date.isoformat())
    display_success_message(f"Date changed.\nCurrent date is {new_date.isoformat()}")
    update_inventory()
            

def add_action_to_history(action):
    with open("./data/history.txt", "a") as txt_file:
        txt_file.write(action)
        txt_file.write("\n")


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

