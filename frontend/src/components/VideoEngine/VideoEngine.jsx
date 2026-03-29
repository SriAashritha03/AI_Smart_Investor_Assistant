import React, { useState } from "react";
import "./VideoEngine.css";
import { generateStructuredVideo, generateLegacyVideo } from "../../services/api";

function VideoEngine() {
  const [ticker, setTicker] = useState("MSFT");
  const [videoType, setVideoType] = useState("structured"); // structured | legacy
  const [loading, setLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState(null);
  const [videoMetadata, setVideoMetadata] = useState(null);
  const [error, setError] = useState(null);

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
    setVideoMetadata(null);
    setError(null);

    try {
      let blob, metadata;

      if (videoType === "structured") {
        // Generate structured video with audio sync
        const result = await generateStructuredVideo(ticker);
        if (!result.success) {
          throw new Error(result.error || "Structured video generation failed");
        }
        blob = result.videoBlob;
        metadata = result.metadata;
      } else {
        // Generate legacy video
        blob = await generateLegacyVideo(ticker);
        metadata = {
          duration: "~8s",
          frameCount: 1,
          audioSync: "Standard",
        };
      }

      const url = URL.createObjectURL(blob);
      setVideoUrl(url);
      setVideoMetadata(metadata);

    } catch (err) {
      console.error(err);
      setError(err.message || "Video generation failed");
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

        {/* VIDEO TYPE SELECTOR */}
        <div className="video-type-selector">
          <label className={videoType === "structured" ? "active" : ""}>
            <input
              type="radio"
              name="videoType"
              value="structured"
              checked={videoType === "structured"}
              onChange={(e) => setVideoType(e.target.value)}
              disabled={loading}
            />
            <span className="material-symbols-outlined">stimulus</span>
            Structured (Synced)
          </label>
          <label className={videoType === "legacy" ? "active" : ""}>
            <input
              type="radio"
              name="videoType"
              value="legacy"
              checked={videoType === "legacy"}
              onChange={(e) => setVideoType(e.target.value)}
              disabled={loading}
            />
            <span className="material-symbols-outlined">movie</span>
            Legacy
          </label>
        </div>

        <button onClick={generateVideo} disabled={loading}>
          <span className="material-symbols-outlined">
            {loading ? 'sync' : 'movie_filter'}
          </span>
          {loading ? 'Synthesizing...' : 'Generate Matrix'}
        </button>
      </div>

      {/* ERROR MESSAGE */}
      {error && (
        <div className="video-error">
          <span className="material-symbols-outlined">error</span>
          <p>{error}</p>
        </div>
      )}

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
        <div className="video-output">
          {/* METADATA DISPLAY */}
          {videoMetadata && (
            <div className="video-metadata">
              <div className="metadata-item">
                <span className="material-symbols-outlined">schedule</span>
                <span>Duration: <strong>{videoMetadata.duration || "~40s"}</strong></span>
              </div>
              <div className="metadata-item">
                <span className="material-symbols-outlined">image_frame</span>
                <span>Frames: <strong>{videoMetadata.frameCount || "3"}</strong></span>
              </div>
              <div className="metadata-item">
                <span className="material-symbols-outlined">done_all</span>
                <span>Audio Sync: <strong>{videoMetadata.audioSync || "✓ Synchronized"}</strong></span>
              </div>
            </div>
          )}

          {/* VIDEO PLAYER */}
          <div className="video-player">
            <video
              controls
              autoPlay
              src={videoUrl}
            />
          </div>

          {/* INSIGHTS SUMMARY */}
          {videoMetadata && videoMetadata.insights && (
            <div className="video-insights">
              <h4>📊 AI Analysis Summary</h4>
              {videoMetadata.insights.confidence && (
                <p><strong>Confidence:</strong> {videoMetadata.insights.confidence}</p>
              )}
              {videoMetadata.insights.trend && (
                <p><strong>Trend:</strong> {videoMetadata.insights.trend}</p>
              )}
              {videoMetadata.insights.recommendation && (
                <p><strong>Recommendation:</strong> {videoMetadata.insights.recommendation}</p>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default VideoEngine;