import streamlit as st
import pandas as pd

from tvdatafeed import TvDatafeed, Interval

from bokeh.plotting import figure, show, output_file
from bokeh.io import output_notebook

tv = TvDatafeed()

st.write("# Crypto Data Viz")
st.write("This is a basic app for visualizing crypto related data using trading view datafeed.")
asset = st.text_input("Choose crypto:", "VETUSD")
market = st.text_input("Choose market:", "BINANCE")
timeframe = st.text_input("Choose Timeframe:", "1d")

if timeframe == '1d':
    tf_interval = Interval.in_daily
    w = 12 * 60 * 60 * 1000 # 12 hours in milliseconds, usually half of timeframe
    #   h    min   s    ms
elif timeframe == '4h':
    tf_interval = Interval.in_4_hour
    w = 2 * 60 * 60 * 1000
elif timeframe == '5m':
    tf_interval = Interval.in_5_minute
    w = 1 * 5 * 60 * 1000


data = tv.get_hist(
    symbol = asset.upper(),
    exchange = market.upper(),
    interval = tf_interval,
    n_bars = 10000
)

inc = data.close > data.open
dec = data.open > data.close

TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

p = figure(x_axis_type="datetime", tools=TOOLS, width=2000, title = "OHLC Chart", y_axis_type = 'log')
p.grid.grid_line_alpha=0.9
p.segment(data.index, data.high, data.index, data.low, color="black")
p.vbar(data.index[inc], w, data.open[inc], data.close[inc], fill_color="#90ee90", line_color="black")
p.vbar(data.index[dec], w, data.open[dec], data.close[dec], fill_color="#f08080", line_color="black")

st.write(data)
st.bokeh_chart(p, use_container_width=True)
