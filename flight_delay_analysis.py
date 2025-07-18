# Import the tools 
import pandas as pd
import matplotlib.pyplot as plt 

#load the data
#Put csv file in a folder called input
file_name = 'input/On_Time_Marketing_Carrier_On_Time_Performance_(Beginning_January_2018)_2025_1.csv'
data = pd.read_csv(file_name, low_memory=False)

#make columns lowercase so i don't worry about capital letters
data.columns = [c.lower() for c in data.columns]
 
#delay columns to analyze
delay_cols = [
    'depdelay',
    'carrierdelay',
    'weatherdelay',
    'nasdelay',
    'securitydelay',
    'lateaircraftdelay'
]
# keep only the delay columns that actually exisst
existing_delay_cols = [col for col in delay_cols if col in data.columns]

#clean delay columns 
for col in existing_delay_cols:
    data[col] = data[col]. fillna(0)  
    data[col] = data[col].astype(int)
# overall delay summary
total_flights = len(data)
delayed_flights = (data['depdelay'] > 0).sum() if 'depdelay' in data.columns else 0
delayed_percent = round(delayed_flights / total_flights * 100, 1)

print(f"Total flights: {total_flights}")
print(f"Flights delayed: {delayed_flights} ({delayed_percent}%)")

# count number of fligts with each delay type
delay_counts = {}
for col in existing_delay_cols:
    if col == "depdelay":
        delay_counts[col] = delayed_flights
        continue
    delay_counts [col] = (data[col] > 0).sum()

print("Delay by reason:")
for k, v in delay_counts.items():
    print(f"{k}: {v}")

#bar chart of delay reasons
if delay_counts:
    reasons = list(delay_counts.keys())
    counts = [delay_counts[r] for r in reasons]

    plt.bar(reasons,counts)
    plt.title("Number of Flihts by Delay Reason- Israel Munguia")
    plt.ylabel("Count of Flights")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()
