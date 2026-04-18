import BaseTextArea from "../base/BaseTextArea/BaseTextArea";

interface NoteTextFieldProps {
  value: string;
  onChange: (value: string) => void;
}

function NoteTextFieldProps({ value, onChange }: NoteTextFieldProps) {
  return (
    <BaseTextArea
      id="note"
      name="note"
      value={value}
      onChange={onChange}
      rows={10}
    />
  );
}

export default NoteTextFieldProps;
