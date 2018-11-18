#!/usr/bin/python3

import os
import string
import secrets
from sqlite3 import IntegrityError
import subprocess
from time import sleep
import threading
from crypto import encrypt_db, decrypt_db
from db_utils import (create_new_db,
                      add_new_creds,
                      view_all_creds,
                      count_creds,
                      update_creds_by_id,
                      update_creds_by_account_name)

gpg_passphrase = ""
preloader = ""

def loader():
    global preloader

    while preloader == True:
        print("|", end="\r")
        sleep(.25)

        if preloader == True:
            print("/", end="\r")
            sleep(.25)

        if preloader == True:
            print("-", end="\r")
            sleep(.25)

        if preloader == True:
            print("\\", end="\r")
            sleep(.25)

        print(" ", end="\r")

def get_pw_method():
    valid = False

    while valid == False:
        print("\nWould you like to:")
        print("1) Generate new password")
        print("2) Add pre-created password")
        
        try:
            choice = int(input("Your choice: "))

            if choice == 1 or choice == 2:
                valid = True
                return choice

            else:
                print("\n[ERROR] You must choose 1 or 2.")

        except ValueError:
            print("\n[ERROR] You must choose 1 or 2.")

def get_field_choice():
    valid = False

    while valid == False:
        print("\nChoose a field to edit:")
        print("1) Account/service name")
        print("2) Username/email")
        print("3) Password")
        
        try:
            choice = int(input("Your choice: "))

            if choice == 1 or \
               choice == 2 or \
               choice == 3:

                if choice == 1:
                   field = "accountname"

                if choice == 2:
                    field = "username"

                if choice == 3:
                    field = "password"

                valid = True
                return field

            else:
                print("\n[ERROR] You must choose 1, 2, or 3.")

        except ValueError:
            print("\n[ERROR] You must choose 1, 2, or 3.")

def get_id():
    global preloader
    preloader = True
    wait = threading.Thread(target=loader, daemon=True)
    wait.start()

    if os.path.isfile('pwmanager.sqlite3.gpg'):
        decrypt_db(gpg_passphrase)

    view_all_creds()
    total_creds = count_creds()

    if not os.path.isfile('pwmanager.sqlite3.gpg'):

        encrypt_db(gpg_passphrase)

    preloader = False
    wait.join()

    valid = False

    while valid == False:
        try:
            id = int(input("Enter the ID of the credentials to update: "))

            if id > total_creds or id < 1:
                print("\n[ERROR] You must enter a valid ID.\n")

            else:
                valid = True
                return id
            
        except ValueError:
            print("\n[ERROR] You must enter a valid ID.\n")

def get_account_name():
    valid = False
    
    while valid == False:
        try:
            account_name = str(input("\nEnter the name of the account or service: ")).lower().strip()

            if account_name != "":
                valid = True
                return account_name

            else:
                print("\n[ERROR] You must enter a valid account or service name.")

        except ValueError:
            print("\n[ERROR] You must enter a valid account or service name.")

def get_username():
    valid = False

    while valid == False:
        try:
            username = str(input("Enter the username/email for the account or service: ")).lower().strip()

            if username != "":
                valid = True
                return username

            else:
                print("\n[ERROR] You must enter a valid username or email.\n")

        except ValueError:
            print("\n[ERROR] You must enter a valid username or email.\n")

def get_password():
    valid = False

    while valid == False:
        try:
            pw = str(input("Enter the password for the account or service: ")).strip()

            if pw != "":
                valid = True
                return pw

            else:
                print("\n[ERROR] You must enter a valid password.\n")

        except ValueError:
            print("\n[ERROR] You must enter a valid password.\n")

def get_pw_length():
    valid = False
    valid_choices = [1, 2, 3, 4]
    pw_length = 0

    while valid == False:
        try:
            print("\nChoose the length of your new password:")
            print("1) 8 characters")
            print("2) 16 characters")
            print("3) 32 characters")
            print("4) 64 characters")
            choice = int(input("Your choice (1-4): "))

            if choice in valid_choices:
                if choice == 1:
                    pw_length = 8

                elif choice == 2:
                    pw_length = 16

                elif choice == 3:
                    pw_length = 32

                elif choice == 4:
                    pw_length = 64

                if pw_length != 0:
                    valid = True
                    return pw_length

                else:
                    print("\n[ERROR] You must choose 1, 2, 3, or 4.")

            else:
                print("\n[ERROR] You must choose 1, 2, 3, or 4.")

        except ValueError:
            print("\n[ERROR] You must choose 1, 2, 3, or 4.")

def get_pw_chars():
    valid = False
    uc_valid = False
    lc_valid = False
    d_valid = False
    p_valid = False
    char_list = ""
    punctuation = "~!@#$%^&*()_+=-][{}|;:/?.>,<"

    while valid == False:
        print("\nShould your password contain:")

        while uc_valid == False:
            try:
                uppercase = str(input("Uppercase Letters? (y/n): ")).lower()

                if uppercase == "y":
                    char_list = f"{char_list}{string.ascii_uppercase}"
                    uc_valid = True

                elif uppercase == "n":
                    uc_valid = True
                else:
                    print("\n[ERROR] You must choose y on n.\n")

            except ValueError:
                print("\n[ERROR] You must choose y on n.\n")

        while lc_valid == False:
            try:
                lowercase = str(input("Lowercase Letters? (y/n): ")).lower()

                if lowercase == "y":
                    char_list = f"{char_list}{string.ascii_lowercase}"
                    lc_valid = True

                elif lowercase == "n":
                    lc_valid = True

                else:
                    print("\n[ERROR] You must choose y on n.\n")

            except ValueError:
                print("\n[ERROR] You must choose y on n.\n")

        while d_valid == False:
            try:
                digits = str(input("Digits? (y/n): ")).lower()

                if digits == "y":
                    char_list = f"{char_list}{string.digits}"
                    d_valid = True

                elif digits == "n":
                    d_valid = True

                else:
                    print("\n[ERROR] You must choose y on n.\n")

            except ValueError:
                print("\n[ERROR] You must choose y on n.\n")

        while p_valid == False:
            try:
                punc = str(input("Punctuation? (y/n): ")).lower()

                if punc == "y":
                    char_list = f"{char_list}{punctuation}"
                    p_valid = True

                elif punc == "n":
                    p_valid = True

                else:
                    print("\n[ERROR] You must choose y on n.\n")

            except ValueError:
                print("\n[ERROR] You must choose y on n.\n")

        if char_list != "":
            valid = True
            return char_list

        else:
            uc_valid = False
            lc_valid = False
            d_valid = False
            p_valid = False
            print("\n[ERROR] Your password must contain some characters.")

def create_pw(pw_length, pw_chars):
    pw = ''

    for i in range(int(pw_length)):
        pw = f'{pw}{secrets.choice(pw_chars)}'
    
    return pw

def create_new_creds():
    global preloader
    valid = False

    while valid == False:
        account_name = get_account_name()
        username = get_username()
        pw_length = get_pw_length()
        pw_chars = get_pw_chars()
        pw = create_pw(pw_length, pw_chars)

        try:
            preloader = True
            wait = threading.Thread(target=loader, daemon=True)
            wait.start()

            if os.path.isfile('pwmanager.sqlite3.gpg'):
                decrypt_db(gpg_passphrase)
            
            add_new_creds(account_name, username, pw)

            if not os.path.isfile('pwmanager.sqlite3.gpg'):
                encrypt_db(gpg_passphrase)

            preloader = False
            wait.join()

            valid = True

        except IntegrityError:
            print("\n[ERROR] Account or service name already exists.")
            preloader = True
            wait = threading.Thread(target=loader, daemon=True)
            wait.start()

            if not os.path.isfile('pwmanager.sqlite3.gpg'):
                encrypt_db(gpg_passphrase)

            preloader = False
            wait.join()

def update_creds_method():
    valid = False

    while valid == False:
        print("\nWhat would you like to do:")
        print("1) View all credentials and select by ID")
        print("2) Search credentials by account or service name")
        
        try:
            choice = int(input("Your choice: "))

            if choice == 1 or choice == 2:
                valid = True
                return choice

            else:
                print("\n[ERROR] You must choose 1 or 2.")

        except ValueError:
            print("\n[ERROR] You must choose 1 or 2.")

def add_existing_creds():
    global preloader
    account_name = get_account_name()
    username = get_username()
    pw = get_password()

    preloader = True
    wait = threading.Thread(target=loader, daemon=True)
    wait.start()

    if os.path.isfile('pwmanager.sqlite3.gpg'):
        decrypt_db(gpg_passphrase)

    add_new_creds(account_name, username, pw)

    if not os.path.isfile('pwmanager.sqlite3.gpg'):
        encrypt_db(gpg_passphrase)

    preloader = False
    wait.join()

def choose_action():
    valid = False

    while valid == False:
        print("\nWelcome! What would you like to do?")
        print("1) Generate password for new account")
        print("2) Add pre-created credentials")
        print("3) View all credentials")
        print("4) Update credentials")

        try:
            choice = int(input("Your choice: "))

            if choice == 1 or \
               choice == 2 or \
               choice == 3 or \
               choice == 4:

                valid = True
                return choice

            else:
                print("\n[ERROR] You must choose 1, 2, 3, or 4.")

        except ValueError:
            print("\n[ERROR] You must choose 1, 2, 3, or 4.") 
        
def check_for_db():
    global gpg_passphrase
    global preloader

    if not os.path.isfile('pwmanager.sqlite3.gpg'):
        print("\nIt looks like this is the first run.")
        gpg_passphrase = str(input("Enter a passphrase to access your credentials: "))
        preloader = True
        wait = threading.Thread(target=loader, daemon=True)
        wait.start()
        create_new_db()
        encrypt_db(gpg_passphrase)
        preloader = False
        wait.join()

    else:
        gpg_passphrase = str(input("\nEnter the passphrase to unlock your credentials: "))
        preloader = True
        wait = threading.Thread(target=loader, daemon=True)
        wait.start()
        decrypt_db(gpg_passphrase)
        encrypt_db(gpg_passphrase)
        preloader = False
        wait.join()

def main():
    global gpg_passphrase
    global preloader

    try:
        check_for_db()
        action_choice = choose_action()

        if action_choice == 1:
            create_new_creds()

        elif action_choice == 2:
            add_existing_creds()

        elif action_choice == 3:
            preloader = True
            wait = threading.Thread(target=loader, daemon=True)
            wait.start()

            if os.path.isfile('pwmanager.sqlite3.gpg'):
                decrypt_db(gpg_passphrase)

            view_all_creds()

            if not os.path.isfile('pwmanager.sqlite3.gpg'):
                encrypt_db(gpg_passphrase)

            preloader = False
            wait.join()

        elif action_choice == 4:
            method_choice = update_creds_method()

            if method_choice == 1:
                id = get_id()
                field = get_field_choice()
                
                if field == "accountname":
                    new_cred = get_account_name()

                elif field == "username":
                    new_cred = get_username()

                elif field == "password":
                    pw_method = get_pw_method()

                    if pw_method == 1:
                        pw_length = get_pw_length()
                        pw_chars = get_pw_chars()
                        new_cred = create_pw(pw_length, pw_chars)

                    elif pw_method == 2:
                        new_cred = get_password()

                preloader = True
                wait = threading.Thread(target=loader, daemon=True)
                wait.start()

                if os.path.isfile('pwmanager.sqlite3.gpg'):
                            decrypt_db(gpg_passphrase)

                update_creds_by_id(id, field, new_cred)

                if not os.path.isfile('pwmanager.sqlite3.gpg'):
                    encrypt_db(gpg_passphrase)

                preloader = False
                wait.join()

            elif method_choice == 2:
                account_name = get_account_name()
                field = get_field_choice()

                if field == "accountname":
                    new_cred = get_account_name()

                elif field == "username":
                    new_cred = get_username()

                elif field == "password":
                    pw_method = get_pw_method()

                    if pw_method == 1:
                        pw_length = get_pw_length()
                        pw_chars = get_pw_chars()
                        new_cred = create_pw(pw_length, pw_chars)

                    elif pw_method == 2:
                        new_cred = get_password()

                preloader = True
                wait = threading.Thread(target=loader, daemon=True)
                wait.start()

                if os.path.isfile('pwmanager.sqlite3.gpg'):
                            decrypt_db(gpg_passphrase)

                update_creds_by_account_name(account_name, field, new_cred)

                if not os.path.isfile('pwmanager.sqlite3.gpg'):
                    encrypt_db(gpg_passphrase)

                preloader = False
                wait.join()
            
    except KeyboardInterrupt:
        print("\nGoodbye.")
        if not os.path.isfile('pwmanager.sqlite3.gpg'):
            try:
                preloader = True
                wait = threading.Thread(target=loader, daemon=True)
                wait.start()
                encrypt_db(gpg_passphrase)
                preloader = False
                wait.join()
            except FileNotFoundError:
                pass

        exit(0)

if __name__ == '__main__':
    main()
