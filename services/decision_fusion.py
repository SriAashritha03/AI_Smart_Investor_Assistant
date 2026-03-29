"""
FINAL DECISION FUSION ENGINE
=============================

Consolidates all analysis sources into ONE unified decision:
- Pattern Engine (Breakout, Support, MA Crossover)
- Sentiment Analysis (Positive/Negative/Neutral)
- Event Signals (Price Spike, Volume Surge)
- Opportunity Radar (Technical Signals)

PRIORITY ORDER:
1. Strong bearish pattern (Death Cross) → SELL
2. Strong bullish (breakout + uptrend + positive sentiment) → BUY
3. Mixed signals → HOLD

Ensures:
- ONLY ONE action output (BUY/HOLD/SELL)
- Aligned confidence levels
- Corrected sentiment labels
- Consistent reasoning across all sections
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)


class DecisionFusionEngine:
    """
    Final arbitrator for unified trading decisions.
    
    Resolves conflicts between different analysis sources and ensures
    a single, consistent action recommendation with full explainability.
    """
    
    CONFIDENCE_BANDS = {
        "Weak": (0, 40),
        "Moderate": (40, 70),
        "Strong": (70, 100),
    }
    
    ACTION_EMOJIS = {
        "BUY": "🟢",
        "HOLD": "🔵",
        "SELL": "🔴",
    }
    
    def __init__(self, analysis_data: Dict) -> None:
        """
        Initialize fusion engine with complete analysis data.
        
        Args:
            analysis_data: Full API response from analyzer.py
        """
        self.data = analysis_data
        self.chart_patterns = analysis_data.get("chart_patterns", {})
        self.news_sentiment = analysis_data.get("news_sentiment", {})
        self.event_signals = analysis_data.get("event_signals", {})
        self.signals_triggered = analysis_data.get("signals_triggered", [])
        self.current_action = analysis_data.get("action", "HOLD")
        self.current_confidence = analysis_data.get("confidence", 50)
        self.current_opportunity = analysis_data.get("opportunity_level", "Weak")
    
    def fuse(self) -> Dict:
        """
        Execute full decision fusion process.
        
        Returns:
            Dict: Updated analysis_data with unified decision + explainability + score breakdown
        """
        logger.info("=== STARTING FINAL DECISION FUSION ===")
        
        # Step 1: Detect bearish signals (highest priority)
        has_death_cross = self._has_death_cross()
        bearish_patterns = self._get_bearish_patterns()
        
        # Step 2: Detect bullish signals
        has_strong_bullish = self._has_strong_bullish_pattern()
        bullish_patterns = self._get_bullish_patterns()
        
        # Step 3: Analyze sentiment
        sentiment_label, sentiment_corrected = self._correct_sentiment()
        
        # Step 4: Determine unified action
        unified_action, fusion_reasoning = self._determine_unified_action(
            has_death_cross, has_strong_bullish, sentiment_label
        )
        
        # Step 5: Adjust confidence to match opportunity level
        adjusted_confidence = self._align_confidence(
            unified_action, has_strong_bullish
        )
        
        # Step 6: Ensure opportunity level matches confidence
        aligned_opportunity = self._align_opportunity_level(adjusted_confidence)
        
        # Step 7: Generate signal summary (fixes "No trading signals" + bearish patterns issue)
        signal_summary = self._generate_signal_summary(
            bearish_patterns, bullish_patterns
        )
        
        # Step 8: Generate explanation block (2-3 reasons why this decision)
        explanation_block = self._generate_explanation_block(
            unified_action, bearish_patterns, bullish_patterns, sentiment_label, adjusted_confidence
        )
        
        # Step 9: Generate score breakdown (Technical, Sentiment, Events)
        score_breakdown = self._generate_score_breakdown()
        
        # Step 10: Apply corrections to response
        self.data["action"] = unified_action
        self.data["confidence"] = adjusted_confidence
        self.data["opportunity_level"] = aligned_opportunity
        self.data["news_sentiment"]["sentiment_label"] = sentiment_label
        self.data["_fusion_reasoning"] = fusion_reasoning
        self.data["signal_summary"] = signal_summary
        self.data["explanation_block"] = explanation_block
        self.data["score_breakdown"] = score_breakdown
        self.data["bearish_patterns"] = bearish_patterns
        self.data["bullish_patterns"] = bullish_patterns
        
        logger.info(f"✓ Unified Decision: {unified_action} | Confidence: {adjusted_confidence}% | Opportunity: {aligned_opportunity}")
        logger.info(f"✓ Signal Summary: {signal_summary}")
        logger.info(f"✓ Explanation: {explanation_block[0] if explanation_block else 'None'}")
        logger.info("=== DECISION FUSION COMPLETE ===")
        
        return self.data
    
    def _has_death_cross(self) -> bool:
        """Detect Death Cross (bearish MA crossover)."""
        patterns = self.chart_patterns.get("patterns_detected", [])
        for pattern in patterns:
            if (pattern.get("pattern_name") == "MA Crossover" and 
                pattern.get("detected") == True and
                pattern.get("crossover_type") == "Death Cross"):
                logger.info("🔴 CRITICAL: Death Cross detected!")
                return True
        return False
    
    def _has_strong_bullish_pattern(self) -> bool:
        """
        Detect strong bullish patterns:
        - Breakout + Support both detected
        - Breakout + positive sentiment
        - Uptrend triggered + positive sentiment
        """
        patterns = self.chart_patterns.get("patterns_detected", [])
        has_breakout = any(p.get("pattern_name") == "Breakout" and p.get("detected") == True for p in patterns)
        has_support = any(p.get("pattern_name") == "Support" and p.get("detected") == True for p in patterns)
        has_golden_cross = any(
            p.get("pattern_name") == "MA Crossover" and 
            p.get("detected") == True and
            p.get("crossover_type") == "Golden Cross" 
            for p in patterns
        )
        
        # Sentiment check
        sentiment = self.news_sentiment.get("sentiment_label", "Neutral")
        positive_sentiment = sentiment == "Positive"
        
        # Event signals check
        events = self.event_signals.get("events_detected", [])
        has_volume_surge = "Volume Surge" in events
        has_price_spike = "Price Spike" in events
        
        # Strong bullish = multiple confirmations
        bullish_score = sum([
            has_breakout and has_support,  # +2 (dual confirmation)
            has_golden_cross,               # +1
            positive_sentiment,             # +1
            has_volume_surge,               # +1
            has_price_spike,                # +1
        ])
        
        is_strong = bullish_score >= 2
        if is_strong:
            logger.info(f"🟢 Strong Bullish Pattern Detected (score: {bullish_score})")
        
        return is_strong
    
    def _correct_sentiment(self) -> tuple[str, bool]:
        """
        Correct sentiment labels based on the sentiment_score (authoritative).
        
        IMPORTANT: The sentiment_score IS the true label. Don't override it.
        - score > 0.3 = Positive
        - score < -0.3 = Negative  
        - else = Neutral
        
        Low confidence just means fewer articles - doesn't change the sentiment direction.
        
        Returns:
            tuple: (label_from_score, was_corrected)
        """
        original_label = self.news_sentiment.get("sentiment_label", "Neutral")
        score = self.news_sentiment.get("sentiment_score", 0)
        confidence = self.news_sentiment.get("confidence", 0)
        
        # Determine label ONLY from the score
        if score > 0.3:
            corrected_label = "Positive"
        elif score < -0.3:
            corrected_label = "Negative"
        else:
            corrected_label = "Neutral"
        
        # Log if we had to correct due to wrong backend label
        was_corrected = corrected_label != original_label
        if was_corrected:
            logger.info(f"⚠️  Correcting sentiment '{original_label}' → '{corrected_label}' (score: {score}, matched to score, confidence: {confidence}%)")
        
        return corrected_label, was_corrected
    
    def _determine_unified_action(
        self, has_death_cross: bool, has_strong_bullish: bool, sentiment_label: str
    ) -> tuple[str, str]:
        """
        Apply priority-based decision logic:
        1. Death Cross → SELL
        2. Strong Bullish + Positive Sentiment → BUY
        3. Strong Bullish + Neutral Sentiment → BUY (with caution)
        4. Mixed signals → HOLD
        5. Negative sentiment without bullish → HOLD/SELL
        
        Returns:
            tuple: (action, reasoning)
        """
        
        # PRIORITY 1: Death Cross = SELL
        if has_death_cross:
            return "SELL", "Death Cross detected - strong bearish signal"
        
        # PRIORITY 2: Strong bullish patterns
        if has_strong_bullish:
            if sentiment_label == "Positive":
                return "BUY", "Strong bullish patterns with positive sentiment alignment"
            elif sentiment_label == "Neutral":
                return "BUY", "Strong bullish technical patterns (neutral sentiment)"
            else:  # Negative sentiment
                return "HOLD", "Bullish patterns conflict with negative sentiment - caution advised"
        
        # PRIORITY 3: Mixed signals
        if sentiment_label == "Positive":
            return "BUY", "Positive sentiment with moderate technical support"
        elif sentiment_label == "Negative":
            return "HOLD", "Negative sentiment with insufficient bullish confirmation"
        else:
            return "HOLD", "Neutral setup - insufficient signals for strong conviction"
    
    def _align_confidence(self, action: str, has_strong_bullish: bool) -> float:
        """
        Align confidence with action and bullish signals.
        
        Mapping:
        - BUY with strong bullish: 70-80%
        - BUY without strong bullish: 55-65%
        - HOLD: 40-55%
        - SELL: 60-75%
        """
        if action == "SELL":
            # SELL confidence based on bearish strength
            return 65.0
        elif action == "BUY":
            if has_strong_bullish:
                # Strong bullish gets higher confidence
                return min(self.current_confidence + 5, 80.0)
            else:
                # Moderate bullish caps at 65%
                return min(self.current_confidence, 65.0)
        else:  # HOLD
            # HOLD is always conservative
            return min(self.current_confidence, 55.0)
    
    def _align_opportunity_level(self, confidence: float) -> str:
        """
        Ensure opportunity_level matches confidence:
        
        0-40% → Weak
        40-70% → Moderate
        70%+ → Strong
        """
        for level, (min_conf, max_conf) in self.CONFIDENCE_BANDS.items():
            if min_conf <= confidence < max_conf:
                return level
        
        # Fallback for edge case (confidence = 70+)
        return "Strong" if confidence >= 70 else "Weak"
    
    def validate_consistency(self) -> Dict[str, bool]:
        """
        Audit consistency across sections.
        
        Returns:
            Dict: Status of each validation check
        """
        checks = {
            "action_matches_sentiment": self._validate_action_sentiment(),
            "confidence_matches_opportunity": self._validate_confidence_opportunity(),
            "patterns_align_with_action": self._validate_patterns_action(),
            "sentiment_is_valid": self._validate_sentiment_format(),
        }
        
        all_valid = all(checks.values())
        logger.info(f"Consistency Validation: {checks} | Overall: {'✓ PASS' if all_valid else '✗ FAIL'}")
        
        return checks
    
    def _validate_action_sentiment(self) -> bool:
        """Check if action aligns with sentiment."""
        action = self.data["action"]
        sentiment = self.data["news_sentiment"]["sentiment_label"]
        
        if action == "BUY" and sentiment == "Negative":
            logger.warning("⚠️  Consistency Warning: BUY action with Negative sentiment")
            return False
        return True
    
    def _validate_confidence_opportunity(self) -> bool:
        """Check if confidence band matches opportunity level."""
        confidence = self.data["confidence"]
        opportunity = self.data["opportunity_level"]
        
        min_conf, max_conf = self.CONFIDENCE_BANDS.get(opportunity, (0, 100))
        
        if not (min_conf <= confidence <= max_conf):
            logger.warning(
                f"⚠️  Consistency Warning: Confidence {confidence}% outside "
                f"{opportunity} band ({min_conf}-{max_conf})"
            )
            return False
        return True
    
    def _validate_patterns_action(self) -> bool:
        """Check if patterns support the action."""
        action = self.data["action"]
        patterns = self.data["chart_patterns"]["patterns_detected"]
        
        has_breakout = any(p.get("pattern_name") == "Breakout" and p.get("detected") for p in patterns)
        
        if action == "BUY" and not any(p.get("detected") for p in patterns):
            logger.warning("⚠️  Consistency Warning: BUY action without detected patterns")
            return False
        return True
    
    def _validate_sentiment_format(self) -> bool:
        """Check if sentiment is one of valid values."""
        sentiment = self.data["news_sentiment"]["sentiment_label"]
        valid = sentiment in ["Positive", "Negative", "Neutral"]
        
        if not valid:
            logger.warning(f"⚠️  Invalid sentiment label: {sentiment}")
        return valid
    
    # ===== NEW METHODS FOR EXPLAINABILITY & SCORE BREAKDOWN =====
    
    def _get_bearish_patterns(self) -> list:
        """
        Extract bearish patterns from chart patterns.
        
        Returns:
            List[str]: List of bearish patterns detected
        """
        bearish = []
        patterns = self.chart_patterns.get("patterns_detected", [])
        
        for pattern in patterns:
            if pattern.get("detected") == True:
                if pattern.get("pattern_name") == "MA Crossover" and pattern.get("crossover_type") == "Death Cross":
                    bearish.append("Death Cross")
                elif pattern.get("pattern_name") == "Support" and pattern.get("is_resistance") == True:
                    bearish.append("Resistance Hold")
        
        return bearish
    
    def _get_bullish_patterns(self) -> list:
        """
        Extract bullish patterns from chart patterns.
        
        Returns:
            List[str]: List of bullish patterns detected
        """
        bullish = []
        patterns = self.chart_patterns.get("patterns_detected", [])
        
        for pattern in patterns:
            if pattern.get("detected") == True:
                if pattern.get("pattern_name") == "Breakout":
                    bullish.append("Breakout")
                elif pattern.get("pattern_name") == "Support":
                    bullish.append("Support Hold")
                elif pattern.get("pattern_name") == "MA Crossover" and pattern.get("crossover_type") == "Golden Cross":
                    bullish.append("Golden Cross")
        
        return bullish
    
    def _generate_signal_summary(self, bearish_patterns: list, bullish_patterns: list) -> str:
        """
        Generate context-aware signal summary that replaces generic "No trading signals" text.
        
        FIXES THE ISSUE: Now shows bearish patterns even when no bullish signals
        
        Returns:
            str: Human-readable signal summary
        """
        signals = self.signals_triggered
        sentiment = self.data["news_sentiment"]["sentiment_label"]
        
        # Case 1: Bearish patterns present (even without triggered signals)
        if bearish_patterns and not signals:
            if "Death Cross" in bearish_patterns:
                return "No bullish signals detected. ⚠️ Death Cross present - strong bearish signal."
            return f"No bullish signals detected. Bearish pattern(s) present: {', '.join(bearish_patterns)}"
        
        # Case 2: Mixed signals - some bullish, some bearish
        if signals and bearish_patterns:
            signal_text = ", ".join(signals)
            return f"Mixed signals: {signal_text}. Counter-signal: {', '.join(bearish_patterns)}"
        
        # Case 3: Strong bullish signals
        if len(signals) >= 2:
            return f"Strong signals detected: {', '.join(signals)}"
        
        # Case 4: Single bullish signal
        if len(signals) == 1:
            return f"Single signal detected: {signals[0]}. Awaiting confirmation."
        
        # Case 5: No signals at all
        return "No trading signals triggered. Monitor for breakout setup."
    
    def _generate_explanation_block(
        self, action: str, bearish_patterns: list, bullish_patterns: list, 
        sentiment: str, confidence: float
    ) -> list:
        """
        Generate "💡 Why this decision" block with 2-3 specific reasons.
        
        Returns:
            List[str]: 2-3 bullet points explaining the decision
        """
        reasons = []
        
        # Reason 1: Pattern-based reasoning
        if action == "SELL" and bearish_patterns:
            reasons.append(f"Pattern analysis: {', '.join(bearish_patterns)} indicates downtrend")
        elif action == "BUY" and bullish_patterns:
            reasons.append(f"Pattern analysis: {', '.join(bullish_patterns)} confirms upside potential")
        elif action == "HOLD":
            if bearish_patterns and bullish_patterns:
                reasons.append(f"Mixed signals: {len(bullish_patterns)} bullish vs {len(bearish_patterns)} bearish patterns")
            else:
                reasons.append("Insufficient technical confirmation for strong conviction")
        
        # Reason 2: Sentiment-based reasoning
        if sentiment == "Positive" and action == "BUY":
            reasons.append("Positive news sentiment aligns with technical strength")
        elif sentiment == "Negative":
            reasons.append("Negative news sentiment suggests caution")
        elif sentiment == "Neutral":
            reasons.append("Neutral sentiment - signals not amplified or dampened by news")
        
        # Reason 3: Confidence context
        confidence_label = "High" if confidence >= 70 else ("Moderate" if confidence >= 40 else "Low")
        triggered_count = len(self.signals_triggered)
        
        if triggered_count >= 3:
            reasons.append(f"{confidence_label} confidence ({float(confidence):.0f}%) from multiple signal confluence")
        elif triggered_count >= 1:
            reasons.append(f"{confidence_label} confidence ({float(confidence):.0f}%) with limited confirmation signals")
        else:
            reasons.append(f"{confidence_label} confidence ({float(confidence):.0f}%) due to weak signal setup")
        
        # Return at most 3 reasons
        return reasons[:3]
    
    def _generate_score_breakdown(self) -> Dict:
        """
        Generate score breakdown for Technical, Sentiment, and Events.
        
        Returns:
            Dict with Technical, Sentiment, Events scores (0-100)
        """
        # Technical Score: Based on signals triggered and patterns
        signal_count = len(self.signals_triggered)
        pattern_count = len(self.chart_patterns.get("patterns_detected", []))
        detected_patterns = sum(1 for p in self.chart_patterns.get("patterns_detected", []) if p.get("detected"))
        technical_score = min(100, (signal_count * 15) + (detected_patterns * 20) + (self.current_confidence * 0.5))
        
        # Sentiment Score: Normalized from -1.0 to +1.0 to 0-100 scale
        sentiment_score_raw = self.news_sentiment.get("sentiment_score", 0)
        sentiment_confidence = self.news_sentiment.get("confidence", 50)
        # Normalize: -1.0 → 0, 0 → 50, +1.0 → 100
        sentiment_score = ((sentiment_score_raw + 1) / 2 * 100) * (sentiment_confidence / 100)
        sentiment_score = max(0, min(100, sentiment_score))
        
        # Events Score: Based on event signals detected
        events = self.event_signals.get("events_detected", [])
        events_score = min(100, len(events) * 40 + 10)  # Base 10 even with no events
        
        # Price spike and volume surge boost
        if self.event_signals.get("price_spike", {}).get("detected"):
            events_score = min(100, events_score + 15)
        if self.event_signals.get("volume_surge", {}).get("detected"):
            events_score = min(100, events_score + 15)
        
        return {
            "technical": float(max(0, min(100, technical_score))),
            "sentiment": float(max(0, min(100, sentiment_score))),
            "events": float(max(0, min(100, events_score)))
        }


def apply_decision_fusion(analysis_data: Dict) -> Dict:
    """
    Main entry point for decision fusion.
    
    Args:
        analysis_data: Complete analysis response from analyzer.py
        
    Returns:
        Dict: Updated analysis_data with unified decision
    """
    engine = DecisionFusionEngine(analysis_data)
    fused_data = engine.fuse()
    
    # Run validation audit
    engine.validate_consistency()
    
    return fused_data
