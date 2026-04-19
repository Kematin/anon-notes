import styles from "./ActionButton.module.css";

import BaseButton from "../base/BaseButton/BaseButton";

interface ActionButtonProps {
  label: string;
  action: () => void;
  disabled?: boolean;
}

function ActionButton({ label, action, disabled }: ActionButtonProps) {
  return (
    <BaseButton
      label={label}
      onClick={action}
      className={styles.actionButton}
      disabled={disabled}
    />
  );
}

export default ActionButton;
