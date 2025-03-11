Real-time Data Processing and Visualization

Overview
This project implements a real-time data pipeline consisting of three components:

1. Data Generator: Produces random messages containing a color name and a numerical value, then publishes them to a Kafka topic.
2. Worker: Consumes messages from Kafka, processes them, aggregates numerical values by color, and stores the results in InfluxDB.
3. Visualization Dashboard: Queries InfluxDB and visualizes the aggregated data over time using Matplotlib.

Technologies Used
- Python for scripting
- Kafka for real-time message streaming
- InfluxDB for time series data storage
- Matplotlib for data visualization
- Docker for containerization

Installation & Setup

1. Clone the Repository
git clone https://github.com/ashwitha2401/RealTimeDataProcessing.git
cd RealTimeDataProcessing

2. Start the Docker Containers
docker-compose up -d

3. Create Kafka Topic
Find the Kafka container ID: docker ps

Then, create the Kafka topic:
docker exec -it <container_id> kafka-topics --create --topic color_data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

4. Setup InfluxDB
1. Open InfluxDB UI at: [http://localhost:8086](http://localhost:8086)
2. Create an account and update the credentials in 'worker.py' and 'docker-compose.yml'.

5. Install Dependencies
pip install -r requirements.txt

Running the Pipeline
1. Start the Data Generator
python data_generator.py

2. Start the Worker to Process Messages
python worker.py

3. Run the Visualization Script
python visualize.py


Project Structure

kafka-influxdb-project
├── data_generator.py   Produces messages to Kafka
├── worker.py           Consumes Kafka messages & writes to InfluxDB
├── visualize.py        Queries InfluxDB & plots data
├── requirements.txt    Python dependencies
├── docker-compose.yml  Container setup for Kafka, Zookeeper, InfluxDB
├── README.md           Project documentation

