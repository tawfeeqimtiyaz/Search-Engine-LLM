# 🔎 LangChain Chat with Search

A Streamlit chat app where a Groq-hosted LLM answers your questions by calling search tools. The agent decides which tool to use for each question: web search (DuckDuckGo), research papers (arXiv), or encyclopedia articles (Wikipedia).

## Features

- Chat interface built with Streamlit
- LangChain tool-calling agent (`create_openai_tools_agent`)
- Three tools:
  - **Search**: DuckDuckGo for current web results
  - **arxiv**: research paper lookup
  - **wiki**: Wikipedia summaries for general knowledge
- Live tool-call steps shown in the chat with `StreamlitCallbackHandler`
- Groq API key entered in the sidebar, never hardcoded

## Tech Stack

- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [Groq](https://groq.com/) (`openai/gpt-oss-120b`)
- DuckDuckGo, arXiv, and Wikipedia via `langchain-community`

## Project Structure

```
5-Search Engine/
├── app.py
├── requirements.txt
└── README.md
```

## Setup

1. Clone the repository and open the project folder.

2. Create and activate a virtual environment:

   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

4. Get a Groq API key from [console.groq.com/keys](https://console.groq.com/keys).

5. (Optional) Create a `.env` file in the project folder:

   ```
   GROQ_API_KEY=gsk_your_key_here
   ```

   If you skip this, paste the key into the sidebar when the app runs.

## Run

```powershell
python -m streamlit run app.py
```

Open the URL Streamlit prints (usually `http://localhost:8501`), enter your Groq API key in the sidebar, and ask a question such as "What is machine learning?" or "Summarize recent papers on retrieval-augmented generation."

## How It Works

1. The user's question goes to the LLM along with the list of tools.
2. The LLM decides whether to call a tool and with what query.
3. The tool's result goes back to the LLM, which can call more tools (up to 6 steps).
4. The final answer appears in the chat.

## Requirements

```
streamlit
python-dotenv
langchain-groq
langchain-core
langchain-classic
langchain-community
ddgs
arxiv<2.2
wikipedia
```

## Notes

- `langchain-community` shows a deprecation warning. The app still runs.
- If a tool fails (for example, network timeout), the agent receives the error message and continues.

## License

MIT