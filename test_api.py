import requests
import sys

# Switch localhost to explicit IPv4 loopback to bypass Windows routing bugs
BASE_URL = "http://127.0.0.1:5000/api/v1/locations"
HEADERS = {
    "x-api-key": "DEMO_KEY_2026",
    "Content-Type": "application/json"
}

def verify_b2b_platform():
    print(" Sending authenticated request to Capstone Server...")
    try:
        # Added a 5-second timeout so the script fails fast instead of hanging
        response = requests.get(f"{BASE_URL}/states", headers=HEADERS, timeout=5)
        
        if response.status_code == 200:
            payload = response.json()
            print(f"\n Authenticated Client Recognized: {payload.get('client')}")
            states = payload.get('data', [])
            print(f" Success! Pulled {len(states)} normalized states from PostgreSQL.")
            
            if states:
                sample_state = states[0]
                print(f" Sample State Entry: {sample_state['state_name']} (ID: {sample_state['id']})")
        else:
            print(f" Server responded with error status: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.Timeout:
        print("\n Error: The request timed out! Your server is running but taking too long to respond.")
    except requests.exceptions.ConnectionError:
        print("\n Error: Connection refused! Is 'node server.js' currently running in your other terminal?")
    except Exception as e:
        print(f"\n Unexpected Error: {e}")

if __name__ == "__main__":
    verify_b2b_platform()