import { useParams } from "react-router-dom";

function NoteView() {
  const { note_id } = useParams();

  return <div>Note View: {note_id}</div>;
}

export default NoteView;
