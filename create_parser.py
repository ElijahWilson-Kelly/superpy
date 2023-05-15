import argparse

def create_parser():
    parser = argparse.ArgumentParser()
    
    sub_parsers = parser.add_subparsers(dest="action")

    buy_parser = sub_parsers.add_parser("buy")
    buy_parser.add_argument("--product-name", required=True)
    buy_parser.add_argument("--price", required=True, type=int)
    buy_parser.add_argument("--expiration-date", required=True)

    sell_parser = sub_parsers.add_parser("sell")
    sell_parser.add_argument("--product-name", required=True)
    sell_parser.add_argument("--price", required=True, type=int)

    inventory_parser = sub_parsers.add_parser("inventory")

    reset_parser = sub_parsers.add_parser("reset")
    
    return parser