import type { ReactNode } from "react";

interface BaseButtonProps {
  label: string;
  className: string;
  onClick?: () => void;
  disabled?: boolean;
  innerComponent?: ReactNode;
}

function BaseButton({ label, className, onClick, disabled, innerComponent }: BaseButtonProps) {
  return (
    <button
      className={className}
      onClick={onClick}
      disabled={disabled}
    >
      {innerComponent}
      <span>{label}</span>
    </button>
  );
}

export default BaseButton;
