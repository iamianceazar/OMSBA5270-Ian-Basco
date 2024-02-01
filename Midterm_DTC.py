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
companyCIK = pd.DataFrame.from_dict(companyTickers.json(), orient = 'index')

# adding zero's to CIK
companyCIK['cik_str'] = companyCIK['cik_str'].astype(str).str.zfill(10)
# selecting CIK entries
# 649:650 675:676
n = 2
a = 555
b = 556

# while n != 0:
#
#     cik = companyCIK[a:b].cik_str.iloc[0]
#     companyTitle = companyCIK[a:b].title.iloc[0]
#     print(companyTitle, cik)
#
#     # get all companies facts data
#     companyFacts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers)
#
#     ### Solvency Ratio - Debt-to-Equity ratio calculation
#
#     debt_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['Liabilities']['units']['USD'])
#     debt_df = debt_df[debt_df.frame.notna()]
#     debt_df_filtered = debt_df[debt_df['form'] == '10-K']
#     debt_df_filtered = debt_df_filtered.rename(columns={'val' : 'debt'})
#     # print(debt_df_filtered)
#
#     equity_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['StockholdersEquity']['units']['USD'])
#     equity_df = equity_df[equity_df.frame.notna()]
#     equity_df_filtered = equity_df[equity_df['form'] == '10-K']
#     equity_df_filtered = equity_df_filtered.rename(columns={'val' : 'equity'})
#     # print(equity_df_filtered)
#
#     # merge debt and equity dataframes
#     merge_dataframes = pd.merge(debt_df_filtered, equity_df_filtered, on = 'accn')
#     # print(merge_dataframes)
#
#     # calculating ratio of debt to equity (debt ratio)
#     merge_dataframes['debt-to-equity ratio'] = merge_dataframes['debt'] / merge_dataframes['equity']
#     print(merge_dataframes.groupby(['end_x'])['debt-to-equity ratio'].mean())
#
#     # pd.options.plotting.backend = "plotly"
#     # graph_net = merge_dataframes.plot(x = 'end_x',
#     #                                   y = ['debt-to-equity ratio'],
#     #                                   title=companyTitle + " Debt-to-Equity ratio",
#     #                                   labels={"end_x": "Year",
#     #                                           "value": "D/E Ratio"}
#     #                                   )
#     # graph_net.show()
#
#     ### Liquidity Ratios - Current Ratio and Quick Ratio calculations
#
#     # Current Ratio calculation
#     currentAssets_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['AssetsCurrent']['units']['USD'])
#     currentAssets_df = currentAssets_df[currentAssets_df.frame.notna()]
#     currentAssets_df_filtered = currentAssets_df[currentAssets_df['form'] == '10-K']
#     currentAssets_df_filtered = currentAssets_df_filtered.rename(columns={'val' : 'current assets'})
#     # print(currentAssets_df_filtered)
#
#     currentLiabilities_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['LiabilitiesCurrent']['units']['USD'])
#     currentLiabilities_df = currentLiabilities_df[currentLiabilities_df.frame.notna()]
#     currentLiabilities_df_filtered = currentLiabilities_df[currentLiabilities_df['form'] == '10-K']
#     currentLiabilities_df_filtered = currentLiabilities_df_filtered.rename(columns={'val' : 'current liabilities'})
#     # print(currentLiabilities_df_filtered)
#
#     # merge debt and equity dataframes
#     merge_currentRatio_dataframes = pd.merge(currentAssets_df_filtered, currentLiabilities_df_filtered, on = 'accn')
#     # print(merge_currentRatio_dataframes)
#
#     # calculating current ratio
#     merge_currentRatio_dataframes['current ratio'] = merge_currentRatio_dataframes['current assets'] / merge_currentRatio_dataframes['current liabilities']
#     print(merge_currentRatio_dataframes.groupby(['end_x'])['current ratio'].mean())
#
#     # Quick Ratio calculation
#
#     currentAssets_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['AssetsCurrent']['units']['USD'])
#     currentAssets_df = currentAssets_df[currentAssets_df.frame.notna()]
#     currentAssets_df_filtered = currentAssets_df[currentAssets_df['form'] == '10-K']
#     currentAssets_df_filtered = currentAssets_df_filtered.rename(columns={'val' : 'current assets'})
#     # print(currentAssets_df_filtered)
#
#     inventory_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['InventoryNet']['units']['USD'])
#     inventory_df = inventory_df[inventory_df.frame.notna()]
#     inventory_df_filtered = inventory_df[inventory_df['form'] == '10-K']
#     inventory_df_filtered = inventory_df_filtered.rename(columns={'val' : 'inventory'})
#     # print(inventory_df_filtered)
#
#     currentLiabilities_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['LiabilitiesCurrent']['units']['USD'])
#     currentLiabilities_df = currentLiabilities_df[currentLiabilities_df.frame.notna()]
#     currentLiabilities_df_filtered = currentLiabilities_df[currentLiabilities_df['form'] == '10-K']
#     currentLiabilities_df_filtered = currentLiabilities_df_filtered.rename(columns={'val' : 'current liabilities'})
#     # print(currentLiabilities_df_filtered)
#
#     # merge inventory, current assets and current liabilities dataframes
#     merge_quickRatio_dataframes = pd.merge(currentAssets_df_filtered, inventory_df_filtered, on = 'accn')
#     merge_quickRatio_dataframes = pd.merge(merge_quickRatio_dataframes, currentLiabilities_df_filtered, on = 'accn')
#     # print(merge_quickRatio_dataframes)
#
#     # calculating quick ratio
#     merge_quickRatio_dataframes['quick ratio'] = (merge_quickRatio_dataframes['current assets'] - merge_quickRatio_dataframes['inventory']) \
#                                                  / merge_currentRatio_dataframes['current liabilities']
#
#     print(merge_quickRatio_dataframes.groupby(['end_x'])['quick ratio'].mean())
#
#     ### Profitability Ratios - gross profit margin calculation
#
#     grossProfit = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['GrossProfit']['units']['USD'])
#     grossProfit = grossProfit[grossProfit.frame.notna()]
#     grossProfit_filtered = grossProfit[grossProfit['form'] == '10-K']
#     grossProfit_filtered = grossProfit_filtered.rename(columns={'val': 'gross profit'})
#
#     revenue_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['SalesRevenueNet']['units']['USD'])
#     revenue_df = revenue_df[revenue_df.frame.notna()]
#     revenue_df_filtered = revenue_df[revenue_df['form'] == '10-K']
#     revenue_df_filtered = revenue_df_filtered.rename(columns={'val': 'revenue'})
#
#     # merge netProfit and revenue_df dataframes
#     merge_dataframes = pd.merge(grossProfit_filtered, revenue_df_filtered, on='accn')
#
#     merge_dataframes['gross profit margin'] = ((merge_dataframes['gross profit'] /
#                                                 merge_dataframes['revenue']) * 100)
#     # print(merge_dataframes.groupby(['fy_x'])['gross profit margin'].sum())
#     # print(merge_dataframes.groupby(['fy_x']).apply(lambda x: merge_dataframes['gross profit']/merge_dataframes['revenue']))
#     print(merge_dataframes.groupby(['fy_x'])['gross profit margin'].mean())
#
#     # Interest ratio
#     grossProfit = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['GrossProfit']['units']['USD'])
#     grossProfit = grossProfit[grossProfit.frame.notna()]
#     grossProfit_filtered = grossProfit[grossProfit['form'] == '10-K']
#     grossProfit_filtered = grossProfit_filtered.rename(columns={'val': 'gross profit'})
#
#     operatingExpense = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['OperatingExpenses']['units']['USD'])
#     operatingExpense = operatingExpense[operatingExpense.frame.notna()]
#     operatingExpense_filtered = operatingExpense[operatingExpense['form'] == '10-K']
#     operatingExpense_filtered = operatingExpense_filtered.rename(columns={'val': 'operating expense'})
#     print(operatingExpense_filtered)
#
#     interestExpense_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['InterestExpense']['units']['USD'])
#     interestExpense_df = interestExpense_df[interestExpense_df.frame.notna()]
#     interestExpense_df_filtered = interestExpense_df[interestExpense_df['form'] == '10-K']
#     interestExpense_df_filtered = interestExpense_df_filtered.rename(columns={'val': 'interest expense'})
#     print(interestExpense_df_filtered)
#
#
#     a -= 26
#     b -= 26
#     n -= 1


## Profitability Ratios - gross profit margin and  Ratio calculations

cik = companyCIK[555:556].cik_str.iloc[0]
companyTitle = companyCIK[555:556].title.iloc[0]
print(companyTitle, cik)

# get all companies facts data
companyFacts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers)

grossProfit = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['GrossProfit']['units']['USD'])
grossProfit = grossProfit[grossProfit.frame.notna()]
grossProfit_filtered = grossProfit[grossProfit['form'] == '10-K']
grossProfit_filtered = grossProfit_filtered.rename(columns={'val': 'gross profit'})

revenue_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['SalesRevenueNet']['units']['USD'])
revenue_df = revenue_df[revenue_df.frame.notna()]
revenue_df_filtered = revenue_df[revenue_df['form'] == '10-K']
revenue_df_filtered = revenue_df_filtered.rename(columns={'val': 'revenue'})

# merge netProfit and revenue_df dataframes
merge_dataframes = pd.merge(grossProfit_filtered, revenue_df_filtered, on='accn')

merge_dataframes['gross profit margin'] = ((merge_dataframes['gross profit'] /
                                         merge_dataframes['revenue']) * 100)
# print(merge_dataframes.groupby(['fy_x'])['gross profit margin'].sum())
# print(merge_dataframes.groupby(['fy_x']).apply(lambda x: merge_dataframes['gross profit']/merge_dataframes['revenue']))
print(merge_dataframes.groupby(['fy_x'])['gross profit margin'].mean())


cik = companyCIK[529:530].cik_str.iloc[0]
companyTitle = companyCIK[529:530].title.iloc[0]
print(companyTitle, cik)

# get all companies facts data
companyFacts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers)

grossProfit = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['GrossProfit']['units']['USD'])
grossProfit = grossProfit[grossProfit.frame.notna()]
grossProfit_filtered = grossProfit[grossProfit['form'] == '10-K']
grossProfit_filtered = grossProfit_filtered.rename(columns={'val': 'gross profit'})

revenue_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['SalesRevenueNet']['units']['USD'])
revenue_df = revenue_df[revenue_df.frame.notna()]
revenue_df_filtered = revenue_df[revenue_df['form'] == '10-K']
revenue_df_filtered = revenue_df_filtered.rename(columns={'val': 'revenue'})

# merge netProfit and revenue_df dataframes
merge_dataframes = pd.merge(grossProfit_filtered, revenue_df_filtered, on='accn')

merge_dataframes['gross profit margin'] = ((merge_dataframes['gross profit'] /
                                         merge_dataframes['revenue']) * 100)
# print(merge_dataframes.groupby(['fy_x'])['gross profit margin'].sum())
# print(merge_dataframes.groupby(['fy_x']).apply(lambda x: merge_dataframes['gross profit']/merge_dataframes['revenue']))
print(merge_dataframes.groupby(['fy_x'])['gross profit margin'].mean())