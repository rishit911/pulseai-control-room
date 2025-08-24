from pathlib import Path
import streamlit as st

def _assets() -> Path:
    return Path(__file__).resolve().parents[1] / "assets"

def inject_css():
    css = (_assets() / "styles.css").read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

def topbar(title: str, org: str, role: str):
    st.markdown(f'''
    <div class="topbar">
        <div class="brand">
            <div class="logo-spin"></div>
            <span class="brand-text">{title}</span>
        </div>
        <div class="badges">
            <span class="badge">Org: {org}</span>
            <span class="badge badge-role">{role}</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
