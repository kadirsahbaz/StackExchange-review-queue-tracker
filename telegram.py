# import the necessary packages
from bs4 import BeautifulSoup
from requests import Session
import telebot
import time

bot = telebot.TeleBot("your_authorization_token_here")

# A sample StackExchange site
website = "https://gis.stackexchange.com"
email = "email_here"
password = "password_here"
telegram_chat_id = "chat_id_here"

numbers_dict = {'Close votes': 0,
                'First questions': 0,
                'First answers': 0,
                'Late answers': 0,
                'Low quality posts': 0,
                'Reopen votes': 0,
                'Suggested edits': 0}

links = {'Close votes': website + "/review/close",
         'First questions': website + "/review/first-questions",
         'First answers': website + "/review/first-answers",
         'Late answers': website + "/review/late-answers",
         'Low quality posts': website + "/review/low-quality-posts",
         'Reopen votes': website + "/review/reopen",
         'Suggested edits': website + "/review/suggested-edits"}

session = Session()
session.post(website + "/users/login",
             {"email": email,
              "password": password,
              "rememberMe": "true",
              "top_login": "true"})

while True:
    try:
        page = session.get(website + "/review").content
        soup = BeautifulSoup(page, 'html.parser')
        
        numbers = [int(d.find(class_='fs-body3').text) for d in soup.find_all(class_='wmn1')]
        review_names = [d.find('a').text for d in soup.find_all(class_='mb2') if d.find('a') is not None]

        review_number_pairs = dict(zip(review_names, numbers))
        
        # to ignore any queue to avoid intensive messages, ex. 'First questions'
        del review_number_pairs['First questions']

        message = ''
        for k in review_number_pairs:
            n = review_number_pairs[k]
            if n > 0:
                message +=  f"{n} - {k}\n{links[k]}\n\n"

        bot.send_message(telegram_chat_id, message, disable_web_page_preview=True)

        numbers_dict = dict(review_number_pairs)

    # for possible unimportant errors
    except Exception as e:
        print("ERROR: " + str(e))
        session = Session()
        session.post(website + "/users/login",
                     {"email": "email_here",
                      "password": "password_here",
                      "rememberMe": "true",
                      "top_login": "true"})

    time.sleep(300) # check every 5 minutes
