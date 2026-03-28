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