import csv
import datetime
import os
import re
import shutil

from scripts.util_functions import find_closest_expiration_date, get_next_id, get_internal_date, convert_string_to_date, get_revenue, get_profit, remove_last_entry, is_valid_name, get_current_company_dir_path, change_json_data, get_bought_csv_path, get_sold_csv_path, get_inventory_csv_path, get_expired_csv_path, get_history_csv_path, ItemNotInStock

from scripts.console_display import display_response, display_success_message, display_table

FIELDNAMES = {
    "bought": ["id", "product_name", "buy_date", "buy_price", "expiration_date"],
    "sold": ["id", "product_name", "bought_id", "sell_date", "sell_price"],
    "inventory": ["product_name", "bought_prices", "bought_ids", "count"],
    "expired": ["product_name", "money_lost", "count"]
}

def create_company(name):
    name = name.lower()
    company_folder_path = os.path.join(os.getcwd(), "companies", name)
    try:
        os.mkdir(company_folder_path)
        initiate_empty_company(company_folder_path)
        change_current_company(name)
    except FileExistsError:
        display_response("Company Already Exists!", [f"Would you like to overwrite the company \"{name}\" with a new company?", "This cannot be undone"])
        response = ""
        while response != "y" and response != "n":
            response = input("y or n: ")
            response = response.lower()
        
        if response == "y":
            shutil.rmtree(company_folder_path)
            create_company(name)
            
    
def change_current_company(company_name):
    company_path = os.path.join(os.getcwd(), "companies", company_name)
    if not os.path.isdir(company_path):
        display_response("Company does not Exist", [f"Would you like to create a new company called \"{company_name}\"?"])
        response = ""
        while response != "y" and response != "n":
            response = input("y or n: ")
            response = response.lower()
        if response == "y":
            create_company(company_name)
    else:
        change_json_data("current_company", company_name)


def buy_item(item):
    """Add item to bought database

    Args:
        item (dict):
        {
            product_name,
            expiration_date,
            price,
        }    
    """
    expiration_date = convert_string_to_date(item["expiration_date"]) # Convert date to insure is a valid date
    item["expiration_date"] = expiration_date.isoformat()
    is_valid_name(item["product_name"]) # Verify is a valid name if not function will raise an exception

    date_current = convert_string_to_date("today")

    path = get_bought_csv_path()
    id_num = get_next_id(path)
    with open(path, "a", newline="") as csvfile:
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
    display_success_message("Item bought", [f"{item['product_name']} bought for ${item['price']}"])


def sell_item(item):
    date_current = convert_string_to_date("today")
    bought_ids = None

    inventory_path = get_inventory_csv_path()
    with open(inventory_path, newline="") as csvfile:
        entries_inventory = csv.DictReader(csvfile)
        for entry in entries_inventory:
            if entry["product_name"] == item["product_name"]:
                bought_ids = entry["bought_ids"]
    if bought_ids == None:
        raise ItemNotInStock("Item not in stock.", [f"{item['product_name'].capitalize()} is not currently in stock."])
    
    sold_path = get_sold_csv_path()   
    id_num = get_next_id(sold_path)
    item_to_sell = find_closest_expiration_date(bought_ids) 
    with open(sold_path, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES["sold"])
        writer.writerow({
            "id": id_num, 
            "product_name": item["product_name"],
            "bought_id": item_to_sell["id"], 
            "sell_date": date_current.isoformat(),
            "sell_price": item["price"]
        })
    add_action_to_history("sell")
    display_success_message("Item Sold", f"You sold a {item['product_name']} for {item['price']}")
    update_inventory()


def update_inventory():
    date_current = convert_string_to_date("today")
    bought_ids_product_sold = [] # Get all bought_ids from products sold
    sold_path = os.path.join(get_current_company_dir_path(), "dbs", "sold.csv")
    with open(sold_path, newline="") as csvfile:
        entries_sold = csv.DictReader(csvfile)
        for entry in entries_sold:
            date_sold = convert_string_to_date(entry["sell_date"])
            if date_sold > date_current:
                # Sold after current date
                continue
            bought_ids_product_sold.append(entry["bought_id"])

    inventory = {}
    expired = {}
    bought_path = os.path.join(get_current_company_dir_path(), "dbs", "bought.csv")
    with open(bought_path, newline="") as csvfile:
        entries_bought = csv.DictReader(csvfile)
        for entry in entries_bought:
            product_name = entry["product_name"]
            expiration_date = convert_string_to_date(entry["expiration_date"])
            bought_date = convert_string_to_date(entry["buy_date"])
            if entry["id"] in bought_ids_product_sold:
                # Item has been sold
                continue
            if expiration_date <= date_current:
                # Item has expired
                if product_name not in expired:
                    expired[product_name] = {
                        "product_name": product_name
                    }
                
                expired[product_name]["money_lost"] = expired[product_name].get("money_lost", 0) + int(entry["buy_price"])
                expired[product_name]["count"] = expired[product_name].get("count", 0) + 1
                continue
            if bought_date > date_current:
                # Item has not been purchased yet acording to internal date
                continue
            
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
    inventory_path = os.path.join(get_current_company_dir_path(), "dbs", "inventory.csv")
    with open(inventory_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES["inventory"])
        writer.writeheader()
        writer.writerows(inventory.values())
    expired_path = os.path.join(get_current_company_dir_path(), "dbs", "expired.csv")
    with open(expired_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES["expired"])
        writer.writeheader()
        writer.writerows(expired.values())


def show_inventory(): 
    items = []
    inventory_path = os.path.join(get_current_company_dir_path(), "dbs", "inventory.csv")
    with open(inventory_path) as csvfile:
        entries_inventory = csv.DictReader(csvfile)
        for entry in entries_inventory:
            items.append(entry)
    if len(items) == 0:
        display_response("Inventory is empty", ["There is currently nothing in the inventory."])
    else:
        display_table(items)

def show_expired_items():
    items = []
    expired_path = os.path.join(get_current_company_dir_path(), "dbs", "expired.csv")
    with open(expired_path) as csvfile:
        entries = csv.DictReader(csvfile)
        for entry in entries:
            items.append(entry)
    if (len(items)) == 0:
        display_response("No expired Items", "")
    else:
        display_table(items)

def change_date(new_date):
    new_date = convert_string_to_date(new_date)
    change_json_data("current_date", new_date.isoformat())
    display_success_message("Date changed.",[f"Current date is {new_date.isoformat()}"])
    update_inventory()
            

def add_action_to_history(action):
    history_path = os.path.join(get_current_company_dir_path(), "history.txt")
    with open(history_path, "a") as txt_file:
        txt_file.write(action)
        txt_file.write("\n")


def report(commands):
    report_type = commands["type"]
    date = None
    if commands["date"]:
        date = convert_string_to_date(commands["date"])
    else:
        date = get_internal_date()
    if report_type == "profit":
        income = money_made(date)
        expenditure = money_spent(date)
        profit = income - expenditure
        heading = f"Profit for {date.isoformat()}"
        msg = "${0:,.2f}".format(profit)
        display_response(heading, msg)
    else:
        income = money_made(date)
        heading = f"Revenue for {date.isoformat()}"
        msg = "${0:,.2f}".format(income)
        display_response(heading, msg)
        

def undo():
    action = None
    rows = []
    history_path = os.path.join(get_current_company_dir_path(), "history.txt")
    with open(history_path) as txt_file:
        rows = re.findall("\w+", txt_file.read())
        print(rows)
        action = rows.pop()
    
    with open(history_path, "w") as txt_file:
        txt_file.write("\n".join(rows) + "\n")
    
    if action == "buy":
        bought_path = os.path.join(get_current_company_dir_path(), "dbs", "bought.csv")
        remove_last_entry(bought_path)
    elif action == "sell":
        sold_path = os.path.join(get_current_company_dir_path(), "dbs", "sold.csv")
        remove_last_entry(sold_path)
    update_inventory()


def initiate_empty_company(company_dir_path):
    db_dir_path = os.path.join(company_dir_path, "dbs")
    os.mkdir(db_dir_path)
    
    with open(os.path.join(db_dir_path, "bought.csv"), "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES["bought"])
        writer.writeheader()
    with open(os.path.join(db_dir_path, "sold.csv"), "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES["sold"])
        writer.writeheader()
    with open(os.path.join(db_dir_path, "inventory.csv"), "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES["inventory"])
        writer.writeheader()
    with open(os.path.join(db_dir_path, "expired.csv"), "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES["expired"])
        writer.writeheader()
    with open(os.path.join(company_dir_path, "history.txt"), "w") as txt_file:
        txt_file.write("")
    update_inventory()

