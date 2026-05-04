# 🔐 Sentinel Privacy – AI-Driven Privacy Risk Analysis & Advisory System

Sentinel Privacy is a Streamlit-based web application powered by a local **Ollama LLM + RAG chatbot** that analyzes user privacy risks and provides actionable recommendations.

---

## 🚀 Features

* 📊 Privacy Risk Dashboard
* 🤖 AI Chatbot (RAG-based using Ollama)
* 📁 Excel-based knowledge ingestion
* 🔍 Personalized privacy recommendations

---

## 🧰 Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python (RAG-based chatbot)
* **LLM:** Ollama (`gemma3:4b`)
* **Embeddings:** `mxbai-embed-large`

---

## ⚙️ Prerequisites

Make sure you have installed:

* Python 3.9 or above
* Git
* Ollama → https://ollama.com

---

## 🧠 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/NidhsJain/Sentinal-Privacy.git
cd Sentinal-Privacy
```

---

### 2. Create & Activate Virtual Environment (Recommended)

```bash
python -m venv antigravity
antigravity\Scripts\activate   # Windows
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install pandas numpy ollama openpyxl fastapi uvicorn
```

---

### 4. Setup Ollama Models

```bash
ollama pull gemma3:4b
ollama pull mxbai-embed-large
```

👉 Make sure Ollama is running in the background.

---

### 5. Setup Environment Variables

Create a `.env` file from template:

```bash
copy .env.example .env
```

Edit `.env` and add values:

```env
OLLAMA_MODEL=gemma3:4b
BASE_URL=http://localhost:8000
```

---

## ▶️ Running the Project

### 🔹 Option 1: One-click Run (Recommended)

```bash
run_all.bat
```

---

### 🔹 Option 2: Manual Run

#### Step 1: Start Backend (RAG Chatbot)

```bash
cd SGP_6THSEM_CHATBOT\SGP_6THSEM_CHATBOT
python rag_file.py
```

---

#### Step 2: Start Frontend (New Terminal)

```bash
streamlit run app.py
```

---

## 🌐 Access the Application

* Streamlit UI → http://localhost:8501 *(default)*
* Backend API → http://localhost:8000 *(default, if used)*

⚠️ If ports are busy, they may change (check terminal output).

---

## ⚠️ Important Notes

* First run may take time (embedding generation)
* If Excel files are updated, delete:

```bash
vector_store.pkl
```

* Do NOT upload `.env` (contains sensitive data)

---

## 📁 Project Structure

```
Sentinal-Privacy/
│
├── SGP_6THSEM_CHATBOT/
├── pages/
├── utils/
├── data/
├── app.py
├── run_all.bat
├── requirements.txt
├── .env.example
└── README.md
```

---

## 👨‍💻 Author

**Nidhi Jain**

---

## 📌 Future Improvements

* Convert backend to FastAPI API service
* Improve UI/UX
* Add cloud deployment

---

## ⭐ If you found this useful, consider starring the repo!
