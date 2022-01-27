from flask import Blueprint, render_template
from .bot import StrategyEMA, StrategyRSI, Bot
from datetime import datetime
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go

routes = Blueprint('routes', __name__)
    
@routes.route('/forex', methods=['GET', 'POST'])
def forex():
    # EURUSD
    forex = Bot('EURUSD', datetime(2021, 12, 30), datetime(2021, 12, 31), 'h12').load_data('EURUSD', 'h12')
    fig1 = go.Figure(
      data=[go.Candlestick(x=forex.index, low=forex['low'], high=forex['high'], close=forex['close'], open=forex['open'], increasing_line_color='green', decreasing_line_color='red')]
    )
    fig1.update_xaxes(title_text='Date')
    fig1.update_yaxes(title_text='Price')
    fig1.update_layout(title=f'EURUSD', xaxis_rangeslider_visible=False)
    graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    # AUDUSD
    forex2 = Bot('AUDUSD', datetime(2021, 12, 30), datetime(2021, 12, 31), 'h12').load_data('AUDUSD', 'h12')
    fig2 = go.Figure(
      data=[go.Candlestick(x=forex2.index, low=forex2['low'], high=forex2['high'], close=forex2['close'], open=forex2['open'], increasing_line_color='green', decreasing_line_color='red')]
    )
    fig2.update_xaxes(title_text='Date')
    fig2.update_yaxes(title_text='Price')
    fig2.update_layout(title=f'AUDUSD', xaxis_rangeslider_visible=False)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('forex.html', graphJSON1=graphJSON1, graphJSON2=graphJSON2)

@routes.route('/stock')
def stock():    
    return render_template('stock.html')

@routes.route('/cryptocurrency')
def cryptocurrency():
    return render_template('cryptocurrency.html')
