# import all modules
import matplotlib.pyplot as plt
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import requests
import yfinance as yf
from datetime import datetime, timedelta
import warnings

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 23)
pd.options.display.float_format = '{:.2f}'.format
warnings.simplefilter(action='ignore', category=FutureWarning)

# desired stock symbol
# allows for input of stock symbol and change for testing
stock_symbol = 'PM'
print(stock_symbol)
# create a request header
headers = {'User-Agent': 'ibasco@seattleu.edu'}

# get all companies data
companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers)
companyCIK = pd.DataFrame.from_dict(companyTickers.json(), orient = 'index')

# adding zero's to CIK
companyCIK['cik_str'] = companyCIK['cik_str'].astype(str).str.zfill(10)

company_information = companyCIK[companyCIK['ticker'] == stock_symbol]
cik = company_information['cik_str'].values[0]
companyTitle = company_information.title.iloc[0]
print(companyTitle)

# get all companies facts data
companyFacts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers)

print(companyFacts.json()['facts']['us-gaap']['StockholdersEquity']['description'])
# print(companyFacts.json()['facts']['us-gaap']['SalesRevenueNet']['units'])

# Check the dividend payments that shareholders receive
# print(companyFacts.json()['facts']['us-gaap']['PaymentsOfDividends']['description'])
dividends_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['PaymentsOfDividends']['units']['USD'])
dividends_df = dividends_df[dividends_df.frame.notna()]
dividend_df_filtered = dividends_df[dividends_df['form'] == '10-K']
dividend_df_filtered = dividend_df_filtered.rename(columns={'val' : 'dividend distribution'})
print(dividend_df_filtered[['end','dividend distribution']])

pd.options.plotting.backend = "plotly"
graph_marketing = dividend_df_filtered.plot(x = "end",
                                            y = "dividend distribution",
                                            title = companyTitle + f" dividend payments from 2007 to 2023",
                                            labels={"end": "Year",
                                                    "dividend distribution": "Dividend distribution (USD)"}
                                            )
graph_marketing.show()

salesRevenue_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['SalesRevenueNet']['units']['USD'])
salesRevenue_df = salesRevenue_df[salesRevenue_df.frame.notna()]
salesRevenue_df_filtered = salesRevenue_df[salesRevenue_df['form'] == '10-K']
salesRevenue_df_filtered = salesRevenue_df_filtered.rename(columns={'val' : 'sales revenue'})
grouped_salesRevenue = salesRevenue_df_filtered.groupby('fy')['sales revenue'].sum().reset_index()
# print(salesRevenue_df_filtered)
print(grouped_salesRevenue)
#
pd.options.plotting.backend = "plotly"
graph_marketing = grouped_salesRevenue.plot(x = "fy",
                                            y = "sales revenue",
                                            title = companyTitle + f" sales revenue from 2009 to 2017",
                                            labels={"fy": "Year",
                                                    "sales revenue": "Sales revenue (USD)"}
                                            )
graph_marketing.show()

### D/E Ratio calculation
debt_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['Liabilities']['units']['USD'])
debt_df = debt_df[debt_df.frame.notna()]
debt_df_filtered = debt_df[debt_df['form'] == '10-K']
debt_df_filtered = debt_df_filtered.rename(columns={'val' : 'debt'})
# print(debt_df_filtered)

equity_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['StockholdersEquity']['units']['USD'])
equity_df = equity_df[equity_df.frame.notna()]
equity_df_filtered = equity_df[equity_df['form'] == '10-K']
equity_df_filtered = equity_df_filtered.rename(columns={'val' : 'equity'})
# print(equity_df_filtered)

# merge debt and equity dataframes
merge_dataframes = pd.merge(debt_df_filtered, equity_df_filtered, on = 'accn')
grouped_merge_dataframes = merge_dataframes.groupby('end_x').agg({'debt': 'mean', 'equity': 'mean'}).reset_index()
# print(grouped_merge_dataframes)

# calculating ratio of debt to equity (debt ratio)
grouped_merge_dataframes['debt-to-equity ratio'] = grouped_merge_dataframes['debt'] / grouped_merge_dataframes['equity']
print(grouped_merge_dataframes)

pd.options.plotting.backend = "plotly"
graph1 = grouped_merge_dataframes.plot(x = "end_x",
                                       y = "debt-to-equity ratio",
                                       title = companyTitle + " Debt-to-Equity ratio",
                                       labels={"end_x": "Year End",
                                               "debt-to-equity ratio": "Debt-to-Equity ratio"}
                                       )
graph1.show()

### Current Ratio calculation

currentAssets_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['AssetsCurrent']['units']['USD'])
currentAssets_df = currentAssets_df[currentAssets_df.frame.notna()]
currentAssets_df_filtered = currentAssets_df[currentAssets_df['form'] == '10-K']
currentAssets_df_filtered = currentAssets_df_filtered.rename(columns={'val' : 'current assets'})
# print(currentAssets_df_filtered)

currentLiabilities_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['LiabilitiesCurrent']['units']['USD'])
currentLiabilities_df = currentLiabilities_df[currentLiabilities_df.frame.notna()]
currentLiabilities_df_filtered = currentLiabilities_df[currentLiabilities_df['form'] == '10-K']
currentLiabilities_df_filtered = currentLiabilities_df_filtered.rename(columns={'val' : 'current liabilities'})
# print(currentLiabilities_df_filtered)

merge_dataframes = pd.merge(currentAssets_df_filtered, currentLiabilities_df_filtered, on = 'accn')
# print(merge_dataframes)
grouped_merge_dataframes = merge_dataframes.groupby('end_x').agg({'current assets': 'mean', 'current liabilities': 'mean'}).reset_index()
# print(grouped_merge_dataframes.to_string())

# calculating current ratio
grouped_merge_dataframes['current ratio'] = grouped_merge_dataframes['current assets'] / grouped_merge_dataframes['current liabilities']
print(grouped_merge_dataframes)

pd.options.plotting.backend = "plotly"
graph2 = grouped_merge_dataframes.plot(x = "end_x",
                                       y = "current ratio",
                                       title = companyTitle + " Current ratio",
                                       labels={"end_x": "Year End",
                                               "current ratio": "Current ratio"}
                                       )
graph2.show()

### Return on Equity calculation

grossProfit = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['GrossProfit']['units']['USD'])
grossProfit = grossProfit[grossProfit.frame.notna()]
grossProfit_filtered = grossProfit[grossProfit['form'] == '10-K']
grossProfit_filtered = grossProfit_filtered.rename(columns={'val': 'profit'})

merge_dataframes = pd.merge(grossProfit_filtered, equity_df_filtered, on = 'accn')
merge_dataframes = merge_dataframes.groupby('fy_x').agg({'profit': 'sum', 'equity': 'sum'}).reset_index()
merge_dataframes['ROE'] = merge_dataframes['profit'] / merge_dataframes['equity']
print(merge_dataframes)

pd.options.plotting.backend = "plotly"
graph3 = merge_dataframes.plot(x = "fy_x",
                              y = "ROE",
                              title = companyTitle + " Return on Equity",
                              labels={"fy_x": "File Year",
                                      "ROE": "Return on Equity"}
                              )
graph3.show()


#SEC filling API call

companyFiling = requests.get(f'https://data.sec.gov/submissions/CIK{cik}.json', headers = headers)
# print(companyFiling.json()['filings'].keys())

allFilings = pd.DataFrame.from_dict((companyFiling.json()['filings']['files']))
# print(allFilings)
# print(allFilings['name'][0])

# pull historic data from SEC archive
companyFiling_archive = requests.get(f"https://data.sec.gov/submissions/{allFilings['name'][0]}", headers = headers)

# turn the archive into a dataframe
allFilings_archive_df = pd.DataFrame.from_dict(companyFiling_archive.json())
# print(companyFiling_archive.json())
# print(allFilings_archive_df)

# pull all the unique filing types
uniqueFiling_types = allFilings_archive_df['form'].unique()
# print(uniqueFiling_types)
#
form_4_filings = allFilings_archive_df[allFilings_archive_df['form'] == '10-Q']

# create empty column to add stock price too
form_4_filings.loc[:,'stock price'] = 0
# print(form_4_filings)

for index, row in form_4_filings.iterrows():
    value = row['filingDate']

    tickerSymbol = stock_symbol
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
print(form_4_filings[['filingDate','stock price',  'form']])

# graph filing vs stock price
pd.options.plotting.backend = "plotly"
graph = form_4_filings.plot(x = 'filingDate',
                            y = 'stock price',
                            title = f"Stock Price vs. Filing Date for {companyTitle} (NYSE: {tickerSymbol})",
                            labels = {'stock price':'Stock Price (USD)', 'filingDate':"Filing Date"})
graph.show()

allFilings_cor = pd.DataFrame.from_dict(companyFiling.json()['filings']['recent'])
filtered_df = allFilings_cor[allFilings_cor['form'] == '10-Q']
filtered_df = filtered_df[['accessionNumber', 'reportDate', 'form']]
# print(filtered_df)

# define the timeframe for data that we want to look at
start_date = '2020-03-01' # 03/11 COVID was declared a pandemic by WHO
end_date = '2020-03-31'

filtered_df = filtered_df[(filtered_df['reportDate'] >= start_date) & (filtered_df['reportDate'] <= end_date)]

# start the stock integration with yfinance
stock_prices_df = pd.DataFrame()


# step 1: convert reportDate to datetime
filtered_df['reportDate'] = pd.to_datetime(filtered_df['reportDate'])
# set ticker symbol equal to stock_symbol
ticker_symbol = stock_symbol


# write function for getting stock price
def get_stock_price(ticker_symbol, filing_dates):
    prices = {'reportDate': [], '0_days_after': [], '30_days_after': [], '60_days_after': [], '90_days_after': [],
              '120_days_after': []}

    for filing_date in filing_dates:
        for days_after in [0, 30, 60, 90, 120]:
            target_date = filing_date + timedelta(days=days_after)

            # adjust for weekends
            if target_date.weekday() == 5:
                target_date += timedelta(days=2)
            elif target_date.weekday() == 6:
                target_date += timedelta(days=1)

            try:
                historical_data = yf.download(ticker_symbol, start=target_date.strftime('%Y-%m-%d'),
                                              end=(target_date + timedelta(days=1)).strftime('%Y-%m-%d'))
                if not historical_data.empty:
                    price = historical_data['Close'].values[0]

                else:
                    price = None
            except Exception as e:
                print(f'Error fetching data for {ticker_symbol} on {target_date}: {e}')
                price = None

            prices[f'{days_after}_days_after'].append(price)
        prices['reportDate'].append(filing_date)
    return pd.DataFrame(prices)


stock_prices_df = get_stock_price(ticker_symbol, filtered_df['reportDate'])

print(stock_prices_df)

# melt the dataframe to turn on axis for easier graphing
melted_df = pd.melt(stock_prices_df, id_vars=['reportDate'], var_name='Days After', value_name='Stock Price')

print(melted_df)

import plotly.express as px

# convert days after to strftime in stead of date time
melted_df['Days After'] = melted_df['Days After'].astype(str) + ' days after'

print(melted_df)
#
fig = px.line(melted_df, x='Days After', y= 'Stock Price',
              title= f'Stock Price Evolution After Filing Dates {stock_symbol} {start_date} <-> {end_date}',
              labels={'Days After': 'Period After Filing', 'reportDate': 'Report Date', 'Stock Price': 'Stock Price ($)'})

fig.update_layout(
        xaxis_title='Report Date',
        yaxis_title='Stock Price ($)',
        legend_title='Time After Filing',

)


fig.show()