@echo off
echo Starting Sentinel Privacy Backend (Ollama Chatbot)...
start cmd /k "cd SGP_6THSEM_CHATBOT\SGP_6THSEM_CHATBOT && python rag_file.py"

echo Starting Sentinel Privacy Frontend (Streamlit Dashboard)...
start cmd /k "streamlit run app.py"

echo Both services have been launched in separate windows!
