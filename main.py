# This is the main module of the project, which implements the interfacing
# application

import common.db_handler as db_handler
from os import system

welcome_message = """
Welcome to the vocabulary database!
"""

operations_message = """
The application supports the following operations:
1. Search for terms in the database based on a keyword provided.
2. Store a keyword along with a description.
3. Update a keyword with additional description.

To quit, type 'q' or 'Q'.
"""
def clear_screen():
    system("clear")

# A method to print entries of a list of tuples, provided from the database
def print_entries(input_data):

    # Assuming for now, the tuple is arranged as follows:
    # 0 ===> phrase
    # 1 ===> description

    output = "~=~"*20 + "\n"
    for each_tuple in input_data:
        output += each_tuple[0] + ": \t" + each_tuple[1] + "\n"
    output += "~=~"*20 + "\n"

    print(output)

def handle_search(data_handler):
    # Clear the screen for the operation
    clear_screen()
    # operation loop
    while True:
        user_input = input("Enter a keyword to search in the database or 'e' to exit:\n>").strip()
        # Break the operation loop upon 'e'
        if user_input.lower() == 'e':
            break
        
        result = data_handler.get_from_db(user_input)
        # Check if any matches were found
        if result is None or len(result) == 0:
            print("No matches to keyword '{}'. Try again!".format(
                user_input
            ))
            continue
        # Else, print all the matches
        else:
            print("Keyword '{}' hit '{}' matches! Showing all of them:".format(
                user_input, len(result)
            ))
            print_entries(result)


def handle_store(data_handler, operation):
    # Clear the screen for the operation
    clear_screen()

    # Generate an appropriate prompt message
    prompt_msg = "Enter a phrase to {} in the database or 'e' to exit:\n>".format(
        operation
    )
    # operation loop
    while True:
        user_input = input(prompt_msg).strip()
        # Break the opeation loop upon 'e'
        if user_input.lower() == 'e':
            break

        keyword = user_input
        user_input = input("Enter a description for the keyword:\n>")
        desc = user_input
        if operation == "store":
            successful = data_handler.put_in_db(keyword, desc)
        elif operation == "update":
            successful = data_handler.update_in_db(keyword, desc)

        if successful:
            print("[DEBUG] Operation successful in the database!")
        else:
            print("[DEBUG] Operation failed in the database!")
        

def main_application():
    # Initialize the database handler
    data_handler = db_handler.SqliteHandler()

    # Main application loop:
    while True:
        print(welcome_message)
        print(operations_message)
        user_input = input("What would you like to do?\n>").strip()
        
        # Handle the quit case
        if user_input.lower() == 'q':
            break

        elif int(user_input) == 1:
            handle_search(data_handler)
        elif int(user_input) == 2:
            handle_store(data_handler, "store")
        elif int(user_input) == 3:
            handle_store(data_handler, "update")
            
        


# When exporting this as a module, uncomment this part
# if __name__ == '__main__':
#     main_application()

main_application()