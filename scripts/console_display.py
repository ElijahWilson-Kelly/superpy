from rich.console import Console
from rich.table import Table

from scripts.util_functions import get_json_data

console = Console(highlight=False)

# -----------------------------------------------------------------------------
#
# Functions for displaying responses back to client
#
# -----------------------------------------------------------------------------

def display_error_message(heading, msgs = []):
    console.print("")
    console.print(heading, style="bold red")
    for msg in msgs:
        console.print(msg, style="white")
    console.print("")

def display_success_message(heading, msgs = []):
    console.print("")
    console.print(heading, style="bold green")
    for msg in msgs:
        console.print(msg, style="white")
    console.print("")

def display_response(heading, msgs = []):
    console.print("")
    console.print(heading, style="bold magenta")
    for msg in msgs:
        console.print(msg, style="white")
    console.print("")

def display_table(headers, items):
    table = Table(show_header=True, header_style="dark_turquoise")
    for name in headers:
        table.add_column(name, width=20)

    for item in items:
        table.add_row(*item)
    
    company_name = get_json_data("current_company")
    date = get_json_data("current_date")
    console.print("")
    console.print(f"- {company_name.capitalize()} -", style="bold blue")
    console.print(f"- {date.capitalize()} -", style="cyan2")
    console.print(table)
    console.print("")
