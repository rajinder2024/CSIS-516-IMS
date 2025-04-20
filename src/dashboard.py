import os
import shutil
from tkinter import ttk, messagebox
from tkinter import *
from PIL import Image,ImageTk
import sqlite3
import time, datetime
from employee import employeeClass
from supplier import supplierClass
from category import categoryClass
from product import productClass
from sales import salesClass
from sales_forecast import SalesForecastClass 
import subprocess

# ===== Clear __pycache__ =====
'''def clear_pycache():
    pycache_path = os.path.join(os.path.dirname(__file__), '__pycache__')
    if os.path.exists(pycache_path):
        shutil.rmtree(pycache_path)
        print("[INFO] __pycache__ cleared.")
    else:
        print("[INFO] No __pycache__ found.")

clear_pycache()
'''
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # IMS/
IMG_DIR = os.path.join(BASE_DIR, "images")
class IMS:
    def __init__(self, root):  
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System")  # Set a window title
        self.root.config(bg="white")
        BASE_IMAGE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
        img_path = os.path.join(IMG_DIR, "logo1.png")
        print("Image path:", img_path)  # Debug path

        self.icon_title = PhotoImage(file=img_path)

       

        #======title========
        #img_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images', 'logo1.png')
        

        #PhotoImage(file=os.path.join(BASE_IMAGE_PATH, 'logo1.png'))


        title = Label(
            self.root,
            text="Inventory Management System", image=self.icon_title, compound= RIGHT,
            font=("times new roman", 40, "bold"),
            bg="#010c48",
            fg="white",anchor="w",padx=20,
        )
        title.place(x=0, y=0, relwidth=1, height=70)

        #===========button_logout=========
        btn_logout= Button(self.root,text="Logout",command=self.logout,font=("times new roman",15,"bold"),
                           bg="red", cursor="hand2").place(x=1150,y=10,height=50, width =150)
        #========Label_clock=============
        self.lbl_clock = Label(
            self.root,
            text="Welcome to Inventory Management System\t\t Date: MM:HH:YYYY\t\t Time: HH:MM:SS", 
            font=("times new roman", 15), bg="#010c48",
            fg="white",)
        self.lbl_clock.place(x=0, y=70, relwidth=1, height=30)

        #======Left_Menu=================

        menu_path = os.path.join(IMG_DIR, "menu_im.png")
        self.MenuLogo = Image.open(menu_path)
        self.MenuLogo = self.MenuLogo.resize((200,200),Image.Resampling.LANCZOS) # resize image 
        self.MenuLogo = ImageTk.PhotoImage(self.MenuLogo) 
        #=====Create Left Menu Frame=====

        LeftMenu= Frame(self.root,bd=2,relief=RIDGE,bg="white")
        LeftMenu.place(x=0,y=102,width=200,height=565)

        #====Add logo to Left Menu========
        lbl_menulogo = Label(LeftMenu, image=self.MenuLogo)
        lbl_menulogo.pack(side=TOP, fill=X)
        
        #======Add Button to left menu================
        side_path = os.path.join(IMG_DIR, "side.png")
        self.icon_side = PhotoImage(file=side_path)
        
        lbl_menu = Label(LeftMenu,text="Menu",font=("times new roman",20),bg="#009698").pack(side=TOP, fill=X)

        btn_employee = Button(LeftMenu,text="Employee",command=self.employee,image=self.icon_side,compound=LEFT,padx=5,anchor="w",
                          font=("times new roman",20),bg="white",bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_supplier = Button(LeftMenu, text="Supplier", command=self.supplier,image=self.icon_side, compound=LEFT, padx=5, anchor="w",
                              font=("times new roman", 20), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_category = Button(LeftMenu, text="Category",command=self.category,image=self.icon_side, compound=LEFT, padx=5, anchor="w",
                              font=("times new roman", 20), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_product = Button(LeftMenu, text="Product",command=self.product, image=self.icon_side, compound=LEFT, padx=5, anchor="w",
                             font=("times new roman", 20), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_sales = Button(LeftMenu, text="Sales",command=self.sales,image=self.icon_side, compound=LEFT, padx=5, anchor="w",
                           font=("times new roman", 20), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        btn_exit = Button(LeftMenu, text="Exit",command=exit, image=self.icon_side, compound=LEFT, padx=5, anchor="w",
                          font=("times new roman", 20), bg="white", bd=3, cursor="hand2").pack(side=TOP, fill=X)
        
        #========ContentLabel==============

        self.lbl_employee =Label(self.root,text="Total Employee\n[0]",bd=5, relief= RIDGE,bg="#33bbf9",fg="white", 
                                 font=("goudy old style",20,"bold"))
        self.lbl_employee.place(x=300,y=120,height=150,width=300)

         # Supplier Label
        self.lbl_supplier = Label(self.root, text="Total Supplier\n[0]", bd=5, relief=RIDGE, bg="#ff5722", fg="white",
                                  font=("goudy old style", 20, "bold"))
        self.lbl_supplier.place(x=650, y=120, height=150, width=300)

        # Category Label
        self.lbl_category = Label(self.root, text="Total Category\n[0]", bd=5, relief=RIDGE, bg="#009688", fg="white",
                                  font=("goudy old style", 20, "bold"))
        self.lbl_category.place(x=1000, y=120, height=150, width=300)

        # Product Label
        self.lbl_product = Label(self.root, text="Total Product\n[0]", bd=5, relief=RIDGE, bg="#607d8b", fg="white",
                                 font=("goudy old style", 20, "bold"))
        self.lbl_product.place(x=300, y=300, height=150, width=300)

        # Sales Label
        self.lbl_sales = Label(self.root, text="Total Sales\n[0]", bd=5, relief=RIDGE, bg="#3f51b5", fg="white",
                               font=("goudy old style", 20, "bold"))
        self.lbl_sales.place(x=650, y=300, height=150, width=300)
        # Sales _forcast
        btn_forecast = Button(self.root, text="Sales Forecast", command=self.forecast,
                      font=("times new roman", 16, "bold"), bg="green", fg="white", cursor="hand2")
        btn_forecast.place(x=550, y=630, width=250, height=40)





        #=======Footer=================
        footer = Label(self.root, text="Inventory Management System | Developed by Rajinder | © 2025",
                       font=("times new roman", 15), bg="#4d636d", fg="white").pack(side=BOTTOM,fill=X)
        
        self.update_content()
        
#######EmployeeFunction######
    
    def employee(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = employeeClass(self.new_win)

########## Supplier Function
    def supplier(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = supplierClass(self.new_win)

########## Category Function
    def category(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = categoryClass(self.new_win)
    
########### product function
    def product(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = productClass(self.new_win)

########## Sales Function
    def sales(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = salesClass(self.new_win)

############### Sales Forecast
    def forecast(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = SalesForecastClass(self.new_win)

    def run_sales_forecast(self):
        try:
            subprocess.Popen(["python", "sales_forecast.py"])
        except Exception as ex:
            messagebox.showerror("Error", f"Could not run forecast:\n{str(ex)}", parent=self.root)



    def update_content(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            product =cur.fetchall()
            self.lbl_product.config(text=f'Total Product\n[{str(len(product))}]')

            cur.execute("select * from supplier")
            supplier=cur.fetchall()
            self.lbl_supplier.config(text=f'Total Supplier\n[{str(len(supplier))}]')

            cur.execute("select * from category")
            category =cur.fetchall()
            self.lbl_category.config(text=f'Total Category\n[{str(len(category))}]')

            cur.execute("select * from employee")
            employee =cur.fetchall()
            self.lbl_employee.config(text=f'Total Employee\n[{str(len(employee))}]')
            bill= len(os.listdir('bill'))
            self.lbl_sales.config(text=f'Total Sales [{str(bill)}]')

            time_=time.strftime("%H:%M:%S") ################ get time
            date_=time.strftime("%m-%d-%Y")
            self.lbl_clock.config(text=f"Welcome to Inventory Management System\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            self.lbl_clock.after(200,self.update_content)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

    def exit(self):
        confirm = messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?", parent=self.root)
        if confirm:
            self.root.destroy()


    def logout(self):
        self.root.destroy()
        os.system("python  src/login.py")


# Create the main Tkinter window
if __name__ == "__main__":
    root = Tk()
    obj = IMS(root)
    root.mainloop()
