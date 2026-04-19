import styles from "./BaseInput.module.css";

interface BaseInputProps {
  name: string;
  id: string;
  type?: "text" | "password" | "email";
  placeholder?: string;
  value?: string;
  disabled?: boolean;
  className?: string;
  autoFocus?: boolean;
  onChange?: (value: string) => void;
}

function BaseInput({
  name,
  id,
  type = "text",
  placeholder = "...",
  value,
  onChange,
  disabled,
  className = styles.input,
  autoFocus,
}: BaseInputProps) {
  return (
    <input
      name={name}
      id={id}
      type={type}
      className={className}
      placeholder={placeholder}
      value={value}
      onChange={(e) => onChange?.(e.target.value)}
      disabled={disabled}
      autoFocus={autoFocus}
    />
  );
}

export default BaseInput;
