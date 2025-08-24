import time
import streamlit as st  # type: ignore
from components.ui import inject_css, topbar
from tabs import control_room, data_health, model_status, drift_fairness, recovery, explainability, reports


st.set_page_config(page_title="PulseAI — Ultra", layout="wide", page_icon="⚙️")
inject_css()

# --------- Auth config ---------
USER = "Devanjan123"
PASS = "Dev123"

LOGIN_BG_URL = "https://multisite.talent500.co/talent500-blog/wp-content/uploads/sites/42/2025/01/Machine-Learning.jpg"

def _apply_login_css(bg_url: str):
    """Full-viewport background; left-half login card; no scroll."""
    st.markdown(
        f"""
        <style>
          /* hide Streamlit chrome on login */
          header[data-testid="stHeader"], div[data-testid="stToolbar"], #MainMenu, footer {{
            display: none !important; visibility: hidden !important;
          }}

          /* background image + overlay on the whole app view */
          [data-testid="stAppViewContainer"] {{
            background: linear-gradient(rgba(8,12,24,0.65), rgba(8,12,24,0.65)),
                        url('{bg_url}') center / cover no-repeat fixed !important;
          }}

          /* one-screen layout; center vertically, align LEFT horizontally */
          [data-testid="stAppViewContainer"] > .main {{
            min-height: 100vh;
            display: grid;
            align-content: center;      /* vertical centering */
            justify-items: start;       /* LEFT align the card */
            padding: 0 !important;
          }}

          /* LEFT half card (≈50% width), with glass look */
          main .block-container {{
            width: 50vw;                /* <<< left half */
            max-width: 720px;           /* keep it reasonable on very wide screens */
            margin-left: 6vw;           /* gutter from the very left */
            padding: 28px !important;
            background: rgba(20,26,50,.65);
            border: 1px solid rgba(255,255,255,.12);
            border-radius: 16px;
            box-shadow: 0 18px 48px rgba(0,0,0,.45);
            backdrop-filter: blur(6px);
          }}

          /* rounded inputs + icons (like your reference) */
          .login-title {{ color:#eef1ff; font-weight:800; font-size: 2rem; margin: 0 0 .25rem 0; }}
          .login-sub   {{ color:#a3a7c7; margin-bottom: 1rem; }}

          .login-card [data-testid="stTextInput"] {{ position: relative; margin-bottom: .6rem; }}
          .login-card [data-testid="stTextInput"] input {{
            height: 44px; border-radius: 999px !important; padding-right: 46px;
            background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.12);
          }}
          .login-card [data-testid="stTextInput"]:nth-of-type(1)::after {{
            content: "👤"; position: absolute; right: 14px; top: 36px; font-size: 18px; opacity: .8;
          }}
          .login-card [data-testid="stTextInput"]:nth-of-type(2)::after {{
            content: "🔒"; position: absolute; right: 14px; top: 36px; font-size: 18px; opacity: .8;
          }}

          .login-card button[kind="primary"] {{
            border-radius: 999px !important;
            background: #ffffff !important; color: #0f1220 !important;
            border: none; height: 44px; font-weight: 700;
          }}

          .login-meta {{ display:flex; align-items:center; justify-content:space-between; margin: .25rem 4px 1rem 4px; color:#d9def7; }}
          .login-meta a {{ color:#d9def7; text-decoration: none; opacity: .9; }}
          .login-meta a:hover {{ text-decoration: underline; }}

          .login-bottom {{ text-align:left; margin-top:.6rem; color:#d9def7; opacity:.9; }}
          .login-bottom a {{ color:#fff; font-weight:700; text-decoration:none; }}
          .login-bottom a:hover {{ text-decoration:underline; }}

          /* lock scroll on login page */
          html, body {{ height: 100vh; overflow: hidden; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _clear_login_css():
    """Restore normal app layout after login."""
    st.markdown(
        """
        <style>
          [data-testid="stAppViewContainer"] { background: unset !important; }
          [data-testid="stAppViewContainer"] > .main { display: block; min-height: auto; }
          html, body { overflow: auto; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def init_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

def login_view():
    _apply_login_css(LOGIN_BG_URL)

    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">Login</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-sub">Sign in to access the control room.</div>', unsafe_allow_html=True)

    with st.form("login-form", clear_on_submit=False):
        u = st.text_input("Username", value="", placeholder="Enter username")
        p = st.text_input("Password", value="", placeholder="Enter password", type="password")

        # remember/forgot row
        st.markdown(
            '''
            <div class="login-meta">
              <label><input type="checkbox" style="transform:translateY(2px); margin-right:6px;"> Remember Me</label>
              <a href="#">Forgot Password?</a>
            </div>
            ''',
            unsafe_allow_html=True,
        )

        submitted = st.form_submit_button("Login", use_container_width=True)

    if submitted:
        if u == USER and p == PASS:
            ph = st.empty()
            ph.markdown('<div class="auth-anim"><div class="ring"></div>Authenticating…</div>', unsafe_allow_html=True)
            time.sleep(1.0)
            st.session_state.logged_in = True
            ph.empty()
            st.success("Welcome! Redirecting…")
            time.sleep(0.5)
            st.rerun()
        else:
            st.error("Invalid credentials. Try again.")

    st.markdown(
        '<div class="login-bottom">Don\'t have an account? <a href="#">Register</a></div>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)  # /login-card

# --------- Router ---------
def _app():
    topbar(title="PulseAI", org="Company XYZ", role="Business Viewer")
    tabs = {
        "🏠 Control Room": control_room.render,
        "📊 Model Status": model_status.render,
        "📉 Drift & Fairness": drift_fairness.render,
        "🧪 Data Health": data_health.render,
        "🛟 Recovery": recovery.render,
        "🧠 Explainability": explainability.render,
        "📄 Report": reports.render,

        # "🧰 Pipelines (E1)": pipelines.render,     # reserved for Engineer 1 — commented
        # "📈 Monitoring (E2)": monitoring.render,   # reserved for Engineer 2 — commented
        # "🧩 Serving API (E3)": serving.render,     # reserved for Engineer 3 — commented
    }
    st.sidebar.title("Navigation")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    choice = st.sidebar.radio("Go to", list(tabs.keys()), index=0)
    tabs[choice]()

# --------- Entry ---------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login_view()
    st.stop()

_clear_login_css()
_app()
