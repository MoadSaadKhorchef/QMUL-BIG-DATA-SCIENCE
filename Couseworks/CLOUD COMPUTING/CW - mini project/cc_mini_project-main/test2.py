import arrow
import requests

# Get first hour of today
start = arrow.utcnow()

# Get last hour of today
end = arrow.utcnow().shift(hours=5)

response = requests.get(
  'https://api.stormglass.io/v2/weather/point',
  params={
    'lat': 50.8225,
    'lng': 0.1372,
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

print(json_data)