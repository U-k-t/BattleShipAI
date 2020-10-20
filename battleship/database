import sqlite3

class database:

    db = 'database_file'
    connection = sqlite3.connect(db)
    c = connection.cursor()
  
    def add(coord, ship):
        c.execute("INSERT INTO db (ship) VALUES (coord)")
        c.commit()
  

    def get(coord):
        return c.execute("SELECT * FROM db WHERE symbol = '%s' % coord")