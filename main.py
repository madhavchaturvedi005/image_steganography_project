import streamlit as st
from PIL import Image
import base64
import random
from io import BytesIO
from quantum_crypto import generate_bb84_key, xor_encrypt, xor_decrypt, key_bits_to_str, str_to_key_bits
from styles import load_css

st.set_page_config(page_title="ImageShield", page_icon="assets/logo.png" if False else ":shield:", layout="wide")
load_css()

# ── Helpers ───────────────────────────────────────────────────────────────────

def encode_data(image, data):
    data += "$"
    data_bin = ''.join(format(ord(c), '08b') for c in data)
    pixels = list(image.getdata())
    out = []
    for i, px in enumerate(pixels):
        out.append(((px[0] & 254) | int(data_bin[i]), px[1], px[2]) if i < len(data_bin) else px)
    return out

def decode_data(image):
    bits = "".join(bin(p[0])[-1] for p in image.getdata())
    msg = ""
    for i in range(0, len(bits), 8):
        ch = chr(int(bits[i:i+8], 2))
        msg += ch
        if ch == "$":
            break
    return msg[:-1]

def generate_otp():
    return str(random.randint(100000, 999999))

def otp_crypt(text, otp):
    return ''.join(chr(ord(c) ^ int(otp[i % len(otp)])) for i, c in enumerate(text))

def toggle_widget(label, desc, key, help_text=""):
    """Render a styled toggle row with visible label, description, and checkbox."""
    st.markdown(
        f'<div style="background:#f9fafb;border:1.5px solid #e5e7eb;border-radius:10px;padding:1rem 1.25rem;margin-bottom:0.75rem;">'
        f'<div style="font-size:0.92rem;font-weight:700;color:#111;margin-bottom:0.3rem;">{label}</div>'
        f'<div style="font-size:0.8rem;color:#9ca3af;">{desc}</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    return st.checkbox("Enable", key=key, help=help_text)

# ── Navigation ────────────────────────────────────────────────────────────────

st.markdown('''
<div class="navbar">
  <div class="nav-brand">
    <div class="nav-logo">S</div>
    <span class="nav-title">ImageShield</span>
  </div>
  <div class="nav-links">
    <a class="nav-link active" href="#">Tool</a>
    <a class="nav-link" href="#" onclick="alert('Documentation coming soon.')">Documentation</a>
    <a class="nav-btn" href="https://github.com/madhavchaturvedi005/image_steganography_project" target="_blank">View Source</a>
  </div>
</div>
''', unsafe_allow_html=True)

# ── Hero (full width) ────────────────────────────────────────────────────────

st.markdown('''
<div class="hero">
  <div class="hero-tag">LSB Steganography + Quantum Encryption</div>
  <div class="hero-title">Hide secrets in plain sight</div>
  <div class="hero-desc">
    Embed messages invisibly into images using Least Significant Bit encoding.
    Layer on quantum-simulated BB84 key encryption or OTP protection for added security.
  </div>
  <div class="chips">
    <span class="chip">Zero visible change</span>
    <span class="chip">BB84 Quantum Key</span>
    <span class="chip">PNG / JPG support</span>
  </div>
</div>
''', unsafe_allow_html=True)

# ── Content wrapper (with side margins) ───────────────────────────────────────

st.markdown('<div class="content-wrap">', unsafe_allow_html=True)

# ── Tab state ─────────────────────────────────────────────────────────────────

if 'tab' not in st.session_state:
    st.session_state.tab = 0

st.markdown('<div class="tab-bar">', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    if st.button("Encode — Hide Message", key="tab_enc", use_container_width=True):
        st.session_state.tab = 0
with c2:
    if st.button("Decode — Reveal Message", key="tab_dec", use_container_width=True):
        st.session_state.tab = 1
st.markdown('</div>', unsafe_allow_html=True)

# ── Encode ────────────────────────────────────────────────────────────────────

if st.session_state.tab == 0:
    st.markdown('''
    <div class="card">
      <div class="card-head">
        <div class="card-icon">E</div>
        <div>
          <div class="card-head-title">Encode Secret Message</div>
          <div class="card-head-desc">Your message will be invisibly embedded into the image pixels.</div>
        </div>
      </div>
      <div class="card-body">
    ''', unsafe_allow_html=True)

    message    = st.text_area("Message", placeholder="Type your secret message...", key="enc_msg", height=110)
    image_file = st.file_uploader("Cover Image", type=["png", "jpg", "jpeg"], key="enc_img")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;font-weight:700;color:#9ca3af;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.75rem;">Security Options</div>', unsafe_allow_html=True)

    otp_mode = toggle_widget("OTP Protection", "Generate a 6-digit code required to decode the message.", "enc_otp")
    q_mode   = toggle_widget("Quantum Mode (BB84)", "Encrypt using a simulated BB84 quantum key distribution.", "enc_q")

    enc_btn = st.button("Encode and Hide Message", key="enc_btn", use_container_width=True, disabled=not (message and image_file))

    st.markdown('</div></div>', unsafe_allow_html=True)

    if enc_btn and image_file and message:
        try:
            payload = message

            if otp_mode:
                otp = generate_otp()
                payload = otp_crypt(payload, otp)
                st.success(f"OTP generated: **{otp}** — save this to decode the message.")

            if q_mode:
                with st.spinner("Generating quantum key via BB84 simulation..."):
                    key_bits = generate_bb84_key(len(payload) * 8)
                    payload  = xor_encrypt(payload, key_bits)
                st.info("Quantum key generated — save this to decode:")
                st.code(key_bits_to_str(key_bits), language=None)

            img = Image.open(image_file).convert("RGB")
            out = img.copy()
            out.putdata(encode_data(img, payload))
            buf = BytesIO()
            out.save(buf, format="PNG")
            b64 = base64.b64encode(buf.getvalue()).decode()

            st.image(out, caption="Encoded image — message hidden inside", use_column_width=True)
            st.markdown(
                f'<div style="text-align:center;margin-top:1rem;">'
                f'<a class="dl-btn" href="data:file/png;base64,{b64}" download="encoded.png">Download Encoded Image</a>'
                f'</div>',
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Encoding failed: {e}")
    else:
        st.markdown('''
        <div class="preview-box">
          <div class="preview-title">Encoded Image Preview</div>
          <div class="preview-desc">Result will appear here after encoding</div>
        </div>
        ''', unsafe_allow_html=True)

# ── Decode ────────────────────────────────────────────────────────────────────

if st.session_state.tab == 1:
    st.markdown('''
    <div class="card">
      <div class="card-head">
        <div class="card-icon">D</div>
        <div>
          <div class="card-head-title">Decode Hidden Message</div>
          <div class="card-head-desc">Upload an encoded image to extract the hidden message.</div>
        </div>
      </div>
      <div class="card-body">
    ''', unsafe_allow_html=True)

    dec_file = st.file_uploader("Encoded Image", type=["png", "jpg", "jpeg"], key="dec_img")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.8rem;font-weight:700;color:#9ca3af;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:0.75rem;">Security Options</div>', unsafe_allow_html=True)

    otp_dec   = toggle_widget("OTP Protected", "Enable if the message was encoded with OTP protection.", "dec_otp")
    otp_input = st.text_input("6-digit OTP", key="otp_in", placeholder="e.g. 482910", max_chars=6) if otp_dec else ""

    q_dec = toggle_widget("Quantum Mode (BB84)", "Enable if the message was encoded with Quantum Mode.", "dec_q")
    q_key = st.text_input("Quantum Key", key="dec_qkey", placeholder="Paste the key from encoding...") if q_dec else ""

    dec_btn = st.button("Decode and Reveal Message", key="dec_btn", use_container_width=True, disabled=not dec_file)

    st.markdown('</div></div>', unsafe_allow_html=True)

    if dec_btn and dec_file:
        try:
            img = Image.open(dec_file).convert("RGB")
            msg = decode_data(img)

            if q_dec and q_key:
                msg = xor_decrypt(msg, str_to_key_bits(q_key))
            if otp_dec:
                if not otp_input or len(otp_input) != 6 or not otp_input.isdigit():
                    st.error("Please enter a valid 6-digit OTP.")
                    st.stop()
                msg = otp_crypt(msg, otp_input)

            if msg:
                st.markdown(
                    f'<div class="decoded-label">Hidden Message</div>'
                    f'<div class="decoded-box">{msg}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.warning("No hidden message found in this image.")
        except Exception as e:
            st.error(f"Decoding failed: {e}")
    else:
        st.markdown('''
        <div class="preview-box">
          <div class="preview-title">Decoded Message Preview</div>
          <div class="preview-desc">The hidden message will appear here after decoding</div>
        </div>
        ''', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────

st.markdown('''
<div class="app-footer">
  All processing happens locally — no data is sent to any server.<br>
  ImageShield &copy; 2024 &mdash; Educational use only.
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # close page-wrap
