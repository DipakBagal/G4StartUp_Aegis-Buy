# 🎬 Demo Video Script - Aegis-Buy AI Procurement Agent
## Duration: 3 Minutes | Google for Startups - Scaler Showcase

---

## **[0:00-0:20] INTRODUCTION (20 seconds)**

**[Screen: Your face/avatar]**

"Hi! I'm [Your Name], and I'm excited to share **Aegis-Buy** - an AI-powered procurement agent that ensures you never overpay for online purchases.

Have you ever bought something on Amazon, only to see the price drop the next week? Or wondered if you're getting a good deal?

That's the problem Aegis-Buy solves."

---

## **[0:20-0:45] THE PROBLEM (25 seconds)**

**[Screen: Show example of price fluctuation graph or screenshots]**

"The problem is real:
- Amazon prices change **multiple times per day**
- Buyers don't know if it's the 'right time' to purchase
- Price comparison sites only show numbers - they don't tell you **WHEN to buy**
- Web reviews are scattered across Reddit, forums, and review sites

Traditional tools are **calculators**, not **advisors**."

---

## **[0:45-1:30] THE SOLUTION - DEMO (45 seconds)**

**[Screen: Live Streamlit app at https://g4startup-aegis-buy.streamlit.app]**

"Aegis-Buy is a **multi-agent AI system** powered by Google Gemini 2.5 Flash. Watch how it works:

**[Paste an Amazon product URL]**

1. **Researcher Agent** - Fetches real-time prices from Amazon via Rainforest API
   - Current price, MSRP, ratings
   
2. **Sentiment Agent** - Analyzes web reviews from Reddit and tech forums using SerpApi
   - Are people happy? Any known defects? New models coming?
   
3. **Strategist Agent** - The brain powered by Gemini
   - Combines price data + sentiment + your urgency
   - Gives you a clear verdict: **BUY**, **WATCH**, or **WAIT**

**[Show the verdict appearing with color-coded styling]**

Notice how it doesn't just say 'good price' - it explains **WHY** and considers your timeline."

---

## **[1:30-2:15] THE MAGIC - TECHNICAL DEEP DIVE (45 seconds)**

**[Screen: Show architecture diagram or code snippets]**

"The magic behind Aegis-Buy:

1. **LangGraph Orchestration**
   - Three specialized agents working in sequence
   - State management ensures context flows between agents
   
2. **The Golden Prompt**
   - I gave Gemini a 'fiduciary duty' - protect the buyer's wallet
   - Clear decision framework: price analysis + sentiment + urgency
   - Structured output: verdict + 3 bullet justification
   
3. **Multi-Currency Global Support**
   - Auto-detects Amazon domain (amazon.in, .com, .co.uk, etc.)
   - Shows prices in local currency (₹, $, £, €)
   - Works across 12+ countries

**[Show Golden Prompt document or screenshot]**

This single prompt became the DNA for the entire strategist agent."

---

## **[2:15-2:45] BUSINESS IMPACT (30 seconds)**

**[Screen: Stats or mockup of use cases]**

"Why this matters:

**For Consumers:**
- Save money by buying at the right time
- Avoid products with known issues
- Make confident purchase decisions

**For Businesses:**
- B2B procurement teams can use this for bulk purchases
- Reduce overspending on office supplies, equipment
- Track price missions and build historical data

**Market Size:**
- E-commerce is a $5.7 trillion market
- Even 5% savings = massive value

The prototype already stores missions in Supabase for analytics."

---

## **[2:45-3:00] CALL TO ACTION (15 seconds)**

**[Screen: App URL + GitHub]**

"Try it now: **https://g4startup-aegis-buy.streamlit.app**

Built with:
- ✅ Google Gemini 2.5 Flash
- ✅ LangGraph for agent orchestration
- ✅ Streamlit for the UI
- ✅ Supabase for data persistence

Thank you for watching! I'd love your feedback."

**[End screen with: Your name, App URL, GitHub repo]**

---

## **RECORDING TIPS**

### Tools Needed:
- **Screen recorder**: OBS Studio (free) or Loom
- **Microphone**: Built-in laptop mic is fine
- **Video editor** (optional): DaVinci Resolve (free) or Windows Photos

### Recording Steps:

1. **Script practice**: Read the script 2-3 times before recording
2. **Screen sections**:
   - Introduction: Your face/avatar (webcam or animated avatar)
   - Demo: Full-screen app walkthrough
   - Technical: Code snippets or architecture diagram
   - Closing: Back to face or app URL
   
3. **Voiceover tips**:
   - Speak clearly and enthusiastically
   - Pause between sections for editing
   - Don't worry about perfection - authenticity beats polish

4. **Visual enhancements**:
   - Add text overlays for key points
   - Use zoom-in effects when showing specific features
   - Add background music (low volume) for energy

### Test Run Flow:
1. Open app
2. Have product URL ready (something interesting with real prices)
3. Walk through the 3 agents step-by-step
4. Show the final verdict with styling
5. Click debug expander if showing technical depth

---

## **SUBMISSION CHECKLIST**

✅ **Live App URL**: https://g4startup-aegis-buy.streamlit.app  
✅ **Demo Video**: 3 minutes max (record using script above)  
✅ **Golden Prompt**: Already documented in `GOLDEN_PROMPT.md`  
✅ **GitHub Repo**: https://github.com/DipakBagal/G4StartUp_Aegis-Buy

---

**Good luck with your submission! 🚀**
