"""import smtplib

my_email = "bansh8956@gmail.com"
password = "lrry hlza eojl hvlc"



with smtplib.SMTP_SSL("smtp.gmail.com", 465) as connection:
    # connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(
        from_addr=my_email, to_addrs=my_email, msg="Subject:Hello\n\nThis is the body"
    )


import smtplib
import getpass

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

HOST = "smtp.gmail.com"
PORT = 587

FROM_EMAIL = "bansh8956@gmail.com"
TO_EMAIL = "bansh8956@gmail.com"
PASSWORD = "lrry hlza eojl hvlc"

message = MIMEMultipart("alternative")
message["Subject"] = "<add subject here>"
message["From"] = FROM_EMAIL
message["To"] = TO_EMAIL
message["Cc"] = FROM_EMAIL
message["Bcc"] = FROM_EMAIL
html = ""
with open("templates/reset_password.html", "r") as file:
    html = file.read()

html_part = MIMEText(html, "html")
message.attach(html_part)

smtp = smtplib.SMTP(HOST, PORT)

status_code, response = smtp.ehlo()
print(f"[*] Echoing the server: {status_code} {response}")

status_code, response = smtp.starttls()
print(f"[*] Starting TLS connection: {status_code} {response}")

status_code, response = smtp.login(FROM_EMAIL, PASSWORD)
print(f"[*] Logging in: {status_code} {response}")

smtp.sendmail(FROM_EMAIL, TO_EMAIL, message.as_string())
smtp.quit()
"""
