# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.
from scripts.create_parser import create_parser
from scripts.actions import buy_item, sell_item, show_inventory, show_expired_items, report, change_date, create_company, change_current_company, undo, delete_everything
from scripts.console_display import display_error_message
from scripts.util_functions import InvalidInput, ItemNotInStock, NoCompanySelected

def main():
    parser = create_parser()
    commands = vars(parser.parse_args())
    try:
        match commands["action"]:
            case "buy": 
                buy_item(commands)
            case "sell":
                sell_item(commands)
            case "inventory":
                if commands["expired"]:
                    show_expired_items()
                else:
                    show_inventory()
            case "report":
                report(commands)
            case "change-date":
                change_date(commands["new_date"])
            case "create-company":
                create_company(commands["name"])
            case "change-company":
                change_current_company(commands["name"])
            case "undo":
                undo()
            case "delete-all":
                delete_everything()
    except (InvalidInput, ItemNotInStock, NoCompanySelected) as error:
        display_error_message(error.title, error.descriptions)
    
    
    

if __name__ == "__main__":
    main()
