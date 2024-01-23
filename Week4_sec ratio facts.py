# import all modules

import pandas as pd
import requests
import plotly.express as px

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 15)

# create a request header
headers = {'User-Agent': 'ibasco@seattleu.edu'}

# get all companies data
companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers)

# print(companyTickers.json()['0']['cik_str'])

companyCIK = pd.DataFrame.from_dict(companyTickers.json(), orient = 'index')
print(companyCIK)

# adding zero's to CIK

companyCIK['cik_str'] = companyCIK['cik_str'].astype(str).str.zfill(10)
print(companyCIK)

# selecting CIK entry # 13
cik = companyCIK[0:1].cik_str.iloc[0]
companyTitle = companyCIK[0:1].title.iloc[0]
print(companyTitle, cik)
#

# get all companies facts data
companyFacts = requests.get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", headers=headers)
# print(companyFacts.json())
# print(companyFacts.json().keys())

# print only the facts - factual data from the SEC
# print(companyFacts.json()['facts'])
# print(companyFacts.json()['facts'].keys())
# print(companyFacts.json()['facts']['us-gaap'].keys())
# print(companyFacts.json()['facts']['us-gaap']['Revenues'].keys())
# print(companyFacts.json()['facts']['us-gaap']['Revenues']['description'])
# print(companyFacts.json()['facts']['us-gaap']['Revenues']['units'].keys())

# convert the facts on assets to a dataframe
assets_dataframe = pd.DataFrame.from_dict((companyFacts.json()['facts']['us-gaap']['Assets']['units']['USD']))
# print(assets_dataframe)

assets_dataframe = assets_dataframe[assets_dataframe.frame.notna()]
# print(assets_dataframe)

# pull all liabilities to filter and later merge
liabilities_dataframe = pd.DataFrame.from_dict((companyFacts.json()['facts']['us-gaap']['Liabilities']['units']['USD']))
# print(liabilities_dataframe)

liabilities_dataframe = liabilities_dataframe[liabilities_dataframe.frame.notna()]
# print(liabilities_dataframe)

assets_dataframe_filtered = assets_dataframe[assets_dataframe['form'] == '10-K']
liabilities_dataframe_filtered = liabilities_dataframe[liabilities_dataframe['form'] == '10-K']
print(assets_dataframe_filtered,'\n',liabilities_dataframe_filtered)

# merge assets and liabilities dataframes
merge_dataframes = pd.merge(assets_dataframe_filtered, liabilities_dataframe_filtered, on = 'accn')
print(merge_dataframes)

merge_dataframes = merge_dataframes.drop(merge_dataframes.columns[10:], axis = 1)
print(merge_dataframes)

# calculating ratio of assets to liabilities (debt ratio)
merge_dataframes['ratio_assets_liabilities'] = merge_dataframes['val_y'] / merge_dataframes['val_x']
print(merge_dataframes)

# import plotly.express package and graph the data
pd.options.plotting.backend = "plotly"
graph = merge_dataframes.plot(x = "filed_x",
                              y = "ratio_assets_liabilities",
                              title = companyTitle + " ratio of assets and liabilities",
                              labels={"filed_x": "Quarter End Data",
                                      "ratio_assets_liabilities": "Ratio of assets and liabilities"}
                              )
graph.show()