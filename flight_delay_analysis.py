# Import the tools
import pandas as pd
import matplotlib.pyplot as plt
plt.close('all')  # Close any old plots


# Load the CSV file from the input folder
file_name = 'input/Airline_Delay_Cause.csv'
data = pd.read_csv(file_name, low_memory=False)


# Make all column names lowercase so I don’t have to worry about capital letters
data.columns = [c.lower().strip() for c in data.columns]


# Only keep data from January 2024 to April 2025
data = data[(data['year'] == 2024) | ((data['year'] == 2025) & (data['month'] <= 4))]


# List of delay columns to analyze
delay_cols = [
   'carrier_delay',
   'weather_delay',
   'nas_delay',
   'security_delay',
   'late_aircraft_delay'
]
# Only use delay columns that actually exist in the file
existing_delay_cols = [col for col in delay_cols if col in data.columns]


# Clean delay columns (fill missing values with 0 and make sure they’re integers)
for col in existing_delay_cols:
   data[col] = data[col].fillna(0).astype(int)


# Use carrier_name if it exists; otherwise fallback to carrier code
if 'carrier_name' in data.columns:
   data['airline_name'] = data['carrier_name']
else:
   data['airline_name'] = data['carrier']


# Total flights and delays
total_flights = data['arr_flights'].sum()
delayed_flights = data['arr_del15'].sum()
delayed_percent = round(delayed_flights / total_flights * 100, 1) if total_flights else 0


print(f"Total flights (Jan 2024 to Apr 2025): {int(total_flights):,}")
print(f"Flights delayed: {int(delayed_flights):,} ({delayed_percent}%)")


# Total delays by reason
delay_counts = {}
print("\nDelay by reason (Jan 2024 to Apr 2025):")
for col in existing_delay_cols:
   count = data[col].sum()
   delay_counts[col] = int(count)
   print(f"{col}: {int(count):,}")

# Bar chart of delay causes
delay_reason_labels = {
   'carrier_delay': 'Airline Delay',
   'weather_delay': 'Weather Delay',
   'nas_delay': 'Air Traffic Delay',
   'security_delay': 'Security Delay',
   'late_aircraft_delay': 'Late Aircraft Delay'
}

if delay_counts:
   sorted_keys = sorted(delay_counts, key=delay_counts.get, reverse=True)
   labels = [delay_reason_labels.get(k, k) for k in sorted_keys]
   values = [delay_counts[k] for k in sorted_keys]


   fig, ax = plt.subplots(figsize=(8, 4.5))
   bars = ax.bar(labels, values)


   ax.set_title("Flight Delay Causes (Jan 2024 to Apr 2025)")
   ax.set_xlabel("Delay Cause")
   ax.set_ylabel("Number of Delayed Flights")
   ax.set_xticks(range(len(labels)))
   ax.set_xticklabels(labels, rotation=25, ha="right")


# Add numbers above each bar
   for b, count in zip(bars, values):
       height = b.get_height()
       ax.text(b.get_x() + b.get_width()/2, height, f"{int(height):,}", ha="center", va="bottom", fontsize=9)


   ax.yaxis.grid(True, linestyle="--", alpha=0.4)
   ax.set_axisbelow(True)


   fig.tight_layout()
   plt.show()
else:
   print("No delay causes to plot.")


# Total and delayed flights by airline
if 'airline_name' in data.columns:
   total_by_airline = data.groupby('airline_name')['arr_flights'].sum().sort_values(ascending=False)
   delayed_by_airline = data.groupby('airline_name')['arr_del15'].sum().sort_values(ascending=False)


   print("\nTotal flights by airline (Jan 2024 to Apr 2025):")
   for name, count in total_by_airline.items():
       print(f"{name}: {int(count):,}")


   print("\nDelayed flights by airline (Jan 2024 to Apr 2025):")
   for name, count in delayed_by_airline.items():
       percent = round(count / total_flights * 100, 2) if total_flights else 0
       print(f"{name}: {int(count):,} ({percent}%)")


# Bar chart of delayed flights by airline
   fig, ax = plt.subplots(figsize=(14, 6))
   bars = ax.bar(delayed_by_airline.index, delayed_by_airline.values)

   ax.set_title("Delayed Flights per Airline (Jan 2024 - Apr 2025)")
   ax.set_xlabel("Airline")
   ax.set_ylabel("Number of Delayed Flights")
   ax.set_xticks(range(len(delayed_by_airline.index)))
   ax.set_xticklabels(delayed_by_airline.index, rotation=45, ha='right')

   for b, name in zip(bars, delayed_by_airline.index):
       height = b.get_height()
       percent = round(height / total_flights * 100, 2) if total_flights else 0
       ax.text(b.get_x() + b.get_width()/2, height, f"{int(height):,}\n({percent}%)", ha="center", va="bottom", fontsize=9)

   fig.tight_layout()
   plt.show()
else:
   print("Missing 'airline_name' column.")