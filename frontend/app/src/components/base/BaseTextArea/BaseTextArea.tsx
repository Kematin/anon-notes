import styles from "./BaseTextArea.module.css";

interface TextAreaProps {
  name: string;
  id: string;
  placeholder?: string;
  value?: string;
  rows?: number;
  disabled?: boolean;
  className?: string;
  onChange?: (value: string) => void;
  onKeyDown?: (e: React.KeyboardEvent<HTMLTextAreaElement>) => void;
}

function BaseTextArea({
  name,
  id,
  placeholder = "...",
  value,
  onChange,
  onKeyDown,
  rows = 4,
  disabled,
  className = styles.textArea,
}: TextAreaProps) {
  return (
    <textarea
      name={name}
      className={className}
      id={id}
      placeholder={placeholder}
      value={value}
      onChange={(e) => onChange?.(e.target.value)}
      onKeyDown={onKeyDown}
      rows={rows}
      disabled={disabled}
    />
  );
}

export default BaseTextArea;
