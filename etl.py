import sys
import csv
import sqlite3


file = sys.argv[1]
fieldnames = ("Job Title", "Category", "Status", "Location")
connection = sqlite3.connect('jobs.db')
cursor = connection.cursor()
cursor.execute("CREATE TABLE jobs (%s text, %s text, %s text, %s text)" %
               fieldnames)
with open(file, newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader, None)
    for row in reader:
        cursor.execute("INSERT INTO jobs VALUES (?, ?, ?, ?)", row)
connection.commit()
connection.close()
