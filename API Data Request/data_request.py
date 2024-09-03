import requests
import pandas as pd

tornado_days = pd.read_csv('tornado_sample.csv')
tornado_days['BEGIN_DATE_TIME'] = pd.to_datetime(tornado_days['BEGIN_DATE_TIME'])
tornado_days['END_DATE_TIME'] = pd.to_datetime(tornado_days['END_DATE_TIME'])
tornado_days['begin_date'] = tornado_days['BEGIN_DATE_TIME'].dt.date
tornado_days['end_date'] = tornado_days['END_DATE_TIME'].dt.date

no_tornado_days = pd.read_csv('non_tornado_sample.csv')



def fetch_weather_data(location, start_date, end_date):
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}%2C%20US/{start_date}/{end_date}?unitGroup=us&include=days&key=key&contentType=json'


    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        print(f"Error fetching data for {location} from {start_date} to {end_date}: {e}")
        print(response.text)
        return []

daily_data = []

for index, row in no_tornado_days.iterrows():
    location = row['state']
    begin_date = row['date']
    end_date = row['date']
    print(location, begin_date, end_date)
    data = fetch_weather_data(location, begin_date, end_date)
    if data:
        days_data = data.get('days', [])
        daily_data.extend(days_data)
    else:
        print(f'Location not found{location}')

df = pd.DataFrame(daily_data)
print(df.head())
print(len(df))     
df.to_csv('./long_non_tornado_weather_data.csv', index = False, header = True)





