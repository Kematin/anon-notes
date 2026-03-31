import BaseTextArea from "../base/BaseTextArea/BaseTextArea";

function NoteTextField() {
  return (
    <BaseTextArea
      id="note"
      name="note"
      rows={8}
    />
  );
}

export default NoteTextField;
