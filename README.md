# Running Playlist Builder

A full‑stack application that connects with Spotify to generate cadence‑matched running playlists. The project consists of a **Flask backend** (Spotify OAuth, playlist generation, optional MySQL user accounts) and a **React frontend** (runner inputs, playlist selection, and summary).

> **Status**: Spotify OAuth flow is the primary authentication method. Database‑backed account creation/login is partially implemented and may evolve.

---

## Features

### Backend

* **Spotify OAuth** login
* Fetch user playlists and compute durations
* Generate cadence‑matched running playlists from selected playlists
* Save generated playlists to Spotify
* (Optional) MySQL user accounts & playlist persistence (WIP)

### Frontend

* **LoginPage** — Account creation or sign in with Spotify【95†source】
* **CreateRunPage** — Input run details (title, distance, time, height, sex)【94†source】
* **SpotifyPlaylistSelectionPage** — Browse and select source Spotify playlists【97†source】
* **PlaylistSummaryPage** — Preview generated playlist with distance, duration, average tempo, and tracks【96†source】
* **Header** — Top navigation with logo and menu icon【131†source】
* **HeroSection** — Landing page hero with motivating message and image【132†source】
* **Reusable UI components**:

  * `Button` — generic styled button【133†source】
  * `FormBox` / `FormContainer` — login/register forms with email & password inputs【134†source】【135†source】
  * `InputBox` — labeled input field【137†source】
  * `InfoCard` — styled container for content【136†source】
* **API client** — `api.js` with helper methods `createAccount` and `login` calling backend endpoints【138†source】
* Responsive design styled via `index.css` and `App.css`【103†source】【98†source】

---

## Architecture

### Backend

* **Framework**: Flask + Flask‑CORS
* **Files**: `app.py`, `config.py`, `db.py`, `init_db.py`, `schema.sql`, `simple_auth.py`
* **Data**: `track_data.csv` (tempo enrichment), `accounts.json` (legacy JSON auth)

### Frontend

* **Framework**: React (React Router for navigation)
* **Entry point**: `App.js` — defines routes (`/`, `/create-run`, `/playlist-selection`, `/playlist-summary`)【99†source】
* **Styling**: `index.css` (custom UI), `App.css` (CRA defaults)【98†source】【103†source】
* **Testing**: Jest with `App.test.js`, `setupTests.js`【101†source】【102†source】
* **Performance reporting**: `reportWebVitals.js`【100†source】
* **UI Components**: Header, HeroSection, Button, FormBox, FormContainer, InfoCard, InputBox【131†source】【132†source】【133†source】【134†source】【135†source】【136†source】【137†source】
* **API Layer**: `api.js` — manages account creation and login calls【138†source】

---

## Prerequisites

* Python 3.9+
* Node.js 16+
* Spotify Developer app (client ID/secret, redirect URI)
* (Optional) MySQL 8+ if using DB features

---

## Installation

### Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set environment variables in `.env` (see backend section in previous README draft). Run server:

```bash
flask --app app.py run --debug --port 5000
```

### Frontend

```bash
cd frontend
npm install
```

Create `.env` in `frontend/`:

```dotenv
REACT_APP_BACKEND_URL=http://localhost:5000
```

Run development server:

```bash
npm start
```

The frontend will be available at `http://localhost:3000`.

---

## Usage Flow

1. **Visit `/`** → LoginPage

   * Create account or sign in with Spotify【95†source】
2. **After auth**, go to `/create-run` → input run details【94†source】
3. **Select playlists** on `/playlist-selection`【97†source】
4. **Preview & save** generated playlist on `/playlist-summary`【96†source】

---

## API Reference (Backend)

See previous backend README draft for detailed endpoint docs (`/auth`, `/callback`, `/playlists`, `/generate-playlist`, `/save-playlist`).

---

## Development Tips

* Always set `REACT_APP_BACKEND_URL` in frontend `.env`
* Ensure backend session cookies are included (`credentials: "include"` already set)
* CORS enabled in backend for local dev
* For DB mode, run `init_db.py` before account creation
* Use the reusable frontend components for consistent styling and behavior

---

## Roadmap

* Finalize DB account system or remove in favor of Spotify‑only login
* Add playlist persistence & analytics
* Expand tests (React components + Flask API)
* Enhance landing page with HeroSection and InfoCards for more user guidance

