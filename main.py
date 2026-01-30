# %%
# https://medium.com/@josemarcialportilla/using-python-and-auto-arima-to-forecast-seasonal-time-series-90877adff03c
# https://towardsdatascience.com/arima-forecasting-in-python-90d36c2246d3
# %%
import streamlit as st
from datetime import date
from datetime import datetime, timedelta
import yfinance as yf
from plotly import graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import matplotlib.style as style
import matplotlib.pyplot as plt
import seaborn as sns
import json
from datamover import DataMover
import statsmodels.api as sm
from pylab import rcParams
# from statsmodels.tsa.arima_model import ARIMA  # Depricated
from statsmodels.tsa.arima.model import ARIMA
import mplfinance as mpf
import numpy as np
from scipy import stats
from statsmodels.tsa.stattools import acf
import warnings

# Suppress convergence warnings from statsmodels (models still produce usable results)
# These warnings are expected and don't affect functionality - the models work fine
warnings.filterwarnings('ignore', category=UserWarning, module='statsmodels')
warnings.filterwarnings('ignore', category=FutureWarning, module='statsmodels')
warnings.filterwarnings('ignore', message='.*Maximum Likelihood optimization failed to converge.*')
warnings.filterwarnings('ignore', message='.*Non-invertible starting MA parameters.*')
warnings.filterwarnings('ignore', message='.*Unknown keyword arguments.*')

# %%
def main():
    # %%
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rc('patch', force_edgecolor=True,edgecolor='black')
    plt.rc('hist', bins='auto')
    sns.set_context('notebook')
    sns.set_palette('gist_heat')
    st.set_page_config(
        layout='wide',
        page_title="Stock Analysis Dashboard",
        page_icon="📈"
    )
    
    # Define consistent color palette across all visualizations
    COLOR_PALETTE = {
        'primary': '#03fca5',      # Theme primary color
        'close': '#1f77b4',        # Blue for Close price
        'mean': '#2ca02c',         # Green for Mean/Rolling Mean
        'std': '#ff7f0e',          # Orange for Std/Volatility
        'volume': '#42a5f5',       # Light blue for Volume
        'returns': '#ab47bc',      # Purple for Returns
        'forecast': '#2ca02c',     # Green for forecasts
        'residual': '#d62728',     # Red for residuals/errors
        'trend': '#2ca02c',        # Green for trend
        'seasonal': '#ff7f0e',     # Orange for seasonal
        'observed': '#1f77b4'      # Blue for observed data
    }
    
    # %%
    today = date.today().strftime("%Y-%m-%d")
    mover = DataMover("2018-04-26", today)
    ticker_list = ["AAPL", "GOOG", "MSFT", "TSLA"]
    
    # Initialize session state for ticker selection
    if 'selected_ticker' not in st.session_state:
        st.session_state.selected_ticker = ticker_list[0]
    
    # ============= SIDEBAR: TICKER SELECTION =============
    with st.sidebar:
        st.title("📊 Dashboard Controls")
        st.markdown("---")
        
        st.subheader("Stock Selection")
        
        # Option to choose between predefined or custom ticker
        selection_mode = st.radio(
            "Selection Mode:",
            options=["Quick Select", "Custom Ticker"],
            horizontal=True,
            help="Choose from popular stocks or enter your own ticker symbol"
        )
        
        if selection_mode == "Quick Select":
            selected_ticker = st.selectbox(
                "Choose a stock ticker to analyze:",
                options=ticker_list,
                index=ticker_list.index(st.session_state.selected_ticker) if st.session_state.selected_ticker in ticker_list else 0,
                key='ticker_selector'
            )
        else:
            selected_ticker = st.text_input(
                "Enter ticker symbol:",
                value=st.session_state.selected_ticker,
                placeholder="e.g., NVDA, AMZN, META",
                help="Enter any valid stock ticker symbol from Yahoo Finance",
                key='custom_ticker_input'
            ).upper().strip()
            
            if not selected_ticker:
                st.warning("⚠️ Please enter a ticker symbol")
                selected_ticker = st.session_state.selected_ticker
            
            # Show helpful examples
            with st.expander("📖 Ticker Symbol Examples"):
                st.markdown("""
                **Tech Stocks:**
                - NVDA (NVIDIA)
                - AMZN (Amazon)
                - META (Meta/Facebook)
                - NFLX (Netflix)
                - AMD (AMD)
                
                **Other Sectors:**
                - BA (Boeing)
                - JPM (JP Morgan)
                - DIS (Disney)
                - NKE (Nike)
                - COIN (Coinbase)
                
                **International Stocks:**
                - TSM (Taiwan Semiconductor)
                - BABA (Alibaba)
                - SHOP (Shopify)
                
                💡 Visit [Yahoo Finance](https://finance.yahoo.com/) to find more ticker symbols!
                """)
        
        st.session_state.selected_ticker = selected_ticker
        
        st.markdown("---")
        st.markdown("""
        ### 📈 Popular Tickers
        - **AAPL** - Apple Inc.
        - **GOOG** - Alphabet Inc.
        - **MSFT** - Microsoft Corp.
        - **TSLA** - Tesla Inc.
        - **NVDA** - NVIDIA Corp.
        - **AMZN** - Amazon.com Inc.
        - **META** - Meta Platforms Inc.
        
        ### 📅 Data Range
        April 2018 - Present
        
        ### 🔄 Analysis Features
        - Rolling Statistics
        - Volume & Returns Analysis
        - Seasonal Decomposition
        - ARIMA Predictions
        - SARIMAX Forecasting
        - Future Price Projections
        
        ### 💡 Tip
        Use **Custom Ticker** mode to analyze any stock available on Yahoo Finance!
        """)
        
        st.markdown("---")
        
        # Connect section
        st.subheader("🤝 Connect With Me")
        
        col_linkedin, col_github = st.columns(2)
        
        with col_linkedin:
            st.markdown("""
            <a href="https://www.linkedin.com/in/dominik-huffield" target="_blank" style="text-decoration: none;">
                <div style="padding: 10px; background-color: #0077b5; border-radius: 5px; text-align: center; color: white; font-weight: bold;">
                    🔗 LinkedIn
                </div>
            </a>
            """, unsafe_allow_html=True)
        
        with col_github:
            st.markdown("""
            <a href="https://github.com/cogentdom" target="_blank" style="text-decoration: none;">
                <div style="padding: 10px; background-color: #333; border-radius: 5px; text-align: center; color: white; font-weight: bold;">
                    💻 GitHub
                </div>
            </a>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <p style="font-size: 12px; text-align: center; margin-top: 10px; color: #999;">
        Built with ❤️ for data analysis and forecasting
        </p>
        """, unsafe_allow_html=True)
    
    # ============= DATA LOADING SECTION =============
    # Cache data loading to improve performance
    @st.cache_data(ttl=3600, show_spinner=False)  # Cache for 1 hour
    def load_ticker_data(ticker_symbol, start_date, end_date):
        """Load and cache ticker data"""
        temp_mover = DataMover(start_date, end_date)
        return temp_mover.load_data(ticker_symbol)
    
    # Load data for selected ticker
    try:
        # Display loading status
        with st.spinner(f'📊 Loading data for {selected_ticker}...'):
            data = load_ticker_data(selected_ticker, "2018-04-26", today)
        
        # Validate data
        if data is None or len(data) == 0:
            st.error(f"❌ No data available for ticker '{selected_ticker}'. Please check the symbol and try again.")
            st.info("""
            💡 **Troubleshooting Tips:**
            - Make sure you're using a valid ticker symbol from Yahoo Finance
            - Try popular tickers: AAPL, MSFT, GOOGL, AMZN, NVDA, META
            - Some international tickers may need suffixes (e.g., VOD.L for London)
            """)
            st.stop()
        
    except Exception as e:
        st.error(f"❌ Error loading data for ticker '{selected_ticker}'")
        with st.expander("View Error Details"):
            st.code(str(e))
        st.info("""
        💡 **Common Issues:**
        - Ticker symbol doesn't exist on Yahoo Finance
        - No data available for the specified date range (April 2018 - Present)
        - Network connection problem
        - Invalid ticker format
        
        **Try these popular tickers:** AAPL, MSFT, GOOGL, AMZN, NVDA, TSLA, META
        """)
        st.stop()
    
    # ============= MAIN DASHBOARD HEADER =============
    st.title("📈 Stock Market Analysis Dashboard")
    
    # Display key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Selected Ticker", f"{selected_ticker}", help="Currently analyzing this stock")
    with col2:
        latest_price = data['Close'].iloc[-1] if 'Close' in data.columns and len(data) > 0 else 0
        st.metric("Latest Price", f"${latest_price:.2f}", help="Most recent closing price")
    with col3:
        price_change = ((data['Close'].iloc[-1] - data['Close'].iloc[0]) / data['Close'].iloc[0] * 100) if len(data) > 1 else 0
        st.metric("Total Change", f"{price_change:+.2f}%", delta=f"{price_change:+.2f}%", help="Price change over entire period")
    with col4:
        st.metric("Data Points", f"{len(data)}", help="Number of daily records")
    
    # Warning for limited data
    if len(data) < 50:
        st.warning(f"⚠️ Limited data available for {selected_ticker} ({len(data)} points). Analysis may be less accurate. Consider selecting a different ticker with more historical data.")
    
    st.markdown(f"""
    ### Comprehensive Time Series Analysis for **{selected_ticker}**
    
    This dashboard provides advanced technical analysis and forecasting for stocks. 
    Explore historical trends, statistical decomposition, predictive models, and future price projections 
    using state-of-the-art time series techniques including ARIMA, SARIMAX, and Exponential Smoothing.
    
    **Data Period:** April 2018 - {today} | **Analysis Type:** Biweekly Aggregation
    """)
    st.markdown("---")
    
    # %%
    def datetime_range(start=None, end=None):
        span = end - start
        for i in range(span.days + 1):
            yield start + timedelta(days=i)
    date_index = list(datetime_range(start=datetime(2018, 4, 26), end=datetime(2021, 4, 26)))
    # %%
    data.Date = pd.to_datetime(data.Date)
    data.set_index('Date', inplace=True)
    data.sort_index(inplace=True, ascending=True)
    # %%
    thin_data = data.resample('2w').mean()
    # %%
    def tripleGraph(data, ticker_name):
        chart1 = data
        chart2 = data.rolling(window = 12).mean().dropna()
        chart3 = data.rolling(window = 12).std().dropna()

        df = pd.concat([chart1, chart2, chart3], axis=1)
        df.columns=['Close', 'Rolling Mean', 'Rolling Std']

        st.title(f'Rolling value decomposition on {ticker_name} stock')
        st.line_chart(df, width=800)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.line_chart(df['2018-04-28':'2019-04-28'], width=200)
        with col2:
            st.line_chart(df['2019-04-28':'2020-04-28'], width=200)
        with col3:
            st.line_chart(df['2020-04-28':'2021-04-28'], width=200)

    # ============= SECTION 1: ROLLING STATISTICS =============
    st.header("📊 Section 1: Rolling Statistics Analysis")
    st.markdown("""
    **Purpose:** Understand price trends and volatility over time using rolling windows.
    
    - **Close Price:** Raw closing price data (biweekly aggregated)
    - **Rolling Mean (12-period):** Smoothed trend line revealing long-term direction
    - **Rolling Std (12-period):** Volatility indicator showing price stability
    
    The yearly breakdowns below reveal how volatility and trends evolved across different market conditions.
    """)

    tripleGraph(thin_data['Close'], selected_ticker)
    st.markdown("---")
    # %%
    # ============= SECTION 2: TRADING ACTIVITY & VOLATILITY =============
    st.header("💹 Section 2: Trading Activity & Volatility Analysis")
    st.markdown("""
    **Purpose:** Examine trading patterns, return distributions, and market volatility.
    
    - **Trading Volume:** Shows market activity and liquidity trends over time
    - **Daily Returns Distribution:** Histogram revealing the probability distribution of daily percentage changes
    - **Price Change vs Volume:** Correlation between trading volume and price movements (green = gains, red = losses)
    - **Rolling Volatility (30-day):** Standard deviation of returns indicating market risk and uncertainty
    
    Higher volatility periods often coincide with major market events or company announcements.
    """)
    
    # Create volume and daily returns analysis chart
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=(
            'Trading Volume Over Time',
            'Daily Returns Distribution',
            'Price Change vs Volume',
            'Rolling Volatility (30-day)'
        ),
        specs=[[{"type": "bar"}, {"type": "histogram"}],
               [{"type": "scatter"}, {"type": "scatter"}]],
        vertical_spacing=0.18,
        horizontal_spacing=0.08
    )
    
    # Calculate daily returns
    daily_data = data.copy()
    daily_data['Returns'] = daily_data['Close'].pct_change() * 100
    daily_data['Price_Change'] = daily_data['Close'].diff()
    daily_data['Volatility'] = daily_data['Returns'].rolling(window=30).std()
    daily_data = daily_data.dropna()
    
    # 1. Volume over time (bar chart) - use consistent color
    fig.add_trace(
        go.Bar(
            x=thin_data.index,
            y=thin_data['Volume'],
            marker_color=COLOR_PALETTE['volume'],
            name='Volume'
        ),
        row=1, col=1
    )
    
    # 2. Daily returns histogram - use consistent color
    fig.add_trace(
        go.Histogram(
            x=daily_data['Returns'],
            nbinsx=50,
            marker_color=COLOR_PALETTE['returns'],
            name='Returns %'
        ),
        row=1, col=2
    )
    
    # 3. Price change vs Volume scatter
    fig.add_trace(
        go.Scatter(
            x=daily_data['Volume'],
            y=daily_data['Returns'],
            mode='markers',
            marker=dict(
                color=daily_data['Returns'],
                colorscale='RdYlGn',
                size=5,
                opacity=0.6
            ),
            name='Price vs Vol'
        ),
        row=2, col=1
    )
    
    # 4. Rolling volatility - use consistent color for volatility/std
    fig.add_trace(
        go.Scatter(
            x=daily_data.index,
            y=daily_data['Volatility'],
            mode='lines',
            line=dict(color=COLOR_PALETTE['std'], width=2),
            name='Volatility'
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        title=f'{selected_ticker} Trading Activity & Volatility Analysis',
        height=700,
        showlegend=False,
        template='plotly_dark'
    )
    
    fig.update_xaxes(title_text='Date', row=1, col=1)
    fig.update_xaxes(title_text='Return %', row=1, col=2)
    fig.update_xaxes(title_text='Volume', row=2, col=1)
    fig.update_xaxes(title_text='Date', row=2, col=2)
    fig.update_yaxes(title_text='Volume', row=1, col=1)
    fig.update_yaxes(title_text='Frequency', row=1, col=2)
    fig.update_yaxes(title_text='Return %', row=2, col=1)
    fig.update_yaxes(title_text='Volatility %', row=2, col=2)

    st.plotly_chart(fig, key="volume-analysis-chart", use_container_width=True)
    st.markdown("---")
    
    # %%
    # ============= SECTION 3: SEASONAL DECOMPOSITION =============
    st.header("🔄 Section 3: Seasonal Decomposition")
    st.markdown("""
    **Purpose:** Break down the time series into fundamental components to understand underlying patterns.
    
    - **Observed:** The original closing price data as recorded
    - **Trend:** Long-term direction of the stock price, removing short-term fluctuations
    - **Seasonal:** Repeating patterns that occur at regular intervals (cyclical market behavior)
    - **Residual:** Random noise and irregular variations not explained by trend or seasonality
    
    This decomposition uses an additive model where: **Observed = Trend + Seasonal + Residual**
    
    A good model should show clear trend and seasonal components with minimal, random residuals.
    """)
    
    # Seasonal Decomposition using Plotly
    decomp = sm.tsa.seasonal_decompose(thin_data['Close'], model='additive', extrapolate_trend='freq', period=6)
    
    decomp_plotly = make_subplots(
        rows=4, cols=1,
        subplot_titles=('Observed', 'Trend', 'Seasonal', 'Residual'),
        vertical_spacing=0.08,
        shared_xaxes=True
    )
    
    decomp_plotly.add_trace(
        go.Scatter(x=thin_data.index, y=thin_data['Close'], mode='lines', 
                   line=dict(color=COLOR_PALETTE['observed'], width=2), name='Observed'),
        row=1, col=1
    )
    decomp_plotly.add_trace(
        go.Scatter(x=thin_data.index, y=decomp.trend, mode='lines',
                   line=dict(color=COLOR_PALETTE['trend'], width=2), name='Trend'),
        row=2, col=1
    )
    decomp_plotly.add_trace(
        go.Scatter(x=thin_data.index, y=decomp.seasonal, mode='lines',
                   line=dict(color=COLOR_PALETTE['seasonal'], width=2), name='Seasonal'),
        row=3, col=1
    )
    decomp_plotly.add_trace(
        go.Scatter(x=thin_data.index, y=decomp.resid, mode='markers',
                   marker=dict(color=COLOR_PALETTE['residual'], size=5), name='Residual'),
        row=4, col=1
    )
    
    decomp_plotly.update_layout(
        title=f'{selected_ticker} - Seasonal Decomposition',
        height=800,
        showlegend=False,
        template='plotly_dark'
    )
    decomp_plotly.update_xaxes(title_text='Date', row=4, col=1)
    
    st.plotly_chart(decomp_plotly, key="seasonal-decomp-chart", use_container_width=True)
    st.markdown("---")
    # %%
    # ============= SECTION 4: ARIMA MODEL PREDICTIONS =============
    st.header("📉 Section 4: ARIMA Model Predictions")
    st.markdown("""
    **Purpose:** Validate statistical forecasting models by comparing predictions against actual historical data.
    
    **ARIMA** (AutoRegressive Integrated Moving Average) is a classical statistical method for time series forecasting:
    - **AutoRegressive (AR):** Uses past values to predict future values
    - **Integrated (I):** Differences the data to achieve stationarity
    - **Moving Average (MA):** Uses past forecast errors in the prediction
    
    This section shows:
    - **Historical data** (faded lines): The actual observed values for Close Price, Rolling Mean, and Rolling Std
    - **ARIMA predictions** (bold lines): Model forecasts for the last 20 periods to assess prediction accuracy
    
    Matching colors indicate the same metric: Blue = Close Price, Green = Rolling Mean, Orange = Rolling Std
    """)
    
    st.subheader(f"ARIMA Model Predictions - {selected_ticker}")
    
    indx = thin_data.index
    start_pred = indx[-20]
    end_pred = indx[-1]
    
    # Fit ARIMA models with increased iterations for convergence
    arima_model = ARIMA(thin_data['Close'][:-20], order=(2,1,2)).fit(method_kwargs={'maxiter': 500})
    pred = arima_model.predict(start_pred, end_pred)
    
    rolling_mean = thin_data['Close'].rolling(window=12).mean().dropna()
    rolling_std = thin_data['Close'].rolling(window=12).std().dropna()
    
    arima_mean_model = ARIMA(rolling_mean[:-20], order=(1,1,1)).fit(method_kwargs={'maxiter': 500})
    pred_mean = arima_mean_model.predict(start_pred, end_pred)
    
    arima_std_model = ARIMA(rolling_std[:-20], order=(1,1,1)).fit(method_kwargs={'maxiter': 500})
    pred_std = arima_std_model.predict(start_pred, end_pred)
    
    # Create Plotly figure with consistent colors
    fig_arima = go.Figure()
    
    # Historical data (semi-transparent) - using consistent color palette
    fig_arima.add_trace(go.Scatter(
        x=thin_data.index, y=thin_data['Close'],
        mode='lines', name='Close Price',
        line=dict(color=COLOR_PALETTE['close'], width=1.5), opacity=0.5
    ))
    fig_arima.add_trace(go.Scatter(
        x=rolling_mean.index, y=rolling_mean.values,
        mode='lines', name='Rolling Mean',
        line=dict(color=COLOR_PALETTE['mean'], width=1.5), opacity=0.5
    ))
    fig_arima.add_trace(go.Scatter(
        x=rolling_std.index, y=rolling_std.values,
        mode='lines', name='Rolling Std',
        line=dict(color=COLOR_PALETTE['std'], width=1.5), opacity=0.5
    ))
    
    # Predicted values (same colors, bolder solid line)
    fig_arima.add_trace(go.Scatter(
        x=pred.index, y=pred.values,
        mode='lines', name='Predicted Close',
        line=dict(color=COLOR_PALETTE['close'], width=3)
    ))
    fig_arima.add_trace(go.Scatter(
        x=pred_mean.index, y=pred_mean.values,
        mode='lines', name='Predicted Mean',
        line=dict(color=COLOR_PALETTE['mean'], width=3)
    ))
    fig_arima.add_trace(go.Scatter(
        x=pred_std.index, y=pred_std.values,
        mode='lines', name='Predicted Std',
        line=dict(color=COLOR_PALETTE['std'], width=3)
    ))
    
    fig_arima.update_layout(
        title=f'{selected_ticker} - ARIMA Predictions vs Historical',
        xaxis_title='Date',
        yaxis_title='Price ($)',
        height=500,
        template='plotly_dark',
        hovermode='x unified',
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    st.plotly_chart(fig_arima, key="arima-predictions-chart", use_container_width=True)
    st.markdown("---")
    
    # %%
    # ============= SECTION 5: SARIMAX FORECASTING ANALYSIS =============
    st.header(f"📈 Section 5: Advanced Time Series Forecasting (SARIMAX)")
    st.markdown("""
    **Purpose:** Apply advanced seasonal forecasting techniques and validate model performance.
    
    **SARIMAX** (Seasonal ARIMA with eXogenous variables) extends ARIMA to handle seasonal patterns:
    - Accounts for repeating patterns at fixed intervals
    - Provides confidence intervals for uncertainty quantification
    - Enables rigorous model diagnostics
    
    This comprehensive analysis includes:
    1. **Model Diagnostics:** Validates that our model assumptions are met
    2. **Forecast Validation:** Compares predictions against actual data
    3. **Accuracy Metrics:** Quantifies prediction errors (MSE, RMSE, MAE, MAPE)
    4. **Future Forecasting:** Projects prices beyond the historical data
    """)
    
    # Prepare data for SARIMAX model
    y_series = thin_data['Close'].dropna()
    
    # Create a proper DatetimeIndex with explicit frequency for forecasting
    date_range = pd.date_range(start=y_series.index[0], periods=len(y_series), freq='2W')
    y_series = pd.Series(y_series.values, index=date_range)
    
    # Fit SARIMAX model with optimal parameters (similar to notebook's approach)
    try:
        mod = sm.tsa.statespace.SARIMAX(
            y_series,
            order=(1, 1, 1),
            seasonal_order=(1, 1, 0, 6),  # 6 periods for biweekly data
            enforce_stationarity=False,
            enforce_invertibility=False,
            initialization='approximate_diffuse'
        )
        results = mod.fit(disp=False, maxiter=500)
        
        # 1. ARIMA Model Diagnostics Plot
        st.subheader("🔍 Model Diagnostics")
        st.markdown("""
        **Diagnostic checks ensure model validity:**
        - **Standardized Residuals:** Should fluctuate randomly around zero with no patterns (indicating good model fit)
        - **Histogram + Normal Curve:** Residuals should approximate a normal distribution (bell curve)
        - **Q-Q Plot:** Points should closely follow the diagonal line (confirms normality assumption)
        - **Correlogram (ACF):** Bars should stay within confidence bands (no remaining autocorrelation)
        
        If diagnostics look good, we can trust the model's forecasts. Systematic patterns in residuals suggest room for improvement.
        """)
        
        # Get standardized residuals
        residuals = results.resid
        std_residuals = (residuals - residuals.mean()) / residuals.std()
        
        # Create 2x2 subplot for diagnostics
        diag_fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Standardized Residuals',
                'Histogram + Normal Distribution',
                'Normal Q-Q Plot',
                'Correlogram (ACF)'
            ),
            vertical_spacing=0.18,
            horizontal_spacing=0.12
        )
        
        # 1. Standardized Residuals (top-left)
        diag_fig.add_trace(
            go.Scatter(
                x=std_residuals.index, y=std_residuals.values,
                mode='lines', name='Std Residuals',
                line=dict(color=COLOR_PALETTE['close'], width=1)
            ),
            row=1, col=1
        )
        diag_fig.add_hline(y=0, line_dash="dash", line_color=COLOR_PALETTE['residual'], row=1, col=1)
        
        # 2. Histogram with KDE (top-right)
        diag_fig.add_trace(
            go.Histogram(
                x=std_residuals.values, nbinsx=30,
                name='Residuals', opacity=0.7,
                marker_color=COLOR_PALETTE['close'],
                histnorm='probability density'
            ),
            row=1, col=2
        )
        
        # Add normal distribution curve
        x_range = np.linspace(std_residuals.min(), std_residuals.max(), 100)
        normal_curve = stats.norm.pdf(x_range, 0, 1)
        diag_fig.add_trace(
            go.Scatter(
                x=x_range, y=normal_curve,
                mode='lines', name='N(0,1)',
                line=dict(color=COLOR_PALETTE['std'], width=2)
            ),
            row=1, col=2
        )
        
        # 3. Q-Q Plot (bottom-left)
        sorted_residuals = np.sort(std_residuals.dropna().values)
        n = len(sorted_residuals)
        theoretical_quantiles = stats.norm.ppf(np.arange(1, n + 1) / (n + 1))
        
        diag_fig.add_trace(
            go.Scatter(
                x=theoretical_quantiles, y=sorted_residuals,
                mode='markers', name='Sample Quantiles',
                marker=dict(color=COLOR_PALETTE['close'], size=5)
            ),
            row=2, col=1
        )
        
        # Add diagonal reference line for Q-Q plot
        qq_min = min(theoretical_quantiles.min(), sorted_residuals.min())
        qq_max = max(theoretical_quantiles.max(), sorted_residuals.max())
        diag_fig.add_trace(
            go.Scatter(
                x=[qq_min, qq_max], y=[qq_min, qq_max],
                mode='lines', name='Reference',
                line=dict(color=COLOR_PALETTE['residual'], width=2, dash='dash')
            ),
            row=2, col=1
        )
        
        # 4. Correlogram / ACF (bottom-right)
        acf_values = acf(residuals.dropna(), nlags=20)
        lags = list(range(len(acf_values)))
        conf_interval = 1.96 / np.sqrt(len(residuals.dropna()))
        
        diag_fig.add_trace(
            go.Bar(
                x=lags, y=acf_values,
                name='ACF', marker_color=COLOR_PALETTE['close']
            ),
            row=2, col=2
        )
        
        # Add confidence interval lines
        diag_fig.add_hline(y=conf_interval, line_dash="dash", line_color=COLOR_PALETTE['residual'], row=2, col=2)
        diag_fig.add_hline(y=-conf_interval, line_dash="dash", line_color=COLOR_PALETTE['residual'], row=2, col=2)
        diag_fig.add_hline(y=0, line_dash="solid", line_color="gray", row=2, col=2)
        
        # Update layout
        diag_fig.update_layout(
            height=800,
            showlegend=False,
            template='plotly_dark',
            title=f'{selected_ticker} - SARIMAX Model Diagnostics',
            margin=dict(t=80, b=60)
        )
        
        # Update subplot title positions to avoid overlap
        for annotation in diag_fig['layout']['annotations']:
            annotation['y'] = annotation['y'] + 0.02
        
        diag_fig.update_xaxes(title_text='Date', title_font_size=11, row=1, col=1)
        diag_fig.update_yaxes(title_text='Residual', title_font_size=11, row=1, col=1)
        diag_fig.update_xaxes(title_text='Residual Value', title_font_size=11, row=1, col=2)
        diag_fig.update_yaxes(title_text='Density', title_font_size=11, row=1, col=2)
        diag_fig.update_xaxes(title_text='Theoretical Quantiles', title_font_size=11, row=2, col=1)
        diag_fig.update_yaxes(title_text='Sample Quantiles', title_font_size=11, row=2, col=1)
        diag_fig.update_xaxes(title_text='Lag', title_font_size=11, row=2, col=2)
        diag_fig.update_yaxes(title_text='ACF', title_font_size=11, row=2, col=2)
        
        st.plotly_chart(diag_fig, key="diagnostics-chart", use_container_width=True)
        
        # 2. Forecast Validation - One-step ahead predictions with confidence intervals
        st.subheader("🎯 Forecast Validation")
        st.markdown("""
        **One-step ahead forecasting** tests model accuracy by predicting each point using only prior data.
        The shaded confidence interval shows the range where we expect true values with 95% probability.
        
        Ideally, the orange forecast line should closely track the blue observed line, with actual values
        falling within the confidence bands.
        """)
        
        # Get predictions for the last portion of data using integer indices
        split_point = len(y_series) - 20 if len(y_series) > 20 else len(y_series) // 2
        
        pred = results.get_prediction(start=split_point, end=len(y_series) - 1, dynamic=False)
        pred_ci = pred.conf_int()
        
        # Map the prediction index back to dates
        pred_dates = y_series.index[split_point:]
        
        # Create validation plot using Plotly with consistent colors
        fig_validation = go.Figure()
        
        # Plot observed data (blue - observed)
        fig_validation.add_trace(go.Scatter(
            x=y_series.index, y=y_series.values,
            mode='lines', name='Observed',
            line=dict(color=COLOR_PALETTE['observed'], width=2)
        ))
        
        # Plot one-step ahead forecast (orange - std/volatility color for forecast uncertainty)
        fig_validation.add_trace(go.Scatter(
            x=pred_dates, y=pred.predicted_mean.values,
            mode='lines', name='One-step ahead Forecast',
            line=dict(color=COLOR_PALETTE['std'], width=2)
        ))
        
        # Add confidence interval (upper bound)
        fig_validation.add_trace(go.Scatter(
            x=pred_dates, y=pred_ci.iloc[:, 1].values,
            mode='lines', name='Upper CI',
            line=dict(width=0),
            showlegend=False
        ))
        
        # Add confidence interval (lower bound with fill) - matching forecast color
        fig_validation.add_trace(go.Scatter(
            x=pred_dates, y=pred_ci.iloc[:, 0].values,
            mode='lines', name='95% Confidence Interval',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(255, 127, 14, 0.2)'  # Orange with transparency
        ))
        
        fig_validation.update_layout(
            title=f'{selected_ticker} - Forecast Validation',
            xaxis_title='Date',
            yaxis_title='Stock Price ($)',
            height=500,
            template='plotly_dark',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_validation, key="forecast-validation-chart", use_container_width=True)
        
        # 3. Calculate and display forecast accuracy metrics
        y_forecasted = pred.predicted_mean.values
        y_truth = y_series.iloc[split_point:].values
        
        # Calculate metrics directly
        if len(y_forecasted) > 0 and len(y_truth) > 0:
            mse = ((y_forecasted - y_truth) ** 2).mean()
            rmse = np.sqrt(mse)
            mae = np.abs(y_forecasted - y_truth).mean()
            mape = (np.abs((y_truth - y_forecasted) / y_truth) * 100).mean()
            
            # Display metrics in columns
            st.subheader("📊 Forecast Accuracy Metrics")
            st.markdown("""
            These metrics quantify prediction accuracy. Lower values indicate better performance:
            - **MSE/RMSE:** Penalizes large errors more heavily
            - **MAE:** Average absolute prediction error in dollars
            - **MAPE:** Average percentage error (scale-independent)
            """)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Mean Squared Error", f"{mse:,.2f}", help="Average of squared prediction errors")
            with col2:
                st.metric("Root MSE", f"${rmse:,.2f}", help="Square root of MSE, in original units")
            with col3:
                st.metric("Mean Absolute Error", f"${mae:,.2f}", help="Average absolute prediction error")
            with col4:
                st.metric("MAPE", f"{mape:.2f}%", help="Mean Absolute Percentage Error")
        
        # Add model summary in expander
        with st.expander("📋 View SARIMAX Model Summary"):
            st.text(str(results.summary()))
            
    except Exception as e:
        st.warning(f"SARIMAX diagnostics error: {str(e)}")
    
    # 4. Future Forecast with Uncertainty Bounds (using Exponential Smoothing)
    st.subheader("🔮 Future Price Forecast")
    st.markdown("""
    **Purpose:** Project stock prices into the future using Holt-Winters Exponential Smoothing.
    
    This method is ideal for data with trends and seasonality:
    - **Historical (blue line):** Actual past prices
    - **Fitted (orange dotted):** Model's fit to historical data
    - **Forecast (green dashed):** Projected future prices
    - **Confidence Interval (green shaded):** 95% probability range for future values
    
    The vertical line marks where historical data ends and forecasts begin. The widening confidence
    interval reflects increasing uncertainty further into the future.
    """)
    
    try:
        from statsmodels.tsa.holtwinters import ExponentialSmoothing
        
        # Prepare data - use numpy array to avoid timestamp issues
        hist_values = thin_data['Close'].dropna().values
        hist_dates = thin_data['Close'].dropna().index
        
        # Forecast parameters
        forecast_steps = 20
        
        # Fit Holt-Winters Exponential Smoothing model
        model = ExponentialSmoothing(
            hist_values,
            trend='add',
            seasonal='add',
            seasonal_periods=6,  # Approximate seasonal cycle
            damped_trend=True
        )
        fitted_model = model.fit(optimized=True)
        
        # Generate forecast
        forecast_values = fitted_model.forecast(forecast_steps)
        
        # Generate future dates
        last_date = hist_dates[-1]
        future_dates = pd.date_range(start=last_date + pd.Timedelta(weeks=2), periods=forecast_steps, freq='2W')
        
        # Calculate confidence intervals using fitted residuals
        residual_std = np.std(fitted_model.resid)
        ci_multipliers = np.sqrt(np.arange(1, forecast_steps + 1))
        ci_lower = forecast_values - 1.96 * residual_std * ci_multipliers
        ci_upper = forecast_values + 1.96 * residual_std * ci_multipliers
        
        # Create future forecast plot using Plotly with consistent colors
        fig_forecast = go.Figure()
        
        # Plot historical data (blue - consistent with observed)
        fig_forecast.add_trace(go.Scatter(
            x=hist_dates, y=hist_values,
            mode='lines', name='Historical',
            line=dict(color=COLOR_PALETTE['observed'], width=2)
        ))
        
        # Plot fitted values (orange - consistent with volatility/uncertainty)
        fig_forecast.add_trace(go.Scatter(
            x=hist_dates, y=fitted_model.fittedvalues,
            mode='lines', name='Fitted',
            line=dict(color=COLOR_PALETTE['std'], width=1, dash='dot'),
            opacity=0.7
        ))
        
        # Plot forecast (green - consistent with forecast/trend)
        fig_forecast.add_trace(go.Scatter(
            x=future_dates, y=forecast_values,
            mode='lines', name='Forecast',
            line=dict(color=COLOR_PALETTE['forecast'], width=2, dash='dash')
        ))
        
        # Add uncertainty bounds (upper)
        fig_forecast.add_trace(go.Scatter(
            x=future_dates, y=ci_upper,
            mode='lines', name='Upper CI',
            line=dict(width=0),
            showlegend=False
        ))
        
        # Add uncertainty bounds (lower with fill) - green matching forecast
        fig_forecast.add_trace(go.Scatter(
            x=future_dates, y=ci_lower,
            mode='lines', name='95% Confidence Interval',
            line=dict(width=0),
            fill='tonexty',
            fillcolor='rgba(44, 160, 44, 0.2)'  # Green with transparency
        ))
        
        # Add a vertical line to separate historical from forecast
        # Convert timestamp to string to avoid pandas/plotly compatibility issue
        forecast_start_str = str(hist_dates[-1])
        fig_forecast.add_vline(
            x=forecast_start_str, 
            line_dash="dot", 
            line_color="gray"
        )
        # Add annotation separately to avoid timestamp arithmetic issues
        fig_forecast.add_annotation(
            x=forecast_start_str,
            y=1.05,
            yref="paper",
            text="Forecast Start",
            showarrow=False,
            font=dict(color="gray", size=11)
        )
        
        fig_forecast.update_layout(
            title=f'{selected_ticker} - Future Price Forecast (Holt-Winters Exponential Smoothing)',
            xaxis_title='Date',
            yaxis_title='Stock Price ($)',
            height=500,
            template='plotly_dark',
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_forecast, key="future-forecast-chart", use_container_width=True)
        
        # Show model info
        with st.expander("📋 View Exponential Smoothing Model Info"):
            st.markdown(f"""
            **Model Type:** Holt-Winters Exponential Smoothing (Additive)
            - **Trend:** Additive with damping
            - **Seasonality:** Additive (6 periods)
            - **Forecast Horizon:** {forecast_steps} periods (~{forecast_steps * 2} weeks)
            - **Residual Std Dev:** ${residual_std:.2f}
            """)
        
    except Exception as e:
        st.warning(f"Could not generate forecast: {str(e)}")
        st.info("The forecast model encountered an issue with this data.")
    
    # ============= DASHBOARD FOOTER =============
    st.markdown("---")
    
    # About section
    st.markdown("""
    ### 📚 About This Dashboard
    
    This comprehensive stock analysis dashboard combines multiple advanced time series techniques:
    - **Statistical Decomposition** to understand underlying patterns
    - **ARIMA/SARIMAX Models** for rigorous forecasting with uncertainty quantification
    - **Exponential Smoothing** for trend and seasonal projections
    - **Model Diagnostics** to ensure prediction reliability
    
    **Data Source:** Yahoo Finance API via `yfinance`  
    **Analysis Period:** April 2018 - Present (biweekly aggregation)  
    **Models:** ARIMA(2,1,2), SARIMAX(1,1,1)(1,1,0,6), Holt-Winters Exponential Smoothing
    """)
    
    st.markdown("---")
    
    # Connect and attribution section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 20px;">
            <h3>🤝 Let's Connect!</h3>
            <p>Interested in data science, finance, or time series analysis? Let's connect!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Social media buttons
        col_a, col_b, col_c = st.columns([1, 1, 1])
        
        with col_a:
            st.markdown("")
        
        with col_b:
            st.markdown("""
            <div style="display: flex; justify-content: center; gap: 20px; margin: 20px 0;">
                <a href="https://www.linkedin.com/in/dominik-huffield" target="_blank" style="text-decoration: none;">
                    <div style="padding: 12px 24px; background: linear-gradient(135deg, #0077b5 0%, #005885 100%); 
                         border-radius: 8px; text-align: center; color: white; font-weight: bold; 
                         box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.2s;">
                        🔗 LinkedIn
                    </div>
                </a>
                <a href="https://github.com/cogentdom" target="_blank" style="text-decoration: none;">
                    <div style="padding: 12px 24px; background: linear-gradient(135deg, #333 0%, #1a1a1a 100%); 
                         border-radius: 8px; text-align: center; color: white; font-weight: bold; 
                         box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: transform 0.2s;">
                        💻 GitHub
                    </div>
                </a>
            </div>
            """, unsafe_allow_html=True)
        
        with col_c:
            st.markdown("")
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; padding: 20px; color: #999; font-size: 14px;">
        <p>Dashboard built with ❤️ using Streamlit, Plotly, and Statsmodels</p>
        <p style="font-size: 12px;">© 2026 - All Rights Reserved</p>
    </div>
    """, unsafe_allow_html=True)

# %%
if __name__ == '__main__':
    main()    
        