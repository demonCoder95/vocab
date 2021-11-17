# This is the main module of the project, which implements the interfacing
# application

import db_handler

def main_application():
    data_handler = db_handler.SqliteHandler()

# When exporting this as a module, uncomment this part
# if __name__ == '__main__':
#     main_application()

main_application()