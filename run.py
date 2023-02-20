from urllib.request import Request, urlopen
from lxml import html
import requests
from twilio.rest import Client
import os
import smtplib
import datetime 


# Sending email
def send_email(message):
    my_pass = os.environ.get('ggg')
    my_email = "cejvanniekirk098@gmail.com"
    receiver = "kirko190255@gmail.com" # TODO change to os after restart


    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(my_email, my_pass)
        subject = "New Weekly Ads"
        body = message

        msg = f"Subject: {subject}\n\n{body}"

        smtp.sendmail(my_email, receiver, msg)






url="https://www.myweeklyads.net/winco-foods-sales/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
}

req = Request(url, headers=headers)

# Make the request and retrieve the response content
response = urlopen(req)
content = response.read()

weekly_ad = str(content)[270:323]


response = requests.get(url)
tree = html.fromstring(response.content)
data = tree.xpath("/html/body/div[1]/div/div/div/main/article/div/p[5]")


text_content = str(data[0].text_content())


text = f"\n\n{weekly_ad}\n\n{text_content}"

phone_number = os.environ.get("my_number")





# str of today date converted to int
today = int(str(datetime.datetime.now()).split(' ')[0].split('-')[2])

weekly_ad_split = weekly_ad.split(' ')

ad_start_date = int(weekly_ad_split[5])
ad_end_date = int(weekly_ad_split[8].replace(',', ''))



if today in range(ad_start_date, ad_end_date+1):
    pass
else:
    send_email(text)















# # for texting
# # def send_text():
# #     twilio_number = "+18889393604"
# #     account_sid = os.environ.get('twilio_account_SID')
# #     auth_token = os.environ.get('twilio_auth_token')
# #     client = Client(account_sid, auth_token)

# #     message = client.messages.create(
# #         body=text,
# #         from_=twilio_number,
# #         to=phone_number
# #     )




