from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime, timedelta
import pandas as pd

class SalesReportClass:
    def __init__(self, root):  
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Sales Report | Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()
        
        # Variables
        self.var_search_by = StringVar()
        self.var_date_from = StringVar()
        self.var_date_to = StringVar()
        
        # Title
        title = Label(self.root, text="Sales Reports", font=("goudy old style", 30), 
                     bg="#184a45", fg="white", bd=3, relief=RIDGE)
        title.pack(side=TOP, fill=X, padx=10, pady=20)
        
        # Search Frame
        search_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        search_frame.place(x=10, y=80, width=1080, height=70)
        
        # Search Options
        lbl_search = Label(search_frame, text="Search By:", font=("goudy old style", 15), bg="white")
        lbl_search.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        cmd_search = ttk.Combobox(search_frame, textvariable=self.var_search_by,
                                 values=("Daily", "Weekly", "Monthly", "Yearly", "Custom"), 
                                 state='readonly', font=("goudy old style", 12))
        cmd_search.current(0)
        cmd_search.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        lbl_from = Label(search_frame, text="From:", font=("goudy old style", 15), bg="white")
        lbl_from.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        
        txt_from = Entry(search_frame, textvariable=self.var_date_from, 
                        font=("goudy old style", 12), bg="lightyellow")
        txt_from.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        lbl_to = Label(search_frame, text="To:", font=("goudy old style", 15), bg="white")
        lbl_to.grid(row=0, column=4, padx=5, pady=5, sticky="e")
        
        txt_to = Entry(search_frame, textvariable=self.var_date_to, 
                      font=("goudy old style", 12), bg="lightyellow")
        txt_to.grid(row=0, column=5, padx=5, pady=5, sticky="w")
        
        btn_search = Button(search_frame, text="Search", command=self.search_data,
                          font=("goudy old style", 12), bg="#2196f3", fg="white", cursor="hand2")
        btn_search.grid(row=0, column=6, padx=10, pady=5)
        
        btn_show_all = Button(search_frame, text="Show All", command=self.show_all,
                            font=("goudy old style", 12), bg="gray", fg="white", cursor="hand2")
        btn_show_all.grid(row=0, column=7, padx=10, pady=5)
        
        btn_export = Button(search_frame, text="Export to Excel", command=self.export_to_excel,
                           font=("goudy old style", 12), bg="green", fg="white", cursor="hand2")
        btn_export.grid(row=0, column=8, padx=10, pady=5)
        
        # Report Frame
        report_frame = Frame(self.root, bd=3, relief=RIDGE)
        report_frame.place(x=10, y=160, width=500, height=330)
        
        scroll_y = Scrollbar(report_frame, orient=VERTICAL)
        scroll_x = Scrollbar(report_frame, orient=HORIZONTAL)
        
        self.sales_table = ttk.Treeview(report_frame, columns=("invoice", "date", "customer", "amount", "discount", "net_pay"),
                                      yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.sales_table.xview)
        scroll_y.config(command=self.sales_table.yview)
        
        self.sales_table.heading("invoice", text="Invoice No.")
        self.sales_table.heading("date", text="Date")
        self.sales_table.heading("customer", text="Customer")
        self.sales_table.heading("amount", text="Amount")
        self.sales_table.heading("discount", text="Discount")
        self.sales_table.heading("net_pay", text="Net Pay")
        
        self.sales_table["show"] = "headings"
        
        self.sales_table.column("invoice", width=80)
        self.sales_table.column("date", width=80)
        self.sales_table.column("customer", width=100)
        self.sales_table.column("amount", width=80)
        self.sales_table.column("discount", width=80)
        self.sales_table.column("net_pay", width=80)
        
        self.sales_table.pack(fill=BOTH, expand=1)
        
        # Chart Frame
        self.chart_frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        self.chart_frame.place(x=520, y=160, width=570, height=330)
        
        # Summary Frame
        summary_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        summary_frame.place(x=10, y=500, width=1080, height=80)
        
        lbl_total = Label(summary_frame, text="Total Sales:", font=("goudy old style", 15), bg="white")
        lbl_total.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.lbl_total_value = Label(summary_frame, text="0", font=("goudy old style", 15, "bold"), bg="white")
        self.lbl_total_value.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        lbl_total_discount = Label(summary_frame, text="Total Discount:", font=("goudy old style", 15), bg="white")
        lbl_total_discount.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        
        self.lbl_total_discount_value = Label(summary_frame, text="0", font=("goudy old style", 15, "bold"), bg="white")
        self.lbl_total_discount_value.grid(row=0, column=3, padx=5, pady=5, sticky="w")
        
        lbl_net_pay = Label(summary_frame, text="Net Pay:", font=("goudy old style", 15), bg="white")
        lbl_net_pay.grid(row=0, column=4, padx=10, pady=5, sticky="w")
        
        self.lbl_net_pay_value = Label(summary_frame, text="0", font=("goudy old style", 15, "bold"), bg="white")
        self.lbl_net_pay_value.grid(row=0, column=5, padx=5, pady=5, sticky="w")
        
        # Initialize with current date
        today = datetime.now().strftime("%d-%m-%Y")
        self.var_date_from.set(today)
        self.var_date_to.set(today)
        
        self.show_daily_report()
    
    def search_data(self):
        search_by = self.var_search_by.get()
        
        if search_by == "Daily":
            self.show_daily_report()
        elif search_by == "Weekly":
            self.show_weekly_report()
        elif search_by == "Monthly":
            self.show_monthly_report()
        elif search_by == "Yearly":
            self.show_yearly_report()
        elif search_by == "Custom":
            self.show_custom_report()
    
    def show_daily_report(self):
        date = self.var_date_from.get()
        try:
            datetime.strptime(date, "%d-%m-%Y")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use DD-MM-YYYY", parent=self.root)
            return
        
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        
        try:
            # Get all bill files for the selected date
            bill_files = []
            for file in os.listdir('bill'):
                if file.endswith('.txt'):
                    bill_date = self.extract_date_from_bill(file)
                    if bill_date == date:
                        bill_files.append(file)
            
            # Clear existing data
            self.sales_table.delete(*self.sales_table.get_children())
            
            total_amount = 0
            total_discount = 0
            total_net_pay = 0
            
            for file in bill_files:
                invoice_no = file.split('.')[0]
                with open(f'bill/{file}', 'r') as f:
                    lines = f.readlines()
                    
                    # Extract customer name (assuming it's on line 5)
                    customer_line = lines[4].strip()
                    customer = customer_line.split(':')[1].strip()
                    
                    # Extract amounts (assuming they're at the bottom)
                    amount_line = [line for line in lines if "Bill Amount" in line][0]
                    amount = float(amount_line.split('Rs.')[1].strip())
                    
                    discount_line = [line for line in lines if "Discount" in line][0]
                    discount = float(discount_line.split('Rs.')[1].strip())
                    
                    net_pay_line = [line for line in lines if "Net Pay" in line][0]
                    net_pay = float(net_pay_line.split('Rs.')[1].strip())
                    
                    self.sales_table.insert('', END, values=(
                        invoice_no, date, customer, amount, discount, net_pay
                    ))
                    
                    total_amount += amount
                    total_discount += discount
                    total_net_pay += net_pay
            
            # Update summary
            self.lbl_total_value.config(text=f"Rs. {total_amount:.2f}")
            self.lbl_total_discount_value.config(text=f"Rs. {total_discount:.2f}")
            self.lbl_net_pay_value.config(text=f"Rs. {total_net_pay:.2f}")
            
            # Update chart
            self.update_chart(date, total_amount, total_discount, total_net_pay)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()
    
    def extract_date_from_bill(self, filename):
        try:
            with open(f'bill/{filename}', 'r') as f:
                for line in f:
                    if "Date:" in line:
                        return line.split("Date:")[1].strip().split()[0]
        except:
            return ""
    
    def update_chart(self, date, amount, discount, net_pay):
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Create new chart
        fig, ax = plt.subplots(figsize=(5.5, 3.2), dpi=100)
        
        categories = ['Total Amount', 'Discount', 'Net Pay']
        values = [amount, discount, net_pay]
        
        bars = ax.bar(categories, values, color=['#4CAF50', '#FFC107', '#2196F3'])
        ax.set_title(f'Sales Summary for {date}')
        ax.set_ylabel('Amount (Rs.)')
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'Rs.{height:.2f}',
                    ha='center', va='bottom')
        
        # Embed chart in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    
    def show_weekly_report(self):
        # Implement weekly report logic
        pass
    
    def show_monthly_report(self):
        # Implement monthly report logic
        pass
    
    def show_yearly_report(self):
        # Implement yearly report logic
        pass
    
    def show_custom_report(self):
        # Implement custom date range report logic
        pass
    
    def show_all(self):
        # Show all sales data
        pass
    
    def export_to_excel(self):
        # Export data to Excel
        pass

if __name__ == "__main__":
    root = Tk()
    obj = SalesReportClass(root)
    root.mainloop()