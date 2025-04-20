import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SalesReportClass:
    def __init__(self, parent_frame, db_path="ims.db"):
        self.parent = parent_frame
        self.db_path = db_path
        self.style = ttk.Style()
        self.setup_styles()
        self.create_widgets()
        self.display_report()

    def setup_styles(self):
        self.style.configure("Card.TFrame", background="#f0f4f7", borderwidth=1, relief="ridge")
        self.style.configure("Title.TLabel", font=("Helvetica", 14, "bold"))
        self.style.configure("Text.TLabel", font=("Helvetica", 11))

    def create_widgets(self):
        # Main container
        self.main_container = ttk.Frame(self.parent)
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Left and right frames
        self.left_frame = ttk.Frame(self.main_container)
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.right_frame = ttk.Frame(self.main_container)
        self.right_frame.pack(side="right", fill="both", expand=True)

        # Refresh button
        self.refresh_btn = ttk.Button(
            self.parent, 
            text="🔄 Refresh Report", 
            command=self.display_report
        )
        self.refresh_btn.pack(side="bottom", pady=5)

    def fetch_sales_data(self):
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()

        cur.execute("SELECT SUM(total), SUM(discount) FROM sales")
        total, discount = cur.fetchone()

        cur.execute("""
            SELECT date, COUNT(invoice), SUM(total)
            FROM sales
            GROUP BY date
            ORDER BY date DESC
            LIMIT 7
        """)
        daily_sales = cur.fetchall()

        cur.execute("""
            SELECT strftime('%Y-%m', date), COUNT(invoice), SUM(total)
            FROM sales
            WHERE strftime('%Y', date) = ?
            GROUP BY 1
            ORDER BY 1 DESC
        """, (datetime.now().strftime("%Y"),))
        monthly_sales = cur.fetchall()

        cur.execute("""
            SELECT product_name, SUM(quantity), SUM(total)
            FROM sales_items
            GROUP BY product_id
            ORDER BY SUM(quantity) DESC
            LIMIT 5
        """)
        top_products = cur.fetchall()

        cur.execute("SELECT AVG(total) FROM sales")
        avg = cur.fetchone()[0]

        con.close()
        return total, discount, daily_sales, monthly_sales, top_products, avg

    def create_chart(self, title, x, y, xlabel, ylabel, color):
        fig, ax = plt.subplots(figsize=(6, 3))
        bars = ax.bar(x, y, color=color)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_xticks(range(len(x)))
        ax.set_xticklabels(x, rotation=45)
        ax.grid(True, axis='y', linestyle='--', alpha=0.5)

        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, 
                    f'{height:.2f}', ha='center', fontsize=8)

        return fig

    def add_separator(self, parent):
        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=10, pady=10)

    def make_card(self, parent, label, value):
        card = ttk.Frame(parent, style="Card.TFrame", padding=10)
        ttk.Label(card, text=label, style="Title.TLabel").pack(anchor='w')
        ttk.Label(card, text=value, style="Text.TLabel").pack(anchor='w')
        return card

    def display_report(self):
        total, discount, daily_sales, monthly_sales, top_products, avg = self.fetch_sales_data()

        # Clear previous content
        for widget in self.left_frame.winfo_children():
            widget.destroy()
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        # --- Summary Cards ---
        summary_frame = ttk.Frame(self.left_frame)
        summary_frame.pack(pady=10, padx=10, fill='x')

        self.make_card(summary_frame, "Total Sales", f"Rs.{total:.2f}").pack(side="left", expand=True, fill="both", padx=5)
        self.make_card(summary_frame, "Total Discount", f"Rs.{discount:.2f}").pack(side="left", expand=True, fill="both", padx=5)
        self.make_card(summary_frame, "Average Sale Value", f"Rs.{avg:.2f}").pack(side="left", expand=True, fill="both", padx=5)

        self.add_separator(self.left_frame)

        # --- Daily Sales Summary ---
        ttk.Label(self.left_frame, text="Daily Sales (Last 7 Days)", style="Title.TLabel").pack(anchor="w", padx=10)
        for row in daily_sales:
            ttk.Label(self.left_frame, 
                     text=f"{row[0]} - Transactions: {row[1]}, Sales: Rs.{row[2]:.2f}", 
                     style="Text.TLabel").pack(anchor='w', padx=20)

        self.add_separator(self.left_frame)

        # --- Monthly Sales Summary ---
        ttk.Label(self.left_frame, text="Monthly Sales Summary (This Year)", style="Title.TLabel").pack(anchor="w", padx=10)
        for row in monthly_sales:
            ttk.Label(self.left_frame, 
                     text=f"{row[0]} - Transactions: {row[1]}, Sales: Rs.{row[2]:.2f}", 
                     style="Text.TLabel").pack(anchor='w', padx=20)

        self.add_separator(self.left_frame)

        # --- Top Products ---
        ttk.Label(self.left_frame, text="Top 5 Selling Products", style="Title.TLabel").pack(anchor="w", padx=10)
        for row in top_products:
            ttk.Label(self.left_frame, 
                     text=f"{row[0]} - Sold: {row[1]} units - Sales: Rs.{row[2]:.2f}", 
                     style="Text.TLabel").pack(anchor='w', padx=20)

        # --- Chart Tabs ---
        notebook = ttk.Notebook(self.right_frame)
        notebook.pack(fill='both', expand=True)

        # Chart 1: Daily Sales
        tab1 = ttk.Frame(notebook)
        dates = [row[0] for row in reversed(daily_sales)]
        sales = [row[2] for row in reversed(daily_sales)]
        fig1 = self.create_chart("Daily Sales (Last 7 Days)", dates, sales, "Date", "Sales (Rs.)", "#4a90e2")
        canvas1 = FigureCanvasTkAgg(fig1, tab1)
        canvas1.get_tk_widget().pack(fill='both', expand=True)
        canvas1.draw()
        notebook.add(tab1, text=" Daily")

        # Chart 2: Monthly Sales
        tab2 = ttk.Frame(notebook)
        months = [row[0] for row in reversed(monthly_sales)]
        monthly_totals = [row[2] for row in reversed(monthly_sales)]
        fig2 = self.create_chart(" Monthly Sales (This Year)", months, monthly_totals, "Month", "Sales (Rs.) ", "#50c878")
        canvas2 = FigureCanvasTkAgg(fig2, tab2)
        canvas2.get_tk_widget().pack(fill='both', expand=True)
        canvas2.draw()
        notebook.add(tab2, text="Monthly")

        # Chart 3: Top Products
        tab3 = ttk.Frame(notebook)
        products = [row[0] for row in top_products]
        units = [row[1] for row in top_products]
        fig3 = self.create_chart(" Top 5 Products (Units Sold)", products, units, "Product", "Units", "#e94e77")
        canvas3 = FigureCanvasTkAgg(fig3, tab3)
        canvas3.get_tk_widget().pack(fill='both', expand=True)
        canvas3.draw()
        notebook.add(tab3, text=" Top Products")


# Example usage in your dashboard:
if __name__ == "__main__":
    root = tk.Tk()
    root.title("📈 Sales Report Dashboard")
    root.geometry("1150x800")
    root.configure(bg="#e6ecf0")
    
    # Create the sales report in your dashboard
    sales_report = SalesReportClass(root)
    
    root.mainloop()