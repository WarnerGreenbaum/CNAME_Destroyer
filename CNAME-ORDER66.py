import requests
from datetime import datetime 
import json

url = "https://cyder-dev.nws.oregonstate.edu/api/v1/dns/cname/?i:ctnr=247"
MY_TOKEN = "your token here"
headers = {'Authorization': f'Token {MY_TOKEN}'}

# Grabbign current  date 
now = datetime.now()
current_date = now.date()
current_date = datetime.strptime(str(current_date), '%Y-%m-%d')
print(current_date)

# Cycling through each page 
while url: 
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    # Going through each entry in page
    for entry in data['results']:
        created = entry['created'][:10]
        created = datetime.strptime(created, '%Y-%m-%d')
        print(created)
        diff = abs((created - current_date).days)
        if diff > 365:
            print("DELETING ENTRY:\n")
            print(entry['fqdn'] + "\n")
            print(entry['target'] + "\n")
            delete_url = f"https://cyder-dev.nws.oregonstate.edu/api/v1/dns/cname/{entry['id']}/" 
            print("del url: " + delete_url)
            delete_response = requests.delete(delete_url, headers=headers)
            print("del response: " + str(delete_response))
                
        json_data = json.dumps(entry, indent=4)
        # print(json_data)
    # json_data = json.dumps(data, indent=4)
    # print(json_data)
    url = data.get('next')



