import sqlite3


connection = sqlite3.connect(':memory:')
cursor = connection.cursor()

data = (
    (
        'cus_343141',
        'John Smith',
        '04050404',
        'rezende.f@outlook.com'
    ),
    (
        'cus_3431422',
        'Jane Kobrinsky',
        '04343304',
        'janew@hotmail.com'
    ),
    (
        'cus_343143',
        'Jack Jones',
        '434343404',
        'jack@gmail.com'
    )
)

with sqlite3.connect(':memory:') as connection:
    cursor = connection.cursor()
    query = "SELECT datetime('now', 'localtime');"

    time = cursor.execute(query).fetchone()[0]

    cursor.executescript(
        """DROP TABLE IF EXISTS Customer;
            CREATE TABLE Customer(
                Id TEXT,
                Name TEXT,
                Phone TEXT,
                Email TEXT
            );"""
    )

    #cursor.executemany("INSERT INTO Customer VALUES(?, ?, ?, ?)", data) # ? must match the number of objects in the tuple

#cursor.execute(
##    """CREATE TABLE Address(
 #       City TEXT,
 ##       Street TEXT,
  #      PostCode TEXT,
  #      State TEXT
  #  );"""
#)

#cursor.execute(
#    """CREATE TABLE Subscription(
#        Plan TEXT,
#        BinCollection TEXT,
#        BinsSelected TEXT,
#        TotalPaid INTEGER
#    );"""
#)

    

#cursor.execute(
#    """INSERT INTO Address VALUES(
#        'Basingstoke',
#        '40 Seattle Court',
#       'RG21 3AZ',
#        'Hampshire'
#    );"""
#)

#cursor.execute(
#    """INSERT INTO Subscription VALUES(
#        'Gold',
#        'Monday',
#       'G',
#       36
#   );"""
#)

#connection.commit()
#connection.close() # Close the connection - however to access db this needs to be commented out

#cursor.execute("DROP TABLE Customer")
#connection.close()
# retrieves objects
print(cursor.execute("SELECT * FROM Customer"))
# retrieves a tuple with the first row of the results
print(cursor.fetchall())

