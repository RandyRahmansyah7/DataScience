import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# ==========================================
# 1. PAGE CONFIGURATION & CUSTOM CSS
# ==========================================
st.set_page_config(
    page_title="Retail Profitability Analyzer",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. DATA LOADING & PROCESSING
# ==========================================
@st.cache_data
def load_data():
    try:
        # Mengakomodasi potensi typo nama file (Superstore vs Superstone)
        file_name = 'SampleSuperstore.csv'
        if not os.path.exists(file_name) and os.path.exists('SampleSuperstone.csv'):
            file_name = 'SampleSuperstone.csv'
            
        df = pd.read_csv(file_name, encoding='latin-1')
        
        # Standarisasi spasi pada nama kolom
        df.columns = [col.strip() for col in df.columns]
        
        # Ekstraksi fitur waktu dari Order Date
        if 'Order Date' in df.columns:
            df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed', dayfirst=False, errors='coerce')
            df['Year'] = df['Order Date'].dt.year.astype(str)
            df['Month'] = df['Order Date'].dt.month
            df['Month_Name'] = df['Order Date'].dt.strftime('%b')
            
        return df
    except Exception as e:
        st.error(f"⚠️ Gagal memuat data. Pastikan file '{file_name}' ada di direktori yang sama. Error: {e}")
        return pd.DataFrame()

df = load_data()

# Helper fungsi untuk format mata uang
def format_currency(num):
    if num >= 1_000_000:
        return f"${num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"${num/1_000:.0f}K"
    elif num <= -1_000:
        return f"-${abs(num)/1_000:.0f}K"
    else:
        return f"${num:.0f}"

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #ed8936;'>🧊 Super Store</h2>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio(
        "Navigation",
        ["🏠 Executive Dashboard", "📊 Category Deep-Dive", "🚨 Discount Trap", "👥 Customer Tier"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.caption("Settings & Export")
    csv = df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Export Data (CSV)",
        data=csv,
        file_name='Superstore_Clean_Data.csv',
        mime='text/csv',
        use_container_width=True
    )


# ==========================================
# 4. MAIN DASHBOARD CONTENT
# ==========================================

if df.empty:
    st.warning("Data tidak tersedia. Harap periksa file CSV Anda.")
    st.stop()

# ---------------------------------------------------------
# PAGE 1: EXECUTIVE DASHBOARD
# ---------------------------------------------------------
if menu == "🏠 Executive Dashboard":
    
    st.title("Executive Dashboard")
    st.caption("Overall profitability and loss analysis")

    # --- DATA CALCULATION FOR ROW 1 ---
    total_rev = df['Sales'].sum()
    total_prof = df['Profit'].sum()
    avg_margin = (total_prof / total_rev) * 100
    loss_rate = (len(df[df['Profit'] < 0]) / len(df)) * 100
    
    rev_yoy_str, prof_yoy_str = "N/A", "N/A"
    if 'Year' in df.columns:
        years = sorted(df['Year'].dropna().unique())
        if len(years) >= 2:
            latest_yr = years[-1]
            prev_yr = years[-2]
            
            rev_latest = df[df['Year'] == latest_yr]['Sales'].sum()
            rev_prev = df[df['Year'] == prev_yr]['Sales'].sum()
            prof_latest = df[df['Year'] == latest_yr]['Profit'].sum()
            prof_prev = df[df['Year'] == prev_yr]['Profit'].sum()
            
            rev_yoy = ((rev_latest - rev_prev) / rev_prev) * 100 if rev_prev else 0
            prof_yoy = ((prof_latest - prof_prev) / prof_prev) * 100 if prof_prev else 0
            
            rev_yoy_str = f"{rev_yoy:+.1f}% YoY"
            prof_yoy_str = f"{prof_yoy:+.1f}% YoY"

    # --- ROW 1: TOP KPI CARDS ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", format_currency(total_rev), rev_yoy_str)
    col2.metric("Total Profit", format_currency(total_prof), prof_yoy_str)
    col3.metric("Avg Profit Margin", f"{avg_margin:.1f}%", "-Needs Improvement" if avg_margin < 15 else "+Healthy Margin")
    col4.metric("Loss Rate", f"{loss_rate:.1f}%", "Of total transactions", delta_color="off")

    st.divider()

    # --- ROW 2: MIDDLE CHARTS ---
    col_mid1, col_mid2, col_mid3 = st.columns([1, 1.5, 1])
    
    with col_mid1:
        st.subheader("Profit by Category")
        cat_profit = df.groupby('Category')['Profit'].sum().reset_index()
        cat_profit = cat_profit.sort_values('Profit', ascending=False)
        
        fig_donut = go.Figure(data=[go.Pie(
            labels=cat_profit['Category'], values=cat_profit['Profit'], hole=0.7,
            marker_colors=['#38b2ac', '#81e6d9', '#e2e8f0']
        )])
        fig_donut.update_layout(
            showlegend=False, margin=dict(t=20, b=20, l=20, r=20), height=300,
            annotations=[dict(text=format_currency(total_prof), x=0.5, y=0.5, font_size=24, font_weight='bold', showarrow=False)]
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_mid2:
        st.subheader("Revenue vs Profit")
        if 'Year' in df.columns:
            yearly = df.groupby('Year')[['Sales', 'Profit']].sum().reset_index()
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(x=yearly['Year'], y=yearly['Sales'], mode='lines+markers', name='Revenue',
                                          line=dict(color='#cbd5e1', width=2, dash='dash')))
            fig_line.add_trace(go.Scatter(x=yearly['Year'], y=yearly['Profit'], mode='lines+markers', name='Profit',
                                          line=dict(color='#38b2ac', width=3)))
            fig_line.update_layout(
                margin=dict(t=30, b=20, l=10, r=10), height=300, showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.warning("Data trend tahunan tidak dapat ditampilkan.")

    with col_mid3:
        st.subheader("Profit Leaks (Causes)")
        loss_df = df[df['Profit'] < 0]
        total_losses = len(loss_df)
        
        if total_losses > 0:
            high_disc_loss = len(loss_df[loss_df['Discount'] >= 0.3])
            furn_loss = len(loss_df[loss_df['Category'] == 'Furniture'])
            low_sales_loss = len(loss_df[loss_df['Sales'] < 50])

            st.write("**High Discount (>= 30%)**")
            st.progress(high_disc_loss / total_losses, text=f"{(high_disc_loss / total_losses)*100:.0f}% of Leaks")
            st.write("**Furniture Category**")
            st.progress(furn_loss / total_losses, text=f"{(furn_loss / total_losses)*100:.0f}% of Leaks")
            st.write("**Low Value Sales (< $50)**")
            st.progress(low_sales_loss / total_losses, text=f"{(low_sales_loss / total_losses)*100:.0f}% of Leaks")
        else:
            st.success("Tidak ada kerugian terdeteksi!")

    st.divider()

    # --- ROW 3: BOTTOM CHARTS ---
    col_bot1, col_bot2 = st.columns([1, 2.5])

    with col_bot1:
        st.subheader("Category Margins")
        cat_summary = df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
        cat_summary['Margin'] = (cat_summary['Profit'] / cat_summary['Sales']) * 100
        cat_summary = cat_summary.sort_values('Margin', ascending=False)
        
        df_margin_display = pd.DataFrame({
            "Category": cat_summary['Category'],
            "Revenue": cat_summary['Sales'].apply(format_currency),
            "Margin": cat_summary['Margin'].apply(lambda x: f"{x:.1f}%")
        })
        st.dataframe(df_margin_display, hide_index=True, use_container_width=True)

    with col_bot2:
        st.subheader("Seasonality (Margin vs Discount)")
        if 'Month' in df.columns:
            monthly = df.groupby(['Month', 'Month_Name']).apply(
                lambda x: pd.Series({'Sales': x['Sales'].sum(), 'Profit': x['Profit'].sum(), 'Avg_Discount': x['Discount'].mean() * 100})
            ).reset_index()
            monthly['Avg_Margin'] = (monthly['Profit'] / monthly['Sales']) * 100
            monthly = monthly.sort_values('Month')
            
            fig_area = go.Figure()
            fig_area.add_trace(go.Scatter(x=monthly['Month_Name'], y=monthly['Avg_Margin'], fill='tozeroy', mode='lines', name='Avg Margin (%)', line=dict(color='#38b2ac', width=2)))
            fig_area.add_trace(go.Scatter(x=monthly['Month_Name'], y=monthly['Avg_Discount'], mode='lines+markers', name='Avg Discount (%)', line=dict(color='#ed8936', width=2)))
            fig_area.update_layout(margin=dict(t=20, b=20, l=10, r=10), height=300, showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_area, use_container_width=True)
        else:
             st.warning("Data trend bulanan tidak dapat ditampilkan.")


# ---------------------------------------------------------
# PAGE 2: CATEGORY DEEP-DIVE
# ---------------------------------------------------------
elif menu == "📊 Category Deep-Dive":
    
    st.title("Category & Sub-Category Analysis")
    st.caption("Uncovering the illusion of high revenue in underperforming categories")
    
    # Kalkulasi summary data kategori
    cat_df = df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    cat_df['Margin'] = (cat_df['Profit'] / cat_df['Sales']) * 100
    
    # --- ROW 1: CATEGORY REVENUE VS PROFIT ---
    st.subheader("Revenue vs Profit by Category")
    
    fig_cat = go.Figure()
    fig_cat.add_trace(go.Bar(
        x=cat_df['Category'], y=cat_df['Sales'], 
        name='Revenue', marker_color='#cbd5e1', 
        text=cat_df['Sales'].apply(format_currency), textposition='auto'
    ))
    fig_cat.add_trace(go.Bar(
        x=cat_df['Category'], y=cat_df['Profit'], 
        name='Profit', marker_color='#38b2ac',
        text=cat_df['Profit'].apply(format_currency), textposition='auto'
    ))
    
    fig_cat.update_layout(
        barmode='group', margin=dict(t=30, b=20, l=10, r=10), height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_title="", yaxis_title="USD ($)"
    )
    st.plotly_chart(fig_cat, use_container_width=True)
    
    st.divider()
    
    # --- ROW 2: PROFIT MARGIN GAUGE ---
    st.subheader("Profit Margin Health")
    st.caption("Target benchmark is set at 12.5% (Overall Average)")
    
    col_g1, col_g2, col_g3 = st.columns(3)
    
    def create_gauge(val, title):
        # Logika warna: Hijau (>=12.5), Kuning (0-12.5), Merah (<0)
        color = "#38b2ac" if val >= 12.5 else "#ed8936" if val >= 0 else "#e53e3e"
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=val,
            number={'suffix': "%", 'font': {'size': 30, 'color': color}},
            title={'text': title, 'font': {'size': 18, 'color': '#334155'}},
            gauge={
                'axis': {'range': [-10, 25], 'tickwidth': 1, 'tickcolor': "#cbd5e1"},
                'bar': {'color': color},
                'bgcolor': "white",
                'borderwidth': 0,
                'steps': [
                    {'range': [-10, 0], 'color': '#fee2e2'},     # Merah muda
                    {'range': [0, 12.5], 'color': '#ffedd5'},    # Oranye muda
                    {'range': [12.5, 25], 'color': '#ccfbf1'}    # Hijau toska muda
                ],
                'threshold': {
                    'line': {'color': "#475569", 'width': 3}, 
                    'thickness': 0.75, 
                    'value': 12.5
                }
            }
        ))
        fig.update_layout(height=280, margin=dict(t=50, b=20, l=20, r=20))
        return fig
    
    with col_g1:
        tech_margin = cat_df[cat_df['Category'] == 'Technology']['Margin'].values[0]
        st.plotly_chart(create_gauge(tech_margin, "Technology"), use_container_width=True)
        
    with col_g2:
        office_margin = cat_df[cat_df['Category'] == 'Office Supplies']['Margin'].values[0]
        st.plotly_chart(create_gauge(office_margin, "Office Supplies"), use_container_width=True)
        
    with col_g3:
        furn_margin = cat_df[cat_df['Category'] == 'Furniture']['Margin'].values[0]
        st.plotly_chart(create_gauge(furn_margin, "Furniture"), use_container_width=True)
        
    st.divider()
    
    # --- ROW 3: SUB-CATEGORY WINNERS & LOSERS ---
    st.subheader("Sub-Category Performance (The Winners & Losers)")
    
    subcat_df = df.groupby('Sub-Category')[['Sales', 'Profit']].sum().reset_index()
    top_5 = subcat_df.sort_values('Profit', ascending=False).head(5)
    bottom_5 = subcat_df.sort_values('Profit', ascending=True).head(5)
    
    col_sub1, col_sub2 = st.columns(2)
    
    with col_sub1:
        st.markdown("**🏆 Top 5 Most Profitable**")
        fig_top = go.Figure(go.Bar(
            x=top_5['Profit'], y=top_5['Sub-Category'], 
            orientation='h', marker_color='#38b2ac',
            text=top_5['Profit'].apply(format_currency), textposition='inside'
        ))
        fig_top.update_layout(
            yaxis={'categoryorder':'total ascending'}, margin=dict(t=10, b=10, l=10, r=10), height=300,
            xaxis_visible=False
        )
        st.plotly_chart(fig_top, use_container_width=True)
        
    with col_sub2:
        st.markdown("**🚨 Bottom 5 Least Profitable (Loss Makers)**")
        fig_bot = go.Figure(go.Bar(
            x=bottom_5['Profit'], y=bottom_5['Sub-Category'], 
            orientation='h', marker_color='#e53e3e',
            text=bottom_5['Profit'].apply(format_currency), textposition='inside'
        ))
        fig_bot.update_layout(
            yaxis={'categoryorder':'total descending'}, margin=dict(t=10, b=10, l=10, r=10), height=300,
            xaxis_visible=False
        )
        st.plotly_chart(fig_bot, use_container_width=True)


# ---------------------------------------------------------
# PAGE 3: DISCOUNT TRAP
# ---------------------------------------------------------
elif menu == "🚨 Discount Trap":
    st.title("The Discount Trap")
    st.caption("Investigating how excessive discounts are destroying profit margins")

    # Data Prep: Membuat Discount Buckets
    bins = [-0.01, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0]
    labels = ['0%', '1-10%', '11-20%', '21-30%', '31-40%', '41-50%', '>50%']
    df['Discount_Bucket'] = pd.cut(df['Discount'], bins=bins, labels=labels)

    # --- ROW 1: DISCOUNT KPIs ---
    high_disc_df = df[df['Discount'] > 0.2]
    extreme_disc_df = df[df['Discount'] >= 0.5]

    total_loss_high = high_disc_df[high_disc_df['Profit'] < 0]['Profit'].sum()
    total_loss_extreme = extreme_disc_df[extreme_disc_df['Profit'] < 0]['Profit'].sum()

    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    col_kpi1.metric("Transactions >20% Discount", f"{len(high_disc_df):,}", "High Risk Zone", delta_color="off")
    col_kpi2.metric("Profit Lost (>20% Disc)", format_currency(total_loss_high), "-Immediate Leak", delta_color="inverse")
    col_kpi3.metric("Profit Lost (>=50% Disc)", format_currency(total_loss_extreme), f"{len(extreme_disc_df)} Transactions", delta_color="inverse")

    st.divider()

    # --- ROW 2: PROFIT & VOLUME BY BUCKET ---
    st.subheader("Profitability & Volume by Discount Tier")
    col_d1, col_d2 = st.columns(2)

    disc_summary = df.groupby('Discount_Bucket', observed=False).agg({'Profit': 'sum', 'Sales': 'count'}).reset_index()
    disc_summary.rename(columns={'Sales': 'Transactions'}, inplace=True)

    with col_d1:
        # Bar chart for Profit
        colors = ['#e53e3e' if p < 0 else '#38b2ac' for p in disc_summary['Profit']]
        fig_disc_prof = go.Figure(go.Bar(
            x=disc_summary['Discount_Bucket'],
            y=disc_summary['Profit'],
            marker_color=colors,
            text=disc_summary['Profit'].apply(format_currency),
            textposition='auto'
        ))
        fig_disc_prof.update_layout(
            title="Total Profit Impact",
            margin=dict(t=40, b=10, l=10, r=10),
            height=350,
            xaxis_title="Discount Level Applied",
            yaxis_title="Total Profit ($)"
        )
        # Add visual threshold line
        fig_disc_prof.add_vline(x=2.5, line_width=2, line_dash="dash", line_color="#475569", annotation_text=" Danger Zone (>20%)")
        st.plotly_chart(fig_disc_prof, use_container_width=True)

    with col_d2:
        # Bar chart for Volume
        fig_disc_vol = go.Figure(go.Bar(
            x=disc_summary['Discount_Bucket'],
            y=disc_summary['Transactions'],
            marker_color='#cbd5e1',
            text=disc_summary['Transactions'],
            textposition='auto'
        ))
        fig_disc_vol.update_layout(
            title="Number of Transactions",
            margin=dict(t=40, b=10, l=10, r=10),
            height=350,
            xaxis_title="Discount Level Applied",
            yaxis_title="Number of Orders"
        )
        st.plotly_chart(fig_disc_vol, use_container_width=True)

    st.divider()

    # --- ROW 3: SCATTER PLOT ---
    st.subheader("Correlation: Profit vs Discount by Category")
    st.caption("Every dot represents a transaction. Notice how profits crash below zero as the discount passes 20%.")
    
    fig_scatter = go.Figure()
    colors_cat = {'Technology': '#38b2ac', 'Office Supplies': '#81e6d9', 'Furniture': '#ed8936'}

    for cat in df['Category'].unique():
        cat_data = df[df['Category'] == cat]
        fig_scatter.add_trace(go.Scatter(
            x=cat_data['Discount'],
            y=cat_data['Profit'],
            mode='markers',
            name=cat,
            marker=dict(color=colors_cat.get(cat, '#cbd5e1'), size=6, opacity=0.6)
        ))

    fig_scatter.update_layout(
        xaxis_title="Discount Rate",
        yaxis_title="Profit Generated ($)",
        height=450,
        margin=dict(t=20, b=20, l=10, r=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Add Break-even (Zero Profit) line
    fig_scatter.add_hline(y=0, line_width=2, line_dash="solid", line_color="#e53e3e")
    
    # Add 20% discount vertical limit line
    fig_scatter.add_vline(x=0.2, line_width=2, line_dash="dash", line_color="#475569", annotation_text=" Recommended Max Discount (20%) ")

    st.plotly_chart(fig_scatter, use_container_width=True)

# ---------------------------------------------------------
# PAGE 4: CUSTOMER TIER
# ---------------------------------------------------------
elif menu == "👥 Customer Tier":
    st.title("Customer Tier & Profitability")
    st.caption("Segmenting customers to identify top contributors and major loss-makers")

    # Data Prep: Agregasi level Customer
    cust_df = df.groupby('Customer Name').agg({
        'Sales': 'sum', 
        'Profit': 'sum', 
        'Discount': 'mean',
        'Order ID': 'nunique'
    }).reset_index()
    cust_df.rename(columns={'Order ID': 'Total_Orders'}, inplace=True)
    
    # Membuat segmentasi/Tier
    def assign_tier(profit):
        if profit < 0:
            return 'Loss Maker'
        elif profit >= 1000:
            return 'VIP'
        else:
            return 'Standard'
            
    cust_df['Tier'] = cust_df['Profit'].apply(assign_tier)
    
    # --- ROW 1: CUSTOMER KPIs ---
    total_cust = len(cust_df)
    vip_df = cust_df[cust_df['Tier'] == 'VIP']
    loss_df = cust_df[cust_df['Tier'] == 'Loss Maker']
    
    vip_profit = vip_df['Profit'].sum()
    loss_leak = loss_df['Profit'].sum()

    col_c1, col_c2, col_c3 = st.columns(3)
    col_c1.metric("Total Unique Customers", f"{total_cust:,}", "Active Accounts", delta_color="off")
    col_c2.metric("VIP Customers", f"{len(vip_df):,}", f"Generating {format_currency(vip_profit)}", delta_color="normal")
    col_c3.metric("Loss-Making Customers", f"{len(loss_df):,}", f"Draining {format_currency(abs(loss_leak))}", delta_color="inverse")

    st.divider()

    # --- ROW 2: SCATTER PLOT & PIE CHART ---
    col_cht1, col_cht2 = st.columns([2, 1])

    with col_cht1:
        st.subheader("Customer Value Matrix (Sales vs Profit)")
        
        fig_cust_scatter = go.Figure()
        
        # Mapping warna
        tier_colors = {'VIP': '#38b2ac', 'Standard': '#cbd5e1', 'Loss Maker': '#e53e3e'}
        
        for tier in ['VIP', 'Standard', 'Loss Maker']:
            t_data = cust_df[cust_df['Tier'] == tier]
            fig_cust_scatter.add_trace(go.Scatter(
                x=t_data['Sales'],
                y=t_data['Profit'],
                mode='markers',
                name=tier,
                text=t_data['Customer Name'], # Hover text
                hovertemplate="<b>%{text}</b><br>Sales: $%{x:,.2f}<br>Profit: $%{y:,.2f}<extra></extra>",
                marker=dict(color=tier_colors[tier], size=8, opacity=0.7)
            ))

        fig_cust_scatter.update_layout(
            xaxis_title="Total Lifetime Sales ($)",
            yaxis_title="Total Lifetime Profit ($)",
            height=400,
            margin=dict(t=10, b=20, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        # Garis batas impas (Break-even)
        fig_cust_scatter.add_hline(y=0, line_width=1, line_dash="solid", line_color="#475569")
        st.plotly_chart(fig_cust_scatter, use_container_width=True)

    with col_cht2:
        st.subheader("Tier Distribution")
        
        tier_counts = cust_df['Tier'].value_counts().reset_index()
        tier_counts.columns = ['Tier', 'Count']
        
        fig_tier_pie = go.Figure(data=[go.Pie(
            labels=tier_counts['Tier'], 
            values=tier_counts['Count'],
            hole=0.5,
            marker_colors=[tier_colors[t] for t in tier_counts['Tier']]
        )])
        fig_tier_pie.update_layout(
            showlegend=True, 
            margin=dict(t=20, b=20, l=10, r=10), 
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_tier_pie, use_container_width=True)

    st.divider()

    # --- ROW 3: TOP & BOTTOM CUSTOMERS TABLE ---
    col_tbl1, col_tbl2 = st.columns(2)

    with col_tbl1:
        st.markdown("**👑 Top 10 Most Valuable Customers**")
        top_10 = cust_df.nlargest(10, 'Profit')[['Customer Name', 'Sales', 'Profit', 'Total_Orders']]
        
        # Format agar rapi di tabel
        top_10['Sales'] = top_10['Sales'].apply(lambda x: f"${x:,.0f}")
        top_10['Profit'] = top_10['Profit'].apply(lambda x: f"${x:,.0f}")
        st.dataframe(top_10, hide_index=True, use_container_width=True)

    with col_tbl2:
        st.markdown("**🚨 Top 10 Worst Customers (Highest Losses)**")
        
        # PERBAIKAN: Ambil kolom 'Discount' bawaan dataframe terlebih dahulu
        bot_10 = cust_df.nsmallest(10, 'Profit')[['Customer Name', 'Sales', 'Profit', 'Discount']].copy()
        
        # Ganti nama kolom untuk tampilan
        bot_10.rename(columns={'Discount': 'Avg Discount (%)'}, inplace=True)
        
        # Format agar rapi di tabel
        bot_10['Sales'] = bot_10['Sales'].apply(lambda x: f"${x:,.0f}")
        bot_10['Profit'] = bot_10['Profit'].apply(lambda x: f"-${abs(x):,.0f}")
        # Kalikan dengan 100 dan tambahkan lambang %
        bot_10['Avg Discount (%)'] = bot_10['Avg Discount (%)'].apply(lambda x: f"{x * 100:.1f}%")
        
        st.dataframe(bot_10, hide_index=True, use_container_width=True)
