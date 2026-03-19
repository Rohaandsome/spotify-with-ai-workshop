import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import { Track } from "../model/Playlist.ts";
import { Spinner } from "../components/Spinner/Spinner.tsx";
import { useUserId } from "../hooks/useUserId.ts";
import styles from "./GeneratorPage.module.css";

export const GeneratorPage = () => {
  const { playlistId } = useParams<{ playlistId: string }>();
  const userId = useUserId();
  const [tracks, setTracks] = useState<Track[]>([]);
  const [coverUrl, setCoverUrl] = useState<string | null>(null);
  const [description, setDescription] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [generatingDescription, setGeneratingDescription] = useState(false);
  const [settingCover, setSettingCover] = useState(false);
  const [coverSet, setCoverSet] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTracks = async () => {
      try {
        setLoading(true);
        const response = await axios.get(`/api/get-tracks?playlist_id=${playlistId}`);
        setTracks(response.data);
        setError(null);
      } catch (err) {
        console.error("Error fetching tracks:", err);
        setError("Failed to load tracks. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    if (playlistId) {
      fetchTracks();
    }
  }, [playlistId]);

  const generateCover = async () => {
    try {
      setGenerating(true);
      setError(null);
      const response = await axios.get(`/api/generate-cover?playlist_id=${playlistId}&userId=${userId}`);
      setCoverUrl(response.data.image_url);
    } catch (err) {
      console.error("Error generating cover:", err);
      setError("Failed to generate cover. Please try again.");
    } finally {
      setGenerating(false);
    }
  };

  const setCoverOnSpotify = async () => {
    if (!coverUrl) return;
    try {
      setSettingCover(true);
      setError(null);
      await axios.put(
        `/api/set-cover?playlist_id=${playlistId}&userId=${userId}`,
        { image_url: coverUrl }
      );
      setCoverSet(true);
    } catch (err) {
      console.error("Error setting cover:", err);
      setError("Failed to set cover on Spotify. Please try again.");
    } finally {
      setSettingCover(false);
    }
  };

  const generateDescription = async () => {
    try {
      setGeneratingDescription(true);
      setError(null);
      const response = await axios.get(`/api/generate-description?playlist_id=${playlistId}&userId=${userId}`);
      setDescription(response.data.description);
    } catch (err) {
      console.error("Error generating description:", err);
      setError("Failed to generate description. Please try again.");
    } finally {
      setGeneratingDescription(false);
    }
  };

  if (loading) {
    return <Spinner />;
  }

  if (error && !tracks.length) {
    return (
      <div className={styles.container}>
        <p style={{ color: "red" }}>{error}</p>
        <Link to="/">
          <button>Back to Playlists</button>
        </Link>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <Link to="/">
        <button className={styles.backButton}>← Back to Playlists</button>
      </Link>

      {/* <h1>Generate</h1> */}

      <div className={styles.tracksSection}>
        <h2>Tracks in Playlist ({tracks.length})</h2>
        <ul className={styles.trackList}>
          {tracks.slice(0, 10).map((item, index) => (
            <li key={index}>
              <strong>{item.item.name}</strong> by{" "}
              {item.item.artists.map((a) => a.name).join(", ")}
            </li>
          ))}
        </ul>
        {tracks.length > 10 && <p>...and {tracks.length - 10} more tracks</p>}
      </div>

      <button
        onClick={generateCover}
        disabled={generating || tracks.length === 0}
        className={styles.generateButton}
      >
        {generating ? "Generating..." : "Generate AI Cover Image"}
      </button>

      <button
        onClick={generateDescription}
        disabled={generatingDescription || tracks.length === 0}
        className={styles.generateButton}
      >
        {generatingDescription ? "Generating..." : "Generate AI Description"}
      </button>

      {generating && (
        <div className={styles.generatingSection}>
          <Spinner />
          <p>Creating your unique cover image...</p>
        </div>
      )}

      {generatingDescription && (
        <div className={styles.generatingSection}>
          <Spinner />
          <p>Creating your playlist description...</p>
        </div>
      )}

      {error && coverUrl === null && description === null && (
        <p style={{ color: "red", marginTop: "1rem" }}>{error}</p>
      )}

      {coverUrl && (
        <div className={styles.coverSection}>
          <h2>Generated Cover</h2>
          <img src={coverUrl} alt="Generated playlist cover" className={styles.coverImage} />
          <button
            onClick={setCoverOnSpotify}
            disabled={settingCover || coverSet}
            className={styles.generateButton}
          >
            {settingCover ? "Setting..." : coverSet ? "Cover Set on Spotify ✓" : "Set as Spotify Cover"}
          </button>
        </div>
      )}
      
      {description && (
        <div className={styles.coverSection}>
          <h2>Generated Description</h2>
          <p className={styles.description}>{description}</p>
        </div>
      )}
    </div>
  );
};
