"""
Retail Profitability Analyzer — Enhanced Executive Dashboard
Adaptive Light/Dark Mode Premium Design + Decision-Support Features

Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Retail Profitability Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DESIGN TOKENS
# ============================================================
PRIMARY   = "#2563EB"   # Blue
SUCCESS   = "#10B981"   # Emerald
WARNING   = "#F59E0B"   # Amber
DANGER    = "#EF4444"   # Red
PURPLE    = "#8B5CF6"   # Purple
NEUTRAL   = "#94A3B8"   # Slate
PALETTE   = ["#2563EB", "#38BDF8", "#818CF8", "#C084FC", "#F472B6"]

# Konfigurasi standar Plotly agar responsif di HP/Tablet
PLOTLY_CONFIG = {
    "displayModeBar": False, # Menyembunyikan menu zoom/pan yang mengganggu di layar kecil
    "responsive": True
}

# ============================================================
# GLOBAL CSS (ADAPTIVE LIGHT/DARK MODE & MOBILE RESPONSIVE)
# ============================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    /* Sembunyikan footer bawaan Streamlit */
    footer {visibility: hidden;}
    
    .block-container { padding-top: 1rem; padding-bottom: 3rem; max-width: 1280px; }

    /* ===== SIDEBAR ===== */
    .sidebar-logo { display: flex; align-items: center; gap: 10px; margin-bottom: 4px; }
    .sidebar-logo-mark {
        width: 36px; height: 36px; border-radius: 9px;
        background: linear-gradient(135deg, #2563EB, #8B5CF6);
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; font-size: 17px; color: white;
    }
    .sidebar-logo-text { font-size: 15px; font-weight: 800; color: var(--text-color); line-height: 1.2; }
    .sidebar-logo-sub  { font-size: 10.5px; color: gray; letter-spacing: 0.5px; font-weight: 600; }

    /* ===== ALERT BANNER ===== */
    .alert-banner {
        border-radius: 10px; padding: 14px 18px; margin-bottom: 10px;
        display: flex; align-items: flex-start; gap: 12px; 
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    .alert-critical { background-color: rgba(239, 68, 68, 0.1); border-color: rgba(239, 68, 68, 0.3); }
    .alert-warning  { background-color: rgba(245, 158, 11, 0.1); border-color: rgba(245, 158, 11, 0.3); }
    .alert-success  { background-color: rgba(16, 185, 129, 0.1); border-color: rgba(16, 185, 129, 0.3); }
    .alert-icon { font-size: 18px; line-height: 1.4; }
    .alert-text { font-size: 13.5px; color: var(--text-color); line-height: 1.5; flex: 1; }
    .alert-text b { font-weight: 700; }
    .alert-critical .alert-text b { color: #EF4444; }
    .alert-warning  .alert-text b { color: #F59E0B; }
    .alert-success  .alert-text b { color: #10B981; }

    /* ===== KPI CARD (Adaptive) ===== */
    .kpi-card {
        background-color: var(--secondary-background-color); 
        border: 1px solid rgba(128, 128, 128, 0.2); 
        border-radius: 14px; padding: 20px 22px; height: 100%; 
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }
    .kpi-card:hover { box-shadow: 0 8px 20px rgba(0,0,0,0.15); transform: translateY(-2px); }
    .kpi-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
    .kpi-label { font-size: 11.5px; font-weight: 700; letter-spacing: 0.6px; text-transform: uppercase; color: gray; }
    .kpi-icon { width: 32px; height: 32px; border-radius: 9px; display: flex; align-items: center; justify-content: center; font-size: 15px; flex-shrink: 0; }
    .kpi-value { font-size: 28px; font-weight: 800; color: var(--text-color); line-height: 1.1; margin-bottom: 8px; }
    .delta-up   { background-color: rgba(16, 185, 129, 0.1); color: #10B981; }
    .delta-down { background-color: rgba(239, 68, 68, 0.1); color: #EF4444; }
    .kpi-delta { font-size: 12.5px; font-weight: 700; display: inline-flex; align-items: center; gap: 4px; padding: 2px 8px; border-radius: 6px; }
    .kpi-sub { font-size: 12px; color: gray; margin-top: 6px; }

    /* ===== SECTION HEADER ===== */
    .sec-header { display: flex; align-items: center; gap: 10px; margin: 8px 0 2px 0; }
    .sec-title { font-size: 19px; font-weight: 800; color: var(--text-color); }
    .sec-desc  { font-size: 13px; color: gray; margin: 4px 0 16px 0; max-width: 760px; line-height: 1.6; }

    /* ===== CONTAINER STYLING (SAFE) ===== */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: var(--secondary-background-color);
        border-radius: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border: 1px solid rgba(128, 128, 128, 0.2);
    }
    .chart-card-title { font-size: 14.5px; font-weight: 700; color: var(--text-color); margin-bottom: 2px; padding: 0 5px; }
    .chart-card-sub   { font-size: 12px; color: gray; margin-bottom: 10px; padding: 0 5px; }

    /* ===== ACTION CARD ===== */
    .action-card { background-color: var(--secondary-background-color); border: 1px solid rgba(128, 128, 128, 0.2); border-radius: 12px; padding: 18px 20px; margin-bottom: 12px; }
    .action-badge { font-size: 10.5px; font-weight: 700; padding: 3px 10px; border-radius: 5px; display: inline-block; margin-bottom: 10px; }
    .action-badge.p1 { background-color: rgba(239, 68, 68, 0.1); color: #EF4444; }
    .action-badge.p2 { background-color: rgba(245, 158, 11, 0.1); color: #F59E0B; }
    .action-title { font-size: 15px; font-weight: 700; color: var(--text-color); margin-bottom: 6px; }
    .action-body  { font-size: 13px; color: gray; line-height: 1.6; margin-bottom: 12px; }
    .action-stats { display: flex; flex-wrap: wrap; gap: 24px; padding-top: 10px; border-top: 1px solid rgba(128, 128, 128, 0.2); }
    .action-stat-label { font-size: 10.5px; color: gray; text-transform: uppercase; margin-bottom: 2px; }
    .action-stat-value { font-size: 14.5px; font-weight: 700; color: var(--text-color); }

    h1, h2, h3 { color: var(--text-color) !important; margin-bottom: 0.1rem !important; }
    hr { margin: 1.8rem 0 !important; border-color: rgba(128, 128, 128, 0.2); opacity: 0.8; }
    .footer { text-align:center; padding: 24px 0 4px 0; color: gray; font-size: 12px; }

    /* ===== MOBILE RESPONSIVE ===== */
    @media (max-width: 768px) {
        .block-container { padding-top: 2rem; padding-bottom: 1.5rem; padding-left: 0.8rem; padding-right: 0.8rem; }
        .kpi-card { padding: 14px 16px; }
        .kpi-value { font-size: 22px; margin-bottom: 5px; }
        .kpi-icon { width: 26px; height: 26px; font-size: 12px; }
        .kpi-label { font-size: 10px; }
        .kpi-sub { font-size: 11px; }
        h1 { font-size: 1.6rem !important; margin-top: 10px !important; }
        .sec-title { font-size: 16px; }
        .sec-desc { font-size: 12px; margin-bottom: 12px; }
        .chart-card-title { font-size: 13.5px; }
        .action-stats { gap: 14px; flex-direction: row; }
        .alert-banner { padding: 12px 14px; align-items: center; }
        .alert-icon { font-size: 16px; }
        .alert-text { font-size: 12.5px; }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SIDEBAR & NAVIGATION
# ============================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-mark">R</div>
        <div>
            <div class="sidebar-logo-text">SuperStore</div>
            <div class="sidebar-logo-sub">EXECUTIVE DASHBOARD</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    menu = st.radio(
        "Navigation",
        ["🏠 Executive Summary", "📈 Trend & Seasonality", "🌎 Geo-Performance",
         "🛒 Product Portfolio", "🚨 Profitability Risks", "👥 Customer Insights"],
        label_visibility="collapsed"
    )

# ============================================================
# DATA LOADING
# ============================================================
@st.cache_data(show_spinner=False)
def load_data():
    candidates = ["Sample_-_Superstore.csv", "SampleSuperstore.csv", "Superstore.csv", "projects/retail_profitability/data/SampleSuperstore.csv"]
    df = None
    for path in candidates:
        if os.path.exists(path):
            df = pd.read_csv(path, encoding="latin-1")
            break

    if df is None:
        # Dummy fallback
        st.warning("⚠️ File CSV tidak ditemukan. Menggunakan data simulasi untuk demonstrasi.")
        np.random.seed(42)
        dates = pd.date_range(start='2020-01-01', end='2023-12-31', freq='D')
        n = len(dates)
        df = pd.DataFrame({
            'Order Date': dates,
            'Sales': np.random.uniform(10, 2000, n),
            'Discount': np.random.choice([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7], n, p=[0.4, 0.2, 0.15, 0.1, 0.05, 0.05, 0.05]),
            'Category': np.random.choice(['Technology', 'Furniture', 'Office Supplies'], n),
            'Sub-Category': np.random.choice([f'Sub-{i}' for i in range(1, 10)], n),
            'Region': np.random.choice(['East', 'West', 'Central', 'South'], n),
            'Segment': np.random.choice(['Consumer', 'Corporate', 'Home Office'], n),
            'Customer Name': np.random.choice([f'Customer-{i}' for i in range(1, 100)], n),
            'Product Name': np.random.choice([f'Product-{i}' for i in range(1, 200)], n)
        })
        base_m = {'Technology': 0.3, 'Office Supplies': 0.4, 'Furniture': 0.15}
        df['Profit'] = df.apply(lambda row: row['Sales'] * (base_m[row['Category']] - row['Discount'] * 1.2), axis=1)

    # Clean Columns
    df.columns = [c.strip() for c in df.columns]
    
    if "Order Date" in df.columns:
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
        df = df.dropna(subset=["Order Date"]).copy()
        df["Year"]       = df["Order Date"].dt.year.astype(int).astype(str)
        df["Month"]      = df["Order Date"].dt.month
        df["Month Name"] = df["Order Date"].dt.strftime("%b")
    else:
        df["Year"] = "All"
        df["Month Name"] = "All"
        df["Order Date"] = pd.Timestamp.today()
    
    for col in ["Sales", "Profit", "Discount"]:
        if col not in df.columns: df[col] = 0

    df["Profit Margin"] = np.where(df["Sales"] > 0, df["Profit"] / df["Sales"], 0)
    df["Is Loss"]    = df["Profit"] < 0

    bins = [-0.01, 0.00, 0.10, 0.20, 0.30, 0.50, 1.01]
    labels = ["No Discount", "1–10%", "11–20%", "21–30%", "31–50%", "51%+"]
    df["Discount Bucket"] = pd.cut(df["Discount"], bins=bins, labels=labels)
    return df

df_raw = load_data()

if df_raw is None or df_raw.empty:
    st.error("⚠️ Dataset tidak ditemukan atau kosong. Silakan pastikan file CSV tersedia.")
    st.stop()

# ============================================================
# HELPERS
# ============================================================
def fmt_currency(num):
    if pd.isna(num): return "$0"
    if abs(num) >= 1_000_000: return f"${num/1_000_000:.2f}M"
    if abs(num) >= 1_000: return f"${num/1_000:.1f}K"
    return f"${num:.0f}"

def fmt_pct(num):
    if pd.isna(num): return "0%"
    return f"{num:.1f}%"

def delta_badge(value, suffix="%", invert=False):
    is_up = value >= 0
    good = is_up if not invert else not is_up
    cls = "delta-up" if good else "delta-down"
    arrow = "▲" if is_up else "▼"
    return f'<span class="kpi-delta {cls}">{arrow} {abs(value):.1f}{suffix}</span>'

def chart_layout(fig, height=380, show_legend=True):
    # PERBAIKAN CHART RESPONSIVE: Margin automargin dan legend di bawah (bottom) rata tengah
    fig.update_layout(
        height=height,
        margin=dict(t=20, b=40, l=10, r=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", size=11), 
        hoverlabel=dict(font_size=12, font_family="Inter"),
        showlegend=show_legend,
        legend=dict(
            orientation="h", 
            yanchor="top", y=-0.15, 
            xanchor="center", x=0.5, 
            font=dict(size=10)
        ) if show_legend else None,
        autosize=True
    )
    fig.update_xaxes(showgrid=False, zeroline=False, automargin=True)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(128,128,128,0.2)", zeroline=False, automargin=True)
    return fig

def render_kpi_card(label, value, icon, icon_bg, icon_color, delta_val=None, delta_suffix="%", invert_delta=False, sub_text=None, value_color=None):
    value_cls = f' style="color:{value_color};"' if value_color else ""
    delta_html = delta_badge(delta_val, delta_suffix, invert_delta) if delta_val is not None else ""
    sub_html = f'<div class="kpi-sub">{sub_text}</div>' if sub_text else ""
    
    html_output = (
        f'<div class="kpi-card">'
        f'<div class="kpi-top">'
        f'<div class="kpi-label">{label}</div>'
        f'<div class="kpi-icon" style="background:{icon_bg}; color:{icon_color};">{icon}</div>'
        f'</div>'
        f'<div class="kpi-value"{value_cls}>{value}</div>'
        f'{delta_html}{sub_html}'
        f'</div>'
    )
    st.markdown(html_output, unsafe_allow_html=True)

# ============================================================
# SIDEBAR — GLOBAL FILTERS
# ============================================================
with st.sidebar:
    st.markdown("---")
    st.markdown("**🎛️ Global Filters**")

    available_years = sorted(df_raw["Year"].unique().tolist(), reverse=True)
    sel_year = st.selectbox("Year", ["All Years"] + available_years)

    if "Region" in df_raw.columns:
        available_regions = sorted(df_raw["Region"].dropna().unique().tolist())
        sel_region = st.selectbox("Region", ["All Regions"] + available_regions)
    else:
        sel_region = "All Regions"

    if "Segment" in df_raw.columns:
        available_segments = sorted(df_raw["Segment"].dropna().unique().tolist())
        sel_segment = st.selectbox("Segment", ["All Segments"] + available_segments)
    else:
        sel_segment = "All Segments"

    st.markdown("---")
    st.caption("⚙️ Data Management")
    csv_export = df_raw.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Export Current Data", data=csv_export, file_name="Superstore_Export.csv", mime="text/csv", use_container_width=True)

# ============================================================
# APPLY FILTERS
# ============================================================
df = df_raw.copy()
if sel_year != "All Years":
    df = df[df["Year"] == sel_year]
if sel_region != "All Regions" and "Region" in df.columns:
    df = df[df["Region"] == sel_region]
if sel_segment != "All Segments" and "Segment" in df.columns:
    df = df[df["Segment"] == sel_segment]

if df.empty:
    st.warning("⚠️ Kombinasi filter yang dipilih tidak memiliki data. Silakan ubah opsi filter Anda di Sidebar.")
    st.stop()

# ============================================================
# CORE METRICS & SAFE CALCULATIONS
# ============================================================
total_rev    = df["Sales"].sum()
total_profit = df["Profit"].sum()
avg_margin   = (total_profit / total_rev * 100) if total_rev > 0 else 0

order_col = "Order ID" if "Order ID" in df.columns else "Sales"
total_orders = df[order_col].nunique() if "Order ID" in df.columns else len(df)

loss_count   = df["Is Loss"].sum()
loss_rate    = (loss_count / len(df) * 100) if len(df) > 0 else 0
avg_discount = df["Discount"].mean() * 100

high_disc       = df[df["Discount"] > 0.20]
high_disc_loss  = high_disc["Profit"].sum()
high_disc_count = len(high_disc)

def render_alerts():
    alerts = []
    if avg_margin < 8:
        alerts.append(("critical", "🔴", f"<b>Margin Critical:</b> Overall profit margin is {avg_margin:.1f}%, below the 8% danger threshold. Immediate review recommended."))
    elif avg_margin < 12:
        alerts.append(("warning", "🟡", f"<b>Margin Watch:</b> Overall profit margin is {avg_margin:.1f}%, below the 12% healthy benchmark."))

    if loss_rate > 25:
        alerts.append(("critical", "🔴", f"<b>High Loss Rate:</b> {loss_rate:.1f}% of transactions are losing money — well above the 15% acceptable threshold."))
    elif loss_rate > 15:
        alerts.append(("warning", "🟡", f"<b>Loss Rate Elevated:</b> {loss_rate:.1f}% of transactions are unprofitable (threshold: 15%)."))

    high_disc_share = (high_disc_count / len(df) * 100) if len(df) else 0
    if high_disc_share > 15:
        alerts.append(("critical", "🔴", f"<b>Discount Exposure High:</b> {high_disc_share:.1f}% of transactions exceed the 20% discount threshold, destroying {fmt_currency(abs(high_disc_loss))} in profit."))

    if not alerts:
        alerts.append(("success", "✅", f"<b>Healthy Performance:</b> Margin ({avg_margin:.1f}%) and loss rate ({loss_rate:.1f}%) are within acceptable ranges for the current filter selection."))

    for level, icon, text in alerts:
        st.markdown(f"""
        <div class="alert-banner alert-{level}">
            <div class="alert-icon">{icon}</div>
            <div class="alert-text">{text}</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# PAGE 1: EXECUTIVE SUMMARY
# ============================================================
if menu == "🏠 Executive Summary":
    st.title("Executive Summary")
    st.caption("High-level overview of business health, profitability, and key performance indicators.")

    active_filters = []
    if sel_year != "All Years": active_filters.append(f"Year: {sel_year}")
    if sel_region != "All Regions": active_filters.append(f"Region: {sel_region}")
    if sel_segment != "All Segments": active_filters.append(f"Segment: {sel_segment}")
    if active_filters:
        st.info(f"🔍 **Active Filters:** {' | '.join(active_filters)}")

    rev_yoy = prof_yoy = margin_yoy = loss_rate_yoy = None
    comparison_label = "vs prior period"

    available_years_sorted = sorted(df_raw["Year"].unique().tolist())
    if sel_year == "All Years" and len(available_years_sorted) >= 2:
        latest_yr = available_years_sorted[-1]
        prev_yr   = available_years_sorted[-2]
        base = df_raw.copy()
        if sel_region != "All Regions" and "Region" in base.columns: base = base[base["Region"] == sel_region]
        if sel_segment != "All Segments" and "Segment" in base.columns: base = base[base["Segment"] == sel_segment]

        d_latest = base[base["Year"] == latest_yr]
        d_prev   = base[base["Year"] == prev_yr]

        rev_l, rev_p = d_latest["Sales"].sum(), d_prev["Sales"].sum()
        prof_l, prof_p = d_latest["Profit"].sum(), d_prev["Profit"].sum()
        margin_l = (prof_l / rev_l * 100) if rev_l > 0 else 0
        margin_p = (prof_p / rev_p * 100) if rev_p > 0 else 0
        lr_l = d_latest["Is Loss"].mean() * 100 if len(d_latest) > 0 else 0
        lr_p = d_prev["Is Loss"].mean() * 100 if len(d_prev) > 0 else 0

        rev_yoy    = ((rev_l - rev_p) / rev_p * 100) if rev_p > 0 else 0
        prof_yoy   = ((prof_l - prof_p) / prof_p * 100) if prof_p > 0 else 0
        margin_yoy = margin_l - margin_p
        loss_rate_yoy = lr_l - lr_p
        comparison_label = f"vs {prev_yr}"

    render_alerts()
    st.write("")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_kpi_card("Total Revenue", fmt_currency(total_rev), "$", "rgba(37, 99, 235, 0.1)", PRIMARY,
                        delta_val=rev_yoy, sub_text=comparison_label if rev_yoy is not None else f"{total_orders:,} orders")
    with c2:
        render_kpi_card("Total Profit", fmt_currency(total_profit), "▲", "rgba(16, 185, 129, 0.1)", SUCCESS,
                        delta_val=prof_yoy, sub_text=comparison_label if prof_yoy is not None else f"{avg_margin:.1f}% margin")
    with c3:
        render_kpi_card("Avg Profit Margin", fmt_pct(avg_margin), "%", "rgba(245, 158, 11, 0.1)", WARNING,
                        delta_val=margin_yoy, delta_suffix=" pts", sub_text=comparison_label if margin_yoy is not None else "Target: ≥12%",
                        value_color=DANGER if avg_margin < 8 else None)
    with c4:
        render_kpi_card("Loss Transaction Rate", fmt_pct(loss_rate), "!", "rgba(239, 68, 68, 0.1)", DANGER,
                        delta_val=loss_rate_yoy, delta_suffix=" pts", invert_delta=True,
                        sub_text=comparison_label if loss_rate_yoy is not None else "Threshold: <15%",
                        value_color=DANGER if loss_rate > 15 else None)

    st.markdown("<br>", unsafe_allow_html=True)

    if "Category" in df.columns:
        col_mid1, col_mid2 = st.columns([3, 2], gap="large")

        with col_mid1:
            with st.container(border=True):
                st.markdown('<div class="chart-card-title">Revenue & Profit Contribution by Category</div>', unsafe_allow_html=True)
                st.markdown('<div class="chart-card-sub">Click legend items to isolate a series</div>', unsafe_allow_html=True)

                cat_agg = df.groupby("Category").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()
                
                fig_cat = make_subplots(specs=[[{"secondary_y": True}]])
                fig_cat.add_trace(go.Bar(
                    x=cat_agg["Category"], y=cat_agg["Sales"], name="Revenue",
                    marker_color=PRIMARY, opacity=0.85,
                    text=cat_agg["Sales"].apply(fmt_currency), textposition="outside"
                ), secondary_y=False)
                fig_cat.add_trace(go.Scatter(
                    x=cat_agg["Category"], y=cat_agg["Profit"], name="Profit",
                    mode="lines+markers", line=dict(color=SUCCESS, width=3),
                    marker=dict(size=10, symbol="diamond")
                ), secondary_y=True)

                fig_cat = chart_layout(fig_cat, height=340)
                fig_cat.update_yaxes(title_text="Revenue ($)", secondary_y=False)
                fig_cat.update_yaxes(title_text="Profit ($)", secondary_y=True, showgrid=False)
                st.plotly_chart(fig_cat, use_container_width=True, config=PLOTLY_CONFIG)

        with col_mid2:
            with st.container(border=True):
                st.markdown('<div class="chart-card-title">Profit Leaks by Region</div>', unsafe_allow_html=True)
                st.markdown('<div class="chart-card-sub">Where loss-making transactions concentrate</div>', unsafe_allow_html=True)

                if "Region" in df.columns:
                    loss_df = df[df["Is Loss"]]
                    if not loss_df.empty:
                        total_loss_val = abs(loss_df["Profit"].sum())
                        loss_by_reg = loss_df.groupby("Region")["Profit"].sum().abs().reset_index()
                        loss_by_reg = loss_by_reg.sort_values("Profit", ascending=False)

                        fig_leak = go.Figure(go.Pie(
                            labels=loss_by_reg["Region"], values=loss_by_reg["Profit"], hole=0.62,
                            marker_colors=[DANGER, "#F87171", "#FCA5A5", "#FEE2E2"],
                            textinfo="percent+label"
                        ))
                        fig_leak.update_layout(
                            annotations=[dict(text=f"Total Loss<br><b>{fmt_currency(total_loss_val)}</b>",
                                              x=0.5, y=0.5, font_size=15, showarrow=False, font_color=DANGER)]
                        )
                        fig_leak = chart_layout(fig_leak, height=340, show_legend=False)
                        st.plotly_chart(fig_leak, use_container_width=True, config=PLOTLY_CONFIG)
                    else:
                        st.success("🎉 No loss-making transactions in this view.")
                else:
                    st.info("Region column not found in dataset.")

        st.markdown("---")

        if "Sub-Category" in df.columns:
            st.markdown('<div class="sec-header"><div class="sec-title">🔎 Drill-Down: Category → Sub-Category</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-desc">Select a category below to see how its sub-categories perform.</div>', unsafe_allow_html=True)

            drill_cat = st.selectbox("Select a category to drill into:", sorted(df["Category"].unique()), key="exec_drill")
            drill_df = df[df["Category"] == drill_cat]
            sub_drill = drill_df.groupby("Sub-Category").agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()
            sub_drill = sub_drill.sort_values("Profit")

            with st.container(border=True):
                fig_drill = go.Figure(go.Bar(
                    x=sub_drill["Profit"], y=sub_drill["Sub-Category"], orientation="h",
                    marker_color=[DANGER if p < 0 else SUCCESS for p in sub_drill["Profit"]],
                    text=sub_drill["Profit"].apply(fmt_currency), textposition="outside"
                ))
                fig_drill.add_vline(x=0, line_color="gray", line_width=1.5)
                fig_drill = chart_layout(fig_drill, height=300, show_legend=False)
                fig_drill.update_xaxes(title="Total Profit ($)")
                st.plotly_chart(fig_drill, use_container_width=True, config=PLOTLY_CONFIG)

# ============================================================
# PAGE 2: TREND & SEASONALITY
# ============================================================
elif menu == "📈 Trend & Seasonality":
    st.title("Trend & Seasonality Analysis")
    st.caption("Track performance over time to identify seasonal peaks and structural margin decay.")

    try:
        monthly_ts = df.set_index("Order Date").resample("ME").agg(
            Sales=("Sales", "sum"), Profit=("Profit", "sum"), Discount=("Discount", "mean")
        ).reset_index()
    except Exception:
        monthly_ts = df.set_index("Order Date").resample("M").agg(
            Sales=("Sales", "sum"), Profit=("Profit", "sum"), Discount=("Discount", "mean")
        ).reset_index()
        
    monthly_ts["Margin"] = np.where(monthly_ts["Sales"] > 0, (monthly_ts["Profit"] / monthly_ts["Sales"] * 100), 0)

    neg_months = (monthly_ts["Margin"] < 0).sum()
    if neg_months > 0:
        st.markdown(f"""
        <div class="alert-banner alert-warning">
            <div class="alert-icon">🟡</div>
            <div class="alert-text"><b>{neg_months} month(s)</b> in the selected period show negative profit margin — see heatmap below to identify exactly which months.</div>
        </div>
        """, unsafe_allow_html=True)
    st.write("")

    with st.container(border=True):
        st.markdown('<div class="chart-card-title">Historical Revenue & Profit Margin Trajectory</div>', unsafe_allow_html=True)
        fig_ts = make_subplots(specs=[[{"secondary_y": True}]])
        fig_ts.add_trace(go.Scatter(
            x=monthly_ts["Order Date"], y=monthly_ts["Sales"], name="Revenue",
            mode="lines", fill="tozeroy", line=dict(color=PRIMARY, width=2),
            fillcolor="rgba(37,99,235,0.08)"
        ), secondary_y=False)
        margin_colors = [DANGER if m < 0 else SUCCESS for m in monthly_ts["Margin"]]
        fig_ts.add_trace(go.Scatter(
            x=monthly_ts["Order Date"], y=monthly_ts["Margin"], name="Margin (%)",
            mode="lines+markers", line=dict(color=SUCCESS, width=2.5),
            marker=dict(size=6, color=margin_colors)
        ), secondary_y=True)
        fig_ts.add_hline(y=0, secondary_y=True, line_dash="dash", line_color=DANGER, opacity=0.5)
        fig_ts = chart_layout(fig_ts, height=420)
        fig_ts.update_layout(hovermode="x unified")
        fig_ts.update_yaxes(title_text="Monthly Revenue ($)", secondary_y=False)
        fig_ts.update_yaxes(title_text="Profit Margin (%)", secondary_y=True, showgrid=False)
        st.plotly_chart(fig_ts, use_container_width=True, config=PLOTLY_CONFIG)

    with st.container(border=True):
        st.markdown('<div class="chart-card-title">Seasonality Matrix — Margin by Month & Year</div>', unsafe_allow_html=True)
        st.markdown('<div class="chart-card-sub">Red cells indicate months that consistently underperform on margin</div>', unsafe_allow_html=True)

        if 'Year' in df.columns and 'Month Name' in df.columns:
            sea_df = df.groupby(["Year", "Month", "Month Name"]).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum")).reset_index()
            sea_df["Margin"] = np.where(sea_df["Sales"] > 0, (sea_df["Profit"] / sea_df["Sales"] * 100), 0)
            
            months_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
            sea_df["Month Name"] = pd.Categorical(sea_df["Month Name"], categories=months_order, ordered=True)
            sea_df = sea_df.sort_values(["Year", "Month Name"])
            pivot_margin = sea_df.pivot(index="Year", columns="Month Name", values="Margin")

            fig_heat = go.Figure(go.Heatmap(
                z=pivot_margin.values, x=pivot_margin.columns, y=pivot_margin.index.astype(str),
                colorscale="RdYlGn", zmid=0,
                text=[[f"{v:.1f}%" if pd.notna(v) else "" for v in row] for row in pivot_margin.values],
                texttemplate="%{text}",
                hovertemplate="Year: %{y}<br>Month: %{x}<br>Margin: %{z:.1f}%<extra></extra>"
            ))
            fig_heat = chart_layout(fig_heat, height=320, show_legend=False)
            st.plotly_chart(fig_heat, use_container_width=True, config=PLOTLY_CONFIG)

# ============================================================
# PAGE 3: GEO-PERFORMANCE
# ============================================================
elif menu == "🌎 Geo-Performance":
    st.title("Geographical Performance")
    st.caption("Identify highly profitable regions and isolate areas causing margin dilution.")

    if "Region" in df.columns:
        reg_agg = df.groupby("Region").agg(
            Revenue=("Sales", "sum"), Profit=("Profit", "sum"),
            Orders=(order_col, "nunique" if "Order ID" in df.columns else "count"), 
            AvgDiscount=("Discount", "mean")
        ).reset_index()
        reg_agg["Margin"] = np.where(reg_agg["Revenue"] > 0, (reg_agg["Profit"] / reg_agg["Revenue"] * 100), 0)

        if len(reg_agg) >= 2:
            worst_region = reg_agg.loc[reg_agg["Margin"].idxmin()]
            best_region  = reg_agg.loc[reg_agg["Margin"].idxmax()]
            gap = best_region["Margin"] - worst_region["Margin"]
            if gap > 5:
                st.markdown(f"""
                <div class="alert-banner alert-warning">
                    <div class="alert-icon">🟡</div>
                    <div class="alert-text"><b>{worst_region['Region']}</b> trails <b>{best_region['Region']}</b> by {gap:.1f} percentage points in margin
                    ({worst_region['Margin']:.1f}% vs {best_region['Margin']:.1f}%) despite generating {fmt_currency(worst_region['Revenue'])} in revenue — a discount policy gap, not a demand problem.</div>
                </div>
                """, unsafe_allow_html=True)
            st.write("")

        col1, col2 = st.columns([1.5, 1])
        with col1:
            with st.container(border=True):
                st.markdown('<div class="chart-card-title">Regional Revenue vs Profit Margin</div>', unsafe_allow_html=True)
                st.markdown('<div class="chart-card-sub">Bubble size = order volume</div>', unsafe_allow_html=True)

                max_orders = reg_agg["Orders"].max() if not reg_agg.empty else 1
                size_ref = 2. * max_orders / (40.**2) if max_orders > 0 else 1

                fig_reg = go.Figure(go.Scatter(
                    x=reg_agg["Revenue"], y=reg_agg["Margin"], mode="markers+text",
                    text=reg_agg["Region"], textposition="top center", textfont=dict(size=12),
                    marker=dict(
                        size=reg_agg["Orders"], sizemode="area",
                        sizeref=size_ref, sizemin=12, color=reg_agg["Margin"], colorscale="RdYlGn", 
                        showscale=True, colorbar=dict(title="Margin %"), line=dict(width=2, color="white")
                    )
                ))
                fig_reg = chart_layout(fig_reg, height=380, show_legend=False)
                fig_reg.update_layout(xaxis_title="Total Revenue ($)", yaxis_title="Profit Margin (%)")
                fig_reg.add_hline(y=0, line_dash="dash", line_color=DANGER, annotation_text="Break-even")
                st.plotly_chart(fig_reg, use_container_width=True, config=PLOTLY_CONFIG)

        with col2:
            with st.container(border=True):
                st.markdown('<div class="chart-card-title">Region Metrics</div>', unsafe_allow_html=True)
                disp = reg_agg.copy()
                disp["Revenue"] = disp["Revenue"].apply(fmt_currency)
                disp["Profit"] = disp["Profit"].apply(fmt_currency)
                disp["Margin"] = disp["Margin"].apply(fmt_pct)
                disp["AvgDiscount"] = disp["AvgDiscount"].apply(lambda x: f"{x*100:.1f}%")
                st.dataframe(disp[["Region","Revenue","Profit","Margin","AvgDiscount"]], hide_index=True, use_container_width=True)

        st.write("")
        if "State" in df.columns:
            st.markdown('<div class="sec-header"><div class="sec-title">🔎 Drill-Down: State-Level Detail</div></div>', unsafe_allow_html=True)
            st.markdown('<div class="sec-desc">Select a region to inspect state-level performance within it.</div>', unsafe_allow_html=True)

            drill_region = st.selectbox("Select region:", ["All Regions"] + sorted(df["Region"].unique().tolist()), key="geo_drill")
            geo_drill_df = df if drill_region == "All Regions" else df[df["Region"] == drill_region]
            state_agg = geo_drill_df.groupby("State").agg(Sales=("Sales","sum"), Profit=("Profit","sum")).reset_index()

            col_s1, col_s2 = st.columns(2)
            with col_s1:
                with st.container(border=True):
                    top_states = state_agg.nlargest(10, "Profit").sort_values("Profit")
                    fig_top = go.Figure(go.Bar(
                        x=top_states["Profit"], y=top_states["State"], orientation="h",
                        marker_color=SUCCESS, text=top_states["Profit"].apply(fmt_currency), textposition="auto"
                    ))
                    fig_top = chart_layout(fig_top, height=340, show_legend=False)
                    fig_top.update_layout(title="🏆 Top 10 Most Profitable States", xaxis_title="Profit ($)")
                    st.plotly_chart(fig_top, use_container_width=True, config=PLOTLY_CONFIG)
            with col_s2:
                with st.container(border=True):
                    bot_states = state_agg.nsmallest(10, "Profit").sort_values("Profit", ascending=False)
                    fig_bot = go.Figure(go.Bar(
                        x=bot_states["Profit"], y=bot_states["State"], orientation="h",
                        marker_color=DANGER, text=bot_states["Profit"].apply(fmt_currency), textposition="auto"
                    ))
                    fig_bot = chart_layout(fig_bot, height=340, show_legend=False)
                    fig_bot.update_layout(title="🚨 Top 10 States with Highest Losses", xaxis_title="Losses ($)")
                    st.plotly_chart(fig_bot, use_container_width=True, config=PLOTLY_CONFIG)
    else:
        st.info("Region information not found in the dataset.")

# ============================================================
# PAGE 4: PRODUCT PORTFOLIO
# ============================================================
elif menu == "🛒 Product Portfolio":
    st.title("Product Portfolio Analysis")
    st.caption("Drill down from Categories to specific Products to find the stars and the dead weights.")

    if "Category" in df.columns and "Sub-Category" in df.columns:
        sub_agg = df.groupby(["Category", "Sub-Category"]).agg(Sales=("Sales","sum"), Profit=("Profit","sum")).reset_index()
        sub_agg["Margin"] = np.where(sub_agg["Sales"] > 0, (sub_agg["Profit"] / sub_agg["Sales"] * 100), 0)

        loss_subcats = sub_agg[sub_agg["Profit"] < 0]
        if not loss_subcats.empty:
            names = ", ".join(loss_subcats["Sub-Category"].tolist())
            st.markdown(f"""
            <div class="alert-banner alert-critical">
                <div class="alert-icon">🔴</div>
                <div class="alert-text"><b>{len(loss_subcats)} sub-categor{'y' if len(loss_subcats)==1 else 'ies'} losing money:</b> {names} — combined loss of {fmt_currency(abs(loss_subcats['Profit'].sum()))}.</div>
            </div>
            """, unsafe_allow_html=True)
        st.write("")

        with st.container(border=True):
            st.markdown('<div class="chart-card-title">Sub-Category Performance Matrix</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-card-sub">Box size = revenue · Color = margin (red = loss, green = healthy)</div>', unsafe_allow_html=True)

            sub_agg_map = sub_agg[sub_agg["Sales"] > 0]
            if not sub_agg_map.empty:
                fig_tree = px.treemap(
                    sub_agg_map, path=[px.Constant("All Products"), "Category", "Sub-Category"],
                    values="Sales", color="Margin", color_continuous_scale="RdYlGn", color_continuous_midpoint=0,
                    custom_data=["Profit", "Sales", "Margin"]
                )
                fig_tree.update_traces(
                    hovertemplate="<b>%{label}</b><br>Sales: $%{customdata[1]:,.0f}<br>Profit: $%{customdata[0]:,.0f}<br>Margin: %{customdata[2]:.1f}%<extra></extra>",
                )
                fig_tree = chart_layout(fig_tree, height=440)
                # Full margin untuk treemap
                fig_tree.update_layout(margin=dict(t=10, l=0, r=0, b=0))
                st.plotly_chart(fig_tree, use_container_width=True, config=PLOTLY_CONFIG)

        st.write("")
        st.markdown('<div class="sec-header"><div class="sec-title">🔎 Drill-Down: SKU-Level Detail</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-desc">Select a category to see exactly which products drive its result.</div>', unsafe_allow_html=True)

        drill_pp = st.selectbox("Filter by category:", ["All Categories"] + sorted(df["Category"].unique().tolist()), key="prod_drill")
        pp_df = df if drill_pp == "All Categories" else df[df["Category"] == drill_pp]

        if 'Product Name' in pp_df.columns:
            prod_agg = pp_df.groupby(["Product Name", "Category"]).agg(Sales=("Sales","sum"), Profit=("Profit","sum")).reset_index()

            col_p1, col_p2 = st.columns(2)
            with col_p1:
                with st.container(border=True):
                    st.markdown("**🌟 Top 10 Star Products**")
                    top_p = prod_agg.nlargest(10, "Profit").copy()
                    if not top_p.empty:
                        top_p["Short"] = top_p["Product Name"].apply(lambda x: x[:38] + "…" if len(x) > 38 else x)
                        fig_tp = px.bar(top_p, x="Profit", y="Short", color="Category", orientation="h", color_discrete_sequence=PALETTE)
                        fig_tp = chart_layout(fig_tp, height=380, show_legend=False)
                        fig_tp.update_layout(yaxis={"categoryorder":"total ascending"}, yaxis_title=None, xaxis_title="Profit ($)")
                        st.plotly_chart(fig_tp, use_container_width=True, config=PLOTLY_CONFIG)
                    else:
                        st.info("No data.")
            with col_p2:
                with st.container(border=True):
                    st.markdown("**🗑️ Top 10 Bleeding Products**")
                    bot_p = prod_agg.nsmallest(10, "Profit").copy()
                    if not bot_p.empty:
                        bot_p["Short"] = bot_p["Product Name"].apply(lambda x: x[:38] + "…" if len(x) > 38 else x)
                        fig_bp = px.bar(bot_p, x="Profit", y="Short", color="Category", orientation="h", color_discrete_sequence=PALETTE)
                        fig_bp = chart_layout(fig_bp, height=380, show_legend=False)
                        fig_bp.update_layout(yaxis={"categoryorder":"total descending"}, yaxis_title=None, xaxis_title="Loss ($)")
                        st.plotly_chart(fig_bp, use_container_width=True, config=PLOTLY_CONFIG)
                    else:
                        st.info("No data.")
    else:
         st.info("Category or Sub-Category columns are missing from the dataset.")

# ============================================================
# PAGE 5: PROFITABILITY RISKS (DISCOUNT TRAP)
# ============================================================
elif menu == "🚨 Profitability Risks":
    st.title("Profitability Risks: The Discount Trap")
    st.caption("Analyzing how aggressive discounting strategies are eroding baseline margins.")

    bins = [-0.01, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0]
    labels = ["0%","1-10%","11-20%","21-30%","31-40%","41-50%",">50%"]
    df_risk = df.copy()
    df_risk["Discount Tier"] = pd.cut(df_risk["Discount"], bins=bins, labels=labels)

    high_mask = df_risk["Discount"] > 0.2
    high_df = df_risk[high_mask]
    sales_high = high_df["Sales"].sum()
    
    total_risk_sales = df_risk["Sales"].sum()
    total_risk_len = len(df_risk)
    
    pct_sales_high = (sales_high / total_risk_sales * 100) if total_risk_sales > 0 else 0
    vol_pct_high   = (len(high_df) / total_risk_len * 100) if total_risk_len > 0 else 0
    
    loss_from_disc = high_df[high_df["Profit"] < 0]["Profit"].sum()

    st.markdown(f"""
    <div class="alert-banner alert-critical">
        <div class="alert-icon">🔴</div>
        <div class="alert-text"><b>{len(high_df):,} transactions</b> ({vol_pct_high:.1f}% of volume) exceed the 20% discount threshold,
        destroying <b>{fmt_currency(abs(loss_from_disc))}</b> in profit with virtually no exceptions.</div>
    </div>
    """, unsafe_allow_html=True)
    st.write("")

    c1, c2, c3 = st.columns(3)
    with c1:
        render_kpi_card("Orders >20% Discount", f"{len(high_df):,}", "!", "rgba(239, 68, 68, 0.1)", DANGER,
                        sub_text=f"{vol_pct_high:.1f}% of total volume")
    with c2:
        render_kpi_card("Revenue on High Discount", fmt_currency(sales_high), "%", "rgba(139, 92, 246, 0.1)", PURPLE,
                        sub_text=f"{pct_sales_high:.1f}% of total revenue")
    with c3:
        render_kpi_card("Profit Eroded", fmt_currency(abs(loss_from_disc)), "↓", "rgba(239, 68, 68, 0.1)", DANGER,
                        sub_text="Direct cost of over-discounting", value_color=DANGER)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown('<div class="chart-card-title">Impact of Discount Tiers on Volume and Profitability</div>', unsafe_allow_html=True)
        tier_agg = df_risk.groupby("Discount Tier", observed=False).agg(
            Orders=("Sales","count"), Profit=("Profit","sum"), Sales=("Sales","sum")
        ).reset_index()
        tier_agg["Margin"] = np.where(tier_agg["Sales"] > 0, (tier_agg["Profit"] / tier_agg["Sales"] * 100), 0)

        fig_tier = make_subplots(specs=[[{"secondary_y": True}]])
        fig_tier.add_trace(go.Bar(
            x=tier_agg["Discount Tier"], y=tier_agg["Orders"], name="Order Volume",
            marker_color=NEUTRAL, opacity=0.5
        ), secondary_y=False)
        profit_colors = [DANGER if p < 0 else SUCCESS for p in tier_agg["Profit"]]
        fig_tier.add_trace(go.Scatter(
            x=tier_agg["Discount Tier"], y=tier_agg["Profit"], name="Total Profit",
            mode="lines+markers", line=dict(color=PRIMARY, width=3),
            marker=dict(size=12, color=profit_colors, line=dict(width=2, color="white"))
        ), secondary_y=True)
        fig_tier = chart_layout(fig_tier, height=400)
        fig_tier.update_yaxes(title_text="Number of Orders", secondary_y=False)
        fig_tier.update_yaxes(title_text="Total Profit ($)", secondary_y=True, showgrid=False)
        fig_tier.add_vrect(x0=2.5, x1=6.5, fillcolor=DANGER, opacity=0.08, layer="below", line_width=0)
        fig_tier.add_annotation(x=4.5, y=1, xref="x", yref="paper", text="⚠️ Danger Zone", showarrow=False, font=dict(color=DANGER))
        st.plotly_chart(fig_tier, use_container_width=True, config=PLOTLY_CONFIG)

    st.write("")
    st.markdown('<div class="sec-header"><div class="sec-title">✅ Recommended Actions</div></div>', unsafe_allow_html=True)

    recs = [
        {"p":"p1","label":"P1 · 30 DAYS","title":"Implement a 20% discount hard cap",
         "body":"Cap discounts system-wide. Exceptions above this level require manager-level approval.",
         "impact": fmt_currency(abs(loss_from_disc)*0.6), "effort":"Low"},
        {"p":"p2","label":"P2 · 14 DAYS","title":"Add margin tracking to weekly reporting",
         "body":"Track margin and high-discount share weekly, not monthly, to catch drift early.",
         "impact":"Visibility", "effort":"Low"},
    ]
    rcol1, rcol2 = st.columns(2)
    for i, r in enumerate(recs):
        with (rcol1 if i % 2 == 0 else rcol2):
            st.markdown(f"""
            <div class="action-card">
                <div class="action-badge {r['p']}">{r['label']}</div>
                <div class="action-title">{r['title']}</div>
                <div class="action-body">{r['body']}</div>
                <div class="action-stats">
                    <div><div class="action-stat-label">Est. Impact</div><div class="action-stat-value">{r['impact']}</div></div>
                    <div><div class="action-stat-label">Effort</div><div class="action-stat-value">{r['effort']}</div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================
# PAGE 6: CUSTOMER INSIGHTS
# ============================================================
elif menu == "👥 Customer Insights":
    st.title("Customer Insights & Lifetime Value")
    st.caption("Identify VIP accounts driving the business and problematic accounts draining resources.")

    if "Customer Name" in df.columns:
        cust_agg = df.groupby("Customer Name").agg(
            Total_Sales=("Sales","sum"), Total_Profit=("Profit","sum"),
            Order_Count=(order_col,"nunique" if "Order ID" in df.columns else "count"), 
            Avg_Discount=("Discount","mean")
        ).reset_index()

        def segment_customer(row):
            if row["Total_Profit"] < 0: return "Detractor (Loss)"
            elif row["Total_Profit"] > 1500: return "VIP (High Profit)"
            elif row["Total_Sales"] > 3000: return "High Volume / Low Margin"
            else: return "Standard"

        cust_agg["Segment"] = cust_agg.apply(segment_customer, axis=1)

        detractors = cust_agg[cust_agg["Segment"] == "Detractor (Loss)"]
        if not detractors.empty:
            st.markdown(f"""
            <div class="alert-banner alert-warning">
                <div class="alert-icon">🟡</div>
                <div class="alert-text"><b>{len(detractors)} customers</b> are net loss-making, costing {fmt_currency(abs(detractors['Total_Profit'].sum()))} combined —
                often driven by high average discounts. See the table below.</div>
            </div>
            """, unsafe_allow_html=True)
        st.write("")

        with st.container(border=True):
            st.markdown('<div class="chart-card-title">Customer Value Matrix</div>', unsafe_allow_html=True)
            st.markdown('<div class="chart-card-sub">Each dot is a customer. Upper-right is the ideal target.</div>', unsafe_allow_html=True)

            color_map = {"VIP (High Profit)": SUCCESS, "Standard": NEUTRAL,
                        "Detractor (Loss)": DANGER, "High Volume / Low Margin": WARNING}
            
            if not cust_agg.empty:
                fig_scatter = px.scatter(
                    cust_agg, x="Total_Sales", y="Total_Profit", color="Segment",
                    hover_name="Customer Name", color_discrete_map=color_map, opacity=0.7
                )
                fig_scatter = chart_layout(fig_scatter, height=440)
                fig_scatter.update_traces(marker=dict(size=8, line=dict(width=0.5, color="white")))
                fig_scatter.update_layout(xaxis_title="Lifetime Revenue ($)", yaxis_title="Lifetime Profit ($)")
                fig_scatter.add_hline(y=0, line_color="#CBD5E1", line_width=2)
                st.plotly_chart(fig_scatter, use_container_width=True, config=PLOTLY_CONFIG)

        col_t1, col_t2 = st.columns(2)
        with col_t1:
            with st.container(border=True):
                st.markdown("**💎 Top 10 Most Valuable Customers**")
                top_c = cust_agg.nlargest(10, "Total_Profit")[["Customer Name","Total_Sales","Total_Profit","Order_Count"]].copy()
                top_c["Total_Sales"] = top_c["Total_Sales"].apply(fmt_currency)
                top_c["Total_Profit"] = top_c["Total_Profit"].apply(fmt_currency)
                st.dataframe(top_c, hide_index=True, use_container_width=True)
        with col_t2:
            with st.container(border=True):
                st.markdown("**🚨 Top 10 Most Costly Customers**")
                bot_c = cust_agg.nsmallest(10, "Total_Profit")[["Customer Name","Total_Sales","Total_Profit","Avg_Discount"]].copy()
                bot_c["Total_Sales"] = bot_c["Total_Sales"].apply(fmt_currency)
                bot_c["Total_Profit"] = bot_c["Total_Profit"].apply(fmt_currency)
                bot_c["Avg_Discount"] = bot_c["Avg_Discount"].apply(lambda x: f"{x*100:.1f}%")
                st.dataframe(bot_c, hide_index=True, use_container_width=True)
    else:
        st.info("Customer Name column is missing from the dataset.")

# ============================================================
# FOOTER
# ============================================================
st.markdown(f"""
<div class="footer">
    Retail Profitability Analyzer · Dataset: Sample Superstore (Kaggle) · Built with Streamlit, Pandas & Plotly
</div>
""", unsafe_allow_html=True)
