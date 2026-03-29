"""
Gemini API Integration Service

Handles communication with Google's Gemini 2.5 Flash model
for generating intelligent financial insights based on stock analysis.
"""

import logging
import os
from pathlib import Path
import google.generativeai as genai
from typing import Dict

logger = logging.getLogger(__name__)

# Load environment variables from .env file
def _load_env_file():
    """Load environment variables from .env file."""
    env_path = Path(__file__).parent.parent / ".env"
    if env_path.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(env_path)
        except ImportError:
            # Fallback: manually load .env file
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()

_load_env_file()

# Configure Gemini API from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set. Add GEMINI_API_KEY=your_key to .env file")
    
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
MODEL = "gemini-2.5-flash"


def get_confidence_label(confidence: float) -> str:
    """
    Convert confidence percentage to readable label.
    
    Args:
        confidence: Confidence percentage (0-100)
        
    Returns:
        Label: "Low", "Moderate", or "High"
    """
    if confidence < 30:
        return "Low"
    elif confidence < 70:
        return "Moderate"
    else:
        return "High"


def _validate_analysis_data(analysis: Dict) -> bool:
    """
    Validate that analysis data contains essential fields.
    
    Args:
        analysis: Analysis dictionary to validate
        
    Returns:
        True if analysis has required fields, False otherwise
    """
    if not analysis or not isinstance(analysis, dict):
        return False
    
    # Check that required fields exist and are not None
    # Note: signals_triggered can be an empty list - that's valid data (no signals triggered)
    required_fields = ['stock', 'confidence', 'action', 'signals_triggered']
    return all(field in analysis and analysis[field] is not None for field in required_fields)


def generate_investment_advice(question: str, analysis: Dict, query_type: str = "stock") -> str:
    """
    Generate investment advice using Gemini based on stock analysis.
    
    Args:
        question: User's investment question
        analysis: Stock analysis data from analyze_stock()
        query_type: Type of query (stock, comparison, portfolio, general)
        
    Returns:
        Gemini-generated investment advice - STRICT DETERMINISTIC FORMAT
    """
    
    if not question or not analysis:
        return "No analysis data available."
    
    # Validate analysis data contains essential information
    if not _validate_analysis_data(analysis):
        logger.warning(f"Incomplete analysis data provided. Analysis: {analysis}")
        return "No analysis data available."
    
    try:
        stock = analysis.get('stock', 'Unknown')
        confidence = analysis.get('confidence', 0)
        confidence_label = get_confidence_label(confidence)
        signals = analysis.get('signals_triggered', [])
        signals_text = ', '.join(signals) if signals else 'None (no clear momentum)'
        action = analysis.get('action', 'AVOID')
        
        # Prepare analysis summary
        analysis_summary = f"""
Stock: {stock}
Opportunity Level: {analysis.get('opportunity_level', 'N/A')}
Confidence: {confidence}% ({confidence_label})
Action: {action}
Signals Triggered: {signals_text}
Summary: {analysis.get('summary', 'No summary available')}
"""
        
        # STRICT CONTROL SYSTEM PROMPT - Deterministic Decision Engine
        system_prompt = f"""You are a STRICT financial decision engine.

HARD RULES:
1. ONLY use provided STOCK ANALYSIS DATA
2. Each section MUST be on new line
3. DO NOT compress or change format
4. NO generic hedging language

OUTPUT FORMAT (MANDATORY):

Decision: <BUY / HOLD / AVOID>

Why:
- Signals: <list OR "no clear signals">
- Confidence: <X>% (<Low/Moderate/High>)
- Insight: <1-line interpretation>

Next Step:
<ONE specific actionable suggestion>

FORMAT RULES:
- Max 7 lines total
- Keep format rigid
- Be confident and direct

If no signals → exactly: "no clear signals"
If confidence < 30% → add caution note

Example:

Decision: HOLD

Why:
- Signals: RSI reading above 70
- Confidence: 55% (Moderate)
- Insight: Early overbuy pattern forming

Next Step:
Watch for pullback entry near $150

You are deterministic. Not chatbot."""
        
        # Inject stock explicitly and provide data in prompt
        prompt = f"""USER QUESTION: {question}

STOCK: {stock}

STOCK ANALYSIS DATA:
{analysis_summary}

Apply the strict format rules. Generate your decision:"""
        
        logger.info(f"Generating deterministic advice for {stock} - Confidence: {confidence}%")
        
        # Call Gemini API
        client = genai.GenerativeModel(
            MODEL,
            system_instruction=system_prompt
        )
        response = client.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.3,  # VERY low temperature = deterministic, no creativity
                top_p=0.8,
            )
        )
        
        if response and response.text:
            advice = response.text.strip()
            logger.info(f"✅ Generated advice for {stock}")
            return advice
        else:
            logger.warning(f"Empty response from Gemini for {stock}")
            return "No analysis data available."
            
    except Exception as e:
        logger.error(f"Gemini API error: {type(e).__name__}: {str(e)}")
        return "No analysis data available."


def validate_ticker(ticker: str) -> bool:
    """
    Validate ticker format.
    
    Args:
        ticker: Stock ticker symbol
        
    Returns:
        True if valid format, False otherwise
    """
    if not ticker:
        return False
    
    # Valid formats: AAPL, RELIANCE.NS, TCS.NS, etc.
    ticker_clean = ticker.upper().strip()
    
    # Check basic format (alphanumeric and dots)
    if not all(c.isalnum() or c == '.' for c in ticker_clean):
        return False
    
    # Min 1 char, max 10 chars (including dot)
    if len(ticker_clean) < 1 or len(ticker_clean) > 10:
        return False
    
    return True


def extract_ticker_from_question(question: str) -> str:
    """
    Extract ticker from ambiguous references in question.
    
    Handles patterns like:
    - "what about msft?" → MSFT
    - "should i buy this?" → extract from question context
    - "compare msft vs aapl" → extract first ticker
    
    Args:
        question: User's question
        
    Returns:
        Extracted ticker if found, empty string otherwise
    """
    import re
    
    if not question:
        return ""
    
    # Pattern 1: "ticker" mentioned in context (e.g., "what about msft?")
    # Match capitalized words or words after "about", "buy", "compare"
    patterns = [
        r'(?:about|buy|compare)\s+([A-Z]{1,5}(?:\.[A-Z]{2})?)',  # "about MSFT", "buy MSFT.NS"
        r'^([A-Z]{1,5}(?:\.[A-Z]{2})?)\s*(?:\?|is|was)',  # "MSFT is", "AAPL?"
        r'([A-Z]{1,5}(?:\.[A-Z]{2})?)\s+(?:rally|crash|rise|fall|jump)',  # "MSFT rally", "AAPL crash"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, question, re.IGNORECASE)
        if match:
            ticker = match.group(1).upper()
            if validate_ticker(ticker):
                logger.info(f"Extracted ticker from question: {ticker}")
                return ticker
    
    return ""


def compare_stocks(question: str, analysis1: Dict, analysis2: Dict) -> str:
    """
    Compare two stocks and generate comparison.
    Uses deterministic logic first, then Gemini for nuanced analysis.
    
    Args:
        question: User's comparison question
        analysis1: First stock analysis
        analysis2: Second stock analysis
        
    Returns:
        Comparison analysis
    """
    
    if not all([question, analysis1, analysis2]):
        return "Unable to compare stocks. Missing analysis data."
    
    # Validate both analysis datasets
    if not _validate_analysis_data(analysis1):
        logger.warning(f"Incomplete stock 1 analysis data. Analysis: {analysis1}")
        return "Unable to compare. First stock analysis data is incomplete."
    
    if not _validate_analysis_data(analysis2):
        logger.warning(f"Incomplete stock 2 analysis data. Analysis: {analysis2}")
        return "Unable to compare. Second stock analysis data is incomplete."
    
    try:
        ticker1 = analysis1.get('stock', 'Stock 1')
        ticker2 = analysis2.get('stock', 'Stock 2')
        conf1 = analysis1.get('confidence', 0)
        conf2 = analysis2.get('confidence', 0)
        signals1 = analysis1.get('signals_triggered', [])
        signals2 = analysis2.get('signals_triggered', [])
        
        # DETERMINISTIC LOGIC: Check if stocks are equivalent (same confidence, same signal count)
        if conf1 == conf2 and len(signals1) == len(signals2) and len(signals1) == 0:
            logger.info(f"Deterministic: {ticker1} and {ticker2} have no clear difference")
            return f"""Decision: NO CLEAR WINNER

Why:
- {ticker1}: {conf1}% with no momentum
- {ticker2}: {conf2}% with no momentum
- Insight: Both lack clear trading signals

Next Step:
Wait for stronger momentum to emerge before deciding"""
        
        comparison_data = f"""
STOCK 1: {ticker1}
- Confidence: {conf1}% ({get_confidence_label(conf1)})
- Action: {analysis1.get('action', 'N/A')}
- Signals: {', '.join(signals1) if signals1 else 'None'}
- Opportunity: {analysis1.get('opportunity_level', 'N/A')}

STOCK 2: {ticker2}
- Confidence: {conf2}% ({get_confidence_label(conf2)})
- Action: {analysis2.get('action', 'N/A')}
- Signals: {', '.join(signals2) if signals2 else 'None'}
- Opportunity: {analysis2.get('opportunity_level', 'N/A')}
"""
        
        # System prompt - STRICT COMPARISON ENGINE
        system_prompt = f"""You are a STRICT financial decision engine comparing two stocks.

HARD RULES:
1. ONLY use provided data
2. Each line on new line
3. NO compression
4. Deterministic based on signals + confidence
5. Replace "no signals" with "no clear momentum"

OUTPUT FORMAT (MANDATORY):

Decision: <WINNER or NO CLEAR WINNER>

Why:
- {ticker1}: <confidence>% with <signals>
- {ticker2}: <confidence>% with <signals>
- Insight: <reason for choice>

Next Step:
<ONE specific action>

RULES:
- Max 7 lines total
- Keep format rigid
- Be direct and confident
- If no signals: write "no clear momentum"

Example:

Decision: AAPL over MSFT

Why:
- AAPL: 65% with 3 momentum signals
- MSFT: 52% with no clear momentum
- Insight: AAPL shows stronger trading setup

Next Step:
Enter AAPL on next dip to support

You are deterministic. Not chatbot."""
        
        prompt = f"""USER QUESTION: {question}

COMPARATIVE DATA:
{comparison_data}

Which stock is better based on this data?"""
        
        logger.info(f"Comparing {ticker1} vs {ticker2} with Gemini")
        
        client = genai.GenerativeModel(MODEL, system_instruction=system_prompt)
        response = client.generate_content(
            prompt,
            generation_config={"temperature": 0.3}  # Deterministic comparison
        )
        
        if response and response.text:
            return response.text.strip()
        else:
            return "Unable to generate comparison at this moment."
            
    except Exception as e:
        logger.error(f"Comparison error: {type(e).__name__}: {str(e)}")
        return f"Error generating comparison: {str(e)}"


def analyze_portfolio_with_gemini(question: str, portfolio_data: Dict) -> str:
    """
    Analyze portfolio using Gemini AI.
    
    Args:
        question: User's portfolio question
        portfolio_data: Portfolio analysis result
        
    Returns:
        Gemini-generated portfolio advice
    """
    
    if not all([question, portfolio_data]):
        return "Unable to analyze portfolio. Missing data."
    
    # Validate portfolio data contains essential fields
    if not isinstance(portfolio_data, dict):
        logger.warning("Portfolio data is not a dictionary")
        return "Unable to analyze portfolio. Invalid data format."
    
    required_portfolio_fields = ['portfolio_size', 'risk_score', 'avg_correlation', 'diversification']
    if not all(field in portfolio_data for field in required_portfolio_fields):
        logger.warning(f"Incomplete portfolio data. Missing fields. Portfolio: {portfolio_data}")
        return "Unable to analyze portfolio. Analysis data is incomplete. Ensure risk score, correlation, and diversification are calculated."
    
    try:
        risk_score = portfolio_data.get('risk_score', 0)
        risk_label = "High" if risk_score > 70 else "Moderate" if risk_score > 40 else "Low"
        
        portfolio_context = f"""
Portfolio Size: {portfolio_data.get('portfolio_size', 'N/A')} stocks
Risk Score: {risk_score}/100 ({risk_label})
Average Correlation: {portfolio_data.get('avg_correlation', 'N/A')}
Diversification: {portfolio_data.get('diversification', 'N/A')}
Suggestion: {portfolio_data.get('rebalance_suggestion', 'N/A')}
"""
        
        system_prompt = """You are a portfolio advisor analyzing investment portfolios.

CORE MANDATE:
Use provided data. MUST follow exact format below.

MANDATORY RULES:
1. STRICT format - no deviations
2. Each section on new line
3. Simple investor language
4. Max 7 lines total
5. Decision first, then analysis

PORTFOLIO HEALTH LEVELS:
- Risk > 70: HIGH RISK
- Risk 40-70: IMPROVE
- Risk < 40: GOOD

OUTPUT FORMAT (MANDATORY):

Decision: <GOOD / IMPROVE / HIGH RISK>

Why:
- Risk: <score/100 + assessment>
- Diversification: <assessment>

Next Step:
<ONE specific action>

Example:

Decision: IMPROVE

Why:
- Risk: 58/100 - moderately concentrated
- Diversification: Add 2-3 defensive stocks

Next Step:
Add FMCG or Pharma to balance tech exposure

Be direct. Follow format exactly."""
        
        prompt = f"""USER QUESTION: {question}

PORTFOLIO METRICS:
{portfolio_context}

Analyze this portfolio in simple, investor-friendly language. What's the current state and what should the investor know?"""
        
        logger.info("Analyzing portfolio with Gemini")
        
        client = genai.GenerativeModel(MODEL, system_instruction=system_prompt)
        response = client.generate_content(
            prompt,
            generation_config={"temperature": 0.5}  # Balanced between deterministic and conversational
        )
        
        if response and response.text:
            return response.text.strip()
        else:
            return "Unable to generate portfolio analysis at this moment."
            
    except Exception as e:
        logger.error(f"Portfolio analysis error: {type(e).__name__}: {str(e)}")
        return f"Error analyzing portfolio: {str(e)}"


def analyze_stock_portfolio_combo(question: str, stock_analysis: Dict, portfolio_data: Dict, ticker: str) -> str:
    """
    Analyze a stock in the context of portfolio fit.
    Combines stock analysis with portfolio context for holistic advice.
    
    Args:
        question: User's question about stock + portfolio
        stock_analysis: Stock analysis data from analyze_stock()
        portfolio_data: Portfolio analysis data
        ticker: The stock ticker being analyzed
        
    Returns:
        Combined analysis showing stock fit in portfolio context
    """
    
    if not all([question, stock_analysis, portfolio_data, ticker]):
        return "Unable to analyze. Missing data."
    
    if not _validate_analysis_data(stock_analysis):
        logger.warning(f"Incomplete stock analysis for combo")
        return "Unable to analyze stock in portfolio context. Incomplete stock data."
    
    try:
        stock_conf = stock_analysis.get('confidence', 0)
        stock_action = stock_analysis.get('action', 'AVOID')
        signals = stock_analysis.get('signals_triggered', [])
        signals_text = ', '.join(signals) if signals else 'None'
        
        risk_score = portfolio_data.get('risk_score', 0)
        risk_label = "High" if risk_score > 70 else "Moderate" if risk_score > 40 else "Low"
        diversification = portfolio_data.get('diversification', 'N/A')
        
        combo_context = f"""
STOCK: {ticker}
- Action: {stock_action}
- Confidence: {stock_conf}%
- Signals: {signals_text}

PORTFOLIO:
- Risk Level: {risk_label} ({risk_score}/100)
- Diversification: {diversification}

QUESTION: {question}
"""
        
        system_prompt = """You are analyzing whether a stock fits into an investor's portfolio.

HARD RULES:
1. ONLY use provided stock + portfolio data
2. Each section on new line
3. NO compression
4. Direct and practical

OUTPUT FORMAT (MANDATORY):

Decision: <ADD / SKIP / WAIT>

Why:
- Stock: <confidence>% with <action> signal
- Portfolio: <risk assessment>
- Fit: <how stock matches portfolio needs>

Next Step:
<ONE specific action>

RULES:
- Max 7 lines
- Keep format rigid
- Consider both stock strength AND portfolio balance

Example:

Decision: SKIP FOR NOW

Why:
- NFLX: 45% confidence, HOLD signal
- Portfolio: Already high risk (71/100)
- Fit: Adding growth stock increases concentration risk

Next Step:
Consider defensive stocks to balance portfolio first

Be clear and practical."""
        
        prompt = f"""Analyze whether this stock fits this investor's portfolio.

{combo_context}

Should they add this stock to their portfolio now?"""
        
        logger.info(f"Analyzing {ticker} in portfolio context")
        
        client = genai.GenerativeModel(MODEL, system_instruction=system_prompt)
        response = client.generate_content(
            prompt,
            generation_config={"temperature": 0.4}  # Slightly higher for balanced context
        )
        
        if response and response.text:
            return response.text.strip()
        else:
            return "Unable to generate analysis at this moment."
            
    except Exception as e:
        logger.error(f"Stock-portfolio combo error: {type(e).__name__}: {str(e)}")
        return f"Error analyzing stock fit: {str(e)}"


def answer_general_question(question: str) -> str:
    """
    Answer general financial knowledge questions using Gemini.
    Trader-oriented, conversational, NOT textbook.
    STRICT enforcement of format and tone.
    
    Args:
        question: General finance question
        
    Returns:
        Conversational, trader-focused answer (strictly enforced)
    """
    
    if not question:
        return "Please ask a financial question."
    
    try:
        system_prompt = """You MUST answer like a experienced trader talking to another trader. NOT like a textbook.

🚫 FORBIDDEN (TEXTBOOK STYLE):
- "RSI (Relative Strength Index) is a momentum indicator that..."
- "RSI measures momentum on a scale of 0-100..."
- Any definition that starts with "is used to" or "is a"
- Academic explanations

✅ REQUIRED (TRADER STYLE):
- "RSI tells you if a stock is running out of buyers (overbought) or sellers (oversold)"
- Real action: "When RSI > 70, most traders are watching for pullbacks"
- Focus on: What does THIS mean for YOUR trading?

CORE MANDATE:
1. Talk like you're grabbing coffee with another trader
2. Assume they know basic finance (don't explain what stocks are)
3. Give practical trading insight in 1-2 sentences
4. Provide ONE real-world example of trading this concept
5. End with ONE action they can do TODAY

STRICT RULES:
- NO definitions ("X is a measure of...")
- NO textbook language
- NO generic advice ("do your own research")
- NO hedging ("it depends")
- Start with conversational opening
- Max 6 lines total

EXAMPLE - DO THIS:

For "What is RSI?":

✅ CORRECT:
"RSI just tells you if everyone's already piled in (overbought > 70) or if there's panic selling (oversold < 30).

When RSI > 70, the crowd's maxed out—so smart traders watch for a pullback. When it < 30, that's often a bounce opportunity.

Right now, check a stock you like on a chart and look at the RSI. If it's above 70, avoid chasing rallies."

❌ WRONG (TEXTBOOK):
"RSI (Relative Strength Index) measures momentum on a scale of 0-100..."

YOU MUST FOLLOW THE CORRECT STYLE."""
        
        prompt = f"""USER QUESTION: {question}

CRITICAL: Answer this exactly like experienced traders would explain it to each other.
Talk practical, not textbook. 
Assume basic finance knowledge.
Give ONE action they can take today.
Max 6 lines."""
        
        logger.info("Answering general finance question with Gemini (STRICT trader mode)")
        
        client = genai.GenerativeModel(MODEL, system_instruction=system_prompt)
        response = client.generate_content(
            prompt,
            generation_config={"temperature": 0.2}  # VERY low for strict enforcement
        )
        
        if response and response.text:
            result = response.text.strip()
            logger.debug(f"Answer: {result[:100]}...")
            return result
        else:
            return "Unable to generate answer at this moment."
            
    except Exception as e:
        logger.error(f"General question error: {type(e).__name__}: {str(e)}")
        return "Error generating answer. Try asking differently."
