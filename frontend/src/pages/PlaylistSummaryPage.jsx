import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Header from "../heading/Header";
import HeroSection from "../heading/HeroSection";
import InfoCard from "../components/InfoCard";

const PlaylistSummaryPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const backendUrl = process.env.REACT_APP_BACKEND_URL;

  const [isLoading, setIsLoading] = useState(true);
  const [playlistPreview, setPlaylistPreview] = useState(null);
  const [error, setError] = useState("");

  // location.state should contain run parameters and selectedPlaylists passed from previous pages.
  const state = location.state;

  useEffect(() => {
    if (!state) {
      // If no state is present, redirect back to the Create Run page.
      navigate("/create-run");
      return;
    }

    // Build payload with run parameters and selected playlists.
    const payload = {
      playlistTitle: state.playlistTitle,
      runDistance: state.runDistance,
      runTime: state.runTime,
      height: state.height,
      sex: state.sex,
      selectedPlaylists: state.selectedPlaylists,
    };

    // Send a POST request to generate the running playlist.
    fetch(`${backendUrl}/generate-playlist`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify(payload),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          setPlaylistPreview(data.playlist);
        } else {
          setError(data.message || "Playlist generation failed.");
        }
        setIsLoading(false);
      })
      .catch((err) => {
        console.error("Error generating playlist:", err);
        setError("Error generating playlist.");
        setIsLoading(false);
      });
  }, [backendUrl, navigate, state]);

  // Handler to save the generated playlist to the user's Spotify account.
  const handleSave = () => {
    fetch(`${backendUrl}/save-playlist`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ playlist: playlistPreview }),
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.success) {
          navigate("/create-run");
        } else {
          alert(data.message || "Failed to save playlist.");
        }
      })
      .catch((err) => {
        console.error("Error saving playlist:", err);
        alert("Error saving playlist.");
      });
  };

  // Handler to cancel and return back to the Create Run page (without saving).
  const handleCancel = () => {
    navigate("/create-run");
  };

  if (isLoading) {
    return (
      <div className="app">
        <Header />
        <HeroSection />
        <div className="content">
          <div className="playlist-summary-section">
            <div className="form-card">
              <div className="form-title">Generating Playlist</div>
            </div>
            <InfoCard>
              Generating your personalized running playlist. This may take a moment...
            </InfoCard>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app">
        <Header />
        <HeroSection />
        <div className="content">
          <div className="playlist-summary-section">
            <InfoCard>
              There was an error generating your playlist. Please try again.
            </InfoCard>
            <div className="form-card">
              <div className="form-title">Error</div>
              <div className="form-container">
                <div className="error-message">{error}</div>
                <button className="action-button" onClick={handleCancel}>
                  Back to Create Run
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="app">
      <Header />
      <HeroSection />
      <div className="content">
        <div className="playlist-summary-section">
          <InfoCard>
            Review your personalized running playlist below. You can save it to your Spotify account or go back to create a different playlist.
          </InfoCard>
          <div className="containers-wrapper">
            {/* Playlist Details Container */}
            <div className="form-card details-card">
              <div className="form-container">
                <div className="playlist-details">
                  <div className="playlist-title">{playlistPreview.title}</div>
                  <div className="playlist-cover">
                    <img
                      src="/images/samplecover.jpg"
                      alt="Playlist Cover"
                      className="cover-image"
                    />
                  </div>
                  <div className="playlist-stats">
                    <div className="detail-item">
                      <div className="detail-label">Actual Distance:</div>
                      <div className="detail-value">
                        {playlistPreview.actualDistance} m
                      </div>
                    </div>
                    <div className="detail-item">
                      <div className="detail-label">Actual Duration:</div>
                      <div className="detail-value">
                        {playlistPreview.actualDuration} min
                      </div>
                    </div>
                    <div className="detail-item">
                      <div className="detail-label">Average Tempo (BPM):</div>
                      <div className="detail-value">
                        {playlistPreview.avgTempo}
                      </div>
                    </div>
                  </div>
                  <div className="action-buttons">
                    <button className="cancel-button" onClick={handleCancel}>
                      Cancel
                    </button>
                    <button className="save-button" onClick={handleSave}>
                      Save
                    </button>
                  </div>
                </div>
              </div>
            </div>

            {/* Songs Container */}
            <div className="form-card songs-card">
              <div className="form-container">
                <div className="songs-section">
                  <div className="songs-title">Preview Playlist</div>
                  <div className="songs-container">
                    {playlistPreview.songs.map((song, index) => (
                      <div key={index} className="song-item">
                        <img
                          src={song.image}
                          alt={song.title}
                          className="song-image"
                        />
                        <div className="song-details">
                          <div className="song-title">{song.title}</div>
                          <div className="song-artist">Artist: {song.artist}</div>
                          <div className="song-tempo">
                            Tempo (BPM): {Math.round(song.tempo)}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlaylistSummaryPage;