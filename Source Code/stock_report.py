from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import os
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from tkinter import filedialog

class StockReportClass:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1100x500+220+130")
        self.root.title("Stock Reports | Inventory Management System")
        self.root.config(bg="white")
        self.root.focus_force()
        
        # Variables
        self.var_search_by = StringVar()
        self.var_search_txt = StringVar()
        self.var_category = StringVar()
        self.var_status = StringVar()
        
        # Title
        title = Label(
            self.root, 
            text="Stock Inventory Reports",
            font=("goudy old style", 30),
            bg="#184a45",
            fg="white",
            bd=3,
            relief=RIDGE
        ).pack(side=TOP, fill=X, padx=10, pady=20)
        
        # Search Frame
        search_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        search_frame.place(x=10, y=70, width=1080, height=80)
        
        # Search Options
        lbl_search = Label(search_frame, text="Search By:", font=("times new roman", 15), bg="white")
        lbl_search.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        cmb_search = ttk.Combobox(
            search_frame,
            textvariable=self.var_search_by,
            values=("Select", "Product Name", "Category", "Supplier", "Status", "Low Stock"),
            state="readonly",
            font=("times new roman", 12)
        )
        cmb_search.current(0)
        cmb_search.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        txt_search = Entry(
            search_frame,
            textvariable=self.var_search_txt,
            font=("times new roman", 12),
            bg="lightyellow"
        )
        txt_search.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        
        btn_search = Button(
            search_frame,
            text="Search",
            command=self.search_data,
            font=("times new roman", 12),
            bg="#4CAF50",
            fg="white",
            cursor="hand2"
        )
        btn_search.grid(row=0, column=3, padx=5, pady=5)
        
        btn_show_all = Button(
            search_frame,
            text="Show All",
            command=self.show_all_data,
            font=("times new roman", 12),
            bg="#607d8b",
            fg="white",
            cursor="hand2"
        )
        btn_show_all.grid(row=0, column=4, padx=5, pady=5)
        
        # Filter by Category
        lbl_category = Label(search_frame, text="Category:", font=("times new roman", 15), bg="white")
        lbl_category.grid(row=0, column=5, padx=10, pady=5, sticky="e")
        
        cmb_category = ttk.Combobox(
            search_frame,
            textvariable=self.var_category,
            values=self.get_categories(),
            state="readonly",
            font=("times new roman", 12)
        )
        cmb_category.grid(row=0, column=6, padx=5, pady=5, sticky="w")
        cmb_category.set("All Categories")
        
        # Filter by Status
        lbl_status = Label(search_frame, text="Status:", font=("times new roman", 15), bg="white")
        lbl_status.grid(row=0, column=7, padx=10, pady=5, sticky="e")
        
        cmb_status = ttk.Combobox(
            search_frame,
            textvariable=self.var_status,
            values=("All Status", "Active", "Inactive", "Low Stock"),
            state="readonly",
            font=("times new roman", 12)
        )
        cmb_status.grid(row=0, column=8, padx=5, pady=5, sticky="w")
        cmb_status.set("All Status")
        
        # Report Frame
        report_frame = Frame(self.root, bd=3, relief=RIDGE)
        report_frame.place(x=10, y=160, width=500, height=330)
        
        scroll_y = Scrollbar(report_frame, orient=VERTICAL)
        scroll_x = Scrollbar(report_frame, orient=HORIZONTAL)
        
        self.stock_table = ttk.Treeview(
            report_frame,
            columns=("pid", "name", "category", "supplier", "qty", "price", "status"),
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.stock_table.xview)
        scroll_y.config(command=self.stock_table.yview)
        
        self.stock_table.heading("pid", text="Product ID")
        self.stock_table.heading("name", text="Name")
        self.stock_table.heading("category", text="Category")
        self.stock_table.heading("supplier", text="Supplier")
        self.stock_table.heading("qty", text="Quantity")
        self.stock_table.heading("price", text="Price")
        self.stock_table.heading("status", text="Status")
        
        self.stock_table["show"] = "headings"
        
        self.stock_table.column("pid", width=80)
        self.stock_table.column("name", width=120)
        self.stock_table.column("category", width=100)
        self.stock_table.column("supplier", width=100)
        self.stock_table.column("qty", width=80)
        self.stock_table.column("price", width=80)
        self.stock_table.column("status", width=80)
        
        self.stock_table.pack(fill=BOTH, expand=1)
        self.stock_table.bind("<ButtonRelease-1>", self.get_data)
        
        # Chart Frame
        self.chart_frame = Frame(self.root, bd=3, relief=RIDGE, bg="white")
        self.chart_frame.place(x=520, y=160, width=570, height=330)
        
        # Button Frame
        btn_frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=10, y=500, width=1080, height=50)
        
        btn_export = Button(
            btn_frame,
            text="Export to Excel",
            command=self.export_to_excel,
            font=("times new roman", 12),
            bg="#2196F3",
            fg="white",
            cursor="hand2"
        )
        btn_export.pack(side=LEFT, padx=10)
        
        btn_print = Button(
            btn_frame,
            text="Print Report",
            command=self.print_report,
            font=("times new roman", 12),
            bg="#009688",
            fg="white",
            cursor="hand2"
        )
        btn_print.pack(side=LEFT, padx=10)
        
        btn_low_stock = Button(
            btn_frame,
            text="Low Stock Report",
            command=self.show_low_stock,
            font=("times new roman", 12),
            bg="#FF5722",
            fg="white",
            cursor="hand2"
        )
        btn_low_stock.pack(side=LEFT, padx=10)
        
        btn_category_analysis = Button(
            btn_frame,
            text="Category Analysis",
            command=self.show_category_analysis,
            font=("times new roman", 12),
            bg="#673AB7",
            fg="white",
            cursor="hand2"
        )
        btn_category_analysis.pack(side=LEFT, padx=10)
        
        # Load initial data
        self.show_all_data()
        self.update_chart()
    
    def get_categories(self):
        """Get all product categories from database"""
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        cur.execute("SELECT name FROM category")
        categories = ["All Categories"] + [row[0] for row in cur.fetchall()]
        con.close()
        return categories
    
    def show_all_data(self):
        """Show all stock data"""
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        try:
            cur.execute("""
                SELECT p.pid, p.name, p.Category, p.Supplier, p.qty, p.price, p.status 
                FROM product p
                ORDER BY p.name
            """)
            rows = cur.fetchall()
            self.stock_table.delete(*self.stock_table.get_children())
            for row in rows:
                self.stock_table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()
        self.update_chart()
    
    def search_data(self):
        """Search stock data based on criteria"""
        search_by = self.var_search_by.get()
        search_txt = self.var_search_txt.get()
        category = self.var_category.get()
        status = self.var_status.get()
        
        if search_by == "Select" and category == "All Categories" and status == "All Status":
            messagebox.showwarning("Warning", "Please select search criteria", parent=self.root)
            return
        
        con = sqlite3.connect(database=r'ims.db')
        cur = con.cursor()
        
        try:
            query = "SELECT p.pid, p.name, p.Category, p.Supplier, p.qty, p.price, p.status FROM product p WHERE 1=1"
            params = []
            
            if search_by == "Product Name" and search_txt:
                query += " AND p.name LIKE ?"
                params.append(f"%{search_txt}%")
            elif search_by == "Category" and search_txt:
                query += " AND p.Category LIKE ?"
                params.append(f"%{search_txt}%")
            elif search_by == "Supplier" and search_txt:
                query += " AND p.Supplier LIKE ?"
                params.append(f"%{search_txt}%")
            elif search_by == "Status" and search_txt:
                query += " AND p.status LIKE ?"
                params.append(f"%{search_txt}%")
            elif search_by == "Low Stock":
                query += " AND p.qty < 5 AND p.status='Active'"
            
            if category != "All Categories":
                query += " AND p.Category = ?"
                params.append(category)
            
            if status == "Active":
                query += " AND p.status = 'Active'"
            elif status == "Inactive":
                query += " AND p.status = 'Inactive'"
            elif status == "Low Stock":
                query += " AND p.qty < 5 AND p.status='Active'"
            
            query += " ORDER BY p.name"
            
            cur.execute(query, tuple(params))
            rows = cur.fetchall()
            
            self.stock_table.delete(*self.stock_table.get_children())
            for row in rows:
                self.stock_table.insert('', END, values=row)
                
            if not rows:
                messagebox.showinfo("Info", "No records found", parent=self.root)
                
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()
        self.update_chart()
    
    def show_low_stock(self):
        """Show products with low stock (quantity < 5)"""
        self.var_search_by.set("Low Stock")
        self.var_search_txt.set("")
        self.var_category.set("All Categories")
        self.var_status.set("All Status")
        self.search_data()
    
    def get_data(self, ev):
        """Get data from selected row"""
        f = self.stock_table.focus()
        content = self.stock_table.item(f)
        row = content['values']
        if row:
            self.var_search_txt.set(row[1])  # Product name
    
    def update_chart(self):
        """Update the stock analysis chart"""
        # Get data from table
        items = []
        for child in self.stock_table.get_children():
            items.append(self.stock_table.item(child)['values'])
        
        if not items:
            return
            
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
            
        # Create new chart
        fig = Figure(figsize=(5.5, 3.2), dpi=100)
        ax = fig.add_subplot(111)
        
        # Prepare data for chart
        df = pd.DataFrame(items, columns=["pid", "name", "category", "supplier", "qty", "price", "status"])
        df['qty'] = pd.to_numeric(df['qty'])
        df['price'] = pd.to_numeric(df['price'])
        
        # Chart 1: Stock by Category (Bar Chart)
        if len(df['category'].unique()) > 1:
            category_data = df.groupby('category')['qty'].sum().sort_values(ascending=False)
            ax.bar(category_data.index, category_data.values, color='#3498db')
            ax.set_title('Stock Quantity by Category')
            ax.set_ylabel('Total Quantity')
            ax.tick_params(axis='x', rotation=45)
            
            # Add value labels
            for i, v in enumerate(category_data.values):
                ax.text(i, v + 0.5, str(v), ha='center')
        else:
            # Chart 2: Stock Status (Pie Chart) if only one category
            status_counts = df['status'].value_counts()
            ax.pie(
                status_counts,
                labels=status_counts.index,
                autopct='%1.1f%%',
                colors=['#2ecc71', '#e74c3c', '#f39c12']
            )
            ax.set_title('Stock Status Distribution')
        
        # Embed chart in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=1)
    
    def show_category_analysis(self):
        """Show detailed category analysis"""
        # Get data from table
        items = []
        for child in self.stock_table.get_children():
            items.append(self.stock_table.item(child)['values'])
            
        if not items:
            return
            
        # Create analysis window
        analysis_win = Toplevel(self.root)
        analysis_win.title("Category Analysis")
        analysis_win.geometry("800x600")
        analysis_win.focus_force()
        
        # Create DataFrame
        df = pd.DataFrame(items, columns=["pid", "name", "category", "supplier", "qty", "price", "status"])
        df['qty'] = pd.to_numeric(df['qty'])
        df['price'] = pd.to_numeric(df['price'])
        df['value'] = df['qty'] * df['price']
        
        # Group by category
        category_data = df.groupby('category').agg({
            'qty': 'sum',
            'value': 'sum',
            'pid': 'count'
        }).rename(columns={'pid': 'product_count'})
        
        # Create frames
        top_frame = Frame(analysis_win)
        top_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        bottom_frame = Frame(analysis_win)
        bottom_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Table for category data
        scroll_y = Scrollbar(top_frame)
        scroll_x = Scrollbar(top_frame, orient=HORIZONTAL)
        
        tree = ttk.Treeview(
            top_frame,
            columns=("category", "products", "quantity", "value"),
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set
        )
        
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)
        
        tree.heading("category", text="Category")
        tree.heading("products", text="Products")
        tree.heading("quantity", text="Total Quantity")
        tree.heading("value", text="Total Value (Rs.)")
        
        tree.column("category", width=200)
        tree.column("products", width=100)
        tree.column("quantity", width=150)
        tree.column("value", width=150)
        
        for index, row in category_data.iterrows():
            tree.insert("", END, values=(
                index,
                row['product_count'],
                row['qty'],
                f"{row['value']:,.2f}"
            ))
        
        tree.pack(fill=BOTH, expand=True)
        
        # Chart in bottom frame
        fig = Figure(figsize=(7, 4), dpi=100)
        ax = fig.add_subplot(111)
        
        category_data['value'].plot(
            kind='pie',
            ax=ax,
            labels=category_data.index,
            autopct='%1.1f%%',
            colors=['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']
        )
        ax.set_title('Inventory Value by Category')
        
        canvas = FigureCanvasTkAgg(fig, master=bottom_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
    
    def export_to_excel(self):
        """Export stock data to Excel"""
        # Get data from table
        items = []
        for child in self.stock_table.get_children():
            items.append(self.stock_table.item(child)['values'])
            
        if not items:
            messagebox.showwarning("Warning", "No data to export", parent=self.root)
            return
            
        # Create DataFrame
        df = pd.DataFrame(items, columns=[
            "Product ID", "Name", "Category", "Supplier", "Quantity", "Price", "Status"
        ])
        
        # Get save path
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Save stock report as"
        )
        
        if file_path:
            try:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Report exported to {file_path}", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {str(e)}", parent=self.root)
    
    def print_report(self):
        """Print stock report"""
        # Get data from table
        items = []
        for child in self.stock_table.get_children():
            items.append(self.stock_table.item(child)['values'])
            
        if not items:
            messagebox.showwarning("Warning", "No data to print", parent=self.root)
            return
            
        # Create printable report
        report_win = Toplevel(self.root)
        report_win.title("Stock Report Print Preview")
        report_win.geometry("800x600")
        
        # Report header
        header = Frame(report_win)
        header.pack(fill=X, padx=10, pady=10)
        
        Label(
            header,
            text="STOCK INVENTORY REPORT",
            font=("Helvetica", 16, "bold")
        ).pack(side=TOP)
        
        Label(
            header,
            text=f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            font=("Helvetica", 10)
        ).pack(side=TOP)
        
        # Report content
        text = Text(
            report_win,
            font=("Courier New", 10),
            wrap=NONE
        )
        scroll_y = Scrollbar(report_win, orient=VERTICAL, command=text.yview)
        scroll_x = Scrollbar(report_win, orient=HORIZONTAL, command=text.xview)
        text.config(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.pack(side=BOTTOM, fill=X)
        text.pack(fill=BOTH, expand=True)
        
        # Format report
        text.insert(END, "\n")
        text.insert(END, f"{'ID':<8}{'Name':<30}{'Category':<20}{'Supplier':<20}{'Qty':<10}{'Price':<15}{'Status':<10}\n")
        text.insert(END, "-"*113 + "\n")
        
        for item in items:
            text.insert(END, f"{item[0]:<8}{item[1][:28]:<30}{item[2][:18]:<20}{item[3][:18]:<20}")
            text.insert(END, f"{item[4]:<10}{float(item[5]):<15.2f}{item[6]:<10}\n")
        
        # Print button
        btn_print = Button(
            report_win,
            text="Print",
            command=lambda: self.send_to_printer(text.get("1.0", END)),
            font=("Helvetica", 12),
            bg="#4CAF50",
            fg="white"
        )
        btn_print.pack(side=BOTTOM, pady=10)
    
    def send_to_printer(self, text):
        """Send report text to printer"""
        try:
            import tempfile
            tmp = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt')
            tmp.write(text)
            tmp.close()
            os.startfile(tmp.name, "print")
            messagebox.showinfo("Success", "Report sent to printer", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Printing failed: {str(e)}", parent=self.root)

if __name__ == "__main__":
    root = Tk()
    obj = StockReportClass(root)
    root.mainloop()
