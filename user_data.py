import requests
import os

# --- This file is used to post customer/user data to google sheets using SHEETY API --- #

print("Welcome to Arjunan's Flight Club")
print("We find the best flight deals and email you")
f_name = input("What is your First name?: ").title()
print(f_name)
l_name = input("What is your Last name?: ").title()
print(l_name)
email = input("What is your email?: ")
email1 = input("type your email again.")
SHEETY_USER_ENDPOINT = os.environ["sheety_user6"]
user_header = {
  "Authorization": f'Bearer {os.environ["user_token"]}'
}
new_data = {
    "user": {
        "firstName": f_name,
        "lastName": l_name,
        "email": email
    }
}
if email == email1:
    response = requests.post(
      url=SHEETY_USER_ENDPOINT,
      json=new_data,
      headers=user_header
    )
    print(response.text)
    print("You're in the club...")
if email != email1:
    print("Wrong email, type again")