import random
import time
import requests

# Function to simulate random heart rate readings
def generate_heart_rate():
    return random.randint(50, 150)  # Normal range 60-100, abnormal above 100

# Function to send heart rate data to the Alexa model server
def send_heart_rate(heart_rate):
    url = "http://localhost:5001/process_heart_rate"  # Using localhost as both scripts run on the same machine
    data = {"heart_rate": heart_rate}

    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Response from Alexa model:", response.json())
        else:
            print(f"Failed to send data, status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending data: {e}")

# Main loop to continuously generate and send heart rate
def monitor_heart_rate():
    while True:
        heart_rate = generate_heart_rate()
        print(f"Generated heart rate: {heart_rate}")
        send_heart_rate(heart_rate)
        time.sleep(5)  # Wait 5 seconds before sending another reading

if __name__ == "__main__":
    monitor_heart_rate()