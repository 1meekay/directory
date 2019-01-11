import sqlite3

conn = sqlite3.connect('contactDirectory.db')
cursor = conn.cursor()

class Contacts:
    def __init__(self, name, number):
        self.name = name
        self.number = number