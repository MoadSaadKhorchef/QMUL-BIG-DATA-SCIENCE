import arrow
import requests
import json


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
        'Authorization': '9287cd42-8f13-11eb-a978-0242ac130002-9287cdb0-8f13-11eb-a978-0242ac130002'
      }
    )

    # Do something with response data.
    json_data = response.json()
    return json_data


def fetch_uv_data(lat, lng):
    uv_url_template ='https://api.openuv.io/api/v1/uv?lat={lat}&lng={lng}&dt={data}'
    my_latitude = lat
    my_longitude = lng
    start = arrow.utcnow()
    my_date = start.format('YYYY-MM-DD')
    headers = {'x-access-token': '10d1164b1d5b4a643fe25e8c86a93062'}

    uv_url = uv_url_template.format(lat=my_latitude, lng=my_longitude, data=my_date)
    resp = requests.get(uv_url, headers=headers)
    
    if resp.ok:
        return resp.json()
    else:
        return resp.reason
    
    
def retirve_all_data(lat, lng)

    uv = fetch_uv_data(lat, lng)
    weather_data = get_weather_data(lat, lng)
    
    mylist1 = []
    mylist2 = []
    mylist3 = []
    mylist4 = []
    mylist5 = []

    for i in range(len(json_data['hours'])):

        mylist1.append(weather_data['hours'][i]['airTemperature']['dwd'])
        mylist2.append(weather_data['hours'][i]['waveHeight']['dwd'])
        mylist3.append(weather_data['hours'][i]['gust']['dwd'])
        mylist4.append(weather_data['hours'][i]['cloudCover']['dwd'])
        mylist5.append(weather_data['hours'][i]['precipitation']['dwd'])
        
    x= ' { "Air_Temp_Max":' + str(max(mylist1)) + ' , "Air_Temp_Min":' + str(min(mylist1)) + ' , "Wave_Height_Max": ' + str(max(mylist2) ) + ' , "Wave_Height_Min": ' + str(min(mylist2)) + ' , "Gust_Max": ' + str( max(mylist3) ) + ' , "Gust_Min": ' + str(min(mylist3) ) +' , "Cloud_Cover_Max": ' + str(max(mylist4) ) + ' , "Cloud_Cover_Min": ' + str( min(mylist4) ) + ' , "Precipitation_Max": ' + str( max(mylist5) ) +' , "Precipitation_Min": ' + str( min(mylist5) ) + ' , "UV_Max": ' + str(uv['result']['uv_max'])+'}'
 
    # parse x:
    y = json.loads(x)

    # the result is a Python dictionary:
    #print(y)

    # retun databin JSON format
    return y 

