import React from 'react'
import VideoEngine from '../VideoEngine/VideoEngine'
import './VideoEnginePage.css'

function VideoEnginePage() {
  return (
    <div className="video-engine-page">
      <div className="page-header">
        <h2 className="page-title">
          <span className="material-symbols-outlined" style={{ fontSize: '32px', color: 'var(--primary)' }}>auto_videocam</span>
          Market Synthesis Console
        </h2>
        <p className="page-description">Generate AI-powered dynamic visualisations for asset intelligence streams</p>
      </div>
      <VideoEngine />
    </div>
  )
}

export default VideoEnginePage
