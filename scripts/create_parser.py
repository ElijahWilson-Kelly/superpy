import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        prog='SuperPy',
        description='Allows companies to keep track of inventory and revenue over time',
    )
    
    sub_parsers = parser.add_subparsers(dest="action")

    buy_parser = sub_parsers.add_parser("buy", help="buy a new item")
    buy_parser.add_argument("--product-name", required=True, help="(required) - format {[a-zA-Z_]+}")
    buy_parser.add_argument("--price", required=True, help="(required) - format {[0-9]+\.?[0-9]*}")
    buy_parser.add_argument("--expiration-date", required=True, help="(required) - format {YYYY-MM-DD} or {-?d+} or keywords {yesterday, today, tomorrow}")

    sell_parser = sub_parsers.add_parser("sell", help="sell an item")
    sell_parser.add_argument("--product-name", required=True, help="(required) - format {[a-zA-Z_]+}")
    sell_parser.add_argument("--price", required=True, help="(required) - format {[0-9]+\.?[0-9]*}")

    change_date_parser = sub_parsers.add_parser("change-date", help="change current date")
    change_date_parser.add_argument("--new-date", required=True, help="(required) - format {YYYY-MM-DD} or {-?d+} or keywords {yesterday, today, tomorrow}")

    report_parser = sub_parsers.add_parser("report", help="profit and revenue report")
    report_parser.add_argument("type", choices=["profit", "revenue"], help="type of report - {revenue or profit}]")
    report_parser.add_argument("--date-start", help="start date of range for report (optional - defaults to today) - format {YYYY-MM-DD} or {-?d+} or keywords {yesterday, today, tomorrow}")
    report_parser.add_argument("--date-end", help="end date of range for report (optional - defaults to start date) - format {YYYY-MM-DD or {-?d+} or keywords [yesterday, today, tomorrow]}")

    create_company_parser = sub_parsers.add_parser("create-company", help="create a new company")
    create_company_parser.add_argument("--name", required=True, help="(required) - format {[a-zA-Z-_]+}")

    change_company_parser = sub_parsers.add_parser("change-company", help="change current company")
    change_company_parser.add_argument("--name", required=True, help="(required) - format {[a-zA-Z-_]+}")

    inventory_parser = sub_parsers.add_parser("inventory", help="show inventory")
    inventory_parser.add_argument("--expired", action='store_true', help="(optional) - shows expired items instead")

    sub_parsers.add_parser("undo", help="undo last buy or sell")

    sub_parsers.add_parser("delete-all")
    
    return parser