import psycopg2
import socket

# Variables for the new data being added: Consider using an API 'get' call to obtain this information
userId = 3
userName = 'Jensen'

# Create connection to the database
conn = psycopg2.connect(
            host = "localhost",
            database = "my_database",
            user = "postgres",
            password = "jencena317",
            port = "5432"
            )

# Creating a cursor object
curr = conn.cursor()

# Inserting data to the test_table
curr.execute("INSERT INTO test_table (id,name) VALUES (%s,%s)",(userId,userName))
conn.commit()

# Query for test_table
curr.execute("SELECT id, name FROM test_table")

rows = curr.fetchall()
print(rows)
for r in rows:
    print(f"id: {r[0]} name: {r[1]}")

# Close the Cursor and Connection objects
curr.close()
conn.close()
