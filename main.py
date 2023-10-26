import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def initialize_firestore():
    """
    Create database connection
    """

    # Initialize the app with the provided credentials
    cred = credentials.Certificate("todo-fd2f7-firebase-adminsdk-1ppbf-36c67abdee.json")
    firebase_admin.initialize_app(cred)

    # Get reference to database
    db = firestore.client()
    return db



def view_list(db):
    # Query the collection for the list
    results = db.collection("items").get()

    # Display the results
    print("\nTo-Do List:")
    for result in results:
        print(f"[ ] {result.id}") 

def add_item(db):
    # Get the to-do item name
    name = input("Enter item name\n> ")
    done = False

    # Check if that item already exists
    check = db.collection("items").document(name).get()
    while check.exists:
        print("Item already exists.")
        print("Enter new item name")
        name = input("> ")
        check = db.collection("items").document(name).get()
    
    # Save the item
    data = {"done" : done}
    db.collection("items").document(name).set(data)

    # Save this in the log collection in Firestore       
    log_transaction(db, f"Added {name} to to-do list")

def edit_item(db):
    # List to-do items and tell the user to choose one
    view_list(db)
    print("Select item to edit from the list")
    name = input("> ")

    # Check that the item exists
    check = db.collection("items").document(name).get()
    while not check.exists:
        print("Invalid item name")
        print("Enter item name")
        name = input("> ")
        check = db.collection("items").document(name).get()

    # Get new item name
    new_name = input("Enter new name for item\n> ")

    # Check if the new name is already taken
    new_check = db.collection("items").document(new_name).get()
    while new_check.exists:
        print("Item name already exists")
        print("Enter new item name")
        new_name = input("> ")
        new_check = db.collection("items").document(new_name).get()


    # Create a new document for new name, and delete the old version
    data = check.to_dict()
    db.collection("items").document(new_name).set(data)
    db.collection("items").document(name).delete()

    # Save this in the log collection in Firestore
    log_transaction(db, f"Changed {name} to {new_name}")

def finish_item(db):
    # List to-do items and tell the user to choose one
    view_list(db)
    print("Select item from the list that's finished")
    name = input("> ")

    # Check that the item exists
    check = db.collection("items").document(name).get()
    while not check.exists:
        print("Invalid item name")
        print("Enter item name")
        name = input("> ")
        check = db.collection("items").document(name).get()

    # Update the dictionary to mark the item as done
    data = check.to_dict()
    data["done"] = True
    db.collection("items").document(name).set(data)

    # Save this in the log collection in Firestore       
    log_transaction(db, f"Marked {name} as done")



def log_transaction(db, message):
    # Save a message with current timestamp to the log collection in the Firestore database.
    data = {"message" : message, "timestamp" : firestore.SERVER_TIMESTAMP}
    db.collection("log").add(data)    



def notify_finished_alert(results, changes, read_time):
    for change in changes:
        db.collection("items").document(change.document.id).delete()
        log_transaction(db, f"Removed {change.document.id} from to-do list")    
    
def register_finished_item(db):
    # If there is a finished item, remove it
    db.collection("items").where("done","==",True).on_snapshot(notify_finished_alert)



db = initialize_firestore()
register_finished_item(db)
choice = None
while choice != "0":
    print()
    print("0) Exit")
    print("1) View To-Do list")
    print("2) Add item to To-Do list")
    print("3) Edit item in To-Do list")
    print("4) Mark item as done from To-Do list")
    choice = input(f"> ")
    print()
    if choice == "1":
        view_list(db)
    elif choice == "2":
        add_item(db)
    elif choice == "3":
        edit_item(db)
    elif choice == "4":
        finish_item(db)


