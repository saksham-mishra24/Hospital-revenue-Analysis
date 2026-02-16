import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/ecommerce.csv")

# Convert time column
df['event_time'] = pd.to_datetime(df['event_time'])

# Extract hour
df['hour'] = df['event_time'].dt.hour

# Peak visit time
peak_time = df['hour'].value_counts().sort_index()

plt.figure()
peak_time.plot()
plt.title("Peak Visit Hours")
plt.xlabel("Hour")
plt.ylabel("Number of Visits")
plt.show()

# Conversion Rate
total_events = len(df)
purchase_events = len(df[df['event_type'] == 'purchase'])

conversion_rate = (purchase_events / total_events) * 100
print("Conversion Rate:", conversion_rate)
