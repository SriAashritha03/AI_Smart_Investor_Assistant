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
    a single, consistent action recommendation.
    """
    
    CONFIDENCE_BANDS = {
        "Weak": (0, 40),
        "Moderate": (40, 70),
        "Strong": (70, 100),
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
            Dict: Updated analysis_data with unified decision
        """
        logger.info("=== STARTING FINAL DECISION FUSION ===")
        
        # Step 1: Detect bearish signals (highest priority)
        has_death_cross = self._has_death_cross()
        
        # Step 2: Detect bullish signals
        has_strong_bullish = self._has_strong_bullish_pattern()
        
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
        
        # Step 7: Apply corrections to response
        self.data["action"] = unified_action
        self.data["confidence"] = adjusted_confidence
        self.data["opportunity_level"] = aligned_opportunity
        self.data["news_sentiment"]["sentiment_label"] = sentiment_label
        self.data["_fusion_reasoning"] = fusion_reasoning
        
        logger.info(f"✓ Unified Decision: {unified_action} | Confidence: {adjusted_confidence}% | Opportunity: {aligned_opportunity}")
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
        Correct sentiment labels based on rules:
        - Neutral: If mixed sentiment or low confidence
        - Keep: If clearly positive or negative
        
        Returns:
            tuple: (corrected_label, was_corrected)
        """
        original_label = self.news_sentiment.get("sentiment_label", "Neutral")
        confidence = self.news_sentiment.get("confidence", 0)
        score = self.news_sentiment.get("sentiment_score", 0)
        
        # If mixed signals or low confidence, label as Neutral
        if confidence < 60 or abs(score) < 0.3:
            if original_label != "Neutral":
                logger.info(f"⚠️  Correcting sentiment '{original_label}' → 'Neutral' (confidence: {confidence}%)")
                return "Neutral", True
        
        return original_label, False
    
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
