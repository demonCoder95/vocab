# This is the database handler module that handles the database 
# operations and abstracts the internals of the database
# from the main applications that needs to perform CRUD operations.
import sqlite3
import os

class SqliteHandler():
    # A static variable to store the database file path

    # Note: DO NOT USE RELATIVE PATHS, THEY BREAK THE FUNCTIONALITY
    sqlite_db_path = "db/vocab.db"
    
    # determine the dir path by excluding the file name
    sqlite_db_path_dir = "/".join(sqlite_db_path.split("/")[:-1])
    sqlite_db_name = sqlite_db_path.split("/")[-1]

    # A DB schema to store the k/v pairs
    # for now, it's just an index, a phrase and some description
    sqlite_db_schema = "(phrase TEXT, description TEXT)"
    
    # The table name in the database
    sqlite_db_table_name = "vocab"

    # A constructor to initialize the database for usage upon application 
    # running.
    def __init__(self):
        """
        This constructor needs to initialize the database handler by
        opening the file as stored in the static variable. It will also
        start a cursor on the database to allow for queries execution.
        """       
        # Check if the daatabase path exists
        if os.path.exists(SqliteHandler.sqlite_db_path_dir):
            print("[DEBUG] DB path '{}' exists.".format(
                SqliteHandler.sqlite_db_path_dir
            ))
        else:
            print("[DEBUG] DB path '{}' does not exist. Creating...".format(
                SqliteHandler.sqlite_db_path
            ))
            os.system("mkdir -p {}".format(SqliteHandler.sqlite_db_path_dir))
        
        try: 
            self.connection = sqlite3.connect(SqliteHandler.sqlite_db_path)
        except Exception as e:
            print("[DEBUG] Exception occured when connecting to the database.")
            print("[DEBUG] Dying because '{}'.".format(e))
            # If an exception occured, initialize the connection object anyway
            self.connection = None
            exit(1)

        self.cursor = self.connection.cursor()

        # check if the table already exists in the database
        get_table_query = "SELECT name FROM sqlite_master WHERE type='table'"
        self.cursor.execute(get_table_query)
        tables_tuple = self.cursor.fetchone()

        # If there are no tables in the db, tables_tuple will be None
        if tables_tuple is not None and SqliteHandler.sqlite_db_table_name in tables_tuple:
            print("[DEBUG] Table {} already exists in the database {}".format(
                SqliteHandler.sqlite_db_table_name,
                SqliteHandler.sqlite_db_name
            ))
        else:
            # generate the table query
            create_table_query = '''CREATE TABLE vocab ''' + SqliteHandler.sqlite_db_schema
            # Check if a table exists in the database to store the keywords
            self.cursor.execute(create_table_query)
            # Commit the changes
            self.connection.commit()

        print("[DEBUG] Database ready.")

    # A destructor to clean up database connections, if any are open
    def __del__(self):
        # close the connection
        if self.connection is not None:    
            self.connection.close()

    # A method to retrieve an entry from the database, all matching entries as well
    def get_from_db(self, keyword):
        """This method will return entries from the database as requested.
        Since it will perform pattern matching, it can fetch multiple entries.
        It accepts a keyword to search."""

        # TODO: Perform sanitization of the keyword here before stuffing
        # it in the query.
        get_query = "SELECT * from {} WHERE phrase LIKE '%{}%'".format(
            SqliteHandler.sqlite_db_table_name,
            keyword
        )
        self.cursor.execute(get_query)

        # return all the rows that were fetched
        return self.cursor.fetchall()

    # A method for updating an existing phrase in the database
    def update_in_db(self, phrase, desc):
        response = self.get_from_db(phrase)
        if response is not None:
            # If the phrase exists, add the description as an additional
            # paragraph to the phrase
            update_query = "UPDATE {} SET description='{}' WHERE phrase='{}'".format(
                SqliteHandler.sqlite_db_table_name,
                response[0][1] + "\n" + desc,
                phrase
            )
            try:
                self.cursor.execute(update_query)
                self.connection.commit()
            except Exception as e:
                print("[DEBUG] Failed to update the phrase in the database.")
                print("[DEBUG] Reason: {}".format(e))
                return False
        else:
            # If the phrase doesn't exist, simply add it
            self.put_in_db(phrase, desc)

        return True

    # A method to write a phrase and description to the database
    def put_in_db(self, phrase, desc):
        """This method will return success/failure status of a query that
        has successfully or unsuccessfully been executed on the database
        for storing data.
        return: True if successful, False otherwise.
        """

        # TODO: Perform sanitization of the data before stuffing it in the
        # query here

        # generate the query for inserting the data into the database table
        put_query = "INSERT INTO {} VALUES ('{}','{}')".format(
            SqliteHandler.sqlite_db_table_name,
            phrase,
            desc
        )
        try:
            # execute the query to add the data in the database table
            self.cursor.execute(put_query)

            # commit changes to the database on disk
            self.connection.commit()
        except Exception as e:
            print("[DEBUG] Error occured writing to the database.")
            print("[DEBUG] Reason: {}".format(e))
            # Return a False, for successful operation
            return False

        return True