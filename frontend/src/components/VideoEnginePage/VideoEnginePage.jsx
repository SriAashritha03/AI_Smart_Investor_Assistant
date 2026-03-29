import React from 'react'
import { FaFilm } from 'react-icons/fa'
import VideoEngine from '../VideoEngine/VideoEngine'
import './VideoEnginePage.css'

function VideoEnginePage() {
  return (
    <div className="page-container video-engine-page">
      <div className="page-header">
        <h2 className="page-title"><FaFilm style={{ marginRight: '8px' }} />AI Video Engine</h2>
        <p className="page-description">Generate AI-powered analysis videos for stocks</p>
      </div>
      <VideoEngine />
    </div>
  )
}

export default VideoEnginePage
