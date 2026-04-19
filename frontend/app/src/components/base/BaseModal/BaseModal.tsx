import type { ReactNode } from "react";
import { createPortal } from "react-dom";

import styles from "./BaseModal.module.css";

interface BaseModalProps {
  children: ReactNode;
  onClose: () => void;
}

function BaseModal({ children, onClose }: BaseModalProps) {
  const handleOverlayClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget) onClose();
  };

  return createPortal(
    <div
      className={styles.overlay}
      onClick={handleOverlayClick}
    >
      <div className={styles.modal}>{children}</div>
    </div>,
    document.body,
  );
}

export default BaseModal;
