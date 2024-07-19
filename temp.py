import base64

api_key = 'your_freshservice_api_key'
encoded_api_key = base64.b64encode(api_key.encode()).decode()
print(encoded_api_key)
