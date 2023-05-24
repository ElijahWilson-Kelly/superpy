import csv
import datetime
import re
from rich.console import Console

console = Console()

def display_error_message(msg):
    console.print(msg, style="bold green")

def display_success_message(msg):
    console.print(msg, style="bold green")

def find_closest_expiration_date(bought_ids):
    # bought_ids - {str[]}
    # given an array of ids finds the item with the closest expiration date and returns the item
    item_to_sell = None
    with open("./data/bought.csv", newline="") as csv_file:
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
        for row in contents:
            result += 1
    return result


def string_to_date(string):
    (year, month, day) = string.split("-")
    return datetime.date(int(year), int(month), int(day))


def get_internal_date():
    with open("./date.txt") as date_file:
        (year,month,day) = date_file.read().split("-")
        return datetime.date(int(year), int(month), int(day))
        
   
def convert_string_to_date(input):
    # Takes an input {string} if not in corrext format YYYY-MM-DD or given keyword (i.e. tomorrow) raises exception
    try:
        date = get_internal_date()
        if input.lower() == "tomorrow":
            date += datetime.timedelta(days=1)
        elif input.lower() == "today":
            pass
        elif input.lower() == "yesterday":
            date -= datetime.timedelta(days=1)
        else:
            (year,month,day) = input.split("-")
            date = datetime.date(int(year), int(month), int(day)) 
        return date
    except:
        raise Exception("Invalid Date")


def is_valid_name(name):
    match = re.search("\d+", name)
    if match:
        raise Exception("Product name cannot contain numbers")
        
    
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
    