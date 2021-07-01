import pyrebase
import stdiomask
import db_info

firebaseConfig = db_info.firebaseConfig

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


def log_in():
    print("Log in...")
    email = input("Your email: ")
    #password = input("Your password: ")
    password = stdiomask.getpass(prompt="Your password: ", mask="*")
    try:
        login = auth.sign_in_with_email_and_password(email, password)
        print("Successfully logged in!")
    except:
        print("Invalid email or password")
        log_in()
    return


def sign_up():
    print("Sign in...")
    email = input("Your email: ")
    #password = input("Your password: ")
    password = stdiomask.getpass(prompt="Your password: ", mask="*")
    password_repeat = stdiomask.getpass(prompt="Repeat your password: ", mask="*")
    if password == password_repeat:
        try:
            user = auth.create_user_with_email_and_password(email, password)
            print("Your account is created")
            ask=input("Do you want to login?[y/n] ")
            if ask=='y':
                log_in()
            elif ask == 'n':
                pass
            else:
                print("Error")
                exit()
        except:
            print("Email already exists")
        return
    else:
        print("Passwords dont match. Try again")
        sign_up()


def add_note():

    user_id = auth.current_user['localId']
    note = input("Enter Your note here ")
    data = {"note": note}
    db.child("notes/" + str(user_id)).push(data)




def show_notes():

    user_id = auth.current_user['localId']
    my_notes = db.child("notes/" + str(user_id)).get()
    for note in my_notes.each():
        values = note.val()
        for value in values.values():
            print(value)


def main():
    ans = input("Are You a new user? y/n: ")
    if ans == 'y':
        try:
            sign_up()
            while True:
                function = input("Add note[1] or show Your notes[2]: ")
                if function == '1':
                    add_note()
                    print("Your note is added")
                elif function == '2':
                    try:
                        show_notes()
                    except TypeError:
                        print("You dont have notes")

                else:
                    print("Error")
                    exit()
        except:
            print("Log in first")
            main()

    elif ans == 'n':
        log_in()
        while True:
            function = input("Add note[1] or show Your notes[2]: ")
            if function == '1':
                add_note()
                print("Your note is added")
            elif function == '2':
                try:
                    show_notes()
                except TypeError:
                    print("You dont have notes")

            else:
                print("Error")
                exit()
    else:
        print("Please try again")
        main()
main()