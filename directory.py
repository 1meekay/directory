from directoryClass import sqlite3, Contacts, conn, cursor
import sendSMS, pandas, pickle

def welcome(file_name):
    print("\n=========================\n"
          "Welcome to the Directory.\n"
          "=========================")
    login(file_name)

def login(file_name):
    ui_pass = input('\nEnter the password: ')

    if ui_pass != create_password(file_name):
        print(">> Sorry, wrong password.")
        login(file_name)

    else:
        print('>> Welcome!')
        start_menu()

def create_table():
    try:
        cursor.execute("""CREATE TABLE contacts (
                    name text,
                    number integer) """)
    except sqlite3.OperationalError:
        pass

def start_menu():
    user_action = input('\n===========================\n'
                        'What would you like to do?\n'
                        '===========================\n'
                        'a: Add contact\n'
                        'c: Change contact\n'
                        'd: Delete contact\n'
                        'f: Find contact\n'
                        'v: View contacts\n'
                        '---------------------------\n'
                        'sms: Send SMS\n'
                        '---------------------------\n'
                        'pass: Change password\n'
                        '---------------------------\n'
                        'q: Quit\n'
                        '===========================\n\n'
                        'Enter here: ')
    menu(user_action)

def menu(user_action):
    actions_list = ['a', 'c', 'd', 'f', 'v', 'q', 'sms', 'pass']

    if user_action not in actions_list:
        user_action = input('>> Action not recognized, please try again.\n\n'
                            'Enter here: ')
        menu(user_action)
    else:
        if user_action == 'a':
            add_contact()
        elif user_action == 'c':
            change_contact()
        elif user_action == 'd':
            delete_contact()
        elif user_action == 'f':
            find_contact()
        elif user_action == 'v':
            view_contacts()
        elif user_action == 'sms':
            send_message()
        elif user_action == 'pass':
            change_password()
        elif user_action == 'q':
            exit_directory()

def add_contact():
    name = input('\nEnter contact name: ')
    number = int(input("Enter {}'s number: ".format(name)))

    new_contact = Contacts(name, number)

    cursor.execute("INSERT INTO contacts VALUES (?, ?)", (new_contact.name, new_contact.number))
    conn.commit()

    view_contacts()

def change_contact():
    name = input('\nWhich contact would you like to change? Enter name: ')

    results = cursor.execute("SELECT * FROM contacts WHERE name = (?)", (name,)).fetchall()

    list_results = []

    for items in results:
        for item in items:
            list_results.append(item)

    if name not in list_results:
        another = input('>> This contact does not exist.\n'
                        '>> Try again? (y/n): ')

        if another == 'y':
            change_contact()
        elif another == 'n':
            proceed()
        else:
            print('>> Response not recognized.')
            change_contact()
    else:
        if list_results.count(name) > 1:
            print('\n>> There is more than one {}.'.format(name))

            number_of_name = int(
                input('\nEnter the number of the {} contact that you want to change: '.format(name)))

            if number_of_name not in list_results:
                print(">> Number doesn't match. Try again.")
                change_contact()
            else:
                target_name = cursor.execute("SELECT * FROM contacts WHERE number = (?)", (number_of_name,)).fetchone()[0]

                which_change(target_name, number_of_name)
        else:
            target_number = cursor.execute("SELECT number FROM contacts WHERE name = (?)", (name,)).fetchone()[0]

            which_change(name, target_number)

def which_change(name, number):
    def change_name(old_name, number):
        new_name = input("\n>> Enter {}'s new name: ".format(old_name))

        cursor.execute("UPDATE contacts SET name = (?) WHERE name = (?) AND number = (?)",
                       (new_name, old_name, number,))
        conn.commit()

        view_contacts()

    def change_number(name, old_number):
        new_number = int(input("\n>> Enter {}'s new number: ".format(name)))

        cursor.execute("UPDATE contacts SET number = (?) WHERE name = (?) AND number = (?)",
                       (new_number, name, old_number,))
        conn.commit()

        view_contacts()

    which = input("\nWould you like to change {}'s name or number?"
                  "\n[1-name, 2-number]: ".format(name))

    if which == '1':
        change_name(name, number)
    elif which == '2':
        change_number(name, number)
    else:
        print('>> Response not recognized.')
        which_change(name, number)

def delete_contact():
    name = input('\nEnter the name of the contact you wish to delete: ')

    search_results = cursor.execute("SELECT * FROM contacts WHERE name = (?)", (name,)).fetchall()

    list_of_names = []
    list_of_numbers = []

    for i in range(0, search_results.__len__()):
        list_of_names.append(search_results[i][0])

    if list_of_names.__contains__(name):
        if list_of_names.count(name) > 1:
            print(">> Multiple {}s were found.\n".format(name))

            for some in search_results:
                print(some)

            numbers = cursor.execute("SELECT number FROM contacts WHERE name =  (?)", (name,)).fetchall()

            for items in numbers:
                for number in items:
                    list_of_numbers.append(number)

            target_number = int(
                input('\nEnter the number of the {} contact that you wish to delete: '.format(name)))

            if target_number not in list_of_numbers:
                print(">> Number doesn't match any of the contacts.")
                proceed()
            else:
                cursor.execute("DELETE FROM contacts WHERE name = (?) and number = (?)", (name, target_number,))
                conn.commit()

                print(">> {} has been deleted.".format(name))
                view_contacts()
        else:
            cursor.execute("DELETE FROM contacts WHERE name = (?)", (name,))
            conn.commit()

            print(">> {} has been deleted.".format(name))
            view_contacts()
    else:
        print(">> {} not found.".format(name))
        proceed()

def find_contact():
    name = input('\nEnter the name of the contact you wish to find: ')

    search_results = cursor.execute("SELECT * FROM contacts WHERE name = (?)", (name,)).fetchall()

    list_of_names = []

    for i in range(0, search_results.__len__()):
        list_of_names.append(search_results[i][0])

    if list_of_names.__contains__(name):
        if list_of_names.count(name) > 1:
            print(">> Multiple {}s were found.\n".format(name))

            for item in search_results:
                print(item)
            proceed()
        else:
            target_number = cursor.execute("SELECT number FROM contacts WHERE name = (?)", (name,)).fetchone()[0]

            print(">> {} has been found. {}'s number is {}.".format(name, name, target_number))
            proceed()
    else:
        print(">> {} not found.".format(name))
        proceed()

def view_contacts():
    contacts = pandas.DataFrame(cursor.execute("SELECT * FROM contacts ORDER BY name").fetchall())
    contacts.columns = ['Name', 'Number']

    print()
    print(contacts)

    proceed()

def send_message():
    print("\n==============="
          "\nWelcome to SMS."
          "\n===============")

    to = input("\nTo: ")

    search_results = cursor.execute("SELECT * FROM contacts WHERE name = (?)", (to,)).fetchall()

    list_of_names = []
    list_of_numbers = []

    for i in range(0, search_results.__len__()):
        list_of_names.append(search_results[i][0])

    if list_of_names.__contains__(to):
        if list_of_names.count(to) > 1:
            print(">> Multiple {}s were found.\n".format(to))

            for some in search_results:
                print(some)

            numbers = cursor.execute("SELECT number FROM contacts WHERE name =  (?)", (to,)).fetchall()

            for items in numbers:
                for number in items:
                    list_of_numbers.append(number)

            target_number = int(input('\nEnter the number of the {} contact that you wish to text: '.format(to)))

            if target_number not in list_of_numbers:
                print(">> Number doesn't match any of the contacts.")
                proceed()
            else:
                message = input("Message: ")
                sendSMS.send(target_number, message)
                print("\nYour message to {} has been sent.".format(to))
                proceed()
        else:
            message = input("Message: ")
            number = cursor.execute("SELECT number FROM contacts WHERE name =  (?)", (to,)).fetchone()[0]
            sendSMS.send(number, message)
            print("\nYour message to {} has been sent.".format(to))
            proceed()
    else:
        print(">> {} not found.".format(to))
        proceed()

def proceed():
    user_proceed = input('\nHow would you like to proceed?\n'
                         'm: Return to Main Menu\n'
                         'q: Quit\n\n')

    if user_proceed == 'm':
        start_menu()
    elif user_proceed == 'q':
        exit_directory()
    else:
        print('>> Response not recognized.')
        proceed()

def exit_directory():
    print('>> Enjoy the rest of your day, goodbye!')
    conn.close()

    quit()

def create_password(file):
    try:
        with open('{}.txt'.format(file), 'r') as vault_pass:
            user_pass = vault_pass.read()

            if user_pass.__len__() > 0:
                return user_pass
            else:
                raise FileNotFoundError
    except FileNotFoundError:
        new_pass = input("\n=============================\n"
                         "Welcome to Password Creation.\n"
                         "=============================\n\n"
                         "Enter new password: ")

        with open('{}.txt'.format(file), 'w') as new_vault_pass:
            new_vault_pass.write(new_pass)

        print(">> New password created.")
        create_password(file)

def change_password():
    def retry_options(retry):
        if retry == 'm':
            start_menu()
        elif retry == 'r':
            change_password()
        elif retry != 'm' or 'r':
            unrecognized = input('>> Unrecognized response. Try again.\n\n'
                                 'How would you like to proceed?\n'
                                 'm: Return to Main Menu\n'
                                 'r: Retry password change\n\n')
            retry_options(unrecognized)

    p_in = pickle.load(open('file.pickle', 'rb'))

    old_pass = input('\nEnter old password: ')

    if old_pass != create_password(p_in):
        wrong_pass = input('>> Sorry, you have entered the wrong password.\n\n'
                           'How would you like to proceed?\n'
                           'm: Return to Main Menu\n'
                           'r: Retry password change\n\n')
        retry_options(wrong_pass)
    else:
        new_pass = input('Please enter new password: ')

        with open('{}.txt'.format(p_in), 'w') as new_vault_pass:
            new_vault_pass.write(new_pass)

        print('>> You have successfully changed the password.')
        proceed()

def start():
    try:
        with open('file.pickle', 'wb') as p_out:
            pickle.dump(input('\nEnter password file name (omit file extenstion): '), p_out)
            p_out.close()

        p_in = pickle.load(open('file.pickle', 'rb'))

        if p_in.isidentifier():
            create_password(p_in)
            welcome(p_in)
            create_table()
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        print('>> Unsupported file name. Valid identifiers only.')
        start()

if __name__ == '__main__':
    start()