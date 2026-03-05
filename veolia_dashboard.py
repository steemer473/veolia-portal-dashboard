"""
Veolia Customer Portal Dashboard
Phase 1: Core Adoption Metrics & Business Demographic Segmentation
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Veolia Customer Portal Analytics",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Veolia branding
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #0066CC;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1E3A8A;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #0066CC;
        padding-bottom: 0.5rem;
    }
    .stMetric {
        background-color: #F8FAFC;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #0066CC;
    }
</style>
""", unsafe_allow_html=True)

# Data loading functions
def _normalize_ga4_columns(df_ga4):
    """Ensure GA4 dataframe has date column and optional user_id; add synthetic user_id if missing."""
    # Strip whitespace from column names
    df_ga4.columns = df_ga4.columns.str.strip()

    # Find or create date column
    if "date" not in df_ga4.columns:
        date_candidates = [c for c in df_ga4.columns if "date" in c.lower()]
        if date_candidates:
            df_ga4["date"] = pd.to_datetime(df_ga4[date_candidates[0]], errors="coerce")
        else:
            # Try first column as date
            first = df_ga4.columns[0]
            df_ga4["date"] = pd.to_datetime(df_ga4[first], errors="coerce")
        df_ga4 = df_ga4.dropna(subset=["date"])
    else:
        df_ga4["date"] = pd.to_datetime(df_ga4["date"], errors="coerce")
        df_ga4 = df_ga4.dropna(subset=["date"])

    # user_id is optional: add synthetic per-row id if missing
    if "user_id" not in df_ga4.columns:
        df_ga4["user_id"] = np.arange(len(df_ga4))

    return df_ga4


def load_data_from_uploads(upload_ga4, upload_customers, skip_ga4_first_row=False):
    """Load and merge data from two uploaded CSV files."""
    if upload_ga4 is None or upload_customers is None:
        return None, None, None
    try:
        df_ga4 = pd.read_csv(upload_ga4, skiprows=1 if skip_ga4_first_row else 0)
        df_customers = pd.read_csv(upload_customers)

        # GA4: only date is required (user_id optional)
        df_ga4 = _normalize_ga4_columns(df_ga4)
        if df_ga4.empty:
            raise ValueError("GA4 CSV must contain at least one date column or date-like values.")

        # Customer list: require customer_id
        df_customers.columns = df_customers.columns.str.strip()
        if "customer_id" not in df_customers.columns:
            raise ValueError(f"Customers CSV must have column: customer_id. Found: {list(df_customers.columns)}")

        if "created_at" in df_customers.columns:
            df_customers["created_at"] = pd.to_datetime(df_customers["created_at"], errors="coerce")

        df = df_ga4.merge(
            df_customers,
            left_on="user_id",
            right_on="customer_id",
            how="left",
        )
        return df, df_ga4, df_customers
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

def calculate_wau_mau(df):
    """Calculate Weekly and Monthly Active Users"""
    df['week'] = df['date'].dt.to_period('W')
    df['month'] = df['date'].dt.to_period('M')
    
    wau = df.groupby('week')['user_id'].nunique().reset_index()
    wau.columns = ['week', 'WAU']
    
    mau = df.groupby('month')['user_id'].nunique().reset_index()
    mau.columns = ['month', 'MAU']
    
    return wau, mau

def calculate_returning_users(df):
    """Calculate returning vs new users"""
    user_sessions = df.groupby('user_id')['date'].agg(['min', 'count']).reset_index()
    user_sessions.columns = ['user_id', 'first_session', 'session_count']
    
    returning = user_sessions[user_sessions['session_count'] > 1].shape[0]
    new = user_sessions[user_sessions['session_count'] == 1].shape[0]
    
    return returning, new

# ============================================================================
# SIDEBAR - DATA UPLOAD
# ============================================================================

st.sidebar.image("https://via.placeholder.com/200x80/0066CC/FFFFFF?text=Veolia", use_column_width=True)
st.sidebar.markdown("### 📁 Upload data (CSV)")

upload_ga4 = st.sidebar.file_uploader(
    "GA4 / analytics data",
    type=["csv"],
    help="CSV with a date column (required). user_id optional. First row can be a title.",
)
skip_ga4_header = st.sidebar.checkbox(
    "First row of GA4 file is a title (use next row as column names)",
    value=False,
    help="Check this if your CSV has a title row like 'Login Success Metrics' before the column names.",
)
upload_customers = st.sidebar.file_uploader(
    "Customer list",
    type=["csv"],
    help="CSV with column: customer_id (and optionally created_at, region, sales_org)",
)

df, df_ga4, df_customers = load_data_from_uploads(upload_ga4, upload_customers, skip_ga4_first_row=skip_ga4_header)

if df is None:
    st.info(
        "👆 **Upload two CSV files** in the sidebar to run the dashboard:\n\n"
        "1. **GA4 / analytics** – a **date** column is required (or date-like values in the first column). "
        "`user_id` is optional. Optional: `device_category`, `sessions`, `engagement_rate`, `page_views`, etc. "
        "If the first row is a title, check **First row of GA4 file is a title**.\n\n"
        "2. **Customer list** – at least `customer_id`; optional: `created_at`, `region`, `sales_org`, `account_id`, `company_name`."
    )
    st.stop()

# Remember which optional columns were present (before filling)
has_account_columns = "account_id" in df.columns and "company_name" in df.columns

# Ensure optional columns exist so rest of dashboard runs
for col, default in [
    ("sessions", 0),
    ("engagement_rate", 0.0),
    ("avg_engagement_time", 0.0),
    ("page_views", 0),
    ("event_name", ""),
]:
    if col not in df.columns:
        df[col] = default
for col, default in [("region", "N/A"), ("sales_org", "N/A"), ("account_id", ""), ("company_name", "")]:
    if col not in df.columns:
        df[col] = default
if "device_category" not in df.columns:
    df["device_category"] = "Unknown"

# ============================================================================
# SIDEBAR - FILTERS
# ============================================================================

st.sidebar.markdown("### 📊 Dashboard Filters")

# Date range filter
date_range_options = {
    'Last 7 Days': 7,
    'Last 30 Days': 30,
    'Last 90 Days': 90,
    'All Time': None
}

selected_range = st.sidebar.selectbox(
    'Date Range',
    list(date_range_options.keys()),
    index=1  # Default to Last 30 Days
)

if date_range_options[selected_range]:
    end_date = df['date'].max()
    start_date = end_date - timedelta(days=date_range_options[selected_range])
    df_filtered = df[df['date'] >= start_date].copy()
else:
    df_filtered = df.copy()

# Region filter (optional column)
if "region" in df_customers.columns:
    all_regions = ["All Regions"] + sorted(df_customers["region"].dropna().unique().tolist())
    selected_regions = st.sidebar.multiselect("Region", all_regions, default=["All Regions"])
    if "All Regions" not in selected_regions and selected_regions:
        df_filtered = df_filtered[df_filtered["region"].isin(selected_regions)]
else:
    selected_regions = ["All Regions"]

# Sales Org filter (optional column)
if "sales_org" in df_customers.columns:
    all_sales_orgs = ["All Sales Orgs"] + sorted(df_customers["sales_org"].dropna().unique().tolist())
    selected_sales_orgs = st.sidebar.multiselect("Sales Organization", all_sales_orgs, default=["All Sales Orgs"])
    if "All Sales Orgs" not in selected_sales_orgs and selected_sales_orgs:
        df_filtered = df_filtered[df_filtered["sales_org"].isin(selected_sales_orgs)]

# Device filter (optional column)
if "device_category" in df_ga4.columns:
    device_options = ["All Devices"] + sorted(df_ga4["device_category"].dropna().unique().tolist())
    selected_devices = st.sidebar.multiselect("Device Category", device_options, default=["All Devices"])
    if "All Devices" not in selected_devices and selected_devices:
        df_filtered = df_filtered[df_filtered["device_category"].isin(selected_devices)]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Data updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# ============================================================================
# MAIN DASHBOARD
# ============================================================================

# Header
st.markdown('<h1 class="main-header">💧 Veolia Customer Portal Analytics</h1>', unsafe_allow_html=True)
st.markdown(f"**Reporting Period:** {df_filtered['date'].min().strftime('%Y-%m-%d')} to {df_filtered['date'].max().strftime('%Y-%m-%d')}")

# ============================================================================
# SECTION 1: CORE ADOPTION METRICS
# ============================================================================

st.markdown('<div class="section-header">📈 Core Adoption Metrics</div>', unsafe_allow_html=True)

# Top-level KPIs
col1, col2, col3, col4, col5 = st.columns(5)

# Total Registered Users (cumulative)
total_users = df_customers['customer_id'].nunique()
with col1:
    st.metric(
        "Total Registered Users",
        f"{total_users:,}",
        help="Cumulative registered users since launch"
    )

# WAU
wau, mau = calculate_wau_mau(df_filtered)
current_wau = wau['WAU'].iloc[-1] if len(wau) > 0 else 0
with col2:
    st.metric(
        "Weekly Active Users",
        f"{current_wau:,}",
        help="Unique active users in the last week"
    )

# MAU
current_mau = mau['MAU'].iloc[-1] if len(mau) > 0 else 0
with col3:
    st.metric(
        "Monthly Active Users",
        f"{current_mau:,}",
        help="Unique active users in the last month"
    )

# Returning Users
returning_users, new_users = calculate_returning_users(df_filtered)
with col4:
    st.metric(
        "Returning Users",
        f"{returning_users:,}",
        delta=f"{(returning_users/(returning_users+new_users)*100):.1f}% of total",
        help="Users with more than one session"
    )

# Total Sessions
total_sessions = df_filtered['sessions'].sum()
with col5:
    st.metric(
        "Total Sessions",
        f"{total_sessions:,.0f}",
        help="Total number of sessions"
    )

st.markdown("---")

# Second row of KPIs
col1, col2, col3, col4 = st.columns(4)

# Average Engagement Rate
avg_engagement_rate = df_filtered['engagement_rate'].mean()
with col1:
    st.metric(
        "Avg Engagement Rate",
        f"{avg_engagement_rate:.1%}",
        help="Average percentage of engaged sessions"
    )

# Average Engagement Time
avg_engagement_time = df_filtered['avg_engagement_time'].mean()
with col2:
    st.metric(
        "Avg Engagement Time",
        f"{avg_engagement_time:.1f}s",
        help="Average time users spend engaged with content"
    )

# New Users This Period
new_users_period = df_filtered['user_id'].nunique()
with col3:
    st.metric(
        "Active Users (Period)",
        f"{new_users_period:,}",
        help="Unique users active in selected period"
    )

# Total Page Views
total_page_views = df_filtered['page_views'].sum()
with col4:
    st.metric(
        "Total Page Views",
        f"{total_page_views:,.0f}",
        help="Total pages viewed in selected period"
    )

st.markdown("---")

# Charts Row 1: WAU/MAU Trends
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Weekly Active Users Trend")
    if len(wau) > 0:
        wau['week_str'] = wau['week'].astype(str)
        fig = px.line(
            wau,
            x='week_str',
            y='WAU',
            markers=True,
            line_shape='spline'
        )
        fig.update_traces(line_color='#0066CC', line_width=3, marker=dict(size=8))
        fig.update_layout(
            xaxis_title="Week",
            yaxis_title="Active Users",
            hovermode='x unified',
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for the selected period")

with col2:
    st.subheader("📊 Monthly Active Users Trend")
    if len(mau) > 0:
        mau['month_str'] = mau['month'].astype(str)
        fig = px.line(
            mau,
            x='month_str',
            y='MAU',
            markers=True,
            line_shape='spline'
        )
        fig.update_traces(line_color='#10B981', line_width=3, marker=dict(size=8))
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title="Active Users",
            hovermode='x unified',
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for the selected period")

# Charts Row 2: New vs Returning + Engagement
col1, col2 = st.columns(2)

with col1:
    st.subheader("👥 New vs Returning Users")
    user_type_data = pd.DataFrame({
        'User Type': ['New Users', 'Returning Users'],
        'Count': [new_users, returning_users]
    })
    
    fig = px.pie(
        user_type_data,
        values='Count',
        names='User Type',
        color_discrete_sequence=['#3B82F6', '#10B981'],
        hole=0.4
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("⏱️ Daily Engagement Metrics")
    daily_engagement = df_filtered.groupby('date').agg({
        'engagement_rate': 'mean',
        'avg_engagement_time': 'mean'
    }).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_engagement['date'],
        y=daily_engagement['engagement_rate'] * 100,
        name='Engagement Rate (%)',
        line=dict(color='#0066CC', width=2),
        yaxis='y'
    ))
    fig.add_trace(go.Scatter(
        x=daily_engagement['date'],
        y=daily_engagement['avg_engagement_time'],
        name='Avg Time (s)',
        line=dict(color='#F59E0B', width=2),
        yaxis='y2'
    ))
    
    fig.update_layout(
        yaxis=dict(title='Engagement Rate (%)', side='left'),
        yaxis2=dict(title='Avg Engagement Time (s)', overlaying='y', side='right'),
        hovermode='x unified',
        height=350,
        legend=dict(x=0.5, y=1.1, xanchor='center', orientation='h')
    )
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# SECTION 2: TOP PAGES/SECTIONS
# ============================================================================

st.markdown('<div class="section-header">📄 Top Pages & Sections</div>', unsafe_allow_html=True)

# Simulate page data (since we don't have explicit page data in sheets)
# In production, this would come from GA4 page_view events
top_pages_data = df_filtered[df_filtered['event_name'] == 'page_view'].copy()

if len(top_pages_data) > 0:
    # Group by simulated page paths
    page_stats = top_pages_data.groupby('device_category').agg({
        'page_views': 'sum',
        'user_id': 'nunique',
        'avg_engagement_time': 'mean'
    }).reset_index()
    page_stats.columns = ['Page/Section', 'Total Views', 'Unique Users', 'Avg Engagement Time']
    page_stats = page_stats.sort_values('Total Views', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Top Pages by Views")
        fig = px.bar(
            page_stats.head(10),
            x='Page/Section',
            y='Total Views',
            color='Total Views',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📋 Page Performance Details")
        st.dataframe(
            page_stats.head(10),
            hide_index=True,
            use_container_width=True
        )

# ============================================================================
# SECTION 3: BUSINESS DEMOGRAPHIC SEGMENTATION
# ============================================================================

st.markdown('<div class="section-header">🌍 Business Demographic Segmentation</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("🗺️ Users by Region")
    region_data = df_filtered.groupby('region')['user_id'].nunique().reset_index()
    region_data.columns = ['Region', 'Users']
    region_data = region_data.sort_values('Users', ascending=False)
    
    fig = px.bar(
        region_data,
        x='Users',
        y='Region',
        orientation='h',
        color='Users',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏢 Users by Sales Organization")
    sales_org_data = df_filtered.groupby('sales_org')['user_id'].nunique().reset_index()
    sales_org_data.columns = ['Sales Org', 'Users']
    sales_org_data = sales_org_data.sort_values('Users', ascending=False)
    
    fig = px.bar(
        sales_org_data,
        x='Users',
        y='Sales Org',
        orientation='h',
        color='Users',
        color_continuous_scale='Teal'
    )
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Sessions by Region and Sales Org
st.subheader("📊 Sessions by Region and Sales Organization")
region_sales_sessions = df_filtered.groupby(['region', 'sales_org'])['sessions'].sum().reset_index()
region_sales_sessions = region_sales_sessions.sort_values('sessions', ascending=False)

fig = px.sunburst(
    region_sales_sessions,
    path=['region', 'sales_org'],
    values='sessions',
    color='sessions',
    color_continuous_scale='RdYlBu_r'
)
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# SECTION 4: CUSTOMER ACCOUNT DETAILS
# ============================================================================

if has_account_columns:
    st.markdown('<div class="section-header">👥 Top Active Accounts</div>', unsafe_allow_html=True)

    account_activity = df_filtered.groupby(["account_id", "company_name", "sales_org", "region"]).agg({
        "user_id": "nunique",
        "sessions": "sum",
        "page_views": "sum",
        "avg_engagement_time": "mean",
    }).reset_index()
    account_activity.columns = [
        "Account ID", "Company", "Sales Org", "Region",
        "Active Users", "Total Sessions", "Page Views", "Avg Engagement Time",
    ]
    account_activity = account_activity.sort_values("Total Sessions", ascending=False)

    st.dataframe(
        account_activity.head(20),
        hide_index=True,
        use_container_width=True,
        column_config={
            "Account ID": st.column_config.TextColumn("Account ID", width="small"),
            "Company": st.column_config.TextColumn("Company", width="medium"),
            "Sales Org": st.column_config.TextColumn("Sales Org", width="small"),
            "Region": st.column_config.TextColumn("Region", width="small"),
            "Active Users": st.column_config.NumberColumn("Active Users", format="%d"),
            "Total Sessions": st.column_config.NumberColumn("Sessions", format="%.0f"),
            "Page Views": st.column_config.NumberColumn("Page Views", format="%.0f"),
            "Avg Engagement Time": st.column_config.NumberColumn("Avg Time (s)", format="%.1f"),
        },
    )

# ============================================================================
# SECTION 5: DEVICE & ACCESS PATTERNS
# ============================================================================

st.markdown('<div class="section-header">📱 Device & Access Patterns</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("📱 Sessions by Device")
    device_data = df_filtered.groupby('device_category')['sessions'].sum().reset_index()
    
    fig = px.pie(
        device_data,
        values='sessions',
        names='device_category',
        color_discrete_sequence=px.colors.sequential.Blues_r,
        hole=0.4
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📅 Daily Active Users")
    daily_users = df_filtered.groupby('date')['user_id'].nunique().reset_index()
    daily_users.columns = ['Date', 'Active Users']
    
    fig = px.area(
        daily_users,
        x='Date',
        y='Active Users',
        line_shape='spline'
    )
    fig.update_traces(fillcolor='rgba(0, 102, 204, 0.2)', line_color='#0066CC')
    fig.update_layout(height=350, hovermode='x unified')
    st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**📊 Dashboard Version:** Phase 1 - Baseline Analytics")
with col2:
    st.markdown(f"**📅 Data Range:** {df_filtered['date'].min().strftime('%Y-%m-%d')} to {df_filtered['date'].max().strftime('%Y-%m-%d')}")
with col3:
    st.markdown(f"**🔄 Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Export functionality
st.sidebar.markdown("---")
st.sidebar.markdown("### 📥 Export Data")
if st.sidebar.button("Download Dashboard Data (CSV)"):
    csv = df_filtered.to_csv(index=False)
    st.sidebar.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"veolia_portal_analytics_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
