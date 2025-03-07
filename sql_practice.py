import sqlite3

connection = sqlite3.connect("data.db")

# Query for all the data
cursor =connection.cursor()
a=cursor.execute("SELECT * FROM Events WHERE city= 'Vijayawada'")
result = a.fetchall()
print(result)

# Query for certain data
cursor =connection.cursor()
a=cursor.execute("SELECT band FROM Events WHERE city= 'Vijayawada'")
result = a.fetchall()
print(result)

# Insert New rows
new_rows = [('Cat', 'Cat city', '17-01-2007'),
            ('Dog', 'Dog city', '09-01-2012')]
cursor.executemany("INSERT INTO Events VALUES(?,?,?)",new_rows)
connection.commit()

cursor =connection.cursor()
a=cursor.execute("SELECT * FROM Events ")
result = a.fetchall()
print(result)

