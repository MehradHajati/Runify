import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import CreateRunPage from './pages/CreateRunPage';
import SpotifyPlaylistSelectionPage from './pages/SpotifyPlaylistSelectionPage';
import PlaylistSummaryPage from './pages/PlaylistSummaryPage';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/create-run" element={<CreateRunPage />} />
        <Route path="/playlist-selection" element={<SpotifyPlaylistSelectionPage />} />
        <Route path="/playlist-summary" element={<PlaylistSummaryPage />} />
        {/* Redirect any unknown route to the login page */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
};

export default App;