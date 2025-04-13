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
        
        btn_show_all = Button(search_frame, text="Show All", command=self.show_all_data,
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
    
    def show_all_data(self):
        """Show all sales data in the database"""
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        
        try:
            cur.execute("""
                SELECT invoice, date, customer_name, subtotal, discount, total 
                FROM sales 
                ORDER BY date DESC, time DESC
                LIMIT 100  # Limit to prevent performance issues
            """)
            
            rows = cur.fetchall()
            
            self.sales_table.delete(*self.sales_table.get_children())
            
            total_amount = 0
            total_discount = 0
            total_net_pay = 0
            
            for row in rows:
                self.sales_table.insert('', END, values=row)
                total_amount += row[3]
                total_discount += row[4]
                total_net_pay += row[5]
            
            self.lbl_total_value.config(text=f"Rs. {total_amount:.2f}")
            self.lbl_total_discount_value.config(text=f"Rs. {total_discount:.2f}")
            self.lbl_net_pay_value.config(text=f"Rs. {total_net_pay:.2f}")
            
            self.update_chart("All Sales Data", total_amount, total_discount, total_net_pay)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()
    
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
            # Convert to proper date format for SQL query
            sql_date = datetime.strptime(date, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use DD-MM-YYYY", parent=self.root)
            return
        
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        
        try:
            # Get detailed transactions for the day
            cur.execute("""
                SELECT invoice, date, customer_name, subtotal, discount, total 
                FROM sales 
                WHERE date = ?
                ORDER BY time
            """, (sql_date,))
            
            rows = cur.fetchall()
            
            # Clear existing data
            self.sales_table.delete(*self.sales_table.get_children())
            
            total_amount = 0
            total_discount = 0
            total_net_pay = 0
            
            for row in rows:
                self.sales_table.insert('', END, values=(
                    row[0],     # Invoice No
                    row[1],     # Date
                    row[2],     # Customer
                    row[3],     # Subtotal
                    row[4],     # Discount
                    row[5]      # Total
                ))
                
                total_amount += row[3]
                total_discount += row[4]
                total_net_pay += row[5]
            
            # Update summary labels
            self.lbl_total_value.config(text=f"Rs. {total_amount:.2f}")
            self.lbl_total_discount_value.config(text=f"Rs. {total_discount:.2f}")
            self.lbl_net_pay_value.config(text=f"Rs. {total_net_pay:.2f}")
            
            # Update chart
            self.update_chart(date, total_amount, total_discount, total_net_pay)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show_weekly_report(self):
        """Show weekly sales summary"""
        date = self.var_date_from.get()
        try:
            # Convert to proper date format
            dt = datetime.strptime(date, "%d-%m-%Y")
            start_of_week = dt - timedelta(days=dt.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            
            sql_start = start_of_week.strftime("%Y-%m-%d")
            sql_end = end_of_week.strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use DD-MM-YYYY", parent=self.root)
            return
        
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        
        try:
            # Get weekly summary
            cur.execute("""
                SELECT 
                    strftime('%Y-%m-%d', date) as day,
                    SUM(subtotal) as day_total,
                    SUM(discount) as day_discount,
                    SUM(total) as day_net
                FROM sales
                WHERE date BETWEEN ? AND ?
                GROUP BY date
                ORDER BY date
            """, (sql_start, sql_end))
            
            rows = cur.fetchall()
            
            self.sales_table.delete(*self.sales_table.get_children())
            
            total_amount = 0
            total_discount = 0
            total_net_pay = 0
            
            for row in rows:
                self.sales_table.insert('', END, values=(
                    f"Day {row[0]}",
                    row[0],
                    "All Customers",
                    row[1],
                    row[2],
                    row[3]
                ))
                total_amount += row[1]
                total_discount += row[2]
                total_net_pay += row[3]
            
            # Update summary and chart
            self.lbl_total_value.config(text=f"Rs. {total_amount:.2f}")
            self.lbl_total_discount_value.config(text=f"Rs. {total_discount:.2f}")
            self.lbl_net_pay_value.config(text=f"Rs. {total_net_pay:.2f}")
            self.update_chart(f"Week {start_of_week.strftime('%d-%m-%Y')} to {end_of_week.strftime('%d-%m-%Y')}", 
                            total_amount, total_discount, total_net_pay)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show_monthly_report(self):
        month_year = self.var_date_from.get()  # Expected format: MM-YYYY
        
        try:
            # Convert to proper format for SQL query
            dt = datetime.strptime(f"01-{month_year}", "%d-%m-%Y")
            sql_month = dt.strftime("%Y-%m")
        except ValueError:
            messagebox.showerror("Error", "Invalid format. Use MM-YYYY", parent=self.root)
            return
        
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        
        try:
            # Option 1: Use monthly_sales_summary if available
            try:
                cur.execute("""
                    SELECT month, total_sales, total_discount, net_sales 
                    FROM monthly_sales_summary
                    WHERE strftime('%Y-%m', month) = ?
                """, (sql_month,))
                row = cur.fetchone()
                
                if row:
                    self.show_monthly_summary(row, month_year)
                    return
            except sqlite3.OperationalError:
                pass  # Table doesn't exist
            
            # Option 2: Aggregate from sales table
            cur.execute("""
                SELECT 
                    strftime('%Y-%m', date) as month,
                    SUM(subtotal) as total_sales,
                    SUM(discount) as total_discount,
                    SUM(total) as net_sales
                FROM sales
                WHERE strftime('%Y-%m', date) = ?
                GROUP BY strftime('%Y-%m', date)
            """, (sql_month,))
            
            row = cur.fetchone()
            
            if row:
                self.show_monthly_summary(row, month_year)
            else:
                messagebox.showinfo("Info", "No sales data found for this month", parent=self.root)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show_monthly_summary(self, row, month_year):
        # Clear existing data
        self.sales_table.delete(*self.sales_table.get_children())
        
        # Insert the monthly summary
        self.sales_table.insert('', END, values=(
            "Monthly Summary",  # Invoice No
            row[0],            # Month
            "All Customers",   # Customer
            row[1],           # Total Amount
            row[2],           # Discount
            row[3]            # Net Pay
        ))
        
        # Update summary labels
        self.lbl_total_value.config(text=f"Rs. {row[1]:.2f}")
        self.lbl_total_discount_value.config(text=f"Rs. {row[2]:.2f}")
        self.lbl_net_pay_value.config(text=f"Rs. {row[3]:.2f}")
        
        # Update chart
        self.update_chart(month_year, row[1], row[2], row[3])

    def show_yearly_report(self):
        """Show yearly sales summary"""
        year = self.var_date_from.get()  # Expected format: YYYY
        
        try:
            # Validate year format
            int(year)
            if len(year) != 4:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid year format. Use YYYY", parent=self.root)
            return
        
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        
        try:
            # Get monthly breakdown for the year
            cur.execute("""
                SELECT 
                    strftime('%Y-%m', date) as month,
                    SUM(subtotal) as month_total,
                    SUM(discount) as month_discount,
                    SUM(total) as month_net
                FROM sales
                WHERE strftime('%Y', date) = ?
                GROUP BY strftime('%Y-%m', date)
                ORDER BY month
            """, (year,))
            
            rows = cur.fetchall()
            
            self.sales_table.delete(*self.sales_table.get_children())
            
            total_amount = 0
            total_discount = 0
            total_net_pay = 0
            
            for row in rows:
                self.sales_table.insert('', END, values=(
                    f"Month {row[0]}",
                    row[0],
                    "All Customers",
                    row[1],
                    row[2],
                    row[3]
                ))
                total_amount += row[1]
                total_discount += row[2]
                total_net_pay += row[3]
            
            # Update summary and chart
            self.lbl_total_value.config(text=f"Rs. {total_amount:.2f}")
            self.lbl_total_discount_value.config(text=f"Rs. {total_discount:.2f}")
            self.lbl_net_pay_value.config(text=f"Rs. {total_net_pay:.2f}")
            self.update_chart(f"Year {year}", total_amount, total_discount, total_net_pay)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def show_custom_report(self):
        date_from = self.var_date_from.get()
        date_to = self.var_date_to.get()
        
        try:
            sql_from = datetime.strptime(date_from, "%d-%m-%Y").strftime("%Y-%m-%d")
            sql_to = datetime.strptime(date_to, "%d-%m-%Y").strftime("%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use DD-MM-YYYY", parent=self.root)
            return
        
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        
        try:
            # For short date ranges (<= 7 days), show detailed transactions
            days_diff = (datetime.strptime(sql_to, "%Y-%m-%d") - 
                        datetime.strptime(sql_from, "%Y-%m-%d")).days
            
            if days_diff <= 7:
                cur.execute("""
                    SELECT invoice, date, customer_name, subtotal, discount, total 
                    FROM sales 
                    WHERE date BETWEEN ? AND ?
                    ORDER BY date, time
                """, (sql_from, sql_to))
                
                rows = cur.fetchall()
                
                self.sales_table.delete(*self.sales_table.get_children())
                
                total_amount = 0
                total_discount = 0
                total_net_pay = 0
                
                for row in rows:
                    self.sales_table.insert('', END, values=row)
                    total_amount += row[3]
                    total_discount += row[4]
                    total_net_pay += row[5]
            else:
                # For longer ranges, show daily summaries
                cur.execute("""
                    SELECT 
                        date,
                        SUM(subtotal) as day_total,
                        SUM(discount) as day_discount,
                        SUM(total) as day_net
                    FROM sales
                    WHERE date BETWEEN ? AND ?
                    GROUP BY date
                    ORDER BY date
                """, (sql_from, sql_to))
                
                rows = cur.fetchall()
                
                self.sales_table.delete(*self.sales_table.get_children())
                
                total_amount = 0
                total_discount = 0
                total_net_pay = 0
                
                for row in rows:
                    self.sales_table.insert('', END, values=(
                        f"Day {row[0]}",
                        row[0],
                        "All Customers",
                        row[1],
                        row[2],
                        row[3]
                    ))
                    total_amount += row[1]
                    total_discount += row[2]
                    total_net_pay += row[3]
            
            # Update summary and chart
            self.lbl_total_value.config(text=f"Rs. {total_amount:.2f}")
            self.lbl_total_discount_value.config(text=f"Rs. {total_discount:.2f}")
            self.lbl_net_pay_value.config(text=f"Rs. {total_net_pay:.2f}")
            self.update_chart(f"{date_from} to {date_to}", total_amount, total_discount, total_net_pay)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def update_chart(self, title, total_amount, total_discount, total_net_pay):
        """Update the chart with the current data"""
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Create figure and axis
        fig, ax = plt.subplots(figsize=(5.7, 3.3), dpi=100)
        fig.patch.set_facecolor('white')
        
        # Data for plotting
        categories = ['Total Sales', 'Discount', 'Net Pay']
        values = [total_amount, total_discount, total_net_pay]
        
        # Create bar chart
        bars = ax.bar(categories, values, color=['#4CAF50', '#F44336', '#2196F3'])
        
        # Add value labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'Rs. {height:.2f}',
                    ha='center', va='bottom')
        
        # Set title and labels
        ax.set_title(f'Sales Summary: {title}')
        ax.set_ylabel('Amount (Rs.)')
        
        # Create canvas and add to frame
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    def export_to_excel(self):
        """Export the current report data to Excel"""
        try:
            # Get all data from the treeview
            data = []
            for item in self.sales_table.get_children():
                values = self.sales_table.item(item, 'values')
                data.append(values)
            
            if not data:
                messagebox.showwarning("Warning", "No data to export", parent=self.root)
                return
            
            # Create DataFrame
            df = pd.DataFrame(data, columns=["Invoice", "Date", "Customer", "Amount", "Discount", "Net Pay"])
            
            # Get file path to save
            file_path = os.path.join(os.getcwd(), "sales_report.xlsx")
            
            # Write to Excel
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", f"Data exported to {file_path}", parent=self.root)
            
        except Exception as ex:
            messagebox.showerror("Error", f"Error exporting to Excel: {str(ex)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = SalesReportClass(root)
    root.mainloop()