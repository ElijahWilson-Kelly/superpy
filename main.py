# Imports
from datetime import date

# My Imports
from create_parser import create_parser
from actions import buy_item, sell_item, show_inventory, reset

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"


# Your code below this line.

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
                show_inventory()
            case "reset":
                reset()
    except Exception as msg:
        print(msg)
    
    
    


if __name__ == "__main__":
    main()
