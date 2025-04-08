from tkinter import*
from PIL import ImageTk
from tkinter import messagebox
import sqlite3
import subprocess
import os
class Login_System:
    def __init__(self,root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("Inventory Management System")  # Set a window title
        self.root.config(bg="#fafafa")
        ##### Image 
        self.phone_image= ImageTk.PhotoImage(file="images/phone.png")
        self.lbl_Phone_Image = Label(self.root,image=self.phone_image,bd=0).place(x=200,y=50)

        ##### Login frame
        self.employee_id=StringVar()
        self.password=StringVar()

        login_frame= Frame(self.root,bd=2,relief=RIDGE,bg="white")
        login_frame.place(x=650,y=90,width=350,height=460)

        title= Label(login_frame,text="Login System", font=("Elephant",30,"bold"),bg="white").place(x=0,y=30,relwidth=1)

        lbl_user=Label(login_frame,text="Employee ID",font=("Anadulus",15),bg="white",fg="#767171").place(x=50,y=100)
        txt_employee_id=Entry(login_frame,textvariable=self.employee_id,font=("Times new roman",12),bg="#ECECEC").place(x=50,y=140,width=250)

        lbl_pass=Label(login_frame,text="Password",font=("Anadulus",15),bg="white",fg="#767171").place(x=50,y=200)
        txt_pass=Entry(login_frame,textvariable=self.password,show="*",font=("Times new roman",12),bg="#ECECEC").place(x=50,y=240,width=250)

        btn_login= Button(login_frame,text="Log In",command=self.login, font=("Arial Rounded MT Bold",15),bg="#00B0F0",activebackground="#00b0F0",activeforeground="white",cursor="hand2").place(x=50,y=300,width=250,height=35)
        hr= Label(login_frame,bg="lightgray").place(x=50,y=370,height=2,width=250)
        or_= Label(login_frame,text="OR",bg="white",fg="lightgray",font=("Times new roman",15,"bold")).place(x=150,y=355)

        btn_forget= Button(login_frame,text="Forget Password", font=("times new roman",13),bg="white",fg="#00759E",bd=0,activebackground="white",activeforeground="#00759E").place(x=100,y=390)

        ########## frame2
        register_frame= Frame(self.root,bd=2,relief=RIDGE,bg="white")
        register_frame.place(x=650,y=570,width=350,height=60)

        lbl_reg=Label(register_frame,text="Don't have an account ?",font=("times new roman",13),bg="white").place(x=0,y=20,relwidth=1)
       
        ########### Animation image
        self.im1= ImageTk.PhotoImage(file="images/im1.png")
        self.im2= ImageTk.PhotoImage(file="images/im2.png")
        self.im3= ImageTk.PhotoImage(file="images/im3.png")

        self.lbl_change_image=Label(self.root,bg="lightgray")
        self.lbl_change_image.place(x=367,y=153,width=240,height=428)

        self.animate()
    ########## All Functions
    #    
    def animate(self):
        self.im=self.im1
        self.im1=self.im2
        self.im2=self.im3
        self.im3=self.im
        self.lbl_change_image.config(image=self.im)
        self.lbl_change_image.after(2000,self.animate)


    def login(self):
       con=sqlite3.connect(database=r'ims.db')
       cur=con.cursor()
       try:
           if self.employee_id.get()=="" or self.password.get()=="":
               messagebox.showerror('Error', "All fields are required", parent=self.root)
           else: 
                cur.execute("select utype from employee where eid=? AND pass=?",(self.employee_id.get(), self.password.get()))
                user=cur.fetchone()
                if user== None:
                     messagebox.showerror('Error', "Invalid Username/Password", parent=self.root)
                else:
                    if user[0]=="Admin":
                        self.root.destroy()
                        subprocess.Popen(["python", "Source Code/dashboard.py"])

                        #os.system("python dashboard.py")
                    else:
                        self.root.destroy()
                        subprocess.Popen(["python", "Source Code/billing.py"])

                        
       except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

    def forget_window():
        pass
        

  


root= Tk()
obj= Login_System(root)
root.mainloop()

