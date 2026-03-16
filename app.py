import streamlit as st
import pandas as pd
from astral import LocationInfo
from astral.sun import sun
import datetime
import pytz

# 1. SIVUN ASETUKSET
st.set_page_config(
    page_title="Aurora - Kultainen hetki", 
    page_icon="🌅", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. TYYLITIEDOSTO (Kaikki palkit ja headerit poistettu)
st.markdown("""
<style>
    /* Piilotetaan kaikki Streamlitin omat käyttöliittymäelementit */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    .stAppDeployButton {display:none !important;}
    [data-testid="stHeader"] {display: none !important;}
    
    /* Siirretään sisältöä ylemmäs, kun palkki on poistettu */
    .block-container {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }

    /* Taustaväri: Pehmeä pastelliliukuväri kuvasi mukaan */
    .stApp {
        background: linear-gradient(180deg, #ffafbd 0%, #ffc3a0 50%, #eeffad 100%);
        font-family: 'Segoe UI', sans-serif;
    }

    /* Lasimaiset kortit */
    .glass-card {
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(5px);
        border-radius: 30px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        text-align: center;
    }

    h1 {
        font-size: 4rem !important;
        font-weight: 700;
        color: #3e4a61;
        text-align: center;
        margin-top: 0px;
        padding-top: 20px;
    }

    .sub-title {
        color: #3e4a61;
        text-align: center;
        font-size: 1.3rem;
        margin-bottom: 30px;
    }

    .time-label { font-size: 1rem; color: #4a5568; }
    .time-value { font-size: 2.2rem; font-weight: 600; color: #2d3748; }
    .countdown { font-size: 2.5rem; font-weight: 800; color: #f56565; }

    .ad-slot {
        background: rgba(255, 255, 255, 0.2);
        border: 2px dashed rgba(255, 255, 255, 0.5);
        border-radius: 20px;
        padding: 15px;
        color: #ffffff;
        text-align: center;
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

# 4. SIVUPALKKI
st.sidebar.title("Asetukset")
selected_city = st.sidebar.selectbox("Valitse sijainti", list(CITIES.keys()))

# 5. LASKELMAT
loc = LocationInfo(selected_city, "Finland", "Europe/Helsinki", CITIES[selected_city]["lat"], CITIES[selected_city]["lon"])
s = sun(loc.observer, date=datetime.date.today(), tzinfo=pytz.timezone("Europe/Helsinki"))
golden_hour_start = s['sunset'] - datetime.timedelta(minutes=60)
now = datetime.datetime.now(pytz.timezone("Europe/Helsinki"))

# 6. PÄÄSIVUN SISÄLTÖ
st.markdown("<h1>AURORA</h1>", unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">Auringonlasku ja auringonnousu: {selected_city}</p>', unsafe_allow_html=True)

st.markdown('<div class="ad-slot">Tähän paikkaan voit varata mainoksen</div>', unsafe_allow_html=True)

# Kultainen hetki kortti
st.markdown(f'<div class="glass-card"><p class="time-label">✨ Kultainen hetki alkaa kohteessa {selected_city}</p>', unsafe_allow_html=True)
if now < golden_hour_start:
    diff = golden_hour_start - now
    hours, remainder = divmod(diff.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    st.markdown(f'<p class="countdown">{hours}h {minutes}min päästä</p>', unsafe_allow_html=True)
else:
    st.markdown('<p class="countdown" style="color: #4a5568;">Nauti illasta</p>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Aikakortit
st.markdown(f"""
<div class="glass-card">
    <p class="time-label">🌅 Nousuaika</p>
    <p class="time-value">{s['sunrise'].strftime('%H:%M')}</p>
</div>
<div class="glass-card">
    <p class="time-label">✨ Kultainen hetki</p>
    <p class="time-value">{golden_hour_start.strftime('%H:%M')}</p>
</div>
<div class="glass-card">
    <p class="time-label">🌇 Laskuaika</p>
    <p class="time-value">{s['sunset'].strftime('%H:%M')}</p>
</div>
""", unsafe_allow_html=True)

# 7. TAULUKKO
st.write(f"### 🗓️ Ennuste: {selected_city}")
dates, sunrises, sunsets = [], [], []
today = datetime.date.today()
for i in range(14):
    d = today + datetime.timedelta(days=i)
    s_day = sun(loc.observer, date=d, tzinfo=pytz.timezone("Europe/Helsinki"))
    dates.append(d.strftime("%d.%m."))
    sunrises.append(s_day['sunrise'].strftime("%H:%M"))
    sunsets.append(s_day['sunset'].strftime("%H:%M"))

df = pd.DataFrame({"Päivä": dates, "Nousu": sunrises, "Lasku": sunsets})
st.table(df)

# 8. YHTEYSTIETO
st.write("---")
contact_html = f"""
    <a href="mailto:aino.forss@gmail.com" style="text-decoration: none;">
        <div style="background-color: #2c3e50; color: white; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold;">
            Ota yhteyttä: Aino Forss
        </div>
    </a>
"""
st.markdown(contact_html, unsafe_allow_html=True)
