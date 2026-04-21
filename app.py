import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import os
import re
from datetime import date
import streamlit.components.v1 as components
import csv
import hashlib

st.set_page_config(page_title="SIERA", layout="wide")

# ======================
# SIMPLE AUTHENTICATION
# ======================
# Prioritas: Secrets → Environment Variables (Railway) → Default
secrets_missing = False
try:
    USERNAME = st.secrets["username"]
    PASSWORD_HASH = st.secrets["password_hash"]
except (KeyError, FileNotFoundError):
    username_env = os.environ.get("username")
    password_hash_env = os.environ.get("password_hash")
    
    if username_env and password_hash_env:
        USERNAME = username_env
        PASSWORD_HASH = password_hash_env
    else:
        USERNAME = "peksiv"
        PASSWORD_HASH = "de614bf29764c5dd46f33d6dfe3d2b5a098a34fc06ad1da36f13987393dd7fd6"
        secrets_missing = True

st.session_state.setdefault("authenticated", False)
st.session_state.setdefault("username", "")
st.session_state.setdefault("login_time", None)

if not st.session_state.get("authenticated", False):
    try:
        with open("PEKS IV Logo Colour.png", "rb") as f:
            login_logo = base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        login_logo = ""

    st.markdown(
        """
        <style>
        * { box-sizing: border-box; }
        html, body, .stApp, .main, .block-container {
            background: radial-gradient(circle at top, #eef2ff 0%, #dbeafe 25%, #f8fafc 55%, #ffffff 100%) !important;
            color: #0f172a !important;
            min-height: 100vh !important;
        }
        .appview-container { background: radial-gradient(circle at top, #eef2ff 0%, #dbeafe 25%, #f8fafc 55%, #ffffff 100%) !important; }
        .main { 
            background: transparent !important; 
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            min-height: 100vh !important;
        }
        .block-container {
            background: transparent !important;
            box-shadow: none !important;
            padding: 20px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            min-height: 100vh !important;
            max-width: 100% !important;
        }
        .stForm, form {
            width: 100% !important;
            max-width: 420px !important;
            padding: 32px !important;
            border-radius: 28px !important;
            background: rgba(255, 255, 255, 0.98) !important;
            border: 1px solid rgba(148, 163, 184, 0.28) !important;
            box-shadow: 0 36px 70px rgba(15, 23, 42, 0.12) !important;
        }
        .stForm > div {
            gap: 14px !important;
        }
        .login-logo-wrap {
            width: 80px;
            height: 80px;
            margin: 0 auto 14px;
            border-radius: 22px;
            background: #ffffff;
            display: grid;
            place-items: center;
            border: 1px solid rgba(148, 163, 184, 0.25);
        }
        .login-logo-wrap img {
            width: 48px;
            height: auto;
        }
        .login-brand {
            margin: 0;
            font-size: 32px;
            font-weight: 900;
            text-align: center;
            color: #0b1120;
            letter-spacing: -0.03em;
        }
        .login-tagline {
            margin: 0;
            text-align: center;
            color: #334155;
            font-size: 13px;
            line-height: 1.6;
            letter-spacing: 0.01em;
        }
        .stTextInput>div>label {
            display: none !important;
        }
        .stTextInput>div>div>input {
            background: #f8fafc !important;
            border: 1px solid rgba(148, 163, 184, 0.4) !important;
            border-radius: 16px !important;
            padding: 16px 18px !important;
            color: #0f172a !important;
        }
        .stTextInput>div>div>input::placeholder {
            color: #94a3b8 !important;
        }
        .stTextInput {
            margin-bottom: 16px !important;
        }
        .stButton>button {
            width: 100% !important;
            background: #1d4ed8 !important;
            color: #ffffff !important;
            border-radius: 16px !important;
            padding: 14px 0 !important;
            font-weight: 700 !important;
            border: none !important;
            box-shadow: 0 16px 32px rgba(30, 58, 138, 0.18) !important;
        }
        .stButton>button:hover {
            background: #1e40af !important;
        }
        .login-footer {
            margin-top: 4px;
            text-align: center;
            color: #475569;
            font-size: 13px;
            line-height: 1.5;
        }
        @media (max-width: 640px) {
            .stForm { padding: 32px 24px !important; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="login-page">', unsafe_allow_html=True)
    with st.form("login_form"):
        st.markdown(
            f"""
            <div class="login-logo-wrap"><img src="data:image/png;base64,{login_logo}" alt="PEKS IV"></div>
            <h1 class="login-brand">Dashboard SIERA</h1>
            <div class="login-tagline">Silakan masukkan ID dan Kata sandi Anda</div>
            """,
            unsafe_allow_html=True,
        )
        username = st.text_input("ID Login", placeholder="ID Login")
        password = st.text_input("Kata sandi", type="password", placeholder="Kata sandi")
        submit = st.form_submit_button("Masuk")
        st.markdown(
            """
            <div class="login-footer">Direktorat Pengendalian dan Evaluasi Kebijakan Strategis IV</div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        if username == USERNAME and hashlib.sha256(password.encode()).hexdigest() == PASSWORD_HASH:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.login_time = date.today().isoformat()
            st.success("Login berhasil!")
            st.rerun()
        else:
            st.error("Username atau password salah!")
            if secrets_missing:
                st.info("Jika belum mengatur Streamlit Secrets, gunakan ID Login: `peksiv` dan Kata sandi: `latsar`.")

    if not st.session_state.get("authenticated", False) and secrets_missing:
        st.warning("Streamlit Secrets belum terpasang. Login default berada pada ID `peksiv` dan kata sandi `latsar`.")

    st.stop()

# ======================
# CSS
# ======================
st.markdown(
    """
<style>
body, .stApp, table, th, td, input, textarea, select, button {
    font-family: "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 14px;
    line-height: 1.6;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e3a5f 50%, #2d5a8c 100%);
    padding-top: 12px;
    padding-bottom: 140px;
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

section[data-testid="stSidebar"] > div:first-child {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

section[data-testid="stSidebar"] .stButton > button {
    width: 100%;
    max-width: 220px;
}

.sidebar-welcome {
    color: #f8fafc;
    font-weight: 600;
    margin: 6px 0 10px 0;
    font-size: 15px;
}

.logo-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-bottom: 12px;
}

.logo-img {
    width: 120px;
    margin-bottom: 8px;
}

.logo-title {
    color: white;
    font-size: 20px;
    font-weight: bold;
    text-align: center;
}

.logo-sub {
    color: #cbd5e1;
    font-size: 11px;
    text-align: center;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    padding: 10px 14px !important;
    border-radius: 10px !important;
    color: white !important;
    font-size: 14px !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] input {
    display: none;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: #334155 !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label[data-selected="true"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    font-weight: bold !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label * {
    color: white !important;
}

.stButton > button {
    margin: 0 auto;
    display: block;
}

.sidebar-spacer {
    flex: 1;
    min-height: 220px;
}

.button-right {
    text-align: right;
}

.button-right .stButton > button {
    margin-left: auto !important;
    margin-right: 0 !important;
}

.dashboard-hero {
    position: relative;
    background: rgba(255, 255, 255, 0.22);
    border: 1px solid rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-radius: 32px;
    padding: 34px 36px;
    color: #0f172a;
    box-shadow: 0 24px 70px rgba(15, 23, 42, 0.12);
    margin-bottom: 28px;
    overflow: hidden;
}

.dashboard-hero::before {
    content: "";
    position: absolute;
    top: -40px;
    right: -40px;
    width: 220px;
    height: 220px;
    background: radial-gradient(circle at center, rgba(59, 130, 246, 0.24), transparent 60%);
    pointer-events: none;
}

.dashboard-hero::after {
    content: "";
    position: absolute;
    bottom: -40px;
    left: -40px;
    width: 220px;
    height: 220px;
    background: radial-gradient(circle at center, rgba(16, 185, 129, 0.18), transparent 55%);
    pointer-events: none;
}

.dashboard-hero h1 {
    margin: 0;
    font-size: 42px;
    line-height: 1.05;
}

.dashboard-hero p {
    margin: 12px 0 0 0;
    color: rgba(15, 23, 42, 0.8);
    font-size: 16px;
    max-width: 860px;
}

.dashboard-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 22px 45px rgba(15, 23, 42, 0.08);
    margin-bottom: 20px;
}

.dashboard-card h3 {
    margin: 0 0 10px 0;
    font-size: 18px;
    color: #0f172a;
}

.dashboard-card .metric {
    margin: 0;
    font-size: 38px;
    font-weight: 700;
    color: #1e3a8a;
}

.dashboard-card .metric-label {
    margin: 8px 0 0 0;
    color: #475569;
    font-size: 14px;
}

.dashboard-small-card {
    background: #ffffff;
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 18px 38px rgba(15, 23, 42, 0.06);
    margin-bottom: 20px;
}

.dashboard-small-card p {
    margin: 0;
    color: #475569;
}

    .page-section-card {
        position: relative;
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid rgba(148, 163, 184, 0.18);
        backdrop-filter: blur(22px);
        -webkit-backdrop-filter: blur(22px);
        border-radius: 32px;
        padding: 32px;
        box-shadow: 0 28px 70px rgba(15, 23, 42, 0.12);
        margin-bottom: 26px;
        overflow: hidden;
    }

    .page-section-card::before {
        content: "";
        position: absolute;
        top: -24px;
        right: -24px;
        width: 220px;
        height: 220px;
        background: radial-gradient(circle at top right, rgba(59, 130, 246, 0.18), transparent 55%);
        pointer-events: none;
    }

    .page-section-card::after {
        content: "";
        position: absolute;
        bottom: -28px;
        left: -28px;
        width: 200px;
        height: 200px;
        background: radial-gradient(circle at bottom left, rgba(16, 185, 129, 0.14), transparent 55%);
        pointer-events: none;
    }

    .page-heading {
        display: flex;
        flex-direction: column;
        gap: 12px;
        position: relative;
        z-index: 1;
    }

    .heading-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(59, 130, 246, 0.14);
        color: #1d4ed8;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.02em;
        border: 1px solid rgba(59, 130, 246, 0.22);
        width: fit-content;
    }

    .page-heading-title {
        display: flex;
        align-items: center;
        gap: 18px;
        flex-wrap: wrap;
    }

    .page-heading-title h1 {
        margin: 0;
        font-size: 36px;
        font-weight: 800;
        color: #0f172a;
        letter-spacing: -0.03em;
    }

    .page-heading p {
        margin: 0;
        color: #475569;
        font-size: 15px;
        line-height: 1.8;
        max-width: 740px;
    }

    .chat-container {
        position: relative;
        width: 100%;
        max-width: 1080px;
        margin: 0 auto;
        padding-bottom: 220px;
    }

    .chat-form {
        position: fixed;
        bottom: 24px;
        left: 50%;
        transform: translateX(-50%);
        width: min(1080px, calc(100% - 48px));
        background: rgba(255, 255, 255, 0.98);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 28px;
        box-shadow: 0 28px 70px rgba(15, 23, 42, 0.12);
        padding: 24px;
        z-index: 999;
    }

    .chat-form .stTextArea > div {
        background: #f8fafc !important;
        border: 1px solid rgba(148, 163, 184, 0.24) !important;
        border-radius: 22px !important;
        padding: 16px 18px !important;
    }

    .chat-form .stTextArea textarea {
        min-height: 120px !important;
        border: none !important;
        outline: none !important;
        background: transparent !important;
        font-size: 16px !important;
        color: #0f172a !important;
        padding: 0 !important;
    }

    .chat-form .stTextArea textarea::placeholder {
        color: #94a3b8 !important;
    }

    .chat-form .stTextArea label {
        display: none !important;
    }

    .chat-form .stButton button {
        background-color: #2563eb !important;
        color: white !important;
        border-radius: 999px !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        border: none !important;
        margin-top: 12px !important;
    }

    .chat-form .stButton button:hover {
        background-color: #1d4ed8 !important;
    }

    .heading-deco {
        width: 48px;
        height: 48px;
        display: grid;
        place-items: center;
        border-radius: 16px;
        background: rgba(59, 130, 246, 0.12);
        color: #2563eb;
        font-size: 22px;
        border: 1px solid rgba(59, 130, 246, 0.19);
    }

    .section-subtitle {
        color: #64748b;
        font-size: 13px;
        margin-top: 4px;
    }

    .col-button-green button {
        background-color: #10b981 !important;
        color: white !important;
    }

    .col-button-green button:hover {
        background-color: #059669 !important;
    }


th, td {
    padding: 10px;
    border: 1px solid #d1d5db;
    vertical-align: top;
    font-family: "Inter", "Segoe UI", Roboto, sans-serif;
    font-size: 13px;
    line-height: 1.6;
}

table.detail-table th,
table.detail-table td {
    border: 1px solid #d1d5db;
    padding: 10px;
    vertical-align: top;
    font-family: "Inter", "Segoe UI", Roboto, sans-serif;
    font-size: 13px;
    line-height: 1.6;
}

/* Main content area - ensure light background */
main, .main, [data-testid="stAppViewContainer"] {
    background: #ffffff !important;
}

.block-container {
    background: #ffffff !important;
    color: #0f172a !important;
}

/* Ensure all text is dark on light background */
body, .stApp {
    background: #ffffff !important;
    color: #0f172a !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ======================
# HELPERS
# ======================
def strip_html(text):
    if pd.isna(text):
        return ""
    return re.sub(r"<[^>]+>", "", str(text))

def normalize_detail_text(value):
    if pd.isna(value):
        return ""
    text = str(value)
    text = text.replace("\\r\\n", "\n").replace("\\n", "\n").replace("\\r", "\n")
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("\n", "<br>")
    return text

def save_row_to_csv(row):
    df_row = pd.DataFrame([row])
    df_row.to_csv(
        DATA_PATH,
        mode="a",
        header=not os.path.exists(DATA_PATH) or os.path.getsize(DATA_PATH) == 0,
        index=False,
        quoting=csv.QUOTE_ALL,
        escapechar="\\",
        lineterminator="\n",
        encoding="utf-8-sig",
    )


def get_next_temuan_number(nd_value, dataframe):
    existing = (
        dataframe[dataframe["Nomor ND Pemeriksaan"] == nd_value]["ID_Temuan"]
        .dropna()
        .astype(str)
    )
    nums = []
    for val in existing:
        try:
            nums.append(int(val.split(".")[0]))
        except ValueError:
            continue
    return max(nums, default=0) + 1


# ======================
# SIDEBAR
# ======================
with st.sidebar:
    try:
        with open("Logo_PEKS_IV.png", "rb") as f:
            logo = base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        logo = ""

    st.markdown(
        f"""
    <div class="logo-container">
        <img src="data:image/png;base64,{logo}" class="logo-img"/>
        <div class="logo-title">SIERA</div>
        <div class="logo-sub">Sistem Informasi Evaluasi dan Referensi Analisis Hasil Pengawasan dan Pemeriksaan Kinerja Pembangunan Lingkup Direktorat PEKS IV</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Show user info
    if st.session_state.get("authenticated", False):
        st.markdown(f"<div class='sidebar-welcome'>Welcome, <strong>{st.session_state.get('username', '')}</strong>!</div>", unsafe_allow_html=True)
        st.markdown("---")

    menu = st.radio(
        "",
        ["Beranda", "Daftar Pemeriksaan", "TLHP PEKS IV", "AI SIERA"],
    )

    st.markdown("<div class='sidebar-spacer'></div>", unsafe_allow_html=True)

    if st.button("🚪 Logout", key="sidebar_logout"):
        st.session_state.authenticated = False
        st.session_state.username = ""
        st.session_state.login_time = None
        st.rerun()

# ======================
# LOAD DATA
# ======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data.csv")
TLHP_DATA_PATH = os.path.join(BASE_DIR, "tlhp_data.csv")

EXPECTED_COLUMNS = [
    "Tanggal",
    "Instansi",
    "Tema",
    "Topik",
    "Nomor ND Pemeriksaan",
    "Nomor ND Tanggapan",
    "ID_Temuan",
    "Temuan",
    "ID_Kondisi",
    "Kondisi/Rekomendasi",
    "Uraian",
    "Tanggapan PEKS IV",
    "Dokumen Pendukung",
]

TLHP_COLUMNS = [
    "No",
    "Nama Laporan",
    "Tgl Laporan",
    "Tahun",
    "Pengawas",
    "Temuan",
    "Resuma Kondisi",
    "Rekomendasi",
    "Kode Rekomendasi",
    "Lead UKE I",
    "Lead UKE II",
    "UKE II (Koordinasi)",
    "UKE I (Koordinasi)",
    "Rencana Aksi",
    "Deadline",
    "Progress Pelaksanaan Rencana Aksi",
    "Data Dukung (LinkPortal)",
    "Submit",
    "Tgl Submit",
    "Catatan Penyulut",
    "Catatan Eksternal",
    "Hasil Validasi Pengawasan",
    "Status Penyelesaian",
]

def create_empty_data():
    pd.DataFrame(columns=EXPECTED_COLUMNS).to_csv(
        DATA_PATH,
        index=False,
        quoting=csv.QUOTE_ALL,
    )

def load_data():
    if not os.path.exists(DATA_PATH):
        create_empty_data()

    # Try multiple encodings
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
    for encoding in encodings:
        try:
            return pd.read_csv(
                DATA_PATH,
                dtype=str,
                keep_default_na=False,
                engine="python",
                quotechar='"',
                escapechar="\\",
                on_bad_lines="skip",
                encoding=encoding,
            )
        except (UnicodeDecodeError, LookupError):
            continue
    
    # If all encodings fail, return empty dataframe
    return pd.DataFrame(columns=EXPECTED_COLUMNS)

def create_empty_tlhp_data():
    pd.DataFrame(columns=TLHP_COLUMNS).to_csv(
        TLHP_DATA_PATH,
        index=False,
        quoting=csv.QUOTE_ALL,
    )

def load_tlhp_data():
    if not os.path.exists(TLHP_DATA_PATH):
        create_empty_tlhp_data()

    # Try multiple encodings
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
    for encoding in encodings:
        try:
            return pd.read_csv(
                TLHP_DATA_PATH,
                dtype=str,
                keep_default_na=False,
                engine="python",
                quotechar='"',
                escapechar="\\",
                on_bad_lines="skip",
                encoding=encoding,
            )
        except (UnicodeDecodeError, LookupError):
            continue
    
    # If all encodings fail, return empty dataframe
    return pd.DataFrame(columns=TLHP_COLUMNS)

def save_tlhp_row_to_csv(row):
    df_row = pd.DataFrame([row])
    df_row.to_csv(
        TLHP_DATA_PATH,
        mode="a",
        header=not os.path.exists(TLHP_DATA_PATH) or os.path.getsize(TLHP_DATA_PATH) == 0,
        index=False,
        quoting=csv.QUOTE_ALL,
        escapechar="\\",
        lineterminator="\n",
        encoding="utf-8-sig",
    )

df = load_data()
df.columns = df.columns.str.strip()

df_tlhp = load_tlhp_data()
df_tlhp.columns = df_tlhp.columns.str.strip()

if "ND_Pemeriksaan" in df.columns:
    df = df.rename(columns={"ND_Pemeriksaan": "Nomor ND Pemeriksaan"})

# ======================
# BERANDA
# ======================
if menu == "Beranda":
    st.markdown(
        """
        <div class='dashboard-hero'>
            <h1>Dashboard SIERA</h1>
            <p>SIERA - Sistem Informasi Evaluasi dan Referensi Analisis Hasil Pengawasan dan Pemeriksaan Kinerja Pembangunan Lingkup Direktorat PEKS IV</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    total_pemeriksaan = df["Nomor ND Pemeriksaan"].nunique() if not df.empty else 0
    total_instansi = df["Instansi"].nunique() if not df.empty else 0
    total_tema = df["Tema"].nunique() if not df.empty else 0
    total_tlhp = df_tlhp["Nama Laporan"].nunique() if not df_tlhp.empty else 0

    count_lead_uke_ii = 0
    count_uke_koord = 0
    status_counts = pd.Series(dtype=int)
    if not df_tlhp.empty:
        peks_iv_filter = (
            df_tlhp["Lead UKE II"].fillna("").str.strip().str.lower().str.contains("peks iv", case=False, na=False)
            | df_tlhp["UKE II (Koordinasi)"].fillna("").str.strip().str.lower().str.contains("peks iv", case=False, na=False)
        )
        df_peks_iv = df_tlhp[peks_iv_filter]
        count_lead_uke_ii = df_peks_iv["Lead UKE II"].fillna("").str.strip().str.lower().str.contains("peks iv", case=False, na=False).sum()
        count_uke_koord = df_peks_iv["UKE II (Koordinasi)"].fillna("").str.strip().str.lower().str.contains("peks iv", case=False, na=False).sum()
        status_counts = df_peks_iv["Status Penyelesaian"].value_counts()

    col1, col2, col3, col4 = st.columns(4, gap="large")
    col1.markdown(
        """
        <div class='dashboard-card'>
            <h3>Total Pemeriksaan</h3>
            <p class='metric'>{}</p>
            <p class='metric-label'>Jumlah pemeriksaan unik yang tercatat</p>
        </div>
        """.format(total_pemeriksaan),
        unsafe_allow_html=True,
    )
    col2.markdown(
        """
        <div class='dashboard-card'>
            <h3>Instansi Terlibat</h3>
            <p class='metric'>{}</p>
            <p class='metric-label'>Jumlah instansi dalam data pemeriksaan</p>
        </div>
        """.format(total_instansi),
        unsafe_allow_html=True,
    )
    col3.markdown(
        """
        <div class='dashboard-card'>
            <h3>Tema Unik</h3>
            <p class='metric'>{}</p>
            <p class='metric-label'>Jumlah tema pemeriksaan berbeda</p>
        </div>
        """.format(total_tema),
        unsafe_allow_html=True,
    )
    col4.markdown(
        """
        <div class='dashboard-card'>
            <h3>Total TLHP</h3>
            <p class='metric'>{}</p>
            <p class='metric-label'>Jumlah laporan TLHP yang tercatat</p>
        </div>
        """.format(total_tlhp),
        unsafe_allow_html=True,
    )

    df1 = (
        df.groupby("Instansi")["Nomor ND Pemeriksaan"]
        .nunique()
        .reset_index(name="Jumlah")
        .sort_values("Jumlah", ascending=False)
    )
    df2 = (
        df.groupby("Tema")["Nomor ND Pemeriksaan"]
        .nunique()
        .reset_index(name="Jumlah")
        .sort_values("Jumlah", ascending=False)
    )

    df["Tanggal_Parsed"] = pd.to_datetime(df["Tanggal"], errors="coerce")
    df_month = (
        df.dropna(subset=["Tanggal_Parsed"]) 
        .groupby(df["Tanggal_Parsed"].dt.to_period("M"))["Nomor ND Pemeriksaan"]
        .nunique()
        .reset_index(name="Jumlah")
    )
    if not df_month.empty:
        df_month["Bulan"] = df_month["Tanggal_Parsed"].dt.to_timestamp()
        fig_line = px.area(
            df_month,
            x="Bulan",
            y="Jumlah",
            title="Tren Pemeriksaan Bulanan",
            markers=True,
            color_discrete_sequence=["#6366f1"],
        )
        fig_line.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=False,
        )
        fig_line.update_xaxes(showgrid=False)
        fig_line.update_yaxes(title_text="Jumlah")
    else:
        fig_line = None

    fig1 = px.bar(
        df1,
        x="Instansi",
        y="Jumlah",
        color="Instansi",
        text="Jumlah",
        color_discrete_sequence=px.colors.qualitative.Vivid,
        title="Pemeriksaan per Instansi",
    )
    fig1.update_traces(textposition="outside")
    fig1.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_tickangle=-30,
        showlegend=False,
    )
    fig1.update_xaxes(tickfont=dict(size=12))
    fig1.update_yaxes(title_text="Jumlah")

    fig2 = px.bar(
        df2,
        x="Tema",
        y="Jumlah",
        color="Tema",
        text="Jumlah",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        title="Pemeriksaan per Tema",
    )
    fig2.update_traces(textposition="outside")
    fig2.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_tickangle=-30,
        showlegend=False,
    )
    fig2.update_xaxes(tickfont=dict(size=12))
    fig2.update_yaxes(title_text="Jumlah")

    st.markdown("<div class='dashboard-small-card'><h3 style='margin-bottom:16px;'>Pemeriksaan Terbaru</h3></div>", unsafe_allow_html=True)
    st.markdown("---")

    if fig_line is not None:
        st.plotly_chart(fig_line, use_container_width=True)
    else:
        st.info("Tidak ada data tanggal pemeriksaan yang valid untuk grafik tren bulanan.")

    col5, col6 = st.columns(2, gap="large")
    with col5:
        st.plotly_chart(fig1, use_container_width=True)
    with col6:
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='dashboard-small-card'><h3 style='margin-bottom:16px;'>TLHP PEKS IV</h3></div>", unsafe_allow_html=True)
    if df_tlhp.empty:
        st.info("Tidak ada data TLHP untuk ditampilkan.")
    else:
        df_role_counts = pd.DataFrame({
            "Role": ["Lead UKE II", "UKE II (Koordinasi)"],
            "Jumlah": [count_lead_uke_ii, count_uke_koord],
        })
        df_status = pd.DataFrame({
            "Status": ["Dalam Proses", "Sedang Diusulkan Sesuai"],
            "Jumlah": [
                status_counts.get("Dalam Proses", 0),
                status_counts.get("Sedang Diusulkan Sesuai", 0),
            ],
        })

        fig_role = px.bar(
            df_role_counts,
            x="Jumlah",
            y="Role",
            orientation="h",
            text="Jumlah",
            color="Role",
            color_discrete_map={"Lead UKE II": "#2563eb", "UKE II (Koordinasi)": "#8b5cf6"},
            title="Jumlah Temuan berdasarkan Peran PEKS IV",
        )
        fig_role.update_traces(textposition="outside", marker_line_width=0)
        fig_role.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=40, b=20),
            showlegend=False,
            xaxis_title="Jumlah",
            yaxis_title="",
        )

        fig_status = px.pie(
            df_status,
            names="Status",
            values="Jumlah",
            title="Status Tindak Lanjut TLHP PEKS IV",
            color_discrete_sequence=["#f59e0b", "#3b82f6"],
        )
        fig_status.update_traces(textposition="inside", textinfo="percent+label")
        fig_status.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=20, r=20, t=40, b=20),
        )

        col7, col8 = st.columns([1, 1], gap="large")
        with col7:
            st.plotly_chart(fig_role, use_container_width=True)
        with col8:
            st.plotly_chart(fig_status, use_container_width=True)


# ======================
# DAFTAR PEMERIKSAAN
# ======================

# ======================
# FILTER PEMERIKSAAN
# ======================
if menu == "Daftar Pemeriksaan":
    st.markdown(
        """
        <div class='page-section-card'>
            <div class='page-heading'>
                <h1>Daftar Pemeriksaan</h1>
                <p>Pemeriksaan yang melibatkan PEKS IV berupa rapat pemeriksaan, permintaan data dan informasi, serta follow up LHP.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4, col5, col6 = st.columns([1, 1, 1, 1, 1, 2], gap="small")
    with col1:
        instansi = st.selectbox(
            "", ["Instansi"] + sorted(df["Instansi"].dropna().unique()), label_visibility="collapsed"
        )
    with col2:
        tema = st.selectbox(
            "", ["Tema"] + sorted(df["Tema"].dropna().unique()), label_visibility="collapsed"
        )
    
    with col3:
        dari_tanggal = st.date_input("Dari", value=None, label_visibility="collapsed")
    
    with col4:
        sampai_tanggal = st.date_input("Sampai", value=None, label_visibility="collapsed")
    
    with col5:
        st.markdown("")  # Spacer
    
    with col6:
        st.markdown("")  # Spacer

    col1b, col2b = st.columns([8, 2], gap="large")
    with col1b:
        sort_order = st.radio(
            "Urutkan berdasarkan tanggal",
            ["Terbaru ke Terlama", "Terlama ke Terbaru"],
            index=0,
            horizontal=True,
            key="sort_pemeriksaan_order",
            label_visibility="visible",
        )
    with col2b:
        st.markdown("<div class='col-button-green'>", unsafe_allow_html=True)
        if st.button("➕ Tambah Pemeriksaan", key="btn_tambah_pemeriksaan", use_container_width=True):
            st.session_state.show_add_form = True
            st.session_state.new_findings = [
                {
                    "temuan": "",
                    "conditions": [
                        {"kondisi": "", "uraian": "", "tanggapan": ""}
                    ],
                }
            ]
        st.markdown("</div>", unsafe_allow_html=True)

    df_filter = df.copy()
    if instansi != "Instansi":
        df_filter = df_filter[df_filter["Instansi"] == instansi]
    if tema != "Tema":
        df_filter = df_filter[df_filter["Tema"] == tema]
    
    # Filter by date range
    if dari_tanggal is not None or sampai_tanggal is not None:
        df_filter["Tanggal"] = pd.to_datetime(df_filter["Tanggal"], errors="coerce")
        if dari_tanggal is not None:
            df_filter = df_filter[df_filter["Tanggal"] >= pd.to_datetime(dari_tanggal)]
        if sampai_tanggal is not None:
            df_filter = df_filter[df_filter["Tanggal"] <= pd.to_datetime(sampai_tanggal)]
    
    st.session_state.selected_nd = None
    if "show_add_form" not in st.session_state:
        st.session_state.show_add_form = False
    if "new_findings" not in st.session_state:
        st.session_state.new_findings = [
            {
                "temuan": "",
                "conditions": [
                    {"kondisi": "", "uraian": "", "tanggapan": ""}
                ],
            }
        ]

    if st.session_state.show_add_form:
        st.info("Tambah data pemeriksaan baru. Tambah temuan dan kondisi sesuai kebutuhan.")

        col1f, col2f = st.columns(2)
        with col1f:
            tanggal = st.date_input("Tanggal", value=date.today())
            instansi = st.text_input("Instansi", key="instansi")
            tema = st.text_input("Tema", key="tema")
            nomor_nd_pemeriksaan = st.text_input("Nomor ND Pemeriksaan", key="nomor_nd_pemeriksaan")
            nomor_nd_tanggapan = st.text_input("Nomor ND Tanggapan", key="nomor_nd_tanggapan")
            topik = st.text_area("Topik", height=140, key="topik")
            dokumen = st.text_input("Dokumen Pendukung (URL)", key="dokumen")

        with col2f:
            if st.button("➕ Tambah Temuan", key="add_temuan"):
                st.session_state.new_findings.append(
                    {
                        "temuan": "",
                        "conditions": [
                            {"kondisi": "", "uraian": "", "tanggapan": ""}
                        ],
                    }
                )

            for fi, finding in enumerate(st.session_state.new_findings):
                with st.expander(f"Temuan {fi+1}", expanded=True):
                    finding["temuan"] = st.text_area(
                        "Temuan",
                        value=finding["temuan"],
                        key=f"temuan_{fi}",
                        height=120,
                    )

                    for ci, condition in enumerate(finding["conditions"]):
                        st.markdown(f"**Kondisi {ci+1}**")
                        condition["kondisi"] = st.text_area(
                            "Kondisi/Rekomendasi",
                            value=condition["kondisi"],
                            key=f"kondisi_{fi}_{ci}",
                            height=100,
                        )
                        condition["uraian"] = st.text_area(
                            "Uraian",
                            value=condition["uraian"],
                            key=f"uraian_{fi}_{ci}",
                            height=100,
                        )
                        condition["tanggapan"] = st.text_area(
                            "Tanggapan PEKS IV",
                            value=condition["tanggapan"],
                            key=f"tanggapan_{fi}_{ci}",
                            height=100,
                        )

                    if st.button("➕ Tambah Kondisi", key=f"add_condition_{fi}"):
                        st.session_state.new_findings[fi]["conditions"].append(
                            {"kondisi": "", "uraian": "", "tanggapan": ""}
                        )

        col_left, col_center, col_right = st.columns([1, 1, 1])
        with col_center:
            save_pressed = st.button("Simpan Pemeriksaan", key="save_pemeriksaan")
        with col_right:
            cancel_pressed = st.button("Batal", key="cancel_pemeriksaan")

        if cancel_pressed:
            st.session_state.show_add_form = False
            st.session_state.new_findings = [
                {
                    "temuan": "",
                    "conditions": [
                        {"kondisi": "", "uraian": "", "tanggapan": ""}
                    ],
                }
            ]
            st.rerun()

        if save_pressed:
            if not instansi.strip():
                st.error("Instansi harus diisi.")
            elif not tema.strip():
                st.error("Tema harus diisi.")
            elif not nomor_nd_pemeriksaan.strip():
                st.error("ND Pemeriksaan harus diisi.")
            else:
                next_temuan = get_next_temuan_number(nomor_nd_pemeriksaan, df)
                new_rows = []

                for fi, finding in enumerate(st.session_state.new_findings, start=1):
                    if not finding["temuan"].strip():
                        continue

                    id_temuan = f"{next_temuan + fi - 1}.0"
                    for ci, condition in enumerate(finding["conditions"], start=1):
                        if not any(
                            [
                                condition["kondisi"].strip(),
                                condition["uraian"].strip(),
                                condition["tanggapan"].strip(),
                            ]
                        ):
                            continue

                        new_rows.append(
                            {
                                "Tanggal": tanggal.isoformat(),
                                "Instansi": instansi,
                                "Tema": tema,
                                "Topik": topik,
                                "Nomor ND Pemeriksaan": nomor_nd_pemeriksaan,
                                "Nomor ND Tanggapan": nomor_nd_tanggapan,
                                "ID_Temuan": id_temuan,
                                "Temuan": finding["temuan"],
                                "ID_Kondisi": f"{next_temuan + fi - 1}.{ci}",
                                "Kondisi/Rekomendasi": condition["kondisi"],
                                "Uraian": condition["uraian"],
                                "Tanggapan PEKS IV": condition["tanggapan"],
                                "Dokumen Pendukung": dokumen,
                            }
                        )

                if new_rows:
                    try:
                        for row in new_rows:
                            save_row_to_csv(row)
                        # Reload df dari CSV untuk memastikan update
                        df = pd.read_csv(DATA_PATH)
                        df.columns = df.columns.str.strip()
                        st.success("Data pemeriksaan baru berhasil ditambahkan.")
                        st.session_state.show_add_form = False
                        st.session_state.new_findings = [
                            {
                                "temuan": "",
                                "conditions": [
                                    {"kondisi": "", "uraian": "", "tanggapan": ""}
                                ],
                            }
                        ]
                        st.rerun()  # Gunakan st.rerun() untuk refresh UI
                    except Exception as e:
                        st.error(f"Gagal menyimpan data: {e}")
                else:
                    st.error(
                        "Tambahkan minimal satu kondisi pada setiap temuan yang ingin disimpan."
                    )

# ======================
# DATA PEMERIKSAAN
# ======================


    st.markdown("### Data Pemeriksaan")

    ascending_date = False if sort_order == "Terbaru ke Terlama" else True

    df_summary = df_filter.copy()
    df_summary["Tanggal_Parsed"] = pd.to_datetime(df_summary["Tanggal"], errors="coerce")
    df_summary = (
        df_summary.sort_values(
            ["Tanggal_Parsed", "Instansi", "Tema", "Nomor ND Pemeriksaan"],
            ascending=[ascending_date, True, True, True],
        )
        .drop_duplicates(subset=["Nomor ND Pemeriksaan"], keep="first")
        .copy()
    )

    if "pemeriksaan_page" not in st.session_state:
        st.session_state.pemeriksaan_page = 1

    items_per_page = 10
    total_items = len(df_summary)
    total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
    st.session_state.pemeriksaan_page = min(max(1, st.session_state.pemeriksaan_page), total_pages)

    start_idx = (st.session_state.pemeriksaan_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    page_df = df_summary.iloc[start_idx:end_idx]

    if df_summary.empty:
        st.info("Tidak ada data pemeriksaan untuk filter ini.")
    else:
        # CSS for table styling - matching TLHP table style
        st.markdown("""
        <style>
            .pemeriksaan-table-container {
                max-height: 500px;
                overflow-y: auto;
                border: 1px solid #e5e5e5;
                border-radius: 8px;
                padding-right: 5px;
            }
            .pemeriksaan-table-container::-webkit-scrollbar {
                width: 8px;
            }
            .pemeriksaan-table-container::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 8px;
            }
            .pemeriksaan-table-container::-webkit-scrollbar-thumb {
                background: #c1c1c1;
                border-radius: 8px;
            }
            .pemeriksaan-table-container::-webkit-scrollbar-thumb:hover {
                background: #888;
            }
            .pemeriksaan-table {
                width: 100%;
                border-collapse: collapse;
                font-family: "Segoe UI", Roboto, sans-serif;
                font-size: 14px;
                margin-bottom: 20px;
            }
            .pemeriksaan-table th {
                background: #f5f5f5;
                padding: 14px 12px;
                text-align: left;
                font-weight: 600;
                color: #1a1a1a;
                border-bottom: 2px solid #e5e5e5;
            }
            .pemeriksaan-table td {
                padding: 14px 12px;
                border-bottom: 1px solid #e5e5e5;
                color: #333;
            }
            .pemeriksaan-table tbody tr:hover {
                background: #fafafa;
            }
        </style>
        <div class="pemeriksaan-table-container">
        """, unsafe_allow_html=True)

        # Create header using columns for proper alignment
        header_cols = st.columns([0.6, 1.0, 1.0, 1.6, 1.0, 2.2, 0.6, 0.6])
        
        header_style = "font-weight: 600; color: #1a1a1a; font-size: 14px; text-align: center; padding: 10px 0; border-bottom: 2px solid #e5e5e5;"
        left_header_style = "font-weight: 600; color: #1a1a1a; font-size: 14px; text-align: left; padding: 10px 0; border-bottom: 2px solid #e5e5e5;"
        
        with header_cols[0]:
            st.markdown(f"<div style='{header_style}'>No.</div>", unsafe_allow_html=True)
        with header_cols[1]:
            st.markdown(f"<div style='{header_style}'>Tanggal</div>", unsafe_allow_html=True)
        with header_cols[2]:
            st.markdown(f"<div style='{header_style}'>Instansi</div>", unsafe_allow_html=True)
        with header_cols[3]:
            st.markdown(f"<div style='{left_header_style}'>ND Tanggapan</div>", unsafe_allow_html=True)
        with header_cols[4]:
            st.markdown(f"<div style='{left_header_style}'>Tema</div>", unsafe_allow_html=True)
        with header_cols[5]:
            st.markdown(f"<div style='{left_header_style}'>Topik</div>", unsafe_allow_html=True)
        with header_cols[6]:
            st.markdown(f"<div style='{header_style}'>Detail</div>", unsafe_allow_html=True)
        with header_cols[7]:
            st.markdown(f"<div style='{header_style}'>Dokumen</div>", unsafe_allow_html=True)

        for row_num, (_, row) in enumerate(page_df.iterrows(), start=1):
            display_num = start_idx + row_num
            cols = st.columns([0.6, 1.0, 1.0, 1.6, 1.0, 2.2, 0.6, 0.6])

            row_cell_style = "padding: 14px 0; text-align: center;"
            row_text_style = "padding: 14px 0; text-align: left;"

            cols[0].markdown(
                f"<div style='{row_cell_style}'>{display_num}</div>",
                unsafe_allow_html=True,
            )
            cols[1].markdown(
                f"<div style='{row_cell_style}'>{row['Tanggal']}</div>",
                unsafe_allow_html=True,
            )
            cols[2].markdown(
                f"<div style='{row_cell_style}'>{row['Instansi']}</div>",
                unsafe_allow_html=True,
            )
            cols[3].markdown(
                f"<div style='{row_cell_style}'>{row.get('Nomor ND Tanggapan', '-')}</div>",
                unsafe_allow_html=True,
            )
            cols[4].markdown(
                f"<div style='{row_cell_style}'>{row['Tema']}</div>",
                unsafe_allow_html=True,
            )
            cols[5].markdown(
                f"<div style='{row_text_style}'>{row['Topik']}</div>",
                unsafe_allow_html=True,
            )

            with cols[6]:
                st.markdown(
                    "<div style='display:flex; justify-content:center; align-items:center; height:100%; padding: 14px 0;'>",
                    unsafe_allow_html=True,
                )
                if st.button("🔍", key=f"detail_{display_num}"):
                    st.session_state.selected_nd = row["Nomor ND Pemeriksaan"]
                st.markdown("</div>", unsafe_allow_html=True)

            dokumen_url = row.get("Dokumen Pendukung", "")
            if isinstance(dokumen_url, str) and dokumen_url.strip():
                cols[7].markdown(
                    f"<div style='{row_cell_style}'><a href='{dokumen_url.strip()}' target='_blank'>⬇️</a></div>",
                    unsafe_allow_html=True,
                )
            else:
                cols[7].markdown(f"<div style='{row_cell_style}'>-</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

        pagination_cols = st.columns([1, 1, 1, 1])
        with pagination_cols[0]:
            if st.button("← Sebelumnya", key="pemeriksaan_prev", disabled=st.session_state.pemeriksaan_page == 1):
                st.session_state.pemeriksaan_page = max(1, st.session_state.pemeriksaan_page - 1)
                st.rerun()
        with pagination_cols[1]:
            st.markdown(f"<div style='padding-top: 8px; text-align:center;'>Halaman {st.session_state.pemeriksaan_page} dari {total_pages}</div>", unsafe_allow_html=True)
        with pagination_cols[2]:
            if st.button("Berikutnya →", key="pemeriksaan_next", disabled=st.session_state.pemeriksaan_page == total_pages):
                st.session_state.pemeriksaan_page = min(total_pages, st.session_state.pemeriksaan_page + 1)
                st.rerun()
        with pagination_cols[3]:
            st.markdown("<div></div>", unsafe_allow_html=True)

# ======================
# DETAIL PEMERIKSAAN
# ======================

    selected_nd = st.session_state.get("selected_nd")
    if selected_nd:
        # Get the main pemeriksaan row info
        pemeriksaan_info = df.loc[df["Nomor ND Pemeriksaan"] == selected_nd].iloc[0] if not df.loc[df["Nomor ND Pemeriksaan"] == selected_nd].empty else None
        
        if pemeriksaan_info is not None:
            # Detail findings data
            detail_df = df.loc[
                df["Nomor ND Pemeriksaan"] == selected_nd,
                ["Temuan", "Kondisi/Rekomendasi", "Uraian", "Tanggapan PEKS IV"],
            ].copy()

            if not detail_df.empty:
                detail_df = detail_df.astype(str)
                for col in detail_df.columns:
                    detail_df[col] = detail_df[col].apply(normalize_detail_text)

                # Create detail card with header and close button
                col_header_left, col_header_right = st.columns([10, 1])
                
                with col_header_left:
                    st.markdown(f"""
                    <style>
                        .detail-card-header {{
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                            border-radius: 12px;
                            padding: 20px;
                            margin-bottom: 20px;
                            color: white;
                            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                        }}
                        .detail-card-title {{
                            font-size: 20px;
                            font-weight: 700;
                            margin: 0;
                            display: flex;
                            align-items: center;
                            gap: 10px;
                        }}
                    </style>
                    <div class="detail-card-header">
                        <div class="detail-card-title">📋 Detail Pemeriksaan: {pemeriksaan_info['Topik']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_header_right:
                    st.markdown("""
                    <style>
                        .col-button-red button {
                            background-color: #ef4444 !important;
                            color: white !important;
                        }
                        .col-button-red button:hover {
                            background-color: #dc2626 !important;
                        }
                    </style>
                    <div class="col-button-red" style="margin-top: 10px;">
                    """, unsafe_allow_html=True)
                    
                    if st.button("✖ Tutup", key="btn_close_detail_pemeriksaan", use_container_width=True):
                        st.session_state.selected_nd = None
                        st.rerun()
                    
                    st.markdown("</div>", unsafe_allow_html=True)

                # Display detail table in scrollable container
                detail_html = detail_df.to_html(index=False, classes="detail-table", escape=False)
                
                st.markdown("""
                <style>
                    .detail-table-container {
                        max-height: 500px;
                        overflow-y: auto;
                        border: 1px solid #e5e5e5;
                        border-radius: 8px;
                        padding-right: 5px;
                        margin-top: 20px;
                    }
                    .detail-table-container::-webkit-scrollbar {
                        width: 8px;
                    }
                    .detail-table-container::-webkit-scrollbar-track {
                        background: #f1f1f1;
                        border-radius: 8px;
                    }
                    .detail-table-container::-webkit-scrollbar-thumb {
                        background: #c1c1c1;
                        border-radius: 8px;
                    }
                    .detail-table-container::-webkit-scrollbar-thumb:hover {
                        background: #888;
                    }
                    .detail-table {
                        width: 100%;
                        border-collapse: collapse;
                        font-family: 'Segoe UI', Roboto, sans-serif;
                        font-size: 13px;
                    }
                    .detail-table th {
                        background-color: #059669;
                        color: white;
                        padding: 12px 14px;
                        text-align: left;
                        font-weight: 600;
                        border: 1px solid #059669;
                        text-transform: uppercase;
                        font-size: 11px;
                        letter-spacing: 0.5px;
                        position: sticky;
                        top: 0;
                    }
                    .detail-table td {
                        padding: 14px 14px;
                        border: 1px solid #e0e0e0;
                        vertical-align: top;
                        white-space: normal;
                        word-wrap: break-word;
                        overflow-wrap: break-word;
                        text-align: left;
                    }
                    .detail-table tbody tr:nth-child(odd) td {
                        background-color: #f8f9fa;
                    }
                    .detail-table tbody tr:nth-child(even) td {
                        background-color: #ffffff;
                    }
                    .detail-table tbody tr:hover td {
                        background-color: #f0f0f0 !important;
                    }
                </style>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""<div class="detail-table-container">{detail_html}</div>""", unsafe_allow_html=True)

# ======================
# TLHP PEKS IV
# ======================
if menu == "TLHP PEKS IV":
    st.markdown(
        """
        <div class='page-section-card'>
            <div class='page-heading'>
                <h1>Tindak Lanjut Hasil Pemeriksaan (TLHP) PEKS IV</h1>
                <p>Daftar temuan yang harus ditindaklanjuti oleh Direktorat PEKS IV.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # Filter dan display TLHP
    col1, col2 = st.columns([8, 2])
    with col1:
        st.subheader("Daftar TLHP")
        sort_tlhp_order = st.radio(
            "Urutkan laporan",
            ["Terbaru ke Terlama", "Terlama ke Terbaru"],
            index=0,
            horizontal=True,
            key="sort_tlhp_order",
            label_visibility="visible",
        )
    with col2:
        st.markdown("""
        <style>
            .col-button-green button {
                background-color: #10b981 !important;
                color: white !important;
            }
            .col-button-green button:hover {
                background-color: #059669 !important;
            }
        </style>
        <div class="col-button-green">
        """, unsafe_allow_html=True)
        
        if st.button("➕ Tambah TLHP", key="btn_tambah_tlhp", use_container_width=True):
            st.session_state.show_tlhp_form = True
            st.session_state.tlhp_form_mode = "add"
        
        st.markdown("</div>", unsafe_allow_html=True)

    # Form tambah TLHP
    if "show_tlhp_form" not in st.session_state:
        st.session_state.show_tlhp_form = False
        st.session_state.tlhp_form_mode = "add"

    if st.session_state.show_tlhp_form:
        st.info("Tambah data TLHP baru")

        with st.form("form_tlhp"):
            col1_f, col2_f, col3_f = st.columns(3)
            
            with col1_f:
                nama_laporan = st.text_input("Nama Laporan", key="nama_laporan")
                tgl_laporan = st.date_input("Tanggal Laporan", key="tgl_laporan")
                tahun = st.number_input("Tahun", min_value=2000, max_value=2100, key="tahun_tlhp", step=1)
                pengawas = st.text_input("Pengawas", key="pengawas")

            with col2_f:
                temuan = st.text_area("Temuan", height=100, key="temuan_tlhp")
                resuma_kondisi = st.text_area("Resuma Kondisi", height=100, key="resuma_kondisi")

            with col3_f:
                rekomendasi = st.text_area("Rekomendasi", height=100, key="rekomendasi")
                kode_rekomendasi = st.text_input("Kode Rekomendasi", key="kode_rekomendasi")

            st.markdown("---")

            col1_f2, col2_f2, col3_f2 = st.columns(3)
            
            with col1_f2:
                lead_uke_i = st.text_input("Lead UKE I", key="lead_uke_i")
                lead_uke_ii = st.text_input("Lead UKE II", key="lead_uke_ii")
                uke_ii_koordinasi = st.text_input("UKE II (Koordinasi)", key="uke_ii_koordinasi")
                uke_i_koordinasi = st.text_input("UKE I (Koordinasi)", key="uke_i_koordinasi")

            with col2_f2:
                rencana_aksi = st.text_area("Rencana Aksi", height=100, key="rencana_aksi")
                deadline = st.date_input("Deadline", key="deadline")

            with col3_f2:
                progress = st.text_area("Progress Pelaksanaan Rencana Aksi", height=100, key="progress")
                data_dukung = st.text_input("Data Dukung (LinkPortal)", key="data_dukung")

            st.markdown("---")

            col1_f3, col2_f3, col3_f3 = st.columns(3)
            
            with col1_f3:
                submit = st.checkbox("Submit", value=False, key="submit_tlhp")
                tgl_submit = st.date_input("Tanggal Submit", key="tgl_submit") if submit else None

            with col2_f3:
                catatan_penyulut = st.text_area("Catatan Penyulut", height=80, key="catatan_penyulut")

            with col3_f3:
                catatan_eksternal = st.text_area("Catatan Eksternal", height=80, key="catatan_eksternal")
                hasil_validasi = st.selectbox(
                    "Hasil Validasi Pengawasan",
                    ["", "Valid", "Perlu Perbaikan", "Ditolak"],
                    key="hasil_validasi"
                )
                status = st.selectbox(
                    "Status Penyelesaian",
                    ["", "Belum Dimulai", "Sedang Berjalan", "Selesai", "Tertunda"],
                    key="status_tlhp"
                )

            col_save_cancel = st.columns([1, 1, 3])
            with col_save_cancel[0]:
                save_tlhp = st.form_submit_button("Simpan", use_container_width=True)
            with col_save_cancel[1]:
                cancel_tlhp = st.form_submit_button("Batal", use_container_width=True)

            if cancel_tlhp:
                st.session_state.show_tlhp_form = False
                st.rerun()

            if save_tlhp:
                if not nama_laporan.strip():
                    st.error("Nama Laporan harus diisi.")
                else:
                    try:
                        next_no = 1
                        if not df_tlhp.empty:
                            try:
                                next_no = int(df_tlhp["No"].astype(str).str.extract(r"(\d+)")[0].max()) + 1
                            except:
                                next_no = len(df_tlhp) + 1

                        new_tlhp_row = {
                            "No": str(next_no),
                            "Nama Laporan": nama_laporan,
                            "Tgl Laporan": str(tgl_laporan),
                            "Tahun": str(tahun),
                            "Pengawas": pengawas,
                            "Temuan": temuan,
                            "Resuma Kondisi": resuma_kondisi,
                            "Rekomendasi": rekomendasi,
                            "Kode Rekomendasi": kode_rekomendasi,
                            "Lead UKE I": lead_uke_i,
                            "Lead UKE II": lead_uke_ii,
                            "UKE II (Koordinasi)": uke_ii_koordinasi,
                            "UKE I (Koordinasi)": uke_i_koordinasi,
                            "Rencana Aksi": rencana_aksi,
                            "Deadline": str(deadline),
                            "Progress Pelaksanaan Rencana Aksi": progress,
                            "Data Dukung (LinkPortal)": data_dukung,
                            "Submit": "Ya" if submit else "Tidak",
                            "Tgl Submit": str(tgl_submit) if tgl_submit else "",
                            "Catatan Penyulut": catatan_penyulut,
                            "Catatan Eksternal": catatan_eksternal,
                            "Hasil Validasi Pengawasan": hasil_validasi,
                            "Status Penyelesaian": status,
                        }

                        save_tlhp_row_to_csv(new_tlhp_row)
                        df_tlhp = load_tlhp_data()
                        df_tlhp.columns = df_tlhp.columns.str.strip()
                        st.success("Data TLHP berhasil ditambahkan.")
                        st.session_state.show_tlhp_form = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"Gagal menyimpan data: {e}")

    if "selected_tlhp_name" not in st.session_state:
        st.session_state.selected_tlhp_name = None
    if "selected_tlhp_no" not in st.session_state:
        st.session_state.selected_tlhp_no = None

    # Display TLHP Data
    if not df_tlhp.empty:
        df_tlhp_display = df_tlhp.copy()

        display_cols = [
            "Nama Laporan",
            "Tgl Laporan",
            "Tahun",
            "Pengawas",
            "Lead UKE II",
            "UKE II (Koordinasi)",
            "Deadline",
            "Status Penyelesaian",
        ]
        available_cols = [col for col in display_cols if col in df_tlhp_display.columns]

        if "Nama Laporan" in available_cols:
            group_cols = [col for col in available_cols if col != "Nama Laporan"]
            agg_dict = {col: "first" for col in group_cols}
            df_tlhp_summary = (
                df_tlhp_display[["Nama Laporan"] + group_cols]
                .groupby("Nama Laporan", sort=False, as_index=False)
                .agg(agg_dict)
            )

            # Parse tanggal for sorting; fallback to string sort if parse fails
            df_tlhp_summary["Tgl_Laporan_Parsed"] = pd.to_datetime(
                df_tlhp_summary["Tgl Laporan"], errors="coerce"
            )
            if sort_tlhp_order == "Terbaru ke Terlama":
                df_tlhp_summary = df_tlhp_summary.sort_values(
                    ["Tgl_Laporan_Parsed", "Nama Laporan"],
                    ascending=[False, True],
                    na_position="last",
                )
            else:
                df_tlhp_summary = df_tlhp_summary.sort_values(
                    ["Tgl_Laporan_Parsed", "Nama Laporan"],
                    ascending=[True, True],
                    na_position="last",
                )
            df_tlhp_summary = df_tlhp_summary.reset_index(drop=True)
            df_tlhp_summary.insert(0, "No", range(1, len(df_tlhp_summary) + 1))

            if "tlhp_page" not in st.session_state:
                st.session_state.tlhp_page = 1

            items_per_page = 10
            total_items = len(df_tlhp_summary)
            total_pages = max(1, (total_items + items_per_page - 1) // items_per_page)
            st.session_state.tlhp_page = min(max(1, st.session_state.tlhp_page), total_pages)

            start_idx = (st.session_state.tlhp_page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            page_df = df_tlhp_summary.iloc[start_idx:end_idx]

            status_color = {
                "Belum Dimulai": "#ef4444",
                "Dalam Proses": "#fbbf24",
                "Sedang Berjalan": "#f59e0b",
                "Sedang Diusulkan Sesuai": "#3b82f6",
                "Selesai": "#10b981",
                "Tertunda": "#8b5cf6",
            }

            df_tlhp_summary = df_tlhp_summary.fillna("")

            # CSS for table styling
            st.markdown("""
            <style>
                .tlhp-table {
                    width: 100%;
                    border-collapse: collapse;
                    font-family: "Segoe UI", Roboto, sans-serif;
                    font-size: 14px;
                    margin-bottom: 20px;
                }
                .tlhp-table th {
                    background: #f5f5f5;
                    padding: 14px 12px;
                    text-align: left;
                    font-weight: 600;
                    color: #1a1a1a;
                    border-bottom: 2px solid #e5e5e5;
                }
                .tlhp-table td {
                    padding: 14px 12px;
                    border-bottom: 1px solid #e5e5e5;
                    color: #333;
                }
                .tlhp-table tbody tr:hover {
                    background: #fafafa;
                }
                .tlhp-table tbody tr:last-child td {
                    border-bottom: none;
                }
                .status-badge {
                    padding: 6px 12px;
                    border-radius: 20px;
                    font-weight: 500;
                    color: white;
                    font-size: 12px;
                    display: inline-block;
                }
            </style>
            """, unsafe_allow_html=True)
            
            status_color = {
                "Belum Dimulai": "#ef4444",
                "Dalam Proses": "#fbbf24",
                "Sedang Berjalan": "#f59e0b",
                "Sedang Diusulkan Sesuai": "#3b82f6",
                "Selesai": "#10b981",
                "Tertunda": "#8b5cf6",
            }

            st.markdown("""
            <style>
                .status-badge {
                    padding: 6px 12px;
                    border-radius: 20px;
                    font-weight: 500;
                    color: white;
                    font-size: 12px;
                    display: inline-block;
                }
            </style>
            """, unsafe_allow_html=True)
            
            # Create header using columns for proper alignment
            header_cols = st.columns([0.35, 4.5, 1.0, 0.8, 1.0, 1.4, 1.4, 1.0, 1.0, 0.8])
            
            header_style = "font-weight: 600; color: #1a1a1a; font-size: 14px; text-align: center; padding: 10px 0; border-bottom: 2px solid #e5e5e5;"
            
            with header_cols[0]:
                st.markdown(f"<div style='{header_style}; text-align: center;'>No</div>", unsafe_allow_html=True)
            with header_cols[1]:
                st.markdown(f"<div style='{header_style}; text-align: left;'>Nama Laporan</div>", unsafe_allow_html=True)
            with header_cols[2]:
                st.markdown(f"<div style='{header_style}'>Tgl Laporan</div>", unsafe_allow_html=True)
            with header_cols[3]:
                st.markdown(f"<div style='{header_style}'>Tahun</div>", unsafe_allow_html=True)
            with header_cols[4]:
                st.markdown(f"<div style='{header_style}'>Pengawas</div>", unsafe_allow_html=True)
            with header_cols[5]:
                st.markdown(f"<div style='{header_style}'>Lead UKE II</div>", unsafe_allow_html=True)
            with header_cols[6]:
                st.markdown(f"<div style='{header_style}'>UKE II (Koordinasi)</div>", unsafe_allow_html=True)
            with header_cols[7]:
                st.markdown(f"<div style='{header_style}'>Deadline</div>", unsafe_allow_html=True)
            with header_cols[8]:
                st.markdown(f"<div style='{header_style}'>Status</div>", unsafe_allow_html=True)
            with header_cols[9]:
                st.markdown(f"<div style='{header_style}'>Detail</div>", unsafe_allow_html=True)
            
            # Create rows with columns for button alignment
            for index, row in page_df.iterrows():
                try:
                    status_val = str(row.get('Status Penyelesaian', '-') or '-')
                    status_bg = status_color.get(status_val, '#6b7280')
                    
                    no = str(row.get('No', '-'))
                    nama_laporan = str(row.get('Nama Laporan', '-'))
                    tgl_laporan = str(row.get('Tgl Laporan', '-'))
                    tahun = str(row.get('Tahun', '-'))
                    pengawas = str(row.get('Pengawas', '-'))
                    lead_uke_ii = str(row.get('Lead UKE II', '-'))
                    uke_ii_koordinasi = str(row.get('UKE II (Koordinasi)', '-'))
                    deadline = str(row.get('Deadline', '-'))
                    
                    # Create a row using columns
                    row_cols = st.columns([0.35, 4.5, 1.0, 0.8, 1.0, 1.4, 1.4, 1.0, 1.0, 0.8])
                    
                    with row_cols[0]:
                        st.markdown(f"<div style='text-align: center; padding: 14px 0;'>{no}</div>", unsafe_allow_html=True)
                    with row_cols[1]:
                        st.markdown(f"<div style='padding: 14px 0;'>{nama_laporan}</div>", unsafe_allow_html=True)
                    with row_cols[2]:
                        st.markdown(f"<div style='text-align: center; padding: 14px 0;'>{tgl_laporan}</div>", unsafe_allow_html=True)
                    with row_cols[3]:
                        st.markdown(f"<div style='text-align: center; padding: 14px 0;'>{tahun}</div>", unsafe_allow_html=True)
                    with row_cols[4]:
                        st.markdown(f"<div style='text-align: center; padding: 14px 0;'>{pengawas}</div>", unsafe_allow_html=True)
                    with row_cols[5]:
                        st.markdown(f"<div style='text-align: center; padding: 14px 0;'>{lead_uke_ii}</div>", unsafe_allow_html=True)
                    with row_cols[6]:
                        st.markdown(f"<div style='text-align: center; padding: 14px 0;'>{uke_ii_koordinasi}</div>", unsafe_allow_html=True)
                    with row_cols[7]:
                        st.markdown(f"<div style='text-align: center; padding: 14px 0;'>{deadline}</div>", unsafe_allow_html=True)
                    with row_cols[8]:
                        st.markdown(f"<div style='text-align: center; padding: 14px 0;'><span class='status-badge' style='background: {status_bg};'>{status_val}</span></div>", unsafe_allow_html=True)
                    with row_cols[9]:
                        st.markdown(f"<div style='text-align: center;'>", unsafe_allow_html=True)
                        if st.button("🔍", key=f"tlhp_detail_{index}", help="Lihat detail"):
                            st.session_state.selected_tlhp_name = row.get('Nama Laporan', '')
                            st.rerun()
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Add bottom border
                    st.markdown("<div style='height: 0; border-bottom: 1px solid #e5e5e5; margin-bottom: -15px;'></div>", unsafe_allow_html=True)
                    
                except Exception as e:
                    st.warning(f"Error processing row {index}: {str(e)}")
                    continue

            pagination_cols = st.columns([1, 1, 1, 1])
            with pagination_cols[0]:
                if st.button("← Sebelumnya", key="tlhp_prev", disabled=st.session_state.tlhp_page == 1):
                    st.session_state.tlhp_page = max(1, st.session_state.tlhp_page - 1)
                    st.rerun()
            with pagination_cols[1]:
                st.markdown(f"<div style='padding-top: 8px; text-align:center;'>Halaman {st.session_state.tlhp_page} dari {total_pages}</div>", unsafe_allow_html=True)
            with pagination_cols[2]:
                if st.button("Berikutnya →", key="tlhp_next", disabled=st.session_state.tlhp_page == total_pages):
                    st.session_state.tlhp_page = min(total_pages, st.session_state.tlhp_page + 1)
                    st.rerun()
            with pagination_cols[3]:
                st.markdown("<div></div>", unsafe_allow_html=True)

        else:
            st.warning("Kolom 'Nama Laporan' tidak ditemukan di data TLHP.")
    else:
        st.info("Belum ada data TLHP. Klik tombol 'Tambah TLHP' untuk menambahkan data baru.")

    selected_name = st.session_state.selected_tlhp_name
    if isinstance(selected_name, str) and selected_name.strip() and "Nama Laporan" in df_tlhp.columns:
        selected_name = selected_name.strip()
        detail_df = df_tlhp[df_tlhp["Nama Laporan"].astype(str).str.strip() == selected_name].copy()

        detail_cols = [
            "Temuan",
            "Resuma Kondisi",
            "Rekomendasi",
            "Rencana Aksi",
            "Lead UKE II",
            "Deadline",
            "Status Penyelesaian",
            "Catatan Penyulut",
            "Data Dukung (LinkPortal)",
        ]

        if "Status Penyelesaian" not in detail_df.columns:
            detail_df["Status Penyelesaian"] = ""

        detail_display_cols = [col for col in detail_cols if col in detail_df.columns]

        # Create header and close button together
        col_header_left, col_header_right = st.columns([10, 1])
        
        with col_header_left:
            st.markdown("""
            <style>
                .detail-card-header {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 12px;
                    padding: 20px;
                    margin-bottom: 20px;
                    color: white;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
                }
                .detail-card-title {
                    font-size: 20px;
                    font-weight: 700;
                    margin: 0;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }
            </style>
            """, unsafe_allow_html=True)
            
            # Display header with dynamic title
            header_html = f'<div class="detail-card-header"><div class="detail-card-title">📋 Detail TLHP: {selected_name}</div></div>'
            st.markdown(header_html, unsafe_allow_html=True)
        
        with col_header_right:
            st.markdown("""
            <style>
                .col-button-red button {
                    background-color: #ef4444 !important;
                    color: white !important;
                }
                .col-button-red button:hover {
                    background-color: #dc2626 !important;
                }
            </style>
            <div class="col-button-red" style="margin-top: 10px;">
            """, unsafe_allow_html=True)
            
            if st.button("✖ Tutup", key="btn_close_modal", use_container_width=True):
                st.session_state.selected_tlhp_name = None
                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)

        if not detail_df.empty and detail_display_cols:
            detail_display = detail_df[detail_display_cols].copy()
            detail_display = detail_display.rename(columns={
                "Resuma Kondisi": "Resume Kondisi",
                "Catatan Penyulut": "Catatan Inspektorat",
                "Data Dukung (LinkPortal)": "Data Dukung",
            })
            
            # Apply normalize to all columns
            for col in detail_display.columns:
                detail_display[col] = detail_display[col].apply(normalize_detail_text)
            
            # Create table styles
            st.markdown("""
            <style>
                .detail-table {
                    width: 100%;
                    border-collapse: collapse;
                    font-family: 'Segoe UI', Roboto, sans-serif;
                    font-size: 13px;
                    margin-top: 16px;
                }
                .detail-table th {
                    background-color: #059669;
                    color: white;
                    padding: 12px 14px;
                    text-align: left;
                    font-weight: 600;
                    border: 1px solid #059669;
                    text-transform: uppercase;
                    font-size: 11px;
                    letter-spacing: 0.5px;
                }
                .detail-table td {
                    padding: 14px 14px;
                    border: 1px solid #e0e0e0;
                    vertical-align: top;
                    white-space: normal;
                    word-wrap: break-word;
                    overflow-wrap: break-word;
                    text-align: left;
                }
                .detail-table tbody tr:nth-child(odd) td {
                    background-color: #f8f9fa;
                }
                .detail-table tbody tr:nth-child(even) td {
                    background-color: #ffffff;
                }
                .detail-table tbody tr:hover td {
                    background-color: #f0f0f0 !important;
                }
                .table-scroll-container {
                    max-height: 500px;
                    overflow-y: auto;
                    overflow-x: auto;
                    border: 1px solid #e0e0e0;
                    border-radius: 6px;
                }
                .table-scroll-container::-webkit-scrollbar {
                    width: 8px;
                    height: 8px;
                }
                .table-scroll-container::-webkit-scrollbar-track {
                    background: #f1f1f1;
                    border-radius: 10px;
                }
                .table-scroll-container::-webkit-scrollbar-thumb {
                    background: #888;
                    border-radius: 10px;
                }
                .table-scroll-container::-webkit-scrollbar-thumb:hover {
                    background: #555;
                }
            </style>
            """, unsafe_allow_html=True)
            
            # Convert to HTML table
            detail_html = detail_display.to_html(index=False, classes="detail-table", escape=False)
            
            # Wrap table in scrollable container
            scrollable_html = f"""
            <div class="table-scroll-container">
                {detail_html}
            </div>
            """
            st.markdown(scrollable_html, unsafe_allow_html=True)

    else:
        if st.session_state.selected_tlhp_name:
            st.session_state.selected_tlhp_name = None
            st.session_state.selected_tlhp_no = None

# ======================
# TANYA AI SIERA (SMART + CONTEXT AWARE)
# ======================
if menu == "AI SIERA":
    st.markdown(
        """
        <div class='page-section-card'>
            <div class='page-heading'>
                <h1>🤖 Tanya AI SIERA</h1>
                <p>Masukkan pertanyaan untuk mendapatkan jawaban dari AI SIERA.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='chat-container'><div class='chat-form'>", unsafe_allow_html=True)
    with st.form("ai_siera_form"):
        query = st.text_area(
            "",
            value=st.session_state.get("ai_siera_query", ""),
            placeholder="Ketik pertanyaan Anda...",
            label_visibility="collapsed",
            key="ai_siera_query",
            height=140,
        )
        submit = st.form_submit_button("Send")
    st.markdown("</div></div>", unsafe_allow_html=True)

    if submit:
        st.session_state.ai_siera_query = query

    # ======================
    # INTENT DETECTION
    # ======================
    def detect_intent(q):
        q = q.lower()
        if "jumlah" in q or "berapa" in q:
            return "count"
        if "ringkas" in q:
            return "summary"
        if "isu" in q or "masalah" in q or "analisis" in q:
            return "analysis"
        if "tampilkan" in q or "cari" in q:
            return "search"
        return "general"

    # ======================
    # SMART SEARCH + FILTER
    # ======================
    def find_matches(question, df, top_n=5):
        question = question.lower()
        df_filtered = df.copy()

        # ======================
        # FILTER: TEMA
        # ======================
        tema_list = df["Tema"].dropna().str.lower().unique()
        for t in tema_list:
            if t in question:
                df_filtered = df_filtered[df_filtered["Tema"].str.lower() == t]
                break

        # ======================
        # FILTER: INSTANSI
        # ======================
        instansi_list = df["Instansi"].dropna().str.lower().unique()
        for inst in instansi_list:
            if inst in question:
                df_filtered = df_filtered[df_filtered["Instansi"].str.lower() == inst]
                break

        # ======================
        # FILTER: ND
        # ======================
        if "nd" in question:
            df_filtered = df_filtered[
                df_filtered["ND_Pemeriksaan"].astype(str).str.lower().str.contains(question)
            ]

        # ======================
        # KEYWORDS
        # ======================
        keywords = [w for w in re.findall(r"\w+", question) if len(w) >= 2]

        weights = {
            "Instansi": 2,
            "Tema": 5,
            "Topik": 3,
            "Temuan": 2,
            "Kondisi/Rekomendasi": 1,
            "Uraian": 1,
        }

        scores = []

        for _, row in df_filtered.iterrows():
            score = 0
            for col, w in weights.items():
                text = str(row.get(col, "")).lower()
                for kw in keywords:
                    if kw in text:
                        score += w

            if score > 0:
                scores.append((score, row))

        scores.sort(key=lambda x: x[0], reverse=True)

        return [row for _, row in scores[:top_n]]

    # ======================
    # EXECUTION
    # ======================
    if query and not df.empty:

        intent = detect_intent(query)

        # COUNT
        if intent == "count":
            if "temuan" in query.lower():
                st.success(f"Jumlah temuan: {df['ID_Temuan'].nunique()}")
            elif "pemeriksaan" in query.lower() or "nd" in query.lower():
                st.success(f"Jumlah pemeriksaan (ND): {df['ND_Pemeriksaan'].nunique()}")
            else:
                st.info("Spesifikkan: jumlah temuan atau pemeriksaan")

        else:
            matches = find_matches(query, df)

            st.markdown("### Jawaban AI SIERA")

            if not matches:
                st.warning("Tidak ditemukan data yang relevan.")

            else:
                st.success(f"Ditemukan {len(matches)} hasil relevan")

                # ======================
                # AI INSIGHT
                # ======================
                temuan_list = [strip_html(r["Temuan"]) for r in matches]

                st.info(
                    f"AI Insight: Terdapat pola temuan yang berulang, terutama terkait: "
                    f"{temuan_list[0][:120]}..."
                )

                # ======================
                # INTERACTIVE RESULT
                # ======================
                for i, row in enumerate(matches, 1):
                    with st.expander(f"{i}. {row['Instansi']} | {row['Tema']}"):

                        st.markdown(f"**ND Pemeriksaan:** {row['ND_Pemeriksaan']}")
                        st.markdown(f"**Topik:** {row['Topik']}")

                        st.markdown("**Temuan:**")
                        st.write(strip_html(row["Temuan"]))

                        st.markdown("**Kondisi/Rekomendasi:**")
                        st.write(strip_html(row["Kondisi/Rekomendasi"]))

                        st.markdown("**Uraian:**")
                        st.write(strip_html(row["Uraian"]))

                        st.markdown("**Tanggapan PEKS IV:**")
                        st.write(strip_html(row["Tanggapan PEKS IV"]))

    if df.empty:
        st.warning("Data belum tersedia.")
