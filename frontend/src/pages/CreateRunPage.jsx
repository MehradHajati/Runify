import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Header from "../heading/Header";
import HeroSection from "../heading/HeroSection";
import Button from "../components/Button";
import InfoCard from "../components/InfoCard";

const CreateRunPage = () => {
  const navigate = useNavigate();

  const [playlistTitle, setPlaylistTitle] = useState("");
  const [runDistance, setRunDistance] = useState("");
  const [runTime, setRunTime] = useState("");
  const [height, setHeight] = useState("");
  const [sex, setSex] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    // Move to the Spotify Playlist Selection page, passing along the parameters.
    navigate("/playlist-selection", {
      state: {
        playlistTitle,
        runDistance,
        runTime,
        height,
        sex,
      },
    });
  };

  return (
    <div className="app">
      <Header />
      <HeroSection />

      <div className="content">
        <div
          className="create-run-section"
          style={{ width: "530px", maxWidth: "100%" }}
        >
          <InfoCard>
            Create a personalized running playlist by entering your run details
            below.
          </InfoCard>

          <div className="form-box">
            <div className="form-title">Create New Run Playlist</div>
            <div className="form-container">
              <form onSubmit={handleSubmit}>
                <div className="input-group">
                  <div className="input-label">Playlist Title</div>
                  <input
                    type="text"
                    className="input-field"
                    value={playlistTitle}
                    onChange={(e) => setPlaylistTitle(e.target.value)}
                    placeholder="My Running Playlist"
                    required
                  />
                </div>

                <div className="input-group">
                  <div className="input-label">
                    Target Run Distance (meters)
                  </div>
                  <input
                    type="number"
                    step="any"
                    className="input-field"
                    value={runDistance}
                    onChange={(e) => setRunDistance(e.target.value)}
                    placeholder="5000"
                    required
                  />
                </div>

                <div className="input-group">
                  <div className="input-label">Target Run Time (minutes)</div>
                  <input
                    type="number"
                    step="any"
                    className="input-field"
                    value={runTime}
                    onChange={(e) => setRunTime(e.target.value)}
                    placeholder="30"
                    required
                  />
                </div>

                <div className="input-group">
                  <div className="input-label">Height (meters)</div>
                  <input
                    type="number"
                    step="any"
                    className="input-field"
                    value={height}
                    onChange={(e) => setHeight(e.target.value)}
                    placeholder="1.75"
                    required
                  />
                </div>

                <div className="input-group">
                  <div className="input-label">Sex</div>
                  <select
                    className="input-field"
                    value={sex}
                    onChange={(e) => setSex(e.target.value)}
                    required
                  >
                    <option value="">Select Sex</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <Button type="submit">Generate Run</Button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CreateRunPage;
