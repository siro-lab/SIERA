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
# Prioritas: Environment Variables (Railway) → Secrets (Local) → Default
secrets_missing = False

# Try environment variables first (Railway)
username_env = os.environ.get("username")
password_hash_env = os.environ.get("password_hash")

if username_env and password_hash_env:
    USERNAME = username_env
    PASSWORD_HASH = password_hash_env
else:
    # Try secrets.toml (local development only)
    try:
        USERNAME = st.secrets.get("username", "peksiv")
        PASSWORD_HASH = st.secrets.get("password_hash", "de614bf29764c5dd46f33d6dfe3d2b5a098a34fc06ad1da36f13987393dd7fd6")
    except FileNotFoundError:
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
        html, body {
            background: radial-gradient(circle at top, #eef2ff 0%, #dbeafe 25%, #f8fafc 55%, #ffffff 100%) !important;
            color: #0f172a !important;
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
            min-height: 100vh !important;
        }
        .stApp {
            background: radial-gradient(circle at top, #eef2ff 0%, #dbeafe 25%, #f8fafc 55%, #ffffff 100%) !important;
            width: 100vw !important;
            min-height: 100vh !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        .appview-container { 
            background: radial-gradient(circle at top, #eef2ff 0%, #dbeafe 25%, #f8fafc 55%, #ffffff 100%) !important;
            width: 100% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        .main { 
            background: transparent !important; 
            padding: 20px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 100% !important;
            max-width: 100% !important;
        }
        .block-container {
            background: transparent !important;
            box-shadow: none !important;
            padding: 20px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 100% !important;
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
            margin: 0 auto !important;
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
        padding-bottom: 200px;
    }

    .chat-form {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        width: calc(100% - 40px);
        max-width: 900px;
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        padding: 16px 20px;
        z-index: 9999;
        backdrop-filter: blur(10px);
    }

    .chat-form .stTextInput > div {
        margin-bottom: 0 !important;
    }

    .chat-form .stTextInput > div > label {
        display: none !important;
    }

    .chat-form .stTextInput > div > div > input {
        background: #f3f4f6 !important;
        border: 1px solid #e5e7eb !important;
        border-radius: 16px !important;
        padding: 14px 18px !important;
        font-size: 15px !important;
        color: #1f2937 !important;
        width: 100% !important;
    }

    .chat-form .stTextInput > div > div > input::placeholder {
        color: #9ca3af !important;
    }

    .chat-form .stTextInput > div > div > input:focus {
        outline: none !important;
        border: 1px solid #3b82f6 !important;
        background: #ffffff !important;
    }

    .chat-form .stFormSubmitButton > button {
        background: transparent !important;
        color: #3b82f6 !important;
        border: none !important;
        cursor: pointer !important;
        font-size: 20px !important;
        padding: 8px 12px !important;
        height: 40px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    .chat-form .stFormSubmitButton > button:hover {
        color: #2563eb !important;
        background: #f3f4f6 !important;
        border-radius: 8px !important;
    }

    .chat-form form {
        margin: 0 !important;
        padding: 0 !important;
    }

    .chat-form .stColumn {
        padding: 0 4px !important;
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
# POPUP DIALOG FUNCTIONS
# ======================

@st.dialog("➕ Tambah Pemeriksaan Baru", width="large")
def popup_tambah_pemeriksaan():
    # Gunakan variabel lokal agar tidak konflik dengan global
    st.info("Tambah data pemeriksaan baru. Tambah temuan dan kondisi sesuai kebutuhan.")
    
    col1f, col2f = st.columns(2)
    with col1f:
        tgl = st.date_input("Tanggal", value=date.today())
        inst = st.text_input("Instansi")
        tm = st.text_input("Tema")
        nd_p = st.text_input("Nomor ND Pemeriksaan")
        nd_t = st.text_input("Nomor ND Tanggapan")
        tpk = st.text_area("Topik", height=100)
        dok = st.text_input("Dokumen Pendukung (URL)")

    with col2f:
        if st.button("➕ Tambah Temuan Baru"):
            st.session_state.new_findings.append({
                "temuan": "",
                "conditions": [{"kondisi": "", "uraian": "", "tanggapan": ""}]
            })

        for fi, finding in enumerate(st.session_state.new_findings):
            with st.expander(f"Temuan {fi+1}", expanded=True):
                finding["temuan"] = st.text_area("Temuan", value=finding["temuan"], key=f"p_temuan_{fi}")
                for ci, condition in enumerate(finding["conditions"]):
                    st.markdown(f"**Kondisi {ci+1}**")
                    condition["kondisi"] = st.text_area("Kondisi", value=condition["kondisi"], key=f"p_kondisi_{fi}_{ci}")
                    condition["uraian"] = st.text_area("Uraian", value=condition["uraian"], key=f"p_uraian_{fi}_{ci}")
                    condition["tanggapan"] = st.text_area("Tanggapan", value=condition["tanggapan"], key=f"p_tanggapan_{fi}_{ci}")
                
                if st.button("➕ Tambah Kondisi", key=f"p_btn_cond_{fi}"):
                    finding["conditions"].append({"kondisi": "", "uraian": "", "tanggapan": ""})
                    st.rerun()

    if st.button("💾 Simpan Pemeriksaan", use_container_width=True, type="primary"):
        if inst and nd_p:
            next_t = get_next_temuan_number(nd_p, df)
            for fi, finding in enumerate(st.session_state.new_findings, start=1):
                id_t = f"{next_t + fi - 1}.0"
                for ci, cond in enumerate(finding["conditions"], start=1):
                    new_row = {
                        "Tanggal": tgl.isoformat(), "Instansi": inst, "Tema": tm, "Topik": tpk,
                        "Nomor ND Pemeriksaan": nd_p, "Nomor ND Tanggapan": nd_t, "ID_Temuan": id_t,
                        "Temuan": finding["temuan"], "ID_Kondisi": f"{next_t + fi - 1}.{ci}",
                        "Kondisi/Rekomendasi": cond["kondisi"], "Uraian": cond["uraian"],
                        "Tanggapan PEKS IV": cond["tanggapan"], "Dokumen Pendukung": dok
                    }
                    save_row_to_csv(new_row)
            st.success("Berhasil disimpan!")
            st.rerun()

@st.dialog("📋 Detail Pemeriksaan", width="large")
def popup_detail_pemeriksaan(selected_nd):
    # Ambil data spesifik berdasarkan ND
    p_info = df.loc[df["Nomor ND Pemeriksaan"] == selected_nd].iloc[0]
    det_df = df.loc[df["Nomor ND Pemeriksaan"] == selected_nd, 
                    ["Temuan", "Kondisi/Rekomendasi", "Uraian", "Tanggapan PEKS IV"]].copy()
    
    if not det_df.empty:
        det_df = det_df.astype(str).map(normalize_detail_text)
        
        st.markdown(f"### {p_info['Topik']}")
        st.markdown("---")
        
        for _, row in det_df.iterrows():
            with st.container(border=True):
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("#### 🔍 Temuan")
                    st.markdown(row["Temuan"], unsafe_allow_html=True)
                    
                    # Garis pemisah antara Temuan dan Rekomendasi
                    st.markdown("---")
                    
                    st.markdown("#### 💡 Kondisi/Rekomendasi")
                    st.markdown(row["Kondisi/Rekomendasi"], unsafe_allow_html=True)
                with col_b:
                    st.markdown("#### 📝 Uraian")
                    st.markdown(row["Uraian"], unsafe_allow_html=True)
                    
                    # Garis pemisah antara Uraian dan Tanggapan
                    st.markdown("---")
                    
                    st.markdown("#### ✅ Tanggapan PEKS IV")
                    st.markdown(row["Tanggapan PEKS IV"], unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

@st.dialog("➕ Tambah TLHP Baru", width="large")
def popup_tambah_tlhp():
    with st.form("form_tlhp_popup", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            nama = st.text_input("Nama Laporan")
            tgl = st.date_input("Tanggal Laporan")
            thn = st.number_input("Tahun", value=2026)
            peng = st.text_input("Pengawas")
        with c2:
            tem = st.text_area("Temuan")
            rek = st.text_area("Rekomendasi")
            kode = st.text_input("Kode Rekomendasi")
        with c3:
            status = st.selectbox("Status", ["Belum Dimulai", "Dalam Proses", "Selesai"])
            dl = st.date_input("Deadline")
            link = st.text_input("Link Data Dukung")
        
        if st.form_submit_button("Simpan TLHP", use_container_width=True):
            next_no = len(df_tlhp) + 1
            row = {
                "No": str(next_no), "Nama Laporan": nama, "Tgl Laporan": str(tgl), "Tahun": str(thn),
                "Pengawas": peng, "Temuan": tem, "Rekomendasi": rek, "Kode Rekomendasi": kode,
                "Deadline": str(dl), "Status Penyelesaian": status, "Data Dukung (LinkPortal)": link
            }
            save_tlhp_row_to_csv(row)
            st.success("TLHP Tersimpan!")
            st.rerun()

@st.dialog("📋 Detail Tindak Lanjut (TLHP)", width="large")
def popup_detail_tlhp(selected_name):
    detail_df = df_tlhp[df_tlhp["Nama Laporan"].astype(str).str.strip() == selected_name.strip()].copy()
    
    if not detail_df.empty:
        detail_df = detail_df.astype(str).map(normalize_detail_text)
        
        st.markdown(f"### {selected_name}")
        st.markdown("---")
        
        # Penomoran Temuan dengan gaya Box
        for i, (_, row) in enumerate(detail_df.iterrows(), start=1):
            # Badge Box untuk penanda nomor temuan
            st.markdown(f"""
                <div style='background-color: #1e3a8a; color: white; padding: 5px 15px; border-radius: 5px; display: inline-block; font-weight: 700; margin-bottom: 10px;'>
                    TEMUAN {i}
                </div>
            """, unsafe_allow_html=True)
            
            with st.container(border=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("**🔍 Temuan**")
                    st.markdown(row.get("Temuan", "-"), unsafe_allow_html=True)
                    st.markdown("---")
                    st.markdown("**💡 Rekomendasi**")
                    st.markdown(row.get("Rekomendasi", "-"), unsafe_allow_html=True)
                
                with c2:
                    st.markdown("**📝 Rencana Aksi**")
                    st.markdown(row.get("Rencana Aksi", "-"), unsafe_allow_html=True)
                    st.markdown("---")
                    st.markdown("**✅ Progress Pelaksanaan**")
                    st.markdown(row.get("Progress Pelaksanaan Rencana Aksi", "-"), unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown(f"**🔗 Data Dukung:** {row.get('Data Dukung (LinkPortal)', '-')}", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

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
# DAFTAR PEMERIKSAAN & FILTER
# ======================
if menu == "Daftar Pemeriksaan":
    st.markdown(
       """
        <div class='page-section-card'>
            <div class='page-heading'>
                <h1 style='font-size: 32px; font-weight: 800;'>Daftar Pemeriksaan</h1>
                <p style='font-size: 16px; color: #4b5563;'>Basis data koordinasi pemeriksaan, permintaan informasi, serta tindak lanjut Laporan Hasil Pemeriksaan (LHP).</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- TOMBOL TAMBAH (POSISI ATAS) ---
    col_btn_1, col_btn_2 = st.columns([8, 2])
    with col_btn_2:
        st.markdown("<div class='col-button-green'>", unsafe_allow_html=True)
        if st.button("➕ Tambah Pemeriksaan", key="btn_tambah_pemeriksaan_top", use_container_width=True):
            if "new_findings" not in st.session_state:
                st.session_state.new_findings = [{"temuan": "", "conditions": [{"kondisi": "", "uraian": "", "tanggapan": ""}]}]
            popup_tambah_pemeriksaan()
        st.markdown("</div>", unsafe_allow_html=True)

    # --- AREA FILTER DATA (COMPACT VERSION) ---
    with st.container(border=True):
        # Header kecil agar hemat ruang
        st.markdown("<h6 style='margin-bottom: -10px; font-size: 14px;'>🔍 Filter Data</h6>", unsafe_allow_html=True)
        
        # Baris Filter: Kita buat labelnya masuk ke dalam (collapsed) atau pakai font kecil
        c1, c2, c3, c4 = st.columns([1.2, 1.2, 1, 1], gap="small")
        with c1:
            instansi_sel = st.selectbox("Instansi", ["Instansi"] + sorted(df["Instansi"].dropna().unique()), label_visibility="visible")
        with c2:
            tema_sel = st.selectbox("Tema", ["Tema"] + sorted(df["Tema"].dropna().unique()), label_visibility="visible")
        with c3:
            dari_tanggal = st.date_input("Dari", value=None)
        with c4:
            sampai_tanggal = st.date_input("Sampai", value=None)

        # Baris Urutan: Dibuat satu baris tipis
        st.markdown("<div style='margin-top: -15px; border-top: 1px solid #f1f5f9; padding-top: 10px;'></div>", unsafe_allow_html=True)
        
        sort_order = st.radio(
            "**Urutan:**",
            ["Terbaru", "Terlama"],
            index=0,
            horizontal=True,
            key="sort_pemeriksaan_order",
        )

    # --- LOGIKA FILTER DATA ---
    df_filter = df.copy()
    if instansi_sel != "Instansi":
        df_filter = df_filter[df_filter["Instansi"] == instansi_sel]
    if tema_sel != "Tema":
        df_filter = df_filter[df_filter["Tema"] == tema_sel]
    
    if dari_tanggal is not None or sampai_tanggal is not None:
        df_filter["Tanggal"] = pd.to_datetime(df_filter["Tanggal"], errors="coerce")
        if dari_tanggal is not None:
            df_filter = df_filter[df_filter["Tanggal"] >= pd.to_datetime(dari_tanggal)]
        if sampai_tanggal is not None:
            df_filter = df_filter[df_filter["Tanggal"] <= pd.to_datetime(sampai_tanggal)]

    # ======================
    # DATA PEMERIKSAAN (TABEL) - ULTRA PREMIUM UI
    # ======================
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 1. Heading Utama (Clean & Bold)
    st.markdown("""
        <div style='background: #ffffff; padding: 10px 0px; border-bottom: 3px solid #1e3a8a; margin-bottom: 25px;'>
            <h2 style='color: #1e3a8a; margin: 0; font-family: "Inter", sans-serif; font-size: 28px; font-weight: 800; letter-spacing: -0.5px;'>
                📋 Data Pemeriksaan
            </h2>
        </div>
    """, unsafe_allow_html=True)

    # 2. CSS Global (Force Font Inter & Card Styling)
    # 2. CSS Terisolasi (Hanya untuk konten Tabel Daftar Pemeriksaan)
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
            
            /* Targetkan hanya elemen di dalam area konten utama, bukan Sidebar */
            [data-testid="stAppViewContainer"] {
                font-family: 'Inter', sans-serif !important;
            }

            /* Gunakan kelas khusus agar tidak bentrok dengan card di Beranda */
            .pemeriksaan-card-premium {
                background: white;
                border: 1px solid #f1f5f9;
                border-radius: 12px;
                padding: 15px;
                margin-bottom: 10px;
                transition: all 0.3s ease;
            }

            .text-premium-main {
                font-size: 16px !important;
                font-weight: 700 !important;
                color: #0f172a !important;
            }

            .text-premium-sub {
                font-size: 16px !important;
                font-weight: 400 !important;
                color: #334155 !important;
                line-height: 1.5;
            }
        </style>
    """, unsafe_allow_html=True)

    # Logika Pengurutan
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

    # Paginasi
    items_per_page = 10
    total_pages = max(1, (len(df_summary) + items_per_page - 1) // items_per_page)
    if "pemeriksaan_page" not in st.session_state: st.session_state.pemeriksaan_page = 1
    
    start_idx = (st.session_state.pemeriksaan_page - 1) * items_per_page
    page_df = df_summary.iloc[start_idx : start_idx + items_per_page]

    if df_summary.empty:
        st.info("Data tidak ditemukan.")
    else:
        # 3. HEADER TABEL SOLID (Navy Blue Background)
        st.markdown("""
            <div style='background-color: #1e3a8a; padding: 15px; border-radius: 10px 10px 0 0; border: 1px solid #1e3a8a;'>
                <div style='display: flex; flex-direction: row; align-items: center;'>
                    <div style='flex: 0.5; color: white; font-weight: 700; font-size: 13px; text-align: center;'>NO</div>
                    <div style='flex: 1.2; color: white; font-weight: 700; font-size: 13px;'>TANGGAL</div>
                    <div style='flex: 1.3; color: white; font-weight: 700; font-size: 13px;'>INSTANSI</div>
                    <div style='flex: 1.8; color: white; font-weight: 700; font-size: 13px;'>ND TANGGAPAN</div>
                    <div style='flex: 1.3; color: white; font-weight: 700; font-size: 13px;'>TEMA</div>
                    <div style='flex: 2.7; color: white; font-weight: 700; font-size: 13px;'>TOPIK</div>
                    <div style='flex: 0.7; color: white; font-weight: 700; font-size: 13px; text-align: center;'>DETAIL</div>
                    <div style='flex: 0.7; color: white; font-weight: 700; font-size: 13px; text-align: center;'>FILE</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

        # 4. ISI DATA (Premium Cards)
        for row_num, (_, row) in enumerate(page_df.iterrows(), start=1):
            idx = start_idx + row_num
            
            with st.container():
                cols = st.columns([0.5, 1.2, 1.3, 1.8, 1.3, 2.7, 0.7, 0.7])
                
                cols[0].markdown(f"<div class='text-premium-main' style='text-align: center;'>{idx}</div>", unsafe_allow_html=True)
                cols[1].markdown(f"<div class='text-premium-sub'>{row['Tanggal']}</div>", unsafe_allow_html=True)
                cols[2].markdown(f"<div class='text-premium-main' style='color: #1d4ed8;'>{row['Instansi']}</div>", unsafe_allow_html=True)
                cols[3].markdown(f"<div class='text-premium-sub' style='font-family: monospace; font-weight: bold;'>{row.get('Nomor ND Tanggapan', '-')}</div>", unsafe_allow_html=True)
                
                cols[4].markdown(f"<span class='badge-tema-solid'>{row['Tema']}</span>", unsafe_allow_html=True)
                cols[5].markdown(f"<div class='text-premium-sub'>{row['Topik']}</div>", unsafe_allow_html=True)

                with cols[6]:
                    if st.button("🔍", key=f"btn_v_{idx}", use_container_width=True):
                        st.session_state.selected_nd = row["Nomor ND Pemeriksaan"]
                
                with cols[7]:
                    url = row.get("Dokumen Pendukung", "")
                    if isinstance(url, str) and url.strip():
                        st.markdown(f"<div style='text-align: center;'><a href='{url.strip()}' target='_blank' style='font-size: 22px; text-decoration: none;'>📂</a></div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div style='text-align: center; color: #cbd5e1; font-size: 22px;'>-</div>", unsafe_allow_html=True)
                
                st.markdown("<div style='border-bottom: 1px solid #f1f5f9; margin: 15px 0;'></div>", unsafe_allow_html=True)

        # 5. NAVIGATION
        st.markdown("<br>", unsafe_allow_html=True)
        n_col1, n_col2, n_col3 = st.columns([1, 2, 1])
        with n_col1:
            if st.button("← Previous", key="prev_p", disabled=st.session_state.pemeriksaan_page == 1, use_container_width=True):
                st.session_state.pemeriksaan_page -= 1
                st.rerun()
        with n_col2:
            st.markdown(f"<div style='text-align: center; font-weight: 700; color: #1e293b; font-size: 16px; padding-top: 8px;'>Halaman {st.session_state.pemeriksaan_page} dari {total_pages}</div>", unsafe_allow_html=True)
        with n_col3:
            if st.button("Next →", key="next_p", disabled=st.session_state.pemeriksaan_page == total_pages, use_container_width=True):
                st.session_state.pemeriksaan_page += 1
                st.rerun()

        # ======================
        # DETAIL PEMERIKSAAN
        # ======================
        # Karena detail sudah muncul via Popup (st.dialog), 
        # kita hanya perlu memastikan state pilihan dibersihkan saat tidak digunakan.

        if st.session_state.get("selected_nd"):
            # Memanggil fungsi popup yang sudah kamu buat di bagian HELPERS
            popup_detail_pemeriksaan(st.session_state.selected_nd)
            
            # Setelah popup tertutup/selesai, kita kosongkan pilihan agar tidak muncul terus-menerus
            st.session_state.selected_nd = None

# ======================
# TLHP PEKS IV - FULL PREMIUM UI
# ======================
if menu == "TLHP PEKS IV":
    # 1. HERO HEADING (SAMA DENGAN DAFTAR PEMERIKSAAN)
    st.markdown(
        """
        <div class='page-section-card'>
            <div class='page-heading'>
                <h1 style='font-size: 32px; font-weight: 800;'>Tindak Lanjut Hasil Pemeriksaan (TLHP)</h1>
                <p style='font-size: 16px; color: #4b5563;'>Pemantauan realisasi rencana aksi dan validasi data dukung tindak lanjut hasil pengawasan secara akuntabel.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- TOMBOL TAMBAH (POSISI ATAS) ---
    col_btn_1, col_btn_2 = st.columns([8, 2])
    with col_btn_2:
        st.markdown("<div class='col-button-green'>", unsafe_allow_html=True)
        # PASTIKAN memanggil fungsi popup_tambah_tlhp() di sini
        if st.button("➕ Tambah TLHP", key="btn_tambah_tlhp_top", use_container_width=True):
            popup_tambah_tlhp() 
        st.markdown("</div>", unsafe_allow_html=True)


    # FILTER & SORTING
    with st.container(border=True):
        st.markdown("##### Filter Data")
        sort_tlhp_order = st.radio("**Urutan Laporan:**", ["Terbaru ke Terlama", "Terlama ke Terbaru"], index=0, horizontal=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if not df_tlhp.empty:
        # Logika Summary & Sorting
        df_tlhp_summary = df_tlhp.groupby("Nama Laporan", sort=False, as_index=False).first()
        df_tlhp_summary["Tgl_Parsed"] = pd.to_datetime(df_tlhp_summary["Tgl Laporan"], errors="coerce")
        asc_tlhp = False if sort_tlhp_order == "Terbaru ke Terlama" else True
        df_tlhp_summary = df_tlhp_summary.sort_values("Tgl_Parsed", ascending=asc_tlhp).reset_index(drop=True)

        # Pagination
        if "tlhp_page" not in st.session_state: st.session_state.tlhp_page = 1
        items_per_page = 10
        total_p = max(1, (len(df_tlhp_summary) + items_per_page - 1) // items_per_page)
        start_idx = (st.session_state.tlhp_page - 1) * items_per_page
        page_df = df_tlhp_summary.iloc[start_idx : start_idx + items_per_page]

        # HEADER TABEL SOLID NAVY
        st.markdown("""
            <div style='background-color: #1e3a8a; padding: 15px; border-radius: 10px 10px 0 0; border: 1px solid #1e3a8a;'>
                <div style='display: flex; flex-direction: row; align-items: center;'>
                    <div style='flex: 0.4; color: white; font-weight: 700; font-size: 13px; text-align: center;'>NO</div>
                    <div style='flex: 4.0; color: white; font-weight: 700; font-size: 13px;'>NAMA LAPORAN</div>
                    <div style='flex: 1.0; color: white; font-weight: 700; font-size: 13px; text-align: center;'>TAHUN</div>
                    <div style='flex: 1.5; color: white; font-weight: 700; font-size: 13px;'>LEAD UKE II</div>
                    <div style='flex: 1.2; color: white; font-weight: 700; font-size: 13px; text-align: center;'>STATUS</div>
                    <div style='flex: 0.8; color: white; font-weight: 700; font-size: 13px; text-align: center;'>DETAIL</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

        # ISI DATA
        # Pemetaan warna status yang diperbarui
        status_colors = {
            "Selesai": "#10b981",              # Hijau (Final)
            "Sedang Diusulkan Sesuai": "#84cc16", # Lime/Hijau Kekuningan (Antara Oranye & Hijau)
            "Dalam Proses": "#f59e0b",         # Oranye (Sedang dikerjakan)
            "Sedang Berjalan": "#fbbf24",      # Kuning (Baru mulai)
            "Belum Dimulai": "#ef4444",        # Merah (Belum ada aksi)
            "Tertunda": "#8b5cf6"              # Ungu
        }

        for i, row in page_df.iterrows():
            idx = start_idx + i + 1
            s_val = str(row.get('Status Penyelesaian', '-') or '-')
            s_bg = status_colors.get(s_val, '#64748b')

            cols = st.columns([0.4, 4.0, 1.0, 1.5, 1.2, 0.8])
            cols[0].markdown(f"<div style='text-align: center; font-weight: 700;'>{idx}</div>", unsafe_allow_html=True)
            cols[1].markdown(f"<div style='font-weight: 700;'>{row['Nama Laporan']}</div>", unsafe_allow_html=True)
            cols[2].markdown(f"<div style='text-align: center;'>{row['Tahun']}</div>", unsafe_allow_html=True)
            cols[3].markdown(f"<div style='color: #1d4ed8; font-weight: 700;'>{row['Lead UKE II']}</div>", unsafe_allow_html=True)
            cols[4].markdown(f"<div style='text-align: center;'><span style='background: {s_bg}; color: white; padding: 4px 10px; border-radius: 6px; font-size: 12px; font-weight: 700;'>{s_val}</span></div>", unsafe_allow_html=True)
            
            with cols[5]:
                if st.button("🔍", key=f"tlhp_v_{idx}", use_container_width=True):
                    popup_detail_tlhp(row['Nama Laporan']) # Langsung panggil popup

            st.markdown("<div style='border-bottom: 1px solid #f1f5f9; margin: 15px 0;'></div>", unsafe_allow_html=True)

        # NAVIGASI HALAMAN
        n1, n2, n3 = st.columns([1, 2, 1])
        with n1:
            if st.button("← Previous", key="tlhp_prev", disabled=st.session_state.tlhp_page == 1):
                st.session_state.tlhp_page -= 1
                st.rerun()
        with n2:
            st.markdown(f"<div style='text-align: center; font-weight: 700;'>Halaman {st.session_state.tlhp_page} dari {total_p}</div>", unsafe_allow_html=True)
        with n3:
            if st.button("Next →", key="tlhp_next", disabled=st.session_state.tlhp_page == total_p):
                st.session_state.tlhp_page += 1
                st.rerun()
    else:
        st.info("Belum ada data TLHP.")

# ======================
# AI SIERA (SMART & SECURE ENGINE) - SMART LOGIC FIX
# ======================
if menu == "AI SIERA":
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    current_user = st.session_state.get('username', 'peksiv')

    st.markdown(
        """
        <div class='page-section-card'>
            <div class='page-heading'>
                <h1 style='font-size: 32px; font-weight: 800;'>🛡️ AI SIERA (Smart & Secure Engine)</h1>
                <p style='font-size: 16px; color: #4b5563;'>Asisten cerdas berbasis data untuk membantu akurasi status, substansi topik, dan monitoring hasil pemeriksaan.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- CSS: LAYOUT & FIXED BUTTON ---
    st.markdown("""
        <style>
            [data-testid="stChatMessageContainer"] { padding-bottom: 180px !important; }
            
            /* Bubble Chat Kanan-Kiri */
            [data-testid="stChatMessage"] { padding: 1rem !important; border-radius: 15px !important; margin-bottom: 15px !important; max-width: 80% !important; display: flex !important; }
            div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) { flex-direction: row-reverse !important; margin-left: auto !important; background-color: #dbeafe !important; border: 1px solid #bfdbfe !important; }
            [data-testid="chatAvatarIcon-user"] { display: none !important; }
            div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) { margin-right: auto !important; background-color: #ffffff !important; border: 1px solid #e2e8f0 !important; border-left: 5px solid #1e3a8a !important; }

            /* Fixed Floating Button */
            .floating-clear-container { position: fixed; bottom: 95px; right: 50px; z-index: 1000000; }
            .floating-clear-container button { background-color: white !important; border: 1px solid #cbd5e1 !important; box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important; color: #475569 !important; }
            
            /* Chat Input Contrast */
            div[data-testid="stChatInput"] { background-color: #f1f5f9 !important; border: 2px solid #cbd5e1 !important; border-radius: 12px !important; }
        </style>
    """, unsafe_allow_html=True)

    df_ref = df.copy() 
    df_monitoring = df_tlhp.copy() 

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    def siera_smart_brain(query):
        q = query.lower().strip()
        user_name = st.session_state.get('username', 'peksiv')
        
        # 1. KAMUS SINONIM SEDERHANA (Manual Synonyms)
        synonyms = {
            "progres": ["proses", "tindak lanjut", "jalan", "pelaksanaan"],
            "stunting": ["tengkes", "gizi buruk", "anak"],
            "mbg": ["makan bergizi gratis", "makan siang", "pangan"],
            "anggaran": ["dana", "biaya", "keuangan"]
        }
        
        # Ekspansi kueri berdasarkan sinonim
        expanded_q = q
        for key, vals in synonyms.items():
            if key in q:
                expanded_q += " " + " ".join(vals)

        # 2. LOGIKA MONITORING TLHP
        is_all_tlhp = any(x in q for x in ["tlhp peks iv", "semua tlhp", "daftar tlhp", "tampilkan tlhp"])
        is_process_query = any(x in q for x in ["tlhp proses", "tlhp progres", "sedang diproses"])

        if is_all_tlhp or is_process_query or any(word in q for word in ["selesai", "rekomendasi"]):
            if is_all_tlhp:
                df_filtered = df_monitoring
                narasi = f"Halo **{user_name}**, berikut adalah seluruh data **TLHP PEKS IV** yang tersedia:"
            elif is_process_query:
                df_filtered = df_monitoring[df_monitoring["Status Penyelesaian"].str.lower().isin(["dalam proses", "sedang diusulkan sesuai"])]
                narasi = f"Halo **{user_name}**, ini adalah daftar TLHP yang berstatus **Dalam Proses** atau **Sedang Diusulkan Sesuai**:"
            else:
                target_status = ["selesai"] if "selesai" in q else ["dalam proses", "sedang diusulkan sesuai"]
                df_filtered = df_monitoring[df_monitoring["Status Penyelesaian"].str.lower().isin(target_status)]
                narasi = f"Halo **{user_name}**, berikut data TLHP dengan status terkait kueri Anda:"

            if df_filtered.empty: 
                return f"Maaf **{user_name}**, data TLHP tidak ditemukan.", None, "fail"
            return narasi, df_filtered, "tlhp_detail_mode"
            
        # 3. LOGIKA DATABASE PEMERIKSAAN (DENGAN WEIGHTING)
        else:
            # PEMBERIAN BOBOT: Topik, Tema, dan Instansi diberikan pengulangan agar lebih diprioritaskan AI
            df_ref["kb_text"] = df_ref.apply(lambda r: (
                f"{r.get('Topik',' ')} " * 3 + 
                f"{r.get('Tema',' ')} " * 2 + 
                f"{r.get('Instansi',' ')} " + 
                f"{r.get('Temuan',' ')} " + 
                f"{r.get('Kondisi/Rekomendasi',' ')}"
            ).lower(), axis=1)
            
            vectorizer = TfidfVectorizer(ngram_range=(1, 2))
            tfidf_matrix = vectorizer.fit_transform(df_ref["kb_text"])
            query_vec = vectorizer.transform([expanded_q])
            cos_sim = cosine_similarity(query_vec, tfidf_matrix).flatten()
            
            top_indices = cos_sim.argsort()[-3:][::-1]
            matches = [df_ref.iloc[idx] for idx in top_indices if cos_sim[idx] > 0.05]
            
            if matches: 
                return f"Halo **{user_name}**, berikut referensi database pemeriksaan yang relevan:", matches, "ref_mode"
            return f"Maaf **{user_name}**, SIERA tidak menemukan data yang relevan. Coba gunakan kata kunci lain.", None, "fail"

    # --- DISPLAY CHAT ---
    for role, content in st.session_state.chat_history:
        narasi, data, mode = content
        with st.chat_message(role):
            st.markdown(narasi)
            if data is not None:
                if mode == "tlhp_detail_mode":
                    for lap in data["Nama Laporan"].unique():
                        with st.expander(f"📋 {lap}"):
                            for _, r in data[data["Nama Laporan"] == lap].iterrows():
                                st.info(f"**Rekomendasi:** {r.get('Rekomendasi', '-')}")
                                st.caption(f"📅 Deadline: {r.get('Deadline', '-')} | Status: {r.get('Status Penyelesaian', '-')}")
                elif mode == "ref_mode":
                    for r in data:
                        with st.expander(f"🔍 {r.get('Instansi','-')} | {r.get('Tema','-')}"):
                            st.markdown(f"**Topik:** {r.get('Topik', '-')}")
                            st.markdown("---")
                            st.write(f"**Temuan:** {r.get('Temuan', '-')}")
                            st.markdown("---")
                            st.info(f"**Kondisi/Rekomendasi:**\n{r.get('Kondisi/Rekomendasi', '-')}")
                            st.success(f"**Tanggapan PEKS IV:**\n{r.get('Tanggapan PEKS IV', '-')}")

    # --- BRAIN LOGIC ---
    if user_input := st.chat_input("Tanya SIERA..."):
        st.session_state.chat_history.append(("user", (user_input, None, "user_msg")))
        st.rerun()

    if st.session_state.chat_history and st.session_state.chat_history[-1][0] == "user":
        u_in = st.session_state.chat_history[-1][1][0]
        with st.chat_message("assistant"):
            with st.spinner("SIERA sedang berpikir..."):
                resp = siera_smart_brain(u_in)
                st.session_state.chat_history.append(("assistant", resp))
        st.rerun()

    # --- FIXED FLOATING CLEAR BUTTON ---
    st.markdown('<div class="floating-clear-container">', unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat", key="final_fixed_clear"):
        st.session_state.chat_history = []
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)