import "@/assets/styles/MainView.css";

import cat from "@/assets/images/cat.png";
import gramophone from "@/assets/images/gramophone.png";

import NoteTextFieldProps from "../components/NoteTextField/NoteTextField";
import TimerSelect from "../components/TimerSelect/TimerSelect";
import ActionButton from "../components/ActionButton/ActionButton";
import Image from "../components/Image/Image";
import PasswordModal from "../components/PasswordModal/PasswordModal";

import { TimerSelection } from "@/constants/timerSelection";
import { buildNoteService } from "@/services/noteService";

import { useState } from "react";

function MainView() {
  const noteService = buildNoteService();

  const [noteText, setNoteText] = useState("");
  const [selectedTimer, setSelectedTimer] = useState(TimerSelection.Momentum);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleSendClick = () => {
    setIsModalOpen(true);
  };

  const handleConfirm = (password: string) => {
    setIsModalOpen(false);
    noteService.createNote(noteText, selectedTimer, password);
  };

  const handleCancel = () => {
    setIsModalOpen(false);
  };

  return (
    <section id="main">
      <div className="writer-content">
        <Image
          src={cat}
          wrapperStyles="cat-image-wrapper"
        />
        <Image
          src={gramophone}
          wrapperStyles="gramophone-image-wrapper"
        />
        <div className="note-container">
          <NoteTextFieldProps
            value={noteText}
            onChange={setNoteText}
          />
        </div>
        <div className="note-options">
          <TimerSelect onChange={setSelectedTimer} />
          <ActionButton
            label="Send"
            action={handleSendClick}
          />
        </div>
      </div>

      {isModalOpen && (
        <PasswordModal
          description="The note will be encrypted with this password. The recipient will need it to read the note."
          onConfirm={handleConfirm}
          onCancel={handleCancel}
        />
      )}
    </section>
  );
}

export default MainView;
