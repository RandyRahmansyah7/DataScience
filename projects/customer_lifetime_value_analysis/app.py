import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Customer Analytics Dashboard",
    page_icon="👥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
#MainMenu, footer { visibility: hidden; }

section[data-testid="stSidebar"] {
    background-color: #ffffff;
    border-right: 1px solid #e5e7eb;
}
section[data-testid="stSidebar"] .block-container { padding-top: 1rem; }

.main .block-container {
    background-color: #f3f4f6;
    padding: 1rem 1.5rem 2rem;
    max-width: 100%;
}

.dash-header {
    background: white;
    border-bottom: 1px solid #e5e7eb;
    padding: 0.65rem 1.2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    border-radius: 10px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.dash-header h1 {
    font-size: 1.1rem;
    font-weight: 700;
    color: #111827;
    margin: 0;
}
.badge-live {
    background: #dcfce7;
    color: #15803d;
    font-size: 0.68rem;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    border: 1px solid #bbf7d0;
}
.badge-interactive {
    background: #eef2ff;
    color: #4338ca;
    font-size: 0.68rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
}

.kpi-card {
    border-radius: 12px;
    padding: 1.1rem 1.2rem;
    color: white;
    position: relative;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.10);
    min-height: 136px;
}
.kpi-card-green  { background: linear-gradient(135deg, #10b981, #059669); }
.kpi-card-amber  { background: linear-gradient(135deg, #f59e0b, #d97706); }
.kpi-card-blue   { background: linear-gradient(135deg, #2563eb, #4f46e5); }
.kpi-card-purple { background: linear-gradient(135deg, #7c3aed, #6d28d9); }
.kpi-card-red    { background: linear-gradient(135deg, #ef4444, #dc2626); }

.kpi-label { font-size: 0.65rem; font-weight: 700; opacity: 0.88; text-transform: uppercase; letter-spacing: 0.07em; }
.kpi-value { font-size: 2rem; font-weight: 700; line-height: 1.15; margin: 5px 0 13px; }
.kpi-subgrid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    border-top: 1px solid rgba(255,255,255,0.25);
    padding-top: 9px;
    text-align: center;
    gap: 4px;
}
.kpi-sub-label { font-size: 0.60rem; opacity: 0.78; display: block; margin-bottom: 1px; }
.kpi-sub-value { font-size: 0.73rem; font-weight: 700; display: block; }
.kpi-icon {
    position: absolute;
    right: 14px;
    top: 12px;
    font-size: 2.6rem;
    opacity: 0.11;
}

.sidebar-section-title {
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #6b7280;
    border-bottom: 1px solid #e5e7eb;
    padding-bottom: 4px;
    margin-bottom: 8px;
}

.chart-box {
    background: white;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    padding: 0.85rem 1rem 0.5rem 1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    margin-bottom: 0;
    height: 100%;
}
.chart-box-title {
    font-size: 0.76rem;
    font-weight: 700;
    color: #1f2937;
    margin: 0 0 1px;
}
.chart-box-subtitle {
    font-size: 0.63rem;
    color: #9ca3af;
    margin: 0 0 8px;
}
.chart-box-divider {
    border: none;
    border-top: 1px solid #f1f5f9;
    margin: 0 0 4px;
}
.chart-box-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 4px;
}

.pill-blue   { background:#eef2ff; color:#4338ca; font-size:0.63rem; padding:2px 9px; border-radius:20px; font-weight:600; }
.pill-gray   { background:#f1f5f9; color:#64748b; font-size:0.63rem; padding:3px 9px; border-radius:6px; display:inline-block; }
.pill-amber  { background:#fffbeb; color:#b45309; font-size:0.63rem; padding:3px 9px; border-radius:6px; border:1px solid #fde68a; display:inline-block; }

.section-intro {
    background: linear-gradient(135deg, #ffffff, #f8fafc);
    border: 1px solid #e5e7eb;
    border-left: 4px solid #4f46e5;
    border-radius: 8px;
    padding: 0.7rem 1rem;
    margin-bottom: 1rem;
}
.section-intro .lvl-tag {
    display: inline-block;
    background: #4338ca;
    color: white;
    font-size: 0.60rem;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 5px;
    margin-right: 8px;
    letter-spacing: 0.04em;
}
.section-intro p { font-size: 0.76rem; color: #4b5563; margin: 4px 0 0; line-height: 1.45; }
.section-intro strong { color: #111827; }

.insight-card {
    border-radius: 10px;
    padding: 1rem 1.1rem;
    background: white;
    border: 1px solid #e5e7eb;
    border-left-width: 5px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    height: 100%;
}
.insight-card .ic-title {
    font-size: 0.62rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 7px;
}
.insight-card .ic-headline { font-size: 0.91rem; font-weight: 700; color: #111827; line-height: 1.35; }
.insight-card .ic-sub      { font-size: 0.73rem; color: #6b7280; margin-top: 5px; line-height: 1.4; }

.reco-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.55rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    border-left: 4px solid #4f46e5;
}
.reco-card .reco-head { display:flex; justify-content:space-between; align-items:baseline; flex-wrap:wrap; gap:6px; }
.reco-card .reco-seg  { font-size:0.85rem; font-weight:700; color:#111827; }
.reco-card .reco-meta { font-size:0.63rem; color:#6b7280; }
.reco-card .reco-action    { font-size:0.73rem; font-weight:600; color:#4338ca; margin-top:4px; }
.reco-card .reco-rationale { font-size:0.70rem; color:#6b7280; margin-top:2px; line-height:1.4; }

.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: white;
    padding: 4px;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
}
.stTabs [data-baseweb="tab"] {
    font-size: 0.76rem;
    font-weight: 600;
    color: #6b7280;
    padding: 6px 14px;
    border-radius: 7px;
}
.stTabs [aria-selected="true"] {
    background: #eef2ff !important;
    color: #4338ca !important;
}

div[data-testid="stPlotlyChart"]        { margin: 0 !important; padding: 0 !important; }
div[data-testid="stPlotlyChart"] > div { margin: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def fmt_currency(val):
    if val >= 1_000_000: return f"{val/1_000_000:.2f}M"
    if val >= 1_000:     return f"{val/1_000:.1f}K"
    return str(round(val))

def fmt_num(val):
    return f"{round(val):,}"

def section_intro(level_tag, title, desc):
    st.markdown(f"""
    <div class="section-intro">
      <span class="lvl-tag">{level_tag}</span><strong>{title}</strong>
      <p>{desc}</p>
    </div>
    """, unsafe_allow_html=True)

BASE_LAYOUT = dict(
    font=dict(family="Inter, sans-serif", size=11),
    paper_bgcolor="white",
    plot_bgcolor="white",
)

PLOTLY_CONFIG = {"displayModeBar": False}

RFM_SEGMENTS = ['Champions','Loyal Customers','Potential Loyalists','New Customers',
                'At Risk','Cant Lose Them','Lost Customers']
RFM_COLORS   = ['#4C72B0','#55A868','#64B5F6','#81C784','#F4B400','#E57373','#9CA3AF']
COLOR_MAP    = dict(zip(RFM_SEGMENTS, RFM_COLORS))


# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data():
    raw_path   = "projects/customer_lifetime_value_analysis/data/raw/online_retail_raw.csv"
    clean_path = "projects/customer_lifetime_value_analysis/data/raw/online_retail_clean.csv"
    rfm_path   = "projects/customer_lifetime_value_analysisdata/raw/rfm_segments.csv"

    df_raw = pd.read_csv(raw_path, parse_dates=["InvoiceDate"])

    if os.path.exists(clean_path):
        df = pd.read_csv(clean_path, parse_dates=["InvoiceDate"])
    else:
        np.random.seed(42)
        df = df_raw.copy()
        df = df[df["CustomerID"].notna() & (df["CustomerID"] != 0)]
        df = df[df["UnitPrice"] > 0]
        df = df[df["Quantity"] > 0]
        df["CustomerID"] = df["CustomerID"].astype(int)
        df["Revenue"] = df["Quantity"] * df["UnitPrice"]
        margin = np.random.uniform(0.30, 0.55, size=len(df))
        df["Profit"] = df["Revenue"] * margin

    if "InvoiceMonth" not in df.columns:
        df["InvoiceMonth"] = df["InvoiceDate"].dt.to_period("M").dt.to_timestamp()
    if "DayOfWeek" not in df.columns:
        df["DayOfWeek"] = df["InvoiceDate"].dt.day_name()
    if "Hour" not in df.columns:
        df["Hour"] = df["InvoiceDate"].dt.hour
    if "Revenue" not in df.columns:
        df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    if "Profit" not in df.columns:
        np.random.seed(42)
        df["Profit"] = df["Revenue"] * np.random.uniform(0.30, 0.55, size=len(df))

    if os.path.exists(rfm_path):
        rfm = pd.read_csv(rfm_path)
    else:
        snapshot = df["InvoiceDate"].max() + pd.Timedelta(days=1)
        rfm = df.groupby("CustomerID").agg(
            Recency=("InvoiceDate", lambda x: (snapshot - x.max()).days),
            Frequency=("InvoiceNo", "nunique"),
            Monetary=("Revenue", "sum")
        ).reset_index()
        rfm["R_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5,4,3,2,1]).astype(int)
        rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
        rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
        def seg(row):
            R, F, M = row["R_Score"], row["F_Score"], row["M_Score"]
            if R >= 4 and F >= 4 and M >= 4:      return "Champions"
            elif F >= 4 and R >= 3:                return "Loyal Customers"
            elif R >= 4 and 2 <= F <= 3:           return "Potential Loyalists"
            elif R >= 4 and F == 1:                return "New Customers"
            elif 2 <= R <= 3 and F >= 2:           return "At Risk"
            elif R == 1 and F >= 3:                return "Cant Lose Them"
            elif R <= 2 and F <= 2:                return "Lost Customers"
            else:                                  return "Others"
        rfm["Segment"] = rfm.apply(seg, axis=1)

    return df, rfm

with st.spinner("Loading data…"):
    df, rfm = load_data()


# ─────────────────────────────────────────────
# SIDEBAR — FILTERS
# ─────────────────────────────────────────────
def reset_filters():
    st.session_state.kpi_filter       = "Revenue"
    st.session_state.value_qty_filter = "Value"
    st.session_state.year_filter      = "All"
    st.session_state.month_filter     = "All"
    st.session_state.country_filter   = "All"
    st.session_state.segment_filter   = "All"

with st.sidebar:
    st.markdown('<div class="sidebar-section-title">📊 Metric</div>', unsafe_allow_html=True)
    kpi       = st.radio("Select Metric", ["Revenue", "Profit", "Orders", "Customers"], index=0, key="kpi_filter")
    value_qty = st.radio("Metric Type", ["Value", "Qty"], horizontal=True, index=0, key="value_qty_filter")

    st.divider()
    st.markdown('<div class="sidebar-section-title">📅 Date</div>', unsafe_allow_html=True)
    year_opts  = ["All"] + sorted(df["InvoiceDate"].dt.year.unique().tolist(), reverse=True)
    month_opts = ["All","Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    col_y, col_m = st.columns(2)
    with col_y: year  = st.selectbox("Year",  year_opts,  index=0, key="year_filter")
    with col_m: month = st.selectbox("Month", month_opts, index=0, key="month_filter")

    st.divider()
    st.markdown('<div class="sidebar-section-title">📍 Location</div>', unsafe_allow_html=True)
    country_opts = ["All"] + sorted(df["Country"].dropna().unique().tolist())
    country = st.selectbox("Country", country_opts, index=0, key="country_filter")

    st.divider()
    st.markdown('<div class="sidebar-section-title">👥 Segment</div>', unsafe_allow_html=True)
    seg_opts = ["All"] + RFM_SEGMENTS
    segment  = st.selectbox("Segment Focus", seg_opts, index=0, key="segment_filter")

    st.divider()
    st.button("↺ Reset Filters", type="secondary", use_container_width=True, on_click=reset_filters)

    st.markdown(
        "<div style='text-align:center;font-size:0.58rem;color:#9ca3af;margin-top:8px'>"
        "Customer Analytics v5.0<br><strong style='color:#6b7280'>Live Data · Level 1–7</strong></div>",
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────
# FILTER DATA
# ─────────────────────────────────────────────
dff = df.copy()

if year != "All":
    dff = dff[dff["InvoiceDate"].dt.year == int(year)]
if month != "All":
    month_num = month_opts.index(month)
    dff = dff[dff["InvoiceDate"].dt.month == month_num]
if country != "All":
    dff = dff[dff["Country"] == country]

rfm_filtered = rfm.copy()
if segment != "All":
    seg_customers = rfm[rfm["Segment"] == segment]["CustomerID"]
    dff = dff[dff["CustomerID"].isin(seg_customers)]
    rfm_filtered = rfm[rfm["Segment"] == segment]


# ═══════════════════════════════════════════════════════════
# METRIC CONFIGURATION
# ═══════════════════════════════════════════════════════════
if value_qty == "Qty":
    METRIC_COL      = "Quantity"
    METRIC_LABEL    = "Quantity"
    METRIC_PREFIX   = ""
    METRIC_IS_COUNT = False
elif kpi == "Revenue":
    METRIC_COL      = "Revenue"
    METRIC_LABEL    = "Revenue"
    METRIC_PREFIX   = "£"
    METRIC_IS_COUNT = False
elif kpi == "Profit":
    METRIC_COL      = "Profit"
    METRIC_LABEL    = "Profit"
    METRIC_PREFIX   = "£"
    METRIC_IS_COUNT = False
elif kpi == "Orders":
    METRIC_COL      = "InvoiceNo"
    METRIC_LABEL    = "Orders"
    METRIC_PREFIX   = ""
    METRIC_IS_COUNT = True
else:
    METRIC_COL      = "CustomerID"
    METRIC_LABEL    = "Customers"
    METRIC_PREFIX   = ""
    METRIC_IS_COUNT = True

CLV_COL    = METRIC_COL    if not METRIC_IS_COUNT else "Revenue"
CLV_LABEL  = METRIC_LABEL  if not METRIC_IS_COUNT else "Revenue"
CLV_PREFIX = METRIC_PREFIX if not METRIC_IS_COUNT else "£"

pfx = METRIC_PREFIX


def grouped_metric(data, groupby_col, **kwargs):
    if METRIC_IS_COUNT:
        return data.groupby(groupby_col, **kwargs)[METRIC_COL].nunique()
    else:
        return data.groupby(groupby_col, **kwargs)[METRIC_COL].sum()


def fmt_metric(val):
    if METRIC_PREFIX:
        return f"{METRIC_PREFIX}{val:,.0f}"
    return f"{val:,.0f}"


def fmt_clv(val):
    if CLV_PREFIX:
        return f"{CLV_PREFIX}{val:,.0f}"
    return f"{val:,.0f}"


# ─────────────────────────────────────────────
# COMPUTE KPIs
# ─────────────────────────────────────────────
total_revenue  = dff["Revenue"].sum()
total_profit   = dff["Profit"].sum() if "Profit" in dff.columns else total_revenue * 0.42
profit_margin  = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
total_orders   = dff["InvoiceNo"].nunique()
total_customers= dff["CustomerID"].nunique()

cust_orders = dff.groupby("CustomerID")["InvoiceNo"].nunique()
returning   = int((cust_orders > 1).sum())
one_time    = int((cust_orders == 1).sum())
repeat_rate = returning / total_customers * 100 if total_customers > 0 else 0

aov = (dff.groupby("InvoiceNo")["Revenue"].sum().mean()) if total_orders > 0 else 0

snapshot_date = df["InvoiceDate"].max()
last_purch    = dff.groupby("CustomerID")["InvoiceDate"].max()
churned       = (((snapshot_date - last_purch).dt.days) > 90).sum()
churn_rate    = churned / total_customers * 100 if total_customers > 0 else 0
retention_rate= 100 - churn_rate

clv_per_cust  = dff.groupby("CustomerID")["Revenue"].sum()
avg_clv       = clv_per_cust.mean() if len(clv_per_cust) > 0 else 0

if value_qty == "Qty":
    main_kpi_val = dff["Quantity"].sum()
elif kpi == "Revenue":
    main_kpi_val = total_revenue
elif kpi == "Profit":
    main_kpi_val = total_profit
elif kpi == "Orders":
    main_kpi_val = total_orders
else:
    main_kpi_val = total_customers

KPI_CARD_LABEL = "Total Quantity" if value_qty == "Qty" else f"Total {kpi}"


# ─────────────────────────────────────────────
# DASHBOARD HEADER
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="dash-header">
  <div style="display:flex;align-items:center;gap:10px">
    <span style="font-size:1.25rem">👥</span>
    <h1>Customer Analytics Dashboard</h1>
    <span class="badge-live">● Live Data</span>
  </div>
  <div style="display:flex;align-items:center;gap:12px;font-size:0.73rem">
    <span class="badge-interactive">Interactive</span>
    <span style="color:#d1d5db">|</span>
    <span style="color:#6b7280">Metric: <strong style="color:#111827">{METRIC_LABEL}</strong></span>
    <span style="color:#d1d5db">|</span>
    <span style="color:#6b7280">Type: <strong style="color:#111827">{value_qty}</strong></span>
    <span style="color:#d1d5db">|</span>
    <span style="color:#6b7280">Country: <strong style="color:#111827">{country}</strong></span>
    <span style="color:#d1d5db">|</span>
    <span style="color:#6b7280">Segment: <strong style="color:#111827">{segment}</strong></span>
  </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Executive Overview",
    "🔄 Retention & Cohort",
    "💎 CLV & Value Concentration",
    "🎯 RFM Segmentation",
    "🕒 Customer Behavior",
    "💡 Business Recommendations",
])


# ═══════════════════════════════════════════════════════════
# TAB 1 — EXECUTIVE OVERVIEW
# ═══════════════════════════════════════════════════════════
with tab1:
    section_intro("LEVEL 1–2", "Executive Snapshot & Acquisition Engine",
        "Ringkasan KPI utama bisnis beserta mesin akuisisi pelanggan dari bulan ke bulan — "
        "apakah pertumbuhan benar-benar solid atau hanya <strong>sugar high</strong> di awal periode.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="kpi-card kpi-card-green">
          <div class="kpi-icon">💰</div>
          <div class="kpi-label">{KPI_CARD_LABEL}</div>
          <div class="kpi-value">{pfx}{fmt_currency(main_kpi_val)}</div>
          <div class="kpi-subgrid">
            <div><span class="kpi-sub-label">Profit</span><span class="kpi-sub-value">£{fmt_currency(total_profit)}</span></div>
            <div><span class="kpi-sub-label">Margin</span><span class="kpi-sub-value">{profit_margin:.1f}%</span></div>
            <div><span class="kpi-sub-label">AOV</span><span class="kpi-sub-value">£{fmt_currency(aov)}</span></div>
          </div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-card kpi-card-amber">
          <div class="kpi-icon">👥</div>
          <div class="kpi-label">Total Customers</div>
          <div class="kpi-value">{fmt_num(total_customers)}</div>
          <div class="kpi-subgrid">
            <div><span class="kpi-sub-label">Returning</span><span class="kpi-sub-value">{fmt_num(returning)}</span></div>
            <div><span class="kpi-sub-label">One-time</span><span class="kpi-sub-value">{fmt_num(one_time)}</span></div>
            <div><span class="kpi-sub-label">Repeat Rate</span><span class="kpi-sub-value">{repeat_rate:.1f}%</span></div>
          </div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="kpi-card kpi-card-blue">
          <div class="kpi-icon">💎</div>
          <div class="kpi-label">Avg Lifetime Value</div>
          <div class="kpi-value">£{fmt_currency(avg_clv)}</div>
          <div class="kpi-subgrid">
            <div><span class="kpi-sub-label">Orders</span><span class="kpi-sub-value">{fmt_num(total_orders)}</span></div>
            <div><span class="kpi-sub-label">Retention</span><span class="kpi-sub-value">{retention_rate:.1f}%</span></div>
            <div><span class="kpi-sub-label">Churn</span><span class="kpi-sub-value" style="color:#fca5a5">{churn_rate:.1f}%</span></div>
          </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    r2c1, r2c2, r2c3 = st.columns([4, 4, 4])

    with r2c1:
        st.markdown(f"""
        <div class="chart-box">
          <div class="chart-box-title">{METRIC_LABEL} by Country</div>
          <div class="chart-box-subtitle">Top 10 markets by total {METRIC_LABEL.lower()}</div>
          <hr class="chart-box-divider">
        </div>""", unsafe_allow_html=True)
        metric_by_country = grouped_metric(dff, "Country").sort_values(ascending=True).tail(10)
        fig_country = go.Figure(go.Bar(
            x=metric_by_country.values,
            y=metric_by_country.index,
            orientation="h",
            marker=dict(
                color=metric_by_country.values,
                colorscale=[[0,"#bfdbfe"],[1,"#1d4ed8"]],
                showscale=False,
            ),
            text=[fmt_metric(v) for v in metric_by_country.values],
            textposition="outside",
            textfont_size=9,
        ))
        fig_country.update_layout(
            **BASE_LAYOUT, height=285,
            xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            yaxis=dict(tickfont_size=9, showgrid=False),
            margin=dict(l=5, r=65, t=5, b=10),
        )
        st.plotly_chart(fig_country, use_container_width=True, config=PLOTLY_CONFIG)

    with r2c2:
        st.markdown("""
        <div class="chart-box">
          <div class="chart-box-title">Customer Composition</div>
          <div class="chart-box-subtitle">Returning vs One-time buyers</div>
          <hr class="chart-box-divider">
        </div>""", unsafe_allow_html=True)
        fig_comp = go.Figure(go.Pie(
            labels=["Returning (>1 order)", "One-time Buyer"],
            values=[max(returning, 1), max(one_time, 1)],
            hole=0.55,
            marker=dict(colors=["#4C72B0","#DD8452"], line=dict(color="white", width=2)),
            textinfo="percent",
            textfont_size=11,
            pull=[0.03, 0],
        ))
        fig_comp.update_layout(
            **BASE_LAYOUT, height=285,
            legend=dict(orientation="h", y=-0.1, font_size=10),
            margin=dict(l=5, r=5, t=10, b=35),
        )
        st.plotly_chart(fig_comp, use_container_width=True, config=PLOTLY_CONFIG)

    with r2c3:
        st.markdown("""
        <div class="chart-box">
          <div class="chart-box-title">Retention vs Churn</div>
          <div class="chart-box-subtitle">Based on 90-day inactivity proxy</div>
          <hr class="chart-box-divider">
        </div>""", unsafe_allow_html=True)
        fig_ret = go.Figure(go.Pie(
            labels=["Retention Rate", "Churn Rate"],
            values=[max(round(retention_rate, 2), 0.01), max(round(churn_rate, 2), 0.01)],
            marker=dict(colors=["#55A868","#C44E52"], line=dict(color="white", width=2)),
            textinfo="percent+label",
            textfont_size=10,
            pull=[0.03, 0],
        ))
        fig_ret.update_layout(
            **BASE_LAYOUT, height=285,
            legend=dict(orientation="h", y=-0.1, font_size=10),
            margin=dict(l=5, r=5, t=10, b=35),
        )
        st.plotly_chart(fig_ret, use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    r3c1, r3c2 = st.columns([5, 7])

    with r3c1:
        first_purchase_df = dff.groupby("CustomerID")["InvoiceDate"].min().reset_index()
        first_purchase_df["FirstMonth"] = first_purchase_df["InvoiceDate"].dt.to_period("M").dt.to_timestamp()
        new_per_month = first_purchase_df.groupby("FirstMonth")["CustomerID"].nunique().reset_index(name="NewCustomers")

        st.markdown("""
        <div class="chart-box">
          <div class="chart-box-title">New Customers per Month</div>
          <div class="chart-box-subtitle">Monthly acquisition cohort size</div>
          <hr class="chart-box-divider">
        </div>""", unsafe_allow_html=True)
        fig_acq = go.Figure(go.Bar(
            x=new_per_month["FirstMonth"].dt.strftime("%b '%y"),
            y=new_per_month["NewCustomers"],
            marker=dict(color="#4C72B0", line=dict(width=0)),
        ))
        fig_acq.update_layout(
            **BASE_LAYOUT, height=265,
            xaxis=dict(tickfont_size=8, showgrid=False, tickangle=-45),
            yaxis=dict(tickfont_size=9, gridcolor="#f1f5f9", title="New Customers"),
            bargap=0.3,
            margin=dict(l=45, r=10, t=5, b=60),
        )
        st.plotly_chart(fig_acq, use_container_width=True, config=PLOTLY_CONFIG)

    with r3c2:
        metric_by_month = grouped_metric(
            dff, dff["InvoiceDate"].dt.to_period("M").dt.to_timestamp()
        ).reset_index()
        metric_by_month.columns = ["Month", METRIC_LABEL]
        metric_by_month["GrowthPct"] = metric_by_month[METRIC_LABEL].pct_change() * 100

        st.markdown(f"""
        <div class="chart-box">
          <div class="chart-box-title">{METRIC_LABEL} & MoM Growth Trend</div>
          <div class="chart-box-subtitle">Monthly {METRIC_LABEL.lower()} with % Month-over-Month growth overlay</div>
          <hr class="chart-box-divider">
        </div>""", unsafe_allow_html=True)
        fig_rev = go.Figure()
        fig_rev.add_trace(go.Bar(
            x=metric_by_month["Month"].dt.strftime("%b '%y"),
            y=metric_by_month[METRIC_LABEL],
            name=METRIC_LABEL,
            marker_color="#93c5fd",
            yaxis="y1",
        ))
        fig_rev.add_trace(go.Scatter(
            x=metric_by_month["Month"].dt.strftime("%b '%y"),
            y=metric_by_month["GrowthPct"],
            name="MoM Growth %",
            mode="lines+markers",
            line=dict(color="#C44E52", width=2.5),
            marker=dict(size=5, color="white", line=dict(color="#C44E52", width=2)),
            yaxis="y2",
        ))
        fig_rev.add_hline(y=0, line_dash="dash", line_color="#d1d5db", line_width=1, yref="y2")
        fig_rev.update_layout(
            **BASE_LAYOUT, height=265,
            xaxis=dict(tickfont_size=8, showgrid=False, tickangle=-45),
            yaxis=dict(tickfont_size=9, gridcolor="#f1f5f9",
                       tickprefix=METRIC_PREFIX if METRIC_PREFIX else "",
                       tickformat=",", title=METRIC_LABEL),
            yaxis2=dict(tickfont_size=9, ticksuffix="%", overlaying="y", side="right",
                        showgrid=False, title="Growth %"),
            legend=dict(orientation="h", y=1.08, font_size=9),
            bargap=0.3,
            margin=dict(l=55, r=55, t=30, b=60),
        )
        st.plotly_chart(fig_rev, use_container_width=True, config=PLOTLY_CONFIG)


# ═══════════════════════════════════════════════════════════
# TAB 2 — RETENTION & COHORT
# ═══════════════════════════════════════════════════════════
with tab2:
    section_intro("LEVEL 3", "Customer Retention Analysis",
        "Cohort Retention Heatmap menunjukkan kapan pelanggan mulai berhenti membeli, dan "
        "Purchase Frequency Distribution menunjukkan betapa timpangnya frekuensi order antar pelanggan.")

    @st.cache_data(show_spinner=False)
    def build_cohort_table(_dff):
        fp = _dff.groupby("CustomerID")["InvoiceDate"].min().reset_index()
        fp.columns = ["CustomerID", "CohortDate"]
        fp["CohortMonth"] = fp["CohortDate"].dt.to_period("M")
        merged = _dff.merge(fp[["CustomerID","CohortMonth"]], on="CustomerID")
        merged["InvoiceMonth"] = merged["InvoiceDate"].dt.to_period("M")
        merged["CohortIndex"] = (
            (merged["InvoiceMonth"].dt.year - merged["CohortMonth"].dt.year) * 12 +
            (merged["InvoiceMonth"].dt.month - merged["CohortMonth"].dt.month)
        )
        cohort_data = merged.groupby(["CohortMonth","CohortIndex"])["CustomerID"].nunique().reset_index()
        cohort_pivot = cohort_data.pivot(index="CohortMonth", columns="CohortIndex", values="CustomerID")
        cohort_size  = cohort_pivot[0]
        retention    = cohort_pivot.divide(cohort_size, axis=0) * 100
        retention.index = retention.index.astype(str)
        return retention, cohort_size

    retention_table, cohort_size = build_cohort_table(dff)

    cols_to_show = [c for c in retention_table.columns if c <= 11]
    rt_display = retention_table[cols_to_show].copy()

    st.markdown("""
    <div class="chart-box">
      <div class="chart-box-title">Customer Retention Cohort Heatmap</div>
      <div class="chart-box-subtitle">Retention rate (%) over time for each monthly cohort — the "Layer Cake" view</div>
      <hr class="chart-box-divider">
    </div>""", unsafe_allow_html=True)

    z_vals = rt_display.values
    text_vals = [[f"{v:.0f}%" if not np.isnan(v) else "" for v in row] for row in z_vals]

    fig_heat = go.Figure(go.Heatmap(
        z=z_vals,
        x=[f"M+{c}" for c in cols_to_show],
        y=rt_display.index.tolist(),
        text=text_vals,
        texttemplate="%{text}",
        textfont=dict(size=9),
        colorscale=[[0,"#f8fafc"],[0.15,"#dbeafe"],[0.35,"#93c5fd"],[0.65,"#3b82f6"],[1.0,"#1d4ed8"]],
        zmin=0, zmax=60,
        showscale=True,
        hoverongaps=False,
        colorbar=dict(title="Retention %", tickfont_size=9, thickness=12, len=0.85),
    ))
    fig_heat.update_layout(
        **BASE_LAYOUT, height=400,
        xaxis=dict(title="Months Since First Purchase", tickfont_size=10, showgrid=False),
        yaxis=dict(title="Cohort Month", tickfont_size=9, showgrid=False, autorange="reversed"),
        margin=dict(l=80, r=70, t=10, b=50),
    )
    st.plotly_chart(fig_heat, use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    r2c1, r2c2 = st.columns([6, 6])

    with r2c1:
        avg_ret = rt_display.mean(axis=0)
        st.markdown("""
        <div class="chart-box">
          <div class="chart-box-title">Average Retention Curve</div>
          <div class="chart-box-subtitle">The "cliff" at M+1 and the stable "floor" that forms after</div>
          <hr class="chart-box-divider">
        </div>""", unsafe_allow_html=True)
        fig_curve = go.Figure(go.Scatter(
            x=[f"M+{c}" for c in avg_ret.index],
            y=avg_ret.values,
            mode="lines+markers+text",
            text=[f"{v:.0f}%" for v in avg_ret.values],
            textposition="top center",
            textfont_size=8,
            line=dict(color="#4C72B0", width=2.5),
            marker=dict(size=7, color="#4C72B0"),
            fill="tozeroy",
            fillcolor="rgba(76,114,176,0.1)",
        ))
        fig_curve.update_layout(
            **BASE_LAYOUT, height=290,
            xaxis=dict(tickfont_size=9, showgrid=False),
            yaxis=dict(tickfont_size=9, gridcolor="#f1f5f9", ticksuffix="%", range=[0, 115]),
            margin=dict(l=40, r=10, t=15, b=40),
        )
        st.plotly_chart(fig_curve, use_container_width=True, config=PLOTLY_CONFIG)

    with r2c2:
        cust_freq = dff.groupby("CustomerID")["InvoiceNo"].nunique()
        freq_clip = cust_freq.clip(upper=20)
        pct_one   = (cust_freq == 1).mean() * 100
        avg_freq  = cust_freq.mean()

        st.markdown("""
        <div class="chart-box">
          <div class="chart-box-title">Purchase Frequency Distribution</div>
          <div class="chart-box-subtitle">Orders per customer — clipped at 20+ orders</div>
          <hr class="chart-box-divider">
        </div>""", unsafe_allow_html=True)

        freq_counts = freq_clip.value_counts().sort_index()
        fig_freq = go.Figure(go.Bar(
            x=[str(int(b)) if b < 20 else "20+" for b in freq_counts.index],
            y=freq_counts.values,
            marker=dict(color="#4C72B0", line=dict(width=0)),
        ))
        fig_freq.add_vline(
            x=min(avg_freq - 1, 18),
            line_dash="dash", line_color="#C44E52",
            annotation_text=f"Avg: {avg_freq:.1f}",
            annotation_font_size=9,
            annotation_bgcolor="#C44E52",
            annotation_font_color="white",
        )
        fig_freq.update_layout(
            **BASE_LAYOUT, height=250,
            xaxis=dict(title="Number of Orders", tickfont_size=9, showgrid=False),
            yaxis=dict(title="Customers", tickfont_size=9, gridcolor="#f1f5f9"),
            bargap=0.15,
            margin=dict(l=45, r=10, t=10, b=40),
        )
        st.plotly_chart(fig_freq, use_container_width=True, config=PLOTLY_CONFIG)

        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:4px">
          <div style="background:#fef2f2;border-radius:8px;padding:8px;text-align:center">
            <div style="font-size:1.3rem;font-weight:700;color:#C44E52">{pct_one:.0f}%</div>
            <div style="font-size:0.65rem;color:#6b7280">only 1 order</div>
          </div>
          <div style="background:#eff6ff;border-radius:8px;padding:8px;text-align:center">
            <div style="font-size:1.3rem;font-weight:700;color:#4C72B0">{avg_freq:.1f}x</div>
            <div style="font-size:0.65rem;color:#6b7280">avg orders</div>
          </div>
          <div style="background:#f0fdf4;border-radius:8px;padding:8px;text-align:center">
            <div style="font-size:1.3rem;font-weight:700;color:#55A868">{retention_rate:.0f}%</div>
            <div style="font-size:0.65rem;color:#6b7280">retention</div>
          </div>
        </div>""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
# TAB 3 — CLV & VALUE CONCENTRATION
# ═══════════════════════════════════════════════════════════
with tab3:
    section_intro("LEVEL 4", "Customer Lifetime Value (CLV)",
        "Mengukur seberapa terkonsentrasi nilai pelanggan: siapa 20 pelanggan teratas, "
        "bagaimana distribusi nilai, dan seberapa kuat prinsip Pareto 80/20 berlaku.")

    clv_df = dff.groupby("CustomerID").agg(
        Revenue=(CLV_COL, "sum"),
        Profit=("Profit", "sum") if "Profit" in dff.columns else ("Revenue", "sum"),
        NumOrders=("InvoiceNo", "nunique"),
        Country=("Country", "first"),
    ).reset_index().sort_values("Revenue", ascending=False)

    clv_sorted = clv_df.sort_values("Revenue", ascending=False).reset_index(drop=True)
    clv_sorted["CumRev"]    = clv_sorted["Revenue"].cumsum()
    clv_sorted["CumRevPct"] = clv_sorted["CumRev"] / clv_sorted["Revenue"].sum() * 100
    clv_sorted["CustPct"]   = (clv_sorted.index + 1) / len(clv_sorted) * 100
    top20_pct = clv_sorted[clv_sorted["CustPct"] <= 20]["Revenue"].sum() / clv_sorted["Revenue"].sum() * 100

    r1c1, r1c2 = st.columns([4, 8])

    with r1c1:
        st.markdown(f"""
        <div class="chart-box">
          <div class="chart-box-title">Value Concentration</div>
          <div class="chart-box-subtitle">Top 20% vs Bottom 80% of Customers</div>
          <hr class="chart-box-divider">
        </div>""", unsafe_allow_html=True)
        fig_split = go.Figure(go.Pie(
            labels=["Top 20% Customers","Bottom 80% Customers"],
            values=[round(top20_pct, 1), round(100 - top20_pct, 1)],
            hole=0.58,
            marker=dict(colors=["#4C72B0","#e2e8f0"], line=dict(color="white", width=2)),
            textinfo="percent",
            textfont_size=11,
            pull=[0.04, 0],
        ))
        fig_split.add_annotation(
            text=f"<b>{top20_pct:.0f}%</b><br><span style='font-size:10'>of {CLV_LABEL.lower()}</span>",
            x=0.5, y=0.5, showarrow=False, font_size=14,
        )
        fig_split.update_layout(
            **BASE_LAYOUT, height=250,
            legend=dict(orientation="h", y=-0.1, font_size=9),
            margin=dict(l=5, r=5, t=5, b=45),
        )
        st.plotly_chart(fig_split, use_container_width=True, config=PLOTLY_CONFIG)
        st.markdown("<p style='text-align:center;font-size:0.63rem;color:#9ca3af;margin-top:-4px'>Pareto Principle verified on live data</p>", unsafe_allow_html=True)

    with r1c2:
        st.markdown(f"""
        <div class="chart-box">
          <div class="chart-box-title">Cumulative CLV Pareto Curve</div>
          <div class="chart-box-subtitle">% Total {CLV_LABEL} generated by % of Customers ranked by {CLV_LABEL.lower()}</div>
          <hr class="chart-box-divider">
        </div>""", unsafe_allow_html=True)
        sample = clv_sorted.iloc[::max(len(clv_sorted)//200, 1)]
        fig_par = go.Figure()
        fig_par.add_trace(go.Scatter(
            x=sample["CustPct"], y=sample["CumRevPct"],
            mode="lines", fill="tozeroy",
            line=dict(color="#4C72B0", width=2.5),
            fillcolor="rgba(76,114,176,0.12)",
            name=f"Cumulative {CLV_LABEL} %",
        ))
        fig_par.add_trace(go.Scatter(
            x=[0, 100], y=[0, 100],
            mode="lines",
            line=dict(color="#d1d5db", width=1.5, dash="dot"),
            name="Perfect Equality",
        ))
        fig_par.add_shape(type="line", x0=20, x1=20, y0=0, y1=top20_pct,
                          line=dict(color="#C44E52", width=1.5, dash="dash"))
        fig_par.add_shape(type="line", x0=0, x1=20, y0=top20_pct, y1=top20_pct,
                          line=dict(color="#C44E52", width=1.5, dash="dash"))
        fig_par.add_annotation(x=20, y=top20_pct, text=f" Top 20% → {top20_pct:.0f}% {CLV_LABEL.lower()}",
                               showarrow=False, font=dict(size=9, color="#C44E52"), xanchor="left")
        fig_par.update_layout(
            **BASE_LAYOUT, height=250,
            xaxis=dict(title="% of Customer Base", tickfont_size=9, showgrid=False, ticksuffix="%"),
            yaxis=dict(title=f"Cumulative {CLV_LABEL} %", tickfont_size=9, gridcolor="#f1f5f9",
                       ticksuffix="%", range=[0, 105]),
            legend=dict(orientation="h", y=1.1, font_size=9),
            margin=dict(l=55, r=15, t=30, b=50),
        )
        st.plotly_chart(fig_par, use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    r2c1, r2c2 = st.columns([5, 7])

    with r2c1:
        top20_cust = clv_df.head(20).sort_values("Revenue")
        top20_rev_pct = top20_cust["Revenue"].sum() / clv_df["Revenue"].sum() * 100
        st.markdown(f"""
        <div class="chart-box">
          <div class="chart-box-header">
            <div>
              <div class="chart-box-title">Top 20 Customers by {CLV_LABEL}</div>
              <div class="chart-box-subtitle">Lifetime {CLV_LABEL.lower()} contribution per customer</div>
            </div>
            <span class="pill-gray">≈ {top20_rev_pct:.1f}% of {CLV_LABEL.lower()}</span>
          </div>
          <hr class="chart-box-divider">
        </div>""", unsafe_allow_html=True)
        fig_top20 = go.Figure(go.Bar(
            x=top20_cust["Revenue"],
            y=top20_cust["CustomerID"].astype(str),
            orientation="h",
            marker=dict(
                color=top20_cust["Revenue"].values,
                colorscale=[[0,"#93c5fd"],[1,"#1d4ed8"]],
                showscale=False,
            ),
            text=[fmt_clv(v) for v in top20_cust["Revenue"]],
            textposition="outside",
            textfont_size=8,
        ))
        fig_top20.update_layout(
            **BASE_LAYOUT, height=420,
            xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            yaxis=dict(tickfont_size=8, showgrid=False, title="Customer ID"),
            margin=dict(l=60, r=70, t=5, b=20),
        )
        st.plotly_chart(fig_top20, use_container_width=True, config=PLOTLY_CONFIG)

    with r2c2:
        rev_clipped = clv_df["Revenue"].clip(upper=clv_df["Revenue"].quantile(0.95))
        st.markdown(f"""
        <div class="chart-box">
          <div class="chart-box-title">CLV Distribution</div>
          <div class="chart-box-subtitle">{CLV_LABEL} per customer — clipped at 95th percentile (right-skewed)</div>
          <hr class="chart-box-divider">
        </div>""", unsafe_allow_html=True)
        fig_clvd = go.Figure(go.Histogram(
            x=rev_clipped, nbinsx=40,
            marker=dict(color="#8172B2", line=dict(color="white", width=0.5)),
        ))
        fig_clvd.add_vline(x=float(clv_df["Revenue"].mean()), line_dash="dash", line_color="#C44E52",
                           annotation_text=f"Mean: {fmt_clv(clv_df['Revenue'].mean())}",
                           annotation_font_size=9, annotation_bgcolor="#C44E52",
                           annotation_font_color="white")
        fig_clvd.add_vline(x=float(clv_df["Revenue"].median()), line_dash="dash", line_color="#55A868",
                           annotation_text=f"Median: {fmt_clv(clv_df['Revenue'].median())}",
                           annotation_font_size=9, annotation_bgcolor="#55A868",
                           annotation_font_color="white")
        fig_clvd.update_layout(
            **BASE_LAYOUT, height=420,
            xaxis=dict(title=f"{CLV_LABEL} per Customer ({CLV_PREFIX if CLV_PREFIX else ''})", tickfont_size=9, gridcolor="#f1f5f9"),
            yaxis=dict(title="Number of Customers", tickfont_size=9, gridcolor="#f1f5f9"),
            margin=dict(l=55, r=15, t=10, b=50),
            bargap=0.04,
        )
        st.plotly_chart(fig_clvd, use_container_width=True, config=PLOTLY_CONFIG)


# ═══════════════════════════════════════════════════════════
# TAB 4 — RFM SEGMENTATION
# ═══════════════════════════════════════════════════════════
with tab4:
    section_intro("LEVEL 5", "RFM Segmentation",
        "Mengelompokkan pelanggan berdasarkan <strong>Recency</strong>, <strong>Frequency</strong>, "
        "dan <strong>Monetary</strong> ke dalam segmen yang actionable.")

    rfm_disp = rfm[rfm["CustomerID"].isin(dff["CustomerID"])].copy()
    rfm_disp = rfm_disp[rfm_disp["Segment"].isin(RFM_SEGMENTS)]

    cust_clv = dff.groupby("CustomerID")[CLV_COL].sum()
    rfm_disp["CLV"] = rfm_disp["CustomerID"].map(cust_clv)

    seg_summary = (
        rfm_disp.groupby("Segment")
        .agg(Customers=("CustomerID","count"), Revenue=("CLV","sum"))
        .reset_index()
    )
    seg_summary["CustPct"] = seg_summary["Customers"] / seg_summary["Customers"].sum() * 100
    seg_summary["RevPct"]  = seg_summary["Revenue"]   / seg_summary["Revenue"].sum()   * 100
    seg_summary = seg_summary.sort_values("Revenue", ascending=False)

    r1c1, r1c2 = st.columns([7, 5])

    with r1c1:
        st.markdown("""
        <div class="chart-box">
          <div class="chart-box-title">RFM Customer Segments — Treemap</div>
          <div class="chart-box-subtitle">Size = number of customers in each segment</div>
          <hr class="chart-box-divider">
        </div>""", unsafe_allow_html=True)
        fig_tree = go.Figure(go.Treemap(
            labels=seg_summary["Segment"],
            parents=[""] * len(seg_summary),
            values=seg_summary["Customers"],
            marker=dict(colors=[COLOR_MAP.get(s, "#aaa") for s in seg_summary["Segment"]]),
            textinfo="label+value+percent root",
            textfont_size=11,
            hovertemplate="<b>%{label}</b><br>%{value:,} customers<br>%{percentRoot:.1%} of total<extra></extra>",
        ))
        fig_tree.update_layout(**BASE_LAYOUT, height=310, margin=dict(l=5,r=5,t=5,b=5))
        st.plotly_chart(fig_tree, use_container_width=True, config=PLOTLY_CONFIG)

    with r1c2:
        st.markdown(f"""
        <div class="chart-box">
          <div class="chart-box-title">Segment {CLV_LABEL} Contribution</div>
          <div class="chart-box-subtitle">Average {CLV_LABEL.lower()} per segment</div>
          <hr class="chart-box-divider">
        </div>""", unsafe_allow_html=True)
        seg_avg = rfm_disp.groupby("Segment")["CLV"].mean().reindex(
            seg_summary["Segment"].tolist()
        ).dropna()
        fig_seg_val = go.Figure(go.Bar(
            x=seg_avg.values,
            y=seg_avg.index,
            orientation="h",
            marker=dict(color=[COLOR_MAP.get(s, "#aaa") for s in seg_avg.index]),
            text=[fmt_clv(v) for v in seg_avg.values],
            textposition="outside",
            textfont_size=9,
        ))
        fig_seg_val.update_layout(
            **BASE_LAYOUT, height=310,
            xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            yaxis=dict(tickfont_size=9, showgrid=False),
            margin=dict(l=120, r=70, t=5, b=10),
        )
        st.plotly_chart(fig_seg_val, use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if "R_Score" in rfm_disp.columns and "F_Score" in rfm_disp.columns:
        rf_pivot = rfm_disp.pivot_table(
            index="F_Score", columns="R_Score",
            values="CustomerID", aggfunc="count", fill_value=0
        ).sort_index(ascending=False)

        st.markdown("""
        <div class="chart-box">
          <div class="chart-box-title">RFM Heatmap: Frequency Score vs Recency Score</div>
          <div class="chart-box-subtitle">Customer count per F/R score combination — top-right corner = Champions candidates</div>
          <hr class="chart-box-divider">
        </div>""", unsafe_allow_html=True)
        fig_rfheat = go.Figure(go.Heatmap(
            z=rf_pivot.values,
            x=[str(c) for c in rf_pivot.columns],
            y=[str(i) for i in rf_pivot.index],
            text=rf_pivot.values.astype(str),
            texttemplate="%{text}",
            textfont_size=11,
            colorscale="YlOrRd",
            showscale=True,
            colorbar=dict(title="Customers", tickfont_size=9, thickness=12),
        ))
        fig_rfheat.update_layout(
            **BASE_LAYOUT, height=340,
            xaxis=dict(title="Recency Score  (5 = bought recently)", tickfont_size=10, showgrid=False),
            yaxis=dict(title="Frequency Score  (5 = most frequent)", tickfont_size=10, showgrid=False),
            margin=dict(l=65, r=70, t=10, b=50),
        )
        st.plotly_chart(fig_rfheat, use_container_width=True, config=PLOTLY_CONFIG)


# ═══════════════════════════════════════════════════════════
# TAB 5 — CUSTOMER BEHAVIOR
# ═══════════════════════════════════════════════════════════
with tab5:
    section_intro("LEVEL 6", "Customer Behavior Analysis",
        "Memahami ritme belanja pelanggan: jarak antar order, ukuran keranjang, "
        "nilai per order, dan kapan pelanggan paling aktif berbelanja.")

    @st.cache_data(show_spinner=False)
    def build_behavior(_dff, metric_col):
        od = _dff.groupby(["CustomerID","InvoiceNo"])["InvoiceDate"].first().reset_index()
        od = od.sort_values(["CustomerID","InvoiceDate"])
        od["PrevDate"] = od.groupby("CustomerID")["InvoiceDate"].shift(1)
        od["DaysSincePrev"] = (od["InvoiceDate"] - od["PrevDate"]).dt.days
        intervals = od["DaysSincePrev"].dropna()

        basket = _dff.groupby("InvoiceNo").agg(
            NumLineItems=("StockCode","nunique"),
            Revenue=("Revenue","sum"),
            Metric=(metric_col, "sum"),
        ).reset_index()

        return intervals, basket

    intervals, basket = build_behavior(dff, CLV_COL)

    r1c1, r1c2 = st.columns(2)

    with r1c1:
        st.markdown("""
        <div class="chart-box">
          <div class="chart-box-title">Order Interval Distribution</div>
          <div class="chart-box-subtitle">Days between consecutive orders — clipped at 120 days</div>
          <hr class="chart-box-divider">
        </div>""", unsafe_allow_html=True)
        iv_clip = intervals.clip(upper=120)
        fig_iv = go.Figure(go.Histogram(
            x=iv_clip, nbinsx=40,
            marker=dict(color="#4C72B0", line=dict(color="white", width=0.5)),
        ))
        med_iv = float(iv_clip.median())
        fig_iv.add_vline(x=med_iv, line_dash="dash", line_color="#C44E52",
                         annotation_text=f"Median: {med_iv:.0f}d",
                         annotation_font_size=9, annotation_bgcolor="#C44E52",
                         annotation_font_color="white")
        fig_iv.update_layout(
            **BASE_LAYOUT, height=280,
            xaxis=dict(title="Days Between Orders", tickfont_size=9, gridcolor="#f1f5f9"),
            yaxis=dict(title="Number of Orders", tickfont_size=9, gridcolor="#f1f5f9"),
            margin=dict(l=50, r=15, t=10, b=45), bargap=0.05,
        )
        st.plotly_chart(fig_iv, use_container_width=True, config=PLOTLY_CONFIG)

    with r1c2:
        st.markdown("""
        <div class="chart-box">
          <div class="chart-box-title">Revenue per Order Distribution</div>
          <div class="chart-box-subtitle">Order value — clipped at 95th percentile</div>
          <hr class="chart-box-divider">
        </div>""", unsafe_allow_html=True)
        rev_clip = basket["Revenue"].clip(upper=basket["Revenue"].quantile(0.95))
        fig_basket = go.Figure(go.Histogram(
            x=rev_clip, nbinsx=40,
            marker=dict(color="#55A868", line=dict(color="white", width=0.5)),
        ))
        fig_basket.add_vline(x=float(basket["Revenue"].mean()), line_dash="dash", line_color="#C44E52",
                             annotation_text=f"Mean: £{fmt_currency(basket['Revenue'].mean())}",
                             annotation_font_size=9, annotation_bgcolor="#C44E52",
                             annotation_font_color="white")
        fig_basket.add_vline(x=float(basket["Revenue"].median()), line_dash="dash", line_color="#4C72B0",
                             annotation_text=f"Median: £{fmt_currency(basket['Revenue'].median())}",
                             annotation_font_size=9, annotation_bgcolor="#4C72B0",
                             annotation_font_color="white")
        fig_basket.update_layout(
            **BASE_LAYOUT, height=280,
            xaxis=dict(title="Revenue per Order (£)", tickfont_size=9, gridcolor="#f1f5f9"),
            yaxis=dict(title="Number of Orders", tickfont_size=9, gridcolor="#f1f5f9"),
            margin=dict(l=55, r=15, t=10, b=45), bargap=0.04,
        )
        st.plotly_chart(fig_basket, use_container_width=True, config=PLOTLY_CONFIG)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    r2c1, r2c2 = st.columns(2)

    with r2c1:
        dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        dow_data = dff.groupby("DayOfWeek")["InvoiceNo"].nunique().reindex(dow_order).fillna(0)

        st.markdown("""
        <div class="chart-box">
          <div class="chart-box-title">Orders by Day of Week</div>
          <div class="chart-box-subtitle">Which days drive the most transaction volume</div>
          <hr class="chart-box-divider">
        </div>""", unsafe_allow_html=True)
        fig_dow = go.Figure(go.Bar(
            x=dow_data.index,
            y=dow_data.values,
            marker=dict(color="#4C72B0", line=dict(width=0)),
        ))
        fig_dow.update_layout(
            **BASE_LAYOUT, height=260,
            xaxis=dict(tickfont_size=9, showgrid=False),
            yaxis=dict(tickfont_size=9, gridcolor="#f1f5f9", title="Orders"),
            bargap=0.25,
            margin=dict(l=45, r=10, t=5, b=40),
        )
        st.plotly_chart(fig_dow, use_container_width=True, config=PLOTLY_CONFIG)

    with r2c2:
        hod_data = dff.groupby("Hour")["InvoiceNo"].nunique()

        # ★ FIX: use numeric x values, format display via ticktext
        hod_hours = list(range(int(hod_data.index.min()), int(hod_data.index.max()) + 1))
        hod_labels = [f"{h:02d}:00" for h in hod_hours]
        peak_hour = int(hod_data.idxmax())

        st.markdown("""
        <div class="chart-box">
          <div class="chart-box-title">Orders by Hour of Day</div>
          <div class="chart-box-subtitle">Peak shopping hours — optimize campaigns & staffing</div>
          <hr class="chart-box-divider">
        </div>""", unsafe_allow_html=True)
        fig_hod = go.Figure(go.Bar(
            x=hod_data.index,
            y=hod_data.values,
            marker=dict(color="#7c3aed", line=dict(width=0)),
        ))
        fig_hod.add_vline(x=peak_hour, line_dash="dash", line_color="#C44E52",
                          annotation_text=f"Peak: {peak_hour:02d}:00",
                          annotation_font_size=9, annotation_bgcolor="#C44E52",
                          annotation_font_color="white")
        fig_hod.update_layout(
            **BASE_LAYOUT, height=260,
            xaxis=dict(
                tickfont_size=7, showgrid=False, tickangle=-45,
                tickvals=hod_hours,
                ticktext=hod_labels,
            ),
            yaxis=dict(tickfont_size=9, gridcolor="#f1f5f9", title="Orders"),
            bargap=0.15,
            margin=dict(l=45, r=10, t=5, b=55),
        )
        st.plotly_chart(fig_hod, use_container_width=True, config=PLOTLY_CONFIG)


# ═══════════════════════════════════════════════════════════
# TAB 6 — BUSINESS RECOMMENDATIONS
# ═══════════════════════════════════════════════════════════
with tab6:
    section_intro("LEVEL 7", "Actionable Business Recommendations",
        "Rekomendasi strategis yang langsung bisa dieksekusi berdasarkan data — "
        "diurutkan dari <strong>impact tertinggi</strong> ke lowest effort.")

    seg_counts = rfm_disp["Segment"].value_counts()
    seg_clv_avg = rfm_disp.groupby("Segment")["CLV"].mean()
    total_seg = seg_counts.sum()

    recommendations = []

    if "Champions" in seg_counts.index:
        cnt = seg_counts["Champions"]
        pct = cnt / total_seg * 100
        clv = seg_clv_avg.get("Champions", 0)
        recommendations.append({
            "seg": "🏆 Champions",
            "meta": f"{cnt:,} customers ({pct:.1f}%) · Avg CLV: £{fmt_currency(clv)}",
            "action": "Launch exclusive VIP tier with early access & bundled premium products",
            "rationale": f"Top {pct:.1f}% of customers generating disproportionate value. Upsell potential is highest here with minimal acquisition cost.",
            "border": "#10b981",
        })

    if "At Risk" in seg_counts.index:
        cnt = seg_counts["At Risk"]
        pct = cnt / total_seg * 100
        clv = seg_clv_avg.get("At Risk", 0)
        recommendations.append({
            "seg": "⚠️ At Risk",
            "meta": f"{cnt:,} customers ({pct:.1f}%) · Avg CLV: £{fmt_currency(clv)}",
            "action": "Trigger win-back campaign within 30 days: personalized discount + product recommendation",
            "rationale": f"These {cnt:,} customers have bought before but are slowing down. Re-acquisition costs 5-7x more than retention.",
            "border": "#f59e0b",
        })

    if "Potential Loyalists" in seg_counts.index:
        cnt = seg_counts["Potential Loyalists"]
        pct = cnt / total_seg * 100
        clv = seg_clv_avg.get("Potential Loyalists", 0)
        recommendations.append({
            "seg": "🌱 Potential Loyalists",
            "meta": f"{cnt:,} customers ({pct:.1f}%) · Avg CLV: £{fmt_currency(clv)}",
            "action": "Implement loyalty points program & cross-sell complementary categories",
            "rationale": f"Recent buyers with moderate frequency. Small nudge can push them into Loyal Customers segment.",
            "border": "#2563eb",
        })

    if "Cant Lose Them" in seg_counts.index:
        cnt = seg_counts["Cant Lose Them"]
        pct = cnt / total_seg * 100
        clv = seg_clv_avg.get("Cant Lose Them", 0)
        recommendations.append({
            "seg": "🚨 Can't Lose Them",
            "meta": f"{cnt:,} customers ({pct:.1f}%) · Avg CLV: £{fmt_currency(clv)}",
            "action": "Assign dedicated account manager / send personalized handwritten-note-level outreach",
            "rationale": f"High-value customers who haven't bought recently. Each lost customer = £{fmt_currency(clv)} lifetime value gone.",
            "border": "#ef4444",
        })

    if "New Customers" in seg_counts.index:
        cnt = seg_counts["New Customers"]
        pct = cnt / total_seg * 100
        clv = seg_clv_avg.get("New Customers", 0)
        recommendations.append({
            "seg": "🆕 New Customers",
            "meta": f"{cnt:,} customers ({pct:.1f}%) · Avg CLV: £{fmt_currency(clv)}",
            "action": "Automated 7-day onboarding sequence: thank you → bestseller guide → first repeat purchase incentive",
            "rationale": f"First 30 days are critical. Without intervention, {pct_one:.0f}% of one-time buyers never return.",
            "border": "#7c3aed",
        })

    if "Lost Customers" in seg_counts.index:
        cnt = seg_counts["Lost Customers"]
        pct = cnt / total_seg * 100
        clv = seg_clv_avg.get("Lost Customers", 0)
        recommendations.append({
            "seg": "📉 Lost Customers",
            "meta": f"{cnt:,} customers ({pct:.1f}%) · Avg CLV: £{fmt_currency(clv)}",
            "action": "Low-priority: batch email reactivation with deep discount — only if CLV justifies cost",
            "rationale": f"Low recency AND low frequency. Focus resources on higher-ROI segments first.",
            "border": "#9ca3af",
        })

    if "Loyal Customers" in seg_counts.index:
        cnt = seg_counts["Loyal Customers"]
        pct = cnt / total_seg * 100
        clv = seg_clv_avg.get("Loyal Customers", 0)
        recommendations.append({
            "seg": "💎 Loyal Customers",
            "meta": f"{cnt:,} customers ({pct:.1f}%) · Avg CLV: £{fmt_currency(clv)}",
            "action": "Launch referral program — they are your best brand ambassadors",
            "rationale": f"Consistent buyers with strong engagement. Referral-acquired customers have 37% higher retention rate.",
            "border": "#55A868",
        })

    for rec in recommendations:
        st.markdown(f"""
        <div class="reco-card" style="border-left-color:{rec['border']}">
          <div class="reco-head">
            <span class="reco-seg">{rec['seg']}</span>
            <span class="reco-meta">{rec['meta']}</span>
          </div>
          <div class="reco-action">→ {rec['action']}</div>
          <div class="reco-rationale">{rec['rationale']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        st.markdown(f"""
        <div class="insight-card" style="border-left-color:#10b981">
          <div class="ic-title" style="color:#10b981">Revenue Protection</div>
          <div class="ic-headline">£{fmt_currency(clv_sorted.head(int(len(clv_sorted)*0.2))['Revenue'].sum())}</div>
          <div class="ic-sub">at risk if top 20% customers churn — equal to {top20_pct:.0f}% of total revenue</div>
        </div>""", unsafe_allow_html=True)
    with ic2:
        st.markdown(f"""
        <div class="insight-card" style="border-left-color:#f59e0b">
          <div class="ic-title" style="color:#f59e0b">Quick Win Opportunity</div>
          <div class="ic-headline">{fmt_num(int(seg_counts.get('Potential Loyalists', 0)))} customers</div>
          <div class="ic-sub">one nudge away from becoming Loyal — lowest effort, high conversion probability</div>
        </div>""", unsafe_allow_html=True)
    with ic3:
        st.markdown(f"""
        <div class="insight-card" style="border-left-color:#ef4444">
          <div class="ic-title" style="color:#ef4444">Urgent Attention</div>
          <div class="ic-headline">{fmt_num(int(seg_counts.get('Cant Lose Them', 0) + seg_counts.get('At Risk', 0)))} customers</div>
          <div class="ic-sub">combined At Risk + Can't Lose Them — act within 30 days or lose them permanently</div>
        </div>""", unsafe_allow_html=True)