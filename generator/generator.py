import random
import time
import requests

URL = "http://backend:8000/ingest"

while True:
    payload = {
        "machine_id": "EUV-01",
        "temperature": round(random.uniform(40, 100), 2),   
        "latency": round(random.uniform(10, 200), 2),       
        "error_count": int(random.randint(0, 5)),           
        "timestamp": int(time.time()),                      
    }

    try:
        r = requests.post(URL, json=payload)
        print(r.status_code, payload)
    except Exception as e:
        print(e)

    time.sleep(2)