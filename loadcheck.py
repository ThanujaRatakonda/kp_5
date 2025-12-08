import requests
import concurrent.futures

URL = "http://10.131.103.92:4000/users"

def hit(_):
    try:
        r = requests.get(URL, timeout=5)
        return r.headers.get("X-Pod-Name", "unknown")
    except:
        return "failed"

def main():
    total = int(input("Enter number of requests: "))

    print(f"\nSending {total} concurrent requests to frontend...\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        results = list(executor.map(hit, range(total)))

    # Count hits per pod
    pod_count = {}
    for pod in results:
        pod_count[pod] = pod_count.get(pod, 0) + 1

    print("\n--- POD HIT COUNT ---")
    for pod, count in pod_count.items():
        print(f"{pod}: {count} requests")

if __name__ == "__main__":
    main()

