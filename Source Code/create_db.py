import sqlite3
def create_db():
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS employee (
            eid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            gender TEXT,
            contact TEXT,
            dob TEXT,
            doj TEXT,
            pass TEXT,
            utype TEXT,
            address TEXT,
            salary TEXT
        )"""
    )
    con.commit()

    cur.execute( 
        """CREATE TABLE IF NOT EXISTS supplier (
            invoice INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT,
            desc TEXT    
        )""" )
    con.commit()
    
    ############## category Table
    cur.execute( 
        """CREATE TABLE IF NOT EXISTS category (
            cid INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT   
        )""" )
    con.commit()

    ########### product table
    cur.execute(
        """CREATE TABLE IF NOT EXISTS product (
            pid INTEGER PRIMARY KEY AUTOINCREMENT,
            Supplier TEXT,
            Category Text,
            name Text,
            price Text,
            qty Text,
            status Text
         )""")
    con.commit()
create_db()