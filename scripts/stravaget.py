"""
Script to export CSV summary data for rides from a Strava account
based on the script published by Johannes Jacob (http://johannesjacob.com/2018/10/18/export-your-strava-data-excel/)
Adapted to export just CSV summary data rather than detailed ride metrics.

To run, this requires a Strava developer API key and client id. See the above URL for details.
"""

from stravalib.client import Client
import pandas as pd

client = Client()
code = 'baccfd19984935c4ae370b53a4cc9ac419d030f5'
client_id = 5805
client_secret = '518be609d5f852ef1bbb64d2017afc1a5b8c71f2'

year = 2019

#access_token = client.exchange_code_for_token(client_id=client_id,
#                       client_secret=client_secret,
#                        code=code)
access_token = '1463d86e5d7987711c560412b7b8e01c08400387'

client = Client(access_token=access_token)
df_overview = pd.DataFrame()

for activity in client.get_activities(after='{}-01-01T00:00:00Z'.format(str(year))):
    
    if activity.workout_type == None:
        wtype = 'Ride'
    elif int(activity.workout_type) == 11:
        wtype = 'Race'
    elif int(activity.workout_type) == 12:
        wtype = 'Workout'
    else:
        wtype = 'Ride'
    
    df_overview = df_overview.append(pd.DataFrame([{
        'date': activity.start_date,
        'distance': round(activity.distance.num / 1000, 1),
        'moving_time': int(activity.moving_time.seconds / 60),
        'elapsed_time': int(activity.elapsed_time.seconds / 60),
        'workout_type': wtype,
        'kudos': activity.kudos_count,
        'device_watts': activity.device_watts,
        'average_watts': activity.average_watts,
        'average_heartrate': activity.average_heartrate,
        'average_temp': activity.average_temp,
        'elevation_gain': activity.total_elevation_gain,
    }]))

    
df_overview.to_csv('strava_export_{}.csv'.format(str(year)), index=False)
