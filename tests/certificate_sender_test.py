"""
Replace the placeholders with your name and email to test
If you want to test this using postman, copy this JSON and for detailed steps check readme
{
    "presentation_id": "1sswT4MWdmwew5zoS_YD1gzv0D1_jL8j8ZmYROC2gUCU",
    "subject": "Certificate of Achievement",
    "body": "Hello {Full_Name}, congratulations! 🎉",
    "rows": [
        {
            "Full Name": "Your Name",
            "Email": "your@email.here"
        },
        {
            "Full Name": "Your Name",
            "Email": "your@email.here"
        }
    ]
}
"""

import requests
import json

url = "http://127.0.0.1:5000//certificate-sender"

#Update the email and name before running
payload = json.dumps({
  "presentation_id": "1sswT4MWdmwew5zoS_YD1gzv0D1_jL8j8ZmYROC2gUCU",
  "subject": "Certificate of Achievement",
  "body": "Hello {Full_Name}, congratulations! 🎉",
  "rows": [
    {
      "Full Name": "Your Name",
      "Email": "your@email.here"
    },
    {
      "Full Name": "Your Name",
      "Email": "your@email.here"
    }
  ]
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
