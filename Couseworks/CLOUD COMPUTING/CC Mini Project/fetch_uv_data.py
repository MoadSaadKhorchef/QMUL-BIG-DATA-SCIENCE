import os
import requests
import arrow

def fetch_uv_data(lat=51.52369, lng=-0.0395857):
    uv_url_template ='https://api.openuv.io/api/v1/uv?lat={lat}&lng={lng}&dt={data}'
    start = arrow.utcnow()
    my_date = start.format('YYYY-MM-DD')
    headers = {'x-access-token': os.environ.get('OPENUV_TOKEN')}
    uv_url = uv_url_template.format(lat=lat, lng=lng, data=my_date)
    resp = requests.get(uv_url, headers=headers)
    
    if resp.ok:
        return resp.json()
    else:
        return resp.reason


def get_weather_data(lat, lng):
    # Get first hour of today
    start = arrow.utcnow()

    # Get last hour of today
    end = arrow.utcnow().shift(hours=5)

    response = requests.get(
      'https://api.stormglass.io/v2/weather/point',
      params={
        'lat': lat,
        'lng': lng,
        'params': ','.join(['waveHeight', 'airTemperature','gust','cloudCover','precipitation']),
        'start': start.timestamp(),  # Convert to UTC timestamp
        'end': end.timestamp()  # Convert to UTC timestamp
      },
      headers={
        'Authorization': os.environ.get('WEATHER_TOKEN')
      }
    )

    # Do something with response data.
    json_data = response.json()
    return json_data


def retrieve_data(lat, lng):
    uv = fetch_uv_data(lat, lng)['result']
    weather_data = get_weather_data(lat, lng)

    # Select a subset of data from OpenUV api
    keys = ['uv_max_time', 'uv_max', 'safe_exposure_time']
    outer_dict = dict((k, uv[k]) for k in keys if k in uv)
    
    # Select a subset of data from stormglass api
    for i in weather_data['hours']:
        t = i['time']
        i.pop('time')
        inner_dict = {k: v.get('dwd', '') for k, v in i.items()}
        outer_dict[t] = inner_dict

    return outer_dict

if __name__ == '__main__':
    data = retrieve_data(48.864716, 2.349014)