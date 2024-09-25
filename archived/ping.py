from pythonping import ping
import requests


# Ping localhost
response_list = ping('127.0.0.1', verbose=True)

# Print the response list
for response in response_list:
    print(response)


response = requests.get('http://google.com')

# Print the status code and the content of the response
print(response.status_code)
print(response.text)
