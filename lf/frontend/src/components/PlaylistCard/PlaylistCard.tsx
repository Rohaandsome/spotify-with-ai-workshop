import { Playlist } from "../../model/Playlist";
import styles from "./PlaylistCard.module.css";
import { Link } from "react-router-dom";

interface PlaylistCardProps {
  playlist: Playlist;
}

export const PlaylistCard = ({ playlist }: PlaylistCardProps) => {
  return (
    <div className={styles.card}>
      <h3>{playlist.name}</h3>
      <Link to={`/cover/${playlist.id}`}>
        <button>Info</button>
      </Link>
    </div>
  );
};
