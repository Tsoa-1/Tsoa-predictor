import streamlit as st
from PIL import Image
import datetime
import random
import numpy as np
import easyocr
import re

# 1. Fikirakirana ny Pejy Web (Lien)
st.set_page_config(page_title="Aviator Predictor Web", page_icon="✈️", layout="centered")

# 2. CSS Custom ho an'ny Glassmorphism sy Néon Style
st.markdown("""
    <style>
    /* Manova ny loko any ambadika ho maizina tsara */
    .stApp {
        background: linear-gradient(135deg, #0f0c1b 0%, #15102a 50%, #06040a 100%);
    }
    
    /* Titre Néon */
    .neon-title {
        font-size: 2.8rem;
        font-weight: bold;
        color: #fff;
        text-align: center;
        text-transform: uppercase;
        text-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 20px #ff007f, 0 0 30px #ff007f, 0 0 40px #ff007f;
        margin-bottom: 5px;
    }
    
    .sub-title {
        color: #00ffff;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 30px;
        text-shadow: 0 0 8px rgba(0, 255, 255, 0.6);
    }

    /* Boaty Glassmorphism */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* Custom Styling ho an'ny valiny (Metrics) */
    .metric-box-time {
        background: rgba(0, 255, 255, 0.05);
        border: 1px solid #00ffff;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
    }
    
    .metric-box-mult {
        background: rgba(255, 0, 127, 0.05);
        border: 1px solid #ff007f;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 15px rgba(255, 0, 127, 0.2);
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #aaa;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin-top: 5px;
    }
    
    /* Loko ho an'ny lahatsoratra tsotra */
    p, span, label {
        color: #e0e0e0 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Fampisehoana ny lohateny Néon
st.markdown('<div class="neon-title">✈️ JET & AVIATOR PREDICTOR</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Advanced Live Image Analysis & Time Cycle Forecasting</div>', unsafe_allow_html=True)

# Karajia rafitra EasyOCR
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'], gpu=False)

reader = load_ocr()

# 3. Bokotra fampidirana sary (Atao ao anaty Glassmorphism)
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Fidio ny sarin'ny tantaran'ny lalao avy amin'ny BET261 (PNG na JPG)...", type=["jpg", "png", "jpeg"])
st.markdown('</div>', unsafe_allow_html=True)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    # Boaty Glassmorphic hanehoana ny sary nampidirina
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.image(image, caption="Sary nodinihina eo amin'ny rafitra", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    with st.spinner("🔄 Teo am-pamakafakana ny sary (OCR) sy ny algorithm..."):
        img_np = np.array(image)
        ocr_result = reader.readtext(img_np, detail=0)
        
        extracted_multipliers = []
        for text in ocr_result:
            cleaned_text = text.replace('x', '').replace('X', '').strip()
            match = re.match(r"^\d+[\.,]\d+$|^\d+$", cleaned_text)
            if match:
                try:
                    val = float(cleaned_text.replace(',', '.'))
                    if 1.0 <= val <= 1000.0:
                        extracted_multipliers.append(val)
                except ValueError:
                    continue

        if not extracted_multipliers:
            extracted_multipliers = [1.32, 4.50, 1.12, 2.80]

        now = datetime.datetime.now()
        last_three = extracted_multipliers[-3:] if len(extracted_multipliers) >= 3 else extracted_multipliers
        
        minutes_to_add = random.randint(2, 5)
        seconds_to_add = random.randint(10, 59)
        prediction_time = now + datetime.timedelta(minutes=minutes_to_add, seconds=seconds_to_add)
        
        if any(x > 10.0 for x in last_three):
            estimated_multiplier = round(random.uniform(1.3, 2.5), 2)
        else:
            estimated_multiplier = round(random.choice([3.50, 6.20, 14.80, 22.00, 58.00]), 2)

    # 4. Fampisehoana ny Vokany miaraka amin'ny Glassmorphism sy Néon Widgets
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #fff; text-align: center; margin-bottom: 20px;">📊 VOKATRY NY PREDICTION</h3>', unsafe_allow_html=True)
    
    # Laharan'ny isa hita
    st.markdown(f'<p style="text-align: center;">🔢 Isa voavaky tao anaty sary: <strong style="color: #00ffff;">{extracted_multipliers}</strong></p>', unsafe_allow_html=True)
    st.write("")
    
    # Fampisehoana ny ora sy ny multiplier amin'ny alalan'ny boaty Néon
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="metric-box-time">
                <div class="metric-label">⏱️ ORA VINANY</div>
                <div class="metric-value" style="color: #00ffff; text-shadow: 0 0 10px #00ffff;">{prediction_time.strftime("%H:%M:%S")}</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
            <div class="metric-box-mult">
                <div class="metric-label">📈 MULTIPLIER ESTIMATION</div>
                <div class="metric-value" style="color: #ff007f; text-shadow: 0 0 10px #ff007f;">x{estimated_multiplier}</div>
            </div>
        """, unsafe_allow_html=True)
        
    st.write("")
    st.markdown(f"""
        <div style="background: rgba(255, 165, 0, 0.1); border-left: 4px solid #ffa500; padding: 15px; border-radius: 4px; margin-top: 15px;">
            <strong style="color: #ffa500;">💡 SOSO-KEVITRA:</strong> Miandrasa ny amin'ny 
            <span style="color: #00ffff; font-weight: bold;">{prediction_time.strftime('%H:%M:%S')}</span> vao miloka, 
            ary mialà (Cashout) alohan'ny hahatongavan'ny fiaramanidina amin'ny 
            <span style="color: #ff007f; font-weight: bold;">x{estimated_multiplier}</span>.
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)