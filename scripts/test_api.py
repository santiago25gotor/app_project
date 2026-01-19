
import requests

try:
    print("Testing GET /api/laliga...")
    r = requests.get("http://localhost:8000/api/laliga")
    print(f"Status Code: {r.status_code}")
    print("Raw text content (first 500 chars):")
    print(r.text[:500])
    
    try:
        data = r.json()
        print(f"\nJSON parsed successfully. Type: {type(data)}")
        if isinstance(data, list):
            print(f"List length: {len(data)}")
            if len(data) > 0:
                print("First item keys:", data[0].keys())
    except Exception as e:
        print(f"\nJSON parse failed: {e}")

except Exception as e:
    print(f"Request failed: {e}")
