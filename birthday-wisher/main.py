import smtplib
from datetime import datetime
from random import randint
import pandas

GOOGLE_PASSWORD = "password"
GOOGLE_SMTP = "smtp.gmail.com"
PORT = 587


def send_birthday_email(smtp, from_email, to_email, password, message):
    with smtplib.SMTP(smtp, port=PORT) as connection:
        connection.starttls()
        connection.login(user=from_email, password=password)
        connection.sendmail(
            from_addr=from_email,
            to_addrs=to_email,
            msg=f"Subject: Happy Birthday\n\n{message}"
        )


data = pandas.read_csv("birthdays.csv")
birthday_dict = {(row.month, row.day): row for (index, row) in data.iterrows()}

today = datetime.now()
today_tuple = (today.month, today.day)

if today_tuple in birthday_dict:
    birthday_person = birthday_dict[today_tuple]
    file_path = f"letter_templates/letter_{randint(1, 3)}.txt"
    with open(file_path) as letter_file:
        contents = letter_file.read()
        new_content = contents.replace("[NAME]", birthday_person["name"])
        send_birthday_email(smtp=GOOGLE_SMTP,
                            from_email="id@gmail.com",
                            to_email=birthday_person["email"],
                            password=GOOGLE_PASSWORD,
                            message=new_content)
