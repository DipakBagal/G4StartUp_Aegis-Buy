import os
import streamlit as st
import requests
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from supabase import create_client, Client
import google.generativeai as genai
from dotenv import load_dotenv

# --- INITIALIZATION & AUTH ---
load_dotenv()

# Support both local .env and Streamlit secrets
def get_secret(key):
    """Get secret from Streamlit secrets or environment variables"""
    # Try Streamlit secrets first (for cloud deployment)
    if hasattr(st, 'secrets') and key in st.secrets:
        return st.secrets[key]
    # Fall back to environment variables (for local development)
    return os.getenv(key)

# Initialize clients
supabase_url = get_secret("SUPABASE_URL")
supabase_key = get_secret("SUPABASE_KEY")
gemini_key = get_secret("GEMINI_API_KEY")

if not supabase_url or not supabase_key:
    st.error("⚠️ Supabase credentials not configured. Please add them to Streamlit secrets.")
    st.stop()

if not gemini_key:
    st.error("⚠️ Gemini API key not configured. Please add it to Streamlit secrets.")
    st.stop()

supabase: Client = create_client(supabase_url, supabase_key)

try:
    genai.configure(api_key=gemini_key)
except Exception as e:
    st.error(f"⚠️ Error configuring Gemini API: {str(e)}")
    st.info("Please check your GEMINI_API_KEY in Streamlit secrets.")
    st.stop()

# --- STATE DEFINITION ---
class AgentState(TypedDict):
    url: str
    asin: str
    urgency: int
    product_data: dict
    sentiment_data: str
    final_verdict: str

# --- AGENT TOOLS (REAL DATA LINKS) ---

def extract_asin(url: str) -> str:
    """Extracts ASIN from a standard Amazon URL."""
    try:
        if "/dp/" in url: return url.split("/dp/")[1].split("/")[0].split("?")[0]
        if "/gp/product/" in url: return url.split("/gp/product/")[1].split("/")[0].split("?")[0]
        return "B000000000"
    except:
        return "B000000000"

def fetch_rainforest_product(asin: str):
    """Calls Rainforest API for real-time Amazon pricing and specs."""
    params = {
        'api_key': get_secret("RAINFOREST_API_KEY"),
        'type': 'product',
        'amazon_domain': 'amazon.com',
        'asin': asin
    }
    response = requests.get('https://api.rainforestapi.com/request', params)
    data = response.json()
    product = data.get('product', {})
    
    return {
        "title": product.get("title", "Unknown Product"),
        "current_price": product.get("buybox_winner", {}).get("price", {}).get("value", 0),
        "rrp": product.get("variants", [{}])[0].get("rrp", {}).get("value", 0), # Simplified for MVP
        "rating": product.get("rating", 0),
        "image": product.get("main_image", {}).get("link", "")
    }

def fetch_serp_sentiment(product_title: str):
    """Uses SerpApi to find Reddit/Tech forum consensus on the product."""
    params = {
        "engine": "google",
        "q": f"{product_title} reddit reviews issues",
        "api_key": get_secret("SERP_API_KEY")
    }
    response = requests.get("https://serpapi.com/search", params)
    results = response.json().get("organic_results", [])
    # Aggregate snippets for the LLM to analyze
    snippets = [res.get("snippet", "") for res in results[:3]]
    return " | ".join(snippets)

# --- AGENT NODES (REASONING) ---

def researcher_node(state: AgentState):
    asin = extract_asin(state["url"])
    product_info = fetch_rainforest_product(asin)
    sentiment = fetch_serp_sentiment(product_info["title"])
    return {"asin": asin, "product_data": product_info, "sentiment_data": sentiment}

def strategist_node(state: AgentState):
    try:
        # Use REST API directly with correct v1 endpoint (not v1beta)
        import requests
        import json
        
        api_key = get_secret("GEMINI_API_KEY")
        
        # Use v1 endpoint (more stable than v1beta)
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        prompt = f"""
Act as a Fiduciary Shopping Agent. 
Product: {state['product_data']['title']}
Current Price: ${state['product_data']['current_price']}
MSRP/RRP: ${state['product_data']['rrp']}
User Urgency: {state['urgency']}/10
Web Sentiment: {state['sentiment_data']}

Reasoning Pattern:
1. Is the current price significantly below RRP?
2. Does web sentiment suggest a batch defect or a new model release?
3. Can the user wait based on their urgency?

Provide a bold 'BUY', 'WATCH', or 'WAIT' verdict and justify it with 3 bullet points.
"""
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            verdict = result['candidates'][0]['content']['parts'][0]['text']
            return {"final_verdict": verdict}
        else:
            # Fallback: Try v1beta with different model
            url_beta = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
            response = requests.post(url_beta, headers=headers, data=json.dumps(payload), timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                verdict = result['candidates'][0]['content']['parts'][0]['text']
                return {"final_verdict": verdict}
            else:
                error_data = response.json() if response.text else {}
                error_msg = error_data.get('error', {}).get('message', f'HTTP {response.status_code}')
                return {"final_verdict": f"⚠️ API Error: {error_msg}"}
    except Exception as e:
        return {"final_verdict": f"⚠️ Error generating verdict: {str(e)}. Please check your API configuration."}

# --- GRAPH ORCHESTRATION ---
builder = StateGraph(AgentState)
builder.add_node("researcher", researcher_node)
builder.add_node("strategist", strategist_node)
builder.set_entry_point("researcher")
builder.add_edge("researcher", "strategist")
builder.add_edge("strategist", END)
aegis_engine = builder.compile()

# --- STREAMLIT PRODUCTION UI ---
st.set_page_config(page_title="Aegis-Buy Agent", page_icon="🛡️", layout="wide")

st.title("🛡️ Aegis-Buy: Agentic AI Procurement")
st.write("Ensuring you never buy at the peak. Powered by Google Gemini AI.")

with st.sidebar:
    st.header("🛒 Mission Parameters")
    urgency = st.select_slider("Procurement Urgency", options=range(1,11), value=5)
    st.info("High Urgency (8-10) prioritizes speed. Low Urgency (1-3) prioritizes the absolute floor price.")

target_url = st.text_input("Paste Amazon Product Link:", placeholder="https://www.amazon.com/dp/B0...")

if st.button("🚀 Launch Sourcing Agent"):
    if not target_url:
        st.error("Please provide a product URL.")
    else:
        with st.spinner("Agent 'Aegis' is researching price bands and social sentiment..."):
            # Execute the Graph
            result = aegis_engine.invoke({"url": target_url, "urgency": urgency})
            
            # Persist Result to Supabase
            supabase.table("price_missions").insert({
                "asin": result["asin"],
                "verdict": result["final_verdict"],
                "current_price": result["product_data"]["current_price"],
                "urgency": urgency
            }).execute()

            # Display Output
            st.divider()
            col_img, col_info = st.columns([1, 2])
            
            with col_img:
                st.image(result["product_data"]["image"], caption=result["product_data"]["title"])
            
            with col_info:
                st.subheader("Agent Fiduciary Verdict")
                st.markdown(result["final_verdict"])
                
                # Metric Cards
                m1, m2 = st.columns(2)
                m1.metric("Current Price", f"${result['product_data']['current_price']}")
                m2.metric("RRP/MSRP", f"${result['product_data']['rrp']}")