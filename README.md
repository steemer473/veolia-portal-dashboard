# Veolia Customer Portal Dashboard

A Streamlit dashboard for **Veolia Customer Portal Analytics** — Phase 1: Core Adoption Metrics & Business Demographic Segmentation.

## Features

- **Core adoption metrics**: Total registered users, Weekly Active Users (WAU), Monthly Active Users (MAU), returning vs new users, and session trends
- **Business demographic segmentation**: Filters and views by region, sales organization, and device category
- **Interactive filters**: Date range (7/30/90 days or all time), region, sales org, and device
- **Visualizations**: Charts built with Plotly (time series, demographics, engagement)
- **Data source**: Manual CSV upload (no Google Sheets or API keys required)

## Requirements

- Python 3.9+
- Dependencies listed in `requirements.txt`

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
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   streamlit run veolia_dashboard.py
   ```

4. Open the URL shown in the terminal (default: http://localhost:8501).
5. In the sidebar, upload two CSV files (see **Data** below).

## Project structure

| File | Description |
|------|-------------|
| `veolia_dashboard.py` | Main Streamlit app and analytics logic |
| `requirements.txt` | Python dependencies (Streamlit, pandas, Plotly, etc.) |

## Data

The dashboard uses **manual CSV upload** in the sidebar. Upload two files:

1. **GA4 / analytics CSV**  
   - **Required columns:** `date`, `user_id`  
   - **Optional:** `device_category`, `sessions`, `engagement_rate`, `avg_engagement_time`, `page_views`, `event_name`

2. **Customer list CSV**  
   - **Required column:** `customer_id` (must match `user_id` in the analytics file for joins)  
   - **Optional:** `created_at`, `region`, `sales_org`, `account_id`, `company_name`

Export your GA4 and customer data to CSV and upload them each time you open or refresh the dashboard. No API keys or Google Sheets access needed.

## License

Internal use — Veolia Customer Portal Analytics.
