<h1 style="font-weight: 350; font-size: 3rem; text-align: center">Report</h1>

---

### Auto update inventory

After most actions (buy, sell, change-date, change-company etc) the inventory will auto update. So that ./inventory.csv represents a realtime view of the inventory for a given company and date. This made it easier to keep track of currently available and expired items when showing a report or checking availability when selling an item. If the system was to be scaled alot this aproach might prove to be slightly inefficient as I am reading and writing to a csv file when its not strictly necessary. However I decided that for my purposes it was worth it as it helped make my code easier to understand.

### History and undo actions

I wanted to give people the ability to undo buying and selling if they desired so for each company i also added a history.txt file. Whenever an item is bought or sold "buy" or "sell" is append onto a new line in the file. Then if the "undo" action is called the last item from the history file is taken of and depending on whether it is "buy" or "sell" the appropraite csv file has its last item removed.

### Multiple companies

I wanted to add the ability to add multiple companies and be able to switch between them. I thought this could be useful to represent multiple stores for a big company or different departments in a big store if it was useful to have them seperated. This required keeping track of the currently selected company so i decided to put that as well as the current date in a json file called data.json.
I also implemented some path generating functions to remove complexity of getting the correct path to the correct csv file depending on the current company.

### Error Handling and Message Response

I wrapped all the main action functions in a try except statement. This allowed me to write a few custom Exceptions for handleing Improper input from the client and send back a response message without the application crashing. An example of this is if they entered a date which was not valid an InvalidInput Exception would get raised sending a message to the user that the date they entered was invalid.

I also added some general and success responses to my app to give the client information about the actions that where taken and what has changed. For the sake of consistency I decided that all response functions would take a heading as its first argument and a list {[]} of messages as its second argument.
