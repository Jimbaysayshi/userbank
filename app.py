import pickle
import time
import pyperclip
import bcrypt
import sys

salt = "$2a$12$x34Q56uw3XyoZ5Cqty15M."


def reset_masterkey():
    """reset masterkey, so new masterkey can be set"""
    try:
        with open('master.p', 'rb') as master_p:
            master = pickle.load(master_p)
            if master['key'] == None:
                return
            else:
                master['key'] = None
        with open('master.p', 'wb') as master_p:
            pickle.dump(master, master_p)
        print("Masterkey has been reset")
    except EOFError:
        print("There is no masterkey")


def is_there_masterkey():
    """check if master key already exists. Return True if it exists"""
    try:
        with open('master.p', 'rb') as master_p:
            master = pickle.load(master_p)
            print(master)
            if master['key'] != None:
                return True
    except EOFError:
        return False
    return False


def set_masterkey():
    """ set masterkey """
    # TODO make sure the password is saved and notify the user
    if is_there_masterkey() == True:
        print("There is a masterkey already, unable to set a new one")
        return
    master = {}
    masterkey = input("Set a masterkey: ")
    masterkey_two = input("Give masterkey again: ")
    if masterkey != masterkey_two:
        print('Passwords didnt match')
        # time.sleep(5)
        return set_masterkey()
    hashed = bcrypt.hashpw(masterkey, salt)
    master['key'] = hashed
    with open('master.p', 'wb') as master_p:
        pickle.dump(master, master_p)


def check_for_masterkey():
    """check if given masterkey is found in the master.p"""

    masterkey = input("Enter your masterkey: ")
    hashed = bcrypt.hashpw(masterkey, salt)
    with open('master.p', 'rb') as master_p:
        master = pickle.load(master_p)
        if master['key'] == hashed:
            return True
        else:
            print("Masterkey didn't work")
            return check_for_masterkey()


def get_user():
    """check if program is in the credentials list"""

    program = input("Enter program name: ").lower()
    try:
        with open('secrets.p', 'rb') as secrets_p:
            secrets = pickle.load(secrets_p)
            for key, value in secrets.items():
                if program == key.lower():
                    username = value[0]
                    password = value[1]
                    pyperclip.copy(username)
                    action = input(
                        f"Username for {program}: {username} copied to clipboard. Press 'Enter' to copy password to clipboard")
                    pyperclip.copy(password)
                    action = input(
                        f"Password for {program} copied to clipboard. Press 'Enter' to clear clipboard")
                    pyperclip.copy("")
                    return
            print("Program not found from credentials")

    except EOFError:
        print("Credential list is empty")


def add_program():
    """save a new program"""

    with open("programs.txt", "r+", encoding='utf-8') as programs:

        programs_list = programs.read().splitlines()
        new_program = input("Enter new program name: ").lower()
        for program in programs_list:
            if program.strip() == new_program.strip():
                print(f"Credentials for {new_program} already exists")
                return
        else:
            programs.write(f"{new_program}\n")
            return add_credentials(new_program)


def add_credentials(new_program):
    """save username and password for given program"""

    username = input("Enter username: ")
    password = input("Enter password: ")
    with open('secrets.p', 'rb') as secrets_p:
        try:
            secrets = pickle.load(secrets_p)
            secrets[new_program] = [username, password]
        except (TypeError, EOFError):
            secrets = {}

    with open('secrets.p', 'wb') as secrets_p:
        secrets[new_program] = [username, password]
        pickle.dump(secrets, secrets_p)

        # TODO check if dumping is successful


def list_programs():
    """prints out a list of programs that have saved credentials"""
    try:
        with open("programs.txt", "r", encoding='utf-8') as programs:
            programs_list = programs.read().splitlines()
            if programs_list == []:
                print("No saved programs")
            else:
                print(programs_list)
    except EOFError:
        print("No saved programs")


def list_credentials():
    """FOR DEBUGGING ONLY"""
    # TODO GET RID OF THIS WHEN READY
    try:
        with open("secrets.p", "rb") as credentials:
            credentials_list = pickle.load(credentials)
            print(credentials_list)
    except EOFError:
        print("No saved credentials")


def clear():
    """clear programs and credential files"""
    choose = input(
        "You are about to erase programs and credentials. Are you sure? y/n ").lower()
    if choose == "y":
        clear_all_programs()
        clear_all_credentials()
    else:
        return


def clear_all_programs():
    """clear all programs"""
    with open("programs.txt", "r+") as programs:
        programs.truncate(0)
    print("Programs erased")


def clear_all_credentials():
    with open("secrets.p", "wb") as credentials:
        credentials.truncate(0)
    print("Credentials erased")


def del_program():
    """delete credentials and program from programs.txt"""
    program = input("Enter program name: ").lower()
    with open('programs.txt', 'r') as programs:
        programs_list = programs.read().splitlines()
        for i, p in enumerate(programs_list):
            if p.strip() == program.strip():
                programs_list.pop(i)
                print(f"Program {p.strip()} has been removed")
    with open('programs.txt', 'w') as programs:
        for p in programs_list:
            programs.write(p)
    del_credential(program.strip())


def del_credential(program):
    """delete credentials assoiated with program"""
    cred = {}
    try:
        with open("secrets.p", "rb") as secrets_p:

            credentials = pickle.load(secrets_p)
            for k, v in credentials.items():
                if k.strip() == program:
                    del credentials[k]
                    cred = credentials
                    print(f"Credentials for {program} has been removed")
        with open("secrets.p", "wb") as secrets_p:
            pickle.dump(credentials, secrets_p)
    except EOFError:
        print(f"No credentials for {program} found")

# def change_password():
#    """change existing password"""
#    program = input("Enter program name: ").lower()
#    with


def change_username():
    """change existing username"""
    pass


def command(args):

    commands = {"reset_masterkey": reset_masterkey, "set_masterkey": set_masterkey,
                "check_for_masterkey": check_for_masterkey, "add_program": add_program,
                "list_programs": list_programs, "list_credentials": list_credentials,
                "clear": clear, "get_user": get_user, "del_program": del_program}

    for c in range(1, len(args)):
        if args[c] == "commands":
            for i in commands.keys():
                print(f"{i}")
            break
        try:
            commands[args[c]]()
        except KeyError:
            print(f"{args[c]} is not a valid command")


if __name__ == "__main__":

    command(sys.argv)

    # reset_masterkey()
    # if is_there_masterkey() == False:
    #    set_masterkey()
    # if check_for_masterkey() == True:
    # clear()
    # list_credentials()
    # list_programs()
    # get_user()
    # add_program()
    # get_user()
