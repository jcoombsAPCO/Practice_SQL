import sqlite3

# Connection to an arbitrary database
database = "my.db"
# try:
#     with sqlite3.connect(database) as conn:
#         print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")
# except sqlite3.OperationalError as e:
#     print("Failed to open database:",e)

# Creating CREATE TABLE statement
create_table = [
    """ CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY,
            name text NOT NULL,
            begin_date DATE,
            end_date DATE
    );""",
    """ CREATE TABLE IF NOT EXISTS tasks(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            priority INT,
            project_id INT NOT NULL,
            status_id INT NOT NULL,
            begin_date DATE NOT NULL,
            end_date DATE NOT NULL,
            FOREIGN KEY (project_id) REFERENCES projects (id)
    );"""
]

# Creating a Database Connection and creating a table
try:
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()      # Creating a cursor to access database
        for statement in create_table:
            cursor.execute(statement)   # Executes CREATE TABLE SQL statements to create table(s)
        conn.commit()               # Confirms and implements changes via the cursor
        print('Tables Created Successfully')
except sqlite3.OperationalError as e:
    print("Failed to create tables:", e)    # If operational error is output by sqlite3, the program outputs statement


