"""
AI-Driven Market Video Engine with Structured Insights

Generates professional video reports with:
- Visual insights overlay (trend, signals, momentum, outlook)
- News summary slide with market drivers
- Final recommendation slide
- AI-generated narration script
"""

import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, TextClip, CompositeVideoClip
from gtts import gTTS
from gtts.lang import tts_langs
import os
import uuid
import json
import logging
from typing import Dict, List, Tuple
from datetime import datetime

# Configure FFmpeg for moviepy
try:
    import imageio_ffmpeg
    os.environ['IMAGEIO_FFMPEG_EXE'] = imageio_ffmpeg.get_ffmpeg_exe()
    import moviepy.config
    moviepy.config.IMAGEMAGICK_BINARY = imageio_ffmpeg.get_ffmpeg_exe()
except:
    pass
# Ensure videos folder exists
VIDEOS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'videos')
os.makedirs(VIDEOS_DIR, exist_ok=True)
logger = logging.getLogger(__name__)


class StructuredVideoFrame:
    """Represents a single frame with text overlays and narration."""
    
    def __init__(self, frame_type: str, title: str, content: Dict, duration: float = 6.0):
        self.frame_type = frame_type  # 'analysis', 'news', 'recommendation'
        self.title = title
        self.content = content
        self.duration = duration
        self.image_path = None
        self.audio_path = None
        self.narration = ""


class AIInsightGenerator:
    """Generates structured AI insights from analysis data."""
    
    @staticmethod
    def extract_insights(analysis_data: Dict) -> Dict:
        """
        Extract key insights from analysis data.
        
        Args:
            analysis_data: Complete analysis from analyzer.py
            
        Returns:
            Dict with trend, signals, momentum, outlook
        """
        try:
            signals_triggered = analysis_data.get("signals_triggered", [])
            confidence = analysis_data.get("confidence", 50)
            action = analysis_data.get("action", "HOLD")
            opportunity_level = analysis_data.get("opportunity_level", "Weak")
            chart_patterns = analysis_data.get("chart_patterns", {})
            news_sentiment = analysis_data.get("news_sentiment", {})
            
            # Determine trend direction
            bullish_patterns = analysis_data.get("bullish_patterns", [])
            bearish_patterns = analysis_data.get("bearish_patterns", [])
            
            if bearish_patterns and len(bearish_patterns) > 0:
                trend = "🔴 BEARISH"
                trend_direction = "Downtrend"
            elif bullish_patterns and len(bullish_patterns) > 0:
                trend = "🟢 BULLISH"
                trend_direction = "Uptrend"
            elif "Uptrend" in signals_triggered:
                trend = "🟢 BULLISH"
                trend_direction = "Uptrend"
            else:
                trend = "🔵 NEUTRAL"
                trend_direction = "Consolidation"
            
            # Calculate momentum strength
            momentum_strength = confidence  # Use confidence as momentum indicator
            if momentum_strength >= 70:
                momentum_label = "STRONG"
            elif momentum_strength >= 50:
                momentum_label = "MODERATE"
            else:
                momentum_label = "WEAK"
            
            # Generate outlook
            if action == "BUY":
                outlook = "BULLISH - Entry opportunity"
            elif action == "SELL":
                outlook = "BEARISH - Exit recommended"
            else:
                outlook = "NEUTRAL - Watch for setup"
            
            return {
                "trend": trend,
                "trend_direction": trend_direction,
                "signal_detected": ", ".join(signals_triggered[:2]) if signals_triggered else "No signals",
                "momentum_strength": f"{momentum_label} ({momentum_strength}%)",
                "momentum_value": momentum_strength,
                "short_outlook": outlook,
                "action": action,
                "confidence": confidence,
                "opportunity": opportunity_level,
                "patterns_detected": len(chart_patterns.get("patterns_detected", [])),
                "sentiment": news_sentiment.get("sentiment_label", "Neutral"),
            }
        except Exception as e:
            logger.error(f"Error extracting insights: {str(e)}")
            return {
                "trend": "🔵 NEUTRAL",
                "trend_direction": "Unknown",
                "signal_detected": "Unable to detect",
                "momentum_strength": "WEAK (0%)",
                "momentum_value": 0,
                "short_outlook": "Insufficient data",
                "action": "HOLD",
                "confidence": 0,
                "opportunity": "Weak",
                "patterns_detected": 0,
                "sentiment": "Neutral",
            }
    
    @staticmethod
    def extract_news_headlines(analysis_data: Dict) -> List[str]:
        """Extract top 2-3 news headlines."""
        headlines = analysis_data.get("news_sentiment", {}).get("top_headlines", [])
        events = analysis_data.get("event_signals", {}).get("events_detected", [])
        
        result = headlines[:3]  # Top 3 headlines
        
        # Add event signals if available
        if events and len(result) < 3:
            for event in events[:2]:
                if len(result) < 3:
                    result.append(f"Event: {event}")
        
        return result if result else ["Market moving sideways", "No major news detected", "Monitor for breakouts"]
    
    @staticmethod
    def generate_recommendation(analysis_data: Dict) -> Dict:
        """Generate final recommendation with confidence and reasons."""
        action = analysis_data.get("action", "HOLD")
        confidence = analysis_data.get("confidence", 50)
        signals = analysis_data.get("signals_triggered", [])
        opportunity = analysis_data.get("opportunity_level", "Weak")
        sentiment = analysis_data.get("news_sentiment", {}).get("sentiment_label", "Neutral")
        
        # Generate 2-3 reasons based on analysis
        reasons = []
        
        if "Breakout" in signals:
            reasons.append("Breakout pattern confirmed")
        if "Uptrend" in signals:
            reasons.append("Price in uptrend")
        if sentiment == "Positive":
            reasons.append("Positive market sentiment")
        if opportunity == "High":
            reasons.append("High opportunity level")
        if "Volume Spike" in signals:
            reasons.append("Volume spike confirmation")
        
        # Ensure at least 2 reasons
        if len(reasons) == 0:
            if action == "BUY":
                reasons = ["Technical setup favorable", "Momentum building"]
            elif action == "SELL":
                reasons = ["Resistance reached", "Momentum weakening"]
            else:
                reasons = ["Setup pending", "Consolidation phase"]
        elif len(reasons) == 1:
            if action == "BUY":
                reasons.append("Favorable risk-reward ratio")
            elif action == "SELL":
                reasons.append("Downside risk increasing")
            else:
                reasons.append("Awaiting confirmation signal")
        
        return {
            "action": action,
            "action_emoji": "🟢" if action == "BUY" else ("🔴" if action == "SELL" else "🔵"),
            "confidence": f"{confidence}%",
            "reasons": reasons[:3],
        }


class VideoFrameBuilder:
    """Builds visual frames with text overlays."""
    
    @staticmethod
    def create_insight_overlay_frame(ticker: str, insights: Dict, data: np.ndarray = None) -> str:
        """Create frame with AI insight overlay."""
        fig, ax = plt.subplots(figsize=(12, 8), facecolor="white")
        
        # Create chart background if data provided
        if data is not None:
            ax_alt = ax.twinx()
            ax_alt.plot(data, color="#1f77b4", linewidth=2, alpha=0.3)
            ax_alt.set_alpha(0.2)
            ax.set_alpha(0.8)
        
        # Title
        ax.text(0.5, 0.95, f"{ticker} - AI Market Insights", 
                ha="center", va="top", fontsize=24, fontweight="bold",
                transform=ax.transAxes)
        
        # Trend direction box
        y_pos = 0.85
        ax.text(0.05, y_pos, "Trend Direction:", fontsize=14, fontweight="bold",
                transform=ax.transAxes)
        ax.text(0.35, y_pos, insights["trend"], fontsize=14, fontweight="bold",
                transform=ax.transAxes, color="darkred" if "BEARISH" in insights["trend"] else 
                ("darkgreen" if "BULLISH" in insights["trend"] else "darkblue"))
        
        # Signal detected
        y_pos = 0.77
        ax.text(0.05, y_pos, "Signals Detected:", fontsize=12,
                transform=ax.transAxes)
        ax.text(0.35, y_pos, insights["signal_detected"], fontsize=12,
                transform=ax.transAxes, style="italic")
        
        # Momentum strength
        y_pos = 0.69
        ax.text(0.05, y_pos, "Momentum Strength:", fontsize=12,
                transform=ax.transAxes)
        color_momentum = "darkgreen" if insights["momentum_value"] >= 70 else \
                        ("orange" if insights["momentum_value"] >= 50 else "darkred")
        ax.text(0.35, y_pos, insights["momentum_strength"], fontsize=12,
                transform=ax.transAxes, color=color_momentum, fontweight="bold")
        
        # Short outlook
        y_pos = 0.61
        ax.text(0.05, y_pos, "Short Outlook:", fontsize=12,
                transform=ax.transAxes)
        ax.text(0.35, y_pos, insights["short_outlook"], fontsize=12,
                transform=ax.transAxes, style="italic", fontweight="bold")
        
        # Additional metrics
        y_pos = 0.48
        ax.text(0.05, y_pos, "Opportunity Level:", fontsize=11,
                transform=ax.transAxes)
        ax.text(0.35, y_pos, insights["opportunity"], fontsize=11,
                transform=ax.transAxes)
        
        y_pos = 0.40
        ax.text(0.05, y_pos, "Sentiment:", fontsize=11,
                transform=ax.transAxes)
        ax.text(0.35, y_pos, insights["sentiment"], fontsize=11,
                transform=ax.transAxes)
        
        # Confidence meter
        y_pos = 0.28
        confidence_val = insights["confidence"]
        ax.text(0.05, y_pos, "Confidence Score:", fontsize=11,
                transform=ax.transAxes)
        
        # Draw confidence bar
        bar_width = 0.2
        bar_height = 0.03
        bar_x = 0.35
        bar_rect = Rectangle((bar_x, y_pos - bar_height/2), bar_width, bar_height,
                             transform=ax.transAxes, facecolor="lightgray", edgecolor="black")
        ax.add_patch(bar_rect)
        
        fill_width = bar_width * (confidence_val / 100.0)
        fill_rect = Rectangle((bar_x, y_pos - bar_height/2), fill_width, bar_height,
                              transform=ax.transAxes, 
                              facecolor="darkgreen" if confidence_val >= 70 else ("orange" if confidence_val >= 50 else "darkred"),
                              edgecolor="black")
        ax.add_patch(fill_rect)
        
        ax.text(bar_x + bar_width + 0.02, y_pos, f"{int(confidence_val)}%", 
                fontsize=11, va="center", transform=ax.transAxes)
        
        # Footer
        ax.text(0.5, 0.05, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                ha="center", fontsize=10, style="italic",
                transform=ax.transAxes, alpha=0.6)
        
        ax.axis("off")
        
        frame_path = os.path.join(VIDEOS_DIR, f"frame_insight_{uuid.uuid4().hex}.png")
        plt.tight_layout()
        plt.savefig(frame_path, dpi=100, bbox_inches="tight", facecolor="white")
        plt.close()
        
        return frame_path
    
    @staticmethod
    def create_news_frame(ticker: str, headlines: List[str]) -> str:
        """Create news/market drivers frame."""
        fig, ax = plt.subplots(figsize=(12, 8), facecolor="white")
        
        # Title
        ax.text(0.5, 0.92, "Key Market Drivers", 
                ha="center", va="top", fontsize=26, fontweight="bold",
                transform=ax.transAxes)
        
        ax.text(0.5, 0.85, f"{ticker}", 
                ha="center", va="top", fontsize=16, style="italic",
                transform=ax.transAxes, alpha=0.7)
        
        # Headlines
        y_pos = 0.75
        for i, headline in enumerate(headlines[:3]):
            # Bullet point
            ax.text(0.08, y_pos, "•", fontsize=20, transform=ax.transAxes, fontweight="bold")
            
            # Headline text (wrap if needed)
            headline_text = headline[:80] + "..." if len(headline) > 80 else headline
            ax.text(0.15, y_pos, headline_text, fontsize=13, transform=ax.transAxes,
                   wrap=True, verticalalignment="center")
            
            y_pos -= 0.18
        
        ax.text(0.5, 0.08, "Monitor these factors for trade confirmation", 
                ha="center", va="center", fontsize=11, style="italic",
                transform=ax.transAxes, alpha=0.7)
        
        ax.axis("off")
        
        frame_path = os.path.join(VIDEOS_DIR, f"frame_news_{uuid.uuid4().hex}.png")
        plt.tight_layout()
        plt.savefig(frame_path, dpi=100, bbox_inches="tight", facecolor="white")
        plt.close()
        
        return frame_path
    
    @staticmethod
    def create_recommendation_frame(ticker: str, recommendation: Dict) -> str:
        """Create final recommendation frame."""
        fig, ax = plt.subplots(figsize=(12, 8), facecolor="white")
        
        # Title
        ax.text(0.5, 0.92, "Final Recommendation", 
                ha="center", va="top", fontsize=26, fontweight="bold",
                transform=ax.transAxes)
        
        # Action box
        action = recommendation["action"]
        color_map = {"BUY": "#2ecc71", "SELL": "#e74c3c", "HOLD": "#3498db"}
        box_color = color_map.get(action, "#95a5a6")
        
        # Draw action box
        from matplotlib.patches import FancyBboxPatch
        box = FancyBboxPatch((0.25, 0.70), 0.5, 0.12, 
                            boxstyle="round,pad=0.01", 
                            transform=ax.transAxes,
                            facecolor=box_color, edgecolor="black", linewidth=2)
        ax.add_patch(box)
        
        ax.text(0.5, 0.76, f"{recommendation['action_emoji']} {action}", 
                ha="center", va="center", fontsize=32, fontweight="bold",
                transform=ax.transAxes, color="white")
        
        # Confidence
        ax.text(0.5, 0.62, f"Confidence: {recommendation['confidence']}", 
                ha="center", va="center", fontsize=16, fontweight="bold",
                transform=ax.transAxes)
        
        # Reasons
        ax.text(0.5, 0.54, "Key Reasons:", 
                ha="center", va="center", fontsize=14, fontweight="bold",
                transform=ax.transAxes)
        
        y_pos = 0.48
        for i, reason in enumerate(recommendation["reasons"], 1):
            ax.text(0.1, y_pos, f"{i}. {reason}", 
                   fontsize=12, transform=ax.transAxes, wrap=True)
            y_pos -= 0.12
        
        ax.text(0.5, 0.08, "Trade at your own risk. This is not financial advice.", 
                ha="center", va="center", fontsize=10, style="italic",
                transform=ax.transAxes, alpha=0.6)
        
        ax.axis("off")
        
        frame_path = os.path.join(VIDEOS_DIR, f"frame_recommendation_{uuid.uuid4().hex}.png")
        plt.tight_layout()
        plt.savefig(frame_path, dpi=100, bbox_inches="tight", facecolor="white")
        plt.close()
        
        return frame_path


class NarrationGenerator:
    """Generates audio narration from text."""
    
    @staticmethod
    def generate_narration(text: str, lang: str = "en") -> str:
        """
        Generate narration audio from text.
        
        Args:
            text: Text to convert to speech
            lang: Language code (default: 'en')
            
        Returns:
            Path to audio file
        """
        try:
            audio_path = os.path.join(VIDEOS_DIR, f"narration_{uuid.uuid4().hex}.mp3")
            tts = gTTS(text, lang=lang, slow=False)
            tts.save(audio_path)
            return audio_path
        except Exception as e:
            logger.error(f"Error generating narration: {str(e)}")
            # Create silent audio as fallback
            raise


class VideoComposer:
    """Composes multiple frames into a single video."""
    
    @staticmethod
    def compose_video(frames: List[StructuredVideoFrame], ticker: str) -> str:
        """
        Compose multiple frames into single video with audio.
        
        Args:
            frames: List of StructuredVideoFrame objects
            ticker: Stock ticker
            
        Returns:
            Path to final video file
        """
        try:
            video_clips = []
            total_duration_expected = 0
            
            for i, frame in enumerate(frames):
                # Create image clip
                img_clip = ImageClip(frame.image_path)
                
                # Add audio and match duration properly
                if frame.audio_path and os.path.exists(frame.audio_path):
                    audio = AudioFileClip(frame.audio_path)
                    # Set frame duration to match audio duration + 0.5 second buffer
                    frame_duration = audio.duration + 0.5
                    img_clip = img_clip.set_duration(frame_duration)
                    # Set audio to start at beginning and trim to frame duration
                    img_clip = img_clip.set_audio(audio)
                    total_duration_expected += frame_duration
                    logger.info(f"Frame {i+1}: audio={audio.duration:.2f}s, set_duration={frame_duration:.2f}s, clip.duration={img_clip.duration:.2f}s")
                else:
                    # Use frame duration for silent frames
                    img_clip = img_clip.set_duration(frame.duration)
                    total_duration_expected += frame.duration
                    logger.info(f"Frame {i+1}: silent, duration={frame.duration:.2f}s, clip.duration={img_clip.duration:.2f}s")
                
                video_clips.append(img_clip)
            
            # Concatenate all clips
            if video_clips:
                logger.info(f"Expected total duration: {total_duration_expected:.2f}s")
                final_video = concatenate_videoclips(video_clips)
                logger.info(f"Actual concatenated video duration: {final_video.duration:.2f}s")
                
                video_path = os.path.join(VIDEOS_DIR, f"video_{ticker}_{uuid.uuid4().hex}.mp4")
                final_video.write_videofile(video_path, fps=24, verbose=False, logger=None)
                
                return video_path
            else:
                raise ValueError("No video clips to compose")
        
        except Exception as e:
            logger.error(f"Error composing video: {str(e)}")
            raise


def generate_structured_video_report(ticker: str, analysis_data: Dict) -> Dict:
    """
    Generate complete structured video report with AI insights.
    
    Args:
        ticker: Stock ticker symbol
        analysis_data: Complete analysis from analyzer.py
        
    Returns:
        Dict with video_path, frames_data, narration_scripts, and summary
    """
    try:
        logger.info(f"Generating structured video report for {ticker}")
        
        # Step 1: Extract AI insights
        logger.info("Extracting AI insights...")
        insights = AIInsightGenerator.extract_insights(analysis_data)
        
        # Step 2: Extract headlines
        logger.info("Extracting news headlines...")
        headlines = AIInsightGenerator.extract_news_headlines(analysis_data)
        
        # Step 3: Generate recommendation
        logger.info("Generating recommendation...")
        recommendation = AIInsightGenerator.generate_recommendation(analysis_data)
        
        # Step 4: Create frames
        logger.info("Building video frames...")
        
        # Get historical data for chart
        try:
            hist_data = yf.download(ticker, period="60d")
            close_prices = hist_data["Close"].values if not hist_data.empty else None
        except:
            close_prices = None
        
        # Insight frame
        insight_frame_path = VideoFrameBuilder.create_insight_overlay_frame(
            ticker, insights, close_prices
        )
        insight_narration = f"Based on current market analysis, {ticker} shows {insights['trend_direction']}. {insights['signal_detected']} with {insights['momentum_strength']} momentum. The outlook suggests {insights['short_outlook']}."
        insight_audio = NarrationGenerator.generate_narration(insight_narration)
        
        # Get actual audio duration
        insight_audio_duration = AudioFileClip(insight_audio).duration if insight_audio else 5.0
        
        insight_frame = StructuredVideoFrame("analysis", f"{ticker} AI Insights", insights, duration=insight_audio_duration + 0.5)
        insight_frame.image_path = insight_frame_path
        insight_frame.audio_path = insight_audio
        insight_frame.narration = insight_narration
        
        # News frame
        news_frame_path = VideoFrameBuilder.create_news_frame(ticker, headlines)
        news_narration = f"Key market drivers for {ticker}: {headlines[0]}. {headlines[1] if len(headlines) > 1 else ''}. {headlines[2] if len(headlines) > 2 else ''}"
        news_audio = NarrationGenerator.generate_narration(news_narration)
        
        # Get actual audio duration
        news_audio_duration = AudioFileClip(news_audio).duration if news_audio else 5.0
        
        news_frame = StructuredVideoFrame("news", f"{ticker} Market Drivers", 
                                         {"headlines": headlines}, duration=news_audio_duration + 0.5)
        news_frame.image_path = news_frame_path
        news_frame.audio_path = news_audio
        news_frame.narration = news_narration
        
        # Recommendation frame
        rec_frame_path = VideoFrameBuilder.create_recommendation_frame(ticker, recommendation)
        rec_narration = f"Final recommendation: {recommendation['action']} with {recommendation['confidence']} confidence. {recommendation['reasons'][0]}. {recommendation['reasons'][1] if len(recommendation['reasons']) > 1 else ''}"
        rec_audio = NarrationGenerator.generate_narration(rec_narration)
        
        # Get actual audio duration
        rec_audio_duration = AudioFileClip(rec_audio).duration if rec_audio else 5.0
        
        rec_frame = StructuredVideoFrame("recommendation", f"{ticker} Recommendation",
                                        recommendation, duration=rec_audio_duration + 0.5)
        rec_frame.image_path = rec_frame_path
        rec_frame.audio_path = rec_audio
        rec_frame.narration = rec_narration
        
        # Step 5: Compose video
        logger.info("Composing final video...")
        frames = [insight_frame, news_frame, rec_frame]
        video_path = VideoComposer.compose_video(frames, ticker)
        
        # Step 6: Build output report
        report = {
            "success": True,
            "ticker": ticker,
            "video_path": video_path,
            "frames": [
                {
                    "type": f.frame_type,
                    "title": f.title,
                    "image": f.image_path,
                    "duration": f.duration,
                    "narration": f.narration,
                    "content": f.content
                }
                for f in frames
            ],
            "insights": insights,
            "recommendation": recommendation,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "trend": insights["trend"],
                "action": recommendation["action"],
                "confidence": recommendation["confidence"],
                "key_reasons": recommendation["reasons"]
            }
        }
        
        logger.info(f"✓ Video report generated: {video_path}")
        return report
    
    except Exception as e:
        logger.error(f"Error generating video report: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "ticker": ticker
        }


def generate_market_video(ticker: str) -> str:
    """
    Legacy function for backward compatibility.
    
    For new implementations, use generate_structured_video_report() instead.
    
    Generates a simple 6-second video with chart and narration.
    """
    img_path = None
    audio_path = None
    try:
        logger.info(f"Generating legacy video for: {ticker}")

        # Fetch data
        data = yf.download(ticker, period="5d")

        if data.empty:
            raise Exception(f"No data found for {ticker}")

        # Create chart PNG
        img_path = os.path.join(VIDEOS_DIR, f"chart_{uuid.uuid4().hex}.png")

        plt.figure(figsize=(8, 5))
        data["Close"].plot(title=f"{ticker} Price Movement (5D)", color='#1f77b4')
        plt.xlabel("Date")
        plt.ylabel("Price ($)")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(img_path, dpi=100, bbox_inches='tight')
        plt.close()

        logger.debug(f"Chart created: {img_path}")

        # Create audio narration - extract scalar values properly
        try:
            last_price_val = data["Close"].iloc[-1]
            if hasattr(last_price_val, 'item'):
                last_price = float(last_price_val.item())
            else:
                last_price = float(last_price_val)
                
            first_price_val = data["Close"].iloc[0]
            if hasattr(first_price_val, 'item'):
                first_price = float(first_price_val.item())
            else:
                first_price = float(first_price_val)
        except:
            last_price = float(data["Close"].values[-1].item())
            first_price = float(data["Close"].values[0].item())
        
        price_change = round(last_price - first_price, 2)
        change_pct = round((price_change / first_price) * 100, 2)
        last_price = round(last_price, 2)
        
        text = f"{ticker} latest price is {last_price} dollars. "
        if price_change >= 0:
            text += f"Up {price_change} dollars, or {change_pct} percent."
        else:
            text += f"Down {abs(price_change)} dollars, or {abs(change_pct)} percent."

        audio_path = os.path.join(VIDEOS_DIR, f"audio_{uuid.uuid4().hex}.mp3")
        tts = gTTS(text, lang='en', slow=False)
        tts.save(audio_path)
        
        logger.debug(f"Audio created: {audio_path}")

        # Create video by combining image + audio
        video_path = os.path.join(VIDEOS_DIR, f"video_{ticker}_{uuid.uuid4().hex}.mp4")

        # Set image duration to match audio
        clip = ImageClip(img_path)
        audio = AudioFileClip(audio_path)
        
        # Get audio duration and set image to that duration
        video_duration = audio.duration + 1  # Add 1 second buffer
        clip = clip.set_duration(video_duration)
        clip = clip.set_audio(audio)
        
        # Write video with specific codec settings
        logger.debug(f"Composing video to: {video_path}")
        clip.write_videofile(
            video_path, 
            fps=24,
            codec='libx264',
            audio_codec='aac',
            verbose=False,
            logger=None,
            preset='fast'  # Faster encoding
        )
        
        logger.info(f"✓ Legacy video created: {video_path}")
        
        return video_path

    except Exception as e:
        logger.error(f"VIDEO ERROR: {type(e).__name__}: {str(e)}")
        # Cleanup on error
        try:
            if img_path and os.path.exists(img_path):
                os.remove(img_path)
            if audio_path and os.path.exists(audio_path):
                os.remove(audio_path)
        except:
            pass
        raise