# Projeto 3 - SEne
# by João Barbosa

import os
import dash
import dash_table
from dash import Dash, html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

from prophet import Prophet

df_plants = pd.read_csv("Project_3/global_power_plant_database.csv")
df_plants_portugal = df_plants[df_plants["country"]=="PRT"]
df_plants_portugal["primary_fuel"] = df_plants_portugal["primary_fuel"].apply(lambda x: "Other" if x in ["Biomass", "Geothermal"] else x)
df_plants_portugal = df_plants_portugal[df_plants_portugal["primary_fuel"].isin(["Hydro", "Solar", "Wind", "Other"])]


df_power = df = pd.read_excel('Project_3/dgeg-ree-1995-2022.xlsx', skiprows=9)
df_power = df_power.rename(columns={"Unnamed: 0": "Year",
									"Hídrica > 10MW": "Hydro > 10MW",
									"Hídrica ≤ 10MW": "Hydro ≤ 10MW",
									"Biomassa(1)": "Biomass",
									"Eólica": "Wind",
									"Geotérmica": "Geothermic",
									"Fotovoltaica": "Solar",
									"Total Renováveis": "Total",
									"Unnamed: 9": "Total All Sources",
									})

df_power["Hydro"] = df_power["Hydro > 10MW"] + df_power["Hydro ≤ 10MW"]
df_power["Other"] = df_power["Biomass"] + df_power["Geothermic"]
df_power['Total'] = df_power['Total'].replace({'': np.nan, ' ': np.nan})
df_power['Total'] = pd.to_numeric(df_power['Total'])

df_power['Year'] = df_power['Year'][:-3]
df_power = df_power.iloc[:-3, :]


df_consumption = pd.read_excel('Project_3/pordata.xlsx', skiprows=7)
df_consumption = df_consumption.iloc[1:29, :9]
df_consumption = df_consumption.rename(columns={"Unnamed: 0": "Year",
												"Total": "Consumption"})
df_consumption['Consumption'] = pd.to_numeric(df_consumption['Consumption']).astype(float)
df_consumption['Consumption'] = df_consumption['Consumption']/1000000

df_power["Consumption"] = df_consumption["Consumption"]


df_solar = df_power[['Year', 'Solar']]
df_wind = df_power[['Year', 'Wind']]
df_hydro = df_power[['Year', 'Hydro']]
df_other = df_power[['Year', 'Other']]
df_total = df_power[['Year', 'Total']]
df_cons = df_consumption[['Year', 'Consumption']]

df_solar.columns = ['ds', 'y']
df_wind.columns = ['ds', 'y']
df_hydro.columns = ['ds', 'y']
df_other.columns = ['ds', 'y']
df_total.columns = ['ds', 'y']
df_cons.columns = ['ds', 'y']

df_solar['ds'] = pd.to_datetime(df_solar['ds'], format='%Y')
df_wind['ds'] = pd.to_datetime(df_wind['ds'], format='%Y')
df_hydro['ds'] = pd.to_datetime(df_hydro['ds'], format='%Y')
df_other['ds'] = pd.to_datetime(df_other['ds'], format='%Y')
df_total['ds'] = pd.to_datetime(df_total['ds'], format='%Y')
df_cons['ds'] = pd.to_datetime(df_cons['ds'], format='%Y')

m_solar = Prophet()
m_solar.fit(df_solar)
future_solar = m_solar.make_future_dataframe(periods=28, freq='Y')
forecast_solar = m_solar.predict(future_solar)

m_wind = Prophet()
m_wind.fit(df_wind)
future_wind = m_wind.make_future_dataframe(periods=28, freq='Y')
forecast_wind = m_wind.predict(future_wind)

m_hydro = Prophet()
m_hydro.fit(df_hydro)
future_hydro = m_hydro.make_future_dataframe(periods=28, freq='Y')
forecast_hydro = m_hydro.predict(future_hydro)

m_other = Prophet()
m_other.fit(df_other)
future_other = m_other.make_future_dataframe(periods=28, freq='Y')
forecast_other = m_other.predict(future_other)

m_total = Prophet()
m_total.fit(df_total)
future_total = m_total.make_future_dataframe(periods=28, freq='Y')
forecast_total = m_total.predict(future_total)

m_cons = Prophet()
m_cons.fit(df_cons)
future_cons = m_cons.make_future_dataframe(periods=28, freq='Y')
forecast_cons = m_cons.predict(future_cons)

forecast_solar['ds'] = forecast_solar['ds'].dt.year.astype(float)
forecast_wind['ds'] = forecast_wind['ds'].dt.year.astype(float)
forecast_hydro['ds'] = forecast_hydro['ds'].dt.year.astype(float)
forecast_other['ds'] = forecast_other['ds'].dt.year.astype(float)
forecast_total['ds'] = forecast_total['ds'].dt.year.astype(float)
forecast_cons['ds'] = forecast_cons['ds'].dt.year.astype(float)

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "Left": 0,
    "bottom": 0,
    "width": '70px',
    "paddingTop": "20px",
    "backgroundColor": "#2b2b2b",
    "color": "#cfcfcf",
    "fontSize": "23px",
}

MAP_STYLE = {
    "position": "fixed",
    "top": 0,
    "bottom": 0,
    "left": "70px",
    "right": "60%",
    "padding": "2rem 1rem",
    "display": "flex",
    "align-items": "center",
    "justify-content": "center"
}

DATA_STYLE = {
    "position": "fixed",
    "top": 0,
    "right": 0,
    "bottom": 0,
    "width": '60%',
    "padding": "2rem",
    "paddingTop": "1rem",
    "paddingRight": "3rem",
    "paddingLeft": "3rem",
    "backgroundColor": "#2b2b2b",
    "color": "#cfcfcf",
    "fontSize": "23px",
}

TABLE_PAGE_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": "70px",
    "right": 0,
    "bottom": 0,
    "paddingTop": "3rem",
    "paddingLeft": "3rem",
    "fontSize": "23px",
}


BLOCK_STYLE = {
    "backgroundColor": "#2b2b2b",
    "border-radius": "15px",
    "padding": "5px",
    "paddingRight": "5rem",
    "paddingLeft": "5rem",
    "paddingBottom": "1rem",
}

BUTTON_STYLE = {
    "width": "50px",
    "height": "50px",
    "borderRadius": "10px",
    "marginBottom": "10px",
    "border": "none"
}

HOVER_STYLE = {
    "backgroundColor": "#333333"
}

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

sidebar = html.Div([
    dbc.Row(

        dbc.Button(html.Img(src="assets/map.svg", style={"width": "30px", "height": "30px"}), color="dark", className="me-1", id="map-button", outline=True, style=BUTTON_STYLE),
        justify="center"
    ),
    dbc.Row(
        dbc.Button(html.Img(src="assets/file-spreadsheet.svg", style={"width": "30px", "height": "30px"}), color="dark", className="me-1", id="chart-button", outline=True, style=BUTTON_STYLE),
        justify="center"
    )
], style=SIDEBAR_STYLE)

color_map = {
    "Wind": "rgb(88,185,157)",
    "Solar": "rgb(231,160,60)",
    "Hydro": "rgb(82,150,213)",
    "Other": "rgb(126,138,139)",
    "Total": "rgb(214,87,69)",
    "Consumption": "rgb(99,208,239)"
}

fig = px.scatter_mapbox(df_plants_portugal, lat="latitude", lon="longitude", height=900, width=535,
						mapbox_style="carto-positron", hover_name="name",
						color="primary_fuel", color_discrete_map=color_map,
						hover_data=["capacity_mw"])
fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    mapbox_center={
    	"lat": 39.5,
        "lon": -8.0
    },
    mapbox_bounds={
    	"west": -11,
     	"east": -5,
      	"south": 35,
       	"north": 45},
    mapbox_zoom=6.3,
    legend=dict(
            orientation="v",
            yanchor="bottom",
            y=0,
            xanchor="left",
            x=0,
            title_text="",
        )
)

map = html.Div([
    dcc.Graph(id='map-graph', figure=fig)
], style=MAP_STYLE)


fig_production = px.line(df_power, x='Year', height=300,
						 y=[df_power['Solar'], df_power['Wind'], df_power['Hydro'], df_power['Other'], df_power['Total'], df_power["Consumption"]],
                         labels={'value': 'Energy (GWh)', 'Year': '', 'variable': ''}, color_discrete_map=color_map,)

fig_production.add_scatter(x=forecast_solar['ds'], y=forecast_solar['yhat'], mode='lines', name='Forecast', line=dict(color='rgb(231,160,60)', dash="dot"))
fig_production.add_scatter(x=forecast_wind['ds'], y=forecast_wind['yhat'], mode='lines', name='Forecast', line=dict(color='rgb(88,185,157)', dash="dot"))
fig_production.add_scatter(x=forecast_hydro['ds'], y=forecast_hydro['yhat'], mode='lines', name='Forecast', line=dict(color='rgb(82,150,213)', dash="dot"))
fig_production.add_scatter(x=forecast_other['ds'], y=forecast_other['yhat'], mode='lines', name='Forecast', line=dict(color='rgb(126,138,139)', dash="dot"))
fig_production.add_scatter(x=forecast_total['ds'], y=forecast_total['yhat'], mode='lines', name='Forecast', line=dict(color='rgb(214,87,69)', dash="dot"))

fig_production.update_layout(
    margin={"r":50,"t":0,"l":0,"b":0},
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="white"
    ),
    legend=dict(
        orientation="h",
        #entrywidth=50,
        yanchor="bottom",
        y=1.02,))

fig_production.update_xaxes(color="white" ,title_font_color="white", showgrid=False, zeroline=True, showline=False, gridcolor="rgb(88,88,88)", gridwidth=1, showticklabels=True)
fig_production.update_yaxes(color="white", title_font_color="white", gridcolor="rgb(88,88,88)", gridwidth=1)

fig_production.add_vline(x=2022, line_dash="dash", line_color="white")


df_years_fuels = pd.DataFrame([(y, f) for y in range(1995, 2023) for f in df_plants_portugal['primary_fuel'].unique()], columns=['commissioning_year', 'primary_fuel'])
df_power_cumulative = df_plants_portugal.groupby(['primary_fuel', 'commissioning_year']).size().groupby(level=[0]).cumsum().reset_index(name='counts')
df_power_cumulative = df_years_fuels.merge(df_power_cumulative, on=['primary_fuel', 'commissioning_year'], how='left')
df_power_cumulative['counts'] = df_power_cumulative.groupby('primary_fuel')['counts'].fillna(method='ffill').fillna(0)


fig_power_plants = px.line(df_power_cumulative, height=300,
                           x='commissioning_year', y='counts', color='primary_fuel',
                           labels={'counts': 'Number of Power Plants', 'commissioning_year': 'Year', 'primary_fuel': ''})

total_plants = df_power_cumulative.groupby('commissioning_year')['counts'].sum().reset_index()

fig_power_plants.add_scatter(x=total_plants['commissioning_year'],
                           y=total_plants['counts'],
                           mode='lines',
                           name='Total',
                           line=dict(color='rgb(214,87,69)'))

fig_power_plants.update_layout(
    margin={"r":50,"t":0,"l":0,"b":50},
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(
        color="white"
    ),
    legend=dict(
        orientation="h",
        entrywidth=108,
        yanchor="bottom",
        y=1.02,)
)

fig_power_plants.update_xaxes(color="white" ,title_font_color="white", showgrid=False, zeroline=False, showline=False, gridcolor="rgb(88,88,88)", gridwidth=1)
fig_power_plants.update_yaxes(color="white", title_font_color="white", gridcolor="rgb(88,88,88)", gridwidth=1)



data = html.Div([
    html.Div([
        dbc.Row(
            [
                dbc.Col(
                    html.H3("Renewable Production"),
                    width="6",
                ),
                dbc.Col(
                    html.H3("Portugal"),
                    width="6",
                    style={"textAlign": "right"}
                ),
            ]),

        html.Hr(style={"margin": "0"}),

        html.Div([
            dbc.Row(
                [
                    dbc.Col(
                        html.H6("Wind"),
                        width="1",
                        align="center"
                    ),
                    dbc.Col(
                        dbc.Progress(id='wind-progress', value=30, color="success", style={"height": "20px"}),
                        width="10",
                        align="center"
                    ),
                    dbc.Col(
                        html.H6("30%", id='wind-percentage'),
                        width="1",
                        align="center",
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.H6("Solar"),
                        width="1",
                        align="center"
                    ),
                    dbc.Col(
                        dbc.Progress(id='solar-progress', value=10, color="warning", style={"height": "20px"}),
                        width="10",
                        align="center"
                    ),
                    dbc.Col(
                        html.H6("10%", id='solar-percentage'),
                        width="1",
                        align="center",
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.H6("Hydro"),
                        width="1",
                        align="center"
                    ),
                    dbc.Col(
                        dbc.Progress(id='hydro-progress', value=60, color="info", style={"height": "20px"}),
                        width="10",
                        align="center"
                    ),
                    dbc.Col(
                        html.H6("60%", id='hydro-percentage'),
                        width="1",
                        align="center",
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        html.H6("Other"),
                        width="1",
                        align="center"
                    ),
                    dbc.Col(
                        dbc.Progress(id='other-progress', value=60, color="dark", style={"height": "20px"}),
                        width="10",
                        align="center"
                    ),
                    dbc.Col(
                        html.H6("60%", id='other-percentage'),
                        width="1",
                        align="center",
                    ),
                ]
            ),
        ], style={"marginTop": "1rem", "marginBottom": "1rem"}),

        html.Hr(style={"margin": "0"}),

        html.Div([
            dbc.Row(
                [
                    dbc.Col(
                        html.H6("Renewables"),
                        width="6",
                    ),
                    dbc.Col(
                        html.H6("00000 GWh", id='renewables-value'),
                        width="6",
                        style={"textAlign": "right"},
                    ),
                ]),

            html.Div([
                dbc.Progress(id='renewables-progress', value=50, color="#cebbb1", style={"height": "20px", "marginBottom": "5px"}),
                dbc.Progress(id='consumption-progress', value=80, color="#7f645a", style={"height": "20px"}),
            ]),

            dbc.Row(
                [
                    dbc.Col(
                        html.H6("Demand"),
                        width="6",
                    ),
                    dbc.Col(
                        html.H6("00000 GWh", id='consumption-value'),
                        width="6",
                        style={"textAlign": "right"}
                    ),
                ]),

        ]),
        html.Hr(style={"margin": "0"}),
    ],style=BLOCK_STYLE),


	html.Div([
		dbc.Tabs([
			dbc.Tab(label='Energy Production', tab_id='tab-1', label_style={"color": "rgb(207,207,207)"}, tab_style={"marginLeft": "auto"}, active_label_style={"color": "rgb(43,43,43)"}),
			dbc.Tab(label='Power Plants', tab_id='tab-2', label_style={"color": "rgb(207,207,207)"}, active_label_style={"color": "rgb(43,43,43)"}),
		], id='tabs', active_tab='tab-1'),
	], style={"marginRight": "50px", "marginLeft": "50px", "marginTop": "15px", "marginBottom": "15px"}),

    html.Div([
        dcc.Graph(id='energy-production', figure=fig_production)
    ]),


    html.Div([
        # dcc.Input(type="range", className="form-range", min="2013", max="2023", step="1", value="2017"),
        dcc.Slider(
        	id='commissioning-year-slider',
            min=1995,
            max=2022,
            step=1,
            value=2022,
            marks={1995: "1995", 2022: "2022"},
            tooltip={"placement": "bottom", "always_visible": True},
            updatemode='drag'
        ),
    ], style={"paddingLeft": "30px", "paddingRight": "30px"}),

], style=DATA_STYLE)

table = html.Div([
	html.Div([
        html.P('Select file:',
                style={"width": "10%", 'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='dropdown-files',
            options=[
                {'label': "Power Plant Data - Global Power Plant Database", 'value': 'plants'},
                {'label': "Energy Generation Data - Direção Geral de Energia e Geologia", 'value': 'production'},
                {'label': "Energy Consumption Data - Pordata", 'value': 'consumption'},
            ],
            value='plants',
            style={"width": "90%",'marginLeft': '10px'}
        ),
    ], style={'display': 'flex',
              'flexDirection': 'row',
              "marginBottom": "20px"}),

	html.Div([
	    dcc.Loading(
	        id="loading-raw-table",
	        type="circle",
	        children=dash_table.DataTable(
	            id='table',
	            columns=[{"name": i, "id": i} for i in df_consumption.columns],
	            data=df_consumption.to_dict('records'),
	            style_table={'overflowX': 'auto', 'overflowY': 'auto'},
	            style_cell={'overflow': 'auto'},
	        )
	    )
	], id='raw-table', style={"width": "95%",'height': '90%', 'overflowY': 'auto', 'overflowX': 'auto'})
], style=TABLE_PAGE_STYLE)

app.layout = html.Div(children=[map, sidebar, data], id="layout")


active_buttons = [True, False]


@app.callback(
    [Output('table', 'data'),
     Output('table', 'columns')],
    [Input('dropdown-files', 'value')]
)
def update_table(selected_file):
    if selected_file == 'plants':
        data = df_plants_portugal.to_dict('records')
        columns = [{"name": i, "id": i} for i in df_plants_portugal.columns]
    elif selected_file == 'production':
        data = df_power.to_dict('records')
        columns = [{"name": i, "id": i} for i in df_power.columns]
    elif selected_file == 'consumption':
        data = df_consumption.to_dict('records')
        columns = [{"name": i, "id": i} for i in df_consumption.columns]

    return data, columns

@app.callback(
    [Output('layout', 'children'),
     Output('map-button', 'active'),
     Output('chart-button', 'active')],
    [Input('map-button', 'n_clicks'),
     Input('chart-button', 'n_clicks')]
)
def update_layout(map_clicks, chart_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        button_id = 'map-button'
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'map-button':
        # Content for the "Map" button
        content = html.Div([map, sidebar, data])
        active_buttons = [True, False]
    elif button_id == 'chart-button':
        # Content for the "Chart" button
        content =  html.Div([sidebar, table])
        active_buttons = [False, True]

    return [content], active_buttons[0], active_buttons[1]




@app.callback(
    [Output('map-graph', 'figure'),
     Output('energy-production', 'figure'),
     Output('solar-progress', 'value'),
     Output('wind-progress', 'value'),
     Output('hydro-progress', 'value'),
     Output('other-progress', 'value'),
     Output('solar-percentage', 'children'),
     Output('wind-percentage', 'children'),
     Output('hydro-percentage', 'children'),
     Output('other-percentage', 'children'),
     Output('renewables-progress', 'value'),
     Output('renewables-value', 'children'),
     Output('consumption-progress', 'value'),
     Output('consumption-value', 'children')],
    [Input('commissioning-year-slider', 'value'),
     Input('tabs', 'active_tab')]
)

def update_map(selected_year, active_tab):
	filtered_df = df_plants_portugal[df_plants_portugal['commissioning_year'] <= selected_year]
	renewables_df = df_power[df_power['Year'] == selected_year]

	solar_percentage = renewables_df['Solar'] / renewables_df['Total'] * 100
	wind_percentage = renewables_df['Wind'] / renewables_df['Total'] * 100
	hydro_percentage = (renewables_df['Hydro > 10MW'] + renewables_df['Hydro ≤ 10MW']) / renewables_df['Total'] * 100
	other_percentage = (renewables_df['Biomass'] + renewables_df['Geothermic']) / renewables_df['Total'] * 100

	total = renewables_df["Total"]
	consumption = renewables_df["Consumption"]
	total_percentage = total / 60000 * 100
	consumption_percentage = consumption / 60000 * 100

	renewables_value = renewables_df['Total']
	consumption_value = renewables_df['Consumption']

	fig = px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude", height=900, width=535,
                            mapbox_style="carto-positron", hover_name="name",
                            color="primary_fuel", color_discrete_map=color_map,
                            hover_data=["capacity_mw"])
	fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox_center={
            "lat": 39.5,
            "lon": -8.0
        },
        mapbox_bounds={
            "west": -11,
            "east": -5,
            "south": 35,
            "north": 45},
        mapbox_zoom=6.3,
        legend=dict(
                orientation="v",
                yanchor="bottom",
                y=0,
                xanchor="left",
                x=0,
                title_text="",
            )
    )

	if active_tab == 'tab-1':
		fig_2 = px.line(df_power, x='Year', height=300,
							 y=[df_power['Wind'], df_power['Solar'], df_power['Hydro'], df_power['Other'], df_power['Total'], df_power['Consumption']],
	                             labels={'value': 'Energy (GWh)', 'Year': '', 'variable': ''}, color_discrete_map=color_map)

		#fig_2.add_scatter(x=df_consumption["Year"], y=df_consumption["Consumption"], mode='lines', name='Consumption', line=dict(color='rgb(231,160,60)'))
		fig_2.add_scatter(x=forecast_solar['ds'][27:], y=forecast_solar['yhat'][27:], mode='lines', name='Solar Forecast', line=dict(color='rgb(231,160,60)', dash="dot"))
		fig_2.add_scatter(x=forecast_wind['ds'][27:], y=forecast_wind['yhat'][27:], mode='lines', name='Wind Forecast', line=dict(color='rgb(88,185,157)', dash="dot"))
		fig_2.add_scatter(x=forecast_hydro['ds'][27:], y=forecast_hydro['yhat'][27:], mode='lines', name='Hydro Forecast', line=dict(color='rgb(82,150,213)', dash="dot"))
		fig_2.add_scatter(x=forecast_other['ds'][27:], y=forecast_other['yhat'][27:], mode='lines', name='Other Forecast', line=dict(color='rgb(126,138,139)', dash="dot"))
		fig_2.add_scatter(x=forecast_total['ds'][27:], y=forecast_total['yhat'][27:], mode='lines', name='Total Forecast', line=dict(color='rgb(214,87,69)', dash="dot"))
		fig_2.add_scatter(x=forecast_cons['ds'][27:], y=forecast_cons['yhat'][27:], mode='lines', name='Consumption Forecast', line=dict(color="rgb(99,208,239)",dash="dot"))

		for trace in fig_2.data:
			if "Forecast" in trace['name']:
				trace['legendgroup'] = trace['name'].split(" ")[0]
				trace['name'] = trace['name'].split(" ")[1]

	if active_tab == 'tab-2':
		fig_2 = px.line(df_power_cumulative, height=300, color_discrete_map=color_map,
                        x='commissioning_year', y='counts', color='primary_fuel',
                        labels={'counts': 'Number of Power Plants', 'commissioning_year': '', 'primary_fuel': ''})

		fig_2.add_scatter(x=total_plants['commissioning_year'],
                             y=total_plants['counts'],
                             mode='lines',
                             name='Total',
                             line=dict(color='rgb(214,87,69)'))

	fig_2.update_layout(
        margin={"r":50,"t":0,"l":0,"b":0},
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(
            color="white"
        ),
        legend=dict(
            orientation="h",
            #entrywidth=50,
            yanchor="bottom",
            y=1.02,
            groupclick="toggleitem"))

	fig_2.update_xaxes(color="white" ,title_font_color="white", showgrid=True, zeroline=False, showline=False, gridcolor="rgb(88,88,88)", gridwidth=1, showticklabels=True)
	fig_2.update_yaxes(color="white", title_font_color="white", gridcolor="rgb(88,88,88)", gridwidth=1)

	fig_2.add_vline(x=selected_year, line_dash="dash", line_color="white")

	return fig, fig_2, solar_percentage, wind_percentage, hydro_percentage, other_percentage, f"{solar_percentage.iloc[0]:.0f}%", f"{wind_percentage.iloc[0]:.0f}%", f"{hydro_percentage.iloc[0]:.0f}%", f"{other_percentage.iloc[0]:.0f}%", total_percentage, f"{renewables_value.iloc[0]:.0f} GWh", consumption_percentage, f"{consumption_value.iloc[0]:.0f} GWh"

if __name__ == '__main__':
    app.run_server()
