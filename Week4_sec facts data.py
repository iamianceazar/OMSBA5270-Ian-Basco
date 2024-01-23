# import the modules

import pandas as pd
import requests
import plotly.express as px

pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 14)

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

# selecting CIK entry # 100
cik = companyCIK[99:100].cik_str.iloc[0]
companyTitle = companyCIK[99:100].title.iloc[0]
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
print(companyFacts.json()['facts']['us-gaap']['Revenues']['description'])
#print(companyFacts.json()['facts']['us-gaap']['Revenues']['units'].keys())

# convert the facts on revenues to a dataframe
revenues_dataframe = pd.DataFrame.from_dict((companyFacts.json()['facts']['us-gaap']['Revenues']['units']['USD']))
print(revenues_dataframe)

revenues_dataframe = revenues_dataframe[revenues_dataframe.frame.notna()]
print(revenues_dataframe)

# import plotly.express package and graph the data
pd.options.plotting.backend = "plotly"
graph = revenues_dataframe.plot(x = 'end',
                                y = "val",
                                title = companyTitle + " Revenues",
                                labels = {"val" : "value in dollas ($)",
                                          "end" : "Quarter End Data"})
graph.show()