import matplotlib.pyplot as plt
import pandas as pd
from influxdb_client import InfluxDBClient
from datetime import datetime

#InfluxDB connection details
url = "http://localhost:8086"  # Ensure this matches your InfluxDB URL
token="0dzVjCd_BCjRSrZJe86cTw7k4IoqYN9b47Mxv5ekjzeusoFMBTOthamr7zNtl5ZwPtV_oUtvA1KJq8ZX3n1g5A=="
#token = "GdhCs0W87zhB1rxKAnnLb54RN3T9VTeQ6FcAOPqplJRHEXUo1X-Pde4zbymS0-DfL4eg23JlKj04IFAssztEXw=="
org = "Linq"
bucket = "realtime_data"

#Initialize InfluxDB client
client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

#Query data
query = '''
from(bucket: "realtime_data")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "color_metrics")
  |> filter(fn: (r) => r["_field"] == "value")
  |> filter(fn: (r) => r["color"] == "blue" or r["color"] == "green" or r["color"] == "red" or r["color"] == "yellow")
  |> group(columns: ["color"])
  |> aggregateWindow(every: 1m, fn: mean, createEmpty: false)
  |> yield(name: "mean_values")
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
