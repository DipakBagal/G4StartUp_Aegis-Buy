# 🌟 The Golden Prompt - Aegis-Buy AI Procurement Agent

## The Core Instruction That Started It All

This is the foundational prompt that kickstarted the Aegis-Buy prototype in Google AI Studio, transforming a simple idea into an agentic AI procurement system.

---

## **The Golden Prompt**

```
Act as a Fiduciary Shopping Agent with the sole mission of protecting the buyer from overpaying.

You will analyze:
1. Current Product Price vs MSRP/RRP (Manufacturer's Suggested Retail Price)
2. Web Sentiment from Reddit, tech forums, and review sites
3. User's Purchase Urgency (1-10 scale)

Your Decision Framework:
- If current price is significantly below RRP (>15% discount) AND web sentiment is positive: **BUY**
- If web sentiment suggests known issues, upcoming model releases, or price drops expected: **WAIT**
- If price is near RRP but user urgency is low: **WATCH** (monitor for better deals)

Output Format:
Provide a bold verdict: 'BUY', 'WATCH', or 'WAIT'
Follow with exactly 3 bullet points justifying your recommendation with:
- Price analysis (current vs historical/RRP)
- Sentiment insights (quality issues, community feedback)
- Timing strategy (based on urgency and market conditions)

Remember: Your fiduciary duty is to the buyer's wallet, not the seller's revenue.
```

---

## **Why This Prompt Works**

### 1. **Clear Role Definition**
- Establishes the AI as a "Fiduciary Shopping Agent" - creating a duty of care framework
- Sets the north star: protect buyer from overpaying

### 2. **Structured Input Parameters**
- Three clear data points: Price, Sentiment, Urgency
- Removes ambiguity about what information the AI needs

### 3. **Explicit Decision Logic**
- Provides conditional reasoning framework
- Teaches the AI *when* to recommend what action
- Uses percentages (>15% discount) for concrete thresholds

### 4. **Constrained Output Format**
- One-word verdict for clarity
- Exactly 3 bullets for structured reasoning
- Forces the AI to be concise and actionable

### 5. **Ethical Anchor**
- "Fiduciary duty to buyer's wallet" creates an alignment mechanism
- Prevents the AI from being overly promotional

---

## **Evolution: From Prompt to Multi-Agent System**

The Golden Prompt became the DNA for our **Strategist Agent**, which works alongside:

1. **Researcher Agent** - Fetches real-time data from Rainforest API (Amazon pricing)
2. **Sentiment Agent** - Uses SerpApi to aggregate web reviews and forum discussions  
3. **Strategist Agent** - Powered by Gemini 2.5 Flash, uses the Golden Prompt logic

This demonstrates the power of **LangGraph** orchestration: breaking a single powerful prompt into specialized agent nodes that work in sequence.

---

## **Technical Implementation**

```python
def strategist_node(state: AgentState):
    # The Golden Prompt powers this agent
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
    
    response = gemini_model.generate_content(prompt)
    return {"final_verdict": response.text}
```

---

## **Key Innovation: Agentic Reasoning**

Unlike traditional price comparison tools that just show numbers, Aegis-Buy:
- ✅ **Synthesizes** multiple data sources (price + sentiment)
- ✅ **Contextualizes** with user urgency
- ✅ **Recommends** an action (BUY/WATCH/WAIT)
- ✅ **Explains** the reasoning transparently

This is the difference between a calculator and a trusted advisor.

---

## **Built for Google for Startups - Scaler Showcase**

**Prototype URL:** https://g4startupaegis-buy-63ncci879g9tn236eshtr6.streamlit.app

**Problem Solved:** Buyers overpay because:
- They don't know if it's the "right time" to buy
- Price comparison sites don't include sentiment/quality analysis
- No tool combines urgency + pricing + reputation

**Aegis-Buy's Mission:** Ensure you never buy at the peak. 🛡️

---

*This document demonstrates how a single well-crafted prompt can be the foundation for an entire multi-agent AI system powered by Google Gemini.*
