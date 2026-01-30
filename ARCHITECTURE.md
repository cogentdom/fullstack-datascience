# Architecture Documentation

## 📐 System Architecture

This document provides a detailed technical overview of the Financial Time Series Analytics Platform architecture, design decisions, and implementation details.

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Layer                            │
│                    (Web Browser)                             │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP
                         │ Port 8501
┌────────────────────────▼────────────────────────────────────┐
│                  Streamlit Application                       │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐      │
│  │   main.py    │  │ datamover.py │  │   Models    │      │
│  │              │  │              │  │             │      │
│  │ • UI Logic   │  │ • Data Fetch │  │ • ARIMA     │      │
│  │ • Routing    │  │ • Transform  │  │ • Stats     │      │
│  │ • State Mgmt │  │ • Cache      │  │ • Decomp    │      │
│  └──────────────┘  └──────────────┘  └─────────────┘      │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTPS API
                         │
┌────────────────────────▼────────────────────────────────────┐
│              External Data Sources                           │
│                                                              │
│  ┌──────────────────────────────────────────────┐          │
│  │         Yahoo Finance API (yfinance)          │          │
│  │                                                │          │
│  │  • Real-time market data                      │          │
│  │  • Historical price data                      │          │
│  │  • Volume and OHLC data                       │          │
│  └──────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Component Details

### 1. Frontend Layer (Streamlit)

**Technology**: Streamlit 1.40.1

**Responsibilities**:
- User interface rendering
- Interactive widget management
- Session state management
- Real-time data updates
- Chart rendering and interactions

**Key Features**:
- Sidebar navigation for ticker selection
- Date range pickers for custom analysis periods
- Real-time parameter adjustment for ARIMA models
- Tabbed interface for organized content
- Responsive layout for various screen sizes

**File**: `main.py` (1033 lines)

### 2. Data Layer (DataMover)

**Technology**: pandas, yfinance

**Responsibilities**:
- Fetching real-time and historical market data
- Data cleaning and preprocessing
- Format standardization
- Caching and persistence
- Multi-ticker data aggregation

**Key Classes**:

```python
class DataMover:
    """
    Handles all data fetching and transformation operations.
    
    Features:
    - Download stock data from Yahoo Finance
    - Handle MultiIndex columns from newer yfinance versions
    - Support for single and multi-ticker loading
    - JSON serialization for data persistence
    """
```

**File**: `datamover.py`

### 3. Analytics Layer

**Technologies**: statsmodels, scipy, numpy

**Responsibilities**:
- Time series forecasting (ARIMA)
- Statistical analysis and testing
- Seasonal decomposition
- Autocorrelation analysis
- Returns and volatility calculations

**Implemented Models**:

#### ARIMA (AutoRegressive Integrated Moving Average)
- **Purpose**: Time series forecasting
- **Parameters**: 
  - p (AR order): 0-5
  - d (Differencing): 0-2
  - q (MA order): 0-5
- **Output**: Future price predictions with confidence intervals

#### Statistical Tests
- **Shapiro-Wilk**: Normality testing
- **ACF/PACF**: Autocorrelation analysis
- **Decomposition**: Trend, seasonal, residual components

### 4. Visualization Layer

**Technologies**: Plotly, Matplotlib, Seaborn, mplfinance

**Responsibilities**:
- Interactive charts (Plotly)
- Static statistical plots (Matplotlib/Seaborn)
- Financial-specific visualizations (mplfinance)
- Consistent color theming

**Visualization Types**:
- Candlestick charts
- Line charts (price, volume, indicators)
- Distribution histograms
- Q-Q plots
- Heatmaps for correlation
- Decomposition plots
- ACF/PACF correlograms

**Color Palette**:
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
}
```

### 5. Infrastructure Layer

#### Docker Configuration

**Container Setup**:

```yaml
services:
  dashboard-report:
    image: dashboard:v0
    container_name: dashboard-report
    build: .
    ports:
      - 8501:8501
    restart: on-failure
```

**Dockerfile Strategy**:
- Base image: Python 3.8-slim (minimal footprint)
- Multi-stage potential for future optimization
- Layer caching for faster rebuilds
- Health checks for container orchestration

## 🔄 Data Flow

### 1. User Request Flow

```
User Input → Streamlit Widget → Session State Update → Data Fetch → 
Processing → Model Training → Visualization → Render to Browser
```

### 2. Data Processing Pipeline

```
Yahoo Finance API
    ↓
yfinance.download()
    ↓
DataFrame Creation
    ↓
Data Cleaning (handle MultiIndex, NaN values)
    ↓
Feature Engineering (returns, rolling stats)
    ↓
Model Training (ARIMA, decomposition)
    ↓
Predictions & Diagnostics
    ↓
Visualization Rendering
```

### 3. Caching Strategy

Streamlit provides built-in caching mechanisms:

```python
@st.cache_data
def load_data(ticker, start, stop):
    """Cache data fetching to avoid redundant API calls"""
    # Implementation
```

**Cache Invalidation**:
- TTL-based for real-time data
- User-triggered via sidebar controls
- Parameter-based (ticker, date range changes)

## 🗄️ Data Models

### Stock Data DataFrame Structure

```python
DataFrame Schema:
- Date (datetime64): Trading date
- Open (float64): Opening price
- High (float64): Highest price of the day
- Low (float64): Lowest price of the day
- Close (float64): Closing price
- Volume (int64): Trading volume
- Adj Close (float64): Adjusted closing price

Additional Computed Columns:
- Daily_Return (float64): Percentage daily return
- Rolling_Mean_N (float64): N-day rolling average
- Rolling_Std_N (float64): N-day rolling standard deviation
- Cumulative_Return (float64): Cumulative return from start
```

### ARIMA Model Structure

```python
Model Parameters:
- order: Tuple (p, d, q)
  - p: Number of lag observations (AR term)
  - d: Degree of differencing (I term)
  - q: Size of moving average window (MA term)

Model Output:
- Fitted values: Historical predictions
- Forecast: Future predictions
- Standard errors: Prediction uncertainty
- Confidence intervals: Upper/lower bounds
- Residuals: Prediction errors
- AIC/BIC: Model quality metrics
```

## 🔐 Security Considerations

### Current Implementation

1. **No Authentication**: Currently open dashboard (suitable for development)
2. **Docker Isolation**: Application runs in isolated containers
3. **Read-Only Operations**: No data writes to external services
4. **API Rate Limiting**: Respects Yahoo Finance API limits

### Production Enhancements (Recommended)

1. **Authentication**: Add Streamlit authentication or OAuth
2. **HTTPS**: Enable SSL certificates via Let's Encrypt
3. **Environment Variables**: Store secrets in env files (not in code)
4. **Rate Limiting**: Implement request throttling
5. **Input Validation**: Sanitize user inputs for ticker symbols
6. **Network Policies**: Restrict container communication

## 📊 Performance Optimization

### Current Optimizations

1. **Caching**: Streamlit's `@st.cache_data` decorator
2. **Lazy Loading**: Data fetched only when needed
3. **Vectorization**: NumPy/Pandas vectorized operations
4. **Minimal Dependencies**: Slim Docker base image

### Future Improvements

1. **Database Layer**: Cache data in Redis or PostgreSQL
2. **Async Operations**: Concurrent data fetching
3. **CDN**: Serve static assets via CDN
4. **Load Balancing**: Multiple Streamlit instances
5. **WebSocket Optimization**: Reduce Streamlit communication overhead

## 🧩 Design Patterns

### 1. Singleton Pattern
- DataMover instance: Single data fetching manager per session

### 2. Factory Pattern
- Visualization creation based on user selection

### 3. Observer Pattern
- Streamlit's reactive model: UI updates on state changes

### 4. Strategy Pattern
- Pluggable forecast models (ARIMA, future: LSTM, Prophet)

## 🚀 Deployment Architecture

### Local Development
```
localhost:8501 → Streamlit App
```

### Docker Local
```
localhost:8501 → Streamlit Container
```

### AWS EC2 Production
```
Domain (Cloudflare DNS)
    ↓
EC2 Public IP (Elastic IP recommended)
    ↓
Port 8501 → Streamlit Container
```

### Scaling Strategy

**Horizontal Scaling**:
- Multiple EC2 instances behind ELB (Elastic Load Balancer)
- Docker Swarm or Kubernetes orchestration
- Shared Redis cache for session state

**Vertical Scaling**:
- Larger EC2 instance types (t3.medium, t3.large)
- Optimized for CPU (model training) or Memory (large datasets)

## 🔍 Monitoring & Observability

### Recommended Tools

1. **Application Metrics**:
   - Prometheus for metrics collection
   - Grafana for visualization
   - Track: response times, error rates, user sessions

2. **Logging**:
   - Centralized logging (ELK stack or CloudWatch)
   - Structured logs with correlation IDs
   - Error tracking (Sentry)

3. **Infrastructure**:
   - Docker health checks
   - EC2 CloudWatch metrics
   - Application access logs

## 🧪 Testing Strategy

### Current State
- Manual testing during development
- Visual validation of charts and predictions

### Recommended Additions

1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test data pipeline end-to-end
3. **UI Tests**: Selenium/Playwright for Streamlit interactions
4. **Performance Tests**: Load testing with locust
5. **Data Validation**: Great Expectations for data quality

## 📈 Future Architecture Enhancements

### Short-term
1. Add PostgreSQL for data persistence
2. Implement user authentication
3. Add more forecasting models (LSTM, Prophet)
4. Real-time alerts and notifications

### Long-term
1. Microservices architecture (separate forecast service)
2. Message queue for async processing (RabbitMQ/Kafka)
3. ML model serving layer (TensorFlow Serving)
4. Multi-region deployment
5. Mobile-responsive PWA

## 📝 Design Decisions Log

### Why Streamlit?
- **Pros**: Rapid prototyping, Python-native, built-in widgets
- **Cons**: Limited customization compared to React/Vue
- **Decision**: Best for MVP and data science focus

### Why ARIMA?
- **Pros**: Industry standard, interpretable, good for univariate series
- **Cons**: Assumes stationarity, linear relationships
- **Decision**: Starting point; can add LSTM/Prophet later

### Why Docker Compose?
- **Pros**: Simple container setup, easy local development
- **Cons**: Not production-grade orchestration
- **Decision**: Sufficient for single-instance deployment; can migrate to K8s

## 🔗 Related Documentation

- [README.md](README.md) - Project overview and quick start
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [requirements.txt](requirements.txt) - Python dependencies

---

**Last Updated**: January 2026  
**Version**: 1.0.0  
**Maintained By**: Project Contributors

