""" 

    This is a simple terminal program that will help you pack things for your trips.

    You can edit presets in config.json, just stick with the syntax.

    Add things you need on every trip into the "Persistant" category (things from this 
    category will be added to your packing list regardless of the preset).

    Items defined with a multiplier: "Socks": 1.2, will get the amount assigned as = multiplier * # of days
    Items defined with a string number: "Jeans": "1", are independent of days
    Items defined with a empty string: Backpack: "", are basically only notes and do not have any amount

"""


import json
import time
import os


def clearConsole():  # To simplify clearing console
    return os.system('cls' if os.name in ('nt', 'dos') else 'clear')


def get_list(list):
    while True:
        chosen_preset = input("\n")

        try:
            return list[chosen_preset]

        except KeyError:
            print('\n"{}" does not exist, try again: '.format(chosen_preset))


def get_number(fraze, cancel=False):  # Tries to get a number
    while True:
        try:
            respond = input(fraze)
            if cancel and respond == 'C':
                return "\/NaN\/"

            return int(respond)
        except ValueError:
            print('\n"{}" is not a valid number, try again: '.format(respond))


def get_item(fraze, list, cancel=False):  # Tries to get a item
    while True:
        try:
            respond = input(fraze)
            if cancel and respond == 'C':
                return "\/NaN\/"

            list[respond]
            return respond
        
        except KeyError:
            print('\n"{}" is not valid, try again: '.format(respond))
            

def display_content(list):  # Displays content from a list
    for content in list.keys():
        if type(list[content]) is float or type(list[content]) is int:
            print("{}x {}".format(list[content], content))

        elif type(list[content]) is str:
            if list[content] == '':
                print("-  {}".format(content))
            else:
                print("{}  {}".format(list[content], content))

    print("\n") 


def enumerate_items():  # Calculates the amounts according to config.json
    global ITP
    actor = {}

    for item in ITP.keys():
        if type(ITP[item]) is float or type(ITP[item]) is int:
            actor = actor | {item: round(ITP[item] * days)}

        elif type(ITP[item]) is str:
            if ITP[item] == '':
                actor = actor | {item: ''}
            else:
                actor = actor | {item: int(ITP[item])}

    ITP = actor


def increase_item_amount():
    global ITP
    item = get_item("What item do you need more of? ('C' to cancel) ", ITP, cancel=True)
    if item == "\/NaN\/":
        return

    if type(ITP[item]) is str:  # Check if this item can be increased in amount
        print("This item cannot be increased in amount.")
        time.sleep(1.5)
        return

    amount = get_number("How much more? ", cancel=True)
    if amount == "\/NaN\/":
        return

    ITP[item] += int(amount)


def decrease_item_amount():
    global ITP
    item = get_item("What item do you need less of? ('C' to cancel) ", ITP, cancel=True)
    if item == "\/NaN\/":
        return

    if type(ITP[item]) is str:
        print("This item cannot be decreased in amount.")
        time.sleep(1.5)
        return

    amount = get_number("How much less? ", cancel=True)
    if amount == "\/NaN\/":
        return

    if ITP[item] - int(amount) < 1:
        ITP.pop(item)
        return

    ITP[item] -= int(amount)


def delete_item(list):
    item = get_item("What item do you want to remove? ('C' to cancel) ", ITP, cancel=True)
    if item == "\/NaN\/":
        return

    list.pop(item)
    

def add_item():
    global ITP
    while True:
        clearConsole()
        print("\nIs this what you need?:")
        display_content(ITP)
        item = input("Add any item to the list by typing its name.\nType '+' to increase the amount of a item or '-' to decrease it.\nType '/' to delete an item.\n\n(press enter to continue) ")

        if item == "":
            break

        elif item == '+':
            increase_item_amount()

        elif item == '-':
            decrease_item_amount()

        elif item == '/':
            delete_item(ITP)

        else:
            while True:
                number = input("How many? ('-' for no amount, 'C' to cancel) ")
                if number == '-':
                    ITP = ITP | {item: ''}
                elif number == 'C':
                    pass
                else:
                    try:
                        ITP = ITP | {item: int(number)}
                        break
                    except ValueError:
                        print('"{}" is invalid, try again.\n'.format(number))


def pack_item(item):
    API[item] = ITP.pop(item)


with open("config.json", "r", encoding='utf-8') as file:
    jFile = json.load(file)


# """ Pick a preset and # of days """ #
clearConsole()
print("Hi, let's start packing!\n")
print("Choose a preset to use: ")

for presets in jFile.keys():
    if presets != "Persistant":
        print(presets)


ITP = get_list(jFile) | jFile["Persistant"]  # Items To Pack
days = get_number("How many day do you plan to travel? ")
enumerate_items()


# """ Verify chosen items """ #
add_item()


# """ Packing assistant """
API = {}  # Already Packed Items
while len(ITP) != 0:
    clearConsole()
    print("\nNow get to packing!\nType the items you packed into console to cross them off.\n\nNeed to pack:")
    display_content(ITP)
    print("\nAlready packed:")
    display_content(API)

    try:
        pack_item(input(""))
    except KeyError:
        print("This was not on your list!")
        time.sleep(0.75)

clearConsole()
print("\nYou have everything you need!")
display_content(API)
print("Have a save trip!")
