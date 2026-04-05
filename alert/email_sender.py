import smtplib

def send_email(message):
    sender = "your_email@gmail.com"
    receiver = "receiver@gmail.com"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, "YOUR_PASSWORD")

    server.sendmail(sender, receiver, message)
    server.quit()