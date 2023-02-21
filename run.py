from urllib.request import Request, urlopen
from lxml import html
import requests
from twilio.rest import Client
import os
import smtplib
import datetime 
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient


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


url_for_email = "https://www.wincofoods.com/store-events"

text = f"\n\nNew WinCo Weekly Ads and Sales.\n{weekly_ad}\n\n{text_content}\n\nCheck out more below\n{url_for_email}"
reminder_email = f"\n\nReminder to check out WinCo Weekly Ads\n\n{weekly_ad}\n\n{text_content}\n\nCheck out more below\n{url_for_email}"

phone_number = os.environ.get("my_number")





# str of today date converted to int
today = int(str(datetime.datetime.now()).split(' ')[0].split('-')[2])

weekly_ad_split = weekly_ad.split(' ')

ad_start_date = int(weekly_ad_split[5])
ad_end_date = int(weekly_ad_split[8].replace(',', ''))



# WORKING WITH MONGO-DB AND FINAL CODE

load_dotenv(find_dotenv())

# password = os.environ.get('MONGODB_PWD')
password = "stars0098"

connection_string = f"mongodb+srv://avrlinetech:{password}@firstmongo.pk2ympr.mongodb.net/?retryWrites=true&w=majority"
                                
client = MongoClient(connection_string)

# returns all databases inside 
dbs = client.list_database_names()

weekly_ads = client.weekly_ads

collenctions = weekly_ads.list_collection_names()



# inserting data in db
def insert_test_doc(timeframe):
    # inserting data like this
    collection = weekly_ads.ad_dates
    test_document = {
        "TimeFrame": timeframe,
    }
    
    inserted_id = collection.insert_one(test_document).inserted_id



# reading data
def read_data():
    weekly_ads2 = weekly_ads.ad_dates
    data = weekly_ads2.find()
    
    for i in data:
        return i['TimeFrame'], i['_id']
    
    
    

def delete_doc_by_id(person_id):
    from bson.objectid import ObjectId
    weekly_ads2 = weekly_ads.ad_dates
    
    _id = ObjectId(person_id)
    
    
    weekly_ads2.delete_one({"_id": _id})


current_ad_timeline = "WinCo Foods Weekly Ad February 15 - February 21, 2023"


reminder = []


# if weekly ad is there
a = read_data()

# if there is nothing there
if a == None:
    insert_test_doc(weekly_ad)
    
    
# if there is something there and that something is equal to the current ad
elif a != None and a[0] == weekly_ad:
    str_spilt = weekly_ad.split(' ')
    start_date = int(str_spilt[5])
    end_date = int(str_spilt[8].replace(',', ''))
    
    for i in range(start_date, end_date+1):
        if i % 2 == 0:
            reminder.append(str(i))
            
    if str(today) in reminder:
        send_email(reminder_email)


# if there is something there and that something is not equal to the current ad
elif a != None and a[0] != weekly_ad:
    delete_doc_by_id(a[1])
    insert_test_doc(weekly_ad)
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




