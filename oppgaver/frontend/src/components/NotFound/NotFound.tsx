import styles from "./NotFound.module.css";

export function NotFound(props: { text: string }) {
    return (
        <div className={styles.notFoundContainer}>
            <img
                src="/sad_cover.jpg"
                alt="Sad Cover"
                className={styles.notFoundImage}
            />
            <p className={styles.notFoundText}>{props.text}</p>
        </div>
    );
}