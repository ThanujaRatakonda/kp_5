import requests
from concurrent.futures import ThreadPoolExecutor

# URL of the backend service
URL = "http://10.131.103.92:5000/users"

def fire_and_forget(_):
    """Simulate 'curl -s > /dev/null'"""
    try:
        requests.get(URL, timeout=10)
    except:
        pass

def check_status_and_pod(_):
    """Simulate 'curl -o /dev/null -w' and show which pod handled the request"""
    try:
        r = requests.get(URL, timeout=10)
        pod = r.headers.get("X-Pod-Name", "unknown")
        print(f"status:{r.status_code}, Time:{r.elapsed.total_seconds():.3f}s, Pod:{pod}")
    except Exception as e:
        print(f"status:ERR, Time:N/A, Pod:N/A")

def main():
    total = int(input("Enter number of requests: "))

    print(f"\nSending {total} fire-and-forget requests...")
    with ThreadPoolExecutor(max_workers=50) as executor:
        list(executor.map(fire_and_forget, range(total)))

    print(f"\nSending {total} requests with status/time and pod info...")
    with ThreadPoolExecutor(max_workers=50) as executor:
        list(executor.map(check_status_and_pod, range(total)))

if __name__ == "__main__":
    main()

