import json
import random
import time
from kafka import KafkaProducer

# Kafka configuration
KAFKA_BROKER = 'localhost:9092'
TOPIC_NAME = 'color_data'

# colors shown in the assignment 
COLORS = ['red', 'blue', 'green', 'yellow']

# Initializing the Kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_message():
    """Generate a random message with color and value."""
    return {
        'color': random.choice(COLORS),
        'value': random.randint(1, 100)
    }

def publish_message():
    """Publish messages to Kafka topic at regular intervals."""
    while True:
        message = generate_message()
        producer.send(TOPIC_NAME, value=message)
        print(f"Published: {message}")
        time.sleep(1)

if __name__ == "__main__":
    publish_message()