from django.apps import AppConfig
import os
import requests, json
from requests.adapters import HTTPAdapter, Retry
import logging, traceback

class WeatherInfoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weather_info'

def get_data_from_cwb():
    CWB_API_KEY = os.environ['CWB_API_KEY']
    uri = f"https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-B0053-031?Authorization={CWB_API_KEY}&downloadType=WEB&format=JSON"

    try:
        s = requests.Session()
        retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504])
        s.mount("https://", HTTPAdapter(max_retries=retries))
        resp = s.get(uri, timeout=1.5)
        print(f"{resp}, {type(resp)}, {resp.status_code}")
        res_dict = resp.json()
        datasetDescription = res_dict["cwbopendata"]["dataset"]["datasetInfo"]["datasetDescription"]
        print(f"download success：{datasetDescription}")
        # resp_str = resp.text
        # data = json.loads(resp_str)
        # dailySave=[]
        # toDay=""
        print('Download 3 days weather from CWB')
        if resp.status_code==200:
            return True
        return False
    except Exception as err:
        print(f'Exception occured: {traceback.format_exc()}')
        return False