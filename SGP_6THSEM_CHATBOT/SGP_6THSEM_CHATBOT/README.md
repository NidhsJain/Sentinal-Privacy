# Mobile Privacy Risk RAG Chatbot

A locally-run, command-line chatbot designed to provide step-by-step guidance on mobile security and privacy risks. It uses a Retrieval-Augmented Generation (RAG) architecture powered by local AI models via Ollama.

## Features

- **Local RAG Architecture**: Reads security data directly from local Excel datasets and generates local embeddings. No cloud APIs are used, keeping everything private.
- **Context-Aware Logic**: Limits advice to only what is provided in the dataset.
- **Strict Response Formatting**: By default, the chatbot provides highly concise, step-by-step instructions without unnecessary theory or conversational fluff.
- **Polite Explanations on Demand**: If explicitly asked to "explain", the chatbot will shift from strict brevity to providing easy-to-understand, polite explanations. 
- **Persistent Vector Store**: Embeddings are saved into `vector_store.pkl` on the first run, allowing the chatbot to load instantly in the future without recalculating.

## Project Structure

- `rag_file.py`: The main Python script containing the RAG logic, Ollama integration, and exact chatbot interaction loop.
- `Files/`: A directory containing the source databases in `.xlsx` format (e.g., `General_Security_Practices.xlsx`, `Device_Configuration.xlsx`).
- `vector_store.pkl`: An auto-generated cache of the vector embeddings. 

## Prerequisites

1. **Python 3.8+** installed on your system.
2. **Ollama** installed and running in the background.
3. The required Ollama models pulled. Open your terminal and run:
   ```bash
   ollama pull mxbai-embed-large
   ollama pull gemma3:4b
   ```

## Setup & Execution

1. **Install Python dependencies**:
   Open a terminal in the project directory and install the required libraries:
   ```bash
   pip install pandas numpy ollama openpyxl
   ```

2. **Run the Chatbot**:
   ```bash
   python rag_file.py
   ```

3. **Interacting with the Bot**:
   - Type your question when prompted with `You:`.
   - The the **first time** you run the script, it will parse the Excel sheets and generate embeddings for about 300 rows. This takes roughly 30-60 seconds depending on your hardware.
   - On **subsequent runs**, it will instantly load `vector_store.pkl` and skip the embedding phase entirely.
   - Type `exit` to close the chatbot.

## Updating the Data
If you modify, add, or delete any of the `.xlsx` files inside the `Files/` directory, you must force the chatbot to rebuild its knowledge base.

To do this, simply delete the `vector_store.pkl` file and run `python rag_file.py` again.
