# Python Basics Book - Database Chapter


import sqlite3
from sqlalchemy import create_engine

# If file doesn't exist in dir, one will be created automatically
# Othereise, db will be connected to the file name below
connection = sqlite3.connect(':memory:')

# Create a cursor object to execute SQL commands
# and fetch results
#cur = con.cursor()

#cur.execute('CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT, mobile TEXT, address TEXT, bin_collection TEXT, total_paid TEXT, description TEXT)')


"""The sqlite3.connect() function is used to connect to, 
or create, a database. When you execute .connect("test_database.db"), 
Python searches for an existing database called "test_database.db". 
If no database with that name is found, a new one is 
created in the current working directory. 
To create a database in a different directory, 
you must specify the full path in the argument to .connect()."""
connection = sqlite3.connect('test_database.db')

# Create a one-time-use db just to playaround

#connection = sqlite3.connect(':memory:')
print(type(connection))

# Create a cursor object to store and retrieve data
cursor = connection.cursor()
print(type(cursor))

# SQLite datetime to get the current local time:
query = "SELECT datetime('now', 'localtime');"
cursor.execute(query)
print(cursor.fetchone()) # Get the date/time from the cursor object

"""Since .fetchone() returns a tuple, 
you need to unpack the tuple elements to get the 
string containing the date and time information. 
Here’s how you can do this by chaining the 
.execute() and .fetchone() methods:"""
time = cursor.execute(query).fetchone()[0]

print(time)
connection.close()

with sqlite3.connect("test_database.db") as connection:
    cursor = connection.cursor()
    query = "SELECT datetime('now', 'localtime');"
    time = cursor.execute(query).fetchone()[0]

print(f'NEW TIME{time}')

with sqlite3.connect("test_database.db") as connection:
    cursor = connection.cursor()
    cursor.execute(
        """CREATE TABLE WheelieWash(
            Name TEXT,
            Email TEXT,
            Address TEXT,
            Subscription TEXT,
            TotalPaid INTEGER,
            Date TEXT,
            BinCollection TEXT
        );"""
    )
    cursor.execute(
        """INSERT INTO WheelieWash VALUES(
            'John Smith',
            'rezende.f@outlook.com',
            '40 Seattle Court, Basingstoke, RG21 3AZ',
            'Gold Subscription',
            '36',
            '2021-09-01',
            'Monday'
        );"""
    )