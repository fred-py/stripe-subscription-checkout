import sqlite3


connection = sqlite3.connect(':memory:')

# .connect() returns a sqlite3.Connection Object
# Verify with type() 
print(type(connection))

# Connection object represents the connection
# between your program and the database file
# To store and retrieve data, you need a cursor object
cursor = connection.cursor()
print(type(cursor))

# Using SQLite datetime to get the current local time:
query = "SELECT datetime('now', 'localtime');"
print(cursor.execute(query))

# .fetchone() returns a tuple with the first row of the results
print(cursor.fetchone())

# Since .fetchone() returns a tuple, unpack the tuple elements
# to get the string containing the date and time information
time = cursor.execute(query).fetchone()[0]
print(time)

# Close the connection
#connection.close()

with sqlite3.connect(':memory:') as connection:
    cursor = connection.cursor()
    query = "SELECT datetime('now', 'localtime');"

    time = cursor.execute(query).fetchone()[0]

print(f'TIME WITHIN "WITH" STATEMENT {time}')

# Create a table
with sqlite3.connect(':memory:') as connection:
    cursor = connection.cursor()
    cursor.execute(
        """CREATE TABLE Customer(
            Name TEXT,
            Email TEXT,
            Address TEXT,
            TotalPaid INTEGER,
            Date TEXT,
            BinCollection TEXT
        );"""
    )
    cursor.execute(
        """INSERT INTO WheelieWash VALUES(
            'John Smith',
            '