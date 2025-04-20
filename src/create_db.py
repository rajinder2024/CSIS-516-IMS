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

    ############ TABLES FOR SALES REPORTING
    # Sales header table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        invoice INTEGER PRIMARY KEY,
        date TEXT,
        time TEXT,
        customer_name TEXT,
        customer_contact TEXT,
        subtotal REAL,
        discount REAL,
        tax REAL,
        total REAL,
        payment_method TEXT,
        employee_id INTEGER,
        FOREIGN KEY(employee_id) REFERENCES employee(eid)
    )""")
    con.commit()

    # Sales items table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS sales_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice INTEGER,
        product_id INTEGER,
        product_name TEXT,
        category TEXT,
        quantity INTEGER,
        price REAL,
        total REAL,
        FOREIGN KEY(invoice) REFERENCES sales(invoice),
        FOREIGN KEY(product_id) REFERENCES product(pid)
    )""")
    con.commit()

    # Daily summary table (for faster reporting)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS daily_sales_summary (
        date TEXT PRIMARY KEY,
        total_sales REAL,
        total_discount REAL,
        total_items_sold INTEGER,
        num_transactions INTEGER
    )""")
    con.commit()

    # Monthly summary table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS monthly_sales_summary (
        year_month TEXT PRIMARY KEY,  -- Format: YYYY-MM
        total_sales REAL,
        total_discount REAL,
        total_items_sold INTEGER,
        num_transactions INTEGER
    )""")
    con.commit()

    # Activity log table 
    cur.execute('''
    CREATE TABLE IF NOT EXISTS activity_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        user_id INTEGER,
        module TEXT,
        details TEXT,
        FOREIGN KEY(user_id) REFERENCES employee(eid)
    )''')
    con.commit()
create_db()