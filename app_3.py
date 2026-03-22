import streamlit as st
import pandas as pd
import base64

# --- 1. KONFIGURACE POŘADÍ A POMOCNÉ FUNKCE ---
PORADI_KAROSERII = ["hatchback", "combi", "sedan"]

def serad_karoserie(seznam_z_dat):
    """Seřadí unikátní hodnoty karoserií podle definovaného klíče."""
    vysledek = []
    for k_ref in PORADI_KAROSERII:
        for k_data in seznam_z_dat:
            if str(k_data).lower() == k_ref:
                vysledek.append(k_data)
    ostatni = sorted([k for k in seznam_z_dat if str(k).lower() not in PORADI_KAROSERII])
    return vysledek + ostatni

def get_base64_of_bin_file(bin_file):
    """Načte obrázek pro pozadí."""
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# --- 2. NASTAVENÍ STRÁNKY A STYLING ---
st.set_page_config(page_title="Fabia Katalog 3.0", page_icon="🚗", layout="wide")

img_base64 = get_base64_of_bin_file('2.png')

style = f'''
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;700;900&display=swap');

.stApp {{
    background-image: url("data:image/png;base64,{img_base64}");
    background-size: cover;
    background-attachment: fixed;
    font-family: 'Quicksand', sans-serif !important;
}}

/* ZVĚTŠENÍ NÁZVŮ NAD SELECTBOXY */
[data-testid="stWidgetLabel"] p {{
    font-size: 20px !important;
    font-weight: 700 !important;
    color: white !important;
    text-shadow: 1px 1px 5px rgba(0,0,0,0.5);
}}

/* Odstranění kotev u nadpisů a Streamlit menu */
h1 a, h2 a, h3 a, h4 a, h5 a, h6 a {{ display: none !important; }}
[data-testid="stHeaderActionElements"] {{ display: none !important; }}

[data-testid="stVerticalBlock"] > div {{
    padding: 0px !important;
    margin: 0px !important;
    gap: 0px !important;
}}

.header-container {{
    width: 100%;
    text-align: center;
    margin-top: -20px;
    margin-bottom: 20px;
}}
.main-title {{
    color: #ffffff !important;
    font-size: 60px !important;
    font-weight: 900;
    text-transform: uppercase;
    text-shadow: 0 0 25px rgba(0,0,0,0.9);
}}

[data-testid="stSidebar"] {{
    background-color: rgba(0, 0, 0, 0.7) !important;
    backdrop-filter: blur(15px);
}}
[data-testid="stSidebar"] h2 {{ color: white !important; font-weight: 900 !important; }}
[data-testid="stSidebar"] h3 {{ color: white !important; font-weight: 900 !important; }}
[data-testid="stSidebar"] label p {{ color: white !important; font-weight: 700 !important; }}
[data-testid="stSidebar"] summary p {{ color: #ffffff !important; font-weight: 700 !important; }}
[data-testid="stSidebar"] .st-expanderIcon {{ fill: #ffffff !important; }}

.custom-card {{
    background: rgba(255, 255, 255, 0.9);
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    color: #1e1e1e;
}}
.card-title {{ font-weight: 900; font-size: 22px; color: #000; border-bottom: 2px solid #ddd; padding-bottom: 5px; margin-bottom: 10px; }}

.top-card {{
    background: rgba(0, 0, 0, 0.75);
    text-align: center;
    border: 1px solid rgba(255,255,255,0.2);
    padding: 30px;
}}
.top-card h1, .top-card p, .top-card b {{ color: #ffffff !important; text-shadow: 2px 2px 10px rgba(0,0,0,1) !important; }}

.compare-header-info {{
    background: rgba(0, 0, 0, 0.85) !important;
    border-radius: 15px;
    padding: 15px;
    border: 1px solid rgba(255,255,255,0.2);
    text-align: center;
    color: white;
    min-height: 100px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    margin-bottom: 25px !important; 
}}
.compare-header-info h2 {{ font-weight: 900; margin: 0; font-size: 22px; color: white !important; }}

.compare-row {{ display: flex; align-items: center; justify-content: center; margin-bottom: 12px; gap: 10px; }}
.compare-label {{ flex: 0.7; min-width: 130px; text-align: center; color: white; font-weight: 700; background: rgba(0,0,0,0.6); padding: 8px; border-radius: 10px; font-size: 13px; }}
.compare-value {{ flex: 1.5; padding: 10px; border-radius: 10px; font-weight: 900; text-align: center; color: white; background: rgba(255,255,255,0.1); }}

.better-spec {{ background-color: rgba(40, 167, 69, 0.85) !important; border: 2px solid #28a745; }}
.worse-spec {{ background-color: rgba(220, 53, 69, 0.85) !important; border: 2px solid #dc3545; }}

.winner-card {{
    background-color: #3e9b4f !important;
    color: white !important;
    text-align: center;
    padding: 20px;
    border-radius: 20px;
    font-size: 26px;
    font-weight: 900;
    margin-top: 20px;
    border: none !important;
}}

.legal-text {{ font-size: 11px !important; color: #ffffff !important; text-align: justify; line-height: 1.4; }}
.price-container {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; }}
.price-item {{ background: rgba(0,0,0,0.05); padding: 10px 20px; border-radius: 12px; border: 1px solid rgba(0,0,0,0.1); text-align: center; min-width: 140px; }}

.motor-grid {{ display: flex; justify-content: space-between; gap: 20px; }}
.motor-col {{ flex: 1; }}
.title-widget {{ background: rgba(0, 0, 0, 0.75); padding: 15px 40px; border-radius: 20px; display: inline-block; border: 1px solid rgba(255,255,255,0.2); text-align: center; margin-bottom: 20px; }}
.title-widget h1 {{ color: white !important; text-transform: uppercase; font-weight: 900; margin: 0 !important; font-size: 32px; }}


/* 1. Zruší bílé pozadí a rámeček u celého expanderu */
[data-testid="stSidebar"] [data-testid="stExpander"] {{
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}

/* 2. Zruší pozadí vnitřní části po rozbalení */
[data-testid="stSidebar"] [data-testid="stExpanderDetails"] {{
    background-color: transparent !important;
    border: none !important;
    padding-top: 0px !important;
}}

/* 3. Nadpis "Právní doložka" a šipka budou VŽDY BÍLÉ a čitelné */
[data-testid="stSidebar"] [data-testid="stExpander"] summary p {{
    color: white !important;
    opacity: 1 !important;
}}
[data-testid="stSidebar"] [data-testid="stExpander"] summary svg {{
    fill: white !important;
    opacity: 1 !important;
}}

/* 4. Text doložky bude také BÍLÝ (protože pozadí je teď tmavé) */
.legal-text {{
    color: white !important;
    font-size: 11px !important;
    text-align: justify;
    line-height: 1.4;
}}

/* 5. Odstraní šedé podbarvení při najetí myší na nadpis */
[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {{
    background-color: transparent !important;
}}
/* Úplné odstranění obdélníku (pozadí i okrajů) u expanderu v sidebaru */
[data-testid="stSidebar"] [data-testid="stExpander"],
[data-testid="stSidebar"] [data-testid="stExpander"] > div,
[data-testid="stSidebar"] [data-testid="stExpanderDetails"],
[data-testid="stSidebar"] [data-testid="stExpander"] summary {{
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}}

/* Zajištění, že text doložky i nadpis budou bílé, protože teď budou na tmavém pozadí */
.legal-text {{
    color: white !important;
}}

[data-testid="stSidebar"] [data-testid="stExpander"] summary p {{
    color: white !important;
    opacity: 1 !important;
}}

[data-testid="stSidebar"] [data-testid="stExpander"] summary svg {{
    fill: white !important;
}}


/* Odsazení textu doložky směrem dolů od nadpisu */
[data-testid="stSidebar"] [data-testid="stExpanderDetails"] {{
    padding-top: 0px !important; /* Čím větší číslo, tím větší mezera */
    margin-top: -25px !important; /* ZÁPORNÁ HODNOTA posune text NAHORU */
    background-color: transparent !important;
    border: none !important;
}}


/* Zvýraznění rámečku expanderu na bílou */
[data-testid="stSidebar"] [data-testid="stExpander"] {{
    border: 1px solid rgba(255, 255, 255, 1) !important; /* Čistě bílá linka */
    border-radius: 10px !important;
    background-color: transparent !important;
}}

/* Odsazení vnitřního textu od nadpisu */
[data-testid="stSidebar"] [data-testid="stExpanderDetails"] {{
    padding-top: 25px !important;
    background-color: transparent !important;
}}

/* Oprava čitelnosti nadpisu (aby byl bílý i v zavřeném stavu) */
[data-testid="stSidebar"] [data-testid="stExpander"] summary p {{
    color: white !important;
    opacity: 1 !important;
}}


/* Cílení přímo na kreslený tvar (path) uvnitř SVG ikony */
[data-testid="stSidebar"] [data-testid="stExpander"] svg path {{
    fill: #ffffff !important;
    stroke: #ffffff !important;
}}

/* Pro jistotu zacílení na celou ikonu s maximální prioritou */
[data-testid="stSidebar"] [data-testid="stExpander"] .st-expanderIcon svg {{
    fill: white !important;
    stroke: white !important;
    color: white !important;
}}

/* Odstranění efektu 'ztmavení' při nečinnosti */
[data-testid="stSidebar"] [data-testid="stExpander"] summary {{
    color: white !important;
}}

</style>
'''
st.markdown(style, unsafe_allow_html=True)

# --- 3. POMOCNÉ FUNKCE PRO VÝBĚR ---
def get_compare_selector(df_input, key_prefix):
    st.markdown('<div style="background:transparent; margin-bottom:10px;">', unsafe_allow_html=True)
    gen = st.selectbox(f"Generace", ["Vyberte"] + sorted(df_input['Generace'].unique().tolist()), key=f"gen_{key_prefix}")
    res = None
    if gen != "Vyberte":
        temp = df_input[df_input['Generace'] == gen]
        seznam_kar = serad_karoserie(temp['Karoserie'].unique().tolist())
        kar = st.selectbox(f"Karoserie", ["Vyberte"] + seznam_kar, key=f"kar_{key_prefix}")
        if kar != "Vyberte":
            temp = temp[temp['Karoserie'] == kar]
            mot = st.selectbox(f"Motorizace", ["Vyberte"] + sorted(temp['Motor'].unique().tolist()), key=f"mot_{key_prefix}")
            if mot != "Vyberte":
                res = temp[temp['Motor'] == mot].iloc[0]
    st.markdown('</div>', unsafe_allow_html=True)
    return res

# --- 4. LOGIKA A DATA ---
try:
    df_origin = pd.read_excel("Py_F_data_3.xlsx")
    
    with st.sidebar:
        st.markdown("## 🛠️ Menu")
        rezim = st.radio("Zvolte režim:", ["Detail vozu", "Porovnávač"])
        st.write("---")
        
        if rezim == "Detail vozu":
            st.markdown("### 🔍 Filtr vozu")
            df_detail = df_origin.copy()
            sel_gen = st.selectbox("1. Generace", ["Vše"] + sorted(df_detail['Generace'].unique().tolist()))
            if sel_gen != "Vše": df_detail = df_detail[df_detail['Generace'] == sel_gen]
            
            seznam_kar_sidebar = serad_karoserie(df_detail['Karoserie'].unique().tolist())
            sel_kar = st.selectbox("2. Karoserie", ["Vše"] + seznam_kar_sidebar)
            if sel_kar != "Vše": df_detail = df_detail[df_detail['Karoserie'] == sel_kar]
            
            sel_mot = st.selectbox("3. Motorizace", ["Vše"] + sorted(df_detail['Motor'].unique().tolist()))
            if sel_mot != "Vše": df_detail = df_detail[df_detail['Motor'] == sel_mot]
        
        for _ in range(12): st.write("")
        with st.expander("⚖️ Právní doložka"):
                st.markdown(f'''
            <div class="legal-text">
            <strong>Právní doložka a prohlášení:</strong> Tento web je neoficiální projekt vytvořený výhradně pro účely maturitní práce a edukaci v oblasti analýzy dat. Projekt je vytvořen v souladu s § 35 odst. 3 zákona č. 121/2000 Sb. (Autorský zákon) o užití školního díla pro potřeby školy a pro účely výuky.<br><br>
            <b>Zdroje dat:</b> Veškeré technické parametry a dobové ceny byly čerpány z veřejně dostupných archivů a oficiálních materiálů Škoda Auto.<br><br>
            <b>Aktualita:</b> Data mají informativní charakter a mohou se lišit od reálných historických nabídek. Autor neručí za případné chyby v datech.<br><br>
            <b>Autorská práva:</b> Užití ochranných známek slouží výhradně k identifikaci produktů a nepředstavuje spojení s držitelem práv. Ochranná známka Škoda a názvy modelů jsou majetkem společnosti Škoda Auto a.s.<br><br>
            <b>Neziskovost:</b> Projekt není využíván ke komerčním účelům ani k žádné formě výdělku.<br><br>
            <strong>Autor:</strong> Vojtěch Hendrych<br>
            <strong>Škola:</strong> SPŠ strojnická, Betlémská 287/4, Praha 1<br>
            <strong>Školní rok:</strong> 2025/2026
            </div>
            ''', unsafe_allow_html=True)

    st.markdown('<div class="header-container"><span class="main-title">KATALOG FABIA</span></div>', unsafe_allow_html=True)

    # --- REŽIM: DETAIL VOZU ---
    if rezim == "Detail vozu":
        if len(df_detail) > 0:
            car = df_detail.iloc[0]
            st.markdown(f'''
                <div class="custom-card top-card">
                    <h1>{car['Motor']}</h1>
                    <p>Generace: <b>{car['Generace']}</b> | Rok: <b>{car.get('Rok', '-')}</b> | Karoserie: <b>{car['Karoserie']}</b></p>
                </div>
            ''', unsafe_allow_html=True)
            
            col_l, col_r = st.columns(2)
            with col_l:
                st.markdown(f'''
                    <div class="custom-card">
                    <div class="card-title">🚗 Motor</div>
                        <p>Objem: <b>{car.get('Objem [l]', '-')} l</b></p>
                        <p>Výkon: <b>{car.get('Výkon [kW]', '-')} kW</b></p>
                        <p>Točivý moment: <b>{car.get('Točivý moment [Nm]', '-')} Nm</b></p> 
                        <p>Zdvihový objem: <b>{car.get('Zdvihový objem v [cm³]', '-')} cm³</b></p>
                        <p>Počet válců: <b>{car.get('Počet válců', '-')}</b></p>
                        <p>Typ: <b>{car.get('Typ', '-')}</b></p> 
                    </div>
                    <div class="custom-card">
                        <div class="card-title">⚙️ Ústrojí</div>
                        <p>Pohon: <b>{car.get('Pohon', '-')}</b></p>
                        <p>Převodovka: <b>{car.get('Převodovka', '-')}</b></p>
                        <p>Spojka: <b>{car.get('Spojka', '-')}</b></p>
                    </div>
                    <div class="custom-card">
                        <div class="card-title">⏱️ Rychlosti</div>
                        <p>Nejvyšší rychlost: <b>{car.get('Nejvyšší rychlost [km/h]', '-')} km/h</b></p>
                        <p>Zrychlení 0-100 km/h: <b>{car.get('Zrychlení 0 - 100 km/h', '-')} s</b></p>
                    </div>
                    
                ''', unsafe_allow_html=True)

            with col_r:
                st.markdown(f'''
                    <div class="custom-card">
                        <div class="card-title">⛽ Palivo</div>
                        <p>Typ paliva: <b>{car.get('Typ paliva', '-')}</b></p>
                        <p>Kombinovaná spotřeba paliva: <b>{car.get('Kombinovaná spotřeba paliva [l/100 km]', '-')} l/100 km</b></p>
                    </div>
                    <div class="custom-card">
                        <div class="card-title">☁️ Emise</div>
                        <p>Emisní hodnoty CO2: <b>{car.get('Emisní hodnoty CO2 [g/km]', '-')} g/km</b></p>
                        <p>Exhalační norma: <b>{car.get('Exhalační norma', '-')}</b></p>
                    </div>
                    <div class="custom-card">
                        <div class="card-title">⚖️ Hmotnosti</div>
                        <p>Celková hmotnost: <b>{car.get('Celková hmotnost [kg]', '-')} kg</b></p>
                        <p>Pohotovostní hmotnost: <b>{car.get('Pohotovostní hmotnost [kg]', '-')} kg</b></p>
                    </div>
                    <div class="custom-card">
                        <div class="card-title">📦 Objemy</div>
                        <p>Objem zavazadlového prostoru: <b>{car.get('Objem zavazadlového prostoru [l]', '-')} l</b></p>
                        <p>Objem palivové nádrže: <b>{car.get('Objem palivové nádrže [l]', '-')} l</b></p>
                    </div>
                ''', unsafe_allow_html=True)

            # Ceny a výbavy
            vybavy_cols = ['Easy', 'Classic', 'Comfort', 'Elegance', 'RS', 'Ambient', 'Scout', 'Sport', 'Monte Carlo', 'Active', 'Ambition', 'Style', 'Selection', 'Top Selection', '130 Let', '130 Premium', 'Dynamic', 'R5']
            ceny_list = []
            for col in vybavy_cols:
                if col in car and pd.notnull(car[col]):
                    val = car[col]
                    formatted = f"{int(val):,}".replace(",", " ") if isinstance(val, (int, float)) else str(val)
                    ceny_list.append(f'<div class="price-item">{col}:<br><b>{formatted} Kč</b></div>')
            
            ceny_html = f'<div class="price-container">{" ".join(ceny_list)}</div>' if ceny_list else "Ceny nejsou k dispozici."
            st.markdown(f'<div class="custom-card"><div class="card-title">🏷️ Dobové ceny a výbavy</div>{ceny_html}</div>', unsafe_allow_html=True)
        else:
            st.info("Upřesněte výběr v levém menu.")

    # --- REŽIM: POROVNÁVAČ ---
    elif rezim == "Porovnávač":
        st.markdown('<div style="text-align: center;"><div class="title-widget"><h1>Porovnávač</h1></div></div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: car1 = get_compare_selector(df_origin, "v1")
        with c2: car2 = get_compare_selector(df_origin, "v2")

        if car1 is not None and car2 is not None:
            st.write("---")
            h1, h_vs, h2 = st.columns([1.5, 0.7, 1.5])
            
            with h1: 
                st.markdown(f'''
                    <div class="custom-card top-card" style="padding: 20px;">
                        <h1>{car1["Motor"]}</h1>
                        <p>Generace: <b>{car1["Generace"]}</b> | Rok: <b>{car1.get("Rok", "-")}</b> | Karoserie: <b>{car1["Karoserie"]}</b></p>
                    </div>
                ''', unsafe_allow_html=True)
                
            with h_vs: 
                st.markdown('<div style="text-align:center; padding-top:45px; font-size:35px; color:white; font-weight:900; text-shadow: 2px 2px 10px rgba(0,0,0,1);">VS</div>', unsafe_allow_html=True)
                
            with h2: 
                st.markdown(f'''
                    <div class="custom-card top-card" style="padding: 20px;">
                        <h1>{car2["Motor"]}</h1>
                        <p>Generace: <b>{car2["Generace"]}</b> | Rok: <b>{car2.get("Rok", "-")}</b> | Karoserie: <b>{car2["Karoserie"]}</b></p>
                    </div>
                ''', unsafe_allow_html=True)
            
            params = [
                ("Objem [l]", "Objem (l)", True),
                ("Výkon [kW]", "Výkon (kW)", True),
                ("Točivý moment [Nm]", "Točivý moment (Nm)", True),
                ("Zdvihový objem v [cm³]", "Zdvihový objem (cm³)", True),
                ("Počet válců", "Počet válců", True),
                ("Nejvyšší rychlost [km/h]", "Nejvyšší rychlost (km/h)", True),
                ("Zrychlení 0 - 100 km/h", "Zrychlení 0-100 km/h (s)", False),
                ("Kombinovaná spotřeba paliva [l/100 km]", "Kombinovaná spotřeba paliva (l/100km)", False),
                ("Emisní hodnoty CO2 [g/km]", "Emisní hodnoty CO2 (g/km)", False),
                ("Celková hmotnost [kg]", "Celková hmotnost (kg)", False),
                ("Pohotovostní hmotnost [kg]", "Pohotovostní hmotnost (kg)", False),
                ("Objem zavazadlového prostoru [l]", "Objem zavazadlového prostoru (l)", True),
                ("Objem palivové nádrže [l]", "Objem palivové nádrže (l)", True)
            ]
            
            s1, s2 = 0, 0
            for ex, lab, hb in params:
                v1, v2 = car1.get(ex, "-"), car2.get(ex, "-")
                cl1, cl2 = "", ""
                try:
                    n1, n2 = float(str(v1).replace(',','.')), float(str(v2).replace(',','.'))
                    if n1 != n2:
                        if (n1 > n2 if hb else n1 < n2): cl1, cl2, s1 = 'better-spec', 'worse-spec', s1 + 1
                        else: cl2, cl1, s2 = 'better-spec', 'worse-spec', s2 + 1
                except: pass
                st.markdown(f'<div class="compare-row"><div class="compare-value {cl1}">{v1}</div><div class="compare-label">{lab}</div><div class="compare-value {cl2}">{v2}</div></div>', unsafe_allow_html=True)

            winner = car1['Motor'] if s1 > s2 else (car2['Motor'] if s2 > s1 else "Remíza")
            st.markdown(f'<div class="winner-card">🏆 Celkový vítěz: {winner} ({s1}:{s2})</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Chyba: {e}")