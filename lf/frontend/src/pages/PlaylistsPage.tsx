import { useState, useEffect } from "react";
import axios from "axios";
import { Playlist } from "../model/Playlist";
import { PlaylistCard } from "../components/PlaylistCard/PlaylistCard";
import { Spinner } from "../components/Spinner/Spinner";

export const PlaylistsPage = () => {
  const [playlists, setPlaylists] = useState<Playlist[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPlaylists = async () => {
      try {
        setLoading(true);
        const response = await axios.get("/api/get-playlist");
        setPlaylists(response.data);
        setError(null);
      } catch (err) {
        console.error("Error fetching playlists:", err);
        setError("Failed to load playlists. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    fetchPlaylists();
  }, []);

  if (loading) {
    return <Spinner />;
  }

  if (error) {
    return (
      <div style={{ textAlign: "center", padding: "2rem" }}>
        <p style={{ color: "red" }}>{error}</p>
      </div>
    );
  }

  return (
    <div>
      <h1>Your Playlists</h1>
      <p>Select a playlist to generate an AI cover image</p>
      <div>
        {playlists.length === 0 ? (
          <p>No playlists found.</p>
        ) : (
          playlists.map((playlist) => (
            <PlaylistCard key={playlist.id} playlist={playlist} />
          ))
        )}
      </div>
    </div>
  );
};
