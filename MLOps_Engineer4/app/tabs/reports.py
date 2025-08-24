import io
from datetime import datetime
import streamlit as st # type: ignore
import pandas as pd
import plotly.express as px # type: ignore
import plotly.graph_objects as go # type: ignore
from reportlab.lib.pagesizes import A4 # type: ignore
from reportlab.pdfgen import canvas # type: ignore
from reportlab.lib.utils import ImageReader # type: ignore
from utils.data import load_json, dummy_dir

def _fig_bytes(fig, w=1000, h=600, scale=2):
    # Requires kaleido
    return fig.to_image(format="png", width=w, height=h, scale=scale)

def _draw_title(c, title):
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, 810, title)
    c.setFont("Helvetica", 10)
    c.drawString(40, 795, f"Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")

def _draw_image(c, img_bytes, x, y, w):
    img = ImageReader(io.BytesIO(img_bytes))
    iw, ih = img.getSize()
    h = w * ih / iw
    c.drawImage(img, x, y, width=w, height=h, preserveAspectRatio=True, mask='auto')
    return h

def render():
    st.title("Report")
    st.caption(f"Source: {dummy_dir()}")

    ms = load_json("model_status.json")
    ts = load_json("metrics_timeseries.json")
    drift = load_json("drift_timeline.json")
    fair = load_json("fairness.json")
    val = load_json("validation.json")

    # ----- Build charts -----
    df_perf = pd.DataFrame({"date": ts["dates"], "accuracy": ts["accuracy"], "precision": ts["precision"], "recall": ts["recall"]})
    perf_melt = df_perf.melt(id_vars="date", var_name="metric", value_name="value")
    fig_perf = px.line(perf_melt, x="date", y="value", color="metric", markers=True, title="Accuracy / Precision / Recall")

    df_drift = pd.DataFrame({"date": drift["dates"], "p_value": drift["p_value"]})
    fig_drift = px.line(df_drift, x="date", y="p_value", markers=True, title="Drift p-value (lower → more drift)")

    df_fair = pd.DataFrame(fair)
    fig_fair = px.bar(df_fair, x="group", y="accuracy", title="Accuracy by Group")

    mv = pd.DataFrame(list(val.get("missing_values", {}).items()), columns=["column", "missing_count"])
    fig_mv = px.bar(mv, x="column", y="missing_count", title="Missing Values by Column")

    # ----- Compose PDF -----
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    W, H = A4

    # Page 1: Title + KPIs + Perf chart
    _draw_title(c, "PulseAI Reliability Report")
    c.setFont("Helvetica", 11)
    c.drawString(40, 770, f"Active Model: {ms.get('active_model','-')}")
    c.drawString(220, 770, f"Accuracy: {ms.get('accuracy',0):.3f}")
    c.drawString(360, 770, f"Precision: {ms.get('precision',0):.3f}")
    c.drawString(500, 770, f"Recall: {ms.get('recall',0):.3f}")
    c.drawString(40, 755, f"Last Trained: {ms.get('last_trained','N/A')}")

    y = 740
    img_h = _draw_image(c, _fig_bytes(fig_perf), x=40, y=y-300, w=W-80)
    c.showPage()

    # Page 2: Drift + Fairness
    _draw_title(c, "Drift & Fairness")
    y = 760
    img_h = _draw_image(c, _fig_bytes(fig_drift), x=40, y=y-300, w=W-80)
    y = y - img_h - 40
    _draw_image(c, _fig_bytes(fig_fair), x=40, y=y-280, w=W-80)
    c.showPage()

    # Page 3: Data Health (Missing Values)
    _draw_title(c, "Data Health")
    _draw_image(c, _fig_bytes(fig_mv), x=40, y=420, w=W-80)
    c.showPage()

    c.save()
    pdf_bytes = buf.getvalue()

    st.download_button(
        "📄 Download PDF Report",
        data=pdf_bytes,
        file_name="pulseai_report.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

    st.info("This PDF includes KPIs and the key charts only (not the whole webpage).")
