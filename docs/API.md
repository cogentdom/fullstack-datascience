# API Documentation

This document describes the internal APIs and data structures used in the Financial Time Series Analytics Platform.

## 📚 Table of Contents

- [DataMover Class](#datamover-class)
- [ModelPlot Class](#modelplot-class)
- [Data Structures](#data-structures)
- [Configuration](#configuration)
- [External APIs](#external-apis)

## 🔄 DataMover Class

The `DataMover` class handles all data fetching and transformation operations.

### Constructor

```python
DataMover(start: str, stop: str)
```

**Parameters:**
- `start` (str): Start date in format "YYYY-MM-DD"
- `stop` (str): End date in format "YYYY-MM-DD"

**Example:**
```python
from datamover import DataMover

mover = DataMover("2018-01-01", "2023-12-31")
```

### Methods

#### load_data()

Fetches stock data for a single ticker.

```python
def load_data(ticker: str) -> pd.DataFrame
```

**Parameters:**
- `ticker` (str): Stock ticker symbol (e.g., "AAPL")

**Returns:**
- `pd.DataFrame`: DataFrame with columns:
  - Date (datetime64)
  - Open (float64)
  - High (float64)
  - Low (float64)
  - Close (float64)
  - Volume (int64)
  - Adj Close (float64)

**Example:**
```python
df = mover.load_data("AAPL")
print(df.head())
```

**Notes:**
- Handles MultiIndex columns from newer yfinance versions
- Resets index to make Date a column
- Converts Date to datetime64

#### load_datas()

Fetches data for multiple tickers.

```python
def load_datas(ticker_list: List[str]) -> pd.DataFrame
```

**Parameters:**
- `ticker_list` (List[str]): List of ticker symbols

**Returns:**
- `pd.DataFrame`: DataFrame with Date column and Close prices for each ticker

**Example:**
```python
tickers = ["AAPL", "GOOG", "MSFT", "TSLA"]
df = mover.load_datas(tickers)
print(df.head())
```

**DataFrame Structure:**
```
      Date        AAPL      GOOG      MSFT      TSLA
0   2018-01-02   41.23    51.36    83.19    20.62
1   2018-01-03   41.40    52.03    83.95    21.13
...
```

#### write_json()

Writes DataFrame to JSON file.

```python
def write_json(df: pd.DataFrame, path: str) -> None
```

**Parameters:**
- `df` (pd.DataFrame): DataFrame to save
- `path` (str): File path for JSON output

**Example:**
```python
mover.write_json(df, "data/stock_data.json")
```

#### read_json()

Reads JSON file and returns as dictionary.

```python
def read_json(path: str) -> dict
```

**Parameters:**
- `path` (str): File path to JSON file

**Returns:**
- `dict`: JSON content as Python dictionary

**Example:**
```python
data = mover.read_json("data/stock_data.json")
```

## 📊 ModelPlot Class

Handles visualization creation (deprecated in main.py, kept for reference).

### Constructor

```python
ModelPlot()
```

Initializes matplotlib style settings.

### Methods

#### decomp_plot()

Creates rolling mean and standard deviation plot.

```python
def decomp_plot(df: pd.Series) -> matplotlib.figure.Figure
```

**Parameters:**
- `df` (pd.Series): Time series data

**Returns:**
- `matplotlib.figure.Figure`: Plot figure

#### plot_raw_data()

Creates interactive Plotly chart (displays in Streamlit).

```python
def plot_raw_data(data: pd.DataFrame) -> None
```

**Parameters:**
- `data` (pd.DataFrame): Stock data with High and Low columns

#### plot_arima()

Creates ARIMA forecast visualization.

```python
def plot_arima(df: pd.DataFrame, label: str) -> matplotlib.figure.Figure
```

**Parameters:**
- `df` (pd.DataFrame): Stock data
- `label` (str): Column name to forecast

**Returns:**
- `matplotlib.figure.Figure`: Plot with forecasts

## 📋 Data Structures

### Stock Data DataFrame

**Schema:**
```python
{
    'Date': 'datetime64[ns]',
    'Open': 'float64',
    'High': 'float64',
    'Low': 'float64',
    'Close': 'float64',
    'Volume': 'int64',
    'Adj Close': 'float64'
}
```

**Example:**
```python
import pandas as pd

# Sample data structure
df = pd.DataFrame({
    'Date': pd.date_range('2023-01-01', periods=5),
    'Open': [150.0, 151.0, 152.0, 153.0, 154.0],
    'High': [155.0, 156.0, 157.0, 158.0, 159.0],
    'Low': [149.0, 150.0, 151.0, 152.0, 153.0],
    'Close': [154.0, 155.0, 156.0, 157.0, 158.0],
    'Volume': [1000000, 1100000, 1200000, 1300000, 1400000],
    'Adj Close': [154.0, 155.0, 156.0, 157.0, 158.0]
})
```

### ARIMA Model Output

```python
{
    'model': ARIMA model object,
    'forecast': pd.Series,        # Predicted values
    'forecast_ci': pd.DataFrame,  # Confidence intervals
    'residuals': pd.Series,       # Model residuals
    'aic': float,                 # Akaike Information Criterion
    'bic': float                  # Bayesian Information Criterion
}
```

### Session State Structure

Streamlit session state variables:

```python
st.session_state = {
    'selected_ticker': str,      # Current ticker
    'data_cache': dict,          # Cached data by ticker
    'arima_params': {            # ARIMA parameters
        'p': int,
        'd': int,
        'q': int
    },
    'forecast_days': int         # Forecast horizon
}
```

## ⚙️ Configuration

### Streamlit Configuration

**File:** `.streamlit/config.toml`

```toml
[theme]
primaryColor = "#03fca5"           # Primary accent color
backgroundColor = "#242b29"         # Main background
secondaryBackgroundColor = "#4d4d4d"  # Sidebar background
textColor = "#e8e8e8"              # Text color
font = "sans serif"                # Font family

[server]
port = 8501                        # Server port
enableCORS = false                 # CORS settings
enableXsrfProtection = true        # CSRF protection

[browser]
gatherUsageStats = false           # Analytics
```

### Color Palette

**Defined in:** `main.py`

```python
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
```

### ARIMA Default Parameters

```python
DEFAULT_ARIMA_PARAMS = {
    'p': 5,  # AR order
    'd': 1,  # Differencing
    'q': 0   # MA order
}
```

## 🌐 External APIs

### Yahoo Finance API (yfinance)

**Library:** `yfinance`  
**Version:** 1.1.0

#### Endpoints Used

```python
import yfinance as yf

# Download stock data
data = yf.download(
    ticker: str,           # Stock symbol
    start: str,            # Start date "YYYY-MM-DD"
    end: str,              # End date "YYYY-MM-DD"
    interval: str = "1d",  # Data interval
    auto_adjust: bool = True  # Adjust for splits/dividends
)
```

#### Rate Limits

- **Limit:** Approximately 2,000 requests per hour
- **Recommendation:** Implement caching to reduce API calls
- **Retry Logic:** Built into yfinance library

#### Error Handling

```python
try:
    data = yf.download(ticker, start, end)
    if data.empty:
        raise ValueError(f"No data found for ticker: {ticker}")
except Exception as e:
    print(f"Error fetching data: {e}")
    # Handle error appropriately
```

#### Available Data Fields

```python
{
    'Open': 'Opening price',
    'High': 'Highest price',
    'Low': 'Lowest price',
    'Close': 'Closing price',
    'Adj Close': 'Adjusted closing price',
    'Volume': 'Trading volume'
}
```

### Ticker Information

```python
import yfinance as yf

ticker = yf.Ticker("AAPL")

# Company information
info = ticker.info
print(info['longName'])      # Company name
print(info['sector'])        # Business sector
print(info['marketCap'])     # Market capitalization
```

## 🔌 Integration Examples

### Basic Data Fetch

```python
from datamover import DataMover
import pandas as pd

# Initialize data mover
mover = DataMover("2020-01-01", "2023-12-31")

# Fetch single ticker
df = mover.load_data("AAPL")

# Calculate returns
df['Returns'] = df['Close'].pct_change()

# Rolling statistics
df['MA_30'] = df['Close'].rolling(window=30).mean()
df['Volatility'] = df['Returns'].rolling(window=30).std()

print(df.tail())
```

### ARIMA Forecasting

```python
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd

# Prepare data
close_prices = df['Close']

# Fit model
model = ARIMA(close_prices, order=(5, 1, 0))
fitted_model = model.fit()

# Generate forecast
forecast_steps = 30
forecast = fitted_model.forecast(steps=forecast_steps)

# Get confidence intervals
forecast_df = fitted_model.get_forecast(steps=forecast_steps)
confidence_intervals = forecast_df.conf_int()

print(f"Forecast for next {forecast_steps} days:")
print(forecast)
```

### Seasonal Decomposition

```python
from statsmodels.tsa.seasonal import seasonal_decompose

# Decompose time series
decomposition = seasonal_decompose(
    df['Close'],
    model='multiplicative',  # or 'additive'
    period=252  # Trading days in a year
)

# Access components
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

# Plot (in Streamlit)
import streamlit as st
st.pyplot(decomposition.plot())
```

## 🧪 Testing API Calls

### Unit Test Example

```python
import unittest
from datamover import DataMover
import pandas as pd

class TestDataMover(unittest.TestCase):
    
    def setUp(self):
        self.mover = DataMover("2023-01-01", "2023-12-31")
    
    def test_load_data(self):
        df = self.mover.load_data("AAPL")
        
        # Check DataFrame is not empty
        self.assertFalse(df.empty)
        
        # Check expected columns exist
        expected_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        for col in expected_columns:
            self.assertIn(col, df.columns)
        
        # Check data types
        self.assertEqual(df['Date'].dtype, 'datetime64[ns]')
        self.assertEqual(df['Close'].dtype, 'float64')
    
    def test_load_multiple_tickers(self):
        tickers = ["AAPL", "GOOG", "MSFT"]
        df = self.mover.load_datas(tickers)
        
        # Check all tickers in columns
        for ticker in tickers:
            self.assertIn(ticker, df.columns)

if __name__ == '__main__':
    unittest.main()
```

## 📝 API Best Practices

1. **Caching:** Use Streamlit's `@st.cache_data` decorator
2. **Error Handling:** Always wrap API calls in try-except
3. **Rate Limiting:** Respect API rate limits
4. **Data Validation:** Validate data after fetching
5. **Logging:** Log API calls for debugging

## 🔗 Related Documentation

- [yfinance Documentation](https://pypi.org/project/yfinance/)
- [statsmodels Documentation](https://www.statsmodels.org/)
- [Streamlit API Reference](https://docs.streamlit.io/)

---

**Last Updated:** January 2026  
**Version:** 1.0.0

