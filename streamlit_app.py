import math
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
from collections import defaultdict
import time
import hashlib
import json
import os
import sqlite3
from pathlib import Path
import sys

# ===== CONFIGURAZIONE =====
st.set_page_config(layout="wide")

# ===== FIX PER STREAMLIT CLOUD =====
# Su Streamlit Cloud, l'unica directory scrivibile è /tmp
DB_PATH = Path("/tmp/hotel_game.db")

# Verifica che possiamo scrivere in /tmp
print(f"📁 Usando database in: {DB_PATH}", file=sys.stderr)
print(f"📁 La directory /tmp è scrivibile: {os.access('/tmp', os.W_OK)}", file=sys.stderr)

# Funzione per ottenere connessione al database
def get_db_connection():
    """Restituisce una connessione al database SQLite"""
    try:
        conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        return conn
    except Exception as e:
        print(f"❌ Errore connessione database: {e}", file=sys.stderr)
        # Fallback: database in memoria
        return sqlite3.connect(":memory:")

# ===== TRADUZIONI =====
TRANSLATIONS = {
    "it": {
        "title": "🏨 Hotel Revenue Management Game",
        "subtitle": "⚡ Metti alla prova le tue competenze di pricing e osserva il fatturato crescere! 💰 Sei pronto a sfidare il mercato?",
        "controls": "⚙️ Controlli",
        "speed": "⏱️ Velocità",
        "speed_help": "Secondi per giorno",
        "start": "▶️ Start",
        "pause": "⏸️ Pausa",
        "reset": "🔄 Reset",
        "stats": "📊 Statistiche",
        "date": "Data",
        "total_revenue": "Revenue Totale",
        "daily_revenue": "Revenue Giornaliero",
        "total_rooms": "Camere Totali",
        "time_remaining": "⏳ Tempo Rimanente",
        "click_start": "👉 Clicca **Start** per iniziare!",
        "click_next_day": "👉 Usa il tasto 'Avanti' per passare al giorno successivo",
        "set_prices": "💰 Imposta prezzi per aprile",
        "price_table_date": "Data",
        "price_table_day": "Giorno",
        "price_table_price": "Prezzo (€)",
        "price_table_bookings": "Prenotazioni",
        "past": "(passato)",
        "future": "(futuro)",
        "occupancy": "📅 Occupazione Aprile",
        "occupancy_table_date": "Data",
        "occupancy_table_bookings": "Camere",
        "occupancy_table_percent": "Occupazione",
        "occupancy_table_revenue": "Revenue",
        "booking_details": "📋 Dettagli Prenotazioni",
        "select_stay_day": "Seleziona giorno di soggiorno",
        "booking_table_date": "Data Prenotazione",
        "booking_table_rooms": "Camere",
        "booking_table_price": "Prezzo",
        "booking_table_revenue": "Revenue",
        "no_bookings": "Nessuna prenotazione",
        "current_state": "📍 Stato Corrente",
        "current_date": "Data Corrente",
        "days_remaining": "Giorni Rimanenti",
        "total_booked": "Totale Prenotato",
        "game_end": "🎉 **GIOCO TERMINATO!** Revenue totale: **€ {revenue:,.0f}**",
        "language": "🌐 Lingua",
        "generating": "⏳ Generando prenotazioni...",
        "price_locked": "🔒 Bloccato",
        "march": "📅 MARZO 2026",
        "april": "🌸 APRILE 2026",
        "booking_from": "Prenotazioni dal",
        "total_for_day": "Totale giornata",
        "rooms": "camere",
        "april_only": "📅 Ad aprile si gioca! Imposta i prezzi ogni giorno, monitora l'occupazione e conquista la classifica. Le prenotazioni partono a marzo, ma i soggiorni sono ad aprile per simulare un hotel già operativo.",
        "instructions": "Imposta i prezzi ogni giorno e cerca di massimizzare il revenue. Buona fortuna!",
        "login": "🔐 Accedi al tuo Profilo",
        "email": "📧 Email",
        "login_identifier": "📧 Email o username",
        "username": "👤 Nome utente",
        "password": "🔑 Password",
        "login_button": "Accedi",
        "register_button": "Registrati",
        "logout": "🚪 Logout",
        "welcome": "Benvenuto",
        "login_error": "Email/username o password errati",
        "register_error": "Email già registrata",
        "register_success": "Registrazione completata! Ora puoi accedere",
        "profile": "👤 Il mio Profilo",
        "best_score": "🏆 Miglior Punteggio",
        "games_played": "🎮 Partite Giocate",
        "last_game": "🕐 Ultima Partita",
        "member_since": "📅 Membro dal",
        "save_score": "💾 Salva Punteggio",
        "score_saved": "Punteggio salvato!",
        "leaderboard": "🏆 Classifica Globale",
        "login_prompt_leaderboard": "Effettua l'accesso o registrati per partecipare alla classifica!",
        "rank": "Posizione",
        "player": "Giocatore",
        "score": "Punteggio",
        "date_achieved": "Data",
        "email_placeholder": "nome@esempio.com o username",
        "username_placeholder": "Scegli un username",
        "password_placeholder": "Minimo 6 caratteri",
        "login_tab": "🔐 Accedi",
        "register_tab": "📝 Registrati",
        "my_scores": "📊 I miei punteggi",
        "no_scores_yet": "Nessun punteggio salvato. Gioca e salva il tuo primo punteggio!",
        "score_history": "Cronologia punteggi",
        "date": "Data",
        "score_value": "Punteggio",
        "next_day": "⏭️ Avanti (Prossimo Giorno)",
        "pickup": "📈 Pick‑up prenotazioni",
    },
    "en": {
        "title": "🏨 Hotel Revenue Management Game",
        "subtitle": "⚡ Master pricing, boost your revenue, and climb the leaderboard! 💰 April is your chance—can you outsmart the market?",
        "controls": "⚙️ Controls",
        "speed": "⏱️ Speed",
        "speed_help": "Seconds per day",
        "start": "▶️ Start",
        "pause": "⏸️ Pause",
        "reset": "🔄 Reset",
        "stats": "📊 Stats",
        "date": "Date",
        "total_revenue": "Total Revenue",
        "daily_revenue": "Daily Revenue",
        "total_rooms": "Total Rooms",
        "time_remaining": "⏳ Time Left",
        "click_start": "👉 Click **Start** to begin!",
        "click_next_day": "👉 Use the 'Next Day' button to advance",
        "set_prices": "💰 Set Prices ( April)",
        "price_table_date": "Date",
        "price_table_day": "Day",
        "price_table_price": "Price (€)",
        "price_table_bookings": "Bookings",
        "past": "(past)",
        "future": "(future)",
        "occupancy": "📅 April Occupancy",
        "occupancy_table_date": "Date",
        "occupancy_table_bookings": "Rooms",
        "occupancy_table_percent": "Occupancy",
        "occupancy_table_revenue": "Revenue",
        "booking_details": "📋 Booking Details",
        "select_stay_day": "Select stay day",
        "booking_table_date": "Booking Date",
        "booking_table_rooms": "Rooms",
        "booking_table_price": "Price",
        "booking_table_revenue": "Revenue",
        "no_bookings": "No bookings yet",
        "current_state": "📍 Current State",
        "current_date": "Current Date",
        "days_remaining": "Days Left",
        "total_booked": "Total Booked",
        "game_end": "🎉 **GAME OVER!** Total revenue: **€ {revenue:,.0f}**",
        "language": "🌐 Language",
        "generating": "⏳ Generating bookings...",
        "price_locked": "🔒 Locked",
        "march": "📅 MARCH 2026",
        "april": "🌸 APRIL 2026",
        "booking_from": "Bookings from",
        "total_for_day": "Daily total",
        "rooms": "rooms",
        "april_only": "📅 April is game time! Set daily prices, monitor occupancy and conquer the leaderboard. Bookings begin in March but stays take place in April to simulate a hotel already in operation.",
        "instructions": "Set daily prices and aim to maximize revenue – good luck, future economists!",
        "login": "🔐 Access Your Profile",
        "email": "📧 Email",
        "login_identifier": "📧 Email or username",
        "username": "👤 Username",
        "password": "🔑 Password",
        "login_button": "Login",
        "register_button": "Register",
        "logout": "🚪 Logout",
        "welcome": "Welcome",
        "login_error": "Invalid email/username or password",
        "register_error": "Email already registered",
        "register_success": "Registration successful! You can now login",
        "profile": "👤 My Profile",
        "best_score": "🏆 Best Score",
        "games_played": "🎮 Games Played",
        "last_game": "🕐 Last Game",
        "member_since": "📅 Member since",
        "save_score": "💾 Save Score",
        "score_saved": "Score saved!",
        "leaderboard": "🏆 Global Leaderboard",
        "login_prompt_leaderboard": "Please log in or register to participate in the leaderboard!",
        "rank": "Rank",
        "player": "Player",
        "score": "Score",
        "date_achieved": "Date",
        "email_placeholder": "name@example.com or username",
        "username_placeholder": "Choose a username",
        "password_placeholder": "Minimum 6 characters",
        "login_tab": "🔐 Login",
        "register_tab": "📝 Register",
        "my_scores": "📊 My Scores",
        "no_scores_yet": "No scores saved yet. Play and save your first score!",
        "score_history": "Score history",
        "date": "Date",
        "score_value": "Score",
        "next_day": "⏭️ Next Day",
        "pickup": "📈 Booking pick-up",
    }
}

def t(key):
    lang = st.session_state.get("language", "it")
    return TRANSLATIONS.get(lang, TRANSLATIONS["it"]).get(key, key)

# ===== DATABASE SETUP =====
def init_database():
    """Inizializza il database SQLite per salvare i profili"""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        # Tabella utenti
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      email TEXT UNIQUE,
                      username TEXT UNIQUE,
                      password TEXT,
                      best_score INTEGER DEFAULT 0,
                      games_played INTEGER DEFAULT 0,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      last_login TIMESTAMP,
                      last_game TIMESTAMP)''')
        
        # Tabella punteggi per classifica
        c.execute('''CREATE TABLE IF NOT EXISTS scores
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      user_id INTEGER,
                      score INTEGER,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      FOREIGN KEY (user_id) REFERENCES users (id))''')
        
        conn.commit()
        conn.close()
        print("✅ Database inizializzato correttamente", file=sys.stderr)
    except Exception as e:
        print(f"❌ Errore inizializzazione database: {e}", file=sys.stderr)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_by_email(email):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    return user

def get_user_by_identifier(identifier):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM users WHERE email = ? OR username = ?",
        (identifier, identifier),
    )
    user = c.fetchone()
    conn.close()
    return user

def get_user_by_id(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def create_user(email, username, password):
    conn = get_db_connection()
    c = conn.cursor()
    try:
        hashed = hash_password(password)
        c.execute("INSERT INTO users (email, username, password, created_at, last_login) VALUES (?, ?, ?, ?, ?)",
                 (email, username, hashed, datetime.now(), datetime.now()))
        conn.commit()
        user_id = c.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def update_user_login(email):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("UPDATE users SET last_login = ? WHERE email = ?", (datetime.now(), email))
    conn.commit()
    conn.close()

def update_user_stats(user_id, score):
    conn = get_db_connection()
    c = conn.cursor()
    
    # Aggiorna best score se necessario
    c.execute("SELECT best_score FROM users WHERE id = ?", (user_id,))
    current_best = c.fetchone()[0]
    
    if score > current_best:
        c.execute("UPDATE users SET best_score = ?, games_played = games_played + 1, last_game = ? WHERE id = ?",
                 (score, datetime.now(), user_id))
    else:
        c.execute("UPDATE users SET games_played = games_played + 1, last_game = ? WHERE id = ?",
                 (datetime.now(), user_id))
    
    # Salva il punteggio nella tabella scores
    c.execute("INSERT INTO scores (user_id, score) VALUES (?, ?)", (user_id, score))
    
    conn.commit()
    conn.close()

def get_user_scores(user_id, limit=10):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT score, created_at 
        FROM scores 
        WHERE user_id = ? 
        ORDER BY created_at DESC
        LIMIT ?
    """, (user_id, limit))
    scores = c.fetchall()
    conn.close()
    return scores

def get_leaderboard(limit=10):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT u.username, MAX(s.score) AS best_score
        FROM scores s
        JOIN users u ON s.user_id = u.id
        GROUP BY u.id
        ORDER BY best_score DESC
        LIMIT ?
    """, (limit,))
    scores = c.fetchall()
    conn.close()
    return scores

def get_user_stats(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT username, email, best_score, games_played, created_at, last_game FROM users WHERE id = ?", (user_id,))
    stats = c.fetchone()
    conn.close()
    return stats

# Inizializza il database all'avvio
init_database()

# ===== LOGIN UI =====
def show_login_ui():
    with st.sidebar:
        st.divider()
        st.subheader(t("login"))
        
        if 'user_id' not in st.session_state:
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.session_state.user_username = None
            st.session_state.auth_tab = st.session_state.get("auth_tab", "login")
        
        if st.session_state.user_id is None:
            col_login, col_register = st.columns(2)
            login_clicked = col_login.button(t("login_tab"), use_container_width=True)
            register_clicked = col_register.button(t("register_tab"), use_container_width=True)
            if login_clicked:
                st.session_state.auth_tab = "login"
            if register_clicked:
                st.session_state.auth_tab = "register"

            if st.session_state.auth_tab == "login":
                identifier = st.text_input(t("login_identifier"), key="login_identifier", placeholder=t("email_placeholder"))
                password = st.text_input(t("password"), type="password", key="login_password", placeholder=t("password_placeholder"))

                if st.button(t("login_button"), use_container_width=True):
                    if identifier and password:
                        user = get_user_by_identifier(identifier)
                        if user and user[3] == hash_password(password):
                            st.session_state.user_id = user[0]
                            st.session_state.user_email = user[1]
                            st.session_state.user_username = user[2]
                            update_user_login(user[1])
                            st.success(f"{t('welcome')}, {user[2]}!")
                            time.sleep(1)
                            st.rerun()
                        else:
                            st.error(t("login_error"))
                    else:
                        st.error("Inserisci email e password")
            else:
                reg_email = st.text_input(t("email"), key="reg_email", placeholder=t("email_placeholder"))
                reg_username = st.text_input(t("username"), key="reg_username", placeholder=t("username_placeholder"))
                reg_password = st.text_input(t("password"), type="password", key="reg_password", placeholder=t("password_placeholder"))
                reg_password_confirm = st.text_input("Conferma password", type="password", key="reg_password_confirm")
                
                if st.button(t("register_button"), use_container_width=True):
                    if not reg_email or not reg_username or not reg_password:
                        st.error("Tutti i campi sono obbligatori")
                    elif '@' not in reg_email:
                        st.error("Inserisci un'email valida")
                    elif len(reg_password) < 6:
                        st.error("La password deve essere almeno 6 caratteri")
                    elif reg_password != reg_password_confirm:
                        st.error("Le password non coincidono")
                    else:
                        existing = get_user_by_email(reg_email)
                        if existing:
                            st.error(t("register_error"))
                        else:
                            user_id = create_user(reg_email, reg_username, reg_password)
                            if user_id:
                                st.success(t("register_success"))
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error("Errore durante la registrazione. Username potrebbe già esistere.")
        else:
            st.success(f"✅ {t('welcome')}, {st.session_state.user_username}!")
            
            stats = get_user_stats(st.session_state.user_id)
            if stats:
                username, email, best_score, games_played, created_at, last_game = stats
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(t("best_score"), f"€{best_score:,.0f}")
                with col2:
                    st.metric(t("games_played"), games_played)
                
                st.caption(f"📧 {email}")
                st.caption(f"{t('member_since')}: {datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y')}")
                if last_game:
                    st.caption(f"{t('last_game')}: {datetime.strptime(last_game, '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y %H:%M')}")
                
                st.divider()
                st.subheader(t("my_scores"))
                scores = get_user_scores(st.session_state.user_id, 5)
                if scores:
                    scores_data = []
                    for score, date in scores:
                        scores_data.append({
                            t('date'): datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').strftime('%d/%m/%Y %H:%M'),
                            t('score_value'): f"€{score:,.0f}"
                        })
                    st.dataframe(pd.DataFrame(scores_data), use_container_width=True, hide_index=True)
                else:
                    st.info(t("no_scores_yet"))
            
            if st.button(t("logout"), use_container_width=True):
                st.session_state.user_id = None
                st.session_state.user_email = None
                st.session_state.user_username = None
                st.rerun()

# ===== LEADERBOARD =====
def show_leaderboard():
    scores = get_leaderboard(10)
    if scores:
        if st.session_state.get("user_id"):
            st.subheader(t("leaderboard"))
        else:
            if st.button(t("leaderboard")):
                st.warning(t("login_prompt_leaderboard"))
                st.session_state.auth_tab = "register"
                st.rerun()
        leaderboard_data = []
        for i, (username, best_score) in enumerate(scores, 1):
            leaderboard_data.append({
                t('rank'): i,
                t('player'): username,
                t('score'): f"€{best_score:,.0f}",
            })
        st.dataframe(pd.DataFrame(leaderboard_data), use_container_width=True, hide_index=True)


st.markdown(
    """
    <style>
    [data-testid="stButton"][data-key="next_day_button"] > button {
        background-color: #ff6600 !important;
        color: white !important;
        font-size: 1.2em !important;
        font-weight: bold !important;
        border-radius: 8px !important;
    }
    .stButton>button {
        padding: 0.6rem 1rem !important;
    }
    .css-1d391kg, .css-18e3th9 {padding: 1rem 2rem !important;}
    .css-1d391kg h1, .css-1d391kg h2 {text-align: center;}
    .css-1d391kg .css-1cpxqw2 {background-color: #f9f9f9;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title(t("title"))
st.markdown(f"**{t('subtitle')}**")
st.caption(t("april_only"))
st.caption(t("instructions"))

# ===== INIZIALIZZAZIONE =====
if "init" not in st.session_state:
    st.session_state.language = "it"
    st.session_state.game_running = False
    st.session_state.current_date = datetime(2026, 3, 1)
    st.session_state.total_rooms = 30  # Valore iniziale predefinito
    st.session_state.total_revenue = 0
    st.session_state.user_id = None
    st.session_state.user_email = None
    st.session_state.user_username = None
    st.session_state.auth_tab = "login"
    
    st.session_state.prices = {}
    d = datetime(2026, 3, 1)
    while d <= datetime(2026, 4, 30):
        st.session_state.prices[d.strftime("%Y-%m-%d")] = 100
        d += timedelta(days=1)
    
    st.session_state.bookings = defaultdict(lambda: defaultdict(int))
    st.session_state.daily_occupancy = defaultdict(int)
    st.session_state.daily_revenue = defaultdict(float)
    
    st.session_state.last_update = time.time()
    st.session_state.elapsed = 0
    st.session_state.paused_elapsed = 0
    st.session_state.init = True
    st.session_state.speed = 2
    st.session_state.game_completed = False

# ===== FUNZIONI =====
def generate_bookings(booking_date):
    booking_str = booking_date.strftime("%Y-%m-%d")
    total_new_bookings = 0

    for day in range(1, 31):
        stay_date = datetime(2026, 4, day)

        if stay_date < booking_date:
            continue

        stay_str = stay_date.strftime("%Y-%m-%d")
        current_occupancy = st.session_state.daily_occupancy[stay_str]

        if current_occupancy >= st.session_state.total_rooms:
            continue

        available = st.session_state.total_rooms - current_occupancy
        stay_price = st.session_state.prices.get(stay_str, 100)

        # Logistic demand curve
        price_0 = 120      # inflection price (50% demand)
        alpha = 0.05       # price sensitivity

        demand_fraction = 1 / (1 + math.exp(alpha * (stay_price - price_0)))

        expected_total_demand = st.session_state.total_rooms * demand_fraction

        # Booking window effect (closer dates book faster)
        days_before = (stay_date - booking_date).days
        time_factor = max(0.5, min(2.0, 20 / max(1, days_before)))

        potential_demand = int(expected_total_demand * time_factor * random.uniform(0.6, 1.4))

        new_bookings = min(potential_demand, available)

        if new_bookings > 0:
            st.session_state.bookings[stay_str][booking_str] += new_bookings
            st.session_state.daily_occupancy[stay_str] += new_bookings

            revenue = new_bookings * stay_price
            st.session_state.daily_revenue[stay_str] += revenue
            st.session_state.total_revenue += revenue

            total_new_bookings += new_bookings

    return total_new_bookings

def advance_day():
    if st.session_state.current_date <= datetime(2026, 4, 30):
        new_bookings = generate_bookings(st.session_state.current_date)
        st.session_state.current_date += timedelta(days=1)
        return new_bookings
    return 0

def reset_game():
    st.session_state.game_running = False
    st.session_state.current_date = datetime(2026, 3, 1)
    st.session_state.total_revenue = 0
    st.session_state.bookings = defaultdict(lambda: defaultdict(int))
    st.session_state.daily_occupancy = defaultdict(int)
    st.session_state.daily_revenue = defaultdict(float)
    st.session_state.last_update = time.time()
    st.session_state.elapsed = 0
    st.session_state.paused_elapsed = 0
    st.session_state.game_completed = False

# ===== SHOW LOGIN UI =====
with st.sidebar:
    language = st.selectbox(
        "Lingua",
        ["🇮🇹 Italiano", "🇬🇧 English"],
        index=0 if st.session_state.get("language", "it") == "it" else 1,
        key="language_selector",
        label_visibility="collapsed"
    )
    selected_lang = "it" if "Italiano" in language else "en"
    if selected_lang != st.session_state.get("language", "it"):
        st.session_state.language = selected_lang
        st.rerun()

show_login_ui()

with st.sidebar:
    st.divider()
    show_leaderboard()

with st.sidebar:
    st.divider()
    st.header(t("controls"))

    # Widget per il numero di camere - usa solo il valore da session_state senza impostarlo anche qui
    rooms_value = st.number_input(
        t("total_rooms"),
        min_value=1,
        max_value=100,
        value=st.session_state.total_rooms,
        step=1,
        disabled=st.session_state.game_running,
        key="rooms_input"
    )
    # Aggiorna session_state solo se il valore è cambiato
    if rooms_value != st.session_state.total_rooms:
        st.session_state.total_rooms = rooms_value

    col_top1, col_top2 = st.columns([1,1])
    with col_top1:
        if st.button(t("start"), use_container_width=True, key="start_button"):
            st.session_state.game_running = True
            st.session_state.last_update = time.time()
            st.session_state.game_completed = False
            if st.session_state.paused_elapsed > 0:
                st.session_state.last_update = time.time() - st.session_state.paused_elapsed
                st.session_state.paused_elapsed = 0
    with col_top2:
        if st.button(t("reset"), use_container_width=True, key="reset_button"):
            reset_game()
    
    if st.session_state.game_running:
        col_bottom = st.columns([2])[0]
        with col_bottom:
            if st.button(t("next_day"), use_container_width=True, key="next_day_button"):
                if st.session_state.current_date <= datetime(2026, 4, 30):
                    advance_day()
                    st.rerun()
                else:
                    st.session_state.game_running = False
                    st.session_state.game_completed = True
                    st.rerun()

    st.divider()
    st.subheader(t("stats"))
    st.metric(t("date"), st.session_state.current_date.strftime("%d/%m/%Y"))
    st.metric(t("total_revenue"), f"€{st.session_state.total_revenue:,.0f}")

    st.divider()

    if st.session_state.game_running:
        st.info(t("click_next_day"))
    else:
        st.info(t("click_start"))

if not st.session_state.game_running and st.session_state.current_date == datetime(2026, 3, 1) and not st.session_state.game_completed:
    st.info(t("click_start"))

if st.session_state.game_completed and st.session_state.user_id:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(f"{t('save_score')} (€{st.session_state.total_revenue:,.0f})", use_container_width=True):
            update_user_stats(st.session_state.user_id, st.session_state.total_revenue)
            st.success(t("score_saved"))
            time.sleep(1)
            st.rerun()

st.header(t("set_prices"))

giorni = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]

rows = []
d = datetime(2026, 4, 1)
while d <= datetime(2026, 4, 30):
    date_str = d.strftime("%Y-%m-%d")
    is_past = d < st.session_state.current_date

    price_val = st.session_state.prices[date_str]
    occ = st.session_state.daily_occupancy[date_str]
    if occ == 0:
        occ_str = f"🟢 {occ}/{st.session_state.total_rooms}"
    elif occ < st.session_state.total_rooms:
        occ_str = f"🟡 {occ}/{st.session_state.total_rooms}"
    else:
        occ_str = f"🔴 {occ}/{st.session_state.total_rooms}"
    rev_str = f"€{st.session_state.daily_revenue[date_str]:,.0f}"

    locked = is_past and st.session_state.current_date.month == 4

    rows.append({
        "Data": d.strftime("%d/%m"),
        "Giorno": giorni[d.weekday()],
        "Prezzo": price_val,
        "_locked": locked,
        "Camere": occ_str,
        "Revenue": rev_str,
        "_key": date_str,
    })
    d += timedelta(days=1)

price_df = pd.DataFrame(rows)

meta_df = price_df[["_locked", "_key"]].copy()
display_df = price_df.drop(columns=["_locked", "_key"])

edited = st.data_editor(
    display_df,
    column_config={
        "Prezzo": st.column_config.NumberColumn(
            "💰 Prezzo",
            min_value=10,
            max_value=500,
            step=5,
        ),
        "Camere": st.column_config.TextColumn("📊 Camere", disabled=True),
        "Revenue": st.column_config.TextColumn("📈 Revenue", disabled=True),
        "Data": st.column_config.TextColumn("📅 Data", disabled=True),
        "Giorno": st.column_config.TextColumn("📆 Giorno", disabled=True),
    },
    hide_index=True,
    use_container_width=True,
)

for idx, row in edited.iterrows():
    key = meta_df.loc[idx, "_key"]
    if not meta_df.loc[idx, "_locked"]:
        st.session_state.prices[key] = row["Prezzo"]

st.header(t("booking_details"))

april_days = []
for date_str in st.session_state.bookings:
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        if date_obj.month == 4 and sum(st.session_state.bookings[date_str].values()) > 0:
            april_days.append(date_str)
    except:
        continue
        
selected = None
if april_days:
    selected = st.selectbox(
        t("select_stay_day"), 
        sorted(april_days),
        format_func=lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%d %b %Y")
    )
    
    st.markdown(f"**{t('booking_from')} {selected}**")

    pickup_data = {}
for book_date, rooms in st.session_state.bookings[selected].items():
    pickup_data[book_date] = pickup_data.get(book_date, 0) + rooms

# Convert to cumulative pick-up
pickup_data = dict(sorted(pickup_data.items()))
cumulative = 0
for k in pickup_data:
    cumulative += pickup_data[k]
    pickup_data[k] = cumulative
    if pickup_data:
        df_pickup = pd.DataFrame(
            sorted(pickup_data.items()),
            columns=[t("date"), t("rooms")]
        )
        st.subheader(t("pickup"))
        df_pickup[t("date")] = pd.to_datetime(df_pickup[t("date")])
        df_pickup = df_pickup.set_index(t("date"))
        st.line_chart(df_pickup)

    details = []
    total_rooms_day = 0
    total_rev_day = 0
    
    for book_date, rooms in sorted(st.session_state.bookings[selected].items()):
        if rooms > 0:
            price = st.session_state.prices.get(book_date, 100)
            revenue = rooms * price
            total_rooms_day += rooms
            total_rev_day += revenue
            
            book_dt = datetime.strptime(book_date, "%Y-%m-%d")
            stay_dt = datetime.strptime(selected, "%Y-%m-%d")
            days_before = (stay_dt - book_dt).days
            
            details.append({
                "Data prenotazione": book_dt.strftime("%d %b"),
                "Giorni prima": days_before,
                "Camere": rooms,
                "Prezzo": f"€{price}",
                "Revenue": f"€{revenue:,.0f}"
            })
    
    if details:
        st.dataframe(pd.DataFrame(details), use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        col1.metric(f"📊 Totale camere prenotate", f"{total_rooms_day}")
        col2.metric(f"💰 Revenue totale giornaliero", f"€{total_rev_day:,.0f}")
    else:
        st.info(f"Nessun dettaglio per {selected}")
else:
    st.info(t("no_bookings"))
    if st.session_state.game_running:
        st.caption(t("generating"))
        
        total_bookings = sum(sum(v.values()) for v in st.session_state.bookings.values())
        if total_bookings > 0:
            st.caption(f"📊 Totale prenotazioni: {total_bookings}")
        
        occupied_days = sum(1 for v in st.session_state.daily_occupancy.values() if v > 0)
        if occupied_days > 0:
            st.caption(f"📅 Giorni con prenotazioni: {occupied_days}/30")
        
        st.caption(f"📍 Data corrente: {st.session_state.current_date.strftime('%d/%m/%Y')}")

st.divider()

st.header(t("current_state"))

total_occ = sum(st.session_state.daily_occupancy.values())
max_possible = st.session_state.total_rooms * 30
occupancy_percentage = (total_occ / max_possible * 100) if max_possible > 0 else 0

if st.session_state.current_date <= datetime(2026, 4, 30):
    days_left = (datetime(2026, 4, 30) - st.session_state.current_date).days
else:
    days_left = 0

current_day_str = st.session_state.current_date.strftime("%Y-%m-%d")
day_rev = st.session_state.daily_revenue.get(current_day_str, 0)

if day_rev > 0:
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric(t("current_date"), st.session_state.current_date.strftime("%d %b %Y"))
    c2.metric(t("days_remaining"), max(0, days_left))
    c3.metric(t("total_booked"), f"{total_occ}/{max_possible} ({occupancy_percentage:.1f}%)")
    c4.metric(t("daily_revenue"), f"€{day_rev:,.0f}")
    c5.metric(t("total_revenue"), f"€{st.session_state.total_revenue:,.0f}")
else:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("current_date"), st.session_state.current_date.strftime("%d %b %Y"))
    c2.metric(t("days_remaining"), max(0, days_left))
    c3.metric(t("total_booked"), f"{total_occ}/{max_possible} ({occupancy_percentage:.1f}%)")
    c4.metric(t("total_revenue"), f"€{st.session_state.total_revenue:,.0f}")

total_days = 61
days_passed = (st.session_state.current_date - datetime(2026, 3, 1)).days
progress = min(1, days_passed / total_days)
st.progress(progress, text=f"Avanzamento: {days_passed}/{total_days} giorni")

if total_occ > 0:
    st.caption(f"📊 {total_occ} camere prenotate su {max_possible} disponibili")

if st.session_state.current_date > datetime(2026, 4, 30):
    st.balloons()
    st.success(t("game_end").format(revenue=st.session_state.total_revenue))
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Occupazione media", f"{occupancy_percentage:.1f}%")
    
    avg_price = st.session_state.total_revenue / total_occ if total_occ > 0 else 0
    col2.metric("Prezzo medio", f"€{avg_price:.0f}")
    
    if st.session_state.daily_occupancy:
        best_day_str = max(st.session_state.daily_occupancy.items(), key=lambda x: x[1])[0]
        best_day = datetime.strptime(best_day_str, "%Y-%m-%d").strftime("%d %b")
        col3.metric("Giorno più pieno", best_day)
