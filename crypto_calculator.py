#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests

from dash import Dash, dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc

from dash import jupyter_dash
jupyter_dash.default_mode = 'external'


# Our application allows the user to select any of the ten coins in `digital_currency_list.csv`.

# In[2]:


df_coins = pd.read_csv('digital_currency_list.csv')

df_coins


# In[3]:


my_key = 'VGDTFP5V0XWQSIU3'

url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey=' + my_key

print(url)


# In[4]:


def get_current_rate(coin, currency, api_key = my_key):
    try:
        url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=' + coin + '&to_currency=' + currency + '&apikey='+ my_key
        data = requests.get(url).json()
        rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])

    except:
        rate = "Missing data"
        
    return(rate)
    


# In[5]:


options_crypto = []
for code, name in zip(df_coins['currency code'], df_coins['currency name']):
    options_crypto.append({'value': code, 'name':name})

options_crypto


# In[6]:


options_crypto = [{'value': code, 'label':name} for code, name in zip(df_coins['currency code'], df_coins['currency name'])]
options_crypto


# In[7]:


crypto = dcc.Dropdown(
        id = 'crypto-dropdown',
        options = options_crypto,
        placeholder = "Choose a crypto",
        value = 'BTC',
        multi = False,
        clearable = False
    )

currency = dcc.Dropdown(
        id = 'currency-dropdown',
        options = ['EUR', 'USD', 'GBP'],
        placeholder = "Choose a currency",
        value = 'USD',
        multi = False,
        clearable = False
    )

input_number = dbc.Input(id = "input_number", 
                        placeholder = "Type a number",
                         value = 1,
                         type = "number")

header = html.H1('Crypto calculator')
result = dbc.Container(
    id = 'calculator',
    style = {'minHeight' : '2rem'})
    


# In[8]:


jupyter_dash.default_mode = "external"
from dash_bootstrap_templates import load_figure_template
from dash.dependencies import Input, Output
load_figure_template("bootstrap")
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css"


# In[9]:


app = Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP, dbc_css])
server = app.server

app.layout = dbc.Container(
    children = [
        header,
        html.Br(),
        dbc.Card(
            children = [
        dbc.Row([
            dbc.Col(input_number, width = 4),
            dbc.Col(crypto, width = 4),
            dbc.Col(currency, width = 4)
        ]),
        html.Br(),
        dbc.Row(dbc.Col(result , width = 12)),
                ],
        body = True,
        className = 'shadow-sm p-3'),
    ],
    className = "dbc"
)


# In[10]:


@app.callback(
    Output('calculator','children'),
    [Input('input_number', 'value'),
    Input('crypto-dropdown', 'value'),
    Input('currency-dropdown', 'value')]
)

def update_conversion(input_number, coin, currency):
    if input_number is None:
        return ''
        
    else:
        numeric_value = get_current_rate(coin, currency) * input_number

        return html.H4(f'{input_number} {coin} = {numeric_value:,.2f}')



# In[11]:

if __name__ == '__main__':
    app.run(debug = True)






