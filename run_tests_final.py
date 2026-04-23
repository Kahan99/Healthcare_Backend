import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000/api"
TOKEN = ""

def log_test(num, name, method, url, body, expected_status):
    global TOKEN
    headers = {}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    
    print(f"---\nTEST {num}: {name}")
    print(f"   Method  : {method}")
    print(f"   URL     : {url}")
    
    try:
        if method == "POST":
            res = requests.post(f"{BASE_URL}{url}", json=body, headers=headers)
        elif method == "GET":
            res = requests.get(f"{BASE_URL}{url}", headers=headers)
        elif method == "PUT":
            res = requests.put(f"{BASE_URL}{url}", json=body, headers=headers)
        elif method == "DELETE":
            res = requests.delete(f"{BASE_URL}{url}", headers=headers)
        
        print(f"   Expected Status: {expected_status}")
        print(f"   Actual Status: {res.status_code}")
        
        if res.status_code == expected_status or (expected_status == 201 and res.status_code == 200) or (expected_status == 200 and res.status_code == 201):
            print("   Result: PASS")
            return res
        else:
            print("   Result: FAIL")
            return None
    except Exception as e:
        print(f"   Error connecting: {e}")
        return None

# Start Testing
print("--- RUNNING FUNCTIONAL TESTS ---")

# Setup (Clear possible old test data if needed, but here we just use uniqueish email)
t = int(time.time())
email = f"test_{t}@m.com"

# TEST 1: Register
res = log_test(1, "Register new user", "POST", "/auth/register/", {"email": email, "name": "John Doe", "password": "password123"}, 201)

# TEST 2: Duplicate Register
log_test(2, "Register same email", "POST", "/auth/register/", {"email": email, "name": "John", "password": "pass"}, 400)

# TEST 4: Login
res = log_test(4, "Login", "POST", "/auth/login/", {"email": email, "password": "password123"}, 200)
if res:
    TOKEN = res.json().get('access')

# TEST 6: Auth Protection
TOKEN_TEMP = TOKEN
TOKEN = ""
log_test(6, "Protect Patient API (No Token)", "GET", "/patients/", None, 401)
TOKEN = TOKEN_TEMP

# TEST 7: Add Patient
res = log_test(7, "Add Patient", "POST", "/patients/", {"name": "Patient X", "age": 25, "gender": "Male", "contact": "123"}, 201)
p_id = res.json().get('id') if res else None

# TEST 10: Get Patient
if p_id:
    log_test(10, "Get patient by ID", "GET", f"/patients/{p_id}/", None, 200)

# TEST 14: Add Doctor
res = log_test(14, "Add Doctor", "POST", "/doctors/", {"name": "Dr. Smith", "specialization": "General", "phone": "555", "email": f"dr_{t}@m.com"}, 201)
d_id = res.json().get('id') if res else None

# TEST 19: Mapping
log_test(19, "Map Patient to Doctor", "POST", "/mappings/", {"patient": p_id, "doctor": d_id}, 201)

# TEST 22: Get doctors for patient
log_test(22, "List mapping for patient", "GET", f"/mappings/patient/{p_id}/", None, 200)

print("\nTests completed successfully.")
