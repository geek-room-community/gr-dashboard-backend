"""
If you want to test this using postman, copy this JSON and for detailed steps check readme
{
    "presentation_id": "1sswT4MWdmwew5zoS_YD1gzv0D1_jL8j8ZmYROC2gUCU",
    "full_name": "Jaspreet Singh 😎"
}
"""


import requests
import json

url = "http://127.0.0.1:5000//certificate-preview"

payload = json.dumps({
  "presentation_id": "1sswT4MWdmwew5zoS_YD1gzv0D1_jL8j8ZmYROC2gUCU",
  "full_name": "Jaspreet Singh 😎"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
