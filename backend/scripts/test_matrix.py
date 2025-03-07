#!/usr/bin/env python
import httpx

# Define the server and the JWT token
server_url = "https://matrix.chat.la-suite.apps.digilab.network"
jwt_token = ""
room_id = "!LniOzkgFNaIQGuvKVR:chat.la-suite.apps.digilab.network"


login_headers = {"Content-Type": "application/json"}

# Define the API endpoint for fetching messages
login_url = f"{server_url}/_matrix/client/r0/login"
login_response = httpx.post(login_url, headers=login_headers, json={"type": "org.matrix.login.jwt", "token": jwt_token})
print(login_response.json())

# url = f"{server_url}/_matrix/client/r0/rooms/{room_id}/messages"
# Set up the request headers
# access_token = login_response.json().get("access_token", None)
# headers = {
#     "Authorization": f"Bearer {access_token}",
#     "Content-Type": "application/json"
# }


# # Send the GET request
# response = httpx.get(url, headers=headers)

# # Check if the request was successful
# if response.status_code == 200:
#     messages = response.json()
#     for message in messages['chunk']:
#         print(f"Sender: {message['sender']}")
#         print(f"Message: {message['content']['body']}")
# else:
#     print("Error:", response.status_code, response.text)
