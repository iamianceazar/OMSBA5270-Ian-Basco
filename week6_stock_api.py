# import all modules

import pandas as pd
import requests
import yfinance as yf
from datetime import datetime, timedelta
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 23)

# create a request header
headers = {'User-Agent': 'ibasco@seattleu.edu'}

# get all companies data
companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers)

# print(companyTickers.json()['0']['cik_str'])

companyCIK = pd.DataFrame.from_dict(companyTickers.json(), orient = 'index')
# print(companyCIK)

# adding zero's to CIK

companyCIK['cik_str'] = companyCIK['cik_str'].astype(str).str.zfill(10)
# print(companyCIK)

a = [789, 420, 45]
b = [790, 421, 46]
for j,k in zip(a,b):
# selecting CIK
    cik = companyCIK[j:k].cik_str.iloc[0]
    companyTitle = companyCIK[j:k].title.iloc[0]
    print(companyTitle)
    print("CIK:", cik)

    # get all companies facts data
    companyFacts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers)

    # Exploratory Data Analysis

    # Average marketing expense calculation
    liabilities_df = pd.DataFrame.from_dict((companyFacts.json()['facts']['us-gaap']['Liabilities']['units']['USD']))
    liabilities_initial_date = liabilities_df['filed'].iloc[0]
    # print(revenues_df)

    # We need a ticker symbol
    tickerSymbol = companyCIK[j:k].ticker.iloc[0]
    print("Ticker:", tickerSymbol)

    # start date for the api call
    start_date_str = liabilities_initial_date
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')

    # calculate the delta
    end_date = start_date + timedelta(days=10950)

    # convert end date to str
    end_date_str = end_date.strftime('%Y-%m-%d')

    # create a yfinance ticker object
    ticker = yf.Ticker(tickerSymbol)

    # pull yfinance historical data
    historical_data = ticker.history(period = '1d', start=start_date_str, end=end_date_str)

    historical_df = pd.DataFrame(historical_data)
    # print(historical_df)

    # add a new column

    liabilities_df['closing stock price'] = 0

    for index, row in liabilities_df.iterrows():
        value = row['filed']

        tickerSymbol = companyCIK[j:k].ticker.iloc[0]
        # print(tickerSymbol)

        # start date for the api call
        start_date_str = value
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')

        # calculate the delta
        end_date = start_date + timedelta(days=10950)

        # convert end date to str
        end_date_str = end_date.strftime('%Y-%m-%d')

        # create a yfinance ticker object
        ticker = yf.Ticker(tickerSymbol)

        # pull yfinance historical data
        historical_data = ticker.history(period='1d', start=start_date_str, end=end_date_str)

        historical_df = pd.DataFrame(historical_data)
        # print(historical_df)

        specific_data = historical_data.iloc[0]['Close']

        liabilities_df.at[index, 'closing stock price'] = specific_data

        # print(specific_data)

    print(liabilities_df)
