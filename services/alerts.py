"""
Smart Alerts System

Generates intelligent alerts based on stock patterns, signals, and technical indicators.
Provides real-time alerts for traders to monitor stocks.

Alert Types:
- BREAKOUT: Price breakout detected
- SUPPORT_BREAK: Support level broken
- TREND_REVERSAL: Trend change detected
- HIGH_RISK: Risky patterns forming
- VOLUME_SPIKE: Unusual volume detected
- RSI_EXTREME: Overbought/Oversold conditions
- MOVING_AVERAGE: MA crossovers
- OPPORTUNITY: Strong buying/selling opportunity
"""

from typing import List, Dict, Optional
from datetime import datetime
import pandas as pd
import numpy as np


class Alert:
    """Represents a single alert"""
    
    def __init__(
        self,
        title: str,
        message: str,
        severity: str,  # INFO, WARNING, CRITICAL, SUCCESS
        alert_type: str,
        timestamp: str = None,
        action: str = None,
    ):
        self.title = title
        self.message = message
        self.severity = severity
        self.alert_type = alert_type
        self.timestamp = timestamp or datetime.now().isoformat()
        self.action = action  # BUY, SELL, HOLD, WATCH
    
    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "message": self.message,
            "severity": self.severity,
            "alert_type": self.alert_type,
            "timestamp": self.timestamp,
            "action": self.action,
        }


class SmartAlertSystem:
    """Generates intelligent alerts from stock analysis data"""
    
    def __init__(self):
        self.alerts: List[Alert] = []
    
    def generate_alerts(
        self,
        stock_ticker: str,
        signals_triggered: List[str],
        signal_details: List[Dict],
        chart_patterns: Optional[Dict] = None,
        opportunity_level: str = "Weak",
        confidence: int = 50,
        action: str = "PASS",
    ) -> Dict:
        """
        Generate alerts based on stock analysis data
        
        Args:
            stock_ticker: Stock symbol
            signals_triggered: List of triggered signals
            signal_details: Detailed signal information
            chart_patterns: Chart pattern analysis data
            opportunity_level: Opportunity level (Strong/Moderate/Weak)
            confidence: Confidence score (0-100)
            action: Recommended action
        
        Returns:
            Dictionary containing alerts list
        """
        self.alerts = []
        
        # Generate baseline alerts
        self._generate_signal_alerts(signals_triggered, signal_details)
        self._generate_pattern_alerts(chart_patterns)
        self._generate_opportunity_alerts(
            opportunity_level, confidence, action, stock_ticker
        )
        self._generate_risk_alerts(signal_details, chart_patterns)
        
        return {
            "stock": stock_ticker,
            "alerts": [alert.to_dict() for alert in self.alerts],
            "alert_count": len(self.alerts),
            "critical_count": sum(1 for a in self.alerts if a.severity == "CRITICAL"),
            "timestamp": datetime.now().isoformat(),
        }
    
    def _generate_signal_alerts(self, signals_triggered: List[str], signal_details: List[Dict]) -> None:
        """Generate alerts from triggered signals"""
        
        if not signals_triggered:
            alert = Alert(
                title="No Signals",
                message="Currently no trading signals are active",
                severity="INFO",
                alert_type="SIGNAL_STATUS",
                action="WATCH",
            )
            self.alerts.append(alert)
            return
        
        # Map signal names to alert messages
        signal_alerts = {
            "Uptrend": {
                "title": "📈 Uptrend Detected",
                "message": "Stock is showing upward momentum. Bullish signal.",
                "severity": "SUCCESS",
                "action": "BUY",
            },
            "Downtrend": {
                "title": "📉 Downtrend Detected",
                "message": "Stock is showing downward momentum. Bearish signal.",
                "severity": "WARNING",
                "action": "SELL",
            },
            "Breakout": {
                "title": "🚀 Breakout Detected",
                "message": "Price has broken above resistance. Strong bullish signal.",
                "severity": "CRITICAL",
                "action": "BUY",
            },
            "Volume Spike": {
                "title": "📊 Volume Spike",
                "message": "Unusual trading volume detected. Increased market interest.",
                "severity": "WARNING",
                "action": "WATCH",
            },
            "Price Surge": {
                "title": "⚡ Price Surge",
                "message": "Stock price rising rapidly. Consider entry point.",
                "severity": "WARNING",
                "action": "BUY",
            },
            "Pullback": {
                "title": "🔄 Pullback Forming",
                "message": "Price pulling back after rise. Normal market behavior.",
                "severity": "INFO",
                "action": "HOLD",
            },
            "Support Level": {
                "title": "🛡️ Support Level",
                "message": "Price near support. Potential bounce area.",
                "severity": "INFO",
                "action": "HOLD",
            },
            "Resistance Level": {
                "title": "🚧 Resistance Level",
                "message": "Price near resistance. Watch for breakout.",
                "severity": "INFO",
                "action": "WATCH",
            },
        }
        
        # Create alerts for triggered signals
        for signal in signals_triggered:
            if signal in signal_alerts:
                data = signal_alerts[signal]
                alert = Alert(
                    title=data["title"],
                    message=data["message"],
                    severity=data["severity"],
                    alert_type="SIGNAL",
                    action=data["action"],
                )
                self.alerts.append(alert)
            else:
                # Generic alert for unknown signals
                alert = Alert(
                    title=f"⚠️ {signal} Detected",
                    message=f"Trading signal '{signal}' is currently active.",
                    severity="INFO",
                    alert_type="SIGNAL",
                )
                self.alerts.append(alert)
    
    def _generate_pattern_alerts(self, chart_patterns: Optional[Dict]) -> None:
        """Generate alerts from detected chart patterns"""
        
        if not chart_patterns:
            return
        
        patterns_detected = chart_patterns.get("patterns_detected", [])
        
        for pattern in patterns_detected:
            pattern_name = pattern.get("pattern_name", "Unknown")
            detected = pattern.get("detected", False)
            strength = pattern.get("strength", "")
            
            if not detected:
                continue
            
            # Map patterns to alerts
            if pattern_name == "Breakout":
                severity = "CRITICAL" if strength == "Strong" else "WARNING"
                alert = Alert(
                    title="🚀 Breakout Pattern",
                    message=f"Strong breakout pattern detected ({strength}). Price breaking above resistance with volume confirmation.",
                    severity=severity,
                    alert_type="PATTERN",
                    action="BUY",
                )
            elif pattern_name == "Support":
                alert = Alert(
                    title="🛡️ Support Pattern",
                    message=f"Support bounce detected ({strength}). Price rebounding from support level.",
                    severity="INFO",
                    alert_type="PATTERN",
                    action="HOLD",
                )
            elif pattern_name == "MA Crossover":
                if "Golden" in str(pattern.get("crossover_type", "")):
                    alert = Alert(
                        title="✨ Golden Cross",
                        message="Moving Average Golden Cross detected. Long-term bullish signal.",
                        severity="SUCCESS",
                        alert_type="PATTERN",
                        action="BUY",
                    )
                else:
                    alert = Alert(
                        title="💀 Death Cross",
                        message="Moving Average Death Cross detected. Long-term bearish signal.",
                        severity="CRITICAL",
                        alert_type="PATTERN",
                        action="SELL",
                    )
            else:
                alert = Alert(
                    title=f"📊 {pattern_name}",
                    message=f"Chart pattern '{pattern_name}' detected with {strength} strength.",
                    severity="INFO",
                    alert_type="PATTERN",
                )
            
            self.alerts.append(alert)
    
    def _generate_opportunity_alerts(
        self,
        opportunity_level: str,
        confidence: int,
        action: str,
        stock_ticker: str,
    ) -> None:
        """Generate alerts based on opportunity assessment"""
        
        # Strong Opportunity
        if opportunity_level == "Strong" and confidence >= 70:
            severity = "CRITICAL" if action == "BUY" else "WARNING"
            message = f"🎯 Strong {action} opportunity for {stock_ticker}"
            
            if action == "BUY":
                alert_msg = f"Strong bullish setup with {confidence}% confidence. High probability trade."
            elif action == "SELL":
                alert_msg = f"Strong bearish setup with {confidence}% confidence. Downside risk identified."
            else:
                alert_msg = f"Strong trading opportunity with {confidence}% confidence."
            
            alert = Alert(
                title=message,
                message=alert_msg,
                severity=severity,
                alert_type="OPPORTUNITY",
                action=action,
            )
            self.alerts.append(alert)
        
        # Moderate Opportunity
        elif opportunity_level == "Moderate" and confidence >= 60:
            alert = Alert(
                title=f"⚡ Moderate {action} Signal",
                message=f"Moderate trading opportunity with {confidence}% confidence. Worth monitoring.",
                severity="INFO",
                alert_type="OPPORTUNITY",
                action=action,
            )
            self.alerts.append(alert)
        
        # High Confidence
        if confidence >= 85:
            alert = Alert(
                title="🎯 High Confidence Alert",
                message=f"Analysis confidence is very high ({confidence}%). Strong conviction signal.",
                severity="SUCCESS" if action == "BUY" else "WARNING",
                alert_type="CONFIDENCE",
                action=action,
            )
            self.alerts.append(alert)
    
    def _generate_risk_alerts(
        self,
        signal_details: List[Dict],
        chart_patterns: Optional[Dict] = None,
    ) -> None:
        """Generate risk-related alerts"""
        
        # Check for bearish signals forming
        bearish_signals = [
            sig for sig in signal_details
            if sig.get("triggered") and "down" in sig.get("name", "").lower()
        ]
        
        if bearish_signals:
            alert = Alert(
                title="⚠️ Bearish Signals Forming",
                message="Multiple bearish indicators detected. Downside risk increasing.",
                severity="WARNING",
                alert_type="RISK",
                action="SELL",
            )
            self.alerts.append(alert)
        
        # Check for extreme volatility
        if chart_patterns:
            patterns = chart_patterns.get("patterns_detected", [])
            extreme_patterns = [
                p for p in patterns
                if p.get("detected") and p.get("strength") == "Strong"
            ]
            
            if len(extreme_patterns) >= 2:
                alert = Alert(
                    title="🌪️ High Volatility Alert",
                    message="Multiple strong patterns detected. Market volatility is high. Use tight stops.",
                    severity="CRITICAL",
                    alert_type="RISK",
                    action="WATCH",
                )
                self.alerts.append(alert)
        
        # No triggered signals = Low momentum
        if not signal_details or not any(s.get("triggered") for s in signal_details):
            alert = Alert(
                title="😴 Low Momentum",
                message="Few trading signals active. Stock lacking clear direction.",
                severity="INFO",
                alert_type="RISK",
                action="HOLD",
            )
            self.alerts.append(alert)


def generate_stock_alerts(
    stock_ticker: str,
    signals_triggered: List[str],
    signal_details: List[Dict],
    chart_patterns: Optional[Dict] = None,
    opportunity_level: str = "Weak",
    confidence: int = 50,
    action: str = "PASS",
) -> Dict:
    """
    Convenience function to generate alerts
    
    Usage:
        alerts_data = generate_stock_alerts(
            stock_ticker="RELIANCE.NS",
            signals_triggered=["Uptrend", "Breakout"],
            signal_details=[...],
            chart_patterns={...},
            opportunity_level="Strong",
            confidence=75,
            action="BUY"
        )
    """
    system = SmartAlertSystem()
    return system.generate_alerts(
        stock_ticker=stock_ticker,
        signals_triggered=signals_triggered,
        signal_details=signal_details,
        chart_patterns=chart_patterns,
        opportunity_level=opportunity_level,
        confidence=confidence,
        action=action,
    )
