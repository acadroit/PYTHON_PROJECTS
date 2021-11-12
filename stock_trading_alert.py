import requests
import pprint as pp
from newsapi import NewsApiClient
import pprint as pp
from twilio.rest import Client


STOCK_NAME="ICICIBANK.BO"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "Stock_api_key"
STOCK_PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}
RESPONSE = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMS)
DATA = RESPONSE.json()
TIME_SERIES_DATA=DATA['Time Series (Daily)']
DATA_LIST = [value for (key, value) in TIME_SERIES_DATA.items()]



'''
Feteching the yesterday and day before yesterday's data
'''
YESTERDAY_DATA=float(DATA_LIST[-1]['4. close'])
DAY_BEFORE_YESTERDAY_DATA=float(DATA_LIST[-2]['4. close'])

'''
Calculating the percentage difference between yesterday and day before yesterday data
'''
DIFFERENCE=YESTERDAY_DATA-DAY_BEFORE_YESTERDAY_DATA
UP_DOWN = None
if DIFFERENCE > 0:
    UP_DOWN = "🔺"
else:
    UP_DOWN = "🔻"

'''
Percentage difference in price between closing price yesterday and closing price the day before yesterday.
'''
DIFF_PERCENT = round((DIFFERENCE /(YESTERDAY_DATA)) * 100)
print(DIFF_PERCENT)
print(UP_DOWN)

'''
Fetching the last 3 news related to my stock
'''

if abs(DIFF_PERCENT) >= 1:
    NEWSAPI = NewsApiClient(api_key="NEWSAPI.orgkey")

    all_articles = NEWSAPI.get_everything(q='ICICI bank',
                                      language='en',
                                      sort_by='relevancy',
                                      )
    FILTERED_ARTICLES=all_articles["articles"]
    news_update=[i.get("content") for i in FILTERED_ARTICLES]

    LATEST_THREE_NEWS=news_update[:3]
    
    print(LATEST_THREE_NEWS)

    #Creating a new list of the first 3 article's headline and description using list comprehension.
    formatted_articles = [f"{STOCK_NAME}: {UP_DOWN}{DIFF_PERCENT}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in LATEST_THREE_NEWS]
    print(formatted_articles)
    #Sending each article as a separate message via Twilio.
    CLIENT = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    #Sending each article as a separate message via Twilio.
    for article in formatted_articles:
        message = CLIENT.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )
