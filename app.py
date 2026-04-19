import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.data_loader import load_data
from src.processing import process_orders, aggregate_supplier_stats
from src.scoring import compute_score, classify_risk
from src.ml_model import train_model

# ─────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="ProcureIQ Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
#  CSS
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-base:      #03080f;
    --bg-surface:   #070f1c;
    --bg-card:      #0b1628;
    --bg-elevated:  #0f1f38;
    --blue-600:     #1a5fb4;
    --blue-500:     #1e6fd4;
    --blue-400:     #3b8ef0;
    --blue-300:     #72b4f8;
    --white:        #f0f6ff;
    --muted:        #4a6080;
    --text-secondary: #7a96b8;
    --border:       rgba(58,142,240,0.12);
    --border-hover: rgba(58,142,240,0.28);
    --radius-sm:    8px;
    --radius-md:    12px;
    --radius-lg:    16px;
    --transition:   all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
}

*, *::before, *::after { box-sizing: border-box; }
html, body, .stApp {
    background: var(--bg-base) !important;
    color: var(--white) !important;
    font-family: 'Inter', sans-serif !important;
}
.block-container {
    padding: 2rem 2.5rem 4rem !important;
    max-width: 1440px !important;
}
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-base); }
::-webkit-scrollbar-thumb { background: var(--blue-600); border-radius: 10px; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: var(--bg-surface) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { font-family: 'Inter', sans-serif !important; }

.sidebar-logo {
    display: flex; align-items: center; gap: 10px;
    padding: 0.2rem 0 1.4rem 0;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.4rem;
}
.sidebar-logo-icon {
    background: var(--blue-600); border-radius: var(--radius-sm);
    width: 34px; height: 34px; display: flex; align-items: center;
    justify-content: center; font-weight: 700; font-size: 1rem;
    color: white; flex-shrink: 0;
}
.sidebar-logo-name { font-weight: 700; font-size: 0.95rem; color: var(--white); line-height:1.2; }
.sidebar-logo-sub  { font-size: 0.67rem; color: var(--muted); }

.s-label {
    font-size: 0.62rem; font-weight: 700; color: var(--muted);
    text-transform: uppercase; letter-spacing: 0.13em;
    margin-bottom: 0.5rem; margin-top: 0.15rem;
}
hr.s-div { border: none; border-top: 1px solid var(--border); margin: 1.1rem 0; }

/* ── SELECTS / MULTISELECT ── */
[data-baseweb="select"] > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--white) !important;
    font-size: 0.84rem !important;
    transition: var(--transition) !important;
}
[data-baseweb="select"] > div:hover  { border-color: var(--border-hover) !important; }
[data-baseweb="select"] > div:focus-within {
    border-color: var(--blue-400) !important;
    box-shadow: 0 0 0 3px rgba(58,142,240,0.12) !important;
}
[data-baseweb="popover"] {
    background: var(--bg-elevated) !important;
    border: 1px solid var(--border-hover) !important;
    border-radius: var(--radius-md) !important;
    box-shadow: 0 16px 40px rgba(0,0,0,0.55) !important;
}
li[role="option"] {
    background: transparent !important; color: var(--text-secondary) !important;
    font-size: 0.84rem !important; padding: 8px 14px !important;
    transition: var(--transition) !important; border-radius: 6px !important;
}
li[role="option"]:hover { background: rgba(30,111,212,0.18) !important; color: var(--white) !important; }
li[aria-selected="true"] { background: rgba(30,111,212,0.22) !important; color: var(--blue-300) !important; }
[data-baseweb="tag"] {
    background: rgba(30,111,212,0.2) !important; color: var(--blue-300) !important;
    border: 1px solid rgba(58,142,240,0.25) !important;
    border-radius: 6px !important; font-size: 0.76rem !important; font-weight: 500 !important;
}
[data-baseweb="tag"] svg { color: var(--blue-300) !important; }

/* ── SLIDER — KILL ALL RED ── */
.stSlider [data-baseweb="slider"] > div {
    background: var(--bg-elevated) !important; height: 4px !important; border-radius: 4px !important;
}
.stSlider [data-baseweb="slider"] > div > div:first-child { background: var(--blue-400) !important; }
.stSlider [role="slider"] {
    background: var(--white) !important; border: 2px solid var(--blue-400) !important;
    width: 14px !important; height: 14px !important; border-radius: 50% !important;
    box-shadow: 0 0 0 4px rgba(58,142,240,0.15) !important; transition: var(--transition) !important;
}
.stSlider [role="slider"]:hover { box-shadow: 0 0 0 7px rgba(58,142,240,0.2) !important; }
.stSlider span, [data-testid="stSlider"] span,
.stSlider p,   [data-testid="stSlider"] p {
    color: var(--blue-300) !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: 0.74rem !important;
}
span[style*="color: red"], span[style*="color:#ff"],
span[style*="color: #ff"] { color: var(--blue-300) !important; }

/* ── INPUT ── */
input[type="text"], input[type="number"] {
    background: var(--bg-card) !important; color: var(--white) !important;
    border: 1px solid var(--border) !important; border-radius: var(--radius-sm) !important;
    font-family: 'Inter', sans-serif !important; font-size: 0.84rem !important;
    padding: 8px 12px !important; transition: var(--transition) !important;
}
input:focus { border-color: var(--blue-400) !important; box-shadow: 0 0 0 3px rgba(58,142,240,0.14) !important; outline: none !important; }
input::placeholder { color: var(--muted) !important; }

/* ── LABELS ── */
label, [data-testid="stSlider"] label, [data-testid="stNumberInput"] label {
    color: var(--muted) !important; font-size: 0.62rem !important; font-weight: 700 !important;
    text-transform: uppercase !important; letter-spacing: 0.12em !important;
}

/* ── METRIC CARDS ── */
[data-testid="stMetric"] {
    background: var(--bg-card) !important; border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important; padding: 1.1rem 1.25rem !important;
    transition: var(--transition) !important;
}
[data-testid="stMetric"]:hover {
    border-color: var(--border-hover) !important; transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.28);
}
[data-testid="stMetric"] label {
    color: var(--muted) !important; font-size: 0.62rem !important;
    font-weight: 700 !important; text-transform: uppercase !important; letter-spacing: 0.12em !important;
}
[data-testid="stMetricValue"] {
    color: var(--white) !important; font-size: 1.6rem !important;
    font-weight: 700 !important; font-family: 'JetBrains Mono', monospace !important;
}
[data-testid="stMetricDelta"] { font-size: 0.75rem !important; }

/* ── TABS ── */
div[data-baseweb="tab-list"] {
    background: var(--bg-surface) !important; border: 1px solid var(--border) !important;
    border-radius: var(--radius-md) !important; padding: 5px !important; gap: 3px !important;
}
button[role="tab"] {
    font-family: 'Inter', sans-serif !important; font-size: 0.82rem !important;
    font-weight: 500 !important; color: var(--text-secondary) !important;
    border-radius: var(--radius-sm) !important; padding: 7px 20px !important;
    background: transparent !important; border: none !important;
    transition: var(--transition) !important;
}
button[role="tab"]:hover { color: var(--white) !important; background: rgba(30,111,212,0.12) !important; }
button[aria-selected="true"] {
    color: var(--white) !important; background: var(--blue-500) !important;
    font-weight: 600 !important; box-shadow: 0 2px 10px rgba(30,111,212,0.35) !important;
}

/* ── CARD ── */
.card {
    background: var(--bg-card); border: 1px solid var(--border);
    border-radius: var(--radius-lg); padding: 1.35rem 1.5rem; margin-bottom: 1rem;
    transition: var(--transition);
}
.card:hover { border-color: var(--border-hover); }

/* ── PAGE HEADER ── */
.page-header { margin-bottom: 1.75rem; padding-bottom: 1.25rem; border-bottom: 1px solid var(--border); }
.page-title  { font-size: 1.45rem; font-weight: 700; color: var(--white); letter-spacing:-0.025em; }
.page-badge  {
    display: inline-block; background: rgba(30,111,212,0.18); color: var(--blue-300);
    border: 1px solid rgba(58,142,240,0.28); border-radius: 20px;
    font-size: 0.66rem; font-weight: 700; padding: 3px 10px;
    letter-spacing: 0.08em; text-transform: uppercase; margin-left: 10px; vertical-align: middle;
}
.page-sub { color: var(--muted); font-size: 0.78rem; margin-top: 5px; }

/* ── SECTION LABEL ── */
.section-label {
    font-size: 0.62rem; font-weight: 700; color: var(--muted);
    text-transform: uppercase; letter-spacing: 0.13em; margin-bottom: 0.85rem;
}

/* ── INSIGHT BOX ── */
.insight-box {
    background: rgba(30,111,212,0.07); border: 1px solid rgba(58,142,240,0.16);
    border-radius: var(--radius-sm); padding: 0.8rem 1rem; margin: 0.6rem 0;
    font-size: 0.79rem; color: var(--text-secondary); line-height: 1.55;
}

/* ── PILLS ── */
.pill-row { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 10px; }
.pill {
    background: rgba(30,111,212,0.14); border: 1px solid rgba(58,142,240,0.22);
    color: var(--blue-300); border-radius: 20px; font-size: 0.72rem;
    font-weight: 500; padding: 3px 12px;
}

/* ── BUTTONS ── */
.stButton > button, .stDownloadButton > button {
    background: var(--blue-500) !important; color: var(--white) !important;
    border: none !important; border-radius: var(--radius-sm) !important;
    font-family: 'Inter', sans-serif !important; font-size: 0.82rem !important;
    font-weight: 600 !important; padding: 9px 22px !important; transition: var(--transition) !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: var(--blue-400) !important; transform: translateY(-1px) !important;
    box-shadow: 0 4px 14px rgba(30,111,212,0.35) !important;
}

/* ── ALERTS ── */
[data-testid="stAlert"] {
    border-radius: var(--radius-sm) !important; font-size: 0.82rem !important;
    border-left-width: 3px !important; font-family: 'Inter', sans-serif !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] { border: 1px solid var(--border) !important; border-radius: var(--radius-md) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  DATA PIPELINE
# ─────────────────────────────────────────
@st.cache_data
def load_pipeline():
    orders, details, suppliers, products = load_data()
    orders = process_orders(orders, details)
    stats  = aggregate_supplier_stats(orders)
    stats  = compute_score(stats, suppliers)
    stats  = classify_risk(stats)
    stats, model, rmse = train_model(stats)
    return stats, model, rmse

supplier_stats, model, rmse = load_pipeline()

# ─────────────────────────────────────────
#  PLOTLY BASE LAYOUT
# ─────────────────────────────────────────
BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor ="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#7a96b8", size=11),
    xaxis=dict(gridcolor="rgba(58,142,240,0.07)", linecolor="rgba(58,142,240,0.15)", showgrid=True),
    yaxis=dict(gridcolor="rgba(58,142,240,0.07)", linecolor="rgba(58,142,240,0.15)", showgrid=True),
    legend=dict(bgcolor="rgba(7,15,28,0.85)", bordercolor="rgba(58,142,240,0.15)",
                borderwidth=1, font=dict(color="#7a96b8", size=11)),
    margin=dict(l=10, r=10, t=36, b=10),
    hoverlabel=dict(bgcolor="rgba(11,22,40,0.95)", bordercolor="rgba(58,142,240,0.3)",
                    font=dict(color="#f0f6ff", size=12, family="Inter")),
    transition=dict(duration=350, easing="cubic-in-out"),
)

RISK_C = {"High Risk": "#ef4444", "Medium Risk": "#f59e0b", "Low Risk": "#22c55e"}

# ─────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">P</div>
        <div>
            <div class="sidebar-logo-name">ProcureIQ</div>
            <div class="sidebar-logo-sub">Supply Chain Analytics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="s-label">Suppliers</div>', unsafe_allow_html=True)
    all_ids = supplier_stats['supplier_id'].tolist()
    supplier_filter = st.multiselect(
        "sup", all_ids, default=all_ids,
        label_visibility="collapsed", placeholder="Select suppliers...",
    )

    st.markdown('<hr class="s-div">', unsafe_allow_html=True)
    st.markdown('<div class="s-label">Risk Level</div>', unsafe_allow_html=True)
    avail_risks = supplier_stats['risk'].unique().tolist()
    # ensure High Risk always appears in options even if none exist yet
    all_risk_opts = sorted(set(avail_risks + ["High Risk", "Medium Risk", "Low Risk"]))
    risk_filter = st.multiselect(
        "risk", all_risk_opts, default=avail_risks,
        label_visibility="collapsed", placeholder="Select risk levels...",
    )

    st.markdown('<hr class="s-div">', unsafe_allow_html=True)
    st.markdown('<div class="s-label">Cost Range</div>', unsafe_allow_html=True)
    cmin, cmax = float(supplier_stats['avg_cost'].min()), float(supplier_stats['avg_cost'].max())
    cost_range = st.slider("cost", cmin, cmax, (cmin, cmax), label_visibility="collapsed")

    st.markdown('<div class="s-label" style="margin-top:0.9rem;">Delay Range (days)</div>', unsafe_allow_html=True)
    dmin, dmax = float(supplier_stats['avg_delay'].min()), float(supplier_stats['avg_delay'].max())
    delay_range = st.slider("delay", dmin, dmax, (dmin, dmax), label_visibility="collapsed")

    st.markdown('<hr class="s-div">', unsafe_allow_html=True)
    st.markdown('<div class="s-label">Search Supplier</div>', unsafe_allow_html=True)
    search = st.text_input("srch", placeholder="e.g. SUP-001", label_visibility="collapsed")

# ─────────────────────────────────────────
#  FILTER
# ─────────────────────────────────────────
filtered = supplier_stats.copy()
if supplier_filter:
    filtered = filtered[filtered['supplier_id'].isin(supplier_filter)]
if risk_filter:
    filtered = filtered[filtered['risk'].isin(risk_filter)]
filtered = filtered[
    filtered['avg_cost'].between(*cost_range) &
    filtered['avg_delay'].between(*delay_range)
]
if search:
    filtered = filtered[filtered['supplier_id'].astype(str).str.contains(search, case=False)]

if filtered.empty:
    st.warning("No suppliers match the current filters. Adjust the sidebar controls.")
    st.stop()

# ─────────────────────────────────────────
#  PAGE HEADER
# ─────────────────────────────────────────
high_risk_pct = (filtered['risk'].str.contains("High")).mean() * 100

st.markdown(f"""
<div class="page-header">
    <span class="page-title">Procurement Analytics Dashboard</span>
    <span class="page-badge">P2 · Procurement Reliability</span>
    <div class="page-sub">Supplier risk monitoring &amp; data-driven decision support &nbsp;·&nbsp; Jan – May 2026 &nbsp;·&nbsp; {len(filtered)} suppliers</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  KPI ROW
# ─────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Suppliers",     f"{len(filtered)}")
k2.metric("Avg Delay",     f"{filtered['avg_delay'].mean():.1f} d")
k3.metric("On-Time Rate",  f"{filtered['on_time_rate'].mean()*100:.1f}%")
k4.metric("Avg Cost",      f"{filtered['avg_cost'].mean():,.0f}")
k5.metric("ML RMSE",       f"{rmse:.2f}")

st.markdown("<div style='margin:1rem 0'></div>", unsafe_allow_html=True)

if high_risk_pct > 30:
    st.error(f"**{high_risk_pct:.0f}% of suppliers are high-risk** — immediate review recommended.")
elif high_risk_pct > 10:
    st.warning(f"**{high_risk_pct:.0f}% of suppliers show moderate risk** — monitor closely.")
else:
    st.success(f"**Risk environment is stable** — {high_risk_pct:.0f}% high-risk exposure.")

st.markdown("<div style='margin:1.25rem 0'></div>", unsafe_allow_html=True)

# ─────────────────────────────────────────
#  TABS
# ─────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Suppliers", "Risk Analysis", "Simulation & ML"])

# ── TAB 1: OVERVIEW ───────────────────────────
with tab1:
    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")

    with c1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Cost vs Delay by Risk</div>', unsafe_allow_html=True)
        fig = px.scatter(
            filtered, x="avg_cost", y="avg_delay", color="risk",
            color_discrete_map=RISK_C,
            hover_data={"supplier_id": True, "avg_cost": ":.1f", "avg_delay": ":.2f"},
            labels={"avg_cost": "Avg Cost", "avg_delay": "Avg Delay (days)", "risk": "Risk"},
        )
        fig.update_traces(marker=dict(size=10, opacity=0.88, line=dict(width=1, color="rgba(255,255,255,0.12)")))
        fig.update_layout(**BASE, height=310)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">On-Time Rate Distribution</div>', unsafe_allow_html=True)
        fig2 = px.histogram(
            filtered, x="on_time_rate", nbins=14,
            color_discrete_sequence=["#1e6fd4"],
            labels={"on_time_rate": "On-Time Rate"},
        )
        fig2.update_traces(marker_line_color="rgba(58,142,240,0.35)", marker_line_width=1)
        fig2.update_layout(**BASE, height=310)
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    c3, c4 = st.columns(2, gap="large")

    with c3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Top 12 Suppliers by Avg Cost</div>', unsafe_allow_html=True)
        top12 = filtered.nlargest(12, "avg_cost")
        fig3 = px.bar(
            top12, x="supplier_id", y="avg_cost",
            color="avg_cost", color_continuous_scale=["#0b1628", "#1a5fb4", "#3b8ef0"],
            labels={"supplier_id": "Supplier", "avg_cost": "Avg Cost"},
        )
        fig3.update_layout(**BASE, height=290, coloraxis_showscale=False)
        fig3.update_xaxes(tickangle=-35)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with c4:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Delay Distribution by Risk Level</div>', unsafe_allow_html=True)
        fig4 = px.box(
            filtered, x="risk", y="avg_delay",
            color="risk", color_discrete_map=RISK_C,
            labels={"risk": "Risk Level", "avg_delay": "Avg Delay (days)"},
        )
        fig4.update_layout(**BASE, height=290, showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ── TAB 2: SUPPLIERS ──────────────────────────
with tab2:
    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Supplier Records</div>', unsafe_allow_html=True)

    def _hl(row):
        if "High"   in str(row.get('risk', '')): return ['background-color:rgba(220,38,38,0.1);color:#fca5a5'] * len(row)
        if "Medium" in str(row.get('risk', '')): return ['background-color:rgba(217,119,6,0.1);color:#fde68a'] * len(row)
        return [''] * len(row)

    dcols = [c for c in ['supplier_id','avg_delay','on_time_rate','avg_cost','risk','score'] if c in filtered.columns]
    st.dataframe(filtered[dcols].style.apply(_hl, axis=1), use_container_width=True, height=400)
    st.markdown('</div>', unsafe_allow_html=True)

    if 'score' in filtered.columns:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Supplier Score vs Avg Delay</div>', unsafe_allow_html=True)
        fig5 = px.scatter(
            filtered, x="score", y="avg_delay", color="risk",
            color_discrete_map=RISK_C, hover_data=["supplier_id"],
            labels={"score": "Supplier Score", "avg_delay": "Avg Delay (days)"},
        )
        fig5.update_traces(marker=dict(size=9, opacity=0.85))
        fig5.update_layout(**BASE, height=300)
        st.plotly_chart(fig5, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ── TAB 3: RISK ANALYSIS ──────────────────────
with tab3:
    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
    r1, r2 = st.columns(2, gap="large")

    with r1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Risk Category Count</div>', unsafe_allow_html=True)
        rc = filtered['risk'].value_counts().reset_index()
        rc.columns = ['risk','count']
        fig6 = px.bar(rc, x='risk', y='count', color='risk',
                      color_discrete_map=RISK_C, text='count',
                      labels={"risk":"Risk Level","count":"Suppliers"})
        fig6.update_traces(textposition='outside', textfont_color="#f0f6ff")
        fig6.update_layout(**BASE, height=300, showlegend=False)
        st.plotly_chart(fig6, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Avg Delay by Risk Level</div>', unsafe_allow_html=True)
        rd = filtered.groupby('risk')['avg_delay'].mean().reset_index()
        fig7 = px.bar(rd, x='risk', y='avg_delay', color='risk',
                      color_discrete_map=RISK_C,
                      text=rd['avg_delay'].round(2),
                      labels={"risk":"Risk Level","avg_delay":"Avg Delay (days)"})
        fig7.update_traces(textposition='outside', textfont_color="#f0f6ff")
        fig7.update_layout(**BASE, height=300, showlegend=False)
        st.plotly_chart(fig7, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Cost Spread Across Risk Levels</div>', unsafe_allow_html=True)
    fig8 = px.violin(
        filtered, x='risk', y='avg_cost', color='risk',
        color_discrete_map=RISK_C, box=True, points="all",
        labels={"risk":"Risk Level","avg_cost":"Avg Cost"},
    )
    fig8.update_traces(meanline_visible=True)
    fig8.update_layout(**BASE, height=330, showlegend=False)
    st.plotly_chart(fig8, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ── TAB 4: SIMULATION & ML ────────────────────
with tab4:
    st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)
    s1, s2 = st.columns(2, gap="large")

    with s1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Delay Shock Simulator</div>', unsafe_allow_html=True)
        sim_delay = st.slider("Simulate Delay Increase (days)", 0.0, 10.0, 0.0, 0.25)
        simulated = filtered.copy()
        simulated['avg_delay'] += sim_delay
        base_avg  = filtered['avg_delay'].mean()
        new_avg   = simulated['avg_delay'].mean()
        dpct      = ((new_avg - base_avg) / base_avg * 100) if base_avg else 0

        m1, m2 = st.columns(2)
        m1.metric("Baseline Avg", f"{base_avg:.2f} d")
        m2.metric("Simulated Avg", f"{new_avg:.2f} d", delta=f"+{dpct:.1f}%")

        if sim_delay > 5:   st.error("Severe disruption — consider alternate sourcing.")
        elif sim_delay > 2: st.warning("Moderate disruption — flag suppliers for review.")
        else:               st.success("Within acceptable thresholds.")

        cmp = pd.DataFrame({
            "Scenario": ["Baseline", "Simulated"],
            "Avg Delay": [base_avg, new_avg],
        })
        fig9 = px.bar(cmp, x="Scenario", y="Avg Delay", color="Scenario",
                      color_discrete_map={"Baseline":"#1e6fd4","Simulated":"#ef4444"},
                      text=cmp["Avg Delay"].round(2))
        fig9.update_traces(textposition='outside', textfont_color="#f0f6ff",
                           marker_line_width=0, width=0.38)
        fig9.update_layout(**BASE, height=260, showlegend=False)
        st.plotly_chart(fig9, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with s2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">ML Delay Predictor</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="insight-box">Random Forest trained on supplier history. '
            f'RMSE: <strong style="color:#72b4f8">{rmse:.2f}</strong>. '
            f'Adjust inputs to predict delay for a hypothetical supplier profile.</div>',
            unsafe_allow_html=True
        )
        input_cost    = st.number_input("Average Cost", value=float(filtered['avg_cost'].mean()), step=100.0)
        input_on_time = st.slider("On-Time Rate", 0.0, 1.0, float(filtered['on_time_rate'].mean()), 0.01)

        input_df = pd.DataFrame({"avg_cost": [input_cost], "on_time_rate": [input_on_time]})
        try:
            pred     = model.predict(input_df)[0]
            avg_base = filtered['avg_delay'].mean()
            st.metric("Predicted Delay", f"{pred:.2f} d", delta=f"{pred - avg_base:+.2f} vs avg")
            if pred > avg_base * 1.2: st.warning("Above average delay predicted — review supplier.")
            else:                     st.success("Predicted delay within normal range.")
        except Exception as e:
            st.error(f"Prediction failed: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────
#  DECISION ASSISTANT
# ─────────────────────────────────────────
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Supplier Decision Assistant</div>', unsafe_allow_html=True)

sel = st.selectbox("Choose a supplier", filtered['supplier_id'], label_visibility="collapsed")
sd  = filtered[filtered['supplier_id'] == sel].iloc[0]

d1, d2, d3 = st.columns(3)
d1.metric("Avg Delay",  f"{sd['avg_delay']:.2f} d")
d2.metric("Avg Cost",   f"{sd['avg_cost']:,.0f}")
d3.metric("On-Time",    f"{sd['on_time_rate']*100:.1f}%")

st.markdown("<div style='height:0.4rem'></div>", unsafe_allow_html=True)
if "High"   in str(sd['risk']): st.error(f"**{sel}** is High Risk — avoid for critical procurement.")
elif "Medium" in str(sd['risk']): st.warning(f"**{sel}** is Medium Risk — use with active monitoring.")
else: st.success(f"**{sel}** is Low Risk — reliable for critical orders.")

pills = [f"Risk: {sd['risk']}"]
if 'score' in sd.index: pills.append(f"Score: {sd['score']:.1f}")
st.markdown(
    '<div class="pill-row">' + ''.join(f'<span class="pill">{p}</span>' for p in pills) + '</div>',
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────
#  DOWNLOAD
# ─────────────────────────────────────────
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
st.download_button(
    "Download Filtered Data (CSV)",
    filtered.to_csv(index=False),
    file_name="filtered_suppliers.csv",
    mime="text/csv",
)