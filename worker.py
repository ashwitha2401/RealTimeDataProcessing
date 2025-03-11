import json
from kafka import KafkaConsumer
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import time
from datetime import datetime

#Kafka configuration
KAFKA_BROKER = 'localhost:9092' #Address of the Kafka broker
TOPIC_NAME = 'color_data' #Kafka topic is to come from 

#Here Initialize Kafka consumer
consumer = KafkaConsumer(TOPIC_NAME,bootstrap_servers=KAFKA_BROKER,value_deserializer=lambda v: json.loads(v.decode('utf-8')))

#InfluxDB connection details
url = "http://localhost:8086"
token = "GdhCs0W87zhB1rxKAnnLb54RN3T9VTeQ6FcAOPqplJRHEXUo1X-Pde4zbymS0-DfL4eg23JlKj04IFAssztEXw=="  # Replace with your token
org = "Linq" # Replace with your organization
bucket = "realtime_data" # Replace with your bucket

#Here Initializing the client
client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

def process_message(message):
    """Process the message and store aggregated data in InfluxDB."""
    color = message['color']
    value = message['value']

    #Creating InfluxDB data point
    data= {"measurement": "color_metrics", "color": color, "value": value}
    point = Point(data["measurement"]) .tag("color", data["color"]) .field("value", data["value"]) .time(datetime.utcnow(), WritePrecision.NS)

    #sending data to the InfluxDB
    try:
        write_api.write(bucket=bucket, org=org, record=point)
        print(f"Writing Message from Data Generator -> InfluxDB: {point.to_line_protocol()}")
    except Exception as e:
        print(f"Failed to write data: {e}")
    #For every iteration 
    time.sleep(10)

def consume_messages():
    """Consume messages from Kafka and process them."""
    for message in consumer:
        process_message(message.value)

if __name__ == "__main__":
    consume_messages()