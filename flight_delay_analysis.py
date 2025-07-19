# Import the tools 
import pandas as pd
import matplotlib.pyplot as plt 
plt.close('all') 


#Put csv file in a folder called input
file_name = 'input/On_Time_Marketing_Carrier_On_Time_Performance_(Beginning_January_2018)_2025_1.csv'
data = pd.read_csv(file_name, low_memory=False)

#make columns lowercase so i don't worry about capital letters
data.columns = [c.lower() for c in data.columns]
 
if "crsdeptime" in data.columns:
    crs_raw = pd.to_numeric(data["crsdeptime"], errors="coerce").fillna(0).astype(int)
    crs_str = crs_raw.astype(str).str.zfill(4)
    data["hour"] = crs_str.str[:2].astype(int).clip(0, 23)
    data["minute"] = crs_str.str[2:].astype(int).clip(0, 59)
    data["hhmm_label"] = (
        data["hour"].astype(str).str.zfill(2)
        + ":" +
        data["minute"].astype(str).str.zfill(2)
    )
#delay columns to analyze
delay_cols = [
    'depdelay',
    'carrierdelay',
    'weatherdelay',
    'nasdelay',
    'securitydelay',
    'lateaircraftdelay'
]
# keep only the delay columns that actually exist
existing_delay_cols = [col for col in delay_cols if col in data.columns]

#clean delay columns 
for col in existing_delay_cols:
    data[col] = data[col].fillna(0)  
    data[col] = data[col].astype(int)
# overall delay summary
total_flights = len(data)
delayed_flights = (data['depdelay'] > 0).sum() if 'depdelay' in data.columns else 0
delayed_percent = round(delayed_flights / total_flights * 100, 1)

print(f"Total flights: {total_flights}")
print(f"Flights delayed: {delayed_flights} ({delayed_percent}%)")

# count number of flights with each delay type
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
    plot_counts = {k: v for k, v in delay_counts.items() if k != 'depdelay'}
    if plot_counts:
        reasons = sorted(plot_counts, key=lambda k: plot_counts[k], reverse=True)
        counts = [plot_counts[r] for r in reasons]

        fig, ax = plt.subplots(figsize=(8, 4.5))
        bars = ax.bar(reasons, counts)

        ax.set_title("Flights with Each Delay Cause")
        ax.set_ylabel("Flight Count")
        ax.set_xlabel("Delay Cause")
        ax.set_xticklabels(reasons, rotation=25, ha="right")

        for b in bars:
            h = b.get_height()
            ax.text(b.get_x() + b.get_width()/2, h, f"{h:,}", ha="center", va="bottom", fontsize=9)

        ax.yaxis.grid(True, linestyle="--", alpha=0.4)
        ax.set_axisbelow(True)

        fig.tight_layout()
        plt.show()
    else:
        print("No specific delay causes to plot.")


#Heatmap: average departure delay by hour and weekday
if "depdelay" in data.columns and "crsdeptime" in data.columns and "dayofweek" in data.columns:
    show_cell_numbers = True
    
    data["crsdeptime"] = pd.to_numeric(data["crsdeptime"], errors="coerce").fillna(0).astype(int)
    data["weekday"] = pd.to_numeric(data["dayofweek"], errors="coerce").fillna(0).astype(int)

    pivot = data.pivot_table(
        index="hour",
        columns="weekday",
        values="depdelay",
        aggfunc="mean",
        fill_value=0
    )

    pivot = pivot.reindex(range(24), fill_value=0)
    pivot = pivot.reindex(columns=[1, 2, 3, 4, 5, 6, 7], fill_value=0)

    fig, ax = plt.subplots(figsize=(8,6))
    img = ax.imshow(pivot.values , origin="lower", aspect="auto", cmap="viridis")

    cbar = fig.colorbar(img, ax=ax)
    cbar.set_label("Avg Dep Delay (min)", rotation=270, labelpad=20)

    ax.set_title("Average Departure Delay by Hour & Weekday")
    ax.set_xlabel("Weekday (1=Mon ... 7=Sun)")
    ax.set_ylabel("Hour of Day (0–23)")
    ax.set_xticks(range(7))
    ax.set_xticklabels([1, 2, 3, 4, 5, 6, 7])
    ax.set_yticks(range(24))
    ax.set_yticklabels(range(24))

    if show_cell_numbers:
        mid = (pivot.values.max() + pivot.values.min()) / 2  # midpoint for contrast
        for i, hour in enumerate(pivot.index):
            for j, wd in enumerate(pivot.columns):
                val = pivot.iloc[i, j]
                # Show all values (change to: if val > 0:  to hide zeros)
                color = "white" if val >= mid else "black"
                ax.text(j, i, f"{val:.0f}", ha="center", va="center",
                        fontsize=8, color=color)
    fig.tight_layout()
    
    plt.show()
    plt.close(fig)

else:
    print("\nSkipping heatmap (missing one of: depdelay, crsdeptime, dayofweek)")
