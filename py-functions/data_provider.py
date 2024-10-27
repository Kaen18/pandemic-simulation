# /backend/python/data_provider.py
import json

def get_data():
    data = {
        "name": "John Doe",
        "age": 30,
        "city": "New York"
    }
    return json.dumps(data)

if __name__ == "__main__":
    print(get_data())
