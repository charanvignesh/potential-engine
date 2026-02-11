import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:5000"
CHANNEL_ID = "3105178"  # Replace with actual Channel ID
API_KEY = "PLFY2DYI5EGL5DWN"   # Replace with actual Read API Key (optional if public)

def test_prediction():
    endpoint = f"{BASE_URL}/api/predict_thingspeak"
    
    payload = {
        "channel_id": CHANNEL_ID,
        "api_key": API_KEY
    }
    
    print(f"Testing endpoint: {endpoint}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(endpoint, json=payload)
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            print("\n✅ Success! Response:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"\n❌ Error: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Could not connect to {BASE_URL}. Is the Flask app running?")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    test_prediction()
