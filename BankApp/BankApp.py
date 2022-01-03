'''
Programmer: Logan Willans
Description: This program simulates an ATM interface. It stores the following information in a separate text file: usernames, passwords, and balances. The program allows users to login using their usernames and passwords, and it then lets them interact with their accounts in a few different ways. It will then update the information in the separate text file.
Date: 7/24/2020
'''

read_path = 'user_information_read.txt'
write_path = 'user_information_write.txt'
user_information_read = open(read_path, 'r+')
user_information_write = open(write_path, 'r+')
counter = 1
valid_user = False
username_index = ""
selection = ""
list_of_usernames = []
list_of_passwords = []
list_of_balances = []
balance = 0

def get_list_of_usernames():
    global counter
    global list_of_usernames
    for line in user_information_read:
        if counter == 1:
            list_of_usernames = line.split()
        counter += 1
    counter = 1
    user_information_read.seek(0)

def get_list_of_passwords():
    global counter
    global list_of_passwords
    for line in user_information_read:
        if counter == 2:
            list_of_passwords = line.split()
        counter += 1
    counter = 1
    user_information_read.seek(0)

def get_list_of_balances():
    global counter
    global list_of_balances
    for line in user_information_read:
        if counter == 3:
            list_of_balances = line.split()
        counter += 1
    counter = 1
    user_information_read.seek(0)

def username_login():
    global list_of_usernames
    global username_index
    global valid_user
    valid_user = False
    print("Welcome to First Bank of Python ATM.")
    username = input("Enter your username: ")
    for i in list_of_usernames:
        if username == i:
            valid_user = True
            username_index = list_of_usernames.index(username)
    if valid_user == False:
        create_new_user = input("That is not a registered username in our system. Would you like to create an account? (Y/N) ")
        while create_new_user.upper() != "Y" and create_new_user.upper() != "N":
            create_new_user = input('''Invalid input. Please enter either "Y" for "Yes" or "N" for "No". Try again: ''')
        if create_new_user.upper() == "Y":
            existing_username = False
            username = input("Enter a username: ")
            for i in list_of_usernames:
                if username == i:
                    existing_username = True
            while existing_username == True:
                existing_username = False
                username = input("Sorry that username is already taken. Please enter a different username: ")
                for i in list_of_usernames:
                    if username == i:
                        existing_username = True
            list_of_usernames.append(username)
            username_index = list_of_usernames.index(username)
            password = input("Create a password: ")
            list_of_passwords.append(password)
            initial_balance = float(input("Enter an initial balance: "))
            while initial_balance <= 0:
                initial_balance = float(input("Invalid amount. Must be greater than zero. Try again: "))
            list_of_balances.append(str(initial_balance))
            valid_user = True

def password_login():
    global list_of_passwords
    global username_index
    global valid_user
    valid_user = False
    password_counter = 4
    password = input("Enter your password: ")
    if password == list_of_passwords[username_index]:
        valid_user = True
    if password != list_of_passwords[username_index]:
        valid_user = False
    if valid_user == False:
        while password_counter > 1:
            print("Incorrect password. You have " + str(password_counter - 1) + " attempts remaining.")
            password = input("Enter your password: ")
            if password == list_of_passwords[username_index]:
                valid_user = True
                password_counter = 0
            password_counter -= 1
            if password_counter == 1:
                print("Access denied. Terminating login procedure...")

def deposit(x):
    global list_of_balances
    global balance
    balance = float(list_of_balances[username_index])
    balance += x
    print("Before the deposit, your balance was " + str(list_of_balances[username_index]))
    print("Now your balance is " + format(balance, '.2f'))
    list_of_balances[username_index] = format(balance, '.2f')

def withdraw(x):
    global list_of_balances
    global balance
    balance = float(list_of_balances[username_index])
    if x <= balance:
        balance -= x
        print("Before the withdrawal, your balance was " + str(list_of_balances[username_index]))
        print("Now your balance is " + format(balance, '.2f'))
        list_of_balances[username_index] = format(balance, '.2f')
    else:
        print("Insufficient funds.")

def view_balance():
    print("Your balance is " + str(list_of_balances[username_index]))

def main_menu():
    global selection
    global valid_user
    if valid_user == True:
        print('D - Deposit')
        print('W - Withdraw')
        print('B - View Balance')
        print('C - Change User')
        print('E - Exit Program')
        selection = input("Please select an option by entering a corresponding letter key: ")
        while selection.upper() != "D" and selection.upper() != "W"  and selection.upper() != "B" and selection.upper() != "C" and selection.upper() != "E" and valid_user != False:
            selection = input("Invalid input. Please select one of the letter keys as indicated above: ")
        if selection.upper() == "D":
            while True:
                try:
                    deposit_amount = float(input("Enter deposit amount: "))
                    while deposit_amount <=0:
                        print("Invalid input. Must be greater than zero.")
                        deposit_amount = float(input("Enter deposit amount: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a numerical value.")
            deposit(deposit_amount)
        if selection.upper() == "W":
            while True:
                try:
                    withdrawal_amount = float(input("Enter withdrawal amount: "))
                    while withdrawal_amount <= 0:
                        print("Invalid input. Must be greater than zero.")
                        withdrawal_amount = float(input("Enter withdrawal amount: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a numerical value.")
            withdraw(withdrawal_amount)
        if selection.upper() == "B":
            view_balance()
        if selection.upper() == "C":
            print("Changing user...")
            login_sequence()

def update_files():
    for i in list_of_usernames:
        user_information_write.write(i + " ")
    user_information_write.write("\n")
    for i in list_of_passwords:
        user_information_write.write(i + " ")
    user_information_write.write("\n")
    for i in list_of_balances:
        user_information_write.write(i + " ")
    user_information_read.seek(0)
    user_information_write.seek(0)
    for line in user_information_write:
        user_information_read.write(line)

def login_sequence():
    global valid_user
    username_login()
    if valid_user == True:
        password_login()

get_list_of_usernames()
get_list_of_passwords()
get_list_of_balances()
login_sequence()

if valid_user == True:
    print("Please select from the following options: ")
    while selection != "e" and valid_user !=False:
        main_menu()

print("Thank you for using First Bank of Python ATM")

update_files()
user_information_read.close()
user_information_write.close()