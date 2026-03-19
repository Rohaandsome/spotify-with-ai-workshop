import { useEffect, useState } from "react";
import { useUserId } from "../hooks/useUserId.ts";
import styles from "./CoverImageListPage.module.css";
import { NotFound } from "../components/NotFound/NotFound";
import { Spinner } from "../components/Spinner/Spinner";

interface CoverImage {
    id: string;
    playlistId: string;
    imageUrl: string;
    playlistName: string;
    createdAt: string;
}

export function CoverImageListPage() {
    const [coverImages, setCoverImages] = useState<CoverImage[]>([]);
    const [loading, setLoading] = useState(true);
    const userId = useUserId();

    useEffect(() => {
        const fetchCoverImages = async () => {
            try {
                setLoading(true);
                const response = await fetch(
                    "/api/cover-images?userId=" + userId
                );

                if (!response.ok) {
                    const errorJson = await response.json();
                    console.error(
                        "fetchCoverImages failed\n",
                        "Status code: " + response.status + "\n",
                        "Error message: " + errorJson.error + "\n"
                    );
                    return;
                }

                const data = await response.json();
                console.log("Fetched cover images:", data);
                setCoverImages(data);
            } catch (error) {
                console.error("Error fetching cover images:", error);
            } finally {
                setLoading(false);
            }
        };
        
        fetchCoverImages();
    }, [userId]);

    const formatDate = (dateString: string) => {
        if (!dateString) return "";
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'short', 
            day: 'numeric' 
        });
    };

    if (loading) {
        return <Spinner />;
    }

    if (!coverImages || coverImages.length === 0) {
        return (
            <div className={styles.container}>
                <NotFound text={"You haven't generated any cover images yet"} />
                <p style={{ textAlign: 'center', color: '#b3b3b3', marginTop: '1rem' }}>
                    Go to <a href="/" style={{ color: '#1db954' }}>Playlists</a> to generate your first cover!
                </p>
            </div>
        );
    }

    return (
        <div className={styles.container}>
            <h1 className={styles.title}>Generated Cover Images</h1>
            <p className={styles.subtitle}>Your AI-generated playlist covers</p>
            
            <div className={styles.grid}>
                {coverImages.map((coverImage) => (
                    <div
                        key={coverImage.id}
                        className={styles.coverImageCard}
                    >
                        <img
                            className={styles.coverImage}
                            src={coverImage.imageUrl}
                            alt={`Cover for ${coverImage.playlistName}`}
                            onError={(e) => {
                                console.error("Failed to load image:", coverImage.imageUrl);
                                e.currentTarget.src = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Crect fill='%23333' width='400' height='400'/%3E%3Ctext fill='%23fff' font-family='Arial' font-size='20' x='50%25' y='50%25' text-anchor='middle' dominant-baseline='middle'%3EImage Failed to Load%3C/text%3E%3C/svg%3E";
                            }}
                        />
                        <div>
                            <p className={styles.playlistName}>
                                {coverImage.playlistName}
                            </p>
                            {coverImage.createdAt && (
                                <p className={styles.createdAt}>
                                    {formatDate(coverImage.createdAt)}
                                </p>
                            )}
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}