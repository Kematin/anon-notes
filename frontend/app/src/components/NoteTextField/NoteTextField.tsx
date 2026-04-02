import BaseTextArea from "../base/BaseTextArea/BaseTextArea";

function NoteTextField() {
  return (
    <BaseTextArea
      id="note"
      name="note"
      rows={10}
    />
  );
}

export default NoteTextField;
