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

def extract_asin(url: str) -> tuple:
    """Extracts ASIN and domain from Amazon URL."""
    try:
        # Detect domain - check for all supported Amazon domains
        if "amazon.in" in url:
            domain = "amazon.in"
        elif "amazon.co.uk" in url:
            domain = "amazon.co.uk"
        elif "amazon.ca" in url:
            domain = "amazon.ca"
        elif "amazon.de" in url:
            domain = "amazon.de"
        elif "amazon.fr" in url:
            domain = "amazon.fr"
        elif "amazon.es" in url:
            domain = "amazon.es"
        elif "amazon.it" in url:
            domain = "amazon.it"
        elif "amazon.com.au" in url:
            domain = "amazon.com.au"
        elif "amazon.co.jp" in url:
            domain = "amazon.co.jp"
        elif "amazon.com.mx" in url:
            domain = "amazon.com.mx"
        elif "amazon.com.br" in url:
            domain = "amazon.com.br"
        else:
            domain = "amazon.com"
        
        # Extract ASIN
        if "/dp/" in url: 
            asin = url.split("/dp/")[1].split("/")[0].split("?")[0]
        elif "/gp/product/" in url: 
            asin = url.split("/gp/product/")[1].split("/")[0].split("?")[0]
        else:
            asin = "B000000000"
            
        return asin, domain
    except:
        return "B000000000", "amazon.com"

def get_currency_info(domain: str) -> dict:
    """Returns currency symbol and code based on Amazon domain."""
    currency_map = {
        "amazon.in": {"symbol": "₹", "code": "INR"},
        "amazon.com": {"symbol": "$", "code": "USD"},
        "amazon.co.uk": {"symbol": "£", "code": "GBP"},
        "amazon.ca": {"symbol": "CA$", "code": "CAD"},
        "amazon.de": {"symbol": "€", "code": "EUR"},
        "amazon.fr": {"symbol": "€", "code": "EUR"},
        "amazon.es": {"symbol": "€", "code": "EUR"},
        "amazon.it": {"symbol": "€", "code": "EUR"},
        "amazon.com.au": {"symbol": "AU$", "code": "AUD"},
        "amazon.co.jp": {"symbol": "¥", "code": "JPY"},
        "amazon.com.mx": {"symbol": "MX$", "code": "MXN"},
        "amazon.com.br": {"symbol": "R$", "code": "BRL"},
    }
    return currency_map.get(domain, {"symbol": "$", "code": "USD"})

def fetch_rainforest_product(asin: str, domain: str = "amazon.com"):
    """Calls Rainforest API for real-time Amazon pricing and specs."""
    params = {
        'api_key': get_secret("RAINFOREST_API_KEY"),
        'type': 'product',
        'amazon_domain': domain,
        'asin': asin
    }
    
    try:
        response = requests.get('https://api.rainforestapi.com/request', params, timeout=10)
        data = response.json()
        product = data.get('product', {})
        
        # Check availability first
        availability = product.get("buybox_winner", {}).get("availability", {})
        is_available = availability.get("type") == "in_stock"
        availability_msg = availability.get("raw", "Unknown availability")
        
        # Try multiple ways to get the price
        current_price = 0
        
        # Method 1: Buybox winner price
        if product.get("buybox_winner", {}).get("price"):
            price_obj = product["buybox_winner"]["price"]
            if isinstance(price_obj, dict):
                if price_obj.get("value"):
                    current_price = price_obj["value"]
                elif price_obj.get("raw"):
                    # Sometimes it's in raw format like "$99.99"
                    raw_price = str(price_obj["raw"]).replace("$", "").replace(",", "").replace("₹", "")
                    try:
                        current_price = float(raw_price)
                    except:
                        pass
            elif isinstance(price_obj, (int, float)):
                current_price = price_obj
        
        # Method 2: Check offers array
        if current_price == 0 and product.get("buybox_winner", {}).get("offers"):
            offers = product["buybox_winner"]["offers"]
            if offers and len(offers) > 0:
                first_offer = offers[0]
                if first_offer.get("price", {}).get("value"):
                    current_price = first_offer["price"]["value"]
        
        # Method 3: Look in bestsellers_rank for typical price (if mentioned)
        # Some products have price in different places when unavailable
        
        # Get RRP/MSRP
        rrp = 0
        
        # Try list_price first
        if product.get("list_price", {}).get("value"):
            rrp = product["list_price"]["value"]
        
        # Try variants
        if rrp == 0 and product.get("variants"):
            for variant in product["variants"]:
                if variant.get("list_price", {}).get("value"):
                    rrp = variant["list_price"]["value"]
                    break
        
        # If product is unavailable but we found no price, check last known price patterns
        # (some APIs store historical price data)
        
        # If no RRP found and we have current price, estimate RRP
        if rrp == 0 and current_price > 0:
            rrp = current_price * 1.2
        
        # If both are 0, mark as unavailable
        product_status = "available" if is_available and current_price > 0 else "unavailable"
        
        # Get currency info
        currency = get_currency_info(domain)
        
        return {
            "title": product.get("title", "Unknown Product"),
            "current_price": current_price,
            "rrp": rrp,
            "rating": product.get("rating", 0),
            "image": product.get("main_image", {}).get("link", ""),
            "availability": availability_msg,
            "status": product_status,
            "currency": currency,
            "raw_data": product  # Keep for debugging
        }
    except Exception as e:
        return {
            "title": "Error fetching product",
            "current_price": 0,
            "rrp": 0,
            "rating": 0,
            "image": "",
            "availability": "Error",
            "status": "error",
            "currency": {"symbol": "$", "code": "USD"},
            "error": str(e)
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
    asin, domain = extract_asin(state["url"])
    product_info = fetch_rainforest_product(asin, domain)
    sentiment = fetch_serp_sentiment(product_info["title"])
    return {"asin": asin, "product_data": product_info, "sentiment_data": sentiment}

def strategist_node(state: AgentState):
    try:
        # Use REST API with models that have available quota
        import requests
        import json
        
        api_key = get_secret("GEMINI_API_KEY")
        
        # Use gemini-2.5-flash (standard stable model with quota)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        
        currency_symbol = state['product_data'].get('currency', {}).get('symbol', '$')
        
        prompt = f"""
Act as a Fiduciary Shopping Agent. 
Product: {state['product_data']['title']}
Current Price: {currency_symbol}{state['product_data']['current_price']}
MSRP/RRP: {currency_symbol}{state['product_data']['rrp']}
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

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .verdict-box {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .verdict-buy {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
    }
    .verdict-wait {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
    }
    .verdict-watch {
        background-color: #cce5ff;
        border-left: 5px solid #007bff;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header"><h1 style="color: white; margin: 0;">🛡️ Aegis-Buy: Agentic AI Procurement</h1><p style="color: #e0e0e0; margin: 0.5rem 0 0 0;">Ensuring you never buy at the peak. Powered by Google Gemini AI.</p></div>', unsafe_allow_html=True)

# Info banner
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🤖 Agent Type", "Multi-Agent AI")
with col2:
    st.metric("🧠 Powered By", "Gemini 2.5 Flash")
with col3:
    st.metric("🌍 Global Coverage", "12+ Countries")

st.divider()

with st.sidebar:
    st.header("🛒 Mission Parameters")
    urgency = st.select_slider("Procurement Urgency", options=range(1,11), value=5)
    st.info("**High Urgency (8-10):** Prioritizes speed\n\n**Low Urgency (1-3):** Prioritizes absolute floor price")
    
    st.divider()
    st.subheader("📊 How It Works")
    st.markdown("""
    1. **🔍 Researcher Agent** - Fetches real-time prices & product data
    2. **💭 Sentiment Agent** - Analyzes web reviews & social sentiment  
    3. **🧠 Strategist Agent** - AI-powered purchase recommendation
    """)
    
    st.divider()
    st.caption("Built for Google for Startups - Scaler Showcase")

target_url = st.text_input("📦 Paste Amazon Product Link:", placeholder="https://www.amazon.com/dp/B0... or amazon.in, amazon.co.uk, etc.")

if st.button("🚀 Launch Sourcing Agent", use_container_width=True):
    if not target_url:
        st.error("Please provide a product URL.")
    else:
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.text("🕵️ Researcher Agent: Extracting product data...")
        progress_bar.progress(33)
        
        with st.spinner("Agent 'Aegis' is researching price bands and social sentiment..."):
            # Execute the Graph
            status_text.text("💭 Sentiment Agent: Analyzing web reviews...")
            progress_bar.progress(66)
            
            result = aegis_engine.invoke({"url": target_url, "urgency": urgency})
            
            status_text.text("🧠 Strategist Agent: Generating fiduciary verdict...")
            progress_bar.progress(100)
            
            # Persist Result to Supabase
            try:
                supabase.table("price_missions").insert({
                    "asin": result["asin"],
                    "verdict": result["final_verdict"],
                    "current_price": result["product_data"]["current_price"],
                    "urgency": urgency
                }).execute()
            except:
                pass  # Silently fail if DB insert fails
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()

            # Display Output
            st.success("✅ Analysis Complete!")
            st.divider()
            
            col_img, col_info = st.columns([1, 2])
            
            with col_img:
                if result["product_data"]["image"]:
                    st.image(result["product_data"]["image"], use_container_width=True)
                st.caption(result["product_data"]["title"])
                st.caption(f"⭐ Rating: {result['product_data'].get('rating', 'N/A')}")
            
            with col_info:
                # Determine verdict type for styling
                verdict_text = result["final_verdict"].upper()
                if "BUY" in verdict_text:
                    verdict_class = "verdict-buy"
                    verdict_icon = "✅"
                elif "WAIT" in verdict_text:
                    verdict_class = "verdict-wait"
                    verdict_icon = "⏸️"
                else:
                    verdict_class = "verdict-watch"
                    verdict_icon = "👀"
                
                st.markdown(f'<div class="{verdict_class} verdict-box"><h3>{verdict_icon} Agent Fiduciary Verdict</h3></div>', unsafe_allow_html=True)
                st.markdown(result["final_verdict"])
                
                # Show availability warning
                if result['product_data'].get('status') == 'unavailable':
                    st.warning(f"⚠️ Product Status: {result['product_data'].get('availability', 'Currently unavailable')}")
                
                # Get currency symbol
                currency_symbol = result['product_data'].get('currency', {}).get('symbol', '$')
                
                # Metric Cards
                m1, m2 = st.columns(2)
                m1.metric("Current Price", f"{currency_symbol}{result['product_data']['current_price']}" if result['product_data']['current_price'] > 0 else "N/A")
                m2.metric("RRP/MSRP", f"{currency_symbol}{result['product_data']['rrp']}" if result['product_data']['rrp'] > 0 else "N/A")
                
                # Debug info
                if result['product_data']['current_price'] == 0:
                    with st.expander("🔍 Debug: API Response"):
                        st.json(result['product_data'].get('raw_data', {}))