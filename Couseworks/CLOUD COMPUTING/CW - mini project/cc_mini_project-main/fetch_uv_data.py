import os
import requests
from pprint import pprint

def fetch_uv_data(lat=51.52369, lng=-0.0395857):
    uv_url_template ='https://api.openuv.io/api/v1/uv?lat={lat}&lng={lng}&dt={data}'
    my_latitude = lat
    my_longitude = lng
    my_date = '2018-11'
    headers = {'x-access-token': os.environ.get('OPENUV_TOKEN')}

    uv_url = uv_url_template.format(lat=my_latitude, lng=my_longitude, data=my_date)
    resp = requests.get(uv_url, headers=headers)
    
    if resp.ok:
        return resp.json()
    else:
        return resp.reason

if __name__ == '__main__':
    uv = fetch_uv_data()
    pprint(uv)