import dash
import os
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Load dataset
df = pd.read_csv("GTD_Dataset.csv")

# Data preprocessing
df = df[['eventid', 'iyear', 'imonth', 'iday', 'country_txt', 'region_txt', 'nkill',
         'attacktype1_txt', 'targtype1_txt', 'gname', 'weaptype1_txt', 'success',
         'crit1', 'latitude', 'longitude']]

df = df.rename(columns={'iyear': 'year', 'imonth': 'month', 'iday': 'day'})
df['month'] = df['month'].replace(0, 1)
df['day'] = df['day'].replace(0, 1)
df['date'] = pd.to_datetime(df[['year', 'month', 'day']])


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])
app.title = "Global Terrorism One-Page Dashboard"

app.layout = dbc.Container([
    html.H1("🌍 Global Terrorism Dashboard", className="text-center my-4 text-primary"),

    
    dbc.Row([
        dbc.Col([html.Label("Select Region"), dcc.Dropdown(id='region-filter', options=[{'label': r, 'value': r} for r in sorted(df['region_txt'].unique())], multi=True, value=[])], width=3),
        dbc.Col([html.Label("Select Country"), dcc.Dropdown(id='country-filter', options=[{'label': c, 'value': c} for c in sorted(df['country_txt'].unique())], multi=True, value=[])], width=3),
        dbc.Col([html.Label("Select Attack Type"), dcc.Dropdown(id='attack-filter', options=[{'label': a, 'value': a} for a in sorted(df['attacktype1_txt'].unique())], multi=True, value=[])], width=3),
        dbc.Col([html.Label("Select Year Range"), 
             dcc.RangeSlider(
                id='year-slider',
                min=df['year'].min(),
                max=df['year'].max(),
                step=1,
                value=[2010, 2017],
                marks= None,
                tooltip={"placement": "bottom", "always_visible": False}
                )], width=3),
                ], className="mb-4"),

   
    dbc.Row(id='kpis', className='mb-4'),

   
    html.Div(id='charts-container', style={'maxHeight': '80vh', 'overflowY': 'auto'})
], fluid=True, style={'padding': '20px'})  

@app.callback(
    [Output('kpis', 'children'),
     Output('charts-container', 'children')],
    [Input('region-filter', 'value'),
     Input('country-filter', 'value'),
     Input('attack-filter', 'value'),
     Input('year-slider', 'value')]
)
def update_dashboard(regions, countries, attacks, years):
    dff = df[(df['year'] >= years[0]) & (df['year'] <= years[1])]

    if regions:
        dff = dff[dff['region_txt'].isin(regions)]
    if countries:
        dff = dff[dff['country_txt'].isin(countries)]
    if attacks:
        dff = dff[dff['attacktype1_txt'].isin(attacks)]

    
    total_attacks = len(dff)
    total_kills = int(dff['nkill'].sum())
    success_rate = round(dff['success'].mean() * 100, 2)

    kpi_cards = [
        dbc.Col(dbc.Card([dbc.CardBody([html.H5("Total Attacks", className="card-title"), html.H2(f"{total_attacks:,}", className="text-danger")])], className="shadow-lg"), width=4),
        dbc.Col(dbc.Card([dbc.CardBody([html.H5("Total Fatalities", className="card-title"), html.H2(f"{total_kills:,}", className="text-warning")])], className="shadow-lg"), width=4),
        dbc.Col(dbc.Card([dbc.CardBody([html.H5("Success Rate", className="card-title"), html.H2(f"{success_rate}%", className="text-success")])], className="shadow-lg"), width=4),
    ]

    
    charts = []

  
    yearly = dff.groupby('year').size().reset_index(name='Attacks')
    fig1 = px.line(yearly, x='year', y='Attacks', title="Yearly Attacks")
    fig1.update_layout(height=500)
    charts.append(fig1)

    
    top_countries = dff['country_txt'].value_counts().nlargest(10).reset_index()
    top_countries.columns = ['country_txt', 'count']
    fig2 = px.bar(top_countries, x='country_txt', y='count', title="Top 10 Countries by Attacks")
    fig2.update_layout(height=500)
    charts.append(fig2)

   
    attack_pie = dff['attacktype1_txt'].value_counts().reset_index()
    attack_pie.columns = ['attacktype1_txt', 'count']
    fig3 = px.pie(attack_pie, names='attacktype1_txt', values='count', title="Attack Types Distribution")
    fig3.update_layout(height=500)
    charts.append(fig3)


    map_df = dff.dropna(subset=['latitude', 'longitude'])
    fig4 = px.scatter_mapbox(map_df, lat="latitude", lon="longitude", hover_name="country_txt", color="region_txt", zoom=1, mapbox_style="carto-positron", title="Attack Locations")
    fig4.update_layout(height=500)
    charts.append(fig4)

    
    temp_df = df.copy()
    temp_df['nkill'] = temp_df['nkill'].fillna(0)
    temp_df['decade'] = (temp_df['year'] // 10) * 10
    agg_df = temp_df.groupby('decade').agg({'eventid': 'count', 'nkill': 'sum'}).rename(columns={'eventid': 'Frequency', 'nkill': 'Total Fatalities'}).reset_index()
    last_5 = agg_df.sort_values('decade', ascending=False).head(5).sort_values('decade')

    fig5 = make_subplots(specs=[[{"secondary_y": True}]])
    fig5.add_trace(go.Bar(x=last_5['decade'], y=last_5['Frequency'], name='Frequency (Number of Attacks)', marker_color='#0072B2'), secondary_y=False)
    fig5.add_trace(go.Scatter(x=last_5['decade'], y=last_5['Total Fatalities'], name='Total Fatalities', mode='lines+markers', line=dict(color='#D55E00', width=3)), secondary_y=True)
    fig5.update_layout(title="Evolution of Terrorist Attacks: Last 5 Decades", xaxis_title="Decade", height=500, legend=dict(x=0.02, y=0.98), template="plotly_white")
    fig5.update_yaxes(title_text="Frequency (Number of Attacks)", secondary_y=False)
    fig5.update_yaxes(title_text="Severity (Total Fatalities)", secondary_y=True)
    charts.append(fig5)

   
    choropleth_df = df.copy()
    choropleth_df['nkill'] = choropleth_df['nkill'].fillna(0)
    choropleth_df['decade'] = (choropleth_df['year'] // 10) * 10
    agg_map = choropleth_df.groupby(['decade', 'country_txt']).agg({'eventid': 'count', 'nkill': 'sum'}).rename(columns={'eventid': 'Frequency', 'nkill': 'Total Fatalities'}).reset_index()

    fig6 = px.choropleth(agg_map, locations='country_txt', locationmode='country names', color='Frequency', hover_name='country_txt', hover_data={'Frequency': True, 'Total Fatalities': True, 'decade': False}, animation_frame='decade', color_continuous_scale='Cividis', title='Terrorist Attacks Frequency by Country over Decades')
    fig6.update_layout(geo=dict(showframe=False, showcoastlines=False), height=500)
    charts.append(fig6)

   
    yearly_agg = df.groupby('year').agg({'eventid': 'count', 'nkill': 'sum'}).rename(columns={'eventid': 'Frequency', 'nkill': 'Total Fatalities'}).reset_index()

    fig7 = make_subplots(specs=[[{"secondary_y": True}]])
    fig7.add_trace(go.Bar(x=yearly_agg['year'], y=yearly_agg['Frequency'], name='Frequency (Number of Attacks)', marker_color='#0072B2'), secondary_y=False)
    fig7.add_trace(go.Scatter(x=yearly_agg['year'], y=yearly_agg['Total Fatalities'], name='Total Fatalities', mode='lines+markers', line=dict(color='#D55E00', width=3)), secondary_y=True)
    fig7.update_layout(title="Global Terrorism Trends by Year", xaxis_title="Year", height=500, legend=dict(x=0.02, y=0.98), template="plotly_white")
    fig7.update_yaxes(title_text="Frequency (Number of Attacks)", secondary_y=False)
    fig7.update_yaxes(title_text="Severity (Total Fatalities)", secondary_y=True)
    charts.append(fig7)

   
    attack_region = dff.groupby('region_txt').size().reset_index(name='count')
    fig8 = px.pie(attack_region, names='region_txt', values='count', title="Frequency of Attacks by Region", hole=0.3, labels={'region_txt': 'Region'})
    fig8.update_layout(title="Frequency of Attacks by Region", height=500)
    charts.append(fig8)

   
    attack_types = [
        'Assassination', 'Hostage Taking (Kidnapping)', 'Bombing/Explosion', 
        'Facility/Infrastructure Attack', 'Armed Assault', 'Hijacking', 'Unknown', 
        'Unarmed Assault', 'Hostage Taking (Barricade Incident)'
    ]

    attack_maps = []


    agg_data = dff.groupby(['attacktype1_txt', 'country_txt'], as_index=False).agg({
    'eventid': 'count',
    'nkill': 'sum'
    }).rename(columns={'eventid': 'Frequency', 'nkill': 'Total Fatalities'})


    for atype in attack_types:
        subset = agg_data[agg_data['attacktype1_txt'] == atype]
    
        if subset.empty:
            continue  
    
        fig9 = px.scatter_geo(
            subset, locations="country_txt", locationmode="country names", 
            color="Frequency", size="Frequency", hover_name="country_txt", 
            hover_data={"Frequency": True, "Total Fatalities": True}, 
            projection="natural earth", 
            title=f"Geographical Distribution of {atype} Attacks", 
            color_continuous_scale="Inferno", template="plotly_white"
    )
    
        charts.append(fig9)
  

    
    df_groups = df[df['gname'] != "Unknown"]
    group_fatalities = df_groups.groupby('gname', as_index=False)['nkill'].sum().rename(columns={'nkill': 'Total Fatalities'})
    top_groups = group_fatalities.sort_values(by='Total Fatalities', ascending=False).head(10)

    fig10 = px.bar(
        top_groups, x='Total Fatalities', y='gname', orientation='h',
        title="Top 10 Terrorist Groups by Total Fatalities", labels={'gname': 'Terrorist Group', 'Total Fatalities': 'Total Fatalities'},
        template="plotly_white", color='Total Fatalities', color_continuous_scale='Viridis'
    )
    fig10.update_layout(yaxis=dict(autorange='reversed'))
    charts.append(fig10)  

    
    chart_rows = []
    for i in range(0, len(charts), 2):
        row = dbc.Row([
            dbc.Col(dcc.Graph(figure=charts[i], config={'displayModeBar': False}, style={'height': '500px'}), width=6, className='mb-4 shadow'),
            dbc.Col(dcc.Graph(figure=charts[i + 1], config={'displayModeBar': False}, style={'height': '500px'}), width=6, className='mb-4 shadow') if i + 1 < len(charts) else None
        ])
        chart_rows.append(row)

    return kpi_cards, chart_rows
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(host='0.0.0.0', port=port, debug=False)
 
