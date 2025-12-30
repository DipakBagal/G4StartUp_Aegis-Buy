import os
import streamlit as st
import requests
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from supabase import create_client, Client
import google.generativeai as genai
from dotenv import load_dotenv

# --- AUTH & CONFIG ---
load_dotenv()
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- STATE DEFINITION ---
class AgentState(TypedDict):
    url: str
    asin: str
    urgency: int
    data: dict
    sentiment: str
    verdict: str

# --- TOOLS (Real-time Data Links) ---
def get_keepa_data(asin: str):
    """Placeholder for Keepa API: https://keepa.com/#!api"""
    # Real implementation would use: requests.get(f"https://api.keepa.com/product?key={KEY}&asin={asin}")
    return {"current": 499, "avg_90": 425, "low": 399}

def get_web_sentiment(asin: str):
    """Placeholder for SerpAPI search for recent product issues."""
    return "Consensus: Battery life is excellent, but avoid 'Used-Like New' warehouse deals."

# --- AGENT NODES ---
def research_node(state: AgentState):
    asin = state["url"].split("/dp/")[1].split("/")[0] if "/dp/" in state["url"] else "B00000"
    return {"asin": asin, "data": get_keepa_data(asin), "sentiment": get_web_sentiment(asin)}

def strategist_node(state: AgentState):
    model = genai.GenerativeModel('gemini-1.5-pro')
    prompt = f"Price: {state['data']}. Urgency: {state['urgency']}. Sentiment: {state['sentiment']}. Strategy?"
    response = model.generate_content(prompt)
    return {"verdict": response.text}

# --- GRAPH BUILDER ---
workflow = StateGraph(AgentState)
workflow.add_node("research", research_node)
workflow.add_node("strategist", strategist_node)
workflow.set_entry_point("research")
workflow.add_edge("research", "strategist")
workflow.add_edge("strategist", END)
compiled_agent = workflow.compile()

# --- STREAMLIT UI ---
st.set_page_config(page_title="Aegis-Buy Prototype", layout="centered")
st.title("🛡️ Aegis-Buy: Agentic AI Procurement")

with st.form("mission_form"):
    url = st.text_input("Amazon Product URL")
    urgency = st.select_slider("How urgent is this purchase?", options=range(1, 11), value=5)
    submitted = st.form_submit_button("Launch Agentic Sourcing")

if submitted and url:
    with st.spinner("Agent exploring price history and sentiment..."):
        result = compiled_agent.invoke({"url": url, "urgency": urgency})
        
        # PERSIST TO SUPABASE
        supabase.table("price_missions").insert({
            "asin": result["asin"],
            "verdict": result["verdict"],
            "current_price": result["data"]["current"],
            "urgency": urgency
        }).execute()

        st.success("Mission Complete")
        st.subheader("Fiduciary Recommendation")
        st.write(result["verdict"])
        
        # Visual Metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("Current", f"${result['data']['current']}")
        c2.metric("90d Avg", f"${result['data']['avg_90']}")
        c3.metric("Best", f"${result['data']['low']}")