import React, { useState, useEffect } from "react";
import { analyzePortfolio } from "../../services/api";
import { getAvailableStocks } from "../../services/stockApi";
import "./Portfolio.css";

function Portfolio() {
  const [selectedStock, setSelectedStock] = useState("");
  const [stocks, setStocks] = useState([]);
  const [availableStocks, setAvailableStocks] = useState([]);
  const [stocksLoading, setStocksLoading] = useState(true);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [portfolioFitStock, setPortfolioFitStock] = useState("");
  const [fitAnalysis, setFitAnalysis] = useState(null);

  // Fetch available stocks on mount
  useEffect(() => {
    const fetchStocks = async () => {
      try {
        const response = await getAvailableStocks();
        setAvailableStocks(response.stocks || []);
      } catch (error) {
        console.error('Failed to fetch stocks:', error);
        // Fallback to default stocks if API fails
        setAvailableStocks([
          { symbol: 'AAPL', name: 'Apple Inc.' },
          { symbol: 'RELIANCE.NS', name: 'Reliance Industries' },
          { symbol: 'TCS.NS', name: 'Tata Consultancy Services' },
          { symbol: 'INFY.NS', name: 'Infosys Limited' },
          { symbol: 'MSFT', name: 'Microsoft Corporation' },
          { symbol: 'TSLA', name: 'Tesla Inc.' },
        ]);
      } finally {
        setStocksLoading(false);
      }
    };

    fetchStocks();
  }, []);

  // ➕ Add stock
  const addStock = () => {
    if (selectedStock && !stocks.includes(selectedStock)) {
      setStocks([...stocks, selectedStock]);
    }
    setSelectedStock("");
  };

  // ❌ Remove stock
  const removeStock = (stock) => {
    setStocks(stocks.filter((s) => s !== stock));
  };

  // 📊 Analyze
  const handleAnalyze = async () => {
    if (stocks.length < 2) {
      alert("Select at least 2 stocks for portfolio analysis");
      return;
    }

    setLoading(true);
    try {
      const res = await analyzePortfolio(stocks);
      setData(res);
    } catch (err) {
      console.error("Portfolio analysis error:", err);
    } finally {
      setLoading(false);
    }
  };

  // 🎯 Portfolio Fit Analysis
  const handlePortfolioFit = async () => {
    if (!portfolioFitStock || !data) return;
    
    try {
      // Call backend smart fit analysis
      const response = await fetch('http://localhost:8000/portfolio-fit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          tickers: stocks,
          test_stock: portfolioFitStock
        })
      });

      const fitResult = await response.json();
      
      if (fitResult.success) {
        setFitAnalysis(fitResult);
      } else {
        console.error('Fit analysis error:', fitResult.error);
        setFitAnalysis({
          stock: portfolioFitStock,
          fit_score: 0,
          fit_level: "Error",
          reasons: [fitResult.error || "Could not analyze fit"]
        });
      }
    } catch (err) {
      console.error('Portfolio fit error:', err);
      setFitAnalysis({
        stock: portfolioFitStock,
        fit_score: 0,
        fit_level: "Error",
        reasons: ["Network error - could not analyze fit"]
      });
    }
  };

  const getActionBadgeColor = (action) => {
    switch (action) {
      case "BUY": return "#4ae176";
      case "SELL": return "#ff5451";
      default: return "#adc6ff";
    }
  };

  const getSentimentBadgeColor = (sentiment) => {
    switch (sentiment) {
      case "Positive": return "#4ae176";
      case "Negative": return "#ff5451";
      default: return "#adc6ff";
    }
  };

  return (
    <div className="portfolio-container">
      {/* HEADER */}
      <div className="portfolio-header">
        <h3><span className="material-symbols-outlined">account_balance_wallet</span>Portfolio Intelligence</h3>
        <span className="info-subtitle">AI-Powered Asset Analysis & Recommendations</span>
      </div>

      {/* SELECTION SECTION */}
      <div className="selection-section">
        <div className="dropdown-wrapper">
          <select
            value={selectedStock}
            onChange={(e) => setSelectedStock(e.target.value)}
            disabled={stocksLoading || loading}
          >
            <option value="">{stocksLoading ? 'Initialising Assets...' : 'Choose Asset to Add'}</option>
            {availableStocks.map((stock) => (
              <option key={stock.symbol} value={stock.symbol}>
                {stock.symbol} — {stock.name || ''}
              </option>
            ))}
          </select>
          <button className="add-btn" onClick={addStock} disabled={!selectedStock || loading}>
            <span className="material-symbols-outlined">add</span>
          </button>
        </div>

        {/* SELECTED CHIPS */}
        <div className="stock-chip-container">
          {stocks.length > 0 ? (
            stocks.map((stock) => (
              <div key={stock} className="stock-chip">
                {stock}
                <span onClick={() => removeStock(stock)}>
                  <span className="material-symbols-outlined" style={{ fontSize: '18px' }}>close</span>
                </span>
              </div>
            ))
          ) : (
            <p style={{ fontSize: '12px', color: 'var(--on-surface-variant)', opacity: 0.6 }}>No assets selected for analysis</p>
          )}
        </div>

        {/* ANALYZE BUTTON */}
        <button 
          className="analyze-btn" 
          onClick={handleAnalyze} 
          disabled={stocks.length < 2 || loading}
        >
          <span className="material-symbols-outlined">{loading ? 'sync' : 'calculate'}</span>
          {loading ? 'Analyzing Portfolio...' : 'Check Portfolio Health'}
        </button>
      </div>

      {/* PORTFOLIO ANALYSIS RESULTS */}
      {data && data.success && !loading && (
        <>
          {/* PORTFOLIO SUMMARY */}
          <div className="portfolio-grid analysis-grid">
            <div className="portfolio-card">
              <span className="card-label">Risk Score</span>
              <span className="card-value">{data.portfolio_summary.risk_score}%</span>
              <div className="progress-bar">
                <div
                  className="progress-fill"
                  style={{ width: `${data.portfolio_summary.risk_score}%` }}
                ></div>
              </div>
            </div>

            <div className="portfolio-card">
              <span className="card-label">Avg Confidence</span>
              <span className="card-value">{data.portfolio_summary.avg_confidence}%</span>
              <p style={{ fontSize: '9px', color: 'var(--on-surface-variant)', margin: '8px 0 0', lineHeight: '1.3' }}>
                {data.portfolio_summary.confidence_insight}
              </p>
            </div>

            <div className="portfolio-card">
              <span className="card-label">Diversification</span>
              <span className="card-value">{data.portfolio_summary.avg_correlation.toFixed(2)}</span>
              <p style={{ fontSize: '10px', color: 'var(--on-surface-variant)', margin: '8px 0 0' }}>
                {data.portfolio_summary.diversification === "High" ? "✅ Good (low correlation)" : data.portfolio_summary.diversification === "Moderate" ? "⚠️ Moderate" : "❌ Low (high correlation)"}
              </p>
            </div>

            <div className="portfolio-card">
              <span className="card-label">Portfolio Size</span>
              <span className="card-value">{data.portfolio_summary.portfolio_size}</span>
              <p style={{ fontSize: '10px', color: 'var(--on-surface-variant)', margin: '8px 0 0' }}>
                {data.portfolio_summary.action_distribution.buy} Buy / {data.portfolio_summary.action_distribution.sell} Sell / {data.portfolio_summary.action_distribution.hold} Hold
              </p>
            </div>
          </div>

          {/* PORTFOLIO INSIGHT */}
          {data.insight && (
            <div className="portfolio-insight">
              <span className="insight-label">
                <span className="material-symbols-outlined">psychology</span>
                Portfolio Intelligence
              </span>
              <p>{data.insight}</p>
            </div>
          )}

          {/* STOCK BREAKDOWN TABLE */}
          {data.stock_breakdown && data.stock_breakdown.length > 0 && (
            <div className="stock-breakdown-section">
              <h4 className="section-title">
                <span className="material-symbols-outlined">table_rows</span>
                Stock Breakdown
              </h4>
              <div className="breakdown-table">
                <div className="table-header">
                  <div className="col col-stock">Stock</div>
                  <div className="col col-sector">Sector</div>
                  <div className="col col-confidence">Confidence</div>
                  <div className="col col-action">Action</div>
                  <div className="col col-signals">Signals</div>
                  <div className="col col-sentiment">Sentiment</div>
                </div>
                {data.stock_breakdown.map((stock, idx) => (
                  <div key={idx} className="table-row">
                    <div className="col col-stock"><strong>{stock.stock}</strong></div>
                    <div className="col col-sector">{stock.sector}</div>
                    <div className="col col-confidence">
                      <span className="confidence-badge">{stock.confidence}%</span>
                    </div>
                    <div className="col col-action">
                      <span 
                        className="action-badge"
                        style={{ 
                          background: `${getActionBadgeColor(stock.action)}20`,
                          color: getActionBadgeColor(stock.action)
                        }}
                      >
                        {stock.action}
                      </span>
                    </div>
                    <div className="col col-signals">
                      <span className="signals-text">
                        {stock.signals.length > 0 ? stock.signals.length + " signals" : "None"}
                      </span>
                    </div>
                    <div className="col col-sentiment">
                      <span 
                        className="sentiment-badge"
                        style={{ 
                          background: `${getSentimentBadgeColor(stock.news_sentiment)}20`,
                          color: getSentimentBadgeColor(stock.news_sentiment)
                        }}
                      >
                        {stock.news_sentiment}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* PORTFOLIO WEAKNESSES */}
          {data.weaknesses && data.weaknesses.length > 0 && (
            <div className="weaknesses-section">
              <h4 className="section-title">
                <span className="material-symbols-outlined">warning</span>
                Portfolio Weaknesses
              </h4>
              <ul className="weakness-list">
                {data.weaknesses.map((weakness, idx) => (
                  <li key={idx}>
                    <span className="bullet">▪</span>
                    <span>{weakness}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* AI RECOMMENDATIONS */}
          {data.recommendations && (
            <div className="recommendations-section">
              <h4 className="section-title">
                <span className="material-symbols-outlined">smart_toy</span>
                AI Recommendations
              </h4>
              <div className="recommendation-content">
                <div className="rec-card">
                  <span className="rec-label">
                    <span className="material-symbols-outlined" style={{ color: '#4ae176' }}>add_circle</span>
                    Add to Portfolio
                  </span>
                  <div className="rec-items">
                    {data.recommendations.add.length > 0 ? (
                      data.recommendations.add.map((stock, idx) => (
                        <span key={idx} className="stock-tag add-tag">{stock}</span>
                      ))
                    ) : (
                      <p style={{ fontSize: '12px', color: 'var(--on-surface-variant)' }}>No additions recommended</p>
                    )}
                  </div>
                </div>

                <div className="rec-card">
                  <span className="rec-label">
                    <span className="material-symbols-outlined" style={{ color: '#ff9800' }}>arrow_downward</span>
                    Reduce from Portfolio
                  </span>
                  <div className="rec-items">
                    {(data.recommendations.reduce || data.recommendations.remove || []).length > 0 ? (
                      (data.recommendations.reduce || data.recommendations.remove || []).map((stock, idx) => (
                        <span key={idx} className="stock-tag reduce-tag">{stock}</span>
                      ))
                    ) : (
                      <p style={{ fontSize: '12px', color: 'var(--on-surface-variant)' }}>No reductions recommended</p>
                    )}
                  </div>
                </div>

                {data.recommendations.monitor && data.recommendations.monitor.length > 0 && (
                  <div className="rec-card">
                    <span className="rec-label">
                      <span className="material-symbols-outlined" style={{ color: '#adc6ff' }}>visibility</span>
                      Monitor
                    </span>
                    <div className="rec-items">
                      {data.recommendations.monitor.map((stock, idx) => (
                        <span key={idx} className="stock-tag monitor-tag">{stock}</span>
                      ))}
                    </div>
                  </div>
                )}

                <div className="rec-reasoning">
                  <strong>Reasoning:</strong> {data.recommendations.reasoning}
                </div>
                <div className="rec-priority">
                  Priority: <strong>{data.recommendations.priority}</strong>
                </div>
              </div>
            </div>
          )}

          {/* PORTFOLIO FIT ANALYSIS */}
          <div className="portfolio-fit-section">
            <h4 className="section-title">
              <span className="material-symbols-outlined">fit_screen</span>
              Portfolio Fit Analysis
            </h4>
            <div className="fit-content">
              <p style={{ fontSize: '12px', color: 'var(--on-surface-variant)', marginBottom: '12px' }}>
                Test how well a new stock aligns with your current portfolio
              </p>
              <div className="fit-input-area">
                <select
                  value={portfolioFitStock}
                  onChange={(e) => setPortfolioFitStock(e.target.value)}
                  style={{ flex: 1, padding: '8px 12px', borderRadius: '8px', border: '1px solid rgba(66, 71, 84, 0.3)', background: 'var(--surface-container)', color: 'var(--on-surface)' }}
                >
                  <option value="">Select a stock to analyze fit...</option>
                  {availableStocks.map((stock) => (
                    <option key={stock.symbol} value={stock.symbol}>
                      {stock.symbol} — {stock.name}
                    </option>
                  ))}
                </select>
                <button
                  onClick={handlePortfolioFit}
                  disabled={!portfolioFitStock}
                  style={{
                    padding: '8px 16px',
                    marginLeft: '8px',
                    borderRadius: '8px',
                    background: 'var(--primary)',
                    color: 'var(--on-primary)',
                    border: 'none',
                    cursor: 'pointer',
                    fontWeight: '600'
                  }}
                >
                  Analyze Fit
                </button>
              </div>

              {fitAnalysis && (
                <div className="fit-result">
                  <p>
                    <strong>{fitAnalysis.stock}</strong> — <span style={{ color: fitAnalysis.fit_score > 70 ? '#4ae176' : fitAnalysis.fit_score > 50 ? '#adc6ff' : '#ff5451' }}>
                      {fitAnalysis.fit_level} ({fitAnalysis.fit_score}%)
                    </span>
                  </p>
                  <ul style={{ marginTop: '8px', fontSize: '12px' }}>
                    {fitAnalysis.reasons && fitAnalysis.reasons.map((reason, idx) => (
                      <li key={idx} style={{ color: 'var(--on-surface-variant)', marginBottom: '4px' }}>
                        {reason}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </>
      )}

      {data && !data.success && (
        <div style={{ color: '#ff5451', padding: '24px', textAlign: 'center' }}>
          <p>❌ {data.error}</p>
        </div>
      )}
    </div>
  );
}

export default Portfolio;