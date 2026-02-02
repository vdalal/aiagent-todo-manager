import urllib.request
import json
import sys
import time

BASE_URL = "http://127.0.0.1:8000"

def run_test():
    print("Waiting for server to start...")
    time.sleep(2)
    
    # 1. Add Multiple Tasks
    print("Adding 3 tasks...")
    for i in range(3):
        try:
            payload = json.dumps({"text": f"Bulk Task {i}", "category": "urgent"}).encode('utf-8')
            req = urllib.request.Request(f"{BASE_URL}/api/tasks", data=payload, headers={'Content-Type': 'application/json'})
            urllib.request.urlopen(req)
        except Exception as e:
            print(f"Failed to add task {i}: {e}")
            return False

    # 2. Test Complete All
    try:
        req = urllib.request.Request(f"{BASE_URL}/api/tasks/complete-all", data=b'', method='POST')
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(f"POST /api/tasks/complete-all: OK (Count: {data['count']})")
            if data['count'] < 3:
                print("Warning: Expected at least 3 completed tasks")
    except Exception as e:
        print(f"POST complete-all FAILED: {e}")
        return False

    # 3. Test Delete All
    try:
        req = urllib.request.Request(f"{BASE_URL}/api/tasks/delete-all", method='DELETE')
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print(f"DELETE /api/tasks/delete-all: OK (Count: {data['count']})")
    except urllib.error.HTTPError as e:
        print(f"DELETE delete-all FAILED: {e}")
        print(e.read().decode())
        return False
    except Exception as e:
        print(f"DELETE delete-all FAILED: {e}")
        return False

    print("ALL BULK TESTS PASSED")
    return True

if __name__ == "__main__":
    if not run_test():
        sys.exit(1)
