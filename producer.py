import requests
import json
import time
from kafka import KafkaProducer

# Kafka producer setup
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

api_urls = [
    'https://api.waqi.info/feed/@2328/?token=67fa88c2f05757e11b93feacaa775b78258b2d7b'
]

def filter(data):
    filtered = {}
    filtered['aqi'] = data["aqi"]
    filtered['dominant'] = data['dominentpol']
    filtered['co'] = data['iaqi']['co']['v']
    filtered['h'] = data['iaqi']['h']['v']
    filtered['no2'] = data['iaqi']['no2']['v']
    filtered['o3'] = data['iaqi']['o3']['v']
    filtered['p'] = data['iaqi']['p']['v']
    filtered['pm10'] = data['iaqi']['pm10']['v']
    filtered['pm25'] = data['iaqi']['pm25']['v']
    filtered['so2'] = data['iaqi']['so2']['v']
    filtered['t'] = data['iaqi']['t']['v']
    filtered['w'] = data['iaqi']['w']['v']

    return filtered


# Function to fetch air quality data from the WAQI API
def fetch_air_quality_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status() 
        data = response.json()
        if 'data' in data:
            return filter(data['data'])
        else:
            print(f"Invalid data format from {api_url}: {data}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {api_url}: {e}")
        return None

# Function to send data to Kafka topic
def send_data_to_kafka(api_urls):
    for api_url in api_urls:
        data = fetch_air_quality_data(api_url)
        if data:
            producer.send('waqi-data', value=data)
            print(f"Data sent to Kafka")

# Infinite loop to continuously fetch and send data
while True:
    send_data_to_kafka(api_urls)
    time.sleep(60) 

# Close the producer gracefully when stopping the script
producer.flush()
producer.close()