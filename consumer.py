from kafka import KafkaConsumer
import json

# Kafka consumer setup
consumer = KafkaConsumer(
    'waqi-data',  # Topic name
    bootstrap_servers='localhost:9092',  # Connect to Kafka broker in the Docker container
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='example-group',  # Consumer group ID
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Consume and process messages
for message in consumer:
    val = message.value
    print(val)
    # print(f'{val["aqi"], val["iaqi"]}')
