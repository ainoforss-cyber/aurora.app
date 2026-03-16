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
    initial_sidebar_state="expanded"
)

# 2. TYYLITIEDOSTO (Palautettu alkuperäinen oranssi-keltainen tyyli)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #fceabb 0%, #f8b500 50%, #fceabb 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

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

    h1 {
        font-size: 3.5rem !important;
        font-weight: 800;
        color: #2c3e50;
        text-align: center;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: -20px;
    }

    .sub-title {
        color: #34495e;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }

    .time-label { font-size: 0.9rem; color: #555; margin-bottom: 5px; }
    .time-value { font-size: 1.8rem; font-weight: bold; color: #2c3e50; }
    .countdown { font-size: 2.5rem; font-weight: 900; color: #e74c3c; margin-top: 10px; }
    
    /* Siisteyttä taulukkoon */
    .stTable {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
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

# 4. SIVUPALKKI (Täältä vaihdetaan kaupunki)
st.sidebar.title("Asetukset")
selected_city = st.sidebar.selectbox("📍 Valitse sijainti", list(CITIES.keys()))

# 5. LASKELMAT
loc = LocationInfo(selected_city, "Finland", "Europe/Helsinki", CITIES[selected_city]["lat"], CITIES[selected_city]["lon"])
s = sun(loc.observer, date=datetime.date.today(), tzinfo=pytz.timezone("Europe/Helsinki"))
golden_hour_start = s['sunset'] - datetime.timedelta(minutes=60)
now = datetime.datetime.now(pytz.timezone("Europe/Helsinki"))

# 6. PÄÄSIVUN SISÄLTÖ
st.markdown("<h1>AURORA</h1>", unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">Auringonlasku ja auringonnousu: {selected_city}</p>', unsafe_allow_html=True)

# Kultainen hetki kortti
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
    st.markdown('<p class="countdown" style="color: #7f8c8d;">Nauti illasta</p>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Sarakkeet rinnakkain (Nousu, Kultainen hetki, Lasku)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""<div class="glass-card">
        <p class="time-label">🌅 Nousu</p>
        <p class="time-value">{s['sunrise'].strftime('%H:%M')}</p>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class="glass-card">
        <p class="time-label">✨ Kultainen</p>
        <p class="time-value">{golden_hour_start.strftime('%H:%M')}</p>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class="glass-card">
        <p class="time-label">🌇 Lasku</p>
        <p class="time-value">{s['sunset'].strftime('%H:%M')}</p>
    </div>""", unsafe_allow_html=True)

# 7. KUUKAUSITAULUKKO (Takaisin mukana!)
st.write(f"### 🗓️ Loppukuun ennuste: {selected_city}")
dates, sunrises, sunsets = [], [], []
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

# 8. LOPPUOSA
st.write("---")
st.info("💡 Kultainen hetki (Golden Hour) on täydellinen hetki valokuvaukselle ja mielenrauhalle.")

contact_html = """
    <a href="mailto:aino.forss@gmail.com" style="text-decoration: none;">
        <div style="background-color: #2c3e50; color: white; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold;">
            Ota yhteyttä: Aino Forss
        </div>
    </a>
"""
st.markdown(contact_html, unsafe_allow_html=True)
