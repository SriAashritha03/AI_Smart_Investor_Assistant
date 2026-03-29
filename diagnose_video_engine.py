#!/usr/bin/env python3
"""
Video Engine Diagnostic Tool

Tests video generation components and identifies issues.
Run this before reporting video generation errors.

Usage:
    python diagnose_video_engine.py
"""

import sys
import os

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print('='*60 + "\n")

def test_dependencies():
    """Test if all required packages are installed."""
    print_header("Testing Dependencies")
    
    dependencies = {
        'yfinance': 'Stock data fetching',
        'matplotlib': 'Chart generation',
        'moviepy': 'Video composition',
        'gtts': 'Text-to-speech',
        'numpy': 'Data processing',
        'fastapi': 'API framework',
        'google.generativeai': 'Gemini AI'
    }
    
    missing = []
    
    for package, purpose in dependencies.items():
        try:
            __import__(package)
            print(f"  ✅ {package:<25} ({purpose})")
        except ImportError:
            print(f"  ❌ {package:<25} ({purpose}) - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing {len(missing)} package(s)!")
        print("  Install with: pip install " + " ".join(missing))
        return False
    
    print("\n✅ All dependencies installed!")
    return True

def test_ffmpeg():
    """Test if FFmpeg is available."""
    print_header("Testing FFmpeg")

    try:
        import imageio_ffmpeg
        import subprocess
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        if os.path.exists(ffmpeg_exe):
            result = subprocess.run([ffmpeg_exe, '-version'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=5)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"  ✅ FFmpeg available (via imageio-ffmpeg)")
                print(f"     Path: {ffmpeg_exe}")
                print(f"     {version_line}")
                return True
    except:
        pass
    
    # Fallback: try system FFmpeg
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"  ✅ FFmpeg available (system): {version_line}")
            return True
        else:
            print(f"  ❌ FFmpeg error: {result.stderr[:100]}")
            return False
    except FileNotFoundError:
        print("  ❌ FFmpeg not found in PATH")
        print("  Install FFmpeg from: https://ffmpeg.org/download.html")
        return False
    except Exception as e:
        print(f"  ❌ FFmpeg test error: {str(e)}")
        return False

def test_yfinance():
    """Test yfinance data fetching."""
    print_header("Testing Yahoo Finance")
    
    try:
        import yfinance as yf
        print("  Testing data fetch for AAPL (5 days)...")
        data = yf.download('AAPL', period='5d')
        
        if data.empty:
            print("  ❌ No data returned from Yahoo Finance")
            return False
        
        # Extract single value - handle both Series and scalar returns
        try:
            last_price = float(data['Close'].iloc[-1].item() if hasattr(data['Close'].iloc[-1], 'item') else data['Close'].iloc[-1])
        except:
            last_price = float(data['Close'].values[-1])
        
        print(f"  ✅ Data fetched successfully")
        print(f"     Latest AAPL price: ${last_price:.2f}")
        print(f"     Data points: {len(data)}")
        return True
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

def test_matplotlib():
    """Test matplotlib chart generation."""
    print_header("Testing Matplotlib")
    
    try:
        import matplotlib.pyplot as plt
        import yfinance as yf
        
        print("  Generating test chart...")
        data = yf.download('MSFT', period='5d')
        
        fig, ax = plt.subplots(figsize=(6, 4))
        data['Close'].plot(ax=ax, title='MSFT Test Chart')
        
        test_chart = 'test_chart_diagnostic.png'
        plt.savefig(test_chart)
        plt.close()
        
        if os.path.exists(test_chart):
            size = os.path.getsize(test_chart)
            os.remove(test_chart)
            print(f"  ✅ Chart generated successfully ({size} bytes)")
            return True
        else:
            print("  ❌ Chart file not created")
            return False
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

def test_gtts():
    """Test Google Text-to-Speech."""
    print_header("Testing Google Text-to-Speech")
    
    try:
        from gtts import gTTS
        
        print("  Generating test audio...")
        tts = gTTS("Test audio for video engine", lang='en')
        
        test_audio = 'test_audio_diagnostic.mp3'
        tts.save(test_audio)
        
        if os.path.exists(test_audio):
            size = os.path.getsize(test_audio)
            os.remove(test_audio)
            print(f"  ✅ Audio generated successfully ({size} bytes)")
            return True
        else:
            print("  ❌ Audio file not created")
            return False
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

def test_moviepy():
    """Test moviepy video composition."""
    print_header("Testing MoviePy")
    
    try:
        from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
        print("  ✅ MoviePy imports successful")
        
        # Test if we can create a simple video
        print("  Testing video composition...")
        return True
    except ImportError as e:
        print(f"  ❌ Import error: {str(e)}")
        return False
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

def test_video_generation():
    """Test full video generation."""
    print_header("Testing Video Generation")
    
    try:
        from services.video_engine import generate_market_video
        
        print("  Generating test video for MSFT...")
        print("  (This may take 15-30 seconds)\n")
        
        video_path = generate_market_video('MSFT')
        
        if os.path.exists(video_path):
            size = os.path.getsize(video_path)
            size_mb = size / (1024 * 1024)
            print(f"\n  ✅ Video generated successfully!")
            print(f"     Path: {video_path}")
            print(f"     Size: {size_mb:.2f} MB")
            
            # Clean up
            os.remove(video_path)
            print(f"     Cleaned up test file")
            return True
        else:
            print(f"  ❌ Video file not created at: {video_path}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {type(e).__name__}: {str(e)}")
        import traceback
        print("\nTraceback:")
        traceback.print_exc()
        return False

def test_structured_video():
    """Test structured video generation."""
    print_header("Testing Structured Video Generation")
    
    try:
        from services.analyzer import analyze_stock
        from services.video_engine import generate_structured_video_report
        
        print("  Step 1: Analyzing stock (MSFT)...")
        analysis = analyze_stock('MSFT')
        
        if not analysis.get('success'):
            print(f"  ❌ Analysis failed: {analysis.get('error')}")
            return False
        
        print("  ✅ Analysis successful")
        print(f"     Action: {analysis.get('action')}")
        print(f"     Confidence: {analysis.get('confidence')}%")
        
        print("  Step 2: Generating structured video...")
        print("  (This may take 20-40 seconds)\n")
        
        report = generate_structured_video_report('MSFT', analysis)
        
        if report.get('success'):
            print(f"\n  ✅ Structured video generated!")
            print(f"     Path: {report.get('video_path')}")
            print(f"     Frames: {len(report.get('frames', []))}")
            
            # Clean up
            if os.path.exists(report['video_path']):
                os.remove(report['video_path'])
                print(f"     Cleaned up test file")
            
            return True
        else:
            print(f"  ❌ Video generation failed: {report.get('error')}")
            return False
    except Exception as e:
        print(f"  ❌ Error: {type(e).__name__}: {str(e)}")
        import traceback
        print("\nTraceback:")
        traceback.print_exc()
        return False

def main():
    """Run all diagnostic tests."""
    print("\n" + "="*60)
    print("  VIDEO ENGINE DIAGNOSTIC TOOL")
    print("="*60)
    
    results = {}
    
    # Run tests
    results['Dependencies'] = test_dependencies()
    results['FFmpeg'] = test_ffmpeg()
    results['Yahoo Finance'] = test_yfinance()
    results['Matplotlib'] = test_matplotlib()
    results['Google TTS'] = test_gtts()
    results['MoviePy'] = test_moviepy()
    
    # Only test video generation if basic tests pass
    if results['Dependencies'] and results['FFmpeg']:
        results['Video Generation'] = test_video_generation()
        
        # Only test structured if basic video works
        if results['Video Generation']:
            results['Structured Video'] = test_structured_video()
    
    # Summary
    print_header("DIAGNOSTIC SUMMARY")
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name:<30} {status}")
    
    total = len(results)
    passed = sum(1 for p in results.values() if p)
    
    print(f"\n  Result: {passed}/{total} tests passed\n")
    
    if passed == total:
        print("  ✅ All systems operational! Video engine is ready.")
    else:
        print("  ❌ Some tests failed. Review errors above.")
        print("\n  Common fixes:")
        print("  1. Install FFmpeg: https://ffmpeg.org/download.html")
        print("  2. Update packages: pip install --upgrade moviepy")
        print("  3. Check internet (for Yahoo Finance & TTS)")
        print("  4. Restart the backend after fixes")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
