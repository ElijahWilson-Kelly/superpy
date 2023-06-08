import re

from rich.console import Console
from rich.table import Table

from scripts.util_functions import find_closest_expiration_date, get_json_data

console = Console(highlight=False)

def display_error_message(heading, msgs):
    console.print("")
    console.print(heading, style="bold red")
    for msg in msgs:
        console.print(msg, style="white")
    console.print("")

def display_success_message(heading, msgs):
    console.print("")
    console.print(heading, style="bold green")
    for msg in msgs:
        console.print(msg, style="white")
    console.print("")

def display_response(heading, msgs):
    console.print("")
    console.print(heading, style="bold magenta")
    for msg in msgs:
        console.print(msg, style="white")
    console.print("")

def display_table(items):
    console.print("")
    table = Table(show_header=True, header_style="purple4")
    table.add_column("Product", width=16)
    table.add_column("Number of Items", width=16)
    table.add_column("Avg Purchase Price", width=16)
    table.add_column("Nearest Expiration Date", width=16)
    for item in items:
        avg_price = 0
        prices = re.findall("\d+\.?\d*", item["bought_prices"])
        for price in prices:
            avg_price += float(price)
        avg_price = avg_price/len(prices)
        bought_ids = re.findall("\d+", item["bought_ids"])
        nearest_expiry_item = find_closest_expiration_date(bought_ids)
        table.add_row(
            item["product_name"].capitalize(),
            item["count"],
            "${0:.2f}".format(avg_price),
            nearest_expiry_item["expiration_date"]
        )
    company_name = get_json_data("current_company")
    date = get_json_data("current_date")
    console.print(f"--- {company_name.capitalize()} ---", style="bold blue")
    console.print(f"--- {date.capitalize()} ---", style="cyan2")
    console.print(table)
    console.print("")