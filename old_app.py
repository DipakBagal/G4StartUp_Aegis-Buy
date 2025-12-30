import os
import streamlit as st
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from supabase import create_client, Client
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# --- INITIALIZATION ---
st.set_page_config(page_title="Aegis-Buy: AI Procurement Agent", layout="wide")
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- STATE DEFINITION ---
class AgentState(TypedDict):
    url: str
    asin: str
    urgency: int
    price_data: dict
    sentiment: str
    verdict: str
    history: List[str]

# --- TOOLS (The Agent's Hands) ---
def fetch_keepa_data(asin: str):
    """Actual API call to Keepa for historical data."""
    # Placeholder for Keepa API integration logic
    return {
        "current": 499.00,
        "90_day_avg": 420.00,
        "lowest": 380.00,
        "percentile": 85 # 85% of history was cheaper
    }

def analyze_web_sentiment(asin: str):
    """Uses Search API to find recent Reddit/Review complaints."""
    return "Recent reports of battery swelling in this batch (Dec 2025)."

# --- AGENT NODES ---
def researcher_node(state: AgentState):
    # Logic to extract ASIN from URL
    asin = state["url"].split("/dp/")[1].split("/")[0] if "/dp/" in state["url"] else "B00000"
    data = fetch_keepa_data(asin)
    return {"asin": asin, "price_data": data}

def strategist_node(state: AgentState):
    model = genai.GenerativeModel('gemini-1.5-pro')
    prompt = f"""
    Analyze as a Fiduciary Procurement Agent:
    Current Price: {state['price_data']['current']}
    90-Day Avg: {state['price_data']['avg_90_day']}
    Historical Low: {state['price_data']['lowest']}
    User Urgency: {state['urgency']}/10
    Sentiment: {state['sentiment']}
    
    Provide a 'BUY', 'WATCH', or 'WAIT' verdict and a 2-sentence strategy.
    """
    response = model.generate_content(prompt)
    return {"verdict": response.text}

# --- GRAPH CONSTRUCTION ---
builder = StateGraph(AgentState)
builder.add_node("researcher", researcher_node)
builder.add_node("strategist", strategist_node)
builder.set_entry_point("researcher")
builder.add_edge("researcher", "strategist")
builder.add_edge("strategist", END)
graph = builder.compile()

# --- STREAMLIT UI ---
st.title("🛡️ Aegis-Buy: Agentic Procurement")
st.markdown("Your private fiduciary agent for smarter Amazon shopping.")

with st.sidebar:
    st.header("User Context")
    urgency = st.slider("How badly do you need this?", 1, 10, 5)
    budget = st.number_input("Maximum Budget ($)", value=500)

product_url = st.text_input("Paste Amazon Product URL here:")

if st.button("Run Sourcing Mission"):
    with st.spinner("Agent is researching price history and sentiment..."):
        # Run the Graph
        initial_state = {"url": product_url, "urgency": urgency, "history": []}
        final_output = graph.invoke(initial_state)
        
        # Persist to Supabase
        supabase.table("missions").insert({
            "asin": final_output["asin"],
            "verdict": final_output["verdict"],
            "price_at_check": final_output["price_data"]["current"]
        }).execute()
        
        # Display Results
        st.subheader("Agent Verdict")
        st.write(final_output["verdict"])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${final_output['price_data']['current']}")
        col2.metric("90-Day Avg", f"${final_output['price_data']['avg_90_day']}")
        col3.metric("Historical Low", f"${final_output['price_data']['lowest']}")