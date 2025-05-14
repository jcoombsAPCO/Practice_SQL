
import sqlite3
from contextlib import closing


# Creating a connection to the aquarium database and verifying connection
connection = sqlite3.connect("aquarium.db")
print(connection.total_changes)
print("entering if statement")
# Creating a table of fish in the aquarium
cursor = connection.cursor()            # Cursor created from previously defined connection
cursor.execute("CREATE TABLE fish (name TEXT, species TEXT, tank_number INTEGER)")
table_exists = True

# Inserting tables of data into 'fish' table
cursor.execute("INSERT INTO fish VALUES ('Sammy','shark',1)")
cursor.execute("INSERT INTO fish VALUES ('Jamie','cuttlefish',7)")

# Printing all rows of data in the 'fish' table
rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
print(rows)
print(connection.total_changes)

# Printing a specified row of data from 'fish' where the fish is a shark
des_species = 'shark'
rows = cursor.execute("SELECT name, species, tank_number FROM fish WHERE species = ?",(des_species,),).fetchall()
print(rows)
print(connection.total_changes)

# Updating a value already present in the 'fish' table
new_tank_number = 2
cursor.execute("UPDATE fish SET tank_number = ? WHERE tank_number = 1",(new_tank_number,)).fetchall()
rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
print(rows)
print(connection.total_changes)

# Deleting a row of data from the table
released_fish = "Sammy"
cursor.execute("DELETE FROM fish WHERE name = ?",(released_fish,)).fetchall()
rows = cursor.execute("SELECT name, species, tank_number FROM fish").fetchall()
print(rows)
print(connection.total_changes)

# Closing connection and cursor objects
with closing(sqlite3.connect("aquarium.db")) as connection:
    with closing(connection.cursor()) as cursor:
        rows = cursor.execute("SELECT 1").fetchall()
        print(rows)

