import os
from dotenv import load_dotenv, dotenv_values, find_dotenv
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient




envpath=find_dotenv()
load_dotenv(envpath)

os.getenv("APIKEY")
os.getenv("account_sid")
os.getenv("auth_token")
os.getenv("MOBNUM")
os.getenv("VRNUM")

MY_LAT = 18.757420
MY_LONG = 73.413727
                                                      

parameters = {
    "lat":MY_LAT,
    "lon":MY_LONG,
    "appid":os.environ["API_KEY"],
    "cnt":4
}


respond = requests.get("https://api.openweathermap.org/data/2.5/forecast",params=parameters)
respond.raise_for_status()
data = respond.json()


will_rain = False
for hour_data in data["list"]:
    value = hour_data["weather"][0]["id"]
    if int(value) < 700:
        will_rain = True
if will_rain :
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(os.getenv("account_sid"), os.environ["auth_token"],http_client=proxy_client)
    message = client.messages.create(
        body="bring your umbrella  ☂️",
        from_=os.getenv("VRNUM"),
        to=os.getenv("MOBNUM"))
    print(message.status)

else:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(os.getenv("account_sid"), os.environ["auth_token"],http_client=proxy_client)
    message = client.messages.create(
        body="DONT bring your umbrella  ☂️",
        from_=os.getenv("VRNUM"),
        to=os.getenv("MOBNUM"))
    print(message.status)

