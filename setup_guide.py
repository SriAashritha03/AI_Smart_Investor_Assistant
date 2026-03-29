#!/usr/bin/env python3
"""
Quick Setup & Test Guide for AI Smart Investor Video Engine

This script provides step-by-step guidance for:
1. Verifying environment setup
2. Installing missing dependencies
3. Testing all components
4. Running the backend

Usage:
    python setup_guide.py
    
Or import in your startup script:
    from setup_guide import verify_setup, diagnose_issues
"""

import subprocess
import sys
import os

def print_section(title, level=1):
    """Print formatted section header."""
    if level == 1:
        print(f"\n{'='*70}")
        print(f"  {title}")
        print('='*70)
    elif level == 2:
        print(f"\n{title}")
        print('-' * len(title))

def print_step(step_num, title, description=""):
    """Print a step."""
    print(f"\n  [{step_num}] {title}")
    if description:
        for line in description.split('\n'):
            print(f"      {line}")

def check_command(cmd):
    """Check if a command exists in PATH."""
    try:
        result = subprocess.run([cmd, '--version'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        return result.returncode == 0
    except:
        return False

def main():
    """Run setup guide."""
    print_section("AI SMART INVESTOR - VIDEO ENGINE SETUP GUIDE")
    
    print("""
This guide will help you set up and test the video generation system.

WARNINGS:
  ⚠️  FFmpeg is REQUIRED - video generation will not work without it
  ⚠️  Internet required for stock data (Yahoo Finance) and text-to-speech
  ⚠️  First video generation takes 15-30 seconds (normal)
""")
    
    # Step 1: Check environment
    print_section("STEP 1: Check Python Environment", level=2)
    print_step(1, "Verify Python version", f"Current: {sys.version.split()[0]}")
    if sys.version_info < (3, 8):
        print("  ❌ Python 3.8+ required")
        return False
    else:
        print(f"  ✅ Python {sys.version_info.major}.{sys.version_info.minor} suitable")
    
    # Step 2: Check dependencies
    print_section("STEP 2: Verify Python Packages", level=2)
    
    packages = [
        ('yfinance', 'Stock data fetching'),
        ('matplotlib', 'Chart generation'),
        ('moviepy', 'Video composition'),
        ('gtts', 'Text-to-speech'),
        ('fastapi', 'Web framework'),
    ]
    
    missing = []
    for pkg, desc in packages:
        try:
            __import__(pkg)
            print(f"  ✅ {pkg:<20} {desc}")
        except ImportError:
            print(f"  ❌ {pkg:<20} {desc}")
            missing.append(pkg)
    
    if missing:
        print(f"\n  Install missing: pip install {' '.join(missing)}")
        print("  Then re-run this script")
        return False
    
    # Step 3: FFmpeg check
    print_section("STEP 3: Check FFmpeg Installation", level=2)
    
    if check_command('ffmpeg'):
        print("  ✅ FFmpeg found in PATH")
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True)
        version = result.stdout.split('\n')[0]
        print(f"     {version}")
    else:
        print("  ❌ FFmpeg NOT FOUND")
        print("""
  INSTALLATION REQUIRED:
  
  Option 1 (Recommended - Chocolatey):
    choco install ffmpeg
    
  Option 2 (Manual):
    1. Download from: https://ffmpeg.org/download.html
    2. Extract to: C:\\ffmpeg
    3. Add C:\\ffmpeg\\bin to PATH environment variable
    4. Restart PowerShell/Command Prompt
    
  Option 3 (Scoop):
    scoop install ffmpeg
    
  See FFMPEG_SETUP.md for detailed instructions.
""")
        print("  ⚠️  Video generation will not work until FFmpeg is installed!")
        return False
    
    # Step 4: Run diagnostics
    print_section("STEP 4: Run Full Diagnostics", level=2)
    
    print("""
  Run the diagnostic tool to test all components:
  
    python diagnose_video_engine.py
    
  This will test:
    ✓ All Python dependencies
    ✓ FFmpeg availability
    ✓ Yahoo Finance data fetching
    ✓ Chart generation
    ✓ Text-to-speech
    ✓ Video composition
    ✓ Full video generation pipeline
""")
    
    # Step 5: Start backend
    print_section("STEP 5: Start Backend Server", level=2)
    
    print("""
  Start the FastAPI server:
  
    python main.py
    
  You should see:
    INFO:     Uvicorn running on http://127.0.0.1:8000
""")
    
    # Step 6: Test endpoints
    print_section("STEP 6: Test Video Generation Endpoints", level=2)
    
    print("""
  After backend is running, test the endpoints:
  
  A) Legacy endpoint (6-second simple video):
     curl "http://localhost:8000/generate-video?ticker=MSFT"
     
  B) New structured endpoint (24-second AI insights):
     curl -X POST "http://localhost:8000/generate-structured-video" \\
       -H "Content-Type: application/json" \\
       -d '{"ticker":"AAPL"}'
  
  Expected results:
    ✓ Downloads MP4 file (2-5 MB per video)
    ✓ Returns within 30 seconds
    ✓ File is playable in any media player
""")
    
    # Step 7: Troubleshooting
    print_section("STEP 7: Troubleshooting", level=2)
    
    print("""
  If you encounter issues:
  
  1. "FFmpeg not found" or "500 error"
     → Install FFmpeg and restart backend
     
  2. "No data found for AAPL"
     → Check internet connection
     → Try valid ticker: MSFT, AAPL, GOOGL, AMZN
     
  3. "Video file not created"
     → Check project directory for video_*.mp4 files
     → Re-run diagnose_video_engine.py to identify root cause
     
  4. "Audio generation failed"
     → Check internet (needed for Google TTS)
     → Try again after a few seconds
     
  5. "Matrix operation error" / Memory issues
     → FFmpeg may need more memory
     → Try generating video for different ticker
     → Restart backend and try again
""")
    
    # Step 8: Next steps
    print_section("STEP 8: Next Steps", level=2)
    
    print("""
  After you've successfully tested video generation:
  
  1. Integrate with frontend application
     → See VIDEO_ENGINE_IMPLEMENTATION.md for React examples
     
  2. Set up batch processing
     → Use example_video_generation.py as reference
     
  3. Monitor video quality
     → Check generated videos in project directory
     → Adjust frame sizes/styles in video_engine.py if needed
     
  4. Production deployment
     → Coordinate with DevOps/deployment team
     → Ensure FFmpeg on production servers
     → Set up caching for frequently generated videos
""")
    
    print_section("Setup Guide Complete")
    print("""
  ✅ Environment verified
  ✅ Dependencies installed
  ✅ FFmpeg configured
  ✅ Ready to generate videos!
  
  Questions? Check these files:
    • FFMPEG_SETUP.md - FFmpeg installation details
    • VIDEO_ENGINE_GUIDE.md - Architecture & API reference
    • VIDEO_ENGINE_IMPLEMENTATION.md - Integration examples
    • diagnose_video_engine.py - Run diagnostics anytime
""")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
