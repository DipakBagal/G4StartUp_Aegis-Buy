# 🛡️ Aegis-Buy: Agentic AI Procurement Assistant

An intelligent procurement agent powered by Google's Gemini 1.5 Pro that helps you make informed purchasing decisions on Amazon products. Aegis-Buy analyzes pricing trends, web sentiment, and market conditions to provide fiduciary recommendations on whether to buy now or wait for better deals.

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
- Built as part of the SKY-UK initiative
- Powered by Scalar technology

## 📞 Support

For questions or issues, please open an issue on GitHub.

---

**Note**: This is a demonstration project for the Google for Startups program. Ensure you comply with Amazon's Terms of Service when using product data APIs.
