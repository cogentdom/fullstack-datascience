# 📈 Financial Time Series Analytics Platform

A full-stack financial analytics dashboard featuring real-time stock market data analysis, ARIMA forecasting models, and interactive visualizations—containerized with Docker and deployable to AWS EC2 with custom domain support.

![banner](https://cogentdom.wordpress.com/wp-content/uploads/2026/01/stock-market-analysis.png)  

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40-red.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## 🌟 Overview

This platform provides comprehensive time series analysis and forecasting for financial markets. It combines statistical modeling (ARIMA), interactive visualizations, and a modern web interface into a containerized application ready for cloud deployment.

**Key Achievement**: Solved complex Docker volume mounting and composition challenges for seamless data persistence across environments—from development to production on AWS EC2.

## ✨ Features

### 📊 Analytics & Modeling
- **Real-time Stock Data**: Live market data fetching via Yahoo Finance API
- **ARIMA Forecasting**: Time series prediction with configurable parameters (p, d, q)
- **Statistical Analysis**: 
  - Moving averages and volatility metrics
  - Returns analysis and distribution modeling
  - Autocorrelation and partial autocorrelation functions
  - Seasonal decomposition (trend, seasonal, residual)
- **Normality Testing**: Shapiro-Wilk and visual Q-Q plots

### 📈 Interactive Visualizations
- **Multi-panel Dashboard**: Candlestick charts, volume analysis, price movements
- **Technical Indicators**: Rolling means, Bollinger bands, volatility measures
- **Forecast Visualization**: Model predictions with confidence intervals
- **Diagnostic Plots**: Residual analysis, ACF/PACF plots, decomposition charts

### 🎨 User Interface
- **Modern Streamlit Dashboard**: Responsive layout with intuitive controls
- **Ticker Selection**: Quick-select popular stocks or enter custom symbols
- **Date Range Filtering**: Analyze specific time periods
- **Customizable Visualizations**: Adjustable parameters and color schemes
- **Real-time Updates**: Dynamic data refresh on selection changes

### 🏗️ Architecture & Deployment
- **Dockerized Application**: Containerized setup for easy deployment
- **AWS EC2 Deployment**: Production-ready cloud infrastructure
- **Custom Domain**: Cloudflare DNS integration for professional access
- **Data Persistence**: Volume mounting for environment consistency
- **CI/CD Ready**: Makefile automation for builds and deployments

## 🚀 Quick Start

### Prerequisites
```bash
# System Requirements
- Python 3.8+
- Docker & Docker Compose
- Git
```

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/architecture-fullstack.git
cd architecture-fullstack
```

2. **Set up Python environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Run the dashboard locally**
```bash
streamlit run main.py
```

The dashboard will open at `http://localhost:8501`

### Docker Deployment

1. **Build and run with Docker Compose**
```bash
docker-compose up --build
```

2. **Access the application**
- Dashboard: `http://localhost:8501`

### Using the Makefile

```bash
# Build new image
make build_new

# Build and publish to Docker Hub
make drhub

# Build and publish to GitHub Container Registry
make git
```

## 📁 Project Structure

```
architecture-fullstack/
├── main.py                 # Main Streamlit application
├── datamover.py           # Data fetching and preprocessing utilities
├── requirements.txt       # Python dependencies
├── Dockerfile            # Container image definition
├── docker-compose.yaml   # Container orchestration
├── Makefile             # Build and deployment automation
├── dev_folder/          # Development notebooks and data
│   ├── dev_notebook.ipynb
│   └── timeseries_analysis.ipynb
└── .streamlit/          # Streamlit configuration
    └── config.toml
```

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.8+**: Primary programming language
- **Streamlit**: Interactive web application framework
- **Pandas & NumPy**: Data manipulation and numerical computing
- **yfinance**: Yahoo Finance API wrapper for real-time market data

### Analytics & Modeling
- **statsmodels**: ARIMA time series forecasting
- **SciPy**: Statistical analysis and testing
- **scikit-learn**: Additional ML utilities

### Visualization
- **Plotly**: Interactive charts and graphs
- **Matplotlib & Seaborn**: Statistical visualizations
- **mplfinance**: Financial-specific chart types (candlesticks, volume)

### DevOps & Infrastructure
- **Docker**: Containerization platform
- **Docker Compose**: Container orchestration
- **AWS EC2**: Cloud compute instance
- **Cloudflare**: DNS and CDN services

## 📊 Usage Examples

### Analyzing a Stock

1. **Select a ticker** from the sidebar (AAPL, GOOG, MSFT, TSLA) or enter a custom symbol
2. **Choose your date range** using the date pickers
3. **Explore the visualizations**:
   - Historical price data and volume
   - Statistical metrics and distributions
   - ARIMA forecast predictions
   - Decomposition analysis

### ARIMA Model Configuration

The dashboard allows you to adjust ARIMA parameters:
- **p (AR order)**: Number of lag observations
- **d (Differencing)**: Degree of differencing
- **q (MA order)**: Size of moving average window

### Forecast Horizon

Set the number of days to forecast into the future (1-90 days).

## 🏛️ Architecture

### Application Architecture
```
┌─────────────────┐
│   User Browser  │
└────────┬────────┘
         │
    ┌────▼────────┐
    │  Streamlit  │ (Port 8501)
    │  Dashboard  │
    └────┬────────┘
         │
    ┌────▼────────┐
    │  yfinance   │
    │     API     │
    └─────────────┘
```

### Data Flow
1. **Data Ingestion**: Real-time stock data fetched via Yahoo Finance API
2. **Processing**: Data cleaning, transformation, and feature engineering
3. **Analysis**: Statistical analysis and ARIMA model training
4. **Visualization**: Interactive charts rendered in Streamlit
5. **Deployment**: Containerized application ready for cloud deployment

## 🌐 Deployment to AWS

### EC2 Setup

1. **Launch EC2 Instance**
   - AMI: Ubuntu 20.04 LTS
   - Instance Type: t2.micro or larger
   - Security Group: Open port 8501

2. **Install Docker**
```bash
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo usermod -aG docker ubuntu
```

3. **Deploy Application**
```bash
git clone <your-repo>
cd architecture-fullstack
docker-compose up -d
```

4. **Configure Domain** (Optional)
   - Point your domain to the EC2 instance IP in Cloudflare DNS

## 🧪 Development

### Running Jupyter Notebooks

The `dev_folder/` contains Jupyter notebooks for experimentation:

```bash
cd dev_folder
jupyter notebook
```

### Adding New Features

1. Create a new branch
2. Implement your feature in `main.py` or create new modules
3. Test locally with `streamlit run main.py`
4. Update tests and documentation
5. Submit a pull request

## 🐛 Troubleshooting

### Common Issues

**Port already in use**
```bash
# Kill process on port 8501
lsof -ti:8501 | xargs kill -9
```

**Docker volume issues**
```bash
# Remove all containers and volumes
docker-compose down -v
docker system prune -a
```

**yfinance data not loading**
- Check your internet connection
- Verify ticker symbol is valid
- Yahoo Finance may temporarily rate-limit requests

## 📝 Configuration

### Streamlit Configuration

Edit `.streamlit/config.toml` to customize:
- Theme colors
- Server settings
- Browser behavior

### Docker Configuration

Modify `docker-compose.yaml` to adjust:
- Port mappings
- Volume mounts
- Resource limits

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Yahoo Finance](https://finance.yahoo.com/) for providing free financial data API
- [Streamlit](https://streamlit.io/) for the amazing web framework
- [statsmodels](https://www.statsmodels.org/) for time series analysis tools

## 📧 Contact

>Dominik Huffield  
>Twitter - [@cogentdom](https://twitter.com/cogentdom)  
>My Work - [portfolio](https://portingdata.com)  
>Business - [ohmic data](https://toroai.io)  

Project Link: [architecture-fullstack](https://github.com/cogentdom/architecture-fullstack)  

---

**⭐ If you found this project helpful, please consider giving it a star!**
