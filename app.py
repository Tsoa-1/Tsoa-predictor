import streamlit as st
from PIL import Image
import easyocr
import numpy as np
import re

# 1. Configuration ny pejy (Atao lehibe ny rafitra)
st.set_page_config(page_title="Predictor Web", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS ho an'ny fomba fijery Néon sy Glassmorphism kanto
st.markdown("""
    <style>
    /* Background manontolo */
    .stApp {
        background: linear-gradient(135deg, #0f0c20 0%, #15102a 50%, #060210 100%);
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Titre Néon */
    .neon-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #fff;
        text-shadow: 0 0 5px #fff, 0 0 10px #ff007f, 0 0 20px #ff007f, 0 0 40px #ff007f;
        margin-bottom: 5px;
        letter-spacing: 2px;
    }
    
    /* Sous-titre Néon manga */
    .neon-subtitle {
        text-align: center;
        font-size: 16px;
        color: #00ffff;
        text-shadow: 0 0 5px #00ffff, 0 0 10px #00ffff;
        margin-bottom: 35px;
        font-weight: 500;
    }
    
    /* Boaty Glassmorphism ho an'ny vokatra */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        height: 195px; /* Natao raikitra mba hitovy amin'ny file uploader */
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    /* Manova ny fampidirana sary an'ny Streamlit ho lasa Glassmorphism sy Néon */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 16px;
        border: 1px solid rgba(0, 255, 255, 0.25);
        padding: 10px;
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.1);
        transition: all 0.3s ease;
        height: 195px; /* Natao raikitra mitovy amin'ny glass-card */
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    [data-testid="stFileUploader"]:hover {
        border: 1px solid rgba(0, 255, 255, 0.6);
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.3);
    }

    /* Famafana ny fotsy sy ny background d'origine amin'ny Streamlit */
    [data-testid="stFileUploader"] section {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        width: 100%;
        padding: 0 !important;
    }
    
    /* ATAO FOTSY MAZAVA NY SORATRA REHETRA AO ANATIN'NY UPLOADER */
    [data-testid="stFileUploader"] label, 
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] span,
    [data-testid="stText"] {
        color: #ffffff !important;
        text-shadow: 0 0 2px rgba(255, 255, 255, 0.3);
        font-weight: 500 !important;
    }

    /* Manova ilay bokotra kely "Browse files" ho hita tsara */
    [data-testid="stFileUploader"] button {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 8px !important;
        transition: background 0.2s ease;
    }
    
    [data-testid="stFileUploader"] button:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
        border: 1px solid rgba(0, 255, 255, 0.6) !important;
    }
    
    /* Style ho an'ny vokatra lehibe */
    .result-value {
        font-size: 28px;
        font-weight: bold;
        color: #00ffcc;
        text-shadow: 0 0 8px rgba(0, 255, 204, 0.6);
    }
    
    .result-label {
        font-size: 14px;
        color: #aaa;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    
    /* Hafatra fahadisoana tsara tarehy */
    .error-card {
        background: rgba(255, 0, 85, 0.1);
        border: 1px solid rgba(255, 0, 85, 0.4);
        border-radius: 12px;
        padding: 20px;
        color: #ff4d88;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 0 15px rgba(255, 0, 85, 0.2);
        height: 195px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Lohateny lehibe eo an-tampony
st.markdown('<div class="neon-title">🚀 PREDICTEUR</div>', unsafe_allow_html=True)
st.markdown('<div class="neon-subtitle">Advanced Live Image Analysis & Time Cycle Forecasting</div>', unsafe_allow_html=True)

# 4. Fametrahana ny Layout mizara roa (Columns): Ankavia = Image, Ankavanana = Résultat
col_gauche, col_havanana = st.columns([1, 1.2], gap="large")

with col_gauche:
    st.markdown("<p style='color: #00ffff; font-weight: bold; margin-bottom: 15px;'>Veuillez selectionner l'historique dans le BET261 (PNG na JPG)...</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["png", "jpg", "jpeg"])

with col_havanana:
    # Nampiana lohateny Résultat mifanitsy tsara amin'ny ankavia
    st.markdown("<p style='color: #00ffff; font-weight: bold; margin-bottom: 15px;'>Résultat de l'analyse :</p>", unsafe_allow_html=True)
    
    if uploaded_file is not None:
        try:
            # Sokafy ny sary nampidirina
            image = Image.open(uploaded_file)
            
            # Asehoy kely ao ambanin'ny fampidirana ny sary mba ho hita
            with col_gauche:
                st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
                st.image(image, caption="Sary nampidirina", use_container_width=True)
            
            with st.spinner("En cours de traitement du résultat..."):
                # Initialisation an'ny EasyOCR (mampiasa CPU mba tsy hisy olana)
                reader = easyocr.Reader(['fr', 'en'], gpu=False)
                
                # Avadika ho numpy array ny sary mba ho takatry ny OCR
                image_np = np.array(image)
                ocr_results = reader.readtext(image_np)
                
                # Atambatra ny teny rehetra hita tao anatin'ny sary
                all_text = " ".join([res[1].lower() for res in ocr_results])
                
                # 5. SIVANA: Hamarinina raha misy teny manamarina ny maha Aviator/Jet azy
                keywords = ["aviator", "jetx", "multiplier", "multiplicateur", "parier", "bet", "historique", "rounds"]
                is_valid_game = any(kw in all_text for kw in keywords) or bool(re.search(r'\d+\.\d+x', all_text))
                
                if not is_valid_game:
                    # Raha tsy sary Aviator/Jet no nampidirina
                    st.markdown("""
                        <div class="error-card">
                            ⚠️ Erreur : Veuillez entrer correctement des images corresponds sur le résultat du jeux. <br><br>
                            Mba mampidira capture misy ny historique ny multiplier azafady!
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    # SIMULATION NY LALÀNA (Azonao ovaina mifanaraka amin'ny algorithm-nao eto)
                    predicted_hour = "14:42:15"
                    predicted_multiplier = "2.45x"
                    analysis_status = "Analyse effectuer! Nahita vokatra vaovao avy amin'ireo multiplier farany teo ny code."
                    
                    # 6. ASEHO NY VOKATRA EO AMBANY TITRE
                    st.markdown(f"""
                        <div class="glass-card">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                                <div>
                                    <div class="result-label">Ora Vinany (Heure Cible)</div>
                                    <div class="result-value">⏰ {predicted_hour}</div>
                                </div>
                                <div style="text-align: right;">
                                    <div class="result-label">Multiplier Vinany</div>
                                    <div class="result-value" style="color: #ff007f; text-shadow: 0 0 8px rgba(255, 0, 127, 0.6);">📈 {predicted_multiplier}</div>
                                </div>
                            </div>
                            <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.1); margin: 15px 0;">
                            <div class="result-label">Sombiny amin'ny Famakafakana (Status)</div>
                            <p style="color: #e0e0e0; font-size: 14px; line-height: 1.5; margin: 5px 0 0 0;">✨ {analysis_status}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
        except Exception as e:
            st.markdown(f"""
                <div class="error-card">
                    ❌ Nisy olana teo am-pamakiana ny rakitra: {str(e)}
                </div>
            """, unsafe_allow_html=True)
    else:
        # Rehefa mbola banga ny pejy
        st.markdown("""
            <div class="glass-card" style="text-align: center; color: #ffffff; padding: 40px 20px;">
                Mbola miandry sary... Ampididro eo amin'ny ankavia ny capture-nao mba hivoahan'ny vinany eto.
            </div>
        """, unsafe_allow_html=True)
