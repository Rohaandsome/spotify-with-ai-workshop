import { Link, useLocation } from "react-router-dom";
import styles from "./Navbar.module.css";

export const Navbar = () => {
  const location = useLocation();

  return (
    <nav className={styles.navbar}>
      <Link to="/" className={styles.logo}>
        <h1>🎵 Spotify AI Workshop</h1>
      </Link>
      
      <div className={styles.navLinks}>
        <Link 
          to="/" 
          className={`${styles.navLink} ${location.pathname === "/" ? styles.active : ""}`}
        >
          Playlists
        </Link>
        <Link 
          to="/gallery" 
          className={`${styles.navLink} ${location.pathname === "/gallery" ? styles.active : ""}`}
        >
          Gallery
        </Link>
        <Link 
          to="/top" 
          className={`${styles.navLink} ${location.pathname === "/top" ? styles.active : ""}`}
        >
          Top
        </Link>
      </div>
    </nav>
  );
};
