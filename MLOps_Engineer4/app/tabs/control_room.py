import streamlit as st  # type: ignore
import pandas as pd
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
from utils.data import load_json, dummy_dir

def sparkline(series):
    df = pd.DataFrame({"x": list(range(len(series))), "y": series})
    fig = px.line(df, x="x", y="y")
    fig.update_layout(height=80, margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    return fig

def render():
    st.title("Control Room")
    st.caption(f"Source: {dummy_dir()}")

    meta = load_json("control_meta.json")
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Operator ID", f"{meta['operator_id']}")
    c2.metric("Batches Today", f"{meta['batches_today']}")
    c3.metric("Drift Alerts (24h)", f"{meta['drift_alerts_24h']}")
    c4.metric("OOC%", f"{meta['ooc_percent']:.2f}%")
    c5.metric("Queue", f"{meta['queue']}")

    # Radial gauge for Time to completion
    st.subheader("Time to completion")
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=float(meta.get("time_to_completion", 0)),
        number={'suffix': " min"},
        gauge={
            'axis': {'range': [0, 120]},
            'bar': {'color': "#22c55e"},
            'steps': [
                {'range': [0, 60], 'color': "rgba(34,197,94,.2)"},
                {'range': [60, 90], 'color': "rgba(245,158,11,.2)"},
                {'range': [90, 120], 'color': "rgba(239,68,68,.2)"},
            ],
        },
        domain={'x': [0, 1], 'y': [0, 1]},
    ))
    gauge.update_layout(height=260, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(gauge, use_container_width=True)

    st.markdown("### Process Control Metrics Summary")
    params = load_json("parameters.json")

    # Grid of parameter rows
    for p in params:
        with st.container():
            c1, c2, c3, c4 = st.columns([1.5, 3, 1.5, 1])
            c1.write(f"**{p['name']}**")
            c2.plotly_chart(sparkline(p['spark']), use_container_width=True)
            # Backward-compatible progress text
            val = min(1.0, float(p['ooc']) / 100.0)
            try:
                c3.progress(val, text=f"OOC {p['ooc']:.2f}%")
            except TypeError:
                c3.progress(val)
            c4.write("✅" if p['pass'] else "❌")

    st.markdown("---")
    st.subheader("Live SPC Chart")
    spc = load_json("spc.json")
    df = pd.DataFrame({"batch": spc["batch"], "value": spc["value"]})
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["batch"],
        y=df["value"],
        mode="lines+markers",
        name="Process",
        line_shape="spline",
    ))
    fig.add_hline(y=spc["ucl"], line_dash="dash", line_color="red",
        annotation_text="UCL", annotation_position="top left")
    fig.add_hline(y=spc["lcl"], line_dash="dash", line_color="red",
        annotation_text="LCL", annotation_position="bottom left")
    fig.add_hline(y=spc["mean"], line_dash="dot", line_color="orange",
        annotation_text="Mean")
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=360)
    st.plotly_chart(fig, use_container_width=True)

    cleft, cright = st.columns([3, 1.2])
    with cleft:
        st.subheader("OOC Distribution by Parameter")
        donut = load_json("ooc_breakdown.json")
        pie_df = pd.DataFrame({"parameter": donut["parameter"], "ooc": donut["ooc"]})
        pie = px.pie(pie_df, values="ooc", names="parameter", hole=0.55)
        st.plotly_chart(pie, use_container_width=True)
    with cright:
        st.subheader("Value Histogram")
        # Robust horizontal histogram
        hist = go.Figure(go.Histogram(y=df["value"], nbinsy=18, orientation="h"))
        hist.update_layout(height=320, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(hist, use_container_width=True)
