# import all modules

import pandas as pd
import requests
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
a = 555
b = 556

# Create empty dataframes. This will be used to store data for visualization.
df1 = pd.DataFrame()
df2 = pd.DataFrame()
dficr1 = pd.DataFrame()
dficr2 = pd.DataFrame()
dfcurrentratio1 = pd.DataFrame()
dfcurrentratio2 = pd.DataFrame()
dfquickratio1 = pd.DataFrame()
dfquickratio2 = pd.DataFrame()
dfgrossprofitmargin1 = pd.DataFrame()
dfgrossprofitmargin2 = pd.DataFrame()

# loops through the code twice
n = 2
while n != 0:
    # Grabbing the company name and CIK
    cik = companyCIK[a:b].cik_str.iloc[0]
    companyTitle = companyCIK[a:b].title.iloc[0]
    print(companyTitle, "CIK: " + cik)

    # get all companies facts data
    companyFacts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers)

    ### Solvency Ratios - Debt-to-Equity and Interest Coverage ratio calculations

    # Debt-to-Equity ratio
    debt_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['Liabilities']['units']['USD'])
    debt_df = debt_df[debt_df.frame.notna()]
    debt_df_filtered = debt_df[debt_df['form'] == '10-K']
    debt_df_filtered = debt_df_filtered.rename(columns={'val' : 'debt'})

    equity_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['StockholdersEquity']['units']['USD'])
    equity_df = equity_df[equity_df.frame.notna()]
    equity_df_filtered = equity_df[equity_df['form'] == '10-K']
    equity_df_filtered = equity_df_filtered.rename(columns={'val' : 'equity'})

    # merge debt and equity dataframes
    merge_DEratio_dataframes = pd.merge(debt_df_filtered, equity_df_filtered, on = 'accn')

    # calculating debt-to-equity ratio
    merge_DEratio_dataframes['debt-to-equity ratio'] = merge_DEratio_dataframes['debt'] / merge_DEratio_dataframes['equity']
    merge_DEratio_dataframes = merge_DEratio_dataframes.groupby(['fy_x'])['debt-to-equity ratio'].mean().reset_index().rename(columns = {'fy_x' : 'fiscal year'})

    # Interest Coverage Ratio
    grossProfit = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['GrossProfit']['units']['USD'])
    grossProfit = grossProfit[grossProfit.frame.notna()]
    grossProfit_filtered = grossProfit[grossProfit['form'] == '10-K']
    grossProfit_filtered = grossProfit_filtered.rename(columns={'val': 'gross profit'})

    SGandA_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['SellingGeneralAndAdministrativeExpense']['units']['USD'])
    SGandA_df = SGandA_df[SGandA_df.frame.notna()]
    SGandA_df_filtered = SGandA_df[SGandA_df['form'] == '10-K']
    SGandA_df_filtered = SGandA_df_filtered.rename(columns={'val': 'SG&A'})

    interestExpense_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['InterestExpense']['units']['USD'])
    interestExpense_df = interestExpense_df[interestExpense_df.frame.notna()]
    interestExpense_df_filtered = interestExpense_df[interestExpense_df['form'] == '10-K']
    interestExpense_df_filtered = interestExpense_df_filtered.rename(columns={'val': 'interest expense'})

    # merging gross profit, selling general and admin expenses and interest expense dataframes
    merge_interestCoverage_df = pd.merge(pd.merge(grossProfit_filtered, SGandA_df_filtered, on='accn'), interestExpense_df_filtered, on = 'accn')

    # calculating interest coverage ratio
    merge_interestCoverage_df['interest coverage ratio'] = (merge_interestCoverage_df['gross profit'] - merge_interestCoverage_df['SG&A'])/ merge_interestCoverage_df['interest expense']
    merge_interestCoverage_df = merge_interestCoverage_df.groupby(['fy_x'])['interest coverage ratio'].mean().reset_index().rename(columns={'fy_x': 'fiscal year'})

    ### Liquidity Ratios - Current Ratio and Quick Ratio calculations

    # Current Ratio calculation

    currentAssets_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['AssetsCurrent']['units']['USD'])
    currentAssets_df = currentAssets_df[currentAssets_df.frame.notna()]
    currentAssets_df_filtered = currentAssets_df[currentAssets_df['form'] == '10-K']
    currentAssets_df_filtered = currentAssets_df_filtered.rename(columns={'val' : 'current assets'})

    currentLiabilities_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['LiabilitiesCurrent']['units']['USD'])
    currentLiabilities_df = currentLiabilities_df[currentLiabilities_df.frame.notna()]
    currentLiabilities_df_filtered = currentLiabilities_df[currentLiabilities_df['form'] == '10-K']
    currentLiabilities_df_filtered = currentLiabilities_df_filtered.rename(columns={'val' : 'current liabilities'})

    # merge current assets with current liabilities dataframes
    merge_currentRatio_dataframes = pd.merge(currentAssets_df_filtered, currentLiabilities_df_filtered, on = 'accn')

    # calculating current ratio
    merge_currentRatio_dataframes['current ratio'] = merge_currentRatio_dataframes['current assets'] / merge_currentRatio_dataframes['current liabilities']
    merged_currentRatio_dataframes = merge_currentRatio_dataframes.groupby(['fy_x'])['current ratio'].mean().reset_index().rename(columns = {'fy_x' : 'fiscal year'})

    # Quick Ratio calculation

    currentAssets_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['AssetsCurrent']['units']['USD'])
    currentAssets_df = currentAssets_df[currentAssets_df.frame.notna()]
    currentAssets_df_filtered = currentAssets_df[currentAssets_df['form'] == '10-K']
    currentAssets_df_filtered = currentAssets_df_filtered.rename(columns={'val' : 'current assets'})

    inventory_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['InventoryNet']['units']['USD'])
    inventory_df = inventory_df[inventory_df.frame.notna()]
    inventory_df_filtered = inventory_df[inventory_df['form'] == '10-K']
    inventory_df_filtered = inventory_df_filtered.rename(columns={'val' : 'inventory'})

    currentLiabilities_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['LiabilitiesCurrent']['units']['USD'])
    currentLiabilities_df = currentLiabilities_df[currentLiabilities_df.frame.notna()]
    currentLiabilities_df_filtered = currentLiabilities_df[currentLiabilities_df['form'] == '10-K']
    currentLiabilities_df_filtered = currentLiabilities_df_filtered.rename(columns={'val' : 'current liabilities'})

    # merge inventory, current assets and current liabilities dataframes
    merge_quickRatio_dataframes = pd.merge(currentAssets_df_filtered, inventory_df_filtered, on = 'accn')
    merge_quickRatio_dataframes = pd.merge(merge_quickRatio_dataframes, currentLiabilities_df_filtered, on = 'accn')

    # calculating quick ratio
    merge_quickRatio_dataframes['quick ratio'] = (merge_quickRatio_dataframes['current assets'] - merge_quickRatio_dataframes['inventory']) \
                                                 / merge_currentRatio_dataframes['current liabilities']
    merge_quickRatio_dataframes = merge_quickRatio_dataframes.groupby(['fy_x'])['quick ratio'].mean().reset_index().rename(columns = {'fy_x' : 'fiscal year'})


    ### Profitability Ratios - gross profit margin calculation

    grossProfit = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['GrossProfit']['units']['USD'])
    grossProfit = grossProfit[grossProfit.frame.notna()]
    grossProfit_filtered = grossProfit[grossProfit['form'] == '10-K']
    grossProfit_filtered = grossProfit_filtered.rename(columns={'val': 'gross profit'})

    revenue_df = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['SalesRevenueNet']['units']['USD'])
    revenue_df = revenue_df[revenue_df.frame.notna()]
    revenue_df_filtered = revenue_df[revenue_df['form'] == '10-K']
    revenue_df_filtered = revenue_df_filtered.rename(columns={'val': 'revenue'})

    # merge gross profit and revenue dataframes
    merge_grossProfitMargin_dataframes = pd.merge(grossProfit_filtered, revenue_df_filtered, on='accn')

    # calculating gross profit margin
    merge_grossProfitMargin_dataframes['gross profit margin'] = ((merge_grossProfitMargin_dataframes['gross profit'] /
                                                merge_grossProfitMargin_dataframes['revenue']) * 100)
    merge_grossProfitMargin_dataframes = merge_grossProfitMargin_dataframes.groupby(['fy_x'])['gross profit margin'].mean().reset_index().rename(columns = {'fy_x' : 'fiscal year'})

    # prints all the results
    print(merge_DEratio_dataframes)
    print(merge_interestCoverage_df)
    print(merged_currentRatio_dataframes)
    print(merge_quickRatio_dataframes)
    print(merge_grossProfitMargin_dataframes)

    # Changes the CIK to the second company
    a -= 26
    b -= 26

    # final loop
    n -= 1

    # stores the result to the empty data frames created at the beginning of the code
    if n == 1:
        df1 = df1._append(merge_DEratio_dataframes)
        dficr1 = dficr1._append(merge_interestCoverage_df)
        dfcurrentratio1 = dfcurrentratio1._append(merged_currentRatio_dataframes)
        dfquickratio1 = dfquickratio1._append(merge_quickRatio_dataframes)
        dfgrossprofitmargin1 = dfgrossprofitmargin1._append(merge_grossProfitMargin_dataframes)
    else:
        df2 = df2._append(merge_DEratio_dataframes)
        dficr2 = dficr2._append(merge_interestCoverage_df)
        dfcurrentratio2 = dfcurrentratio2._append(merged_currentRatio_dataframes)
        dfquickratio2 = dfquickratio2._append(merge_quickRatio_dataframes)
        dfgrossprofitmargin2 = dfgrossprofitmargin2._append(merge_grossProfitMargin_dataframes)


### Visualization

# D/E Ratio comparison between Baxter and Dover
ax1 = df2.plot(x = 'fiscal year',  y = 'debt-to-equity ratio', label = 'Dover Corporation')
df1.plot(ax = ax1, x = 'fiscal year', y = 'debt-to-equity ratio', label = 'Baxter International')
plt.xlabel('Fiscal Year')
plt.ylabel('D/E Ratio')

# Interest Coverage Ratio comparison between Baxter and Dover
ax2 = dficr2.plot(x = 'fiscal year',  y = 'interest coverage ratio', label = 'Dover Corporation')
dficr1.plot(ax = ax2, x = 'fiscal year', y = 'interest coverage ratio', label = 'Baxter International')
plt.xlabel('Fiscal Year')
plt.ylabel('Interest Coverage Ratio')

# Current Ratio comparison between Baxter and Dover
ax3 = dfcurrentratio2.plot(x = 'fiscal year',  y = 'current ratio', label = 'Dover Corporation')
dfcurrentratio1.plot(ax = ax3, x = 'fiscal year', y = 'current ratio', label = 'Baxter International')
plt.xlabel('Fiscal Year')
plt.ylabel('Current Ratio')

# Quick Ratio comparison between Baxter and Dover
ax4 = dfquickratio2.plot(x = 'fiscal year',  y = 'quick ratio', label = 'Dover Corporation')
dfquickratio1.plot(ax = ax4, x = 'fiscal year', y = 'quick ratio', label = 'Baxter International')
plt.xlabel('Fiscal Year')
plt.ylabel('Quick Ratio')

# Gross Profit Margin comparison between Baxter and Dover
ax5 = dfgrossprofitmargin2.plot(x = 'fiscal year',  y = 'gross profit margin', label = 'Dover Corporation')
dfgrossprofitmargin1.plot(ax = ax5, x = 'fiscal year', y = 'gross profit margin', label = 'Baxter International')
plt.xlabel('Fiscal Year')
plt.ylabel('Gross Profit Margin')

plt.show()
