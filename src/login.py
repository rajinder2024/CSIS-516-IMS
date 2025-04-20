from tkinter import *
from tkinter import messagebox
import sqlite3
import subprocess
import sys
import os

class Login_System:
    def __init__(self, root):
        self.root = root
        print(">>> login.py started")
        self.root.geometry("900x500+200+100")
        self.root.title("Inventory Management System - Login")
        self.root.config(bg="#f0f0f0")

        # Variables
        self.employee_id = StringVar()
        self.password = StringVar()

        # Main Frame
        login_frame = Frame(self.root, bg="white", bd=2, relief=RIDGE)
        login_frame.place(x=250, y=80, width=400, height=340)

        title = Label(login_frame, text="Login", font=("Arial", 25, "bold"), bg="white", fg="#333")
        title.pack(pady=20)

        lbl_user = Label(login_frame, text="Employee ID", font=("Arial", 14), bg="white", anchor="w")
        lbl_user.pack(fill=X, padx=40, pady=(10, 0))
        txt_user = Entry(login_frame, textvariable=self.employee_id, font=("Arial", 12), bg="#eaeaea")
        txt_user.pack(fill=X, padx=40, pady=5)

        lbl_pass = Label(login_frame, text="Password", font=("Arial", 14), bg="white", anchor="w")
        lbl_pass.pack(fill=X, padx=40, pady=(10, 0))
        txt_pass = Entry(login_frame, textvariable=self.password, show="*", font=("Arial", 12), bg="#eaeaea")
        txt_pass.pack(fill=X, padx=40, pady=5)

        btn_login = Button(login_frame, text="Log In", command=self.login,
                           font=("Arial", 14, "bold"), bg="#0078D7", fg="white", cursor="hand2")
        btn_login.pack(pady=20, ipadx=5)

        btn_forget = Button(login_frame, text="Forgot Password?", command=self.forget_window,
                            font=("Arial", 10), bg="white", fg="blue", bd=0, cursor="hand2")
        btn_forget.pack()

        # Footer
        footer = Label(self.root, text="© 2025 Inventory Management System", font=("Arial", 10), bg="#f0f0f0")
        footer.pack(side=BOTTOM, fill=X)

    ###################### Login ######################
    def login(self):
        try:
            con = sqlite3.connect(database=r'ims.db')
            con.row_factory = sqlite3.Row
            cur = con.cursor()

            if self.employee_id.get() == "" or self.password.get() == "":
                messagebox.showerror('Error', "All fields are required", parent=self.root)
            else:
                cur.execute("SELECT * FROM employee WHERE eid=? AND pass=?", 
                            (self.employee_id.get(), self.password.get()))
                user = cur.fetchone()
                print(">>> USER FETCHED:", user)

                if user is None:
                    messagebox.showerror('Error', "Invalid Username/Password", parent=self.root)
                else:
                    role = user["utype"].lower()        
                    print(">>> ROLE:", role)

                    if role == "admin":
                        self.root.destroy()
                        os.system("python src/dashboard.py")
                    elif role == "employee":
                        self.root.destroy()
                        os.system("python src/billing.py")
                    else:
                        messagebox.showerror("Error", "Unknown role type", parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

   

    ###################### Forget Password ######################
    def forget_window(self):
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            if self.employee_id.get() == "":
                messagebox.showerror('Error', "Employee ID must be required", parent=self.root)
            else:
                cur.execute("SELECT email FROM employee WHERE eid=?", (self.employee_id.get(),))
                email = cur.fetchone()
                if email is None:
                    messagebox.showerror('Error', "Invalid Employee ID, try again", parent=self.root)
                else:
                    self.var_otp = StringVar()
                    self.var_new_pass = StringVar()
                    self.var_conf_pass = StringVar()

                    self.forget_win = Toplevel(self.root)
                    self.forget_win.title('RESET PASSWORD')
                    self.forget_win.geometry('400x350+500+150')
                    self.forget_win.focus_force()

                    title = Label(self.forget_win, text="Reset Password", font=('Arial', 15, 'bold'), bg='#3f51b5', fg="white")
                    title.pack(side=TOP, fill=X)

                    lbl_reset = Label(self.forget_win, text="Enter OTP sent to registered email", font=("Arial", 12))
                    lbl_reset.place(x=20, y=60)
                    txt_reset = Entry(self.forget_win, textvariable=self.var_otp, font=("Arial", 12), bg="lightyellow")
                    txt_reset.place(x=20, y=90, height=30, width=250)

                    self.btn_reset = Button(self.forget_win, text="SUBMIT", font=("Arial", 12), bg="lightblue")
                    self.btn_reset.place(x=280, y=90, height=30, width=100)

                    lbl_new_pass = Label(self.forget_win, text="New Password", font=("Arial", 12))
                    lbl_new_pass.place(x=20, y=140)
                    txt_new_pass = Entry(self.forget_win, textvariable=self.var_new_pass, font=("Arial", 12), bg="lightyellow")
                    txt_new_pass.place(x=20, y=170, height=30, width=250)

                    lbl_c_pass = Label(self.forget_win, text="Confirm Password", font=("Arial", 12))
                    lbl_c_pass.place(x=20, y=210)
                    txt_c_pass = Entry(self.forget_win, textvariable=self.var_conf_pass, font=("Arial", 12), bg="lightyellow")
                    txt_c_pass.place(x=20, y=240, height=30, width=250)

                    self.btn_update = Button(self.forget_win, text="UPDATE", state='disabled', font=("Arial", 12), bg="lightblue")
                    self.btn_update.place(x=150, y=290, height=30, width=100)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)

###################### Main ######################
if __name__ == "__main__":
    root = Tk()
    obj = Login_System(root)
    root.mainloop()
