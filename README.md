# 🛡️ Aegis-Buy: Agentic AI Procurement Assistant

> **🏆 Built for Google for Startups - Scaler Showcase**  
> **🔗 Live Demo:** https://g4startupaegis-buy-63ncci879g9tn236eshtr6.streamlit.app

An intelligent multi-agent procurement system powered by Google's Gemini 2.5 Flash that helps you make informed purchasing decisions on Amazon products. Aegis-Buy analyzes pricing trends, web sentiment, and market conditions to provide fiduciary recommendations on whether to buy now or wait for better deals.

---

## 🎯 The Problem

Online shoppers face three critical challenges:
1. **Price Volatility** - Amazon prices fluctuate multiple times per day
2. **Timing Uncertainty** - Not knowing if it's the "right time" to buy
3. **Information Overload** - Reviews scattered across Reddit, forums, and review sites

Traditional price comparison tools are **calculators**, not **advisors**. They show you numbers but don't tell you **WHEN** to act.

---

## 💡 The Solution

Aegis-Buy is a **multi-agent AI system** that acts as your fiduciary shopping advisor:

- ✅ **Synthesizes** multiple data sources (price + sentiment + timing)
- ✅ **Contextualizes** with your purchase urgency
- ✅ **Recommends** a clear action: **BUY**, **WATCH**, or **WAIT**
- ✅ **Explains** the reasoning transparently

**Mission:** Ensure you never buy at the peak. 🛡️

---

## 🌟 Features

- **Real-time Price Analysis**: Fetches current Amazon pricing and product specifications via Rainforest API
- **Sentiment Analysis**: Aggregates reviews and discussions from Reddit and tech forums using SerpApi
- **AI-Powered Recommendations**: Uses Gemini 1.5 Pro to provide BUY, WATCH, or WAIT verdicts
- **Urgency-Based Decision Making**: Adjusts recommendations based on your purchase urgency (1-10 scale)
- **Mission Tracking**: Stores all price missions in Supabase for historical analysis
- **Multi-Agent Architecture**: Built with LangGraph for orchestrated decision-making workflow

## 🏗️ Architecture

The system uses a multi-agent approach:

1. **Researcher Agent**: Extracts ASIN, fetches product data, and gathers web sentiment
2. **Strategist Agent**: Analyzes all data and provides final purchasing recommendations
3. **State Graph**: Orchestrates the workflow using LangGraph

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI/ML**: Google Generative AI (Gemini 1.5 Pro)
- **Orchestration**: LangGraph
- **Database**: Supabase
- **APIs**: 
  - Rainforest API (Amazon product data)
  - SerpApi (Web sentiment analysis)

## 📋 Prerequisites

- Python 3.8 or higher
- Active API keys for:
  - Google Gemini API
  - Rainforest API
  - SerpApi
  - Supabase project

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/G4StartUp_Aegis-Buy.git
cd G4StartUp_Aegis-Buy
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Fill in your API keys and credentials

4. Set up the database:
   - Create a Supabase project
   - Run the SQL schema from `schema.sql` in your Supabase SQL editor

## 🎮 Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

Then:
1. Paste an Amazon product URL
2. Set your purchase urgency level (1-10)
3. Click "Launch Sourcing Agent"
4. Review the AI-powered recommendation

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```
GOOGLE_API_KEY=your_google_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SERP_API_KEY=your_serp_api_key
RAINFOREST_API_KEY=your_rainforest_api_key
```

### Database Schema

The application uses a single table `price_missions` to track all procurement decisions. See `schema.sql` for the complete schema.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is part of the Google for Startups program.

## 🙏 Acknowledgments

- Google for Startups for Gemini API access
- Built for the Google for Startups - Scaler contest
- Powered by Google Gemini 2.5 Flash

## 📞 Support

For questions or issues, please open an issue on GitHub.

---

**Note**: This is a demonstration project for the Google for Startups program. Ensure you comply with Amazon's Terms of Service when using product data APIs.
