import React, { useState } from "react";
import "./VideoEngine.css";

function VideoEngine() {
  const [ticker, setTicker] = useState("RELIANCE.NS");
  const [loading, setLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState(null);

  const STOCKS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "AAPL",
    "MSFT",
    "TSLA"
  ];

  const generateVideo = async () => {
    setLoading(true);
    setVideoUrl(null);

    try {
      const response = await fetch(
        `http://localhost:8000/generate-video?ticker=${ticker}`
      );

      if (!response.ok) throw new Error("Server error");
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setVideoUrl(url);

    } catch (err) {
      console.error(err);
      alert("Terminal Error: Synthesis protocol failed. Check backend connectivity.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="video-container">
      {/* HEADER */}
      <div className="video-header">
        <h3>
          <span className="material-symbols-outlined" style={{ color: 'var(--primary)' }}>videocam</span>
          AI Market Synthesis
        </h3>
        <span className="video-subtitle">
          Generate Dynamic Intelligence Visualisation
        </span>
      </div>

      {/* CONTROLS */}
      <div className="video-controls">
        <select value={ticker} onChange={(e) => setTicker(e.target.value)} disabled={loading}>
          {STOCKS.map((s) => (
            <option key={s}>{s}</option>
          ))}
        </select>

        <button onClick={generateVideo} disabled={loading}>
          <span className="material-symbols-outlined">
            {loading ? 'sync' : 'movie_filter'}
          </span>
          {loading ? 'Synthesizing...' : 'Generate Matrix'}
        </button>
      </div>

      {/* LOADING */}
      {loading && (
        <div className="video-loading">
          <div className="spinner"></div>
          <p style={{ color: 'var(--on-surface-variant)', fontSize: '14px' }}>
            Compiling market data & rendering visualisation streams...
          </p>
        </div>
      )}

      {/* VIDEO OUTPUT */}
      {videoUrl && (
        <div className="video-player">
          <video
            controls
            autoPlay
            src={videoUrl}
          />
        </div>
      )}
    </div>
  );
}

export default VideoEngine;