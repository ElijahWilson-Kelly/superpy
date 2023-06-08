import argparse

## report 
# 1 - history
# 2 - multiple companies
# 3 - Inventory update with changes
# 4 - JSON data

def create_parser():
    parser = argparse.ArgumentParser(
        prog='Super Py',
        description='Allows companies to keep track of inventory and revenue over time',
    )
    
    sub_parsers = parser.add_subparsers(dest="action")

    buy_parser = sub_parsers.add_parser("buy", help="buy a new item")
    buy_parser.add_argument("--product-name", required=True, help="(required) - format {[a-zA-Z_]+}")
    buy_parser.add_argument("--price", required=True, help="(required) - format {[0-9]+\.?[0-9]*}")
    buy_parser.add_argument("--expiration-date", required=True, help="(required) - format {YYYY-MM-DD or keywords [yesterday, today, tomorrow]}")

    sell_parser = sub_parsers.add_parser("sell", help="sell an item")
    sell_parser.add_argument("--product-name", required=True)
    sell_parser.add_argument("--price", required=True)

    change_date_parser = sub_parsers.add_parser("change-date", help="change current date")
    change_date_parser.add_argument("new_date")

    report_parser = sub_parsers.add_parser("report", help="income and revenue report")
    report_parser.add_argument("type", choices=["profit", "revenue"])
    report_parser.add_argument("--date")

    create_company_parser = sub_parsers.add_parser("create-company", help="create a new company")
    create_company_parser.add_argument("--name", required=True)

    change_company_parser = sub_parsers.add_parser("change-company", help="change current company")
    change_company_parser.add_argument("--name", required=True)

    inventory_parser = sub_parsers.add_parser("inventory", help="show inventory")
    inventory_parser.add_argument("--expired", action='store_true')

    sub_parsers.add_parser("undo", help="undo last buy or sell")
    
    return parser