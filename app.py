import streamlit as st
import pandas as pd
from astral import LocationInfo
from astral.sun import sun
import datetime
import pytz

# 1. SIVUN ASETUKSET
st.set_page_config(page_title="Aurora - Kultainen hetki", page_icon="🌅", layout="centered")

# 2. TYYLITIEDOSTO (UI-siivous ja lasiefekti)
st.markdown("""
<style>
    /* Piilotetaan yläpalkki, valikko ja jalusta */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    /* Taustaväri ja fontit */
    .stApp {
        background: linear-gradient(135deg, #fceabb 0%, #f8b500 50%, #fceabb 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Lasimainen kortti-efekti */
    .glass-card {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 25px;
        margin-bottom: 20px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
    }

    .main-title {
        font-size: 3rem !important;
        font-weight: 800;
        color: #2c3e50;
        margin-bottom: 0px;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .sub-title {
        color: #34495e;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }

    .time-label { font-size: 0.9rem; color: #555; margin-bottom: 5px; }
    .time-value { font-size: 1.8rem; font-weight: bold; color: #2c3e50; }
    .countdown { font-size: 2.2rem; font-weight: 900; color: #e74c3c; margin-top: 10px; }
    
    /* Mainospaikka-tyyli */
    .ad-slot {
        background: rgba(255, 255, 255, 0.1);
        border: 1px dashed rgba(255, 255, 255, 0.5);
        border-radius: 10px;
        padding: 10px;
        font-size: 0.8rem;
        color: rgba(0,0,0,0.4);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 3. KAUPUNKIEN TIEDOT
CITIES = {
    "Helsinki": {"lat": 60.1695, "lon": 24.9354},
    "Tampere": {"lat": 61.4978, "lon": 23.7610},
    "Turku": {"lat": 60.4518, "lon": 22.2666},
    "Oulu": {"lat": 65.0121, "lon": 25.4651},
    "Rovaniemi": {"lat": 66.5039, "lon": 25.7282}
}

# 4. SOVELLUKSEN SISÄLTÖ
st.markdown('<p class="main-title" style="text-align:center;">AURORA</p>', unsafe_allow_html=True)

# Sijainnin valinta suoraan pääsivulla (toimii paremmin kännykällä)
selected_city = st.selectbox("📍 Valitse sijainti", list(CITIES.keys()))

st.markdown(f'<p class="sub-title" style="text-align:center;">Auringonlasku ja auringonnousu: {selected_city}</p>', unsafe_allow_html=True)

# Mainospaikka 1
st.markdown('<div class="ad-slot" style="text-align:center;">Tähän paikkaan voit varata mainoksen</div>', unsafe_allow_html=True)

# 5. AURINKOLASKELMAT
loc = LocationInfo(selected_city, "Finland", "Europe/Helsinki", CITIES[selected_city]["lat"], CITIES[selected_city]["lon"])
s = sun(loc.observer, date=datetime.date.today(), tzinfo=pytz.timezone("Europe/Helsinki"))

# Kultainen hetki (noin tunti ennen auringonlaskua)
golden_hour_start = s['sunset'] - datetime.timedelta(minutes=60)
now = datetime.datetime.now(pytz.timezone("Europe/Helsinki"))

# 6. NÄKYMÄN RAKENTAMINEN
# Laskenta-kortti
st.markdown(f"""
<div class="glass-card">
    <p class="time-label">✨ Kultainen hetki alkaa kohteessa {selected_city}</p>
""", unsafe_allow_html=True)

if now < golden_hour_start:
    diff = golden_hour_start - now
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    st.markdown(f'<p class="countdown">{hours}h {minutes}min päästä</p>', unsafe_allow_html=True)
elif now < s['sunset']:
    st.markdown('<p class="countdown" style="color: #f39c12;">Kultainen hetki on NYT!</p>', unsafe_allow_html=True)
else:
    st.markdown('<p class="countdown" style="color: #7f8c8d;">Tältä päivältä ohi</p>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Aikataulu-kortit rinnakkain
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""<div class="glass-card">
        <p class="time-label">🌅 Nousuaika</p>
        <p class="time-value">{s['sunrise'].strftime('%H:%M')}</p>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class="glass-card">
        <p class="time-label">✨ Kultainen hetki</p>
        <p class="time-value">{golden_hour_start.strftime('%H:%M')}</p>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class="glass-card">
        <p class="time-label">🌇 Laskuaika</p>
        <p class="time-value">{s['sunset'].strftime('%H:%M')}</p>
    </div>""", unsafe_allow_html=True)

# 7. LOPPUOSA JA MAINOKSET
st.markdown("---")
st.write("### 🧘 Päivän hyvinvointivinkki")
st.info("Kultainen hetki ei ole vain valokuvausta varten. Se on täydellinen hetki pysähtyä, hengittää syvään ja päästää irti päivän stressistä. Kokeile 5 minuutin tietoista läsnäoloa ulkona juuri nyt.")

# Mainospaikka 2 ja Yhteydenotto
st.markdown('<div class="ad-slot" style="text-align:center; margin-top:50px;">Mainospaikka vapaana – tavoita ulkoilun ja hyvinvoinnin ystävät</div>', unsafe_allow_html=True)

st.write("---")
st.write("Haluatko varata mainospaikan tai antaa palautetta?")
contact_html = """
    <a href="mailto:aino.forss@gmail.com" style="text-decoration: none;">
        <div style="background-color: #2c3e50; color: white; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold;">
            Ota yhteyttä: Aino Forss
        </div>
    </a>
"""
st.markdown(contact_html, unsafe_allow_html=True)
