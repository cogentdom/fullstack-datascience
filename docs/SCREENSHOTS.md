# Screenshots and Visuals

This document provides guidance on capturing screenshots and creating visual assets for the project.

## 📸 Recommended Screenshots

For a complete GitHub showcase, capture the following screenshots:

### 1. Main Dashboard View

**Filename:** `dashboard-main.png`

**What to capture:**
- Full dashboard with sidebar open
- Default ticker (e.g., AAPL) selected
- Multiple charts visible
- Clean, professional look

**Tips:**
- Use full HD resolution (1920x1080)
- Clear browser cache before capturing
- Hide browser bookmarks bar
- Use default date range for consistency

### 2. Interactive Chart

**Filename:** `interactive-chart.png`

**What to capture:**
- Hover tooltips showing data
- Interactive features visible
- Plotly controls in corner

### 3. ARIMA Forecast

**Filename:** `arima-forecast.png`

**What to capture:**
- Forecast plot with predictions
- Confidence intervals visible
- Legend clearly shown
- Recent data and predictions

### 4. Statistical Analysis

**Filename:** `statistical-analysis.png`

**What to capture:**
- Multiple statistical plots
- Distribution histograms
- Q-Q plot
- ACF/PACF plots

### 5. Seasonal Decomposition

**Filename:** `seasonal-decomposition.png`

**What to capture:**
- All four decomposition components:
  - Observed
  - Trend
  - Seasonal
  - Residual

### 6. Sidebar Controls

**Filename:** `sidebar-controls.png`

**What to capture:**
- Ticker selection dropdown
- Date range pickers
- ARIMA parameter sliders
- Forecast horizon control

### 7. Multiple Tickers Comparison

**Filename:** `multi-ticker.png`

**What to capture:**
- Comparison view if implemented
- Multiple lines on same chart
- Clear legend

### 8. Docker Setup

**Filename:** `docker-setup.png`

**What to capture:**
- Terminal showing `docker-compose up`
- Container status
- Logs showing successful startup

## 🎨 Creating a Hero Image

Create a banner image for your README:

**Dimensions:** 1280x640px (2:1 ratio)

**Elements to include:**
- Project name: "Financial Time Series Analytics Platform"
- Key visual: Chart or dashboard screenshot
- Tech stack badges: Python, Streamlit, Docker, AWS
- Color scheme: Match `.streamlit/config.toml` theme

**Tools:**
- Figma (recommended)
- Canva
- Adobe Photoshop
- GIMP (free)

## 📊 Architecture Diagram

Create a visual architecture diagram:

**Filename:** `architecture-diagram.png`

**Content:**
```
User Browser
    ↓
Streamlit (Port 8501)
    ↓
yfinance API
```

**Tools:**
- [draw.io](https://app.diagrams.net/)
- [Lucidchart](https://www.lucidchart.com/)
- [Excalidraw](https://excalidraw.com/)

## 🎯 GIF Demonstrations

Create animated GIFs showing:

### 1. Ticker Selection

**Filename:** `demo-ticker-selection.gif`

**Steps:**
1. Open sidebar
2. Select different tickers
3. Show dashboard updating

**Duration:** 5-10 seconds

### 2. ARIMA Parameter Adjustment

**Filename:** `demo-arima-params.gif`

**Steps:**
1. Adjust p, d, q sliders
2. Show forecast updating
3. Highlight changes

**Duration:** 10-15 seconds

### 3. Interactive Chart Navigation

**Filename:** `demo-interactive-chart.gif`

**Steps:**
1. Hover over chart
2. Zoom in/out
3. Pan across time
4. Use Plotly controls

**Duration:** 10 seconds

**Tools:**
- [LICEcap](https://www.cockos.com/licecap/) (Windows/Mac)
- [Kap](https://getkap.co/) (Mac)
- [ScreenToGif](https://www.screentogif.com/) (Windows)
- [Peek](https://github.com/phw/peek) (Linux)

## 📁 Recommended Directory Structure

```
docs/
├── images/
│   ├── screenshots/
│   │   ├── dashboard-main.png
│   │   ├── interactive-chart.png
│   │   ├── arima-forecast.png
│   │   ├── statistical-analysis.png
│   │   ├── seasonal-decomposition.png
│   │   └── sidebar-controls.png
│   ├── diagrams/
│   │   ├── architecture-diagram.png
│   │   └── data-flow-diagram.png
│   ├── gifs/
│   │   ├── demo-ticker-selection.gif
│   │   ├── demo-arima-params.gif
│   │   └── demo-interactive-chart.gif
│   └── hero/
│       └── banner.png
```

## 🖼️ Adding Images to README

### Hero Banner

```markdown
![Financial Time Series Analytics Platform](docs/images/hero/banner.png)
```

### Feature Screenshots

```markdown
## Features

### Real-time Stock Analysis
![Dashboard Main View](docs/images/screenshots/dashboard-main.png)

### ARIMA Forecasting
![ARIMA Forecast](docs/images/screenshots/arima-forecast.png)

### Statistical Analysis
![Statistical Analysis](docs/images/screenshots/statistical-analysis.png)
```

### Animated Demos

```markdown
## Demo

### Interactive Ticker Selection
![Ticker Selection Demo](docs/images/gifs/demo-ticker-selection.gif)

### ARIMA Parameter Adjustment
![ARIMA Demo](docs/images/gifs/demo-arima-params.gif)
```

## 🎨 Style Guidelines

### Screenshot Standards

1. **Resolution:** Minimum 1920x1080
2. **Format:** PNG (lossless)
3. **File Size:** < 2MB per image
4. **Aspect Ratio:** Maintain consistent ratios

### Color Consistency

Match theme from `.streamlit/config.toml`:
- Primary: `#03fca5`
- Background: `#242b29`
- Secondary: `#4d4d4d`
- Text: `#e8e8e8`

### Annotation Guidelines

If annotating screenshots:
- Use arrows for highlighting
- Keep annotations minimal
- Use consistent colors
- Ensure text is readable

## 🔧 Screenshot Tools

### Desktop Capture

**macOS:**
- Cmd+Shift+4: Area selection
- Cmd+Shift+5: Screenshot controls

**Windows:**
- Win+Shift+S: Snipping Tool
- Win+PrtScn: Full screen

**Linux:**
- Flameshot (recommended)
- GNOME Screenshot
- Spectacle (KDE)

### Browser Extensions

- [Awesome Screenshot](https://www.awesomescreenshot.com/)
- [Nimbus Screenshot](https://nimbusweb.me/)
- [Full Page Screen Capture](https://chrome.google.com/webstore)

## 📐 Image Optimization

Before committing images:

```bash
# Install optimization tools
npm install -g imageoptim-cli

# Optimize PNG files
imageoptim docs/images/**/*.png

# Or use online tools:
# - TinyPNG (https://tinypng.com/)
# - Squoosh (https://squoosh.app/)
```

## 🌟 Social Media Assets

Create platform-specific images:

### GitHub Social Preview

**Dimensions:** 1280x640px  
**Location:** Repository Settings → Social Preview

### Twitter Card

**Dimensions:** 1200x675px  
**Format:** PNG or JPG

### LinkedIn

**Dimensions:** 1200x627px  
**Format:** PNG or JPG

## 📝 Image Attribution

If using stock images or icons:

```markdown
## Credits

### Icons
- [Heroicons](https://heroicons.com/) - MIT License
- [Font Awesome](https://fontawesome.com/) - Free License

### Stock Images
- [Unsplash](https://unsplash.com/) - Specific image links
```

## 🔗 External Resources

- [GitHub README Generator](https://rahuldkjain.github.io/gh-profile-readme-generator/)
- [Shields.io](https://shields.io/) - Badges
- [SimpleIcons](https://simpleicons.org/) - Brand icons
- [Carbon](https://carbon.now.sh/) - Code screenshots

---

**Last Updated:** January 2026

