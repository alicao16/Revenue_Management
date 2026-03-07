#!/bin/bash
echo "🚀 Avvio servizi Streamlit..."

# Avvia sulla porta 8501
nohup streamlit run streamlit_app.py --server.port 8501 --server.enableCORS false --server.enableXsrfProtection false > streamlit_8501.log 2>&1 &
echo "✅ Streamlit su porta 8501 avviato (PID: $!)"

# Avvia sulla porta 8505
nohup streamlit run streamlit_app.py --server.port 8505 --server.enableCORS false --server.enableXsrfProtection false > streamlit_8505.log 2>&1 &
echo "✅ Streamlit su porta 8505 avviato (PID: $!)"

echo ""
echo "📊 Per vedere i log:"
echo "   tail -f streamlit_8501.log"
echo "   tail -f streamlit_8505.log"
echo ""
echo "🛑 Per fermare i servizi:"
echo "   pkill -f streamlit"
