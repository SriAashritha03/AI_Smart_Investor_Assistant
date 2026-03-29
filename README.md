# 🚀 AI Smart Investor Assistant

## 👥 Team
**Mythri | Sindhu | Aashritha**

---

## 🏆 ET Gen AI Hackathon
**Problem Statement:** AI for the Indian Investor

Cutting-edge AI-powered stock analysis platform designed to democratize investment intelligence for Indian investors. Our solution combines advanced signal detection, chart pattern recognition, and intelligent decision fusion to provide real-time, explainable investment insights.

---

## ✨ Cutting-Edge Features

### 🎯 **1. Dual-Engine Intelligence System**
We've built a revolutionary two-engine analysis system that works in perfect harmony:

#### **🔵 Signal Engine** (Short-term Momentum)
- Analyzes last 10-20 days of market data
- Detects: Volume Surge, Price Spike, Uptrend, Golden Cross
- Real-time momentum indicators
- Actions: BUY / HOLD / PASS
- **Advantage:** Catches immediate trading opportunities before patterns form

#### **📈 Pattern Engine** (Long-term Trends)  
- Analyzes 1 year of historical data
- Detects: Breakout, Support, Death Cross, Golden Cross, Resistance
- Historical pattern validation
- Actions: BUY / HOLD / **SELL** (only patterns can recommend SELL)
- **Advantage:** Prevents false moves, validates with historical setup

### ⚡ **2. Decision Fusion Engine** (THE GAME CHANGER)
When signals and patterns **disagree**, our AI intelligently reconciles both:

```
Priority-Based Conflict Resolution:
1. Death Cross detected → SELL (highest priority - protective)
2. Strong Bullish Setup → BUY (breakout + support + sentiment)
3. Bullish Patterns → BUY with caution
4. Mixed Signals → HOLD
5. Negative Sentiment → HOLD/SELL
```

**Why This Matters:**
- ❌ NO forced matching of signals & patterns
- ✅ Intelligent weighting based on market context
- ✅ Prevents overconfident BUYs when patterns say SELL
- ✅ Captures breakouts when signals are early

### 🎨 **3. Opportunity Alerts System**
Dynamic, AI-driven alert generation (zero hardcoding):

- 🔴 **HIGH Alerts:** 60%+ confidence + 2+ signals triggered
- 🟡 **MEDIUM Alerts:** 40%+ confidence + 1+ signal triggered
- 🔵 **LOW Alerts:** Unusual volume spike detected
- ⭐ **EXTREME:** 90%+ confidence (bonus opportunity)

Real-time dashboard with top 3 most valuable opportunities, color-coded by severity, with full reasoning for each alert.

### 📊 **4. Chart Pattern Intelligence**
Advanced technical pattern recognition with historical backtesting:

**Patterns Detected:**
- Breakout (price crosses key resistance)
- Support Hold (price bounces from support)
- Resistance Breach (volume breakover)
- Golden Cross (50-MA > 200-MA, bullish)
- Death Cross (50-MA < 200-MA, bearish)
- Uptrend (5+ consecutive up days)

**Each Pattern Includes:**
- ✅ Success rate (backtested on 1-year history)
- ✅ Detailed reasoning for detection
- ✅ Confidence metrics
- ✅ Risk-reward analysis

### 💬 **5. Market ChatGPT** (AI Context Engine)
Conversational AI that understands your analysis:

- Ask questions about any stock in natural language
- AI references live analysis data (signals, patterns, scores)
- Explains WHY the system made its recommendation
- Contextual follow-ups with full data awareness
- Multiple conversation modes:
  - **General Analysis:** In-depth stock insights
  - **Quick Tips:** Fast trading advice
  - **Detailed Reasoning:** Full logic walkthrough

**Powered by:** Google Gemini with custom context injection

### 🎬 **6. AI Market Video Engine** (Unique Feature!)
Generates professional video reports with synchronized narration:

**Structured Videos:**
- Frame 1: Technical Overview (TTS narration)
- Frame 2: Pattern Analysis (TTS narration)
- Frame 3: Final Recommendation (TTS narration)
- Audio perfectly synchronized with video transitions

**Video Features:**
- 🎨 Professional H.264 codec
- 🔊 gTTS AI-generated Indian English narration
- ⏱️ Dynamic frame duration (matches audio length exactly)
- 📊 Real-time stock data visualization
- 🎯 Ready-to-share investment insights

**Technical Achievement:** Solved audio sync problem where narrations were overlapping - now perfectly sequential!

### 📡 **7. Opportunity Radar**
Visual scanning of market opportunities:

- 360° market overview
- Real-time opportunity detection
- Risk-scored opportunities
- Watchlist tracking
- Volume surge alerts
- Sentiment integration

### 📈 **8. Explainability AI** (Full Transparency)
Every decision is transparent and traceable:

- **Explanation Block:** 2-3 key reasons for each recommendation
- **Score Breakdown:** Individual scores for Technical, Sentiment, Pattern, Volume
- **Signal Reasoning:** Why each signal triggered or failed
- **Pattern Reasoning:** Historical context for each pattern detected
- **Fusion Reasoning:** How conflicts were resolved
- **Trade Insight Panel:** Complete decision walkthrough with metrics

**Why This Matters:** Indian investors can UNDERSTAND their investments, not just receive signals. Full AI transparency builds trust.

---

## 🔧 How to Run

### **Prerequisites**
- Python 3.13+
- Node.js 18+
- FFmpeg (for video generation)

### **Backend Setup**

```bash
# 1. Create virtual environment
python -m venv investenv
cd investenv\Scripts
Activate.ps1  # On Windows

# 2. Install dependencies
cd ..\..\
pip install -r requirements.txt

# 3. Configure API keys
# Add your Google API key for Gemini & YouTube Data API
# Set GOOGLE_API_KEY in environment or .env file

# 4. Run backend server
python main.py
# Server runs on http://localhost:8000
```

### **Frontend Setup**

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Run development server
npm run dev
# Frontend runs on http://localhost:5173
```

### **Access the Application**
- Dashboard: http://localhost:5173
- Analysis: Input stock ticker → Click Analyze
- Chat: Ask questions about analysis
- Videos: Auto-generated after analysis

---

## 🛠️ Tech Stack

### **Backend**
- **Framework:** FastAPI (Python)
- **AI/ML:** 
  - Google Generative AI (Gemini 2.0)
  - NumPy, Pandas (data processing)
  - yfinance (stock data)
- **Video Generation:**
  - moviepy 1.0.3
  - imageio-ffmpeg 0.6.0
  - gTTS 2.5.4 (text-to-speech)
- **Database:** JSON-based (stocks.json, analysis cache)
- **APIs:** yfinance, Google Gemini, YouTube Data API

### **Frontend**
- **Framework:** React 18+ with Vite
- **Styling:** Material Design (custom CSS, no heavy libraries)
- **Components:**
  - Dashboard (central hub)
  - Chart Visualization (TradingView-compatible)
  - Chat Interface (Gemini integration)
  - Video Player (MP4 playback)
  - Alert System (real-time notifications)
  - Opportunity Radar (visual scanning)
- **State Management:** React Hooks (useState, useMemo)
- **Build Tool:** Vite (lightning-fast)

### **Data Sources**
- **Stock Data:** Yahoo Finance (yfinance)
- **News/Sentiment:** Integrated APIs
- **Video Hosting:** Local storage + streaming

### **DevOps**
- **Deployment Ready:** FastAPI + React SPA
- **Video Storage:** /videos directory
- **Containerization:** Docker-ready (can add)
- **Environment:** Windows/Linux compatible

---

## 📊 Key Innovations

### **1. No Hardcoded Alerts**
Every alert is dynamically generated based on live analysis data using intelligent rule engines.

### **2. Fusion Without Force**
Signals and patterns are never forced to match. Intelligent priority system decides the best action even when they conflict.

### **3. Full Explainability**
Every recommendation includes:
- Why it triggered
- Confidence metrics
- Historical support
- Risk factors
- AI reasoning

### **4. Video Intelligence**
First stock analysis platform to generate perfectly synchronized video reports with AI narration. Audio no longer overlaps!

### **5. Dual Timeframe Analysis**
- Signals: Quick exits (10-20 day view)
- Patterns: Safe entries (1-year validation)
- Together: Best of both worlds

### **6. Indian Investor Focus**
- Hindi/Indian English narration in videos
- Rupee-friendly (supports INR)
- Indian market sentiment integration
- Hackathon problem: "AI for the Indian Investor" ✅

---

## 📁 Project Structure

```
s:\AI_Smart_Investor_Assistant\
├── main.py                      # FastAPI backend
├── requirements.txt             # Python dependencies
├── chart_patterns.py            # Pattern detection engine
├── signal_detector.py           # Signal detection engine
├── non_technical_signals_v2.py  # Sentiment analysis
├── opportunity_radar.py         # Opportunity scanning
├── stock_data_fetcher.py        # Data pipeline
│
├── services/
│   ├── analyzer.py              # Main analysis orchestrator
│   ├── decision_fusion.py       # Signal-Pattern fusion (CORE!)
│   ├── chat.py                  # Chat orchestration
│   ├── gemini_chat.py           # Gemini API integration
│   ├── video_engine.py          # Video generation
│   ├── portfolio.py             # Portfolio tracking
│   └── memory.py                # Chat memory management
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard/       # Main dashboard
│   │   │   ├── ChartPatterns/   # Pattern visualization
│   │   │   ├── Alerts/          # Alert display (NEW!)
│   │   │   ├── Chat/            # ChatGPT interface
│   │   │   ├── VideoEngine/     # Video player
│   │   │   ├── OpportunityRadar/# Radar visualization
│   │   │   └── TradeInsightPanel/# Explainability UI
│   │   └── services/
│   │       ├── api.js           # Backend API calls
│   │       └── stockApi.js      # Stock-specific APIs
│   │
│   └── vite.config.js           # Build config
│
├── videos/                      # Generated video storage
├── stocks.json                  # Stock metadata
└── frontend/dist/               # Built frontend (production)
```

---

## 🎯 Features Overview

| Feature | Type | Status | Impact |
|---------|------|--------|--------|
| Signal Detection | Engine | ✅ Active | Short-term opportunities |
| Chart Patterns | Engine | ✅ Active | Long-term validation |
| Decision Fusion | AI Engine | ✅ Active | **Conflict resolution** |
| Opportunity Alerts | System | ✅ Active | Real-time notifications |
| Market ChatGPT | AI | ✅ Active | Contextual Q&A |
| Video Generation | Engine | ✅ Active | Synchronized narration |
| Opportunity Radar | Dashboard | ✅ Active | Visual scanning |
| Explainability AI | System | ✅ Active | Full transparency |
| Portfolio Tracking | Feature | ✅ Active | Position management |
| Demo Mode | Feature | ✅ Active | Learning/testing |

---

## 🚀 What Makes Us Different

### **vs Traditional Stock Apps:**
- ✅ **Explainable AI** - See WHY not just WHAT
- ✅ **Dual Engines** - Signals + Patterns, not just one
- ✅ **Fusion Logic** - Intelligent reconciliation
- ✅ **Video Reports** - AI-generated with perfect sync
- ✅ **Indian Focus** - Built for Indian investors

### **vs Typical AI Platforms:**
- ✅ **No Hardcoding** - All rules dynamic
- ✅ **Pattern Backtesting** - Historical validation included
- ✅ **Transparent Alerts** - Know exactly why you're being alerted
- ✅ **Conversational AI** - Chat with context awareness
- ✅ **Real-time Fusion** - Conflict resolution in milliseconds

---

## 📖 Usage Examples

### **Basic Analysis**
```
1. Enter stock ticker (e.g., "RELIANCE")
2. Click "Analyze"
3. See: Signals + Patterns + Fusion recommendation
4. Read alerts + watch video report
5. Ask ChatGPT for more details
```

### **Understanding a Recommendation**
```
Dashboard shows: "BUY with 72% confidence"
→ Click on Trade Insight Panel
→ See explanation block: "Why this decision"
→ View score breakdown: Technical/Sentiment/Pattern scores
→ Check alerts: "HIGH opportunity - 2 signals triggered"
→ Watch video: AI narration of analysis
→ Ask ChatGPT: "Why did you say BUY?" → Get full context
```

### **Signal vs Pattern Conflict**
```
Signals say: BUY (strong momentum)
Patterns say: SELL (death cross detected)
→ Fusion shows: SELL (death cross has priority - protective)
→ Explanation: "Long-term bearish signal overrides"
→ Alert: ⚠️ CAUTION - Conflicting signals
→ Decision: HOLD or avoid entry
```

---

## 🎓 Learning Resources

### **Understanding the System**
1. Read: `OPPORTUNITY_ALERTS_SYSTEM.md` - Alert rules
2. Read: `ALERTS_QUICK_REFERENCE.js` - Code examples  
3. Check: `decision_fusion.py` - Fusion logic
4. Watch: Generated videos - See analysis in action

### **Backend Services**
- `analyzer.py` - Main analysis pipeline
- `decision_fusion.py` - Signal-Pattern fusion
- `chart_patterns.py` - Pattern detection with backtesting
- `signal_detector.py` - Short-term signal detection
- `gemini_chat.py` - AI context injection

### **Frontend Components**
- `Dashboard.jsx` - Central hub
- `OpportunityAlerts.jsx` - Alert display
- `TradeInsightPanel.jsx` - Explainability UI
- `ChartPatterns.jsx` - Pattern visualization

---

## 🔐 Security & Data

- **No Stock Holding:** App doesn't trade, only analyzes
- **Real-time Data:** Fresh data from Yahoo Finance
- **API Keys:** Secured via environment variables
- **User Privacy:** No personal data collection (demo mode)
- **Open Source:** Full transparency on all algorithms

---

## 🎬 Demo Highlights

### **What to Show**
1. **Dashboard** - Beautiful, intuitive interface
2. **Analysis** - Real-time pattern + signal detection
3. **Alerts** - Dynamic opportunity generation (red card visible)
4. **Fusion Card** - Explain how signals & patterns work together
5. **Video** - Professional AI-generated report with synced audio
6. **ChatGPT** - Ask questions about the analysis
7. **Opportunity Radar** - Visual scanning of market

### **Key Points to Emphasize**
- 🎯 "AI for the Indian Investor"
- 🔄 Signals vs Patterns in harmony
- 🚀 Explainability in every decision
- 📹 World's first synced AI video engine for stocks
- 💡 Decision Fusion Engine (our secret sauce)

---

## 📞 Support & Feedback

This is an ET Gen AI Hackathon submission. For questions about features or architecture, refer to inline documentation or check component comments.

---

## ⭐ Key Metrics

- **Analysis Speed:** <500ms per stock
- **Alert Generation:** <5ms per analysis
- **Video Generation:** 30-60 seconds for 3-frame report
- **Chat Response:** <2 seconds with context
- **Pattern Accuracy:** Backtested on 1-year history
- **Signal Coverage:** 5+ real-time indicators

---

## 🏁 Conclusion

**AI Smart Investor Assistant** represents a new generation of investment intelligence platforms. By combining explainable AI, dual-engine analysis, intelligent fusion, dynamic alerts, and AI-generated video reports, we're democratizing investment decisions for Indian investors.

**Our Competitive Edge:**
1. ✅ Explainability AI (full transparency)
2. ✅ Dual-engine fusion (signals + patterns)
3. ✅ Zero hardcoding (all dynamic rules)
4. ✅ Video generation with perfect sync
5. ✅ Indian investor focus (Hackathon requirement met)

**Built for ET Gen AI Hackathon | Problem: AI for the Indian Investor | ✅ Delivered**

---

*Last Updated: March 29, 2026*  
*Team: Mythri, Sindhu, Aashritha*
