#!/usr/bin/env python3
"""Quick test to generate a single MSFT video"""

import sys
sys.path.insert(0, '.')

from services.analyzer import analyze_stock
from services.video_engine import generate_market_video, generate_structured_video_report
import os

print("\n" + "="*60)
print("  QUICK VIDEO GENERATION TEST")
print("="*60 + "\n")

ticker = "MSFT"

# Test 1: Legacy video
print(f"[1] Generating legacy video for {ticker}...")
try:
    video_path = generate_market_video(ticker)
    if os.path.exists(video_path):
        size_mb = os.path.getsize(video_path) / (1024*1024)
        print(f"    ✓ Legacy video created!")
        print(f"      Path: {video_path}")
        print(f"      Size: {size_mb:.2f} MB")
    else:
        print(f"    ✗ Video file not found: {video_path}")
except Exception as e:
    print(f"    ✗ Error: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()

# Test 2: Structured video
print(f"\n[2] Analyzing {ticker} for structured video...")
try:
    analysis = analyze_stock(ticker)
    if analysis.get('success'):
        print(f"    ✓ Analysis complete")
        print(f"      Action: {analysis.get('action')}")
        print(f"      Confidence: {analysis.get('confidence')}%")
        
        print(f"\n[3] Generating structured video...")
        report = generate_structured_video_report(ticker, analysis)
        if report.get('success'):
            video_path = report.get('video_path')
            if os.path.exists(video_path):
                size_mb = os.path.getsize(video_path) / (1024*1024)
                print(f"    ✓ Structured video created!")
                print(f"      Path: {video_path}")
                print(f"      Size: {size_mb:.2f} MB")
                print(f"      Frames: {len(report.get('frames', []))}")
            else:
                print(f"    ✗ Video file not found: {video_path}")
        else:
            print(f"    ✗ Video generation failed: {report.get('error')}")
    else:
        print(f"    ✗ Analysis failed: {analysis.get('error')}")
except Exception as e:
    print(f"    ✗ Error: {type(e).__name__}: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("  Checking videos folder...")
print("="*60)
from pathlib import Path
videos_dir = Path("videos")
mp4_files = list(videos_dir.glob("*.mp4"))
print(f"\nMP4 files in ./videos: {len(mp4_files)}")
for f in sorted(mp4_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
    size = f.stat().st_size / (1024*1024)
    print(f"  - {f.name} ({size:.2f} MB)")

print("\n")
