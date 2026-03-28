import React, { useState } from "react";
import { analyzePortfolio } from "../../services/api";
import "./Portfolio.css";

function Portfolio() {
  const [selectedStock, setSelectedStock] = useState("");
  const [stocks, setStocks] = useState([]);
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  // 👉 Dropdown options (can later come from API)
  const STOCK_OPTIONS = [
    "AAPL",
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "MSFT",
    "TSLA"
  ];

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
      alert("Select at least 2 stocks");
      return;
    }

    setLoading(true);
    const res = await analyzePortfolio(stocks);
    setData(res);
    setLoading(false);
  };

  const getRiskColor = (risk) => {
    if (risk >= 70) return "#ef4444";
    if (risk >= 40) return "#f59e0b";
    return "#10b981";
  };

  return (
    <div className="portfolio-container">

      {/* HEADER */}
      <div className="portfolio-header">
        <h3>📊 Portfolio Analyzer</h3>
        <span className="info-subtitle">Select stocks & analyze</span>
      </div>

      {/* DROPDOWN */}
      <div className="dropdown-wrapper">
        <select
          value={selectedStock}
          onChange={(e) => setSelectedStock(e.target.value)}
        >
          <option value="">Select Stock</option>
          {STOCK_OPTIONS.map((stock) => (
            <option key={stock} value={stock}>
              {stock}
            </option>
          ))}
        </select>

        <button onClick={addStock}>Add</button>
      </div>

      {/* SELECTED CHIPS */}
      <div className="stock-chip-container">
        {stocks.map((stock) => (
          <div key={stock} className="stock-chip">
            {stock}
            <span onClick={() => removeStock(stock)}>✕</span>
          </div>
        ))}
      </div>

      {/* ANALYZE */}
      <button className="analyze-btn" onClick={handleAnalyze}>
        Analyze Portfolio
      </button>

      {/* LOADING */}
      {loading && <p className="loading">Analyzing...</p>}

      {/* RESULT */}
      {data && data.success && (
        <div className="portfolio-grid">

          <div className="portfolio-card">
            <span className="card-label">Risk Score</span>
            <span className="card-value">{data.risk_score}%</span>

            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{
                  width: `${data.risk_score}%`,
                  backgroundColor: getRiskColor(data.risk_score)
                }}
              ></div>
            </div>
          </div>

          <div className="portfolio-card">
            <span className="card-label">Portfolio Size</span>
            <span className="card-value">{data.portfolio_size}</span>
          </div>

          <div className="portfolio-card">
            <span className="card-label">Correlation</span>
            <span className="card-value">{data.avg_correlation}</span>
          </div>

          <div className="portfolio-card">
            <span className="card-label">Diversification</span>
            <span className="card-value">{data.diversification}</span>
          </div>

        </div>
      )}

      {/* SUGGESTION */}
      {data && data.success && (
        <div className="portfolio-suggestion">
          <span className="suggestion-label">Suggestion</span>
          <p>{data.rebalance_suggestion}</p>
        </div>
      )}
    </div>
  );
}

export default Portfolio;