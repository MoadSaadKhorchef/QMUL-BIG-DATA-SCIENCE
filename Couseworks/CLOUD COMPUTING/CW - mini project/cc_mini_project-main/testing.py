import arrow
import requests
import json


start = arrow.utcnow()
end = arrow.utcnow().shift(days=1)

start

response = requests.get(
  'https://api.stormglass.io/v2/tide/extremes/point',
  params={
    'lat': 60.936,
    'lng': 5.114,
    'start': start.timestamp(),  # Convert to UTC timestamp
    'end': end.timestamp(),  # Convert to UTC timestamp
  },
  headers={
    'Authorization': '9287cd42-8f13-11eb-a978-0242ac130002-9287cdb0-8f13-11eb-a978-0242ac130002'
  }
)

# Do something with response data.
json_data = response.json()

print(json_data)