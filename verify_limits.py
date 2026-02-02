import urllib.request
import json
import sys
import time
import urllib.error

BASE_URL = "http://127.0.0.1:8000"

def run_test():
    print("Waiting for server to start...")
    time.sleep(2)
    
    # 1. Clear All
    try:
        req = urllib.request.Request(f"{BASE_URL}/api/tasks/delete-all", method='DELETE')
        urllib.request.urlopen(req)
        print("Cleared tasks.")
    except Exception as e:
        print(f"Setup failed: {e}")
        return False

    # 2. Test Parking Lot Limit (Should be 5)
    print("Testing Parking Lot Limit (Max 5)...")
    for i in range(6):
        try:
            payload = json.dumps({"text": f"PL Task {i}", "category": "parking_lot"}).encode('utf-8')
            req = urllib.request.Request(f"{BASE_URL}/api/tasks", data=payload, headers={'Content-Type': 'application/json'})
            urllib.request.urlopen(req)
            if i == 5:
                print("FAILED: Should have blocked 6th task")
                return False
        except urllib.error.HTTPError as e:
            if i == 5 and e.code == 400:
                print("SUCCESS: Blocked 6th task correctly")
            elif i < 5:
                print(f"FAILED: Could not add task {i}: {e}")
                print(e.read().decode())
                return False

    print("LIMIT TEST PASSED")
    return True

if __name__ == "__main__":
    if not run_test():
        sys.exit(1)
