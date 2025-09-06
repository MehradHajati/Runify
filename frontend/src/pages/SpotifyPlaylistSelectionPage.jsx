import React, { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import Header from "../heading/Header";
import HeroSection from "../heading/HeroSection";
import InfoCard from "../components/InfoCard";
import Button from "../components/Button";

const SpotifyPlaylistSelectionPage = () => {
  const navigate = useNavigate();
  const location = useLocation(); // Contains run parameters from CreateRunPage
  const backendUrl = process.env.REACT_APP_BACKEND_URL;
  const [playlists, setPlaylists] = useState([]);
  const [selectedPlaylists, setSelectedPlaylists] = useState([]);

  // Helper function to format duration in ms to "Xm Ys"
  const formatDuration = (duration_ms) => {
    if (!duration_ms) return "0m 0s";
    const minutes = Math.floor(duration_ms / 60000);
    const seconds = Math.floor((duration_ms % 60000) / 1000);
    return `${minutes}m ${seconds}s`;
  };

  useEffect(() => {
    // Fetch user's Spotify playlists from the backend
    fetch(`${backendUrl}/playlists`, { credentials: "include" })
      .then((response) => response.json())
      .then((data) => {
        if (data.playlists) {
          setPlaylists(data.playlists);
        } else {
          console.error("No playlists found in response.");
        }
      })
      .catch((error) => console.error("Error fetching playlists:", error));
  }, [backendUrl]);

  // Toggle selection for a playlist
  const togglePlaylist = (playlist) => {
    const isSelected = selectedPlaylists.some((p) => p.id === playlist.id);
    if (isSelected) {
      setSelectedPlaylists(
        selectedPlaylists.filter((p) => p.id !== playlist.id),
      );
    } else {
      setSelectedPlaylists([...selectedPlaylists, playlist]);
    }
  };

  // Proceed to PlaylistSummaryPage with run parameters and selected playlists
  const handleGeneratePlaylist = () => {
    if (selectedPlaylists.length === 0) {
      alert("Please select at least one playlist.");
      return;
    }
    navigate("/playlist-summary", {
      state: {
        ...location.state, // Pass along run parameters from CreateRunPage
        selectedPlaylists,
      },
    });
  };

  return (
    <div className="app">
      <Header />
      <HeroSection />

      <div className="content">
        <div
          className="playlist-selection-section"
          style={{ width: "100%", maxWidth: "1200px" }}
        >
          <InfoCard>
            Select the playlists you want to use for generating your running
            playlist. Click on a playlist to select or deselect it.
          </InfoCard>

          <div className="form-card">
            <div className="form-title">Select Spotify Playlists</div>
            <div className="form-container">
              <div
                className="playlists-container"
                style={{
                  display: "grid",
                  gridTemplateColumns: "repeat(auto-fill, minmax(300px, 1fr))",
                  gap: "20px",
                  maxWidth: "100%",
                }}
              >
                {playlists.map((playlist) => {
                  // Determine if this playlist is selected
                  const isSelected = selectedPlaylists.some(
                    (p) => p.id === playlist.id,
                  );
                  // Use the cover image if available; otherwise, show a placeholder.
                  const coverUrl =
                    playlist.images && playlist.images.length > 0
                      ? playlist.images[0].url
                      : "https://via.placeholder.com/120";
                  return (
                    <div
                      key={playlist.id}
                      className={`playlist-card ${
                        isSelected ? "selected" : ""
                      }`}
                      onClick={() => togglePlaylist(playlist)}
                      style={{
                        border: isSelected
                          ? "3px solid #026dff"
                          : "1px solid #ccc",
                        borderRadius: "8px",
                        padding: "10px",
                        cursor: "pointer",
                        display: "flex",
                        alignItems: "center",
                        backgroundColor: "#fff",
                        transition: "all 0.2s ease",
                        boxShadow: isSelected
                          ? "0 4px 8px rgba(2, 109, 255, 0.2)"
                          : "none",
                      }}
                    >
                      <img
                        src={coverUrl}
                        alt={playlist.name}
                        style={{
                          width: "80px",
                          height: "80px",
                          objectFit: "cover",
                          borderRadius: "4px",
                        }}
                      />
                      <div
                        style={{
                          marginLeft: "15px",
                          textAlign: "left",
                          overflow: "hidden",
                        }}
                      >
                        <div
                          style={{
                            fontWeight: "bold",
                            fontSize: "1em",
                            marginBottom: "5px",
                            whiteSpace: "nowrap",
                            overflow: "hidden",
                            textOverflow: "ellipsis",
                          }}
                        >
                          {playlist.name}
                        </div>
                        <div
                          style={{
                            fontSize: "0.9em",
                            color: "#555",
                          }}
                        >
                          Duration: {formatDuration(playlist.duration_ms)}
                        </div>
                        <div
                          style={{
                            fontSize: "0.9em",
                            color: "#555",
                          }}
                        >
                          Tracks: {playlist.total_tracks}
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>

              <div style={{ marginTop: "30px" }}>
                <Button onClick={handleGeneratePlaylist}>
                  Generate Playlist
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SpotifyPlaylistSelectionPage;
