## Created by André Costa for dphacks.com
## Documentation is available at https://github.com/camerahacks/video-production

## Interactive script to manage and backup DaVinci Resolve server postgresql database

import time
from subprocess import PIPE, Popen, check_output
import os
import psycopg2
from psycopg2 import sql
import datetime
import sys
import argparse

### VARIABLES ###
user = '<postgres>' # postgresql username
password = '<password>' # postgresql password
host = '<localhost>' # hostname or IP address
# database = '<DBNAME>'

parser = argparse.ArgumentParser(description='Easy to use Python script to manage DaVinci Resolve databases.')

args = parser.parse_args()

options = {"1":"Backup Single Database", "2":"Restore Single Database", "3":"List Databases"}

def show_options():
    print("Resolve Server Databse Manager")
    for c, desc in options.items():
        print(f"{c}. {desc}")

def dump_database(db):

    # Copy the environment variables so we are not modifying anything
    # Set the postgress user password
    my_env = os.environ.copy()
    my_env["PGPASSWORD"] = password

    commands = ["pg_dump", "-U", user, "-h", host, db]

    # Instead of calling Popen, lets save the string output as a string.
    dump_string = check_output(commands, env=my_env, universal_newlines=True)

    # Get the current date and time
    current_datetime = datetime.datetime.now()

    # Format the date and time as a string
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")

    filename = "resolve_bkp_"+db+"_"+formatted_datetime+".txt"

    # And now, save the string to a text file
    f = open(filename, "a")
    f.write(str(dump_string))
    f.close()

    return filename

def get_databases(host, user, password, dbname='postgres'):
    # Establish a connection to the PostgreSQL server
    connection_params = {
        'host': host,
        'user': user,
        'password': password,
        'dbname': dbname,
    }

    try:
        conn = psycopg2.connect(**connection_params)
        # print("Connected to the PostgreSQL server.")

        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Execute SQL query to list all databases
        query = sql.SQL("SELECT datname FROM pg_database;")
        cursor.execute(query)

        # Fetch all rows and print the database names
        databases = cursor.fetchall()
        # print("List of databases:")
        db_list = {}
        for idx, db in enumerate(databases):
            db_list[str(idx+1)] = db[0]

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return db_list

def backup_database():
    db_list_display = list_postgresql_databases(host, user, password)

    choice = input("Which Database? ")
    while choice not in db_list_display:
        list_postgresql_databases(host, user, password)
        choice = input(f"Which Database? ")

    print("Backing up "+db_list_display[choice]+"...")

    filename = dump_database(db_list_display[choice])

    print(f"Database backed up to {filename}")

def list_postgresql_databases(host, user, password, dbname='postgres'):
    db_list_display = get_databases(host, user, password, dbname)

    print('Databases:')
    for c, name in db_list_display.items():
        print(f"{c}. {name}")

    return db_list_display
    

# Show the option selection menu
show_options()

choice = input("Select Option: ")
while choice not in options:
    show_options()
    choice = input(f"Choose one of: {', '.join(options)}: ")


# Run choices
if choice == "1":
    backup_database()
elif choice == "3":
    list_postgresql_databases(host, user, password)

