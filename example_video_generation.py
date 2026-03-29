#!/usr/bin/env python3
"""
Video Engine Example Script

This script demonstrates how to use the new AI Market Video Engine.
Generate professional stock analysis videos with AI insights.

Usage:
    python example_video_generation.py
    python example_video_generation.py AAPL
    python example_video_generation.py AAPL MSFT GOOGL
"""

import sys
import json
from datetime import datetime
from services.analyzer import analyze_stock, batch_analyze_stocks
from services.video_engine import generate_structured_video_report


def print_header(title):
    """Print formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def print_insight(label, value):
    """Print insight with formatting."""
    print(f"  {label}: {value}")


def example_single_stock(ticker):
    """Generate video for single stock."""
    print_header(f"Generating Video Report for {ticker}")
    
    try:
        # Step 1: Analyze stock
        print(f"📊 Step 1: Analyzing {ticker}...")
        analysis = analyze_stock(ticker)
        
        if not analysis.get("success"):
            print(f"❌ Analysis failed: {analysis.get('error')}")
            return
        
        print(f"✅ Analysis complete")
        print_insight("Opportunity Level", analysis['opportunity_level'])
        print_insight("Confidence", f"{analysis['confidence']}%")
        print_insight("Action", analysis['action'])
        print_insight("Signals", ", ".join(analysis.get('signals_triggered', [])))
        
        # Step 2: Generate video
        print(f"\n🎬 Step 2: Generating video...")
        report = generate_structured_video_report(ticker, analysis)
        
        if not report.get("success"):
            print(f"❌ Video generation failed: {report.get('error')}")
            return
        
        print(f"✅ Video generated!")
        
        # Display results
        print_header(f"📺 Video Report for {ticker}")
        
        print_insight("Video File", report['video_path'])
        print_insight("Generated At", report['generated_at'])
        print()
        
        # Insights
        print("🔍 AI INSIGHTS:")
        insights = report['insights']
        print_insight("  Trend", insights['trend'])
        print_insight("  Direction", insights['trend_direction'])
        print_insight("  Signals", insights['signal_detected'])
        print_insight("  Momentum", insights['momentum_strength'])
        print_insight("  Outlook", insights['short_outlook'])
        print_insight("  Sentiment", insights['sentiment'])
        print()
        
        # Recommendation
        print("🎯 RECOMMENDATION:")
        rec = report['recommendation']
        print_insight("  Action", f"{rec['action_emoji']} {rec['action']}")
        print_insight("  Confidence", rec['confidence'])
        print("  Key Reasons:")
        for i, reason in enumerate(rec['reasons'], 1):
            print(f"    {i}. {reason}")
        print()
        
        # Frames
        print("📹 VIDEO FRAMES:")
        for i, frame in enumerate(report['frames'], 1):
            print(f"\n  Frame {i}: {frame['title']} ({frame['type']})")
            print(f"  ├─ Duration: {frame['duration']} seconds")
            print(f"  ├─ Image: {frame['image']}")
            print(f"  └─ Narration: {frame['narration'][:70]}...")
        
        # Save report to JSON
        report_file = f"video_report_{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            # Make report JSON-serializable by converting datetime
            report_dict = report.copy()
            report_dict['generated_at'] = str(report_dict['generated_at'])
            json.dump(report_dict, f, indent=2)
        
        print(f"\n✅ Report saved to: {report_file}")
        print(f"\n🎉 Video ready at: {report['video_path']}")
        
        return report
        
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {str(e)}")
        return None


def example_batch_stocks(tickers):
    """Generate videos for multiple stocks."""
    print_header(f"Batch Video Generation for {len(tickers)} Stocks")
    
    try:
        # Analyze all stocks
        print(f"📊 Analyzing {len(tickers)} stocks...")
        analyses = batch_analyze_stocks(tickers)
        print(f"✅ Analysis complete")
        
        # Generate videos
        reports = {}
        summary = []
        
        print(f"\n🎬 Generating videos...")
        for ticker, analysis in analyses.items():
            if analysis.get("success"):
                print(f"  • {ticker}: ", end="", flush=True)
                report = generate_structured_video_report(ticker, analysis)
                
                if report.get("success"):
                    reports[ticker] = report
                    summary.append({
                        "ticker": ticker,
                        "action": report['recommendation']['action'],
                        "confidence": report['recommendation']['confidence'],
                        "video": report['video_path']
                    })
                    print("✅")
                else:
                    print(f"❌ ({report.get('error')})")
            else:
                print(f"  • {ticker}: ❌ (Analysis failed)")
        
        # Display summary
        print_header("📊 BATCH REPORT SUMMARY")
        
        print(f"{'Ticker':<12} {'Action':<10} {'Confidence':<15} {'Status':<10}")
        print("-" * 50)
        
        for item in summary:
            emoji = "✅"
            print(f"{item['ticker']:<12} {item['action']:<10} {item['confidence']:<15} {emoji}")
        
        # Statistics
        if summary:
            buys = sum(1 for s in summary if s['action'] == 'BUY')
            sells = sum(1 for s in summary if s['action'] == 'SELL')
            holds = sum(1 for s in summary if s['action'] == 'HOLD')
            
            print("\n📈 Summary:")
            print(f"  • Total processed: {len(summary)}")
            print(f"  • BUY signals: {buys}")
            print(f"  • SELL signals: {sells}")
            print(f"  • HOLD signals: {holds}")
        
        # Save batch report
        batch_report_file = f"batch_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(batch_report_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✅ Batch report saved to: {batch_report_file}")
        print(f"✅ Generated {len(reports)} videos")
        
        return reports
        
    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {str(e)}")
        return {}


def example_interactive():
    """Interactive mode - prompt for ticker."""
    print_header("🎯 AI Market Video Engine - Interactive Mode")
    
    while True:
        ticker = input("Enter stock ticker (or 'quit' to exit): ").strip().upper()
        
        if ticker == 'QUIT':
            print("\n👋 Goodbye!")
            break
        
        if not ticker:
            print("❌ Please enter a valid ticker")
            continue
        
        example_single_stock(ticker)
        
        another = input("\nGenerate another video? (y/n): ").strip().lower()
        if another != 'y':
            print("\n👋 Goodbye!")
            break


def example_extraction():
    """Extract narration and insights for custom use."""
    print_header("Extracting Narration & Insights")
    
    ticker = "AAPL"
    print(f"Analyzing {ticker}...")
    
    analysis = analyze_stock(ticker)
    report = generate_structured_video_report(ticker, analysis)
    
    if report.get("success"):
        # Extract narration
        print("\n📝 NARRATION SCRIPT:")
        print("-" * 70)
        for i, frame in enumerate(report['frames'], 1):
            print(f"\n[FRAME {i}: {frame['title']}]")
            print(frame['narration'])
        
        # Extract insights as CSV-like format
        print("\n\n📊 STRUCTURED INSIGHTS (for database/export):")
        print("-" * 70)
        insights = report['insights']
        for key, value in insights.items():
            print(f"{key}: {value}")
        
        # Extract recommendations
        print("\n\n🎯 RECOMMENDATIONS (for reporting):")
        print("-" * 70)
        rec = report['recommendation']
        for key, value in rec.items():
            print(f"{key}: {value}")


def main():
    """Main entry point."""
    print("\n")
    print(r"""
     ___    _   _   __         _     _               
    / _ \  | | | | / /   ___  | |   | |  ___    ___  
   / /_\ \ | | | |/ /   / _ \ | |   | | / _ \  / _ \ 
  /  ___ \ | | |   <   | | | | | |__| || | | || | | |
 /_/   \_\|_| |_|\_\   |_| |_|  \____/ |_| |_||_| |_|
                                                      
    AI MARKET VIDEO ENGINE
    Transform Stock Analysis Into Professional Videos
    """)
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == 'batch':
            # Batch mode: all remaining args are tickers
            tickers = sys.argv[2:] if len(sys.argv) > 2 else ["AAPL", "MSFT", "GOOGL"]
            example_batch_stocks(tickers)
        elif sys.argv[1].lower() == 'extract':
            # Extract mode
            example_extraction()
        else:
            # Single stock mode
            ticker = sys.argv[1].upper()
            example_single_stock(ticker)
    else:
        # Interactive mode as default
        print("\nOptions:")
        print("  1. Generate video for single stock")
        print("  2. Generate videos for multiple stocks (batch)")
        print("  3. Extract narration and insights")
        print("  4. Exit")
        print()
        
        choice = input("Select option (1-4): ").strip()
        
        if choice == '1':
            ticker = input("Enter ticker (e.g., AAPL): ").strip().upper()
            example_single_stock(ticker)
        elif choice == '2':
            tickers_input = input("Enter tickers comma-separated (e.g., AAPL,MSFT,GOOGL): ").strip()
            tickers = [t.strip().upper() for t in tickers_input.split(',')]
            example_batch_stocks(tickers)
        elif choice == '3':
            example_extraction()
        elif choice == '4':
            print("Goodbye!")
        else:
            print("Invalid option")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        print("""
Usage:
  python example_video_generation.py              # Interactive mode
  python example_video_generation.py AAPL         # Generate video for AAPL
  python example_video_generation.py AAPL MSFT    # Generate for multiple stocks
  python example_video_generation.py batch AAPL MSFT GOOGL
  python example_video_generation.py extract      # Extract narration
        """)
    else:
        main()
