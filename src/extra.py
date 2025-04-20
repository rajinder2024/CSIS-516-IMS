import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Fetch data from SQLite database
def fetch_sales_data():
    con = sqlite3.connect("ims.db")
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

# Create a reusable bar chart function
def create_chart(title, x, y, xlabel, ylabel, color):
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
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.5, f'{height:.2f}', ha='center', fontsize=8)

    return fig

# Draw separator
def add_separator(parent):
    ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=10, pady=10)

# Display everything in GUI
def display_report():
    total, discount, daily_sales, monthly_sales, top_products, avg = fetch_sales_data()

    for widget in left_frame.winfo_children():
        widget.destroy()
    for widget in right_frame.winfo_children():
        widget.destroy()

    style = ttk.Style()
    style.configure("Card.TFrame", background="#f0f4f7", borderwidth=1, relief="ridge")
    style.configure("Title.TLabel", font=("Helvetica", 14, "bold"))
    style.configure("Text.TLabel", font=("Helvetica", 11))

    # --- Summary Cards ---
    summary_frame = ttk.Frame(left_frame)
    summary_frame.pack(pady=10, padx=10, fill='x')

    def make_card(label, value):
        card = ttk.Frame(summary_frame, style="Card.TFrame", padding=10)
        ttk.Label(card, text=label, style="Title.TLabel").pack(anchor='w')
        ttk.Label(card, text=value, style="Text.TLabel").pack(anchor='w')
        return card

    make_card("Total Sales", f"Rs.{total:.2f}").pack(side="left", expand=True, fill="both", padx=5)
    make_card("Total Discount", f"Rs.{discount:.2f}").pack(side="left", expand=True, fill="both", padx=5)
    make_card("Average Sale Value", f"Rs.{avg:.2f}").pack(side="left", expand=True, fill="both", padx=5)

    add_separator(left_frame)

    # --- Daily Sales Summary ---
    ttk.Label(left_frame, text="Daily Sales (Last 7 Days)", style="Title.TLabel").pack(anchor="w", padx=10)
    for row in daily_sales:
        ttk.Label(left_frame, text=f"{row[0]} - Transactions: {row[1]}, Sales: Rs.{row[2]:.2f}", style="Text.TLabel").pack(anchor='w', padx=20)

    add_separator(left_frame)

    # --- Monthly Sales Summary ---
    ttk.Label(left_frame, text="Monthly Sales Summary (This Year)", style="Title.TLabel").pack(anchor="w", padx=10)
    for row in monthly_sales:
        ttk.Label(left_frame, text=f"{row[0]} - Transactions: {row[1]}, Sales: Rs.{row[2]:.2f}", style="Text.TLabel").pack(anchor='w', padx=20)

    add_separator(left_frame)

    # --- Top Products ---
    ttk.Label(left_frame, text="Top 5 Selling Products", style="Title.TLabel").pack(anchor="w", padx=10)
    for row in top_products:
        ttk.Label(left_frame, text=f"{row[0]} - Sold: {row[1]} units - Sales: Rs.{row[2]:.2f}", style="Text.TLabel").pack(anchor='w', padx=20)

    # --- Chart Tabs ---
    notebook = ttk.Notebook(right_frame)
    notebook.pack(fill='both', expand=True)

    # Chart 1: Daily Sales
    tab1 = ttk.Frame(notebook)
    dates = [row[0] for row in reversed(daily_sales)]
    sales = [row[2] for row in reversed(daily_sales)]
    fig1 = create_chart("Daily Sales (Last 7 Days)", dates, sales, "Date", "Sales (Rs.)", "#4a90e2")
    canvas1 = FigureCanvasTkAgg(fig1, tab1)
    canvas1.get_tk_widget().pack(fill='both', expand=True)
    canvas1.draw()
    notebook.add(tab1, text=" Daily")

    # Chart 2: Monthly Sales
    tab2 = ttk.Frame(notebook)
    months = [row[0] for row in reversed(monthly_sales)]
    monthly_totals = [row[2] for row in reversed(monthly_sales)]
    fig2 = create_chart(" Monthly Sales (This Year)", months, monthly_totals, "Month", "Sales (Rs.) ", "#50c878")
    canvas2 = FigureCanvasTkAgg(fig2, tab2)
    canvas2.get_tk_widget().pack(fill='both', expand=True)
    canvas2.draw()
    notebook.add(tab2, text="Monthly")

    # Chart 3: Top Products
    tab3 = ttk.Frame(notebook)
    products = [row[0] for row in top_products]
    units = [row[1] for row in top_products]
    fig3 = create_chart(" Top 5 Products (Units Sold)", products, units, "Product", "Units", "#e94e77")
    canvas3 = FigureCanvasTkAgg(fig3, tab3)
    canvas3.get_tk_widget().pack(fill='both', expand=True)
    canvas3.draw()
    notebook.add(tab3, text=" Top Products")


# --- Main Window Setup ---
root = tk.Tk()
root.title("📈 Sales Report Dashboard")
root.geometry("1150x800")
root.configure(bg="#e6ecf0")

# --- Main Container ---
main_container = ttk.Frame(root)
main_container.pack(fill="both", expand=True, padx=10, pady=10)

# --- Left and Right Frames ---
left_frame = ttk.Frame(main_container)
left_frame.pack(side="left", fill="both", expand=True)

right_frame = ttk.Frame(main_container)
right_frame.pack(side="right", fill="both", expand=True)

# Display report
display_report()

# Run app
root.mainloop()
