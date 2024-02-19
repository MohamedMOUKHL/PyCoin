from pycoingecko import CoinGeckoAPI
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

# Fetch exchange rate between USD and MAD
cg = CoinGeckoAPI()
exchange_rate_data = cg.get_exchange_rates()
usd_to_mad_rate = exchange_rate_data['rates']['usd']['value']

# Fetch Bitcoin data in USD
bitcoin_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=1)
data = pd.DataFrame(bitcoin_data['prices'], columns=['TimeStamp', 'Price'])
data['Date'] = pd.to_datetime(data['TimeStamp'], unit='ms')

# Convert Bitcoin prices to MAD
data['Price_MAD'] = data['Price'] * usd_to_mad_rate

candlestick_data = data.groupby(data.Date.dt.date).agg({'Price_MAD': ['first', 'max', 'min', 'last']})

fig = go.Figure(data=[go.Candlestick(x=candlestick_data.index,
                open=candlestick_data['Price_MAD']['first'],
                high=candlestick_data['Price_MAD']['max'],
                low=candlestick_data['Price_MAD']['min'],
                close=candlestick_data['Price_MAD']['last'])])

fig.update_layout(xaxis_rangeslider_visible=False, xaxis_title='Date', yaxis_title='Price (MAD)',
                  title='Bitcoin Candlestick Chart in MAD')

plot(fig, filename='bitcoin_candlestick_mad.html')
