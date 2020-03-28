from pandas import DataFrame as df
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import date, timedelta
yesterday = date.today() - timedelta(days=1)


confirmed_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
deaths_url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
yesterdays_date = yesterday.strftime('%-m/%d/%y')

confirmed = pd.read_csv(confirmed_url)
deaths = pd.read_csv(deaths_url)
confirmed.iloc[0]['Country/Region'] #Test

death_size = []
confirmed_size = [] #Maybe remake these 6 lines into list comprehensions
#Set minimum size to 13 or 10
for num_cases in confirmed[yesterdays_date]:
    size = num_cases/500
    confirmed_size.append(size) if size > 13 else confirmed_size.append(13)
    #These sizes are for map marker size
for num_deaths in deaths[yesterdays_date]:
    size = num_cases/500
    death_size.append(size) if size > 10 else death_size.append(10)
# for place in deaths[['Province/State','Country/Region']]:
#     if place is float:
#     deaths_names.append()


confirmed['confirmed_size'] = df(confirmed_size)
deaths['death_size'] = df(death_size)
# confirmed['Name'] = df(confirmed_names)
# deaths['Name'] = df(deaths_names)

map_confirmed = go.Scattermapbox(
        customdata = confirmed[yesterdays_date
    ],
        name='Confirmed Cases',
        lon=confirmed['Long'],
        lat=confirmed['Lat'],
        text=confirmed['Country/Region'],
        hovertemplate=
            "<b>%{text}</b><br>" +
            "Confirmed: %{customdata}<br>" +
            "<extra></extra>",
        mode='markers',
        showlegend=True,
        marker=go.scattermapbox.Marker(
            size=confirmed['confirmed_size'],
            color='mediumturquoise',
            opacity=0.7
        )
)

map_deaths = go.Scattermapbox(
        customdata= deaths[yesterdays_date
    ],
        name='Deaths',
        lon=deaths['Long'],
        lat=deaths['Lat'],
        text=deaths['Country/Region'],
        hovertemplate=
            "<b>%{text}</b><br>" +
            "Confirmed: %{customdata}<br>" +
            "<extra></extra>",
        mode='markers',
        showlegend=True,
        marker=go.scattermapbox.Marker(
            size=deaths['death_size'],
            color='salmon',
            opacity=0.7
        )
)

layout = go.Layout(
    mapbox_style='white-bg',
    autosize=True,
    mapbox_layers=[
        {
            'below': 'traces',
            'sourcetype': 'raster',
            'source': [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
    ]
)

data = [map_confirmed, map_deaths]
fig = go.Figure(data=data, layout=layout)
fig.show()