# import all modules

import pandas as pd
import requests
import matplotlib.pyplot as plt

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 23)
pd.options.display.float_format = '{:.2f}'.format

# create a request header
headers = {'User-Agent': 'ibasco@seattleu.edu'}

# get all companies data
companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers)
companyCIK = pd.DataFrame.from_dict(companyTickers.json(), orient = 'index')

# adding zero's to CIK
companyCIK['cik_str'] = companyCIK['cik_str'].astype(str).str.zfill(10)

# selecting CIK (Philip Morris)
a = 77 #76 77
b = 78
cik = companyCIK[a:b].cik_str.iloc[0]
companyTitle = companyCIK[a:b].title.iloc[0]
tickerSymbol = companyCIK[a:b].ticker.iloc[0]
print(companyTitle, "\n", "Ticker:", tickerSymbol, "\n", "CIK:", cik)
cik = "0001413329"
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
# print(dividend_df_filtered)

# pd.options.plotting.backend = "plotly"
# graph_marketing = dividend_df_filtered.plot(x = "end",
#                                             y = "dividend distribution",
#                                             title = companyTitle + f" dividend payments from 2007 to 2023",
#                                             labels={"end": "Year",
#                                                     "dividend distribution": "Dividend distribution (USD)"}
#                                             )
# graph_marketing.show()


salesRevenue_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['SalesRevenueNet']['units']['USD'])
salesRevenue_df = salesRevenue_df[salesRevenue_df.frame.notna()]
salesRevenue_df_filtered = salesRevenue_df[salesRevenue_df['form'] == '10-K']
salesRevenue_df_filtered = salesRevenue_df_filtered.rename(columns={'val' : 'sales revenue'})
grouped_salesRevenue = salesRevenue_df_filtered.groupby('fy')['sales revenue'].sum().reset_index()
# print(salesRevenue_df_filtered)
# print(grouped_salesRevenue)
#
# pd.options.plotting.backend = "plotly"
# graph_marketing = grouped_salesRevenue.plot(x = "fy",
#                                             y = "sales revenue",
#                                             title = companyTitle + f" sales revenue from 2009 to 2017",
#                                             labels={"fy": "Year",
#                                                     "sales revenue": "Sales revenue (USD)"}
#                                             )
# graph_marketing.show()

# D/E Ratio calculation
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
# print(merge_dataframes)
grouped_merge_dataframes = merge_dataframes.groupby('end_x').agg({'debt': 'mean', 'equity': 'mean'}).reset_index()
# print(grouped_merge_dataframes)

# calculating ratio of debt to equity (debt ratio)
grouped_merge_dataframes['debt-to-equity ratio'] = grouped_merge_dataframes['debt'] / grouped_merge_dataframes['equity']
print(grouped_merge_dataframes)

# Current Ratio calculation

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

# calculating ratio of debt to equity (debt ratio)
grouped_merge_dataframes['current ratio'] = grouped_merge_dataframes['current assets'] / grouped_merge_dataframes['current liabilities']
print(grouped_merge_dataframes)

# Gross profit margin calculation

grossProfit = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['GrossProfit']['units']['USD'])
grossProfit = grossProfit[grossProfit.frame.notna()]
grossProfit_filtered = grossProfit[grossProfit['form'] == '10-K']
grossProfit_filtered = grossProfit_filtered.rename(columns={'val': 'gross profit'})

# merge_dataframes = pd.merge(grossProfit_filtered, salesRevenue_df_filtered, on = 'accn')
# print(merge_dataframes.to_string())
# grouped_merge_dataframes = merge_dataframes.groupby('fy_x').agg({'gross profit': 'mean', 'sales revenue': 'sum'}).reset_index()
# print(grouped_merge_dataframes)
#
# # calculating ratio of debt to equity (debt ratio)
# grouped_merge_dataframes['current ratio'] = grouped_merge_dataframes['current assets'] / grouped_merge_dataframes['current liabilities']
# print(grouped_merge_dataframes)