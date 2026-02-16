import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="E-commerce Intelligence Hub",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  PREMIUM CSS  ── Cyber Dark + Neon Gradient
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

.main {
    background: radial-gradient(ellipse at 20% 0%, #0d1b2a 0%, #0a0f1e 60%, #050811 100%);
    color: #e2e8f0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2a 0%, #071120 100%);
    border-right: 1px solid rgba(0, 240, 255, 0.12);
}
section[data-testid="stSidebar"] * {
    font-family: 'DM Mono', monospace !important;
    color: #94a3b8;
}
section[data-testid="stSidebar"] h1, 
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #00f0ff !important;
    letter-spacing: 0.05em;
}

/* ── Metric Cards ── */
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(0,240,255,0.06) 0%, rgba(139,92,246,0.08) 100%);
    padding: 22px 26px;
    border-radius: 16px;
    border: 1px solid rgba(0,240,255,0.18);
    box-shadow: 0 4px 30px rgba(0,0,0,0.4), inset 0 1px 0 rgba(255,255,255,0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}
div[data-testid="stMetric"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 2px;
    background: linear-gradient(90deg, #00f0ff, #8b5cf6, #ff4ecd);
}
div[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 40px rgba(0,240,255,0.15), inset 0 1px 0 rgba(255,255,255,0.05);
}
div[data-testid="metric-container"] label {
    color: #64748b !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e2e8f0 !important;
    font-size: 2rem !important;
    font-weight: 800;
    letter-spacing: -0.02em;
}
div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
}

/* ── Tab bar ── */
div[data-testid="stTabs"] button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 600;
    letter-spacing: 0.04em;
    color: #475569 !important;
    border-radius: 8px 8px 0 0;
    padding: 10px 20px !important;
    transition: color 0.2s;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #00f0ff !important;
    border-bottom: 2px solid #00f0ff !important;
    background: rgba(0,240,255,0.05) !important;
}

/* ── Title ── */
.dashboard-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(90deg, #00f0ff 0%, #8b5cf6 50%, #ff4ecd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.03em;
    margin-bottom: 4px;
}
.dashboard-sub {
    font-family: 'DM Mono', monospace;
    color: #475569;
    font-size: 13px;
    letter-spacing: 0.08em;
    margin-bottom: 24px;
}

/* ── Section headers ── */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 14px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #475569;
    margin: 20px 0 12px 2px;
}

/* ── Chart container ── */
.chart-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 4px;
}

/* ── Selectbox / Multiselect ── */
div[data-testid="stSelectbox"] > div,
div[data-testid="stMultiSelect"] > div {
    background: rgba(0,240,255,0.04) !important;
    border-color: rgba(0,240,255,0.2) !important;
}

/* ── Download button ── */
div[data-testid="stDownloadButton"] button {
    background: linear-gradient(135deg, #00f0ff, #8b5cf6) !important;
    color: #0a0f1e !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-family: 'Syne', sans-serif !important;
    width: 100%;
}

/* ── Divider ── */
hr {
    border-color: rgba(0,240,255,0.08) !important;
    margin: 28px 0 !important;
}

/* ── Caption ── */
.stCaption {
    font-family: 'DM Mono', monospace;
    color: #334155 !important;
    font-size: 11px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PLOTLY THEME  (shared layout defaults)
# ─────────────────────────────────────────────
CHART_BG       = "rgba(0,0,0,0)"
PAPER_BG       = "rgba(0,0,0,0)"
GRID_COLOR     = "rgba(255,255,255,0.05)"
FONT_COLOR     = "#94a3b8"
TITLE_FONT     = dict(family="Syne", size=15, color="#e2e8f0")
AXIS_FONT      = dict(family="DM Mono, monospace", size=11, color="#64748b")

ACCENT_CYAN    = "#00f0ff"
ACCENT_PURPLE  = "#8b5cf6"
ACCENT_PINK    = "#ff4ecd"
ACCENT_AMBER   = "#f59e0b"
ACCENT_GREEN   = "#10b981"
ACCENT_RED     = "#f43f5e"

PALETTE_NEON   = [ACCENT_CYAN, ACCENT_PURPLE, ACCENT_PINK, ACCENT_AMBER, ACCENT_GREEN, ACCENT_RED,
                  "#3b82f6", "#f97316", "#a3e635"]

def base_layout(title="", height=380):
    return dict(
        title=dict(text=title, font=TITLE_FONT, x=0.01, xanchor="left"),
        template="plotly_dark",
        plot_bgcolor=CHART_BG,
        paper_bgcolor=PAPER_BG,
        font=dict(family="Syne, sans-serif", color=FONT_COLOR),
        height=height,
        margin=dict(l=16, r=16, t=48, b=16),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=AXIS_FONT,
                   linecolor=GRID_COLOR),
        yaxis=dict(showgrid=True, gridcolor=GRID_COLOR, zeroline=False,
                   tickfont=AXIS_FONT, linecolor=GRID_COLOR),
        hoverlabel=dict(bgcolor="#1e293b", font_family="DM Mono",
                        font_size=12, bordercolor="rgba(0,240,255,0.4)"),
    )

# ─────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("data/events.csv")
    df['event_time'] = pd.to_datetime(df['event_time'])
    df['date']       = df['event_time'].dt.date
    df['hour']       = df['event_time'].dt.hour
    df['weekday']    = df['event_time'].dt.day_name()
    df['week']       = df['event_time'].dt.isocalendar().week.astype(int)
    return df

df = load_data()

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.markdown("## ⚡ Control Panel")
st.sidebar.markdown("---")

selected_date = st.sidebar.selectbox(
    "📅 Date",
    sorted(df['date'].unique())
)

event_filter = st.sidebar.multiselect(
    "🎯 Event Types",
    df['event_type'].unique(),
    default=df['event_type'].unique()
)

if 'price' in df.columns:
    price_vals = df['price'].dropna()
    price_range = st.sidebar.slider(
        "💰 Price Range",
        float(price_vals.min()), float(price_vals.max()),
        (float(price_vals.min()), float(price_vals.max()))
    )
else:
    price_range = (0, 1e9)

st.sidebar.markdown("---")

filtered_df = df[
    (df['date'] == selected_date) &
    (df['event_type'].isin(event_filter)) &
    (df['price'].between(price_range[0], price_range[1]) if 'price' in df.columns else True)
]

st.sidebar.metric("Filtered Records", f"{len(filtered_df):,}")

st.sidebar.download_button(
    "⬇ Download Filtered CSV",
    filtered_df.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)

# ─────────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────────
st.markdown('<div class="dashboard-title">⚡ E-commerce Intelligence Hub</div>', unsafe_allow_html=True)
st.markdown(f'<div class="dashboard-sub">REPORTING DATE : {selected_date} &nbsp;·&nbsp; {len(filtered_df):,} EVENTS LOADED</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  KPIs  (8 cards)
# ─────────────────────────────────────────────
st.markdown('<div class="section-header">Core KPIs</div>', unsafe_allow_html=True)

purchases_df  = filtered_df[filtered_df['event_type'] == 'purchase']
views_df      = filtered_df[filtered_df['event_type'] == 'view']
cart_df       = filtered_df[filtered_df['event_type'] == 'cart']
total_visits  = len(filtered_df)
total_purch   = len(purchases_df)
total_revenue = purchases_df['price'].sum() if 'price' in purchases_df.columns else 0
conv_rate     = (total_purch / len(views_df) * 100) if len(views_df) > 0 else 0
avg_order     = (total_revenue / total_purch) if total_purch > 0 else 0
cart_rate     = (len(cart_df) / len(views_df) * 100) if len(views_df) > 0 else 0
unique_users  = filtered_df['user_id'].nunique() if 'user_id' in filtered_df.columns else 0
unique_prods  = purchases_df['product_id'].nunique() if 'product_id' in purchases_df.columns else 0

k1, k2, k3, k4, k5, k6, k7, k8 = st.columns(8)
k1.metric("👀 Views",         f"{len(views_df):,}")
k2.metric("🛒 Cart Adds",     f"{len(cart_df):,}")
k3.metric("✅ Purchases",      f"{total_purch:,}")
k4.metric("💰 Revenue",       f"₹{total_revenue:,.0f}")
k5.metric("📈 Conv. Rate",    f"{conv_rate:.1f}%")
k6.metric("🎯 Avg. Order",    f"₹{avg_order:,.0f}")
k7.metric("👥 Unique Users",  f"{unique_users:,}")
k8.metric("📦 Products Sold", f"{unique_prods:,}")

st.markdown("---")

# ─────────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Traffic & Behavior",
    "💰 Revenue Deep Dive",
    "🔥 Funnel & Conversion",
    "📊 Product Intelligence",
    "🗺  Heatmap & Clusters"
])

# ══════════════════════════════════════════════
#  TAB 1 – TRAFFIC & BEHAVIOR
# ══════════════════════════════════════════════
with tab1:
    r1c1, r1c2 = st.columns(2)

    # Spline area – hourly traffic
    with r1c1:
        hourly = filtered_df.groupby(['hour','event_type']).size().reset_index(name='count')
        fig = px.area(hourly, x='hour', y='count', color='event_type',
                      line_shape='spline',
                      color_discrete_sequence=PALETTE_NEON)
        fig.update_layout(**base_layout("Hourly Traffic by Event Type"))
        fig.update_traces(line_width=2)
        st.plotly_chart(fig, use_container_width=True)

    # Donut – event share
    with r1c2:
        ev = filtered_df['event_type'].value_counts().reset_index()
        ev.columns = ['type','count']
        fig2 = px.pie(ev, names='type', values='count', hole=0.55,
                      color_discrete_sequence=PALETTE_NEON)
        fig2.update_traces(textfont_family="DM Mono",
                           marker=dict(line=dict(color="#0a0f1e", width=2)))
        fig2.update_layout(**base_layout("Event Share Distribution"))
        fig2.update_layout(legend=dict(font=dict(family="DM Mono", size=11, color="#94a3b8")))
        st.plotly_chart(fig2, use_container_width=True)

    r2c1, r2c2 = st.columns(2)

    # Clustered / grouped bar – events per hour (compare types side-by-side)
    with r2c1:
        grp = filtered_df.groupby(['hour','event_type']).size().reset_index(name='count')
        fig3 = px.bar(grp, x='hour', y='count', color='event_type', barmode='group',
                      color_discrete_sequence=PALETTE_NEON)
        fig3.update_layout(**base_layout("Clustered: Events Per Hour (by Type)"))
        fig3.update_traces(marker_line_width=0)
        st.plotly_chart(fig3, use_container_width=True)

    # Scatter – session activity (random jitter for exploration feel)
    with r2c2:
        scatter_df = filtered_df.copy()
        scatter_df['jitter'] = np.random.uniform(0, 1, len(scatter_df))
        fig4 = px.scatter(scatter_df.sample(min(3000, len(scatter_df))),
                          x='hour', y='jitter',
                          color='event_type',
                          color_discrete_sequence=PALETTE_NEON,
                          opacity=0.45, size_max=5)
        fig4.update_layout(**base_layout("Activity Scatter (Hourly Distribution)"))
        fig4.update_layout(yaxis=dict(showticklabels=False, title=""),
                           xaxis_title="Hour of Day")
        st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════
#  TAB 2 – REVENUE DEEP DIVE
# ══════════════════════════════════════════════
with tab2:
    r1c1, r1c2 = st.columns(2)

    # Gradient bar – revenue by hour
    with r1c1:
        rev_h = purchases_df.groupby('hour')['price'].sum().reset_index()
        fig = go.Figure(go.Bar(
            x=rev_h['hour'], y=rev_h['price'],
            marker=dict(
                color=rev_h['price'],
                colorscale=[[0,"#0d1b2a"],[0.3,"#00f0ff"],[0.7,"#8b5cf6"],[1,"#ff4ecd"]],
                line_width=0
            )
        ))
        fig.update_layout(**base_layout("Revenue by Hour of Day"))
        st.plotly_chart(fig, use_container_width=True)

    # Box plot – price distribution by event type
    with r1c2:
        fig2 = px.box(filtered_df, x='event_type', y='price',
                      color='event_type',
                      color_discrete_sequence=PALETTE_NEON,
                      points="outliers")
        fig2.update_traces(boxmean='sd', marker_size=4)
        fig2.update_layout(**base_layout("Price Distribution by Event Type"))
        st.plotly_chart(fig2, use_container_width=True)

    r2c1, r2c2 = st.columns(2)

    # Waterfall – cumulative revenue by hour
    with r2c1:
        rev_h2 = purchases_df.groupby('hour')['price'].sum().reset_index()
        measures = ['relative'] * len(rev_h2)
        fig3 = go.Figure(go.Waterfall(
            x=[f"{h:02d}:00" for h in rev_h2['hour']],
            y=rev_h2['price'],
            measure=measures,
            connector=dict(line=dict(color=GRID_COLOR)),
            increasing=dict(marker=dict(color=ACCENT_CYAN)),
            decreasing=dict(marker=dict(color=ACCENT_RED)),
            totals=dict(marker=dict(color=ACCENT_PURPLE))
        ))
        fig3.update_layout(**base_layout("Cumulative Revenue Waterfall"))
        st.plotly_chart(fig3, use_container_width=True)

    # Violin – purchase price spread
    with r2c2:
        fig4 = px.violin(purchases_df, y='price',
                         box=True, points="outliers",
                         color_discrete_sequence=[ACCENT_CYAN])
        fig4.update_layout(**base_layout("Purchase Price Violin"))
        st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════
#  TAB 3 – FUNNEL & CONVERSION
# ══════════════════════════════════════════════
with tab3:
    f1, f2 = st.columns([1, 1])

    # Funnel chart
    with f1:
        v  = len(filtered_df[filtered_df['event_type'] == 'view'])
        c  = len(filtered_df[filtered_df['event_type'] == 'cart'])
        p  = len(filtered_df[filtered_df['event_type'] == 'purchase'])
        fig = go.Figure(go.Funnel(
            y=["Product Views", "Add to Cart", "Purchases"],
            x=[v, c, p],
            textposition="inside",
            textinfo="value+percent initial",
            textfont=dict(family="DM Mono", size=13, color="#e2e8f0"),
            marker=dict(
                color=[ACCENT_CYAN, ACCENT_PURPLE, ACCENT_GREEN],
                line=dict(width=2, color="#0a0f1e")
            ),
            connector=dict(fillcolor="rgba(0,240,255,0.06)")
        ))
        fig.update_layout(**base_layout("Conversion Funnel", height=420))
        st.plotly_chart(fig, use_container_width=True)

    # Gauge – conversion rate
    with f2:
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=round(conv_rate, 2),
            delta={'reference': 5, 'increasing': {'color': ACCENT_GREEN},
                   'decreasing': {'color': ACCENT_RED}},
            title={'text': "Conversion Rate (%)", 'font': TITLE_FONT},
            gauge={
                'axis': {'range': [0, 20], 'tickfont': AXIS_FONT,
                         'tickcolor': GRID_COLOR, 'tickwidth': 1},
                'bar':  {'color': ACCENT_CYAN, 'thickness': 0.25},
                'bgcolor': "rgba(0,0,0,0)",
                'bordercolor': GRID_COLOR,
                'steps': [
                    {'range': [0, 5],  'color': 'rgba(244,63,94,0.15)'},
                    {'range': [5, 10], 'color': 'rgba(245,158,11,0.15)'},
                    {'range': [10, 20],'color': 'rgba(16,185,129,0.15)'},
                ],
                'threshold': {
                    'line': {'color': ACCENT_PINK, 'width': 3},
                    'thickness': 0.7,
                    'value': 10
                }
            },
            number={'font': {'family': 'Syne', 'size': 60, 'color': '#e2e8f0'},
                    'suffix': '%'}
        ))
        fig2.update_layout(
            paper_bgcolor=PAPER_BG,
            plot_bgcolor=CHART_BG,
            height=420,
            margin=dict(l=20, r=20, t=60, b=20),
            font=dict(color=FONT_COLOR)
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Stacked bar – hourly funnel view
    funnel_hourly = filtered_df.groupby(['hour','event_type']).size().reset_index(name='count')
    fig3 = px.bar(funnel_hourly, x='hour', y='count', color='event_type',
                  barmode='stack',
                  color_discrete_sequence=PALETTE_NEON)
    fig3.update_traces(marker_line_width=0)
    fig3.update_layout(**base_layout("Stacked Funnel Steps by Hour", height=320))
    st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════
#  TAB 4 – PRODUCT INTELLIGENCE
# ══════════════════════════════════════════════
with tab4:
    r1c1, r1c2 = st.columns(2)

    # Horizontal bar – top 10 products by purchases
    with r1c1:
        top_p = (purchases_df.groupby('product_id').size()
                 .sort_values(ascending=False).head(10).reset_index(name='count'))
        fig = px.bar(top_p, x='count', y='product_id', orientation='h',
                     color='count',
                     color_continuous_scale=[[0,"#0d1b2a"],[0.5,"#00f0ff"],[1,"#8b5cf6"]])
        fig.update_layout(**base_layout("Top 10 Products by Purchase Volume"))
        fig.update_layout(yaxis=dict(categoryorder='total ascending'))
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(fig, use_container_width=True)

    # Treemap – product revenue contribution
    with r1c2:
        if 'price' in purchases_df.columns and 'category_code' in purchases_df.columns:
            tree_df = purchases_df.groupby(['category_code','product_id'])['price'].sum().reset_index()
            fig2 = px.treemap(tree_df.head(80),
                              path=['category_code','product_id'], values='price',
                              color='price',
                              color_continuous_scale=[[0,"#141e30"],[0.5,"#8b5cf6"],[1,"#00f0ff"]])
        elif 'product_id' in purchases_df.columns:
            tree_df = purchases_df.groupby('product_id')['price'].sum().reset_index()
            fig2 = px.treemap(tree_df.head(60),
                              path=['product_id'], values='price',
                              color='price',
                              color_continuous_scale=[[0,"#141e30"],[0.5,"#8b5cf6"],[1,"#00f0ff"]])
        else:
            tree_df = pd.DataFrame({'label':['No data'],'value':[1]})
            fig2 = px.treemap(tree_df, path=['label'], values='value')

        fig2.update_traces(textfont=dict(family="DM Mono", size=11),
                           marker_line_width=0.5, marker_line_color="#0a0f1e")
        fig2.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=CHART_BG, height=380,
                           margin=dict(l=8,r=8,t=48,b=8),
                           title=dict(text="Revenue Treemap by Product", font=TITLE_FONT))
        st.plotly_chart(fig2, use_container_width=True)

    # Clustered bar – top products: views vs purchases
    top_ids = list(
        filtered_df['product_id'].value_counts().head(12).index
    ) if 'product_id' in filtered_df.columns else []

    if top_ids:
        compare_df = (filtered_df[filtered_df['product_id'].isin(top_ids)]
                      .groupby(['product_id','event_type']).size()
                      .reset_index(name='count'))
        fig3 = px.bar(compare_df, x='product_id', y='count', color='event_type',
                      barmode='group',
                      color_discrete_sequence=PALETTE_NEON)
        fig3.update_traces(marker_line_width=0)
        fig3.update_layout(**base_layout("Top Products: Clustered Comparison (Views / Cart / Purchase)", height=340))
        st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════
#  TAB 5 – HEATMAP & CLUSTERS
# ══════════════════════════════════════════════
with tab5:
    r1c1, r1c2 = st.columns(2)

    # Heatmap – hour × weekday
    with r1c1:
        heatmap_df = filtered_df.groupby(['weekday','hour']).size().reset_index(name='count')
        order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        hm_pivot = heatmap_df.pivot(index='weekday', columns='hour', values='count').fillna(0)
        hm_pivot = hm_pivot.reindex([d for d in order if d in hm_pivot.index])

        fig = go.Figure(go.Heatmap(
            z=hm_pivot.values,
            x=[f"{h:02d}h" for h in hm_pivot.columns],
            y=hm_pivot.index,
            colorscale=[[0,"#0a0f1e"],[0.25,"#0d1b2a"],[0.5,"#8b5cf6"],
                        [0.75,"#00f0ff"],[1,"#ff4ecd"]],
            showscale=True,
            hoverongaps=False,
            xgap=2, ygap=2
        ))
        fig.update_layout(**base_layout("Activity Heatmap: Weekday × Hour"))
        fig.update_layout(yaxis=dict(showgrid=False))
        st.plotly_chart(fig, use_container_width=True)

    # Bubble scatter – product_id vs revenue vs count
    with r1c2:
        if 'product_id' in purchases_df.columns and 'price' in purchases_df.columns:
            bubble = (purchases_df.groupby('product_id')
                      .agg(revenue=('price','sum'), count=('price','count'))
                      .reset_index()
                      .sort_values('revenue', ascending=False)
                      .head(50))
            fig2 = px.scatter(bubble, x='count', y='revenue', size='revenue',
                              color='revenue',
                              color_continuous_scale=[[0,"#0d1b2a"],[0.4,"#8b5cf6"],[1,"#00f0ff"]],
                              hover_data=['product_id'],
                              size_max=48)
            fig2.update_traces(marker=dict(line=dict(width=1, color="#0a0f1e")),
                               opacity=0.85)
            fig2.update_layout(**base_layout("Bubble Chart: Product Revenue vs Volume"))
        else:
            fig2 = go.Figure()
            fig2.add_annotation(text="No product/price data", showarrow=False,
                                font=dict(color="#94a3b8", size=16))
            fig2.update_layout(**base_layout("Bubble Chart"))
        st.plotly_chart(fig2, use_container_width=True)

    # Dual-axis: purchases count + cumulative revenue
    rev_cum = purchases_df.groupby('hour').agg(
        count=('price','count'), revenue=('price','sum')
    ).reset_index()
    rev_cum['cum_revenue'] = rev_cum['revenue'].cumsum()

    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(go.Bar(
        x=rev_cum['hour'], y=rev_cum['count'],
        name="Purchase Count",
        marker=dict(color=ACCENT_CYAN, opacity=0.7, line_width=0)
    ), secondary_y=False)
    fig3.add_trace(go.Scatter(
        x=rev_cum['hour'], y=rev_cum['cum_revenue'],
        name="Cumulative Revenue",
        line=dict(color=ACCENT_PINK, width=3),
        mode='lines+markers',
        marker=dict(size=6, color=ACCENT_PINK)
    ), secondary_y=True)
    fig3.update_layout(**base_layout("Dual-Axis: Purchase Count vs Cumulative Revenue", height=340))
    fig3.update_yaxes(title_text="Count",      secondary_y=False,
                      tickfont=AXIS_FONT, gridcolor=GRID_COLOR, showgrid=True)
    fig3.update_yaxes(title_text="₹ Cumulative Revenue", secondary_y=True,
                      tickfont=AXIS_FONT, showgrid=False)
    fig3.update_layout(legend=dict(font=dict(family="DM Mono", size=11, color="#94a3b8"),
                                   bgcolor="rgba(0,0,0,0)", bordercolor=GRID_COLOR))
    st.plotly_chart(fig3, use_container_width=True)

# ─────────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.caption("⚡ E-commerce Intelligence Hub  ·  Built with Streamlit & Plotly  ·  Cyber Dark UI")