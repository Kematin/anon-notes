import styles from "./NoteStatusMessage.module.css";
import UrlButton from "@/components/base/UrlButton/UrlButton";

interface NoteStatusMessageProps {
  message: string;
}

function NoteStatusMessage({ message }: NoteStatusMessageProps) {
  return (
    <>
      <p className={styles.message}>{message}</p>
      <div className={styles.actions}>
        <UrlButton
          label="Go to main page"
          to="/"
        />
      </div>
    </>
  );
}

export default NoteStatusMessage;
