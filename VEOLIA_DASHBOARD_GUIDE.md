# Veolia Customer Portal Dashboard - Setup Guide

## 🚀 Quick Start (5 Minutes)

### Step 1: Install Dependencies

```bash
pip install -r veolia_requirements.txt
```

Or install individually:
```bash
pip install streamlit pandas plotly numpy openpyxl
```

---

### Step 2: Run the Dashboard

```bash
streamlit run veolia_dashboard.py
```

The dashboard will automatically:
✅ Load data from your Google Sheets
✅ Open in your browser at http://localhost:8501
✅ Display all KPIs and visualizations

---

## 📊 Dashboard Features

### Phase 1: Core Adoption Metrics

**Top KPI Cards:**
- Total Registered Users (cumulative)
- Weekly Active Users (WAU)
- Monthly Active Users (MAU)
- Returning Users
- Total Sessions
- Average Engagement Rate
- Average Engagement Time
- Active Users (Period)
- Total Page Views

**Visualizations:**
1. **Weekly Active Users Trend** - Line chart showing WAU over time
2. **Monthly Active Users Trend** - Line chart showing MAU over time
3. **New vs Returning Users** - Pie chart breakdown
4. **Daily Engagement Metrics** - Dual-axis chart (engagement rate + time)
5. **Top Pages by Views** - Bar chart
6. **Page Performance Details** - Data table

### Phase 2: Business Demographic Segmentation

**Visualizations:**
1. **Users by Region** - Horizontal bar chart
2. **Users by Sales Organization** - Horizontal bar chart
3. **Sessions by Region and Sales Org** - Sunburst chart
4. **Top Active Accounts** - Detailed data table
5. **Sessions by Device** - Pie chart
6. **Daily Active Users** - Area chart

---

## 🎨 Filters (Interactive)

**Sidebar filters allow you to slice data by:**
- Date Range (Last 7/30/90 Days, All Time)
- Region (multi-select)
- Sales Organization (multi-select)
- Device Category (multi-select)

All charts update in real-time when filters change.

---

## 📥 Data Export

**Export filtered data:**
1. Click sidebar → "Export Data"
2. Click "Download Dashboard Data (CSV)"
3. Get timestamped CSV file with all filtered data

---

## 🔄 Auto-Refresh from Google Sheets

**Current Setup:**
- Dashboard loads data from your Google Sheets on each refresh
- Data is cached for 1 hour (3600 seconds)
- Manual refresh: Click "Rerun" in Streamlit or press 'R'

**To enable auto-refresh every X minutes:**

Add this to the top of `veolia_dashboard.py`:

```python
import time
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every 5 minutes (300000 milliseconds)
count = st_autorefresh(interval=300000, key="datarefresh")
```

Install dependency:
```bash
pip install streamlit-autorefresh
```

---

## 🎯 Customization Guide

### Change Colors (Match Your Branding)

Edit the CSS section in `veolia_dashboard.py`:

```python
st.markdown("""
<style>
    .main-header {
        color: #0066CC;  /* Change to your brand color */
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);  /* Your gradient */
    }
</style>
""", unsafe_allow_html=True)
```

### Add Your Logo

Replace the placeholder image in sidebar:

```python
st.sidebar.image("path/to/your/logo.png", use_column_width=True)
```

### Modify KPI Calculations

All KPI calculations are in dedicated functions:
- `calculate_wau_mau()` - Weekly/Monthly active users
- `calculate_returning_users()` - New vs returning split

Edit these functions to adjust logic.

---

## 📊 Data Requirements

### Google Sheets Structure

**Sheet 1: GA4 Data**
Required columns:
- `date` - Date of event (YYYY-MM-DD)
- `user_id` - User identifier
- `event_name` - Event type (login_success, page_view, etc.)
- `device_category` - Device type (desktop, mobile, tablet)
- `sessions` - Number of sessions
- `engagement_rate` - Engagement rate (0-1)
- `avg_engagement_time` - Average engagement time in seconds
- `page_views` - Number of page views

**Sheet 2: customer_tracking**
Required columns:
- `customer_id` - Customer identifier (joins with user_id)
- `customer_email` - Email address
- `company_name` - Company name
- `sales_org` - Sales organization
- `pole` - Business pole
- `region` - Geographic region
- `account_id` - Account/Sold-to number
- `created_at` - Registration date

### Joining Logic

The dashboard joins:
```python
df_ga4.merge(df_customers, left_on='user_id', right_on='customer_id', how='left')
```

**Ensure:** `user_id` in GA4 matches `customer_id` in customer_tracking

---

## 🚀 Deployment Options

### Option 1: Streamlit Cloud (FREE)

1. **Push code to GitHub**
   ```bash
   git init
   git add veolia_dashboard.py veolia_requirements.txt
   git commit -m "Veolia dashboard"
   git push
   ```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `veolia_dashboard.py`
   - Deploy!

3. **Get shareable link**
   - Example: `https://veolia-portal-analytics.streamlit.app`
   - Share with stakeholders

---

### Option 2: Docker Deployment

**Create `Dockerfile`:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY veolia_requirements.txt .
RUN pip install --no-cache-dir -r veolia_requirements.txt

COPY veolia_dashboard.py .

EXPOSE 8501

CMD ["streamlit", "run", "veolia_dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

**Build and run:**
```bash
docker build -t veolia-dashboard .
docker run -p 8501:8501 veolia-dashboard
```

---

### Option 3: Internal Server

**Run with systemd service:**

Create `/etc/systemd/system/veolia-dashboard.service`:

```ini
[Unit]
Description=Veolia Portal Dashboard
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/dashboard
ExecStart=/usr/bin/streamlit run veolia_dashboard.py --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable and start:**
```bash
sudo systemctl enable veolia-dashboard
sudo systemctl start veolia-dashboard
```

---

## 🔐 Security Considerations

### For Production Deployment:

**1. Secure Google Sheets Access**

Current setup uses public export URLs. For production:

```python
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Use service account credentials
creds = service_account.Credentials.from_service_account_file(
    'credentials.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
)

service = build('sheets', 'v4', credentials=creds)
```

**2. Add Authentication**

Install streamlit-authenticator:
```bash
pip install streamlit-authenticator
```

Add to dashboard:
```python
import streamlit_authenticator as stauth

authenticator = stauth.Authenticate(
    names=['Admin User'],
    usernames=['admin'],
    passwords=['hashed_password'],
    cookie_name='veolia_auth',
    key='auth_key',
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    # Show dashboard
    st.write(f'Welcome {name}')
elif authentication_status == False:
    st.error('Username/password is incorrect')
```

**3. Environment Variables**

Store sensitive data in `.env`:
```
GOOGLE_SHEETS_ID=your_sheet_id
GOOGLE_SERVICE_ACCOUNT_PATH=path/to/credentials.json
```

Load with python-dotenv:
```python
from dotenv import load_dotenv
import os

load_dotenv()
sheet_id = os.getenv('GOOGLE_SHEETS_ID')
```

---

## 🐛 Troubleshooting

### Dashboard won't load data

**Error:** "Unable to load data"

**Solutions:**
1. Check Google Sheets is publicly accessible
2. Verify sheet URL is correct
3. Check column names match exactly
4. Look at terminal for specific error messages

### Charts not displaying

**Error:** Blank charts or "No data available"

**Solutions:**
1. Check date range filter - expand to "All Time"
2. Remove region/sales org filters
3. Verify data has values in date column
4. Check data types (dates should be datetime)

### Slow performance

**Solutions:**
1. Reduce data volume - filter in Google Sheets
2. Increase cache TTL: `@st.cache_data(ttl=7200)`
3. Limit date range in filters
4. Deploy to cloud with more resources

---

## 📈 Next Steps / Phase 2 Enhancements

**Features to add:**
- [ ] Drill-down capability (click chart to filter)
- [ ] Comparison mode (compare periods)
- [ ] Goal tracking (set targets, show progress)
- [ ] Email reports (scheduled PDFs)
- [ ] Advanced segmentation (cohort analysis)
- [ ] Predictive analytics (forecast trends)
- [ ] Custom date range picker
- [ ] Export to PowerPoint
- [ ] Mobile-optimized views

---

## 💡 Tips for Success

**1. Start Simple**
- Deploy basic version first
- Get stakeholder feedback
- Iterate based on actual usage

**2. Monitor Usage**
- Add Google Analytics to track dashboard usage
- See which KPIs get the most attention
- Remove unused metrics

**3. Keep Data Fresh**
- Set up automated exports from RJMetrics
- Schedule Google Sheets updates
- Monitor data quality

**4. Document Assumptions**
- Add tooltips explaining calculations
- Include methodology notes
- Version your metrics definitions

---

## 🆘 Support

**Issues with the dashboard?**

1. Check terminal output for errors
2. Verify data format in Google Sheets
3. Test with sample data first
4. Review this guide's troubleshooting section

**Need help?**
- Streamlit docs: https://docs.streamlit.io
- Plotly docs: https://plotly.com/python/
- Pandas docs: https://pandas.pydata.org

---

## 📝 Version History

**v1.0.0** - Initial Phase 1 baseline
- Core adoption metrics
- Business demographic segmentation
- Interactive filters
- Export capability

---

**You're ready to go! Run `streamlit run veolia_dashboard.py` and see your dashboard! 🚀**
