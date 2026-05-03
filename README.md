# KubeSage

KubeSage is a dynamic RAG (Retrieval-Augmented Generation) assistant designed to analyze Kubernetes documentation in real-time using a hybrid AI architecture.

## Architecture

- **LLM (Cloud):** `claude-sonnet-4-20250514` for high-level reasoning and technical synthesis.
- **Embeddings (Local):** `nomic-embed-text` via Ollama for zero-cost, local document indexing.
- **Framework:** Built with LangChain (0.3+) and Streamlit.

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/b-beyaz/KubeSage.git
cd KubeSage
```

### 2. Configure Environment

Create a `.env` file in the root directory:

```env
ANTHROPIC_API_KEY=your_key_here
MODEL_NAME=claude-sonnet-4-20250514
```

### 3. Launch with Docker (Recommended)

```bash
docker compose up --build
```

This will:
- Start the **Ollama** service and expose it on port `11435`
- Automatically pull the `nomic-embed-text` embedding model via `ollama-init`
- Launch the **Streamlit** app on [http://localhost:8501](http://localhost:8501) once the model is ready

> **Note:** The first run may take a few minutes while the `nomic-embed-text` model is being downloaded.

### 4. Launch Locally (Without Docker)

Requires [Ollama](https://ollama.com) installed and running locally:

```bash
ollama pull nomic-embed-text
pip install -r requirements.txt
streamlit run main.py
```

## Services

| Service        | Description                              | Port  |
|----------------|------------------------------------------|-------|
| `streamlit-app`| Main chat UI                             | 8501  |
| `ollama`       | Local embedding model server             | 11435 |
| `ollama-init`  | One-time init container to pull model    | —     |