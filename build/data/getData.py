import pandas as pd

import quandl
import datetime as DT

def getOilAssetData():
    oilData = pd.read_csv("AllActiveWells2015.csv", delimiter=',', encoding="utf-8-sig")
    oilData = oilData.reset_index(drop=True)

    return oilData

## api key

def getOilPriceData():
    ## api key
    quandl.ApiConfig.api_key = "PNfgU7jC1gZw_8wtipbd"

    today = DT.date.today()
    week_ago = today - DT.timedelta(days=7)
    data = quandl.get("OPEC/ORB", start_date=week_ago,end_date=today,collapse = 'daily',  returns="pandas")

    return data

def getFireData():
    # url of daily updated nasa satelitte fire data
    url = "https://firms.modaps.eosdis.nasa.gov/active_fire/viirs/text/VNP14IMGTDL_NRT_USA_contiguous_and_Hawaii_7d.csv"

    # read and reduce data
    fireData = pd.read_csv(url)
    fireData = fireData.reset_index()

    return fireData
