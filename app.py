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
                    action = input("Username for {}: {} copied to clipboard. Press 'Enter' to copy password to clipboard").format(program, username)
                    pyperclip.copy(password)
                    action = input("Password for {} copied to clipboard. Press 'Enter' to clear clipboard").format(program)
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
                print("Credentials for {} already exists").format(new_program)
                return
        else:
            programs.write(new_program + "\n")
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
                print("Program {} has been removed").format(p.strip())
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
                    print("Credentials for {} has been removed").format(program)
        with open("secrets.p", "wb") as secrets_p:
            pickle.dump(credentials, secrets_p)
    except EOFError:
        print("No credentials for {} found").format(program)

def change_password():
    """change existing password"""
    progs = {}
    program = input("Enter program name: ").lower()
    try:
        with open('secrets.p', 'rb') as secrets_p:
            programs = pickle.load(secrets_p)
            credentials = programs.get(program)
            old_pass = input("Enter old password: ")
            if old_pass == credentials[1]:
                new_pass = input("Enter new password: ")
                credentials[1] = new_pass
                programs[program] = credentials
                progs = programs
            else:
                print("Password for {} didn't match").format(program)
                return
    except EOFError:
        print("No credentials for {} found").format(program)
        return
    with open ('secrets.p', 'wb') as secrets_p:
        pickle.dump(progs, secrets_p)


def change_username():
    """change existing username"""
    progs = {}
    program = input("Enter program name: ").lower()
    try:
        with open('secrets.p', 'rb') as secrets_p:
            programs = pickle.load(secrets_p)
            credentials = programs.get(program)
            new_user = input("Enter new username: ")
            credentials[0] = new_user
            programs[program] = credentials
            progs = programs
    except EOFError:
        print("No credentials for {} found").format(program)
    with open ('secrets.p', 'wb') as secrets_p:
        pickle.dump(progs, secrets_p)


def change_credentials():
    """change both existing credentials"""
    progs = {}
    program = input("Enter program name: ").lower()
    try:
        with open('secrets.p', 'rb') as secrets_p:
            programs = pickle.load(secrets_p)
            credentials = programs.get(program)
            old_pass = input("Enter old password: ")
            if old_pass == credentials[1]:
                new_user = input("Enter new username: ")
                new_pass = input("Enter new password: ")
                credentials[0], credentials[1] = new_user, new_pass
                programs[program] = credentials
                progs = programs
            else:
                print("Password for {} didn't match").format(program)
                return
    except EOFError:
        print("No credentials for {} found").format(program)
        return
    with open ('secrets.p', 'wb') as secrets_p:
        pickle.dump(progs, secrets_p)

def command(args):

    commands = {"reset_masterkey": reset_masterkey, "set_masterkey": set_masterkey,
                "check_for_masterkey": check_for_masterkey, "add_program": add_program,
                "list_programs": list_programs, "list_credentials": list_credentials,
                "clear": clear, "get_user": get_user, "del_program": del_program,
                "change_password": change_password, "change_username": change_username,
                "change_credentials": change_credentials}

    for c in range(1, len(args)):
        if args[c] == "commands":
            for i in commands.keys():
                print(i)
            break
        try:
            commands[args[c]]()
        except KeyError:
            print("{} is not a valid command, get list of commands with 'commands'").format(args[c])


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
