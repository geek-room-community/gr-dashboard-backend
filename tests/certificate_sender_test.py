import requests
import json

url = "http://127.0.0.1:5000//certificate-sender"

payload = json.dumps({
  "presentation_id": "1sswT4MWdmwew5zoS_YD1gzv0D1_jL8j8ZmYROC2gUCU",
  "subject": "Certificate of Achievement",
  "body": "Hello {Full_Name}, congratulations! 🎉",
  "rows": [
    {
      "Full Name": "Jaspreet Singh",
      "Email": "jaspreet.jsk.kohli@gmail.com"
    },
    {
      "Full Name": "The JSK",
      "Email": "yojsklol@gmail.com"
    }
  ]
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
