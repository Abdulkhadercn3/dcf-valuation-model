import streamlit as st
import numpy as np
import pandas as pd

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Financial Model",
    page_icon="📊",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background: #0d1117;
    color: #e6edf3;
}

/* Header */
h1, h2, h3 {
    font-family: 'DM Serif Display', serif !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #161b22 !important;
    border-right: 1px solid #30363d;
}

[data-testid="stSidebar"] .stMarkdown h3 {
    color: #58a6ff;
    font-size: 0.85rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    font-family: 'DM Mono', monospace !important;
    border-bottom: 1px solid #21262d;
    padding-bottom: 6px;
    margin-bottom: 12px;
}

/* Number inputs */
[data-testid="stNumberInput"] input {
    background: #0d1117 !important;
    border: 1px solid #30363d !important;
    color: #e6edf3 !important;
    border-radius: 6px !important;
    font-family: 'DM Mono', monospace !important;
}

[data-testid="stNumberInput"] input:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 0 2px rgba(88,166,255,0.15) !important;
}

/* Sliders */
[data-testid="stSlider"] .stSlider > div > div > div {
    background: #58a6ff !important;
}

/* Metric cards */
.metric-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.metric-card:hover { border-color: #58a6ff; }
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #58a6ff, #3fb950);
}
.metric-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #8b949e;
    margin-bottom: 8px;
}
.metric-value {
    font-family: 'DM Serif Display', serif;
    font-size: 2rem;
    color: #e6edf3;
    line-height: 1.1;
}
.metric-sub {
    font-size: 0.78rem;
    color: #8b949e;
    margin-top: 4px;
    font-family: 'DM Mono', monospace;
}

/* Table styling */
.styled-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'DM Mono', monospace;
    font-size: 0.85rem;
}
.styled-table th {
    background: #1c2128;
    color: #58a6ff;
    padding: 10px 14px;
    text-align: right;
    font-weight: 500;
    letter-spacing: 0.06em;
    border-bottom: 1px solid #30363d;
}
.styled-table th:first-child { text-align: left; }
.styled-table td {
    padding: 9px 14px;
    text-align: right;
    border-bottom: 1px solid #21262d;
    color: #c9d1d9;
}
.styled-table td:first-child {
    text-align: left;
    color: #8b949e;
    font-size: 0.78rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
.styled-table tr:hover td { background: #1c2128; }
.styled-table .row-ebit td { color: #3fb950 !important; }
.styled-table .row-fcf td { color: #58a6ff !important; }
.styled-table .row-total { border-top: 2px solid #30363d; }
.styled-table .row-total td { font-weight: 600; }

/* Sensitivity table */
.sens-table { font-family: 'DM Mono', monospace; font-size: 0.82rem; width: 100%; border-collapse: collapse; }
.sens-table th { background: #1c2128; color: #58a6ff; padding: 8px 12px; border-bottom: 2px solid #30363d; }
.sens-table td { padding: 8px 12px; border-bottom: 1px solid #21262d; text-align: right; }
.sens-table tr:hover td { background: #1c2128; }
.sens-highlight { background: #1f2d1f !important; color: #3fb950 !important; font-weight: 600; }
.sens-negative { color: #f85149 !important; }

/* Info box */
.info-box {
    background: #1c2128;
    border: 1px solid #30363d;
    border-left: 3px solid #58a6ff;
    border-radius: 6px;
    padding: 12px 16px;
    font-size: 0.82rem;
    color: #8b949e;
    font-family: 'DM Mono', monospace;
    margin: 8px 0;
}

/* Section title */
.section-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.35rem;
    color: #e6edf3;
    margin: 28px 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #21262d;
}

.wacc-badge {
    display: inline-block;
    background: rgba(88,166,255,0.12);
    color: #58a6ff;
    border: 1px solid rgba(88,166,255,0.3);
    border-radius: 20px;
    padding: 2px 12px;
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    margin-left: 10px;
    vertical-align: middle;
}
</style>
""", unsafe_allow_html=True)


# ── Helper ────────────────────────────────────────────────────────────────────
def fmt(v, prefix="$"):
    if abs(v) >= 1e6:
        return f"{prefix}{v/1e6:.2f}M"
    if abs(v) >= 1e3:
        return f"{prefix}{v/1e3:.1f}K"
    return f"{prefix}{v:.2f}"

def pct(v):
    return f"{v*100:.2f}%"


# ── Sidebar inputs ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Model Inputs")

    # ── Revenue & Variable Costs
    st.markdown("### Revenue & Variable Costs")
    years = ["Year 1", "Year 2", "Year 3", "Year 4"]
    revenues = []
    var_costs = []

    default_rev = [1_000_000, 1_200_000, 1_450_000, 1_750_000]
    default_vc  = [400_000,   480_000,   580_000,   700_000]

    for i, y in enumerate(years):
        st.markdown(f"**{y}**")
        c1, c2 = st.columns(2)
        with c1:
            rev = st.number_input(f"Revenue", value=float(default_rev[i]),
                                  step=10_000.0, format="%.0f", key=f"rev_{i}",
                                  label_visibility="collapsed" if i > 0 else "visible")
        with c2:
            vc = st.number_input(f"Var. Cost", value=float(default_vc[i]),
                                 step=10_000.0, format="%.0f", key=f"vc_{i}",
                                 label_visibility="collapsed" if i > 0 else "visible")
        revenues.append(rev)
        var_costs.append(vc)

    # ── Fixed Costs
    st.markdown("### Fixed Costs")
    fixed_cost = st.number_input("Annual Fixed Cost ($)", value=200_000.0,
                                  step=10_000.0, format="%.0f")

    # ── Tax
    st.markdown("### Tax")
    tax_rate = st.slider("Corporate Tax Rate (%)", 0, 50, 25) / 100

    # ── WACC Inputs
    st.markdown("### WACC Components")
    cost_equity = st.slider("Cost of Equity (%)", 0.0, 30.0, 10.0, 0.1) / 100
    cost_debt   = st.slider("Cost of Debt (%)", 0.0, 20.0, 5.0, 0.1) / 100
    debt_pct    = st.slider("Debt Weight (%)", 0, 100, 40) / 100
    equity_pct  = 1 - debt_pct

    wacc = equity_pct * cost_equity + debt_pct * cost_debt * (1 - tax_rate)

    st.markdown(f"""
    <div class="info-box">
    Equity: {pct(equity_pct)} &nbsp;|&nbsp; Debt: {pct(debt_pct)}<br>
    WACC = <strong style="color:#58a6ff">{pct(wacc)}</strong>
    </div>
    """, unsafe_allow_html=True)

    # ── Discount Rate Override
    st.markdown("### Discount Rate")
    use_wacc = st.checkbox("Use WACC as discount rate", value=True)
    if use_wacc:
        discount_rate = wacc
        st.markdown(f'<span style="color:#8b949e;font-size:0.82rem;font-family:\'DM Mono\',monospace">Discount rate = WACC = {pct(wacc)}</span>', unsafe_allow_html=True)
    else:
        discount_rate = st.slider("Manual Discount Rate (%)", 1.0, 30.0,
                                   round(wacc * 100, 1), 0.1) / 100


# ── Core calculations ─────────────────────────────────────────────────────────
gross_profits = [rev - vc for rev, vc in zip(revenues, var_costs)]
ebits         = [gp - fixed_cost for gp in gross_profits]
taxes         = [max(0, e) * tax_rate for e in ebits]
net_ebits     = [e - t for e, t in zip(ebits, taxes)]
fcfs          = [e * (1 - tax_rate) for e in ebits]   # FCF = EBIT × (1 - tax)

# NPV
npv = sum(fcf / (1 + discount_rate) ** (i + 1) for i, fcf in enumerate(fcfs))
total_fcf = sum(fcfs)


# ── Main layout ───────────────────────────────────────────────────────────────
st.markdown("""
<h1 style='font-family:"DM Serif Display",serif; color:#e6edf3; margin-bottom:4px; font-size:2.4rem;'>
  Financial Model
</h1>
<p style='color:#8b949e; font-family:"DM Mono",monospace; font-size:0.82rem; letter-spacing:0.08em; margin-top:0;'>
  4-YEAR DCF & FREE CASH FLOW ANALYSIS
</p>
""", unsafe_allow_html=True)

# ── KPI row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
kpis = [
    ("Net Present Value",     fmt(npv),         f"@ {pct(discount_rate)} discount rate"),
    ("Total Free Cash Flow",  fmt(total_fcf),    "Undiscounted 4-year sum"),
    ("WACC",                  pct(wacc),         f"E:{pct(equity_pct)} · D:{pct(debt_pct)}"),
    ("Avg. EBIT Margin",      pct(sum(e/r for e,r in zip(ebits,revenues))/4),
                              "Average over 4 years"),
]
for col, (label, value, sub) in zip([k1, k2, k3, k4], kpis):
    with col:
        st.markdown(f"""
        <div class="metric-card">
          <div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div>
          <div class="metric-sub">{sub}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Income statement table ────────────────────────────────────────────────────
st.markdown('<div class="section-title">Income Statement & FCF</div>', unsafe_allow_html=True)

def row(label, values, cls="", prefix="$"):
    cells = "".join(f"<td>{fmt(v, prefix)}</td>" for v in values)
    return f'<tr class="{cls}"><td>{label}</td>{cells}</tr>'

table_html = f"""
<table class="styled-table">
  <thead>
    <tr>
      <th></th>
      {''.join(f'<th>{y}</th>' for y in years)}
    </tr>
  </thead>
  <tbody>
    {row("Revenue", revenues)}
    {row("Variable Costs", [-v for v in var_costs])}
    {row("Gross Profit", gross_profits)}
    {row("Fixed Costs", [-fixed_cost]*4)}
    {row("EBIT", ebits, "row-ebit")}
    {row("Tax ({:.0f}%)".format(tax_rate*100), [-t for t in taxes])}
    {row("Free Cash Flow", fcfs, "row-fcf")}
    <tr class="row-total">
      <td>Discounted FCF</td>
      {''.join(f'<td style="color:#f0883e">{fmt(fcf/(1+discount_rate)**(i+1))}</td>' for i, fcf in enumerate(fcfs))}
    </tr>
  </tbody>
</table>
"""
st.markdown(table_html, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Visual Overview</div>', unsafe_allow_html=True)

ch1, ch2 = st.columns(2)

with ch1:
    chart_data = pd.DataFrame({
        "Revenue":      revenues,
        "Gross Profit": gross_profits,
        "EBIT":         ebits,
        "Free CF":      fcfs,
    }, index=years)
    st.caption("Revenue & Profitability Waterfall")
    st.bar_chart(chart_data, color=["#58a6ff","#3fb950","#f0883e","#bc8cff"])

with ch2:
    margin_data = pd.DataFrame({
        "Gross Margin %": [gp/r*100 for gp, r in zip(gross_profits, revenues)],
        "EBIT Margin %":  [e/r*100  for e,  r in zip(ebits,         revenues)],
        "FCF Margin %":   [f/r*100  for f,  r in zip(fcfs,          revenues)],
    }, index=years)
    st.caption("Margin Trends (%)")
    st.line_chart(margin_data, color=["#3fb950","#58a6ff","#f0883e"])

# ── Sensitivity analysis ──────────────────────────────────────────────────────
st.markdown('<div class="section-title">Sensitivity Analysis — Discount Rate vs NPV</div>', unsafe_allow_html=True)

rates = [r/100 for r in range(5, 21)]
sens_rows = []
for r in rates:
    npv_r = sum(fcf / (1 + r) ** (i + 1) for i, fcf in enumerate(fcfs))
    delta  = npv_r - npv
    sens_rows.append({
        "Discount Rate": pct(r),
        "NPV":           fmt(npv_r),
        "vs Current":    ("+" if delta >= 0 else "") + fmt(delta),
        "NPV Raw":       npv_r,
        "Delta Raw":     delta,
        "Rate Raw":      r,
    })

# Build HTML table
sens_header = "<tr><th>Discount Rate</th><th>NPV</th><th>Δ vs Current</th></tr>"
sens_body = ""
for row_d in sens_rows:
    is_current = abs(row_d["Rate Raw"] - discount_rate) < 0.001
    delta_color = "color:#f85149" if row_d["Delta Raw"] < 0 else "color:#3fb950"
    row_cls = ' style="background:#1f2d1f;"' if is_current else ""
    npv_color = "color:#3fb950" if is_current else ""
    marker = " ◀ current" if is_current else ""
    sens_body += f"""
    <tr{row_cls}>
      <td style="text-align:left; font-family:'DM Mono',monospace; {'color:#58a6ff;font-weight:600' if is_current else ''}">{row_d['Discount Rate']}{marker}</td>
      <td style="{npv_color}">{row_d['NPV']}</td>
      <td style="{delta_color}">{row_d['vs Current']}</td>
    </tr>"""

sens_html = f"""
<table class="sens-table">
  <thead>{sens_header}</thead>
  <tbody>{sens_body}</tbody>
</table>
"""

s_col, _ = st.columns([1, 1])
with s_col:
    st.markdown(sens_html, unsafe_allow_html=True)

with _:
    sens_df = pd.DataFrame({
        "Rate (%)": [r * 100 for r in rates],
        "NPV":      [r["NPV Raw"] for r in sens_rows],
    }).set_index("Rate (%)")
    st.caption("NPV curve across discount rates")
    st.line_chart(sens_df, color=["#58a6ff"])

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<br>
<div style="border-top:1px solid #21262d; padding-top:16px; text-align:center;
     font-family:'DM Mono',monospace; font-size:0.72rem; color:#484f58; letter-spacing:0.08em;">
  FCF = EBIT × (1 − Tax Rate) &nbsp;|&nbsp; NPV = Σ FCFₜ / (1 + r)ᵗ &nbsp;|&nbsp;
  WACC = Ke × We + Kd × Wd × (1 − Tax)
</div>
""", unsafe_allow_html=True)
