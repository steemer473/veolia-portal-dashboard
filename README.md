# Veolia Customer Portal Dashboard

A Streamlit dashboard for **Veolia Customer Portal Analytics** — Phase 1: Core Adoption Metrics & Business Demographic Segmentation.

## Features

- **Core adoption metrics**: Total registered users, Weekly Active Users (WAU), Monthly Active Users (MAU), returning vs new users, and session trends
- **Business demographic segmentation**: Filters and views by region, sales organization, and device category
- **Interactive filters**: Date range (7/30/90 days or all time), region, sales org, and device
- **Visualizations**: Charts built with Plotly (time series, demographics, engagement)
- **Data source**: Reads from Google Sheets (GA4 and customer data), with cached loading

## Requirements

- Python 3.9+
- Dependencies listed in `veolia_requirements.txt`

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/veolia-portal-dashboard.git
   cd veolia-portal-dashboard
   ```

2. **Create a virtual environment and install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   pip install -r veolia_requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   streamlit run veolia_dashboard.py
   ```

4. Open the URL shown in the terminal (default: http://localhost:8501).

## Project structure

| File | Description |
|------|-------------|
| `veolia_dashboard.py` | Main Streamlit app and analytics logic |
| `veolia_requirements.txt` | Python dependencies (Streamlit, pandas, Plotly, etc.) |

## Data

The dashboard expects data from Google Sheets (GA4 export and customer list). Sheet URLs are configured in the app. Ensure the sheets are accessible and contain the expected columns for the dashboard to load correctly.

## License

Internal use — Veolia Customer Portal Analytics.
