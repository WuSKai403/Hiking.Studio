from django.test import TestCase
from .apps import get_data_from_cwb
import environ
import json

env = environ.Env()


def test_get_data_from_cwb(requests_mock):
    key = env.str("CWB_API_KEY")
    result = {
        "cwbopendata": {
            "@xmlns": "urn:cwb:gov:tw:cwbcommon:0.1",
            "identifier": "429023c8-f1a4-4cfb-9a24-447c705b5689",
            "sender": "weather@cwb.gov.tw",
            "sent": "2023-02-14T11:31:13+08:00",
            "status": "Actual",
            "scope": "Public",
            "msgType": "Issue",
            "dataid": "B0053-031",
            "source": "MFC",
            "dataset": {"datasetInfo": {"datasetDescription": "臺灣各育樂區未來1週逐24小時天氣預報"}},
        }
    }
    requests_mock.get(
        f"https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-B0053-031?Authorization={key}&downloadType=WEB&format=JSON",
        text=json.dumps(result),
        status_code=200,
    )
    result = get_data_from_cwb()

    assert result == True
