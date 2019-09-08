import requests
from datetime import datetime
import pandas as pd
import json


def sqlExec(sqlStr, engine):
    conn = engine.connect()
    trans = conn.begin()
    conn.execute(sqlStr)
    trans.commit()
    conn.close()


def weatherReal(cityId):
    host = 'http://aliv13.data.moji.com'
    path = '/whapi/json/alicityweather/condition'
    url = host + path

    headers = \
        {
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Authorization": "APPCODE 40b5a0428140462da25d4c53c8e61dc9"
        }

    bodyReal = \
        {
            'cityId': cityId,
            'token': '''50b53ff8dd7d9fa320d3d3ca32cf8ed1'''
        }

    queryDT = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:00')
    res = requests.post(url, data=bodyReal, headers=headers)
    if res.status_code == 200:
        res = json.loads(res.text)
        dfReal = pd.io.json.json_normalize(res['data']['condition'])
        dfReal.drop(['condition', 'icon', 'vis', 'windDir', 'windDegrees'], axis=1, inplace=True)
        dfReal['dt'] = queryDT
        dfReal.rename(columns={'updatetime': 'measureDT', 'dt': 'queryDT', 'windLevel': 'windPower'}, inplace=True)
        dfOutput = dfReal.loc[:, ['measureDT', 'temp', 'windPower', 'humidity', 'queryDT']].reindex()
    return dfOutput

