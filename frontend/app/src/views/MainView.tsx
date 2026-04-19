import "@/assets/styles/MainView.css";

import cat from "@/assets/images/cat.png";
import gramophone from "@/assets/images/gramophone.png";

import NoteTextField from "../components/NoteTextField/NoteTextField";
import TimerSelect from "../components/TimerSelect/TimerSelect";
import ActionButton from "../components/ActionButton/ActionButton";
import Image from "../components/Image/Image";
import PasswordModal from "../components/PasswordModal/PasswordModal";
import NoteLinkModal from "../components/NoteLinkModal/NoteLinkModal";

import { TimerSelection } from "@/constants/timerSelection";
import { buildNoteService } from "@/services/noteService";

import type { UUID } from "@/types";
import { useState } from "react";

function MainView() {
  const noteService = buildNoteService();

  const [noteText, setNoteText] = useState("");
  const [selectedTimer, setSelectedTimer] = useState(TimerSelection.Momentum);
  const [isPasswordModalOpen, setIsPasswordModalOpen] = useState(false);
  const [createdNoteId, setCreatedNoteId] = useState<UUID | null>(null);

  const handleSendClick = () => {
    setIsPasswordModalOpen(true);
  };

  const handleConfirm = async (password: string) => {
    setIsPasswordModalOpen(false);
    const noteId = await noteService.createNote(noteText, selectedTimer, password);
    setCreatedNoteId(noteId);
  };

  const handleLinkModalClose = () => {
    setCreatedNoteId(null);
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
          <NoteTextField
            value={noteText}
            onChange={setNoteText}
            onSubmit={noteText.length > 0 ? handleSendClick : undefined}
          />
        </div>
        <div className="note-options">
          <TimerSelect onChange={setSelectedTimer} />
          <ActionButton
            label="Send"
            action={handleSendClick}
            disabled={noteText.length === 0}
          />
        </div>
      </div>

      {isPasswordModalOpen && (
        <PasswordModal
          description="The note will be encrypted with this password. The recipient will need it to read the note."
          onConfirm={handleConfirm}
          onCancel={() => setIsPasswordModalOpen(false)}
        />
      )}

      {createdNoteId && (
        <NoteLinkModal
          noteId={createdNoteId}
          onClose={handleLinkModalClose}
        />
      )}
    </section>
  );
}

export default MainView;
