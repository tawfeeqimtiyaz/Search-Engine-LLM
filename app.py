import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.utilities import ArxivAPIWrapper, WikipediaAPIWrapper
from langchain_community.tools import ArxivQueryRun, DuckDuckGoSearchRun
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_classic.agents import create_openai_tools_agent, AgentExecutor

load_dotenv()

## Tools
arxiv = ArxivQueryRun(api_wrapper=ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=1500))

@tool
def arxiv(query: str) -> str:
    """Search arXiv for research papers. Input is a search query string."""
    try:
        return _arxiv.run(query)
    except Exception as e:
        return f"Arxiv lookup failed: {e}"
    
search = DuckDuckGoSearchRun(name="Search")

_wiki = WikipediaAPIWrapper(top_k_results=2, doc_content_chars_max=1500)

@tool
def wiki(query: str) -> str:
    """Search Wikipedia for general knowledge."""
    try:
        return _wiki.run(query)
    except Exception as e:
        return f"Wikipedia lookup failed: {e}"

tools = [search, arxiv, wiki]

## UI
st.title("🔎 LangChain - Chat with search")
st.write("Ask a question. The agent searches DuckDuckGo, Arxiv, and Wikipedia.")

st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

prompt_text = st.chat_input(placeholder="What is machine learning?")

if prompt_text:
    if not api_key:
        st.warning("Enter your Groq API key in the sidebar first.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt_text})
    st.chat_message("user").write(prompt_text)

    llm = ChatGroq(groq_api_key=api_key, model_name="openai/gpt-oss-120b")

    agent_prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful research assistant. Use the tools when needed and answer clearly."),
        ("human", "{input}"),
        MessagesPlaceholder("agent_scratchpad"),
    ])

    agent = create_openai_tools_agent(llm, tools, agent_prompt)
    executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, max_iterations=6,
    early_stopping_method="force",)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        result = executor.invoke({"input": prompt_text}, config={"callbacks": [st_cb]})
        answer = result["output"]
        st.write(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})