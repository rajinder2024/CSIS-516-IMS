from tkinter import *
from PIL import Image, ImageTk
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from sales_report import SalesReportClass
from stock_report import StockReportClass
import sqlite3
from tkinter import ttk
from tkinter import messagebox
import subprocess
import os ,sys
from datetime import datetime
import time


class IMS:
    def __init__(self, root):  
        self.root = root
        self.after_id = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        
        self.current_user_id = None 
        # Custom colors
        self.dark_color = "#010c48"
        self.secondary_color = "#009698"
        
        #======title========
        self.icon_title = PhotoImage(file="C:/Users/Rajinder/CSIS_Project/IMS/images/logo1.png")

        title = Label(
            self.root,
            text="Inventory Management System", image=self.icon_title, compound=RIGHT,
            font=("times new roman", 40, "bold"),
            bg=self.dark_color,
            fg="white", anchor="w", padx=20,
        )
        title.place(x=0, y=0, relwidth=1, height=70)

        #===========button_logout=========
        btn_logout = Button(
            self.root,
            text="Logout", command=self.logout, 
            font=("times new roman", 15, "bold"),
            bg="red", cursor="hand2"
        ).place(x=1150, y=10, height=50, width=150)
        
        #========Label_clock=============
        self.lbl_clock = Label(
            self.root,
            text="Welcome to Inventory Management System\t\t Date: MM:HH:YYYY\t\t Time: HH:MM:SS", 
            font=("times new roman", 15), bg=self.dark_color,
            fg="white"
        )
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        #======Left_Menu=================
        self.MenuLogo = Image.open("C:/Users/Rajinder/CSIS_Project/IMS/images/menu_im.png")
        self.MenuLogo = self.MenuLogo.resize((200, 200), Image.Resampling.LANCZOS)
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo) 

        LeftMenu = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        LeftMenu.place(x=0, y=102, width=200, height=565)

        #====Add logo to Left Menu========
        lbl_menulogo = Label(LeftMenu, image=self.MenuLogo)
        lbl_menulogo.pack(side=TOP, fill=X)
        
        #======Add Button to left menu================
        self.icon_side = PhotoImage(file="C:/Users/Rajinder/CSIS_Project/IMS/images/side.png")
        lbl_menu = Label(LeftMenu, text="Menu", font=("times new roman", 20), bg=self.secondary_color)
        lbl_menu.pack(side=TOP, fill=X)

        btn_employee = Button(
            LeftMenu, text="Employee", command=self.employee,
            image=self.icon_side, compound=LEFT, padx=5, anchor="w",
            font=("times new roman", 20), bg="white", bd=3, cursor="hand2"
        ).pack(side=TOP, fill=X)
        
        btn_supplier = Button(
            LeftMenu, text="Supplier", command=self.supplier,
            image=self.icon_side, compound=LEFT, padx=5, anchor="w",
            font=("times new roman", 20), bg="white", bd=3, cursor="hand2"
        ).pack(side=TOP, fill=X)
        
        btn_category = Button(
            LeftMenu, text="Category", command=self.category,
            image=self.icon_side, compound=LEFT, padx=5, anchor="w",
            font=("times new roman", 20), bg="white", bd=3, cursor="hand2"
        ).pack(side=TOP, fill=X)
        
        btn_product = Button(
            LeftMenu, text="Product", command=self.product,
            image=self.icon_side, compound=LEFT, padx=5, anchor="w",
            font=("times new roman", 20), bg="white", bd=3, cursor="hand2"
        ).pack(side=TOP, fill=X)
        
        btn_sales = Button(
            LeftMenu, text="Sales", command=self.sales,
            image=self.icon_side, compound=LEFT, padx=5, anchor="w",
            font=("times new roman", 20), bg="white", bd=3, cursor="hand2"
        ).pack(side=TOP, fill=X)
        
        btn_exit = Button(
            LeftMenu, text="Exit", image=self.icon_side, compound=LEFT, padx=5, anchor="w",
            font=("times new roman", 20), bg="white", bd=3, cursor="hand2"
        ).pack(side=TOP, fill=X)
       
         #======Right Menu=================
        # Load the top right logo for the right menu
        self.ReportLogo = Image.open("C:/Users/Rajinder/CSIS_Project/IMS/images/report.png")
        self.ReportLogo = self.ReportLogo.resize((200, 200), Image.Resampling.LANCZOS)
        self.ReportLogo = ImageTk.PhotoImage(self.ReportLogo)

        # Load and resize the icons
        self.icon_sales = Image.open("C:/Users/Rajinder/CSIS_Project/IMS/images/sales_icon.png")
        self.icon_sales = self.icon_sales.resize((25, 25), Image.Resampling.LANCZOS)
        self.icon_sales = ImageTk.PhotoImage(self.icon_sales)

        self.icon_stock = Image.open("C:/Users/Rajinder/CSIS_Project/IMS/images/stock_icon.png")
        self.icon_stock = self.icon_stock.resize((25, 25), Image.Resampling.LANCZOS)
        self.icon_stock = ImageTk.PhotoImage(self.icon_stock)

        RightMenu = Frame(self.root, bd=3, relief=GROOVE, bg="white",highlightthickness=1)
        RightMenu.place(x=1150, y=102, width=200, height=565)

        # Add logo to Right Menu
        lbl_rightlogo = Label(RightMenu, image=self.ReportLogo, bg="white")
        lbl_rightlogo.pack(side=TOP, fill=X)

        # Right Menu Title
        lbl_rightmenu = Label(
            RightMenu, text="Reports", font=("times new roman", 20),
            bg=self.secondary_color, fg="black", pady=7
        )
        lbl_rightmenu.pack(side=TOP, fill=X)

        # Sales Report Button
        btn_report = Button(
            RightMenu, text="Sales Report", command=self.sales_report,
            image=self.icon_sales, compound=LEFT, anchor="w",
            font=("times new roman", 20), bg="white", bd=3, cursor="hand2", padx=10
        )
        btn_report.pack(side=TOP, fill=X, pady=5)

        # Stock Report Button
        btn_stock_report = Button(
            RightMenu, text="Stock Report", command=self.stock_report,
            image=self.icon_stock, compound=LEFT, anchor="w",
            font=("times new roman", 20), bg="white", bd=3, cursor="hand2", padx=10
        )
        btn_stock_report.pack(side=TOP, fill=X, pady=5)

        #======Content Area==============
        content_frame = Frame(self.root, bg="white")
        content_frame.place(x=215, y=120, width=900, height=565)

        # Card Size
        card_width = 270
        card_height = 160

        # Employee Card
        self.lbl_employee = Label(
            content_frame, text="Total Employees\n[0]", bd=2, relief=GROOVE,
            bg="#33bbf9", fg="white", font=("goudy old style", 16, "bold"),
            padx=10, pady=10
        )
        self.lbl_employee.place(x=0, y=0, width=card_width, height=card_height)

        # Supplier Card
        self.lbl_supplier = Label(
            content_frame, text="Total Suppliers\n[0]", bd=2, relief=GROOVE,
            bg="#ff5722", fg="white", font=("goudy old style", 16, "bold"),
            padx=10, pady=10
        )
        self.lbl_supplier.place(x=320, y=0, width=card_width, height=card_height)

        # Category Card
        self.lbl_category = Label(
            content_frame, text="Total Categories\n[0]", bd=2, relief=GROOVE,
            bg="#009688", fg="white", font=("goudy old style", 16, "bold"),
            padx=10, pady=10
        )
        self.lbl_category.place(x=640, y=0, width=card_width, height=card_height)

        # Product Card
        self.lbl_product = Label(
            content_frame, text="Total Products\n[0]", bd=2, relief=GROOVE,
            bg="#607d8b", fg="white", font=("goudy old style", 16, "bold"),
            padx=10, pady=10
        )
        self.lbl_product.place(x=0, y=170, width=card_width, height=card_height)

        # Sales Card
        self.lbl_sales = Label(
            content_frame, text="Total Sales\n[0]", bd=2, relief=GROOVE,
            bg="#3f51b5", fg="white", font=("goudy old style", 16, "bold"),
            padx=10, pady=10
        )
        self.lbl_sales.place(x=320, y=170, width=card_width, height=card_height)

        # Recent Activity Frame (bottom section)
        self.activity_frame = Frame(content_frame, bg="white", bd=2, relief=GROOVE)
        self.activity_frame.place(x=0, y=340, width=900, height=180)
        
        Label(
            self.activity_frame,
            text="SYSTEM INFORMATION",
            font=("Helvetica", 14, "bold"),
            bg="white",
            fg=self.dark_color
        ).pack(pady=5)
        
        self.activity_text = Text(
            self.activity_frame,
            font=("Helvetica", 12),
            bg="white",
            fg="#333",
            wrap=WORD,
            padx=10,
            pady=5,
            bd=0
        )
        self.activity_text.pack(fill=BOTH, expand=True, padx=7, pady=(0, 5))
        self.activity_text.insert(END, "System running normally")
        self.activity_text.config(state=DISABLED)

        #=======Footer=================
        footer = Label(
            self.root, 
            text="Inventory Management System | Developed by Rajinder | © 2025",
            font=("times new roman", 15), 
            bg="#4d636d", 
            fg="white"
        ).pack(side=BOTTOM, fill=X)
        
        self.update_content()

    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)
    
    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

    def sales_report(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = SalesReportClass(self.new_win)
        
    def stock_report(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = StockReportClass(self.new_win)

    def update_content(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try: 
            cur.execute("select * from product")
            product = cur.fetchall()
            self.lbl_product.config(text=f'Total Products\n[ {str(len(product))} ]')

            cur.execute("select * from supplier")
            supplier = cur.fetchall()
            self.lbl_supplier.config(text=f'Total Suppliers\n[ {str(len(supplier))} ]')

            cur.execute("select * from category")
            category = cur.fetchall()
            self.lbl_category.config(text=f'Total Categories\n[ {str(len(category))} ]')

            cur.execute("select * from employee")
            employee = cur.fetchall()
            self.lbl_employee.config(text=f'Total Employees\n[ {str(len(employee))} ]')

            bill = len(os.listdir('bill'))
            self.lbl_sales.config(text=f'Total Sales\n [{str(bill)}]')

            # Get total sales count from sales table
            cur.execute("SELECT COUNT(*) FROM sales")
            sales_count = cur.fetchone()[0]
            self.lbl_sales.config(text=f'Total Sales\n [{str(sales_count)}]')

            # Update date and time
            time_ = time.strftime("%H:%M:%S")
            date_ = time.strftime("%m-%d-%Y")
            self.lbl_clock.config(
                text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}"
            )
            self.after_id = self.root.after(200, self.update_content)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

    def on_close(self):
        """Handle window close properly"""
        if hasattr(self, 'after_id') and self.after_id:
            try:
                self.root.after_cancel(self.after_id)
                self.after_id = None
            except Exception as e:
                print(f"Warning: Couldn't cancel after job - {e}")


    def logout(self):
        """100% reliable logout method that handles all path cases"""
        # 1. Clean up Tkinter
        if hasattr(self, 'after_id') and self.after_id:
            try:
                self.root.after_cancel(self.after_id)
                self.after_id = None
            except Exception as e:
                print(f"Warning: Couldn't cancel after job - {e}")

        self.root.destroy()
        # 2. Calculate CORRECT paths
        import sys
        import os
        import subprocess
        
        # Get the absolute path to the Source Code directory
        current_dir = os.path.dirname(os.path.abspath(__file__))  # Where dashboard.py is
        login_script = os.path.join(current_dir, "login.py")
        
        # 3. DEBUG: Print all path information
        print("\n=== PATH DEBUGGING ===")
        print(f"Python executable: {sys.executable}")
        print(f"Current directory: {current_dir}")
        print(f"Login script path: {login_script}")
        print(f"Path exists: {os.path.exists(login_script)}")
        if os.path.exists(current_dir):
            print(f"Directory contents: {os.listdir(current_dir)}")
        print("====================\n")
        
        # 4. Restart process
        try:
            subprocess.Popen(
                [sys.executable, login_script],
                cwd=current_dir,  # Set working directory
                
            )
        except Exception as e:
            import traceback
            traceback.print_exc()
        finally:
            os._exit(0)

    def set_current_user(self, user_id):
        self.current_user_id = user_id
    
        
if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()