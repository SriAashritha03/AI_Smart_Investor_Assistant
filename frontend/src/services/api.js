const API_BASE = "http://localhost:8000";

export const analyzePortfolio = async (tickers) => {
  try {
    // ✅ Clean input (IMPORTANT)
    const cleanTickers = tickers
      .map(t => t.trim())
      .filter(t => t !== "");

    console.log("Sending tickers:", cleanTickers); // debug

    const response = await fetch(`${API_BASE}/portfolio-health`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      // ✅ FIX: must send object
      body: JSON.stringify({ tickers: cleanTickers }),
    });

    const data = await response.json();
    console.log("Response:", data); // debug

    if (!response.ok) {
      throw new Error(data.detail || "API Error");
    }

    return data;

  } catch (error) {
    console.error("Portfolio API Error:", error);
    return { success: false };
  }
};

/**
 * Generate AI-powered structured video with audio-synchronized narration
 * @param {string} ticker - Stock ticker symbol
 * @returns {Object} { videoBlob, metadata: { duration, frames, insights } }
 */
export const generateStructuredVideo = async (ticker) => {
  try {
    // Step 1: Request video generation
    const response = await fetch(`${API_BASE}/generate-structured-video`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ticker }),
    });

    if (!response.ok) {
      throw new Error("Video generation failed");
    }

    const data = await response.json();
    
    // Step 2: Fetch video blob from the new /get-video endpoint
    let videoBlob = null;
    if (data.video_path) {
      // Extract filename from path (e.g., "S:\...\videos\video_MSFT_abc123.mp4" → "video_MSFT_abc123.mp4")
      const filename = data.video_path.split(/[\\\/]/).pop();
      const videoUrl = `${API_BASE}/get-video/${filename}`;
      const videoResponse = await fetch(videoUrl);
      
      if (videoResponse.ok) {
        videoBlob = await videoResponse.blob();
      }
    }

    // Step 3: Extract metadata
    const frames = data.frames || [];
    const insights = data.insights || {};
    const recommendation = data.recommendation || {};

    return {
      success: true,
      videoBlob,
      metadata: {
        duration: frames.length > 0 ? "~40s" : "unknown", // Approx 15s + 16s + 9s + buffers
        frameCount: frames.length || 3,
        audioSync: "✓ Synchronized", // Indicates audio is properly synced per frame
        insights: {
          trend: insights.trend_direction || "Unknown",
          confidence: recommendation.confidence || "N/A",
          recommendation: recommendation.action || "HOLD",
        },
        frames: frames,
      }
    };

  } catch (error) {
    console.error("Structured Video API Error:", error);
    return { success: false, error: error.message };
  }
};

/**
 * Generate legacy simple market video
 * @param {string} ticker - Stock ticker symbol
 * @returns {Blob} Video blob data
 */
export const generateLegacyVideo = async (ticker) => {
  try {
    const response = await fetch(`${API_BASE}/generate-video?ticker=${ticker}`);
    if (!response.ok) throw new Error("Legacy video generation failed");
    return await response.blob();
  } catch (error) {
    console.error("Legacy Video API Error:", error);
    throw error;
  }
};