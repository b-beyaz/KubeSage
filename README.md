KubeSage
KubeSage is a dynamic RAG (Retrieval-Augmented Generation) assistant designed to analyze Kubernetes documentation in real-time using a hybrid AI architecture.

Architecture
LLM (Cloud): claude-sonnet-4-20250514 for high-level reasoning and technical synthesis.

Embeddings (Local): nomic-embed-text via Ollama for zero-cost, local document indexing.

Framework: Built with LangChain (0.3+) and Streamlit.

Quick Start
1-Clone & Install
```bash
git clone https://github.com/b-beyaz/KubeSage.git
```
2-Configure Environment
Create a .env file in the root directory:
```bash
ANTHROPIC_API_KEY=your_key_here
CLAUDE_MODEL_NAME=claude-sonnet-4-20250514
```
3-Launch App
```bash
streamlit run main.py 
```
