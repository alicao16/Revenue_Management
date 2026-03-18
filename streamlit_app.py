import math
import numpy as np
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
        "april_only": "📅 Ad aprile si gioca! Imposta i prezzi ogni giorno, monitora l'occupazione e conquista la classifica. Le prenotazioni partono a marzo, ma i soggiorni sono ad aprile e maggio per simulare un hotel già operativo.",
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
        "april_only": "📅 April is game time! Set daily prices, monitor occupancy and conquer the leaderboard. Bookings begin in March but stays take place in April and May to simulate a hotel already in operation.",
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
    st.session_state.total_rooms = 50  # Valore iniziale predefinito
    st.session_state.total_revenue = 0
    st.session_state.user_id = None
    st.session_state.user_email = None
    st.session_state.user_username = None
    st.session_state.auth_tab = "login"
    
    st.session_state.prices = {}
    d = datetime(2026, 3, 1)
    while d <= datetime(2026, 5, 31):
        st.session_state.prices[d.strftime("%Y-%m-%d")] = 100
        d += timedelta(days=1)
    
    st.session_state.bookings = defaultdict(lambda: defaultdict(int))
    st.session_state.daily_occupancy = defaultdict(int)
    st.session_state.daily_revenue = defaultdict(float)
    st.session_state.daily_pickup = defaultdict(int)  # Added missing initialization
    
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

    stay_date = datetime(2026, 4, 1)

    while stay_date <= datetime(2026, 5, 31):

        if stay_date < booking_date:
            stay_date += timedelta(days=1)
            continue

        stay_str = stay_date.strftime("%Y-%m-%d")

        current_occupancy = st.session_state.daily_occupancy[stay_str]
        C = st.session_state.total_rooms
        available = C - current_occupancy

        if available <= 0:
            stay_date += timedelta(days=1)
            continue

        p = st.session_state.prices.get(stay_str, 100)
        # esempio
        if stay_date.month == 4:
            season_factor = st.session_state.season_april
        elif stay_date.month == 5:
            season_factor = st.session_state.season_may
        else:
            season_factor = 1.0

        n0 = n0 * season_factor  # applicato alla domanda di base
        # ===== PARAMETRI DOMANDA =====
        n0 = st.session_state.get("market_demand", 10)
        p0 = st.session_state.get("p0", 100)
        # ===== Sidebar: Game Controls =====
        st.subheader("📈 Demand Curve Steepness")

        alpha = st.slider(
        "Alpha (demand sensitivity to price)",
        min_value=0.01,
        max_value=0.10,
        value=st.session_state.get("alpha", 0.03),
        step=0.005,
        help="Higher alpha → demand drops faster when price increases"
)

        st.session_state.alpha = alpha
        
        C = st.session_state.total_rooms

        # ===== PREZZO DI SELL-OUT (vincolo di capacità teorico) =====
        if n0 > C:
            p_so = p0 + (1 / alpha) * math.log(n0 / C - 1)
        else:
            p_so = float("inf")

        # ===== SIGMOIDE DELLA DOMANDA =====
        sigma = 1 / (1 + math.exp(alpha * (p - p0)))

        # ===== REGIME CAPACITY CONSTRAINT & CAMPIONAMENTO =====
        sigma = 1 / (1 + math.exp(alpha * (p - p0)))
        bookings = np.random.binomial(n=n0, p=sigma)

        # Applica vincolo capacità
        bookings = min(bookings, available)

        # ===== ADVANCE BOOKING EFFECT =====
        days_before = max(1, (stay_date - booking_date).days)
        time_factor = max(0.4, min(1.0, 20 / days_before))
        bookings = int(bookings * time_factor)

        # ===== VINCOLO DI CAPACITÀ =====
        new_bookings = min(bookings, available)

        if new_bookings > 0:

            st.session_state.bookings[stay_str][booking_str] = {
                "rooms": new_bookings,
                "price": p
            }

            st.session_state.daily_occupancy[stay_str] += new_bookings

            revenue = new_bookings * p
            st.session_state.daily_revenue[stay_str] += revenue
            st.session_state.total_revenue += revenue

            st.session_state.daily_pickup[booking_str] += new_bookings

            total_new_bookings += new_bookings

        stay_date += timedelta(days=1)

    return total_new_bookings

def advance_day():
    if st.session_state.current_date <= datetime(2026, 5, 31):
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
    st.session_state.daily_pickup = defaultdict(int)  # Added missing initialization
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

    st.divider()
    st.header(t("controls"))

    rooms_value = st.number_input(
        t("total_rooms"),
        min_value=1,
        max_value=300,
        value=st.session_state.total_rooms,
        step=1,
        disabled=st.session_state.game_running,
        key="rooms_input"
    )

    st.subheader("📅 Seasonality")

    season_april = st.slider(
        "April demand",
        min_value=0.30,
        max_value=1.50,
        value=st.session_state.get("season_april", 0.70),
        step=0.1
    )

    season_may = st.slider(
        "May demand",
        min_value=0.30,
        max_value=1.50,
        value=st.session_state.get("season_may", 0.70),
        step=0.1
    )

    st.session_state.season_april = season_april
    st.session_state.season_may = season_may


    
# Aggiorna session_state solo se il valore è cambiato
if rooms_value != st.session_state.total_rooms:
        st.session_state.total_rooms = rooms_value

with st.sidebar:

    st.divider()
    st.subheader("🎮 Game")

    if st.button(t("start"), use_container_width=True, key="start_button"):
        st.session_state.game_running = True
        st.session_state.last_update = time.time()
        st.session_state.game_completed = False
        if st.session_state.paused_elapsed > 0:
            st.session_state.last_update = time.time() - st.session_state.paused_elapsed
            st.session_state.paused_elapsed = 0

    if st.button(t("next_day"), use_container_width=True, key="next_day_button"):
        if st.session_state.current_date <= datetime(2026, 5, 31):
            advance_day()
            st.rerun()
        else:
            st.session_state.game_running = False
            st.session_state.game_completed = True
            st.rerun()

    if st.button(t("reset"), use_container_width=True, key="reset_button"):
        reset_game()

st.divider()
st.subheader(t("stats"))
st.metric(t("date"), st.session_state.current_date.strftime("%d/%m/%Y"))
st.metric(t("total_revenue"), f"€{st.session_state.total_revenue:,.0f}")

st.divider()

if st.session_state.game_running:
    st.info(t("click_next_day"))
elif st.session_state.current_date == datetime(2026, 3, 1) and not st.session_state.game_completed:
    st.info(t("click_start"))

if st.session_state.game_completed and st.session_state.user_id:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(f"{t('save_score')} (€{st.session_state.total_revenue:,.0f})", use_container_width=True):
            update_user_stats(st.session_state.user_id, st.session_state.total_revenue)
            st.success(t("score_saved"))
            time.sleep(1)
            st.rerun()

# ===== CALENDARIO PREZZI =====

st.header("💰 Imposta prezzi")

giorni = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]

# mese visualizzato
if "calendar_month" not in st.session_state:
    st.session_state.calendar_month = 3  # Start with March


def change_month(delta):
    new_month = st.session_state.calendar_month + delta
    if 3 <= new_month <= 5:  # Include March, April, May
        st.session_state.calendar_month = new_month


def draw_calendar(month):
    year = 2026
    first_day = datetime(year, month, 1)

    # trova il lunedì della prima settimana
    start = first_day - timedelta(days=first_day.weekday())

    # intestazione mese con frecce
    col1, col2, col3 = st.columns([1,4,1])

    with col1:
        if st.button("⬅️", key="prev_month"):
            change_month(-1)

    with col2:
        month_names = {3: "MARZO 2026", 4: "APRILE 2026", 5: "MAGGIO 2026"}
        st.subheader(month_names.get(month, first_day.strftime("%B %Y").upper()))

    with col3:
        if st.button("➡️", key="next_month"):
            change_month(1)

    # intestazione giorni settimana
    cols = st.columns(7)
    for i, g in enumerate(giorni):
        cols[i].markdown(f"**{g}**")

    d = start

    while True:
        cols = st.columns(7)

        for i in range(7):
            with cols[i]:
                if d.month == month:
                    date_str = d.strftime("%Y-%m-%d")
                    occ = st.session_state.daily_occupancy.get(date_str, 0)
                    rooms = st.session_state.total_rooms

                    if month == 3:  # March - view only, no price input
                        st.markdown(f"**{d.day}**")
                        # Occupazione
                        if occ == 0:
                            st.caption(f"🟢 {occ}/{rooms}")
                        elif occ < rooms:
                            st.caption(f"🟡 {occ}/{rooms}")
                        else:
                            st.caption(f"🔴 {occ}/{rooms}")
                        st.caption("📅 solo pickup")
                    else:  # April & May - price input
                        price = st.number_input(
                            f"{d.day}",
                            min_value=10,
                            max_value=500,
                            step=5,
                            value=st.session_state.prices.get(date_str, 100),
                            key=f"price_{date_str}"
                        )
                        st.session_state.prices[date_str] = price

                        # occupazione
                        if occ == 0:
                            st.caption(f"🟢 {occ}/{rooms}")
                        elif occ < rooms:
                            st.caption(f"🟡 {occ}/{rooms}")
                        else:
                            st.caption(f"🔴 {occ}/{rooms}")
                else:
                    st.write("")

            d += timedelta(days=1)

        if d.month != month and d.weekday() == 0:
            break


draw_calendar(st.session_state.calendar_month)


# ===== PICKUP CHART =====
st.header("📊 Analisi Prenotazioni")

# Tabs per distinguere le due visualizzazioni
tab1, tab2 = st.tabs(["📈 Pickup Chart (cumulativo per giorno di soggiorno)", "📋 Dettaglio per data prenotazione"])

with tab1:
    st.subheader("Pickup Chart - Accumulo prenotazioni nel tempo")
    st.caption("Mostra come si accumulano le prenotazioni giorno per giorno per uno specifico giorno di soggiorno")
    
    # Raccogli tutte le date di soggiorno (aprile-maggio) che hanno prenotazioni
    stay_dates = []
    for stay_date, bookings in st.session_state.bookings.items():
        try:
            date_obj = datetime.strptime(stay_date, "%Y-%m-%d")
            if date_obj.month in [4, 5]:  # Solo aprile e maggio
                # Verifica se ci sono prenotazioni
                has_bookings = False
                if isinstance(bookings, dict):
                    for value in bookings.values():
                        if isinstance(value, dict):
                            if value.get("rooms", 0) > 0:
                                has_bookings = True
                                break
                        elif value > 0:
                            has_bookings = True
                            break
                elif bookings > 0:
                    has_bookings = True
                
                if has_bookings:
                    stay_dates.append(stay_date)
        except (ValueError, TypeError):
            continue
    
    if stay_dates:
        selected_stay = st.selectbox(
            "Seleziona giorno di soggiorno per vedere il pickup cumulativo",
            sorted(stay_dates),
            format_func=lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%d %b %Y"),
            key="stay_select"
        )
        
        if selected_stay and selected_stay in st.session_state.bookings:
            # Ottieni tutte le prenotazioni per questo giorno di soggiorno
            bookings_for_stay = st.session_state.bookings[selected_stay]
            
            # Crea dati per il pickup chart (accumulo giorno per giorno)
            pickup_data = []
            cumulative = 0
            
            if isinstance(bookings_for_stay, dict):
                # Ordina per data di prenotazione
                for book_date, data in sorted(bookings_for_stay.items()):
                    if isinstance(data, dict):
                        rooms = data.get("rooms", 0)
                    else:
                        rooms = data
                    
                    if rooms > 0:
                        cumulative += rooms
                        try:
                            book_dt = datetime.strptime(book_date, "%Y-%m-%d")
                            date_label = book_dt.strftime("%d %b")
                        except:
                            date_label = book_date
                        
                        pickup_data.append({
                            "Data prenotazione": date_label,
                            "Pick-up giornaliero": rooms,
                            "Pick-up cumulativo": cumulative
                        })
            
            if pickup_data:
                df_pickup = pd.DataFrame(pickup_data)
                
                # Spiegazione del concetto di pickup con esempio
                with st.expander("📘 Cos'è il Pick-up?"):
                    st.markdown("""
                    **Pick-up giornaliero**: Nuove prenotazioni arrivate in una specifica data per questo giorno di soggiorno
                    
                    **Pick-up cumulativo**: Totale prenotazioni accumulate fino a quella data per questo giorno di soggiorno
                    
                    **Esempio pratico per il giorno di soggiorno del 10 aprile**:
                    - **1 marzo**: 5 camere prenotate → pick-up giornaliero = 5, cumulativo = 5
                    - **2 marzo**: 3 camere prenotate → pick-up giornaliero = 3, cumulativo = 8
                    - **5 marzo**: 2 camere prenotate → pick-up giornaliero = 2, cumulativo = 10
                    
                    Il grafico mostra come si riempie l'hotel nel tempo per uno specifico giorno di arrivo.
                    """)
                
                # Mostra il grafico del pickup cumulativo
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader(f"Pick-up cumulativo per il {datetime.strptime(selected_stay, '%Y-%m-%d').strftime('%d %b %Y')}")
                    st.line_chart(df_pickup.set_index("Data prenotazione")[["Pick-up cumulativo"]])
                    
                    # Aggiungi anche un grafico a barre del pickup giornaliero
                    st.subheader("Pick-up giornaliero")
                    st.bar_chart(df_pickup.set_index("Data prenotazione")[["Pick-up giornaliero"]])
                
                with col2:
                    # Metriche riassuntive
                    total_rooms = df_pickup["Pick-up giornaliero"].sum()
                    first_booking = df_pickup.iloc[0]["Data prenotazione"] if not df_pickup.empty else "N/A"
                    last_booking = df_pickup.iloc[-1]["Data prenotazione"] if not df_pickup.empty else "N/A"
                    peak_day = df_pickup.loc[df_pickup["Pick-up giornaliero"].idxmax(), "Data prenotazione"] if not df_pickup.empty else "N/A"
                    peak_value = df_pickup["Pick-up giornaliero"].max() if not df_pickup.empty else 0
                    
                    st.metric("🏨 Totale camere prenotate", f"{total_rooms}")
                    st.metric("📅 Prima prenotazione", first_booking)
                    st.metric("📅 Ultima prenotazione", last_booking)
                    st.metric("📈 Giorno con più pickup", f"{peak_day} ({peak_value} camere)")
                
                # Mostra tabella dettagli con i pickup giornalieri
                st.subheader("Dettaglio pickup giornaliero")
                st.dataframe(df_pickup, use_container_width=True, hide_index=True)
                
                # Calcola revenue totale per questo giorno
                total_rev = 0
                if isinstance(bookings_for_stay, dict):
                    for data in bookings_for_stay.values():
                        if isinstance(data, dict):
                            rooms = data.get("rooms", 0)
                            price = data.get("price", st.session_state.prices.get(selected_stay, 100))
                            total_rev += rooms * price
                        else:
                            # Se è un intero, usa il prezzo corrente
                            rooms = data
                            price = st.session_state.prices.get(selected_stay, 100)
                            total_rev += rooms * price
                
                st.metric("💰 Revenue totale per questo giorno di soggiorno", f"€{total_rev:,.0f}")
            else:
                st.info(f"Nessun dato di pickup per il {datetime.strptime(selected_stay, '%Y-%m-%d').strftime('%d %b %Y')}")
    else:
        st.info("Nessuna prenotazione registrata per aprile o maggio")

with tab2:
    st.subheader("Dettaglio prenotazioni per data di prenotazione")
    st.caption("Mostra tutte le prenotazioni fatte in una specifica data PER soggiorni futuri (aprile-maggio)")
    
    # Usa lo STESSO mese selezionato nel calendario "Imposta prezzi"
    selected_month = st.session_state.calendar_month
    
    # Raccogli tutte le date di prenotazione (quando è stata fatta la prenotazione)
    booking_dates = set()
    for stay_date, bookings in st.session_state.bookings.items():
        if isinstance(bookings, dict):
            for booking_date in bookings.keys():
                try:
                    booking_dt = datetime.strptime(booking_date, "%Y-%m-%d")
                    if booking_dt.month == selected_month:
                        booking_dates.add(booking_date)
                except (ValueError, TypeError):
                    continue
    
    booking_dates = sorted(list(booking_dates))
    
    if booking_dates:
        selected_booking_date = st.selectbox(
            "Seleziona data di prenotazione",
            booking_dates,
            format_func=lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%d %b %Y"),
            key="booking_select"
        )
        
        if selected_booking_date:
            st.markdown(f"**Prenotazioni ricevute il {datetime.strptime(selected_booking_date, '%Y-%m-%d').strftime('%d %b %Y')}**")
            
            # Trova tutte le prenotazioni fatte in questa data per soggiorni futuri
            future_stays = []
            total_rooms_booked = 0
            total_revenue_day = 0
            
            for stay_date, bookings in st.session_state.bookings.items():
                if isinstance(bookings, dict) and selected_booking_date in bookings:
                    data = bookings[selected_booking_date]
                    
                    if isinstance(data, dict):
                        rooms = data.get("rooms", 0)
                        price = data.get("price", st.session_state.prices.get(stay_date, 100))
                    else:
                        rooms = data
                        price = st.session_state.prices.get(stay_date, 100)
                    
                    if rooms > 0:
                        revenue = rooms * price
                        total_rooms_booked += rooms
                        total_revenue_day += revenue
                        
                        try:
                            stay_dt = datetime.strptime(stay_date, "%Y-%m-%d")
                            booking_dt = datetime.strptime(selected_booking_date, "%Y-%m-%d")
                            days_before = (stay_dt - booking_dt).days
                            stay_formatted = stay_dt.strftime("%d %b %Y")
                        except (ValueError, TypeError):
                            days_before = "N/A"
                            stay_formatted = stay_date
                        
                        future_stays.append({
                            "Data soggiorno": stay_formatted,
                            "Giorni dopo": days_before,
                            "Camere": rooms,
                            "Prezzo": f"€{price}",
                            "Revenue": f"€{revenue:,.0f}"
                        })
            
            if future_stays:
                # Mostra tabella dettagli
                st.dataframe(pd.DataFrame(future_stays), use_container_width=True, hide_index=True)
                
                # Metriche riassuntive
                col1, col2, col3 = st.columns(3)
                col1.metric("📊 Totale camere prenotate in questo giorno", f"{total_rooms_booked}")
                col2.metric("💰 Revenue generato in questo giorno", f"€{total_revenue_day:,.0f}")
                col3.metric("🏨 Soggiorni futuri prenotati", len(future_stays))
            else:
                st.info(f"Nessuna prenotazione trovata per il {datetime.strptime(selected_booking_date, '%Y-%m-%d').strftime('%d %b %Y')}")
    else:
        month_names = {3: "marzo", 4: "aprile", 5: "maggio"}
        st.info(f"Nessuna prenotazione registrata a {month_names.get(selected_month, '')} {datetime(2026, selected_month, 1).strftime('%Y')}")

st.divider()

st.header(t("current_state"))

total_occ = sum(st.session_state.daily_occupancy.values())
max_possible = st.session_state.total_rooms * 61  # Solo aprile ha 30 giorni
occupancy_percentage = (total_occ / max_possible * 100) if max_possible > 0 else 0

if st.session_state.current_date <= datetime(2026, 5, 31):
    days_left = (datetime(2026, 5, 31) - st.session_state.current_date).days
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

start_date = datetime(2026, 3, 1)
end_date = datetime(2026, 5, 31)

total_days = (end_date - start_date).days + 1  # Include il 1 marzo e il 31 maggio
days_passed = (st.session_state.current_date - start_date).days + 1

progress = min(1, days_passed / total_days)

st.progress(progress, text=f"Avanzamento: {days_passed}/{total_days} giorni")
if total_occ > 0:
    st.caption(f"📊 {total_occ} camere prenotate su {max_possible} disponibili in aprile")

if st.session_state.current_date > datetime(2026, 5, 31):
    st.balloons()
    st.success(t("game_end").format(revenue=st.session_state.total_revenue))
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Occupazione media aprile", f"{occupancy_percentage:.1f}%")
    
    avg_price = st.session_state.total_revenue / total_occ if total_occ > 0 else 0
    col2.metric("Prezzo medio", f"€{avg_price:.0f}")
    
    if st.session_state.daily_occupancy:
        # Trova il giorno con più prenotazioni solo in aprile
        april_occupancy = {date: occ for date, occ in st.session_state.daily_occupancy.items() 
                          if datetime.strptime(date, "%Y-%m-%d").month == 4}
        if april_occupancy:
            best_day_str = max(april_occupancy.items(), key=lambda x: x[1])[0]
            best_day = datetime.strptime(best_day_str, "%Y-%m-%d").strftime("%d %b")
            col3.metric("Giorno più pieno di aprile", best_day)
