# AI-Powered Dashboard Generator - Prompt Template

## 🤖 How to Use This Template

**Copy this prompt → Paste in Claude/Cursor → Attach your data → Get instant dashboard**

---

## 📋 MASTER PROMPT TEMPLATE

```
I need you to analyze my data and build a complete Streamlit dashboard.

## DATA SOURCE
[Attach CSV files OR provide Google Sheets link]

Data includes:
- Sheet 1: [Name and description]
  Columns: [list columns]
  
- Sheet 2: [Name and description]  
  Columns: [list columns]

Join logic: [how tables connect]

## BUSINESS CONTEXT
Industry: [e.g., B2B SaaS, eCommerce, Healthcare]
Purpose: [e.g., Customer analytics, Sales tracking, Operations monitoring]
Primary users: [e.g., Executives, Sales team, Operations]

## REQUIRED METRICS (KPIs)

### Top Priority (must have):
1. [KPI name] - [calculation method]
2. [KPI name] - [calculation method]
3. [KPI name] - [calculation method]

### Secondary (nice to have):
1. [KPI name] - [calculation method]
2. [KPI name] - [calculation method]

## VISUALIZATIONS NEEDED

### Row 1 - KPI Cards:
- [Metric 1] | [Metric 2] | [Metric 3] | [Metric 4]

### Row 2 - Trend Charts:
- [Chart type] showing [metric] over time
- [Chart type] showing [breakdown]

### Row 3 - Detailed Analysis:
- [Table/Chart] for [purpose]
- [Table/Chart] for [purpose]

## FILTERS REQUIRED
- [ ] Date range (last 7/30/90 days, all time)
- [ ] [Dimension 1] (multi-select)
- [ ] [Dimension 2] (multi-select)
- [ ] [Dimension 3] (single select)

## DESIGN REQUIREMENTS
Color scheme: 
- Primary: #[hex]
- Secondary: #[hex]
- Accent: #[hex]

Layout preference: [Wide/Centered/Custom]
Logo: [Attach or describe]
Branding: [Company name, style notes]

## TECHNICAL REQUIREMENTS
- Technology: Streamlit + Plotly + Pandas
- Python version: 3.11+
- Deployment target: [Streamlit Cloud / Docker / Local]
- Data refresh: [Real-time / Hourly / Daily / Manual]

## FEATURES NEEDED
- [ ] Export to CSV
- [ ] Export to PDF  
- [ ] Auto-refresh capability
- [ ] Email reports
- [ ] Drill-down interactivity
- [ ] Mobile responsive
- [ ] User authentication
- [ ] Dark mode toggle

## OUTPUT REQUEST

Please provide:
1. ✅ Complete working Streamlit dashboard code
2. ✅ requirements.txt file
3. ✅ Setup instructions
4. ✅ Deployment guide
5. ✅ Data validation checks
6. ✅ Error handling

The code should be:
- Production-ready
- Well-commented
- Modular and maintainable
- Optimized for performance

Generate the complete solution now.
```

---

## 💡 EXAMPLE USAGE

### Example 1: Sales Dashboard

```
I need you to analyze my data and build a complete Streamlit dashboard.

## DATA SOURCE
Google Sheets: https://docs.google.com/spreadsheets/d/ABC123.../edit

Sheet 1: sales_data
Columns: date, sales_rep, product, revenue, quantity, region

Sheet 2: targets
Columns: sales_rep, monthly_target, product_category

Join: sales_rep

## BUSINESS CONTEXT
Industry: B2B Software Sales
Purpose: Track team performance vs targets
Primary users: Sales managers

## REQUIRED METRICS

### Top Priority:
1. Total Revenue MTD - sum(revenue) for current month
2. % to Target - actual_revenue / target * 100
3. Top Performers - top 5 reps by revenue
4. Revenue by Product - breakdown

### Secondary:
1. Average Deal Size - revenue / quantity
2. Conversion Rate - deals_closed / opportunities

## VISUALIZATIONS

Row 1 - KPIs:
Total Revenue | % to Target | Deals Closed | Avg Deal Size

Row 2:
- Line chart: Daily revenue trend
- Bar chart: Revenue by sales rep

Row 3:
- Table: Top products
- Pie chart: Revenue by region

## FILTERS
- [x] Date range
- [x] Sales rep (multi)
- [x] Product category

## DESIGN
Colors: Blue (#1E40AF), Green (#10B981)
Layout: Wide
Logo: Company logo in sidebar

Generate complete dashboard now.
```

---

### Example 2: Operations Dashboard

```
I need you to analyze my data and build a complete Streamlit dashboard.

## DATA SOURCE
CSV files: operations.csv, incidents.csv

operations.csv: timestamp, facility, equipment_id, status, downtime_mins
incidents.csv: incident_id, facility, severity, resolved

Join: facility

## BUSINESS CONTEXT  
Industry: Manufacturing
Purpose: Monitor equipment uptime and incidents
Users: Operations team, Plant managers

## REQUIRED METRICS

### Critical:
1. Overall Equipment Effectiveness (OEE)
2. Downtime by Facility
3. Mean Time to Repair (MTTR)
4. Open Incidents Count

## VISUALIZATIONS

Row 1: OEE | Total Downtime | MTTR | Open Incidents

Row 2:
- Heatmap: Downtime by facility & hour
- Timeline: Incident resolution

## FILTERS
- Date range (last 24hrs/7days/30days)
- Facility (multi)
- Severity (high/medium/low)

## FEATURES
- Real-time auto-refresh (every 5 min)
- Alert when OEE < 85%
- Export incident report

Generate dashboard.
```

---

## 🎯 QUICK WINS - Pre-Built Templates

### Template A: Customer Analytics
```
Build customer analytics dashboard with:
- MAU/WAU/DAU
- Churn rate
- Retention cohorts
- Feature adoption
- Customer lifetime value
```

### Template B: Marketing Performance
```
Build marketing dashboard with:
- Campaign ROI
- Lead conversion funnel
- Cost per acquisition
- Channel performance
- Attribution analysis
```

### Template C: Financial Metrics
```
Build financial dashboard with:
- Revenue vs forecast
- Cash flow
- P&L summary
- Budget variance
- Key financial ratios
```

---

## 🔄 ITERATION PROMPTS

**After initial generation, refine with:**

### Modify Existing Charts
```
Change the [chart name] to show [new metric] instead, 
grouped by [dimension] and colored by [attribute]
```

### Add New Features
```
Add a new section showing [analysis],
with filters for [dimensions] and
export capability to [format]
```

### Fix Issues
```
The [metric] calculation seems incorrect.
It should be [correct logic].
Please fix and regenerate.
```

### Style Changes
```
Update the color scheme to match this Figma:
[attach screenshot]
Make KPI cards larger and add icons.
```

---

## 📚 LEARNING FROM YOUR VEOLIA EXAMPLE

**What worked well:**

✅ **Clear metric definitions** - You specified exact KPIs needed
✅ **Business context** - B2B portal environment was clear
✅ **Data source provided** - Google Sheets link made it easy
✅ **Segmentation needs** - Region, Sales Org clearly stated

**For future dashboards:**

1. **Start with metrics** - List KPIs first, then visualizations
2. **Provide sample data** - Even 10 rows helps tremendously  
3. **Show desired layout** - Figma/sketch of dashboard structure
4. **Specify filters** - What should users be able to slice by?
5. **Define calculations** - How should metrics be computed?

---

## 🚀 ADVANCED PROMPT TECHNIQUES

### Technique 1: Incremental Building
```
Phase 1: Build basic KPIs only
[Claude generates]

Phase 2: Now add trend charts
[Claude adds]

Phase 3: Add segmentation analysis
[Iterative refinement]
```

### Technique 2: Reference Existing
```
Build a dashboard similar to the Veolia one we created,
but for [new use case] with these changes:
[list differences]
```

### Technique 3: Clone & Customize
```
Take the veolia_dashboard.py code and modify it to:
1. Use these different data sources: [...]
2. Calculate these metrics instead: [...]
3. Use this color scheme: [...]
```

---

## 💾 SAVE THIS TEMPLATE

**Create a file: `my_dashboard_prompt.md`**

Every time you need a dashboard:
1. Copy this template
2. Fill in your specifics
3. Paste to Claude/Cursor
4. Get working dashboard in minutes

---

## 🎓 BEST PRACTICES

**DO:**
✅ Be specific about calculations
✅ Provide actual data samples
✅ Show visual examples (Figma, screenshots)
✅ List priorities (must-have vs nice-to-have)
✅ Specify target audience

**DON'T:**
❌ Use vague terms like "make it look good"
❌ Forget to mention join keys between tables
❌ Skip providing sample data
❌ Leave out business context
❌ Request 50+ metrics in first iteration

---

## ⚡ RAPID PROTOTYPING WORKFLOW

**Speed run: Dashboard in 30 minutes**

1. **5 min:** Gather data, export CSVs
2. **10 min:** Fill out prompt template
3. **5 min:** Submit to Claude, review code
4. **5 min:** Install dependencies, run locally
5. **5 min:** Test, refine, iterate

**Total:** Working dashboard in 30 minutes! 🚀

---

**Save this template and you'll never build dashboards from scratch again!**
