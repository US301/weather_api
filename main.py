import requests
import os
from twilio.rest import Client

URL = os.environ["URL"]
ACCOUNT_SID = os.environ["ACCOUNT_SID"]
AUTH_TOKEN = os.environ["AUTH_TOKEN"]
PHONE_NUMBER = os.environ["PHONE_NUMBER"]
TO_PHONE_NUMBER = os.environ["TO_PHONE_NUMBER"]
parameters = {

    "lat": 43.653225,
    "lon": -79.383186,
    "appid": "e33801547cffca87797e44fdd0c74773",
    "exclude": "current,minutely,daily,alerts",
}

weather_data = requests.get(URL, params=parameters)
weather_data.raise_for_status()
hourly_weather = weather_data.json()["hourly"][:12]

weather_ids = []
will_rain = False

for hour in hourly_weather:
    weather_ids.append(hour["weather"][0]["id"])
    if hour["weather"][0]["id"] < 700:
        will_rain = True

if will_rain:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages \
        .create(
        body="It's going to rain today! Remember to bring an ☔️.",
        from_= PHONE_NUMBER,
        to=TO_PHONE_NUMBER
    )
    print(message.status)

