<h1 style="font-weight: 300; font-size: 3rem; text-align: center">Super Py</h1>

---

## Getting Started

#### Creating a company

Before you can start buying items you first need to create a company. This can be done with the create-company command like so.

```
python main.py create-company [COMPANY_NAME]
```

we can do this to create multiple companies to keep track of inventory in multiple stores.

**Warning** _If you try to create a company that already exists you will be asked whether you would like to reset the company. This will remove all data from the company and cannot be undone_

---

#### Switching between companies

A newly created company is automatacally made the current selected company.
To switch between companies we use the change-company command

```
python main.py change-company [COMPANY_NAME]
```

_If the company does not yet exist you will be asked if you would like to create the company._

---

#### Buying an item

To purchase an item for the currently selected store use the buy command.

```
python main.py buy --product-name [PRODUCT_NAME] --price [PRICE] --expiration-date [EXPIRATION_DATE]
```

---

#### Selling an item

To sell an item use the sell command.

```
python main.py sell --product-name [PRODUCT_NAME] --price [PRICE]
```

If there are multiple of the same item available the item with the nearest expiration date will be sold.

---

#### Changing the date

At all times SuperPy has an iternal conception of what date it is. This allows the program to know whether items are available or expired depending on a given date.
To change the internal date use the change-date command

```
python main.py change-date --new-date [NEW_DATE]
```

--new-date argument is parsed following [date](#date) format.

---

#### Showing Inventory

##### Inventory

To show the current inventory use the inventory command.

```
python main.py inventory
```

This will show the current inventory based upon the current date and company.

###### Properties Shown

_Product_ - Name of the product
_Number of items_ - Number of the product
_Buy Price (AVG)_ - The average buy price
_Expire (closest)_ - The expiry date of the item that will expired soonest

##### Expired Inventory

If you add the argument _--expired_

```
python main.py inventory --expired
```

It will show all the items that have expired.

###### Properties Shown

_Product_ - Name of the product
_Number of items_ - Number of the product
_Money lost (Total)_ - The total cost of all the items

---

#### Undo an action

if you wish to undo either an action you can use the undo command

```
python main.py undo
```

this will undo the last buy or sell action for the selected company

_change-date, create-company & change-company are not effected_

---

#### Get a report

##### Revenue

To get a revenue report for the current day.

```
python main.py report revenue
```

To get a revenue report for a certain day.

```
python main.py report revenue --date-start [DATE]
```

To get a revenue report for a range of days.

```
python main.py report revenue --date-start [DATE_START] --date-end [DATE_END]
```

##### Profit

To get a profit report for the current day.

```
python main.py report profit
```

To get a portfit report for a certain day.

```
python main.py report profit --date-start [DATE]
```

To get a profit report for a range of days.

```
python main.py report profit --date-start [DATE_START] --date-end [DATE_END]
```

---

#### Formats

Inputs that will be excepted as valid for different types of input.

##### Names

Names can contain lowercase letters [a-z] and uppercase leters [A-Z] and underscore (\_) and hyphen (-). _No spaces or numbers_

Names are not case sensitive. "Orange", "oRange" and "orange" will all refer to the same product.

##### Dates

Valid input for date arguments are:

- **Iso Format** - _YYYY-MM-DD_
- **Whole number (positive or negative)** - +/-{number} number of days relative to the current internal date
- **Keyword** - ["yesterday", "today", "tomorrow] relative to current internal date. Equivilant to [-1, 0 , 1] respectively.

**example**

```
python main.py change-date --new-date 2023-06-12
```

changes the current date to 12th June 2023

```
python main.py change-date --new-date 3
```

changes the current date to 15th June 2023

```
python main.py change-date --new-date yesterday
```

changes the current date to 14th June 2023
