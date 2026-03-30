import styles from "./ActionButton.module.css";

import BaseButton from "../base/BaseButton/BaseButton";

interface ActionButtonProps {
  label: string;
  action: () => void;
}

function ActionButton({ label, action }: ActionButtonProps) {
  return (
    <BaseButton
      label={label}
      onClick={action}
      className={styles.actionButton}
    />
  );
}

export default ActionButton;
