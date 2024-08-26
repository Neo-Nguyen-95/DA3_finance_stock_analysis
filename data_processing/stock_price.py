#%% LOAD LIBRARY
# Ref: https://pypi.org/project/yfinance/
# https://aroussi.com/post/python-yahoo-finance
import yfinance as yf

# check available data
stock_data = yf.Ticker('VNM')

stock_data.info

stock_data.history(period='max')

#%% FOR DOWNLOAD
symbol = 'FPT.VN'

stock_data = yf.download(
    symbol,
    start='2024-01-01',
    end='2024-08-01')

print(stock_data)
