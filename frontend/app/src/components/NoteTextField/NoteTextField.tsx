import BaseTextArea from "../base/BaseTextArea/BaseTextArea";

interface NoteTextFieldProps {
  value: string;
  onChange?: (value: string) => void;
  onSubmit?: () => void;
  disabled?: boolean;
}

function NoteTextField({ value, onChange, onSubmit, disabled }: NoteTextFieldProps) {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      onSubmit?.();
    }
  };

  return (
    <BaseTextArea
      id="note"
      name="note"
      value={value}
      onChange={onChange}
      onKeyDown={handleKeyDown}
      disabled={disabled}
      rows={10}
    />
  );
}

export default NoteTextField;
