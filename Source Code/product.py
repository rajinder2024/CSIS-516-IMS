from tkinter import *
from PIL import Image, ImageTk
from activity_logger import ActivityLogger
from tkinter import ttk, messagebox
import sqlite3
class productClass:
    def __init__(self, root):  
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Inventory Management System")  # Set a window title
        self.root.config(bg="white")
        self.root.focus_force()
        #============================
        self.current_user_id = None 
        ####### Variable
        self.var_searchby=StringVar()
        self.var_searchtxt=StringVar()
        self.var_pid=StringVar()
        self.var_cat=StringVar()
        self.var_sup=StringVar()
        self.cat_list=[]
        self.sup_list=[]
        self.fetch_cat_sup()

        self.var_name=StringVar()
        self.var_price=StringVar()
        self.var_qty=StringVar()
        self.var_status=StringVar()

        product_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        product_Frame.place(x=10,y=10,width=450,height=480)

######### Title  #############3
        title=Label(product_Frame,text=" Manage Product Details",font=("goudy old style",18),bg="#0f4d7d",fg="white",cursor="hand2").pack(side=TOP,fill=X)
######## column1  
        lbl_category=Label(product_Frame,text="Category",font=("goudy old style",18),bg="white",cursor="hand2").place(x=30,y=60)
        lbl_supplier=Label(product_Frame,text="Supplier",font=("goudy old style",18),bg="white",cursor="hand2").place(x=30,y=110)
        lbl_product_name=Label(product_Frame,text="Name",font=("goudy old style",18),bg="white",cursor="hand2").place(x=30,y=160)
        lbl_price=Label(product_Frame,text="Price",font=("goudy old style",18),bg="white",cursor="hand2").place(x=30,y=210)
        lbl_quantity=Label(product_Frame,text="Quantity",font=("goudy old style",18),bg="white",cursor="hand2").place(x=30,y=260)
        lbl_status=Label(product_Frame,text="Status",font=("goudy old style",18),bg="white",cursor="hand2").place(x=30,y=310)

       
    ############ Column2
        cmd_cat = ttk.Combobox(product_Frame,textvariable=self.var_cat,values=self.cat_list,state='readonly',justify=CENTER, font=("goudy old style", 15))
        cmd_cat .place(x=150,y=60, width=200)
        cmd_cat.current(0)

        cmd_sup = ttk.Combobox(product_Frame,textvariable=self.var_sup,values=self.sup_list,state='readonly',justify=CENTER, font=("goudy old style", 15))
        cmd_sup .place(x=150,y=110, width=200)
        cmd_sup.current(0)

      
        txt_name =Entry(product_Frame,textvariable=self.var_name, font=("goudy old style", 15),bg="lightyellow").place(x=150,y=160, width=200)
        txt_price =Entry(product_Frame,textvariable=self.var_price, font=("goudy old style", 15),bg="lightyellow").place(x=150,y=210, width=200)
        txt_qty=Entry(product_Frame,textvariable=self.var_qty, font=("goudy old style", 15),bg="lightyellow").place(x=150,y=260, width=200)

        cmd_status = ttk.Combobox(product_Frame,textvariable=self.var_status,values=("Active","Inactive"),state='readonly',justify=CENTER, font=("goudy old style", 15))
        cmd_status .place(x=150,y=310, width=200)
        cmd_status.current(0)

    ######### Buttons  
        btn_add= Button(product_Frame,text="Save", command=self.add,font=("goudy old style",15),bg="gray",fg="white",cursor="hand2").place(x=10,y=400, width=100,height=40)
        btn_update= Button(product_Frame,text="Update",command=self.update, font=("goudy old style",15),bg="Lightblue",fg="white",cursor="hand2").place(x=120,y=400, width=100,height=40)
        btn_delete= Button(product_Frame,text="Delete",command=self.delete, font=("goudy old style",15),bg="Green",fg="white",cursor="hand2").place(x=230,y=400, width=100,height=40)
        btn_clear= Button(product_Frame,text="Clear",command=self.clear,font=("goudy old style",15),bg="red",fg="white",cursor="hand2").place(x=340,y=400, width=100,height=40)
      
    ########### Search Frame ########
        Searchframe = LabelFrame(self.root,text="Search Employee",bg="white", font=("goudy old style", 12, "bold"),bd=2,relief=RIDGE,)
        Searchframe.place(x=480, y=10, height=80, width=600)

        #######  Options ####
        cmd_search = ttk.Combobox(Searchframe,textvariable=self.var_searchby,values=("Select","Category","Supplier","Name"),state='readonly',justify=CENTER, font=("goudy old style", 15))
        cmd_search .place(x=10,y=10, width=180)
        cmd_search.current(0)

        txt_search =Entry(Searchframe, textvariable=self.var_searchtxt,font=("goudy old style",15), bg="lightyellow").place(x=200,y=10)
        btn_search= Button(Searchframe,text="Search",command=self.search,font=("goudy old style",15),bg="gray",fg="white",cursor="hand2").place(x=410,y=9, width=150,height=30)

        ######## Product  Details
        p_frame= Frame(self.root,bd=3,relief=RIDGE)
        p_frame.place(x=480,y=100,width=600,height=390)
        
        scrolly=Scrollbar(p_frame,orient=VERTICAL)
        scrollx=Scrollbar(p_frame,orient=HORIZONTAL)

        self.product_table=ttk.Treeview(p_frame,columns=("pid","Supplier","Category","name","price","qty","status",),
        yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_table.xview)
        scrolly.config(command=self.product_table.yview)


        self.product_table.heading("pid",text="Prod ID")
        self.product_table.heading("Category",text="Category")
        self.product_table.heading("Supplier",text="Supplier")
        self.product_table.heading("name",text="Name")
        self.product_table.heading("price",text="Price")
        self.product_table.heading("qty",text="Qty")
        self.product_table.heading("status",text="Status")
        
        self.product_table["show"]="headings"

        self.product_table.column("pid",width=90)
        self.product_table.column("Category",width=100)
        self.product_table.column("Supplier",width=100)
        self.product_table.column("name",width=100)
        self.product_table.column("price",width=100)
        self.product_table.column("qty",width=100)
        self.product_table.column("status",width=100)
        self.product_table.pack(fill= BOTH,expand=1)
        self.product_table.bind("<ButtonRelease-1>",self.get_data)  #event
        self.show()
        

    ########## categories and supplier names
    def fetch_cat_sup(self):
        self.cat_list.append("Empty")
        self.sup_list.append("Empty")
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("Select name from category")
            cat= cur.fetchall()
            if len(cat)>0:
                del self.cat_list[:]
                self.cat_list.append("Select")
                for i in cat:
                    self.cat_list.append(i[0])

            cur.execute("Select name from supplier")
            sup= cur.fetchall()        
            if len(sup)>0:
                del self.sup_list[:]
                self.sup_list.append("Select")
                for i in sup:
                    self.sup_list.append(i[0])
            print(sup)
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

    def set_current_user(self, user_id):
        """Set the current logged-in user ID for activity logging"""
        self.current_user_id = user_id
    ########## ADD
    def add(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Select" or self.var_cat.get()=="Empty" or self.var_sup.get()=="Select" or self.var_name.get()=="":
                messagebox.showerror("Error", "All fields are required",parent=self.root)
            else:
                cur.execute("Select * from product where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!= None:
                    messagebox.showerror("Error","Product already present, try different",parent=self.root)
                else:
                    cur.execute("Insert INTO product(Category,Supplier,name,price,qty,status) values(?,?,?,?,?,?)",(
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                    ))
                    con.commit()
                    ### log activity
                    ActivityLogger.log_activity(
                        activity=f"Added new product: {self.var_name.get()}",
                        user_id=self.current_user_id,
                        module="products",
                        details={
                            "name": self.var_name.get(),
                            "category": self.var_cat.get(),
                            "supplier": self.var_sup.get(),
                            "price": self.var_price.get(),
                            "quantity": self.var_qty.get(),
                            "status": self.var_status.get()
                        }
                    )
                    messagebox.showinfo("Success","Product  Addedd successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

    def show(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from product")
            rows=cur.fetchall()
            self.product_table.delete(*self.product_table.get_children())
            for row in rows:
                self.product_table.insert('',END,values=row)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

    def get_data(self,ev):
        f=self.product_table.focus()
        content=(self.product_table.item(f))
        row=content['values']
        self.var_pid.set(row[0])
        self.var_cat.set(row[2]),
        self.var_sup.set(row[1]),
        self.var_name.set(row[3]),
        self.var_price.set(row[4]),
        self.var_qty.set(row[5]),
        self.var_status.set(row[6]),
        

########################## update 

    def update(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error", "Please select product from list",parent=self.root)
            else:
                # First get current product details before updating
                cur.execute("SELECT name, Category, Supplier, price, qty, status FROM product WHERE pid=?",(self.var_pid.get(),))
                old_data = cur.fetchone()
                cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row == None:
                    messagebox.showerror("Error","Invalid Product",parent=self.root)
                else:
                    cur.execute("Update product set Category=?,Supplier=?,name=?,price=?,qty=?,status=? where pid=?",(
                        self.var_cat.get(),
                        self.var_sup.get(),
                        self.var_name.get(),
                        self.var_price.get(),
                        self.var_qty.get(),
                        self.var_status.get(),
                        self.var_pid.get()
                    ))
                    con.commit()
                     # Log the activity after successful update
                    ActivityLogger.log_activity(
                        activity=f"Updated product: {self.var_name.get()}",
                        user_id=self.current_user_id,
                        module="products",
                        details={
                            "pid": self.var_pid.get(),
                            "changes": {
                                "name": f"{old_data[0]} → {self.var_name.get()}",
                                "category": f"{old_data[1]} → {self.var_cat.get()}",
                                "supplier": f"{old_data[2]} → {self.var_sup.get()}",
                                "price": f"{old_data[3]} → {self.var_price.get()}",
                                "quantity": f"{old_data[4]} → {self.var_qty.get()}",
                                "status": f"{old_data[5]} → {self.var_status.get()}"
                            }
                        }
                    )
                    messagebox.showinfo("Success","Product Updated successfully",parent=self.root)
                    self.show()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)
                     
################### Delete
    def delete(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_pid.get()=="":
                messagebox.showerror("Error", "Select product from list",parent=self.root)
            else:
                cur.execute("SELECT name, Category, Supplier, price, qty FROM product WHERE pid=?",(self.var_pid.get(),))
                prod_data = cur.fetchone()
                
                if prod_data== None:
                    messagebox.showerror("Error","Invalid",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        # Log the activity before deletion
                        ActivityLogger.log_activity(
                            activity=f"Deleted product: {prod_data[0]}",
                            user_id=self.current_user_id,
                            module="products",
                            details={
                                "pid": self.var_pid.get(),
                                "name": prod_data[0],
                                "category": prod_data[1],
                                "supplier": prod_data[2],
                                "price": prod_data[3],
                                "quantity": prod_data[4]
                            }
                        )
                        
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Product Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)

            '''cur.execute("Select * from product where pid=?",(self.var_pid.get(),))
                row=cur.fetchone()
                if row== None:
                    messagebox.showerror("Error","Invalid ",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to delete?",parent=self.root)
                    if op==True:
                        cur.execute("delete from product where pid=?",(self.var_pid.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Product Deleted Successfully",parent=self.root)
                        self.clear()
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)'''

################## Clear
    def clear(self):
        self.var_cat.set("Select"),
        self.var_sup.set("Select"),
        self.var_name.set(""),
        self.var_price.set(""),
        self.var_qty.set(""),
        self.var_status.set("Active"),
        self.var_pid.set("")
        self.var_searchtxt.set("")
        self.var_searchby.set("Select")
        self.show()

############## Search
    def search(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_searchby.get()=="Select":
                messagebox.showerror("Error","Select Search by Options",parent=self.root)
            elif self.var_searchtxt.get()=="":
                messagebox.showerror("Error","Search input should be required",parent=self.root)

            else:
                cur.execute("select * from product where "+self.var_searchby.get()+" LIKE '%"+self.var_searchtxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_table.delete(*self.product_table.get_children())
                    for row in rows:
                        self.product_table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","No record found",parent=self.root)

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to :{str(ex)}",parent=self.root)




if __name__ == "__main__":
    root = Tk()
    obj = productClass(root)
    root.mainloop()