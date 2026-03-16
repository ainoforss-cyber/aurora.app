import streamlit as st
import pandas as pd
from astral.sun import sun, golden_hour
from astral import LocationInfo, SunDirection
import datetime
import pytz

# 1. SEO & META-TIEDOT
st.set_page_config(
    page_title="Auringonlasku ja auringonnousu tänään – Aurora",
    page_icon="🌅",
    layout="wide",
    initial_sidebar_state="collapsed", # Piilotetaan sivupalkki oletuksena
    menu_items={
        'About': "Aurora - Tarkista auringonnousu, auringonlasku ja kultainen hetki kaikissa Suomen kaupungeissa."
    }
)

# 2. ULKOASU: LUXURY GLASSMORPHISM (Säilytetty täysin samana)
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #ffafbd 0%, #ffc3a0 50%, #c9ffbf 100%);
        background-attachment: fixed;
    }
    
    h1 { 
        color: white !important; 
        font-family: 'Inter', sans-serif;
        font-weight: 800 !important;
        text-align: center;
        text-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        font-size: clamp(2.5rem, 8vw, 5rem) !important;
        margin-bottom: 20px;
    }

    /* Poistetaan sivupalkin elementit käytöstä */
    [data-testid="stSidebar"] {
        display: none;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(15px);
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.4);
        padding: 20px;
        margin-bottom: 15px;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
    }

    .countdown-text {
        font-size: clamp(1.5rem, 5vw, 2.2rem);
        font-weight: 800;
        color: #ff6b6b;
    }

    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.2) !important;
        backdrop-filter: blur(10px);
        border-radius: 20px !important;
        padding: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }

    p, span, label { color: #2c3e50 !important; font-weight: 600; }
    
    .ad-slot {
        background: rgba(255, 255, 255, 0.1);
        border: 1px dashed rgba(255, 255, 255, 0.5);
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        color: white;
        font-size: 0.8rem;
        margin: 10px 0;
    }

    .contact-btn {
        background: rgba(255, 255, 255, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.5);
        padding: 15px 30px;
        border-radius: 50px;
        text-align: center;
        color: white !important;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
        transition: 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .contact-btn:hover {
        background: rgba(255, 255, 255, 0.4);
        transform: translateY(-2px);
    }
    
    /* Tyyli uusia valikoita varten pääsivulla */
    .menu-container {
        background: rgba(255, 255, 255, 0.15);
        padding: 20px;
        border-radius: 25px;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

# 3. DATA
kaupungit = {
    "Helsinki": {"lat": 60.17, "lon": 24.94}, "Turku": {"lat": 60.45, "lon": 22.26},
    "Tampere": {"lat": 61.49, "lon": 23.76}, "Oulu": {"lat": 65.01, "lon": 25.46},
    "Rovaniemi": {"lat": 66.50, "lon": 25.72}, "Inari": {"lat": 68.90, "lon": 27.02}
}

st.title("AURORA")

# 4. VALIKKO PÄÄSIVULLA (Korvaa sivupalkin)
st.markdown("<div class='menu-container'>", unsafe_allow_html=True)
col_a, col_b = st.columns(2)

with col_a:
    valittu_nimi = st.selectbox("📍 Valitse paikkakunta", list(kaupungit.keys()))

with col_b:
    kuukaudet = ["Tammikuu", "Helmikuu", "Maaliskuu", "Huhtikuu", "Toukokuu", "Kesäkuu", 
                 "Heinäkuu", "Elokuu", "Syyskuu", "Lokakuu", "Marraskuu", "Joulukuu"]
    valittu_kk = st.selectbox("📅 Valitse kuukausi", options=kuukaudet, index=2) # Oletus: Maaliskuu
    kk_nro = kuukaudet.index(valittu_kk) + 1
st.markdown("</div>", unsafe_allow_html=True)

# 5. LASKENTA (Säilytetty samana)
coords = kaupungit[valittu_nimi]
loc = LocationInfo(valittu_nimi, "Finland", "Europe/Helsinki", coords["lat"], coords["lon"])
tz = pytz.timezone(loc.timezone)
nyt_tz = datetime.datetime.now(tz)

st.markdown(f"<h2 style='text-align: center; color: white; font-size: 1.2rem; opacity: 0.9;'>Auringonlasku ja auringonnousu: {valittu_nimi}</h2>", unsafe_allow_html=True)

st.markdown("<div class='ad-slot'>Tähän paikkaan voit varata mainoksen</div>", unsafe_allow_html=True)

# Countdown (Säilytetty samana)
try:
    gh_tanaan, _ = golden_hour(loc.observer, date=nyt_tz.date(), direction=SunDirection.SETTING, tzinfo=tz)
    aika_ero = gh_tanaan - nyt_tz
    sekunnit = aika_ero.total_seconds()
    if sekunnit > 0:
        t_cd, m_cd = int(sekunnit // 3600), int((sekunnit % 3600) // 60)
        st.markdown(f"<div class='glass-card'><p style='margin:0; opacity: 0.8;'>✨ Kultainen hetki alkaa kohteessa {valittu_nimi}</p><div class='countdown-text'>{t_cd}h {m_cd}min päästä</div></div>", unsafe_allow_html=True)
except: pass

# Metriikat (Säilytetty samana)
s_tanaan = sun(loc.observer, date=nyt_tz.date(), tzinfo=tz)
m1, m2, m3 = st.columns(3)
with m1: st.metric("🌅 Nousuaika", s_tanaan['sunrise'].strftime('%H:%M'))
with m2: st.metric("✨ Kultainen hetki", gh_tanaan.strftime('%H:%M'))
with m3: st.metric("🌆 Laskuaika", s_tanaan['sunset'].strftime('%H:%M'))

# Hyvinvointivinkki (Säilytetty samana)
st.markdown(f"""
    <div class='glass-card' style='background: rgba(201, 255, 191, 0.3); border-left: 10px solid #c9ffbf;'>
        <p style='margin:0;'><b>🌿 Hyvinvointivinkki:</b> Luonnonvalo parantaa mielialaa ja auttaa jaksamaan. 
        Paras aika ulkoilulle kohteessa {valittu_nimi} on tänään klo {s_tanaan['sunrise'].hour + 1} ja {s_tanaan['sunset'].hour - 1} välillä.</p>
    </div>
""", unsafe_allow_html=True)

# 6. KUUKAUSITAULUKKO (Säilytetty samana)
st.divider()
st.markdown(f"<h3 style='text-align: center; color: white;'>Auringon lasku- ja nousuajat: {valittu_nimi} — {valittu_kk}</h3>", unsafe_allow_html=True)

paivat = []
for d in range(1, 32):
    try:
        pvm = datetime.date(2026, kk_nro, d)
        s = sun(loc.observer, date=pvm, tzinfo=tz)
        gh_s, _ = golden_hour(loc.observer, date=pvm, direction=SunDirection.SETTING, tzinfo=tz)
        paivat.append({"Päivä": d, "🌅 Nousu": s['sunrise'].strftime('%H:%M'), "🌇 Lasku": s['sunset'].strftime('%H:%M'), "☀️ Kultainen": gh_s.strftime('%H:%M')})
    except: continue

st.dataframe(pd.DataFrame(paivat).style.set_properties(**{'background-color': 'rgba(255, 255, 255, 0.05)', 'color': '#2c3e50', 'border-color': 'rgba(255, 255, 255, 0.1)'}), use_container_width=True, hide_index=True)

# SEO-ALATUNNISTE
st.markdown(f"""
    <div style='padding: 20px; color: white; opacity: 0.8; font-size: 0.9rem;'>
        <b>Aurora-sääpalvelu:</b> Tarkat auringon nousu- ja laskuajat paikkakunnalle {valittu_nimi} ja koko Suomeen. 
        Suunnittele valokuvaus kultaisen hetken mukaan ja seuraa valoisan ajan lisääntymistä.
    </div>
""", unsafe_allow_html=True)

# SÄHKÖPOSTI
st.markdown("""
    <div style='text-align: center; margin-top: 20px;'>
        <a href='mailto:aino.forss@gmail.com?subject=Mainostiedustelu - Aurora App' class='contact-btn'>
            📩 Ota yhteyttä ja varaa mainostilaa
        </a>
    </div>
    <br>
    <p style='text-align: center; opacity: 0.5; font-size: 0.7rem; color: white;'>© 2026 Aurora. Kaikki oikeudet pidätetään.</p>
""", unsafe_allow_html=True)
