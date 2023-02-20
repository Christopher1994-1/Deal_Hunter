from urllib.request import Request, urlopen
from lxml import html
import requests
from twilio.rest import Client
import os


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


print(text)




twilio_number = "+18889393604"
account_sid = os.environ.get('twilio_account_SID')
auth_token = os.environ.get('twilio_auth_token')
client = Client(account_sid, auth_token)

message = client.messages.create(
    body=text,
    from_=twilio_number,
    to=phone_number
        )
