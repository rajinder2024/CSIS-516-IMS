from tkinter import *

class IMS:
    def __init__(self, root):  # Fixed spacing in method definition
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System")  # Optional: Set a window title

# Create the main Tkinter window
root = Tk()

# Instantiate the IMS class with the root window
obj = IMS(root)

# Run the Tkinter event loop
root.mainloop()
#################################################################################################################
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class employeeClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()

        # ====================
        ###### Variables ######
        self.var_searchby = StringVar()
        self.var_searchtxt = StringVar()

        self.var_emp_id = StringVar()
        self.var_gender = StringVar()
        self.var_contact = StringVar()
        self.var_name = StringVar()
        self.var_dob = StringVar()
        self.var_doj = StringVar()
        self.var_email = StringVar()
        self.var_password = StringVar()
        self.var_utype = StringVar()
        self.var_salary = StringVar()

        ########### Search Frame ########
        Searchframe = LabelFrame(self.root, text="Search Employee", bg="white", font=("goudy old style", 12, "bold"), bd=2, relief=RIDGE)
        Searchframe.place(x=250, y=20, height=70, width=600)

        ####### Options ####
        cmd_search = ttk.Combobox(Searchframe, textvariable=self.var_searchby, values=("Select", "Email", "Name", "Contact"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmd_search.place(x=10, y=10, width=180)
        cmd_search.current(0)

        Txt_search = Entry(Searchframe, textvariable=self.var_searchtxt, font=("goudy old style", 15), bg="lightyellow").place(x=200, y=10)
        Button(Searchframe, text="Search", font=("goudy old style", 15), bg="gray", fg="white", cursor="hand2").place(x=410, y=9, width=150, height=30)

        ####### Title ####
        title = Label(self.root, text="Employee Details", font=("goudy old style", 15), bg="#0f4d7d", fg="white").place(x=50, y=100, width=1000)

        ########### Page Content ###########
        # Row 1
        lbl_empid = Label(self.root, text="Emp ID", font=("goudy old style", 15), bg="lightyellow").place(x=50, y=150)
        lbl_gender = Label(self.root, text="Gender", font=("goudy old style", 15), bg="white").place(x=350, y=150)
        lbl_contact = Label(self.root, text="Contact", font=("goudy old style", 15), bg="white").place(x=750, y=150)

        Entry(self.root, textvariable=self.var_emp_id, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=150, width=180)
        cmd_gender = ttk.Combobox(self.root, textvariable=self.var_gender, values=("Select", "Male", "Female", "Other"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmd_gender.place(x=500, y=150, width=180)
        cmd_gender.current(0)

        Entry(self.root, textvariable=self.var_contact, font=("goudy old style", 15), bg="white").place(x=850, y=150, width=180)

        # Row 2
        lbl_name = Label(self.root, text="Name", font=("goudy old style", 15), bg="white").place(x=50, y=190)
        lbl_dob = Label(self.root, text="D.O.B", font=("goudy old style", 15), bg="white").place(x=350, y=190)
        lbl_doj = Label(self.root, text="D.O.J", font=("goudy old style", 15), bg="white").place(x=750, y=190)

        Entry(self.root, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=190, width=180)
        Entry(self.root, textvariable=self.var_dob, font=("goudy old style", 15), bg="lightyellow").place(x=500, y=190, width=180)
        Entry(self.root, textvariable=self.var_doj, font=("goudy old style", 15), bg="lightyellow").place(x=850, y=190, width=180)

        # Row 3
        lbl_email = Label(self.root, text="Email", font=("goudy old style", 15), bg="white").place(x=50, y=230)
        lbl_password = Label(self.root, text="Password", font=("goudy old style", 15), bg="white").place(x=350, y=230)
        lbl_utype = Label(self.root, text="User Type", font=("goudy old style", 15), bg="white").place(x=750, y=230)

        Entry(self.root, textvariable=self.var_email, font=("goudy old style", 15), bg="lightyellow").place(x=150, y=230, width=180)
        Entry(self.root, textvariable=self.var_password, font=("goudy old style", 15), bg="lightyellow").place(x=500, y=230, width=180)
        cmd_utype = ttk.Combobox(self.root, textvariable=self.var_utype, values=("Admin", "Employee"), state='readonly', justify=CENTER, font=("goudy old style", 15))
        cmd_utype.place(x=850, y=230, width=180)
        cmd_utype.current(0)

        # Row 4
        lbl_address = Label(self.root, text="Address", font=("goudy old style", 15), bg="white").place(x=50, y=270)
        lbl_salary = Label(self.root, text="Salary", font=("goudy old style", 15), bg="white").place(x=500, y=270)

        self.txt_address = Text(self.root, font=("goudy old style", 15), bg="lightyellow")
        self.txt_address.place(x=150, y=270, width=300, height=60)
        Entry(self.root, textvariable=self.var_salary, font=("goudy old style", 15), bg="lightyellow").place(x=600, y=270, width=180)

        # Buttons
        Button(self.root, text="Save", font=("goudy old style", 15), bg="gray", fg="white", cursor="hand2").place(x=500, y=305, width=110, height=28)
        Button(self.root, text="Update", font=("goudy old style", 15), bg="lightblue", fg="white", cursor="hand2").place(x=620, y=305, width=110, height=28)
        Button(self.root, text="Delete", font=("goudy old style", 15), bg="green", fg="white", cursor="hand2").place(x=740, y=305, width=110, height=28)
        Button(self.root, text="Clear", font=("goudy old style", 15), bg="red", fg="white", cursor="hand2").place(x=860, y=305, width=110, height=28)

        # Employee Info Table
        emp_frame = Frame(self.root, bd=3, relief=RIDGE)
        emp_frame.place(x=0, y=350, relwidth=1, height=150)

        scrolly = Scrollbar(emp_frame, orient=VERTICAL)
        scrollx = Scrollbar(emp_frame, orient=HORIZONTAL)

        self.EmployeeTable = ttk.Treeview(emp_frame, columns=("eid", "name", "email", "gender", "contact", "dob", "doj", "password", "utype", "address", "salary"),
                                          yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("eid", text="EMP ID")
        self.EmployeeTable.heading("name", text="Name")
        self.EmployeeTable.heading("email", text="Email")
        self.EmployeeTable.heading("gender", text="Gender")
        self.EmployeeTable.heading("contact", text="Contact")
        self.EmployeeTable.heading("dob", text="D.O.B")
        self.EmployeeTable.heading("doj", text="D.O.J")
        self.EmployeeTable.heading("password", text="Password")
        self.EmployeeTable.heading("utype", text="User Type")
        self.EmployeeTable.heading("address", text="Address")
        self.EmployeeTable.heading("salary", text="Salary")

        self.EmployeeTable["show"] = "headings"
        for col in self.EmployeeTable["columns"]:
            self.EmployeeTable.column(col, width=100)

        self.EmployeeTable.pack(fill=BOTH, expand=1)

    def add(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            # Check for empty Employee ID
            if self.var_emp_id.get() == "":
                messagebox.showerror("Error", "Employee ID is required", parent=self.root)
            # Check for valid Gender and User Type selection
            elif self.var_gender.get() == "Select" or self.var_utype.get() == "Select":
                messagebox.showerror("Error", "Please select valid Gender and User Type", parent=self.root)
            else:
            # Check if Employee ID already exists
                cur.execute("SELECT * FROM employee WHERE eid=?", (self.var_emp_id.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Employee ID is already assigned", parent=self.root)
                else:
                    # Insert new employee into the database
                    cur.execute("""
                    INSERT INTO employee (
                        eid, name, email, gender, contact, dob, doj, password, utype, address, salary
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        self.var_emp_id.get(), 
                        self.var_name.get(), 
                        self.var_email.get(), 
                        self.var_gender.get(), 
                        self.var_contact.get(), 
                        self.var_dob.get(), 
                        self.var_doj.get(), 
                        self.var_password.get(), 
                        self.var_utype.get(), 
                        self.txt_address.get('1.0', END).strip(), 
                        self.var_salary.get()
                    ))
                    con.commit()
                    # Show success message
                    messagebox.showinfo("Success", "Employee added successfully", parent=self.root)
                    self.show()  # Refresh the table to display the new employee
        except Exception as ex:
            # Handle exceptions
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            # Close the database connection
            con.close()

    def show(self):
        """Fetch and display all employees in the Treeview table."""
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            rows = cur.fetchall()
            # Clear existing entries in the table
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
        # Insert fetched rows into the table
            for row in rows:
                self.EmployeeTable.insert('', END, values=row)
        except Exception as ex:
            # Handle exceptions during fetch
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
        # Close the database connection
            con.close()



if __name__ == "__main__":
    root = Tk()
    obj = employeeClass(root)
    root.mainloop()

