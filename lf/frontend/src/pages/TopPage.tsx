import { useState } from "react";
import axios from "axios";
import { Spinner } from "../components/Spinner/Spinner";
import styles from "./GeneratorPage.module.css";

interface Artist {
  id: string;
  name: string;
  genres?: string[];
  popularity: number;
  images: { url: string }[];
}

interface Track {
  id: string;
  name: string;
  artists: { name: string }[];
  album: { name: string };
  popularity: number;
}

export const TopPage = () => {
  const [artists, setArtists] = useState<Artist[] | null>(null);
  const [tracks, setTracks] = useState<Track[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTopArtists = async () => {
    try {
      setLoading(true);
      setError(null);
      setTracks(null);
      const response = await axios.get("/api/top-artists");
      setArtists(response.data);
    } catch (err) {
      console.error("Error fetching top artists:", err);
      setError("Failed to load top artists.");
    } finally {
      setLoading(false);
    }
  };

  const fetchTopTracks = async () => {
    try {
      setLoading(true);
      setError(null);
      setArtists(null);
      const response = await axios.get("/api/top-tracks");
      setTracks(response.data);
    } catch (err) {
      console.error("Error fetching top tracks:", err);
      setError("Failed to load top tracks.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h2>Your Top Spotify Content</h2>

      <div style={{ display: "flex", gap: "1rem", marginBottom: "1.5rem" }}>
        <button className={styles.generateButton} onClick={fetchTopArtists}>
          Artists
        </button>
        <button className={styles.generateButton} onClick={fetchTopTracks}>
          Tracks
        </button>
      </div>

      {loading && <Spinner />}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {artists && (
        <>
          <h3>Top Artists</h3>
          <ul className={styles.trackList}>
            {artists.map((artist, i) => (
              <li key={artist.id}>
                <strong>{i + 1}. {artist.name}</strong>
                {artist.genres?.length > 0 && (
                  <span style={{ color: "#b3b3b3", marginLeft: "0.5rem" }}>
                    — {artist.genres.slice(0, 3).join(", ")}
                  </span>
                )}
              </li>
            ))}
          </ul>
        </>
      )}

      {tracks && (
        <>
          <h3>Top Tracks</h3>
          <ul className={styles.trackList}>
            {tracks.map((track, i) => (
              <li key={track.id}>
                <strong>{i + 1}. {track.name}</strong>
                {" by "}
                {track.artists.map((a) => a.name).join(", ")}
                <span style={{ color: "#b3b3b3", marginLeft: "0.5rem" }}>
                  — {track.album.name}
                </span>
              </li>
            ))}
          </ul>
        </>
      )}
    </div>
  );
};
