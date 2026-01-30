# %%
import streamlit as st
from datetime import date
import datetime
import yfinance as yf
from plotly import graph_objs as go
import pandas as pd
import matplotlib.style as style
import matplotlib.pyplot as plt
import seaborn as sns
import json
# from statsmodels.tsa.arima_model import ARIMA  # Depricated
from statsmodels.tsa.arima.model import ARIMA
import time
import warnings

# Suppress yfinance warnings that don't affect functionality
warnings.filterwarnings('ignore', category=FutureWarning, module='yfinance')
warnings.filterwarnings('ignore', message='.*possibly delisted.*')

# %%
class DataMover:
    start = ""
    stop = ""
    
    def __init__(self, start, stop):
        self.start = start
        self.stop = stop

    def load_data(self, ticker):
        # Try multiple approaches for better reliability in Docker containers
        max_retries = 3
        retry_delay = 3
        
        for attempt in range(max_retries):
            try:
                print(f"Attempt {attempt + 1}/{max_retries} to fetch data for {ticker}")
                
                # Approach 1: Use download method with better parameters
                # This is more reliable than Ticker.history() in many cases
                df = yf.download(
                    ticker, 
                    start=self.start, 
                    end=self.stop,
                    progress=False,
                    auto_adjust=True,  # Automatically adjust prices for splits/dividends
                    prepost=False,  # Don't include pre/post market data
                    threads=False  # Disable threading for reliability
                )
                
                if not df.empty:
                    print(f"Successfully fetched {len(df)} rows for {ticker}")
                    # Flatten MultiIndex columns if present
                    if isinstance(df.columns, pd.MultiIndex):
                        df.columns = df.columns.get_level_values(0)
                    df.reset_index(inplace=True)
                    df['Date'] = pd.to_datetime(df['Date'])
                    
                    # Validate that we have the required columns
                    required_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
                    missing_cols = [col for col in required_cols if col not in df.columns]
                    if missing_cols:
                        print(f"Warning: Missing columns {missing_cols}, but continuing...")
                    
                    return df
                
                print(f"Download returned empty data on attempt {attempt + 1}")
                
                # If download failed, try Ticker object as fallback
                print(f"Trying Ticker.history() as fallback...")
                ticker_obj = yf.Ticker(ticker)
                df = ticker_obj.history(start=self.start, end=self.stop)
                
                if not df.empty:
                    print(f"Successfully fetched {len(df)} rows via Ticker.history()")
                    df.reset_index(inplace=True)
                    df['Date'] = pd.to_datetime(df['Date'])
                    return df
                
                print(f"Both methods returned empty data on attempt {attempt + 1}")
                
            except Exception as e:
                error_msg = str(e)
                print(f"Error on attempt {attempt + 1}: {error_msg}")
                
                # If it's a JSON decode error, it might be a temporary Yahoo Finance issue
                if "Expecting value" in error_msg or "JSON" in error_msg:
                    print("Detected JSON parsing error - Yahoo Finance may be temporarily unavailable")
                
                if attempt < max_retries - 1:
                    print(f"Waiting {retry_delay} seconds before retry...")
                    time.sleep(retry_delay)
                    continue
                else:
                    # On final attempt, raise a more informative error
                    raise ValueError(
                        f"Failed to download data for '{ticker}' after {max_retries} attempts. "
                        f"This could be due to:\n"
                        f"  1. Invalid ticker symbol\n"
                        f"  2. Yahoo Finance API temporarily unavailable\n"
                        f"  3. Network connectivity issues\n"
                        f"  4. Ticker delisted or no data for date range\n"
                        f"Last error: {error_msg}"
                    )
        
        # If we got here, data is empty after all retries
        raise ValueError(
            f"No data available for ticker '{ticker}' between {self.start} and {self.stop}. "
            f"Please verify the ticker symbol exists on Yahoo Finance and has historical data for this date range."
        )

    def load_datas(self, ticker_list):
        train = []
        for stock in ticker_list:
            df = self.load_data(stock)
            date = df['Date']
            train.append(df['Close'])
        train_df  = pd.concat(train, axis=1)
        train_df.columns = ticker_list
        train_df.set_index(date, inplace=True)
        train_df.reset_index(inplace=True)
        return train_df

    def write_json(self, df, path):
        df.to_json(r'{}'.format(path))
    
    def read_json(self, path):
        with open(path, "r") as file_ptr:
            obj = json.load(file_ptr)
        return obj
    
class ModelPlot:

    def __init__(self):
        # plt.style.use('ggplot')
        plt.rc('patch', force_edgecolor=True,edgecolor='black')
        plt.rc('hist', bins='auto')
        style.use('seaborn-v0_8-darkgrid')
        sns.set_context('notebook')
        sns.set_palette('gist_heat')

    def decomp_plot(self, df):
        fig, ax = plt.subplots(figsize=(17,8))
        ax.plot(df)
        ax.plot(df.rolling(window = 12).mean().dropna(), color='g')
        ax.plot(df.rolling(window = 12).std().dropna(), color='blue')
        ax.set_title('Rolling mean')
        ax.legend(['Apple', 'mean', 'std'])
        return fig

    def plot_raw_data(self, data):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['High'], name='Apple stock'))
        fig.add_trace(go.Scatter(x=data.index, y=data['Low'], name='Google stock'))
        fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)   

    def plot_arima(self, df, label):
        indx = df.index
        start = indx[-20]
        end = indx[-1]

        arima_model = ARIMA(df[label][:-20], order=(2,1,2)).fit()
        pred = arima_model.predict(start, end)
        
        rolling_mean = df[label].rolling(window = 12).mean().dropna()
        rolling_std = df[label].rolling(window = 12).std().dropna()

        arima_model = ARIMA(rolling_mean[:-20], order=(1,1,1), dates=df.index).fit()
        pred_mean = arima_model.predict(start, end)

        arima_model = ARIMA(rolling_std[:-20], order=(1,1,1), dates=df.index).fit()
        pred_std = arima_model.predict(start, end)
        

        fig, ax = plt.subplots(figsize=(17,8))
        ax.plot(df[label], alpha=0.5)
        ax.plot(rolling_mean, color='g', alpha=0.5)
        ax.plot(rolling_std, color='blue', alpha=0.5)

        # Predicted 
        ax.plot(pred)
        ax.plot(pred_mean, color='g')
        ax.plot(pred_std, color='b')
        ax.set_title('Rolling mean')
        ax.legend([label, 'mean', 'std', 'predicted'])
        return fig  
# %%
