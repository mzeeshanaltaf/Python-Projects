import requests
from datetime import datetime
import smtplib
import time

GOOGLE_PASSWORD = "password"
GOOGLE_SMTP = "smtp.gmail.com"
PORT = 587

MY_LAT = 31.500130
MY_LONG = 74.419517

def send_email(smtp, from_email, to_email, password):
    with smtplib.SMTP(smtp, port=PORT) as connection:
        connection.starttls()
        connection.login(user=from_email, password=password)
        connection.sendmail(
            from_addr=from_email,
            to_addrs=to_email,
            msg="Subject: ISS is near-by\n\nISS is near-by. Look-Up!"
        )


def is_iss_overhead():
    """ Based on the specified location (latitude and longitude),
    this function returns whether iss is overhead or not"""
    response = requests.get("http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    # if ISS is within +-5 degree of my position, return True
    if (MY_LAT + 5) >= iss_latitude >= (MY_LAT - 5) and (MY_LONG + 5) >= iss_longitude >= (MY_LONG - 5):
        return True
    else:
        return False


def is_night():
    """ Based on the specified location (latitude and longitude), this function returns whether it's night or not"""
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
        "tzId": "Asia/Karachi",
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    hour = datetime.now().hour

    return hour > sunset or hour < sunrise


while True:
    time.sleep(60)
    if is_iss_overhead and is_night:
        send_email(smtp=GOOGLE_SMTP,
                   from_email="id@gmail.com",
                   to_email="id@yahoo.com",
                   password=GOOGLE_PASSWORD)

