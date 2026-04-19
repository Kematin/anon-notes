import { useState, useEffect } from "react";

import styles from "./PasswordModal.module.css";
import BaseModal from "@/components/base/BaseModal/BaseModal";
import BaseInput from "@/components/base/BaseInput/BaseInput";
import BaseButton from "@/components/base/BaseButton/BaseButton";

interface PasswordModalProps {
  description: string;
  onConfirm: (password: string) => void;
  onCancel: () => void;
}

function PasswordModal({ description, onConfirm, onCancel }: PasswordModalProps) {
  const [password, setPassword] = useState("");

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") onCancel();
      if (e.key === "Enter" && password.length > 0) onConfirm(password);
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [password, onConfirm, onCancel]);

  return (
    <BaseModal onClose={onCancel}>
      <h2 className={styles.title}>Enter password</h2>
      <p className={styles.description}>{description}</p>

      <div className={styles.inputWrapper}>
        <label
          htmlFor="note-password"
          className={styles.label}
        >
          Password
        </label>
        <BaseInput
          name="password"
          id="note-password"
          type="password"
          placeholder="Your password..."
          value={password}
          onChange={setPassword}
          autoFocus
        />
      </div>

      <div className={styles.actions}>
        <BaseButton
          label="Cancel"
          className={styles.cancelButton}
          onClick={onCancel}
        />
        <BaseButton
          label="Encrypt & Send"
          className={styles.confirmButton}
          onClick={() => onConfirm(password)}
          disabled={password.length === 0}
        />
      </div>
    </BaseModal>
  );
}

export default PasswordModal;
