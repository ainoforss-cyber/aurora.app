import streamlit as st
import pandas as pd
from astral import LocationInfo
from astral.sun import sun
import datetime
import pytz

# 1. SIVUN ASETUKSET
st.set_page_config(page_title="Aurora - Kultainen hetki", page_icon="🌅", layout="centered")

# 2. TYYLITIEDOSTO (Alkuperäinen look + Siivous)
st.markdown("""
<style>
    /* Piilotetaan yläpalkki, valikko ja jalusta */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}

    .stApp {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        text-align: center;
    }

    h1 { color: #2c3e50; font-weight: 800; text-transform: uppercase; letter-spacing: 3px; }
    .time-label { font-size: 0.8rem; color: #555; text-transform: uppercase; }
    .time-value { font-size: 1.5rem; font-weight: bold; color: #2c3e50; }
    .countdown { font-size: 2rem; font-weight: bold; color: #ff4b2b; }
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

# 4. SIVUPALKKI (Takaisin paikallaan)
st.sidebar.title("Asetukset")
selected_city = st.sidebar.selectbox("Valitse sijainti", list(CITIES.keys()))

# 5. LASKELMAT (Tämä päivä)
loc = LocationInfo(selected_city, "Finland", "Europe/Helsinki", CITIES[selected_city]["lat"], CITIES[selected_city]["lon"])
s = sun(loc.observer, date=datetime.date.today(), tzinfo=pytz.timezone("Europe/Helsinki"))
golden_hour_start = s['sunset'] - datetime.timedelta(minutes=60)
now = datetime.datetime.now(pytz.timezone("Europe/Helsinki"))

# 6. PÄÄSIVUN SISÄLTÖ
st.markdown(f'<h1 style="text-align:center;">AURORA</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align:center; color:#555;">Auringonlasku ja -nousu: {selected_city}</p>', unsafe_allow_html=True)

# Kultainen hetki kortti
st.markdown(f'<div class="glass-card"><p class="time-label">✨ Kultainen hetki alkaa</p>', unsafe_allow_html=True)
if now < golden_hour_start:
    diff = golden_hour_start - now
    st.markdown(f'<p class="countdown">{diff.seconds//3600}h {(diff.seconds//60)%60}min päästä</p>', unsafe_allow_html=True)
else:
    st.markdown('<p class="countdown">Nauti hetkestä tai odota huomista</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Sarakkeet
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="glass-card"><p class="time-label">🌅 Nousu</p><p class="time-value">{s["sunrise"].strftime("%H:%M")}</p></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="glass-card"><p class="time-label">✨ Kultainen</p><p class="time-value">{golden_hour_start.strftime("%H:%M")}</p></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="glass-card"><p class="time-label">🌇 Lasku</p><p class="time-value">{s["sunset"].strftime("%H:%M")}</p></div>', unsafe_allow_html=True)

# 7. KUUKAUSITAULUKKO (PALAUTETTU!)
st.write(f"### 🗓️ Loppukuun ennuste: {selected_city}")
dates = []
sunrises = []
sunsets = []

today = datetime.date.today()
for i in range(14):
    d = today + datetime.timedelta(days=i)
    s_day = sun(loc.observer, date=d, tzinfo=pytz.timezone("Europe/Helsinki"))
    dates.append(d.strftime("%d.%m."))
    sunrises.append(s_day['sunrise'].strftime("%H:%M"))
    sunsets.append(s_day['sunset'].strftime("%H:%M"))

df = pd.DataFrame({
    "Päivä": dates,
    "Nousuaika": sunrises,
    "Laskuaika": sunsets
})
st.table(df)

# 8. YHTEYSTIEDOT
st.write("---")
st.info("💡 Kultainen hetki on paras aika valokuvaukselle ja rauhoittumiselle.")
st.markdown(f'<a href="mailto:aino.forss@gmail.com" style="text-decoration:none;"><div style="background:#2c3e50; color:white; padding:10px; border-radius:10px; text-align:center;">Ota yhteyttä: Aino Forss</div></a>', unsafe_allow_html=True)
