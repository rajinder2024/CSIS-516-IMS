import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np
from datetime import timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # goes one folder up from /src
db_path = os.path.join(base_dir, "ims.db")
conn = sqlite3.connect(db_path)


class SalesForecastClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Forecast")
        self.root.geometry("1100x500+220+130")
        self.root.config(bg="white")

        title = Label(self.root, text="Sales Forecasting Output", font=("times new roman", 20, "bold"), bg="white", fg="blue")
        title.pack(pady=20)

        # Show predictions directly in the main window
        self.show_predictions()

    def get_sales_prediction(self):
        # Connect to the database
        conn = sqlite3.connect(db_path)

        # Fetch historical daily sales data
        query = "SELECT date, total_sales FROM daily_sales_summary"
        df = pd.read_sql(query, conn)

        # Close connection
        conn.close()

        if df.empty:
            print("No sales data found.")
            return pd.DataFrame(), None

        # Convert date to datetime and sort
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date')

        # Create numeric feature
        df['day_number'] = (df['date'] - df['date'].min()).dt.days
        X = df[['day_number']]
        y = df['total_sales']

        # Train model
        model = LinearRegression()
        model.fit(X, y)

        # Predict next 7 days
        last_day = df['day_number'].max()
        future_days = np.array([last_day + i for i in range(1, 8)]).reshape(-1, 1)

        # Convert future_days to DataFrame with appropriate column name to match training data
        future_days_df = pd.DataFrame(future_days, columns=['day_number'])

        # Make predictions
        predictions = model.predict(future_days_df)

        # Prepare result
        future_dates = [df['date'].max() + timedelta(days=i) for i in range(1, 8)]
        prediction_df = pd.DataFrame({'date': future_dates, 'predicted_sales': predictions})
        prediction_df['predicted_sales'] = prediction_df['predicted_sales'].round(2)

        # Plot
        fig, ax = plt.subplots(figsize=(7, 3))
        ax.plot(df['date'], y, label='Actual Sales')
        ax.plot(prediction_df['date'], prediction_df['predicted_sales'], label='Predicted Sales', linestyle='--', marker='o')
        ax.set_xlabel('Date')
        ax.set_ylabel('Sales')
        ax.set_title('Sales Prediction for Next 7 Days')
        ax.legend()
        fig.tight_layout()

        return prediction_df, fig

    def show_predictions(self):
        prediction_df, fig = self.get_sales_prediction()

        if prediction_df.empty:
            messagebox.showerror("Error", "No sales data found in the database.")
            return

        # Display the table of predictions
        tree_frame = Frame(self.root)
        tree_frame.pack(pady=10)

        tree = ttk.Treeview(tree_frame)
        tree["columns"] = ("date", "predicted_sales")
        tree.column("#0", width=0, stretch=NO)
        tree.column("date", anchor=W, width=150)
        tree.column("predicted_sales", anchor=CENTER, width=120)

        tree.heading("#0", text="", anchor=W)
        tree.heading("date", text="Date", anchor=W)
        tree.heading("predicted_sales", text="Predicted Sales", anchor=CENTER)

        for i, row in prediction_df.iterrows():
            tree.insert("", END, values=(row['date'].strftime('%Y-%m-%d'), row['predicted_sales']))

        tree.pack()

        # Display 
        if fig:
            canvas = FigureCanvasTkAgg(fig, master=self.root)  
            canvas.draw()
            canvas.get_tk_widget().pack(pady=10)


if __name__ == "__main__":
    root = Tk()
    app = SalesForecastClass(root)

    root.mainloop()
