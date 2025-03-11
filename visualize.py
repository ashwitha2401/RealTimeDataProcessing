import matplotlib.pyplot as plt
import pandas as pd
from influxdb_client import InfluxDBClient
from datetime import datetime

#InfluxDB connection details
url = "http://localhost:8086"  # Ensure this matches your InfluxDB URL
token = "GdhCs0W87zhB1rxKAnnLb54RN3T9VTeQ6FcAOPqplJRHEXUo1X-Pde4zbymS0-DfL4eg23JlKj04IFAssztEXw=="
org = "Linq"
bucket = "realtime_data"

#Initialize InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

#Query data
query = '''
from(bucket: "metrics")
  |> range(start: -1h)  #This Retrieves the ata from the last hour
  |> filter(fn: (r) => r["_measurement"] == "color_metrics")
  |> filter(fn: (r) => r["_field"] == "value")
  |> filter(fn: (r) => r["color"] == "blue" or r["color"] == "green" or r["color"] == "red" or r["color"] == "yellow")
  |> group(columns: ["color"])  #To Group the data by color
  |> aggregateWindow(every: 10m, fn: mean, createEmpty: false)  #Aggregate the values over 10-minute windows
  |> yield(name: "mean_values")  #To Output the aggregated data
'''

tables = query_api.query(query)

# Convert the results to Pandas DataFrame
data = []
for table in tables:
    for record in table.records:
        data.append((record.get_time(), record.get_value(), record.values.get("color")))  # Extract timestamp, value, and color

# Create DataFrame
df = pd.DataFrame(data, columns=["time", "value", "color"])
df["time"] = pd.to_datetime(df["time"])  # Convert to datetime format

# Close InfluxDB connection
client.close()

# Check if DataFrame is empty
if df.empty:
    print("No data found in InfluxDB!")
    exit()

color_map = {"red": "red", "blue": "blue", "green": "green", "yellow": "yellow"}

#Group data by color and plot
plt.figure(figsize=(12, 6))
plt.figure(figsize=(12, 6))

for color in df["color"].unique():
    subset = df[df["color"] == color]
    plt.plot(subset["time"], subset["value"], marker="o", linestyle="-", color=color_map.get(color, "black"), label=color)

#Formatting the plot
plt.xlabel("Time")
plt.ylabel("Value")
plt.title("Color Metrics Over Time")
plt.legend(title="Color Groups")
plt.xticks(rotation=45)
plt.grid(True)

#Show the plot
plt.show()