#!/usr/bin/env python3
"""Test audio synchronization in structured video."""

import logging
import sys

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

from services.analyzer import analyze_stock
from services.video_engine import generate_structured_video_report

def main():
    ticker = 'MSFT'
    print(f'\n{"="*60}')
    print(f'Audio Sync Test: {ticker}')
    print(f'{"="*60}\n')
    
    try:
        print(f'Step 1: Analyzing {ticker}...')
        analysis = analyze_stock(ticker)
        print(f'Step 1: DONE - Got analysis data\n')
        
        print(f'Step 2: Generating structured video with audio sync fix...')
        result = generate_structured_video_report(ticker, analysis)
        print(f'\nStep 2: DONE')
        print(f'\nVideo created: {result["video_path"]}')
        
        # Verify video
        from moviepy.editor import VideoFileClip
        video = VideoFileClip(result["video_path"])
        print(f'Video Duration: {video.duration:.2f}s')
        print(f'Video has audio: {video.audio is not None}')
        video.close()
        
    except Exception as e:
        logger.error(f'Error: {e}', exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
