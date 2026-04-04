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
from pathlib import Path
import sys

# ===== SUPABASE SETUP =====


from supabase import create_client, Client

@st.cache_resource
def get_supabase_client() -> Client:
    import os

    url = os.getenv("SUPABASE_URL", "https://drvaaneglmpjelqfmget.supabase.co")
    key = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRydmFhbmVnbG1wamVscWZtZ2V0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzUxNDIxOTAsImV4cCI6MjA5MDcxODE5MH0.FysY6cJ3KOYCwsYhP2GZtIgziaSVAe7ZqtBg7bEoAmQ")

    return create_client(url, key)
    
def supabase() -> Client:
    return get_supabase_client()

# ===== CONFIGURAZIONE =====
st.set_page_config(layout="wide")

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
        "score_value": "Punteggio",
        "next_day": "⏭️ Avanti (Prossimo Giorno)",
        "pickup": "📈 Pick‑up prenotazioni",
        "pickup_explanation": "Mostra come si accumulano le prenotazioni giorno per giorno per uno specifico giorno di soggiorno",
        "booking_explanation": "Mostra tutte le prenotazioni fatte in una specifica data per soggiorni futuri (aprile)",
        "no_bookings_month": "Nessuna prenotazione registrata ad aprile 2026",
        "progress_label": "Avanzamento",
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
        "set_prices": "💰 Set Prices (April)",
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
        "score_value": "Score",
        "next_day": "⏭️ Next Day",
        "pickup": "📈 Booking pick-up",
        "pickup_explanation": "Shows how bookings accumulate day by day for a specific stay date",
        "booking_explanation": "Shows all bookings made on a specific date for future stays (April)",
        "no_bookings_month": "No bookings recorded in April 2026",
        "progress_label": "Progress",
    }
}

def t(key):
    lang = st.session_state.get("language", "it")
    return TRANSLATIONS.get(lang, TRANSLATIONS["it"]).get(key, key)

# ===== DATABASE FUNCTIONS (Supabase) =====

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def _parse_dt(value) -> datetime | None:
    """Parse ISO timestamp string returned by Supabase into a datetime."""
    if not value:
        return None
    try:
        # Supabase returns ISO 8601, e.g. "2026-03-01T12:34:56.789+00:00"
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).replace(tzinfo=None)
    except Exception:
        return None

def get_user_by_email(email: str):
    try:
        res = supabase().table("users").select("*").eq("email", email).maybe_single().execute()
        return res.data
    except Exception as e:
        st.error(f"DB error: {e}")
        return None

def get_user_by_identifier(identifier: str):
    """Lookup by email OR username."""
    try:
        res = (
            supabase()
            .table("users")
            .select("*")
            .or_(f"email.eq.{identifier},username.eq.{identifier}")
            .maybe_single()
            .execute()
        )
        return res.data
    except Exception as e:
        st.error(f"DB error: {e}")
        return None

def get_user_by_id(user_id: int):
    try:
        res = supabase().table("users").select("*").eq("id", user_id).maybe_single().execute()
        return res.data
    except Exception as e:
        st.error(f"DB error: {e}")
        return None

def create_user(email: str, username: str, password: str):
    """Returns the new user id, or None on conflict."""
    try:
        res = (
            supabase()
            .table("users")
            .insert({
                "email": email,
                "username": username,
                "password": hash_password(password),
                "created_at": datetime.utcnow().isoformat(),
                "last_login": datetime.utcnow().isoformat(),
            })
            .execute()
        )
        return res.data[0]["id"] if res.data else None
    except Exception:
        # Unique constraint violation → email/username already taken
        return None

def update_user_login(email: str):
    try:
        supabase().table("users").update({"last_login": datetime.utcnow().isoformat()}).eq("email", email).execute()
    except Exception as e:
        st.error(f"DB error: {e}")

def update_user_stats(user_id: int, score: int):
    try:
        # Fetch current best
        res = supabase().table("users").select("best_score").eq("id", user_id).maybe_single().execute()
        current_best = res.data["best_score"] if res.data else 0

        update_payload = {
            "games_played": None,   # incremented via RPC below
            "last_game": datetime.utcnow().isoformat(),
        }
        if score > (current_best or 0):
            update_payload["best_score"] = score

        # games_played++ — Supabase doesn't support field increments via the REST client
        # directly, so we read and write.
        games_res = supabase().table("users").select("games_played").eq("id", user_id).maybe_single().execute()
        games_played = (games_res.data["games_played"] or 0) + 1
        update_payload["games_played"] = games_played

        supabase().table("users").update(update_payload).eq("id", user_id).execute()

        # Insert score record
        supabase().table("scores").insert({"user_id": user_id, "score": score}).execute()
    except Exception as e:
        st.error(f"DB error: {e}")

def get_user_scores(user_id: int, limit: int = 10):
    """Returns list of (score, created_at_str) tuples."""
    try:
        res = (
            supabase()
            .table("scores")
            .select("score, created_at")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
        return [(row["score"], row["created_at"]) for row in (res.data or [])]
    except Exception as e:
        st.error(f"DB error: {e}")
        return []

def get_leaderboard(limit: int = 10):
    """Returns list of (username, best_score) tuples ordered by best_score desc."""
    try:
        res = (
            supabase()
            .table("users")
            .select("username, best_score")
            .order("best_score", desc=True)
            .limit(limit)
            .execute()
        )
        return [(row["username"], row["best_score"]) for row in (res.data or [])]
    except Exception as e:
        st.error(f"DB error: {e}")
        return []

def get_user_stats(user_id: int):
    """Returns (username, email, best_score, games_played, created_at, last_game) or None."""
    try:
        res = (
            supabase()
            .table("users")
            .select("username, email, best_score, games_played, created_at, last_game")
            .eq("id", user_id)
            .maybe_single()
            .execute()
        )
        if not res.data:
            return None
        d = res.data
        return (d["username"], d["email"], d["best_score"], d["games_played"], d["created_at"], d["last_game"])
    except Exception as e:
        st.error(f"DB error: {e}")
        return None

# ===== LOGIN UI =====
def show_login_ui():
    with st.sidebar:
        st.divider()
        st.subheader(t("login"))

        if "user_id" not in st.session_state:
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.session_state.user_username = None
            st.session_state.auth_tab = "login"

        if st.session_state.user_id is None:
            col_login, col_register = st.columns(2)
            if col_login.button(t("login_tab"), use_container_width=True):
                st.session_state.auth_tab = "login"
            if col_register.button(t("register_tab"), use_container_width=True):
                st.session_state.auth_tab = "register"

            if st.session_state.auth_tab == "login":
                identifier = st.text_input(t("login_identifier"), key="login_identifier", placeholder=t("email_placeholder"))
                password = st.text_input(t("password"), type="password", key="login_password", placeholder=t("password_placeholder"))

                if st.button(t("login_button"), use_container_width=True):
                    if identifier and password:
                        user = get_user_by_identifier(identifier)
                        if user and user["password"] == hash_password(password):
                            st.session_state.user_id = user["id"]
                            st.session_state.user_email = user["email"]
                            st.session_state.user_username = user["username"]
                            update_user_login(user["email"])
                            st.success(f"{t('welcome')}, {user['username']}!")
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
                    elif "@" not in reg_email:
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
                st.session_state.best_score = best_score or 0
                st.session_state.games_played = games_played or 0
                st.session_state.user_email = email
                st.session_state.created_at = created_at
                st.session_state.last_game = last_game

                col1, col2 = st.columns(2)
                with col1:
                    st.metric(t("best_score"), f"€{st.session_state.get('best_score', 0):,.0f}")
                with col2:
                    st.metric(t("games_played"), st.session_state.get("games_played", 0))

                st.caption(f"📧 {st.session_state.get('user_email', '')}")
                created_dt = _parse_dt(st.session_state.get("created_at"))
                if created_dt:
                    st.caption(f"{t('member_since')}: {created_dt.strftime('%d/%m/%Y')}")
                last_game_dt = _parse_dt(st.session_state.get("last_game"))
                if last_game_dt:
                    st.caption(f"{t('last_game')}: {last_game_dt.strftime('%d/%m/%Y %H:%M')}")

                st.divider()
                st.subheader(t("my_scores"))
                scores = get_user_scores(st.session_state.user_id, 5)
                if scores:
                    scores_data = []
                    for score, date in scores:
                        dt = _parse_dt(date)
                        scores_data.append({
                            t("date"): dt.strftime("%d/%m/%Y %H:%M") if dt else date,
                            t("score_value"): f"€{score:,.0f}",
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
                t("rank"): i,
                t("player"): username,
                t("score"): f"€{best_score:,.0f}",
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
    st.session_state.total_rooms = 50
    st.session_state.total_revenue = 0
    st.session_state.user_id = None
    st.session_state.user_email = None
    st.session_state.user_username = None
    st.session_state.auth_tab = "login"

    st.session_state.prices = {}
    d = datetime(2026, 4, 1)
    while d <= datetime(2026, 4, 30):
        st.session_state.prices[d.strftime("%Y-%m-%d")] = 100
        d += timedelta(days=1)

    st.session_state.bookings = defaultdict(lambda: defaultdict(int))
    st.session_state.daily_occupancy = defaultdict(int)
    st.session_state.daily_revenue = defaultdict(float)
    st.session_state.daily_pickup = defaultdict(int)

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

    while stay_date <= datetime(2026, 4, 30):

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

        season_factor = st.session_state.season_april

        n0 = st.session_state.get("market_demand", 5)
        p0 = st.session_state.get("p0", 100)
        alpha = st.session_state.get("alpha", 0.12)
        C = st.session_state.total_rooms

        n0 = n0 * season_factor

        if n0 > C:
            p_so = p0 + (1 / alpha) * math.log(n0 / C - 1)
        else:
            p_so = float("inf")

        sigma = 1 / (1 + math.exp(alpha * (p - p0)))
        bookings = np.random.binomial(n=n0, p=sigma)
        bookings = min(bookings, available)

        days_before = max(1, (stay_date - booking_date).days)
        time_factor = max(0.4, min(1.0, 20 / days_before))
        bookings = int(bookings * time_factor)

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
    st.session_state.daily_pickup = defaultdict(int)
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
    if rooms_value != st.session_state.total_rooms:
        st.session_state.total_rooms = rooms_value

    st.divider()
    st.subheader("📈 Demand Curve Steepness")
    alpha = st.slider(
        "Alpha (demand sensitivity to price)",
        min_value=0.01,
        max_value=0.20,
        value=st.session_state.get("alpha", 0.12),
        step=0.005,
        help="Higher alpha → demand drops faster when price increases"
    )
    st.session_state.alpha = alpha

    st.divider()
    st.subheader("📅 Seasonality")
    season_april = st.slider(
        "April demand",
        min_value=0.30,
        max_value=1.50,
        value=st.session_state.get("season_april", 0.6),
        step=0.05
    )
    st.session_state.season_april = season_april

    st.divider()
    st.subheader("🎮 Game Controls")
    if st.button(t("start"), use_container_width=True):
        st.session_state.game_running = True
        st.session_state.last_update = time.time()
        st.session_state.game_completed = False
        if st.session_state.paused_elapsed > 0:
            st.session_state.last_update = time.time() - st.session_state.paused_elapsed
            st.session_state.paused_elapsed = 0

    if st.button(t("next_day"), use_container_width=True):
        if st.session_state.current_date <= datetime(2026, 4, 30):
            advance_day()
            st.rerun()
        else:
            st.session_state.game_running = False
            st.session_state.game_completed = True
            st.rerun()

    if st.button(t("reset"), use_container_width=True):
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
            update_user_stats(st.session_state.user_id, int(st.session_state.total_revenue))
            st.success(t("score_saved"))
            time.sleep(1)
            st.rerun()

# ===== CALENDARIO PREZZI =====
st.header("💰 Imposta prezzi")

giorni = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]

if "calendar_month" not in st.session_state:
    st.session_state.calendar_month = 4


def draw_calendar(month):
    year = 2026
    first_day = datetime(year, month, 1)
    start = first_day - timedelta(days=first_day.weekday())

    st.subheader("🌸 APRILE 2026")

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

                    price = st.number_input(
                        f"{d.day}",
                        min_value=10,
                        max_value=500,
                        step=5,
                        value=st.session_state.prices.get(date_str, 100),
                        key=f"price_{date_str}"
                    )
                    st.session_state.prices[date_str] = price

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


draw_calendar(4)

# ===== PICKUP CHART =====
st.header("📊 Analisi Prenotazioni")

tab1, tab2 = st.tabs(["📈 Pickup Chart (cumulativo per giorno di soggiorno)", "📋 Dettaglio per data prenotazione"])

with tab1:
    st.subheader("Pickup Chart - Accumulo prenotazioni nel tempo")
    st.caption(t("pickup_explanation"))

    stay_dates = []
    for stay_date, bookings in st.session_state.bookings.items():
        try:
            date_obj = datetime.strptime(stay_date, "%Y-%m-%d")
            if date_obj.month == 4:
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
            sorted(stay_dates, key=lambda x: datetime.strptime(x, "%Y-%m-%d")),
            format_func=lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%d %b %Y"),
            key="stay_select"
        )

        if selected_stay and selected_stay in st.session_state.bookings:
            bookings_for_stay = st.session_state.bookings[selected_stay]

            pickup_data = []
            cumulative = 0

            if isinstance(bookings_for_stay, dict):
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
                        except Exception:
                            book_dt = None
                            date_label = book_date

                        pickup_data.append({
                            "Data prenotazione": date_label,
                            "Data prenotazione_dt": book_dt,
                            "Pick-up giornaliero": rooms,
                            "Pick-up cumulativo": cumulative
                        })

            if pickup_data:
                df_pickup = pd.DataFrame(pickup_data)
                df_pickup = df_pickup.dropna(subset=["Data prenotazione_dt"])
                df_pickup.set_index("Data prenotazione_dt", inplace=True)
                df_pickup.sort_index(inplace=True)

                with st.expander("📘 Cos'è il Pick-up?"):
                    st.markdown("Il **pick-up** misura quante prenotazioni si accumulano nel tempo per un dato giorno di soggiorno. Utile per capire quando i clienti prenotano e regolare i prezzi di conseguenza.")

                col1, col2 = st.columns([2, 1])
                with col1:
                    st.subheader("Pick-up cumulativo per la data di soggiorno selezionata")
                    st.line_chart(df_pickup[["Pick-up cumulativo"]])
                    st.subheader("Pick-up giornaliero")
                    st.bar_chart(df_pickup[["Pick-up giornaliero"]])

                with col2:
                    if not df_pickup.empty:
                        total_rooms_stat = df_pickup["Pick-up giornaliero"].sum()
                        first_booking = df_pickup.index.min().strftime("%d %b")
                        last_booking = df_pickup.index.max().strftime("%d %b")
                        peak_idx = df_pickup["Pick-up giornaliero"].idxmax()
                        peak_day = peak_idx.strftime("%d %b")
                        peak_value = df_pickup.loc[peak_idx, "Pick-up giornaliero"]
                        st.metric("🏨 Totale camere prenotate", f"{total_rooms_stat}")
                        st.metric("📅 Prima prenotazione", first_booking)
                        st.metric("📅 Ultima prenotazione", last_booking)
                        st.metric("📈 Giorno con più pickup", f"{peak_day} ({peak_value} camere)")

                st.subheader("Dettaglio pickup giornaliero")
                st.dataframe(df_pickup[["Data prenotazione", "Pick-up giornaliero", "Pick-up cumulativo"]], use_container_width=True, hide_index=True)

            total_rev = 0
            if isinstance(bookings_for_stay, dict):
                for data in bookings_for_stay.values():
                    if isinstance(data, dict):
                        rooms = data.get("rooms", 0)
                        price = data.get("price", st.session_state.prices.get(selected_stay, 100))
                    else:
                        rooms = data
                        price = st.session_state.prices.get(selected_stay, 100)
                    total_rev += rooms * price
                st.metric("💰 Revenue totale per questo giorno di soggiorno", f"€{total_rev:,.0f}")

with tab2:
    st.subheader("Dettaglio prenotazioni per data di prenotazione")
    st.caption(t("booking_explanation"))

    selected_month = st.session_state.calendar_month

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
                            booking_dt_obj = datetime.strptime(selected_booking_date, "%Y-%m-%d")
                            days_before = (stay_dt - booking_dt_obj).days
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
                st.dataframe(pd.DataFrame(future_stays), use_container_width=True, hide_index=True)
                col1, col2, col3 = st.columns(3)
                col1.metric("📊 Totale camere prenotate in questo giorno", f"{total_rooms_booked}")
                col2.metric("💰 Revenue generato in questo giorno", f"€{total_revenue_day:,.0f}")
                col3.metric("🏨 Soggiorni futuri prenotati", len(future_stays))
            else:
                st.info(f"Nessuna prenotazione trovata per il {datetime.strptime(selected_booking_date, '%Y-%m-%d').strftime('%d %b %Y')}")
    else:
        st.info(t("no_bookings_month"))

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

start_date = datetime(2026, 3, 1)
end_date = datetime(2026, 4, 30)
total_days = (end_date - start_date).days + 1
days_passed = (st.session_state.current_date - start_date).days + 1
progress = min(1, days_passed / total_days)

st.progress(progress, text=f"{t('progress_label')}: {days_passed}/{total_days} giorni")
if total_occ > 0:
    st.caption(f"📊 {total_occ} camere prenotate su {max_possible} disponibili in aprile")

if st.session_state.current_date > datetime(2026, 4, 30):
    st.balloons()
    st.success(t("game_end").format(revenue=st.session_state.total_revenue))

# ===== Aggiorna automaticamente il best score se l'utente è loggato =====
if st.session_state.user_id:
    user_stats = get_user_stats(st.session_state.user_id)
    if user_stats:
        username, email, best_score, games_played, created_at, last_game = user_stats
        st.session_state.best_score = best_score
        st.session_state.games_played = games_played
        st.session_state.user_email = email
        st.session_state.created_at = created_at
        st.session_state.last_game = last_game
        if st.session_state.total_revenue > best_score:
            update_user_stats(st.session_state.user_id, st.session_state.total_revenue)
            st.success(f"🎉 Nuovo record! Best score aggiornato a €{st.session_state.total_revenue:,.0f}")

# ===== Mostra le metriche finali =====
col1, col2, col3 = st.columns(3)
col1.metric("Occupazione media aprile", f"{occupancy_percentage:.1f}%")

avg_price = st.session_state.total_revenue / total_occ if total_occ > 0 else 0
col2.metric("Prezzo medio", f"€{avg_price:.0f}")

if st.session_state.daily_occupancy:
    april_occupancy = {
        date: occ
        for date, occ in st.session_state.daily_occupancy.items()
        if datetime.strptime(date, "%Y-%m-%d").month == 4
    }
    if april_occupancy:
        best_day_str = max(april_occupancy.items(), key=lambda x: x[1])[0]
        best_day = datetime.strptime(best_day_str, "%Y-%m-%d").strftime("%d %b")
        col3.metric("Giorno più pieno di aprile", best_day)

# ===== LEADERBOARD =====
st.divider()
show_leaderboard()
