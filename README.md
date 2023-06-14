<h1 style="font-weight: 300; font-size: 3rem; text-align: center">Super Py</h1>

---

## Getting Started

#### Creating a company

Before you can start buying items you first need to create a company. This can be done with the create-company command like so.

```
python SuperPy create-company --name [COMPANY_NAME]
```

This allows you to keep track of different stock for different stores.

**Warning** _If you try to create a company that already exists you will be asked whether you would like to reset the company. This will remove all data from the company and cannot be undone._

---

#### Switching between companies

A newly created company is automatacally made the current selected company.
To switch between companies we use the change-company command.

```
python SuperPy change-company --name [COMPANY_NAME]
```

_If the company does not yet exist you will be asked if you would like to create the company._

---

#### Buying an item

To purchase an item for the currently selected store use the buy command.

```
python SuperPy buy --product-name [PRODUCT_NAME] --price [PRICE] --expiration-date [EXPIRATION_DATE]
```

---

#### Selling an item

To sell an item use the sell command.

```
python SuperPy sell --product-name [PRODUCT_NAME] --price [PRICE]
```

_If there are multiple of the same item available the item with the nearest expiration date will be sold._

---

#### Changing the date

At all times SuperPy has an iternal conception of what date it is. This allows the program to know whether items are available or expired depending on a given date.
To change the internal date use the change-date command

```
python SuperPy change-date --new-date [NEW_DATE]
```

---

#### Showing Inventory

##### Inventory

To show the current inventory use the inventory command.

```
python SuperPy inventory
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
python SuperPy inventory --expired
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
python SuperPy undo
```

this will undo the last buy or sell action for the selected company

_change-date, create-company & change-company are not effected_

---

#### Get a report

##### Revenue

To get a revenue report for the current day.

```
python SuperPy report revenue
```

To get a revenue report for a certain day.

```
python SuperPy report revenue --date-start [DATE]
```

To get a revenue report for a range of days.

```
python SuperPy report revenue --date-start [DATE_START] --date-end [DATE_END]
```

##### Profit

To get a profit report for the current day.

```
python SuperPy report profit
```

To get a portfit report for a certain day.

```
python SuperPy report profit --date-start [DATE]
```

To get a profit report for a range of days.

```
python SuperPy report profit --date-start [DATE_START] --date-end [DATE_END]
```

---

#### Total Reset

If you would like to completely remove all companies. You can do this with the total-reset command

```
python SuperPy total-reset
```

**Warning** _This action cannot be undone_

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
- **Keyword** - ["yesterday", "today", "tomorrow"] relative to current internal date. Equivilant to [-1, 0 , 1] respectively.

**example**

```
python SuperPy change-date --new-date 2023-06-12
```

changes the current date to 12th June 2023

```
python SuperPy change-date --new-date 3
```

changes the current date to 15th June 2023

```
python SuperPy change-date --new-date yesterday
```

changes the current date to 14th June 2023
