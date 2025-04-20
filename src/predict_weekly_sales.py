import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np
from datetime import datetime, timedelta

# Connect to the database
conn = sqlite3.connect('ims.db')

# Fetch historical daily sales data
query = "SELECT date, total_sales FROM daily_sales_summary"
df = pd.read_sql(query, conn)

# Convert date to datetime and sort
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by='date')

# Create numeric features for regression
df['day_number'] = (df['date'] - df['date'].min()).dt.days
X = df[['day_number']]
y = df['total_sales']

# Train linear regression model
model = LinearRegression()
model.fit(X, y)

# Predict sales for the next 7 days
last_day = df['day_number'].max()
future_days = np.array([last_day + i for i in range(1, 8)]).reshape(-1, 1)
predictions = model.predict(future_days)

# Display predictions
future_dates = [df['date'].max() + timedelta(days=i) for i in range(1, 8)]
prediction_df = pd.DataFrame({'date': future_dates, 'predicted_sales': predictions})
print(prediction_df)

# Optional: Plot results
plt.figure(figsize=(10, 5))
plt.plot(df['date'], y, label='Actual Sales')
plt.plot(prediction_df['date'], prediction_df['predicted_sales'], label='Predicted Sales', linestyle='--', marker='o')
plt.xlabel('Date')
plt.ylabel('Sales')
plt.title('Sales Prediction for Next 7 Days')
plt.legend()
plt.tight_layout()
plt.show()
