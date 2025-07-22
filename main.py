import streamlit as st
from PIL import Image
import base64
from io import BytesIO

st.set_page_config(page_title="SecureSteg | Advanced Image Steganography", page_icon=":shield:", layout="wide")

# --- Helper Functions (encoding/decoding logic) ---
def encode_data(image, data):
    data = data + "$"  # Delimiter
    data_bin = ''.join(format(ord(char), '08b') for char in data)
    pixels = list(image.getdata())
    encoded_pixels = []
    index = 0
    for pixel in pixels:
        if index < len(data_bin):
            red_pixel = pixel[0]
            new_pixel = (red_pixel & 254) | int(data_bin[index])
            encoded_pixels.append((new_pixel, pixel[1], pixel[2]))
            index += 1
        else:
            encoded_pixels.append(pixel)
    return encoded_pixels

def decode_data(image):
    pixels = list(image.getdata())
    data_bin = ""
    for pixel in pixels:
        data_bin += bin(pixel[0])[-1]
    data = ""
    for i in range(0, len(data_bin), 8):
        byte = data_bin[i:i + 8]
        data += chr(int(byte, 2))
        if data[-1] == "$":
            break
    return data[:-1]

# --- Custom CSS for Modern UI (White BG, Full Width, Black Text) ---
st.markdown('''
<style>
body, .stApp, .block-container { background: #fff !important; }
header { display: none; }

/* Header */
.secure-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 2rem; width: 100%; }
.secure-logo { background: #a78bfa; border-radius: 16px; padding: 0.5rem 0.7rem; display: flex; align-items: center; }
.secure-logo-icon { font-size: 2rem; color: #fff; margin-right: 0.5rem; }
.secure-title { font-size: 2rem; font-weight: 700; color: #7c3aed; margin-bottom: 0; }
.secure-subtitle { color: #888; font-size: 1rem; margin-top: -0.5rem; }
.secure-viewsrc { border: 1.5px solid #7c3aed; border-radius: 12px; padding: 0.7rem 1.5rem; color: #fff; background: #7c3aed; font-weight: 600; text-decoration: none; transition: 0.2s; font-size: 1.1rem; box-shadow: 0 2px 8px #ede9fe44; }
.secure-viewsrc:hover { background: #a78bfa; color: #fff; }

/* Hero */
.hero-badge { background: #ede9fe; color: #7c3aed; border-radius: 999px; padding: 0.3rem 1.2rem; font-weight: 600; display: inline-block; margin-bottom: 1.2rem; }
.hero-title { font-size: 3rem; font-weight: 800; color: #222; line-height: 1.1; margin-bottom: 0.5rem; }
.hero-title .highlight { color: #a78bfa; }
.hero-desc { color: #555; font-size: 1.2rem; margin-bottom: 1.2rem; }
.hero-features { display: flex; gap: 2rem; justify-content: center; margin-bottom: 2rem; }
.hero-feature { font-size: 1rem; display: flex; align-items: center; gap: 0.5rem; }
.hero-feature.green { color: #22c55e; }
.hero-feature.purple { color: #7c3aed; }
.hero-feature.yellow { color: #eab308; }

/* Card Tabs */
.card-tabs { display: flex; gap: 1.5rem; justify-content: center; margin-bottom: 2.5rem; width: 100%; }
.card-tab { flex: 1; background: #fff; border-radius: 18px; border: 2.5px solid #ede9fe; padding: 1.5rem 0.5rem; text-align: center; cursor: pointer; transition: 0.2s; font-size: 1.2rem; font-weight: 600; color: #222; box-shadow: 0 2px 8px #ede9fe44; }
.card-tab.selected { border: 2.5px solid #a78bfa; background: #f6f3ff; color: #7c3aed; }
.card-tab .tab-icon { font-size: 2.2rem; display: block; margin-bottom: 0.5rem; }

/* Section Card */
.section-card { background: #fff; border-radius: 18px; box-shadow: 0 2px 8px #ede9fe44; margin-bottom: 2rem; padding: 0; width: 100%; }
.section-header { background: linear-gradient(90deg, #a78bfa 0%, #7c3aed 100%); color: #fff; border-radius: 18px 18px 0 0; padding: 1.2rem 1.5rem; font-size: 1.3rem; font-weight: 700; display: flex; align-items: center; gap: 0.7rem; }
.section-desc { color: #a78bfa; font-size: 1rem; margin: 0 0 1.2rem 0; padding: 0 1.5rem; }
.section-body { padding: 1.5rem; }

/* Inputs & Buttons */
.stTextArea textarea, .stTextInput input { border-radius: 12px !important; border: 1.5px solid #ede9fe !important; font-size: 1.1rem; background: #fff !important; color: #222 !important; }
.stTextArea label, .stTextInput label, .stFileUploader label { color: #222 !important; }
.stFileUploader { border-radius: 12px !important; border: 1.5px solid #ede9fe !important; background: #fff !important; color: #222 !important; }
.stButton > button { border-radius: 12px !important; background: linear-gradient(90deg, #7c3aed 0%, #a78bfa 100%) !important; color: #fff !important; font-weight: 700 !important; font-size: 1.1rem !important; padding: 0.9rem 0 !important; margin-top: 1rem; box-shadow: 0 2px 8px #ede9fe44; }
.stButton > button:disabled { background: #ede9fe !important; color: #bbb !important; }

/* Preview Area */
.preview-area { border: 2.5px dashed #ede9fe; border-radius: 16px; padding: 2.5rem 1rem; text-align: center; color: #a78bfa; margin-bottom: 1.5rem; background: #fff; }
.preview-area .preview-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }
.preview-area .preview-title { font-size: 1.2rem; font-weight: 700; color: #444; }
.preview-area .preview-desc { color: #888; font-size: 1rem; }

/* Footer */
.secure-footer { text-align: center; color: #888; font-size: 1rem; margin-top: 2.5rem; margin-bottom: 0.5rem; width: 100%; }
.secure-footer .footer-icon { color: #a78bfa; margin-right: 0.3rem; }

/* Full width for main container */
.block-container { max-width: 100vw !important; padding-left: 2vw !important; padding-right: 2vw !important; }
</style>
''', unsafe_allow_html=True)

# --- Header ---
st.markdown('''
<div class="secure-header">
  <div style="display: flex; align-items: center; gap: 0.7rem;">
    <span class="secure-logo"><span class="secure-logo-icon">🛡️</span></span>
    <div>
      <div class="secure-title">disma</div>
      <div class="secure-subtitle">Advanced Image Steganography</div>
    </div>
  </div>
  <a class="secure-viewsrc" href="https://github.com/madhavchaturvedi005/image_steganography_project" target="_blank"> <span style="margin-right:0.5em;">🍴</span>View Source</a>
</div>
''', unsafe_allow_html=True)

# --- Hero Section ---
st.markdown('''
<div class="hero-badge"> <span style="margin-right:0.5em;">🔒</span> Military-Grade LSB Steganography </div>
<div class="hero-title">Hide Your Secrets in <span class="highlight">Plain Sight</span></div>
<div class="hero-desc">Securely embed secret messages into images using advanced Least Significant Bit (LSB) steganography. Your secrets remain invisible to the naked eye.</div>
<div class="hero-features">
  <div class="hero-feature green">● Zero Data Loss</div>
  <div class="hero-feature purple">● Browser-Based Security</div>
  <div class="hero-feature yellow">● Undetectable to Human Eye</div>
</div>
''', unsafe_allow_html=True)

# --- Card Tabs ---
tab_labels = ["Hide Message", "Reveal Message"]
tab_icons = ["＋", "🔍"]
tab_descs = ["Encode secret text into an image", "Decode hidden text from an image"]

if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = 0

col1, col2 = st.columns(2)
with col1:
    if st.button("＋ Hide Message", key="tab_hide", use_container_width=True):
        st.session_state.selected_tab = 0
with col2:
    if st.button("🔍 Reveal Message", key="tab_reveal", use_container_width=True):
        st.session_state.selected_tab = 1

# --- Encode Section ---
if st.session_state.selected_tab == 0:
    st.markdown('''<div class="section-card">
      <div class="section-header">🛡️ Encode Secret Message</div>
      <div class="section-desc" style="margin-bottom:0.5rem;">Hide your secret message inside an image using LSB steganography</div>
      <div class="section-body" style="padding-top:0.5rem;">''', unsafe_allow_html=True)
    
    st.markdown('''<style>
    textarea, .stTextArea textarea, .stTextInput input { background: #fff !important; }
    .stFileUploader { background: #fff !important; }
    </style>''', unsafe_allow_html=True)
    
    message = st.text_area("Secret Message", placeholder="Enter your secret message here...", key="encode_msg")
    image_file = st.file_uploader("Cover Image", type=["png", "jpg", "jpeg"], key="encode_img")
    encode_btn = st.button("Hide Message in Image", key="encode_btn", use_container_width=True, disabled=not (message and image_file))
    
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="preview-area">', unsafe_allow_html=True)
    if encode_btn and image_file and message:
        try:
            image = Image.open(image_file).convert("RGB")
            encoded_image = image.copy()
            encoded_image.putdata(encode_data(image, message))
            buffered = BytesIO()
            encoded_image.save(buffered, format="PNG")
            img_bytes = buffered.getvalue()
            st.image(encoded_image, caption="Encoded Image Preview", use_column_width=True)
            img_str = base64.b64encode(img_bytes).decode()
            href = f'<div style="display:flex;justify-content:center;"><a href="data:file/png;base64,{img_str}" download="encoded.png" class="secure-viewsrc" style="margin-top:1.2em;display:inline-block;">⬇️ Download Encoded Image</a></div>'
            st.markdown(href, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error encoding image: {e}")
    else:
        st.markdown('<div class="preview-icon">👁️</div><div class="preview-title">Encoded Image Preview</div><div class="preview-desc">Your steganography result will appear here</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Decode Section ---
if st.session_state.selected_tab == 1:
    st.markdown('''<div class="section-card">
      <div class="section-header">🔍 Reveal Secret Message</div>
      <div class="section-desc" style="margin-bottom:0.5rem;">Decode hidden text from an image using LSB steganography</div>
      <div class="section-body" style="padding-top:0.5rem;">''', unsafe_allow_html=True)
    
    st.markdown('''<style>
    .stFileUploader { background: #fff !important; }
    .preview-area .preview-desc, .preview-area .preview-title, .preview-area .preview-icon { color: #222 !important; }
    </style>''', unsafe_allow_html=True)
    
    decode_image_file = st.file_uploader("Encoded Image", type=["png", "jpg", "jpeg"], key="decode_img")
    decode_btn = st.button("Reveal Message", key="decode_btn", use_container_width=True, disabled=not decode_image_file)
    st.markdown('</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="preview-area">', unsafe_allow_html=True)
    if decode_btn and decode_image_file:
        try:
            decode_image = Image.open(decode_image_file).convert("RGB")
            decoded_message = decode_data(decode_image)
            st.markdown(f'<div class="preview-icon">📜</div><div class="preview-title">Hidden Message Revealed</div><div class="preview-desc" style="color:#222 !important;font-size:1.1rem;margin-top:1em;">{decoded_message if decoded_message else "No hidden message found or image is not properly encoded."}</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error decoding image: {e}")
    else:
        st.markdown('<div style="text-align:center;">'
            '<div class="preview-icon" style="color:#000 !important;">👁️</div>'
            '<div class="preview-title" style="color:#000 !important;">Decoded Message Preview</div>'
            '<div class="preview-desc" style="color:#000 !important;">Your decoded message will appear here</div>'
            '</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Footer ---
st.markdown('''<div class="secure-footer">
  <span class="footer-icon">🛡️</span> Built with security and privacy in mind. All processing happens in your browser.<br>
  © 2024 SecureSteg. Educational purposes only. Use responsibly.
</div>''', unsafe_allow_html=True)
