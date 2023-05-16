import csv
import datetime

def display_error_message(msg):
    print(msg)

def find_closest_expiration_date(bought_ids):
    item_to_sell = None
    with open("./data/bought.csv", newline="") as csv_file:
        entries_bought = csv.DictReader(csv_file)
        nearest_expiry = datetime.date.max
        for entry in entries_bought:
            if entry["id"] not in bought_ids:
                continue
            (day, month, year) = entry["expiration_date"].split("/")
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
    (day, month, year) = string.split("/")
    return datetime.date(int(year), int(month), int(day))

def get_internal_date():
    with open("./date.txt") as date_file:
        (day, month, year) = date_file.read().split("/")
        return datetime.date(int(year), int(month), int(day))
        
   
def convert_date(input):
    # Takes an input {string} and converts it to a date object and then into a string with format DD/MM/YYYY
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
        (year, month, day) = date.isoformat().split("-")
        return f'{year}-{month}-{day}'
    except:
        raise Exception("Invalid Date")
       
    
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
    