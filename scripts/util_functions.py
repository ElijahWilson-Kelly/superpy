import csv
import datetime
import re
import os
import json


class InvalidInput(Exception):
    def __init__(self, title, descriptions):
        self.title = title
        self.descriptions = descriptions

class ItemNotInStock(Exception):
    def __init__(self, title, descriptions):
        self.title = title
        self.descriptions = descriptions

# -----------------------------------------------------------------
# JSON data functions
# -----------------------------------------------------------------

def change_json_data(key, value):
    with open(os.path.join(os.getcwd(), "data.json")) as data_file:
        data = json.loads(data_file.read())
        
    data[key] = value
    with open(os.path.join(os.getcwd(), "data.json"), "w") as data_file:
        data_json = json.dumps(data, indent=1)
        data_file.write(data_json)

def get_json_data(key):
    with open(os.path.join(os.getcwd(), "data.json")) as data_file:
        data = json.loads(data_file.read())
        return data[key]


# -----------------------------------------------------------------
# Path functions
#  - paths change depending on currently selected company
# -----------------------------------------------------------------

def get_current_company_dir_path():
    company_name = get_json_data("current_company")
    return os.path.join(os.getcwd(), "companies", company_name)


def get_bought_csv_path():
    return os.path.join(get_current_company_dir_path(), "dbs", "bought.csv")

def get_sold_csv_path():
    return os.path.join(get_current_company_dir_path(), "dbs", "sold.csv")

def get_inventory_csv_path():
    return os.path.join(get_current_company_dir_path(), "dbs", "inventory.csv")

def get_expired_csv_path():
    return os.path.join(get_current_company_dir_path(), "dbs", "expired.csv")

def get_history_csv_path():
    return os.path.join(get_current_company_dir_path(), "history.txt")

def string_to_date(string):
    (year, month, day) = string.split("-")
    return datetime.date(int(year), int(month), int(day))


def get_internal_date():
    date_iso = get_json_data("current_date")
    return datetime.date.fromisoformat(date_iso)
        
# -----------------------------------------------------------------
# Date functions
# -----------------------------------------------------------------   

def convert_string_to_date(date_string):
    # Takes an input {string} if not in corrext format YYYY-MM-DD or given keyword (i.e. tomorrow) raises exception
    match date_string.lower():
        case "tomorrow":
            date_string = "1"
        case "today":
            date_string = "0"
        case "yesterday":
            date_string = "-1"
    try:
        if re.fullmatch("-?\d+", date_string):
            # Change by a given amount
            date = get_internal_date()
            date += datetime.timedelta(days=int(date_string))
            return date
        else:
            return datetime.date.fromisoformat(date_string)
    except:
        raise InvalidInput("Invalid Date",["YYYY-MM-DD - change date to specefied date", "yesterday, today, tomorrow - change date relative to the current date", "-?\d+ - change date by integer number of days"])




def find_closest_expiration_date(bought_ids):
    # bought_ids - {str[]}
    # given an array of ids finds the item with the closest expiration date and returns the item
    item_to_sell = None
    bought_path = os.path.join(get_current_company_dir_path(), "dbs", "bought.csv")
    with open(bought_path, newline="") as csv_file:
        entries_bought = csv.DictReader(csv_file)
        nearest_expiry = datetime.date.max
        for entry in entries_bought:
            if entry["id"] not in bought_ids:
                continue
            (year, month, day) = entry["expiration_date"].split("-")
            expiration_date = datetime.date(int(year), int(month), int(day))
            if expiration_date < nearest_expiry:
                nearest_expiry = expiration_date
                item_to_sell = entry
    return item_to_sell


def get_next_id(csv_file_path):
    result = 0
    with open(csv_file_path, newline="") as csvfile:
        contents = csv.reader(csvfile)
        for _ in contents:
            result += 1
    return result


def is_valid_name(name):
    match = re.fullmatch("[a-zA-Z_]+", name)
    if not match:
        raise InvalidInput("Invalid Product name", ["Name can only contain word characters [a-zA-Z_]+", f"You tried using the name {name}"])
        
    
def remove_last_entry(path):
    new_entries = []
    with open(path, newline="") as csvfile:
        entries = csv.reader(csvfile)
        for entry in entries:
            new_entries.append(entry)
    removed_entry = new_entries.pop()
    with open(path, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(new_entries)
    return removed_entry


def get_revenue(date_start, date_end = None):
    """Returns revenue for given date range (date_start to date_end inclusive)

    Args:
        date_start (date object): start date for given date range
        date_end (date object): end date for given date range (inclusive). Defaults to start date

    Returns:
        float: revenue made over given date range
    """
    if not date_end:
        date_end = date_start
    amount_made = 0
    with open(get_sold_csv_path()) as csv_file:
        entries = csv.DictReader(csv_file)
        for entry in entries:
            date_of_item = convert_string_to_date(entry["sell_date"])
            if  date_of_item >= date_start and date_of_item <= date_end:
                amount_made += float(entry["sell_price"])
    return round(amount_made, 2)


def get_profit(date_start, date_end = None):
    """Returns revenue for given date range (date_start to date_end inclusive)

    Args:
        date_start (date object): start date for given date range
        date_end (date object, optional): end date for given date range (inclusive). Defaults to start date

    Returns:
        float: profit made over given period
    """
    if not date_end:
        date_end = date_start
    amount_made = 0
    bought_ids = []
    with open(get_sold_csv_path()) as csv_file:
        entries = csv.DictReader(csv_file)
        for entry in entries:
            date_of_item = convert_string_to_date(entry["sell_date"])
            if  date_of_item >= date_start and date_of_item <= date_end:
                amount_made += float(entry["sell_price"])
                bought_ids.append(entry["bought_id"])
    with open(get_bought_csv_path()) as csv_file:
        entries = csv.DictReader(csv_file)
        for entry in entries:
            if entry["id"] in bought_ids:
                amount_made -= float(entry["buy_price"])
    return round(amount_made, 2)

