import requests
import threading

# generated scipt by chat GPT
# TODO : Implement the DDoS attack later

def send_requests(url, num_requests):
    for i in range(num_requests):
        try:
            response = requests.get(url)
            print(f"[{i+1}] Statut: {response.status_code}")
        except requests.RequestException as e:
            print(f"Erreur: {e}")


def simulate_ddos(url, num_threads, requests_per_thread):
    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=send_requests, args=(url, requests_per_thread))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
