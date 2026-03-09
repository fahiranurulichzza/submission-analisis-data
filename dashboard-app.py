"""
E-Commerce Sales Dashboard
Insight selaras dengan Proyek Analisis Data (tren penjualan, kategori profit, RFM).
Prinsip desain: satu pesan per chart, warna konsisten, label jelas, hirarki visual.
"""
import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page config ---
st.set_page_config(
    page_title="E-Commerce Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS: tampilan menarik & mudah dibaca ---
st.markdown("""
<style>
    /* Font & dasar */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 50%, #e2e8f0 100%);
    }

    /* Header - hero style */
    .main-title {
        font-size: 2.25rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0f172a 0%, #334155 50%, #0ea5e9 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.35rem;
        letter-spacing: -0.03em;
        line-height: 1.2;
    }
    .subtitle {
        font-size: 1rem;
        color: #64748b;
        margin-bottom: 2rem;
        font-weight: 500;
        max-width: 720px;
    }

    /* KPI cards - card style dengan shadow & border */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.25rem 1.5rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 4px 12px rgba(14, 165, 233, 0.08);
        border: 1px solid rgba(14, 165, 233, 0.15);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        box-shadow: 0 4px 16px rgba(14, 165, 233, 0.12);
        transform: translateY(-2px);
    }
    [data-testid="stMetricValue"] {
        font-size: 1.75rem !important;
        font-weight: 800 !important;
        color: #0f172a !important;
        letter-spacing: -0.02em;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.875rem !important;
        color: #64748b !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }

    /* Section headers - lebih menonjol */
    h2 {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        color: #0f172a !important;
        margin-top: 2rem !important;
        margin-bottom: 0.75rem !important;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid rgba(14, 165, 233, 0.25);
        display: inline-block;
    }
    h3 { font-size: 1.05rem !important; font-weight: 600 !important; color: #334155 !important; }

    /* Sidebar - lebih elegan */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        box-shadow: 4px 0 24px rgba(0,0,0,0.04);
    }
    [data-testid="stSidebar"] .stMarkdown { font-weight: 600; color: #0f172a; }
    [data-testid="stSidebar"] [data-testid="stSelectbox"], [data-testid="stSidebar"] [data-testid="stMultiSelect"] {
        border-radius: 8px;
    }

    /* Block container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    /* Chart container - card wrapper feel */
    [data-testid="stVerticalBlock"] > div:has([data-testid="stPlotlyChart"]) {
        background: #ffffff;
        padding: 1.25rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid rgba(0,0,0,0.06);
        margin-bottom: 0.5rem;
    }

    /* Insight box - dua variasi */
    .insight-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-left: 4px solid #0ea5e9;
        padding: 1.25rem 1.5rem;
        border-radius: 0 12px 12px 0;
        margin: 1rem 0;
        font-size: 0.95rem;
        line-height: 1.65;
        color: #1e293b;
        box-shadow: 0 2px 8px rgba(14, 165, 233, 0.08);
    }
    .insight-box strong { color: #0c4a6e; }
    .insight-box.alt {
        background: linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%);
        border-left-color: #8b5cf6;
    }
    .insight-box.alt strong { color: #5b21b6; }

    /* Horizontal rule */
    hr {
        margin: 2rem 0 !important;
        border: none !important;
        height: 1px !important;
        background: linear-gradient(90deg, transparent, rgba(14, 165, 233, 0.2), transparent) !important;
    }

    /* Caption / footer */
    [data-testid="stCaption"] {
        font-size: 0.8rem !important;
        color: #94a3b8 !important;
        font-style: italic;
    }

    /* Hide Streamlit branding untuk tampilan bersih (opsional) */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- Load data ---
@st.cache_data
def load_data():
    df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vQVGpZVLvfhsAMIhn1tzuYRvQsZEZQD6XTs-0uyJis9PtYeDfyeGAXK-9hjZht24K7d0tI6dfCqjSFv/pub?gid=381439088&single=true&output=csv")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)
    df["year"] = df["order_purchase_timestamp"].dt.year
    return df

df = load_data()

# --- Sidebar: filter ---
st.sidebar.header("🔧 Filter")
year_options = sorted(df["year"].unique())
year_filter = st.sidebar.selectbox("Tahun", year_options, index=len(year_options) - 1 if year_options else 0)
months_in_year = df[df["year"] == year_filter]["order_month"].unique()
month_options = sorted(months_in_year) if len(months_in_year) > 0 else []
month_filter = st.sidebar.multiselect(
    "Bulan (opsional, kosongkan = semua)",
    month_options,
    default=[],
)
st.sidebar.markdown("---")
st.sidebar.caption("Data: Oktober 2016 – Agustus 2018")

# --- Filter data ---
df_filtered = df[df["year"] == year_filter]
if month_filter:
    df_filtered = df_filtered[df_filtered["order_month"].isin(month_filter)]

# --- Header ---
st.markdown('', unsafe_allow_html=True)
st.markdown('<div class="main-title">E-Commerce Sales Dashboard</div>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Tren penjualan bulanan, kategori produk unggulan, dan segmentasi pelanggan RFM</p>', unsafe_allow_html=True)

# --- KPI row ---
total_revenue = df_filtered["payment_value"].sum().astype(float)
total_orders = df_filtered["order_id"].nunique().astype(float)
avg_order_value = (total_revenue / total_orders) if total_orders else 0.0

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Revenue", f"R$ {total_revenue:,.0f}" if total_revenue == total_revenue else "—")
with col2:
    st.metric("Total Orders", f"{total_orders:,}")
with col3:
    st.metric("Rata-rata Nilai Order", f"R$ {avg_order_value:,.2f}" if total_orders else "—")

# st.markdown("---")

# --- Chart theme (konsisten di semua plot) ---
CHART_THEME = {
    "colorway": ["#0ea5e9", "#8b5cf6", "#10b981", "#f59e0b", "#ef4444", "#6366f1", "#14b8a6", "#f97316"],
    "font_family": "Plus Jakarta Sans, sans-serif",
    "title_font_size": 15,
    "paper_bgcolor": "rgba(0,0,0,0)",
    "plot_bgcolor": "rgba(0,0,0,0)",
    "margin": dict(t=50, b=40, l=50, r=30),
    "xaxis": dict(showgrid=True, gridcolor="rgba(0,0,0,0.06)", zeroline=False),
    "yaxis": dict(showgrid=True, gridcolor="rgba(0,0,0,0.06)", zeroline=False),
}

def apply_theme(fig):
    fig.update_layout(
        font=dict(family=CHART_THEME["font_family"], size=12),
        title=dict(font=dict(size=CHART_THEME["title_font_size"]), x=0.02, xanchor="left"),
        paper_bgcolor=CHART_THEME["paper_bgcolor"],
        plot_bgcolor=CHART_THEME["plot_bgcolor"],
        margin=CHART_THEME["margin"],
        xaxis=CHART_THEME["xaxis"],
        yaxis=CHART_THEME["yaxis"],
        colorway=CHART_THEME["colorway"],
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig

# --- 1. Tren penjualan bulanan (revenue) ---
st.subheader("Tren Revenue Bulanan")
monthly_revenue = (
    df_filtered.groupby("order_month")["payment_value"]
    .sum()
    .reset_index()
    .sort_values("order_month")
)
fig_revenue = px.line(
    monthly_revenue,
    x="order_month",
    y="payment_value",
    markers=True,
    title="Performa Penjualan Bulanan",
    labels={"order_month": "Bulan", "payment_value": "Revenue (R$)"},
)
fig_revenue.update_traces(line=dict(width=2.5), marker=dict(size=8))
fig_revenue = apply_theme(fig_revenue)
st.plotly_chart(fig_revenue, use_container_width=True)

# --- 2. Tren jumlah order bulanan ---
st.subheader("Tren Jumlah Order Bulanan")
monthly_orders = (
    df_filtered.groupby("order_month")["order_id"]
    .nunique()
    .reset_index()
    .rename(columns={"order_id": "jumlah_order"})
    .sort_values("order_month")
)
fig_orders = px.bar(
    monthly_orders,
    x="order_month",
    y="jumlah_order",
    title="Jumlah Order Bulanan",
    labels={"order_month": "Bulan", "jumlah_order": "Jumlah Order"},
)
fig_orders.update_traces(marker_color="#0ea5e9", marker_line_color="rgba(0,0,0,0.1)", marker_line_width=0.5)
fig_orders = apply_theme(fig_orders)
st.plotly_chart(fig_orders, use_container_width=True)

# --- 4. RFM & Segmentasi Pelanggan (sesuai notebook) ---
st.subheader("Segmentasi Pelanggan (RFM)")
snapshot_date = df["order_purchase_timestamp"].max() + pd.Timedelta(days=1)

rfm = df.groupby("customer_unique_id").agg(
    Recency=("order_purchase_timestamp", lambda x: (snapshot_date - x.max()).days),
    Frequency=("order_id", "nunique"),
    Monetary=("payment_value", "sum"),
).reset_index()

# Skor RFM (1–5, R: rendah recency = baik; F,M: tinggi = baik)
rfm["R_Score"] = pd.qcut(rfm["Recency"], 5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm["RFM_Sum"] = rfm[["R_Score", "F_Score", "M_Score"]].sum(axis=1)

def segment_by_score(s):
    if s >= 13:
        return "Best Customers"
    if s >= 11:
        return "Loyal Customers"
    if s >= 9:
        return "Potential Loyalist"
    if s >= 7:
        return "At Risk"
    return "Lost"

rfm["Customer_Segment"] = rfm["RFM_Sum"].apply(segment_by_score)

# Ringkasan RFM (rata-rata) — hindari NaN/undefined
def _safe_mean(series, kind="int", suffix=""):
    if series.empty:
        return "—"
    val = series.mean()
    if pd.isna(val):
        return "—"
    v = float(val)
    if kind == "int":
        return f"{v:.0f}{suffix}"
    if kind == "float":
        return f"{v:.2f}{suffix}"
    return f"R$ {v:,.2f}"

c1, c2, c3 = st.columns(3)
c1.metric("Rata-rata Recency", _safe_mean(rfm["Recency"], "int", " hari"))
c2.metric("Rata-rata Frequency", _safe_mean(rfm["Frequency"], "float"))
c3.metric("Rata-rata Monetary", _safe_mean(rfm["Monetary"], "currency"))

# Pie: proporsi segment
segment_counts = rfm["Customer_Segment"].value_counts()
order_segments = ["Best Customers", "Loyal Customers", "Potential Loyalist", "At Risk", "Lost"]
segment_counts = segment_counts.reindex([s for s in order_segments if s in segment_counts.index]).fillna(0).astype(int)

fig_pie = px.pie(
    values=segment_counts.values,
    names=segment_counts.index,
    title="Proporsi Segmentasi Pelanggan Berdasarkan RFM Score",
    color_discrete_sequence=CHART_THEME["colorway"],
)
fig_pie.update_traces(textposition="inside", textinfo="percent+label")
fig_pie = apply_theme(fig_pie)
st.plotly_chart(fig_pie, use_container_width=True)

# Scatter: Recency vs Monetary, size = Frequency (hover tanpa undefined)
rfm_display = rfm.copy()
rfm_display["hover_label"] = rfm_display["customer_unique_id"].fillna("Customer").astype(str)
fig_rfm = px.scatter(
    rfm_display,
    x="Recency",
    y="Monetary",
    size="Frequency",
    color="Customer_Segment",
    hover_name="hover_label",
    labels={"Recency": "Recency (hari)", "Monetary": "Monetary (R$)", "Frequency": "Frequency"},
    title="Distribusi Pelanggan: Recency vs Monetary (ukuran = Frequency)",
    color_discrete_sequence=CHART_THEME["colorway"],
)
fig_rfm.update_traces(marker=dict(opacity=0.7, line=dict(width=0.5, color="white")))
fig_rfm = apply_theme(fig_rfm)
st.plotly_chart(fig_rfm, use_container_width=True)

# Boxplot setiap metrik per segmen (Plotly)
segment_order = ["Best Customers", "Loyal Customers", "Potential Loyalist", "At Risk", "Lost"]
rfm_ordered = rfm[rfm["Customer_Segment"].isin(segment_order)].copy()
rfm_ordered["Customer_Segment"] = pd.Categorical(
    rfm_ordered["Customer_Segment"], categories=segment_order, ordered=True
)
rfm_ordered = rfm_ordered.sort_values("Customer_Segment")

fig_box_recency = px.box(
    rfm_ordered,
    x="Customer_Segment",
    y="Recency",
    color="Customer_Segment",
    title="Recency per Segmen",
    points=False,
    color_discrete_sequence=CHART_THEME["colorway"],
)
fig_box_recency.update_traces(showlegend=False)
fig_box_recency.update_layout(xaxis_title="", yaxis_title="Recency (hari)")
fig_box_recency = apply_theme(fig_box_recency)
fig_box_recency.update_layout(yaxis_title="Recency (hari)")
st.plotly_chart(fig_box_recency, use_container_width=True)

fig_box_freq = px.box(
    rfm_ordered,
    x="Customer_Segment",
    y="Frequency",
    color="Customer_Segment",
    title="Frequency per Segmen",
    points=False,
    color_discrete_sequence=CHART_THEME["colorway"],
)
fig_box_freq.update_traces(showlegend=False)
fig_box_freq.update_layout(xaxis_title="", yaxis_title="Frequency")
fig_box_freq = apply_theme(fig_box_freq)
fig_box_freq.update_layout(yaxis_title="Frequency")
st.plotly_chart(fig_box_freq, use_container_width=True)

fig_box_monetary = px.box(
    rfm_ordered,
    x="Customer_Segment",
    y="Monetary",
    color="Customer_Segment",
    title="Monetary per Segmen",
    points=False,
    color_discrete_sequence=CHART_THEME["colorway"],
)
fig_box_monetary.update_traces(showlegend=False)
fig_box_monetary.update_layout(xaxis_title="", yaxis_title="Monetary (R$)")
fig_box_monetary = apply_theme(fig_box_monetary)
fig_box_monetary.update_layout(yaxis_title="Monetary (R$)")
st.plotly_chart(fig_box_monetary, use_container_width=True)

# st.markdown("---")

# --- Insight (sesuai kesimpulan di notebook) ---
st.subheader("📌 Insight & Kesimpulan")

st.markdown("""
<div class="insight-box">
<strong>Pertanyaan 1 — Tren penjualan & kategori profit:</strong><br>
Selama periode Oktober 2016 hingga Agustus 2018, performa penjualan menunjukkan tren pertumbuhan yang signifikan.
Revenue bulanan meningkat pesat sejak awal 2017 dan mencapai puncaknya di akhir 2017 (terutama November–Desember 2017).
Setelah puncak tersebut, revenue tetap stabil di level tinggi (rata-rata di atas 1 juta real per bulan hingga pertengahan 2018).
Penyumbang profit utama: <strong>cama_mesa_banho</strong>, <strong>beleza_saude</strong>, dan <strong>informatica_acessorios</strong>.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="insight-box alt">
<strong>Pertanyaan 2 — Segmentasi RFM & perilaku pembelian:</strong><br>
Mayoritas pelanggan hanya melakukan satu kali transaksi (Frequency = 1). Distribusi Recency tersebar luas (ada yang baru belanja dan yang sudah lama tidak transaksi).
Aspek Monetary: sebagian besar pelanggan nilai transaksi total kecil, dengan sedikit pelanggan bernilai sangat besar (outlier).
Segmen terbesar: <strong>Potential Loyalist</strong> dan <strong>At Risk</strong> — perlu strategi retensi dan engagement.
Hanya sekitar 8,5% <strong>Best Customers</strong>; segmen <strong>Lost</strong> juga signifikan sehingga reaktivasi penting.
Rekomendasi: fokus pada retensi, dorongan pembelian ulang, dan perlakuan khusus untuk pelanggan nilai tinggi.
</div>
""", unsafe_allow_html=True)

st.caption("Dashboard selaras dengan analisis di Proyek_Analisis_Data.ipynb — prinsip visualisasi: satu pesan per chart, warna konsisten, label jelas.")
