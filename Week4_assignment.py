# import all modules

import pandas as pd
import requests
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


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

# selecting CIK entry # 100
cik = companyCIK[111:112].cik_str.iloc[0]
companyTitle = companyCIK[111:112].title.iloc[0]
print(companyTitle, cik)


# get all companies facts data
companyFacts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers)
# print(companyFacts.json())
# print(companyFacts.json().keys())

# print only the facts - factual data from the SEC
# print(companyFacts.json()['facts'])
# print(companyFacts.json()['facts'].keys())
print(companyFacts.json()['facts']['us-gaap']['InventoryNet']['description'])
# print(companyFacts.json()['facts']['us-gaap']['SharePrice']['units'])
# print(companyFacts.json()['facts']['us-gaap']['MarketingExpense']['units']['USD'])
# print(companyFacts.json()['facts']['us-gaap']['Dividends']['units'].keys())

# marketingExpense_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['MarketingExpense']['units']['USD'])
# marketingExpense_df = marketingExpense_df[marketingExpense_df.frame.notna()]
# marketingExpense_df_filtered = marketingExpense_df[marketingExpense_df['form'] == '10-K']
# print(marketingExpense_df_filtered)
#

# D/E Ratio

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

# calculating ratio of debt to equity (debt ratio)
merge_dataframes['debt-to-equity ratio'] = merge_dataframes['debt'] / merge_dataframes['equity']
print(merge_dataframes)

# Current Ratio

currentAssets_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['AssetsCurrent']['units']['USD'])
currentAssets_df = currentAssets_df[currentAssets_df.frame.notna()]
currentAssets_df_filtered = currentAssets_df[currentAssets_df['form'] == '10-K']
currentAssets_df_filtered = currentAssets_df_filtered.rename(columns={'val' : 'current assets'})
# print(currentAssets_df_filtered)
# #
currentLiabilities_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['LiabilitiesCurrent']['units']['USD'])
currentLiabilities_df = currentLiabilities_df[currentLiabilities_df.frame.notna()]
currentLiabilities_df_filtered = currentLiabilities_df[currentLiabilities_df['form'] == '10-K']
currentLiabilities_df_filtered = currentLiabilities_df_filtered.rename(columns={'val' : 'current liabilities'})
# print(currentLiabilities_df_filtered)
#
# merge debt and equity dataframes
merge_currentRatio_dataframes = pd.merge(currentAssets_df_filtered, currentLiabilities_df_filtered, on = 'accn')
# print(merge_currentRatio_dataframes)

# calculating current ratio
merge_currentRatio_dataframes['current ratio'] = merge_currentRatio_dataframes['current assets'] / merge_currentRatio_dataframes['current liabilities']
print(merge_currentRatio_dataframes)


# Quick Ratio (acid test)

currentAssets_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['AssetsCurrent']['units']['USD'])
currentAssets_df = currentAssets_df[currentAssets_df.frame.notna()]
currentAssets_df_filtered = currentAssets_df[currentAssets_df['form'] == '10-K']
currentAssets_df_filtered = currentAssets_df_filtered.rename(columns={'val' : 'current assets'})
# print(currentAssets_df_filtered)

inventory_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['InventoryNet']['units']['USD'])
inventory_df = inventory_df[inventory_df.frame.notna()]
inventory_df_filtered = inventory_df[inventory_df['form'] == '10-K']
inventory_df_filtered = inventory_df_filtered.rename(columns={'val' : 'inventory'})
# print(inventory_df_filtered)

currentLiabilities_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['LiabilitiesCurrent']['units']['USD'])
currentLiabilities_df = currentLiabilities_df[currentLiabilities_df.frame.notna()]
currentLiabilities_df_filtered = currentLiabilities_df[currentLiabilities_df['form'] == '10-K']
currentLiabilities_df_filtered = currentLiabilities_df_filtered.rename(columns={'val' : 'current liabilities'})
# print(currentLiabilities_df_filtered)

# merge inventory, current assets and current liabilities dataframes
merge_quickRatio_dataframes = pd.merge(currentAssets_df_filtered, inventory_df_filtered, on = 'accn')
merge_quickRatio_dataframes = pd.merge(merge_quickRatio_dataframes, currentLiabilities_df_filtered, on = 'accn')
# print(merge_quickRatio_dataframes)

# calculating quick ratio
merge_quickRatio_dataframes['quick ratio'] = (merge_quickRatio_dataframes['current assets'] - merge_quickRatio_dataframes['inventory']) \
                                             / merge_currentRatio_dataframes['current liabilities']

# merge_quickRatio_dataframes = merge_dataframes.drop(merge_dataframes.columns[1:-1], axis = 1)
print(merge_quickRatio_dataframes)