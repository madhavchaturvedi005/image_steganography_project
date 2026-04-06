import streamlit as st

def load_css():
    st.markdown('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
* { font-family: 'Inter', sans-serif !important; }
body, .stApp { background: #ffffff !important; }
.block-container { padding: 0 !important; max-width: 100% !important; margin: 0 !important; }
header, footer { display: none !important; }
.navbar { position: sticky; top: 0; z-index: 100; background: #fff; border-bottom: 1px solid #e5e7eb; display: flex; align-items: center; justify-content: space-between; padding: 0 4rem; height: 64px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }
.nav-brand { display: flex; align-items: center; gap: 0.75rem; }
.nav-logo { width: 36px; height: 36px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 1.1rem; font-weight: 800; }
.nav-title { font-size: 1.25rem; font-weight: 800; color: #111; }
.nav-links { display: flex; align-items: center; gap: 0.5rem; }
.nav-link { color: #6b7280 !important; text-decoration: none; font-weight: 600; font-size: 0.9rem; padding: 0.5rem 1rem; border-radius: 8px; transition: all 0.15s; }
.nav-link:hover { background: #f3f4f6; color: #111 !important; }
.nav-link.active { background: #f0f4ff; color: #667eea !important; }
.nav-btn { background: linear-gradient(135deg, #667eea, #764ba2); color: #fff !important; text-decoration: none; font-weight: 700; font-size: 0.9rem; padding: 0.55rem 1.3rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(102,126,234,0.3); transition: all 0.15s; }
.nav-btn:hover { opacity: 0.92; transform: translateY(-1px); }
.hero { background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; text-align: center; padding: 4.5rem 2rem 4rem; }
.hero-tag { display: inline-block; background: rgba(255,255,255,0.2); color: #fff; border: 1px solid rgba(255,255,255,0.3); border-radius: 999px; padding: 0.35rem 1.1rem; font-weight: 600; font-size: 0.8rem; letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 1.5rem; }
.hero-title { font-size: 3.5rem; font-weight: 900; line-height: 1.1; margin-bottom: 1.2rem; }
.hero-desc { font-size: 1.15rem; line-height: 1.7; max-width: 650px; margin: 0 auto 2.5rem; opacity: 0.95; }
.chips { display: flex; gap: 0.75rem; justify-content: center; flex-wrap: wrap; }
.chip { padding: 0.45rem 1.1rem; border-radius: 8px; font-weight: 600; font-size: 0.85rem; background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.3); }
.content-wrap { max-width: 900px; margin: 0 auto; padding: 3rem 4rem 5rem; }
.tab-bar { display: flex; gap: 0; margin-bottom: 2.5rem; background: #f3f4f6; border-radius: 12px; padding: 4px; }
.tab-bar .stButton > button { background: transparent !important; color: #6b7280 !important; -webkit-text-fill-color: #6b7280 !important; box-shadow: none !important; border-radius: 9px !important; font-weight: 600 !important; font-size: 0.95rem !important; padding: 0.65rem 0 !important; margin-top: 0 !important; border: none !important; transition: all 0.15s !important; }
.tab-bar .stButton > button:hover:not(:disabled) { background: #e5e7eb !important; color: #111 !important; -webkit-text-fill-color: #111 !important; transform: none !important; box-shadow: none !important; }
.card { background: #fff; border: 1px solid #e5e7eb; border-radius: 16px; overflow: hidden; margin-bottom: 2rem; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
.card-head { padding: 1.5rem 2rem; border-bottom: 1px solid #f0f0f0; display: flex; align-items: center; gap: 0.75rem; }
.card-icon { width: 40px; height: 40px; border-radius: 10px; background: linear-gradient(135deg, #667eea, #764ba2); display: flex; align-items: center; justify-content: center; font-size: 1.1rem; font-weight: 800; color: #fff; }
.card-head-title { font-size: 1.1rem; font-weight: 700; color: #111; }
.card-head-desc { font-size: 0.88rem; color: #9ca3af; margin-top: 0.15rem; }
.card-body { padding: 2rem; }
.stTextArea label, .stTextInput label, .stFileUploader label { color: #374151 !important; -webkit-text-fill-color: #374151 !important; font-weight: 600 !important; font-size: 0.9rem !important; }
.stTextArea textarea, .stTextInput input { border-radius: 10px !important; border: 1.5px solid #e5e7eb !important; font-size: 0.95rem !important; background: #fafafa !important; color: #111 !important; -webkit-text-fill-color: #111 !important; padding: 0.8rem !important; transition: all 0.2s !important; }
.stTextArea textarea:focus, .stTextInput input:focus { border-color: #667eea !important; background: #fff !important; box-shadow: 0 0 0 3px rgba(102,126,234,0.1) !important; }
div[data-testid="stFileUploaderDropzone"] { background: #1a1a2e !important; border: 2px dashed #667eea !important; border-radius: 10px !important; padding: 2rem !important; }
div[data-testid="stFileUploaderDropzone"]:hover { border-color: #764ba2 !important; }
div[data-testid="stFileUploaderDropzone"] *, div[data-testid="stFileUploaderDropzone"] span, div[data-testid="stFileUploaderDropzone"] p, div[data-testid="stFileUploaderDropzone"] small { color: #e2e8f0 !important; -webkit-text-fill-color: #e2e8f0 !important; }
div[data-testid="stCheckbox"] {
    margin-top: -3.5rem;
    margin-bottom: 1rem;
}
div[data-testid="stCheckbox"] label {
    font-weight: 600 !important;
    color: #374151 !important;
    font-size: 0.9rem !important;
}
.stButton > button { border-radius: 10px !important; background: linear-gradient(135deg, #667eea, #764ba2) !important; color: #fff !important; -webkit-text-fill-color: #fff !important; font-weight: 700 !important; font-size: 0.95rem !important; padding: 0.85rem 0 !important; margin-top: 1.5rem !important; border: none !important; box-shadow: 0 2px 10px rgba(102,126,234,0.3) !important; transition: all 0.15s !important; }
.stButton > button:hover:not(:disabled) { transform: translateY(-1px) !important; box-shadow: 0 4px 16px rgba(102,126,234,0.4) !important; }
.stButton > button:disabled { background: #f3f4f6 !important; color: #9ca3af !important; -webkit-text-fill-color: #9ca3af !important; box-shadow: none !important; }
.preview-box { border: 2px dashed #e5e7eb; border-radius: 12px; padding: 3.5rem 2rem; text-align: center; background: #fafafa; margin-top: 1.5rem; }
.preview-title { font-size: 1rem; font-weight: 700; color: #374151; margin-bottom: 0.4rem; }
.preview-desc { color: #9ca3af; font-size: 0.88rem; }
.decoded-label { font-size: 0.72rem; font-weight: 700; color: #667eea; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.6rem; }
.decoded-box { background: #f8f9ff; border: 1.5px solid #c7d2fe; border-radius: 10px; padding: 1.5rem; font-family: 'Courier New', monospace; font-size: 0.95rem; color: #1a1a1a; white-space: pre-wrap; word-break: break-word; line-height: 1.7; }
.dl-btn { display: inline-block; margin-top: 1.25rem; background: linear-gradient(135deg, #667eea, #764ba2); color: #fff !important; text-decoration: none; padding: 0.75rem 2rem; border-radius: 10px; font-weight: 700; font-size: 0.9rem; box-shadow: 0 2px 10px rgba(102,126,234,0.3); transition: all 0.15s; }
.dl-btn:hover { transform: translateY(-1px); box-shadow: 0 4px 16px rgba(102,126,234,0.4); }
.divider { border: none; border-top: 1px solid #f0f0f0; margin: 2rem 0; }
.app-footer { text-align: center; color: #9ca3af; font-size: 0.85rem; padding: 2.5rem 0 2rem; border-top: 1px solid #f0f0f0; margin-top: 3rem; }
</style>
''', unsafe_allow_html=True)
