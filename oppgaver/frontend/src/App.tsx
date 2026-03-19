import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import "./styles/App.css";
import { PlaylistsPage } from "./pages/PlaylistsPage";
import { GeneratorPage } from "./pages/GeneratorPage";
import { CoverImageListPage } from "./pages/CoverImageListPage";
import { TopPage } from "./pages/TopPage";
import { Navbar } from "./components/Navbar/Navbar";
import { Spinner } from "./components/Spinner/Spinner";

function App() {
  const [authorized, setAuthorized] = useState<boolean | null>(null);

  useEffect(() => {
    axios.get("/api/auth-status")
      .then((res) => setAuthorized(res.data.authorized))
      .catch(() => setAuthorized(false));
  }, []);

  if (authorized === null) {
    return <Spinner />;
  }

  if (!authorized) {
    return (
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", height: "100vh", gap: "1rem" }}>
        <h1>Spotify AI Workshop</h1>
        <p>Log in with Spotify to get started.</p>
        <a href="/api/login">
          <button style={{ padding: "0.75rem 2rem", fontSize: "1rem", borderRadius: "2rem", background: "#1DB954", color: "white", border: "none", cursor: "pointer" }}>
            Login with Spotify
          </button>
        </a>
      </div>
    );
  }

  return (
    <div>
      <Router>
        <div className="header-container">
          <Navbar />
        </div>

        <div className="content">
          <Routes>
            <Route path="/" element={<PlaylistsPage />} />
            <Route path="/cover/:playlistId" element={<GeneratorPage />} />
            <Route path="/gallery" element={<CoverImageListPage />} />
            <Route path="/top" element={<TopPage />} />
          </Routes>
        </div>
      </Router>
    </div>
  );
}

export default App;
