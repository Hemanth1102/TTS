import requests

url = "http://127.0.0.1:5002/synthesize"
payload = {
    "text": "హలో, మీరు ఎలా ఉన్నారు?",
    "speaker": "female"  # or "male" based on your speaker.pth
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print("✅ Audio synthesized and saved as output.wav")
else:
    print(f"❌ Error: {response.status_code}", response.text)
