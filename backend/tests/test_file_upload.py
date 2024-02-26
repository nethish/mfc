import requests

BASE_URL = 'http://localhost:8000/api/v1/parse_cas_summary'
f = {'file': open('nopass.pdf', 'rb')}
r = requests.post(f"{BASE_URL}", files=f)
print(r)
