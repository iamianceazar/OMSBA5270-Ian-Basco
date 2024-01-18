# import the modules

import pandas as pd
import requests
pd.set_option('display.width', 320)
pd.set_option('display.max_columns', 14)

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

# selecting CIK entry # 420
cik = companyCIK[419:420].cik_str.iloc[0]
# print(cik)

#SEC filling API call

companyFilling = requests.get(f'https://data.sec.gov/submissions/CIK{cik}.json', headers = headers)
# print(companyFilling.json().keys())
# print(companyFilling.json()['filings'].keys())

allFilings = pd.DataFrame.from_dict((companyFilling.json()['filings']['recent']))
print(allFilings)

#print column names for cleaning up reference

# print(allFilings.columns)
# print(allFilings[['accessionNumber', 'reportDate', 'form']].head(50))
# print(allFilings.iloc[9])