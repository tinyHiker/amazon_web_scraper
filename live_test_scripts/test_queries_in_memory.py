"""This python script test my SQL queries using an in-memory/RAM database"""

import sqlite3

# Connect to a database (or create if it doesn't exist)
conn = sqlite3.connect(':memory:')  # This will create a file named 'my_database.db'

# Create a cursor object
cursor = conn.cursor()

# Create the 'Users' table
cursor.execute('''
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        master INTEGER REFERENCES users(id) CHECK (master != id)
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        bought INTEGER NOT NULL DEFAULT 0 CHECK (bought IN (0, 1)),
        user_id INTEGER,
        rating INTEGER CHECK (rating >= 1 AND rating <= 10),
        FOREIGN KEY (user_id) REFERENCES Users(id)
    )
    ''')

user_name = "Taha"  # Example user name
cursor.execute("INSERT INTO users (name) VALUES (?)", (user_name,))

# Get the last inserted user's ID
user_id = cursor.lastrowid

# Insert products related to the user into the 'products' table
products = [
    ("Widget", 19.99, 0, 8),
    ("Gadget", 29.99, 1, 9)
]

for product in products:
    cursor.execute("INSERT INTO products (name, price, bought, user_id, rating) VALUES (?, ?, ?, ?, ?)",
                   (product[0], product[1], product[2], user_id, product[3]))

# Select all records from the 'users' table
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()  # Fetch all rows of the query result

print("Users:")
for user in users:
    print(user)  # Each 'user' is a tuple representing a row from the 'users' table

# Select all records from the 'products' table
cursor.execute("SELECT * FROM products")
products = cursor.fetchall()  # Fetch all rows of the query result

print("\nProducts:")
for product in products:
    print(product)  # Each 'product' is a tuple representing a row from the 'products' table

# Commit the changes
conn.commit()

# Close the connection
conn.close()