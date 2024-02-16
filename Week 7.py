# import the modules
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import requests
import yfinance as yf
from datetime import datetime, timedelta
import warnings



warnings.simplefilter(action='ignore', category=FutureWarning)
pd.set_option('display.width', None)
pd.set_option('display.max_columns', 23)

# create a request header
headers = {'User-Agent': 'ibasco@seattleu.edu'}

# get all companies data
companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers)

# print(companyTickers.json()['0']['cik_str'])

companyCIK = pd.DataFrame.from_dict(companyTickers.json(), orient = 'index')
# print(companyCIK.to_string())

# adding zero's to CIK

companyCIK['cik_str'] = companyCIK['cik_str'].astype(str).str.zfill(10)
# print(companyCIK)

# selecting CIK entry # 420
x = 54
y = 55
cik = companyCIK[x:y].cik_str.iloc[0]
companyTitle = companyCIK[x:y].title.iloc[0]
print(cik)
print(companyTitle)
#
#
#SEC filling API call

companyFiling = requests.get(f'https://data.sec.gov/submissions/CIK{cik}.json', headers = headers)
# print(companyFiling.json()['filings'].keys())

allFilings = pd.DataFrame.from_dict((companyFiling.json()['filings']['files']))
print(allFilings)
print(allFilings['name'][0])

# pull historic data from SEC archive
companyFiling_archive = requests.get(f"https://data.sec.gov/submissions/{allFilings['name'][0]}", headers = headers)

# turn the archive into a dataframe
allFilings_archive_df = pd.DataFrame.from_dict(companyFiling_archive.json())
# print(companyFiling_archive.json())
# print(allFilings_archive_df)
#
#
# # pull all the unique filing types
uniqueFiling_types = allFilings_archive_df['form'].unique()
print(uniqueFiling_types)
#
form_4_filings = allFilings_archive_df[allFilings_archive_df['form'] == '8-K']
#
#
# create empty column to add stock price too
form_4_filings.loc[:,'stock price'] = 0
# print(form_4_filings)

for index, row in form_4_filings.iterrows():
    value = row['filingDate']

    tickerSymbol = companyCIK[x:y].ticker.iloc[0]
    # print(tickerSymbol)

    # start date for the api call
    start_date_str = value
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    # print(start_date)

    # calculate the delta
    end_date = start_date + timedelta(days=30)
    # print(end_date)

    # convert end date to str
    end_date_str = end_date.strftime('%Y-%m-%d')

    # create a yfinance ticker object
    ticker = yf.Ticker(tickerSymbol)

    # pull yfinance historical data
    historical_data = ticker.history(period='1d', start=start_date_str, end=end_date_str)

    historical_df = pd.DataFrame(historical_data)
    # print(historical_df)

    specific_data = historical_data.iloc[0]['Close']

    form_4_filings.at[index, 'stock price'] = specific_data

    # print(specific_data)
form_4_filings = form_4_filings.drop(columns=['items',
                                              'size',
                                              'isXBRL',
                                              'act',
                                              'isInlineXBRL',
                                              'primaryDocument',
                                              'primaryDocDescription'])
print(form_4_filings)
# #
#
# # graph filing vs stock price
pd.options.plotting.backend = "plotly"
graph = form_4_filings.plot(x = 'filingDate',
                            y = 'stock price',
                            title = f"Stock Price vs. Filing Date for {companyTitle} (NYSE: {tickerSymbol})",
                            labels = {'stock price':'Stock Price (USD)', 'filingDate':"Filing Date"})
graph.show()
