from sputnik_ide.settings import DATABASES
import sqlite3
import os

if __name__ == '__main__':
    db_path = DATABASES['default']['NAME']
    if not os.path.isfile(db_path):
        sqlite3.connect(db_path)
        print('Database {} created!'.format(db_path))
