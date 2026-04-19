import { useState } from "react";

import styles from "./NoteLinkModal.module.css";
import BaseModal from "@/components/base/BaseModal/BaseModal";
import BaseButton from "@/components/base/BaseButton/BaseButton";

import type { UUID } from "@/types";

interface NoteLinkModalProps {
  noteId: UUID;
  onClose: () => void;
}

function NoteLinkModal({ noteId, onClose }: NoteLinkModalProps) {
  const [copied, setCopied] = useState(false);

  const noteUrl = `${window.location.origin}/note/${noteId}`;

  const handleCopy = () => {
    navigator.clipboard.writeText(noteUrl).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <BaseModal onClose={onClose}>
      <h2 className={styles.title}>Note created</h2>
      <p className={styles.description}>
        Share this link with the recipient. The note will be destroyed according to the selected timer.
      </p>

      <div className={styles.linkRow}>
        <span className={styles.link}>{noteUrl}</span>
      </div>

      <div className={styles.actions}>
        <BaseButton
          label="Close"
          className={styles.closeButton}
          onClick={onClose}
        />
        <BaseButton
          label={copied ? "Copied!" : "Copy"}
          className={copied ? styles.copyButtonCopied : styles.copyButton}
          onClick={handleCopy}
        />
      </div>
    </BaseModal>
  );
}

export default NoteLinkModal;
