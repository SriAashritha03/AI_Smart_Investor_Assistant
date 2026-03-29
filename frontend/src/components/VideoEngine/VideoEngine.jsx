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

      // ✅ check response
      if (!response.ok) {
        throw new Error("Server error");
      }

      // ✅ convert to blob
      const blob = await response.blob();

      // ✅ create URL
      const url = URL.createObjectURL(blob);

      setVideoUrl(url);

    } catch (err) {
      console.error(err);
      alert("Failed to generate video");
    }

    setLoading(false);
  };

  return (
    <div className="video-container">

      {/* HEADER */}
      <div className="video-header">
        <h3>🎬 AI Market Video Engine</h3>
        <span className="video-subtitle">
          Auto-generate market insights video
        </span>
      </div>

      {/* CONTROLS */}
      <div className="video-controls">
        <select value={ticker} onChange={(e) => setTicker(e.target.value)}>
          {STOCKS.map((s) => (
            <option key={s}>{s}</option>
          ))}
        </select>

        <button onClick={generateVideo}>
          Generate Video
        </button>
      </div>

      {/* LOADING */}
      {loading && (
        <div className="video-loading">
          <div className="spinner"></div>
          <p>Generating AI video...</p>
        </div>
      )}

      {/* VIDEO OUTPUT */}
      {videoUrl && (
        <div className="video-player">
          <video
            controls
            src={videoUrl}
            style={{
              width: "100%",
              maxHeight: "400px",
              background: "black"
            }}
          />
        </div>
      )}
    </div>
  );
}

export default VideoEngine;