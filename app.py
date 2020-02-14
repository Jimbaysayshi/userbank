import pickle
import time

import bcrypt

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
    except EOFError:
        pass


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
    master = {}
    masterkey = input("Set a masterkey: \n")
    masterkey_two = input("Give masterkey again: \n")
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

    masterkey = input("Enter your masterkey:\n")
    hashed = bcrypt.hashpw(masterkey, salt)
    with open('master.p', 'rb') as master_p:
        master = pickle.load(master_p)
        if master['key'] == hashed:
            return True
        else:
            print("Masterkey didn't work")
            return check_for_masterkey()


def check_for_program():
    """check if program is in the credentials list"""

    program = input("Enter program name").lower()
    with open('secrets.p', 'rb') as secrets_p:
        secrets = pickle.load(secrets_p)
        for key, value in secrets.keys():
            if program == key.lower():
                username = value[0]
                password = value[1]
                return username, password


def add_program():
    """save new program"""

    new_program = input("Enter new program name")
    with open("programs.txt", "a+") as data:
        programs = data.read()
        if new_program.lower() in programs:
            print(f"Credentials for {new_program} already exists")
            return
        else:
            data.write(new_program)
            return add_credentials(new_program)


def add_credentials(new_program):
    """save username and password for given program"""
    pass


def list_all_programs():
    """return a list of programs that have saved credentials"""
    pass


def secure_pw():
    """hash & salt the password"""
    pass


def check_pw():
    """check for password hash in secrets.p after """
    pass


def delete_credentials():
    """delete credentials and program from programs.txt"""
    pass


def change_password():
    """change existing password"""
    pass


def change_username():
    """change existing username"""
    pass


if __name__ == "__main__":
    reset_masterkey()
    if is_there_masterkey() == False:
        set_masterkey()
    if check_for_masterkey() == True:
