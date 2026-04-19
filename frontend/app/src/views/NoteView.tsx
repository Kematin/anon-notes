import "@/assets/styles/MainView.css";
import styles from "./NoteView.module.css";

import { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";

import NoteTextField from "@/components/NoteTextField/NoteTextField";
import PasswordModal from "@/components/PasswordModal/PasswordModal";
import UrlButton from "@/components/base/UrlButton/UrlButton";
import NoteStatusMessage from "@/components/NoteStatusMessage/NoteStatusMessage";

import { buildNoteService } from "@/services/noteService";
import { TimerDestroyLabel } from "@/constants/timerSelection";

import type { UUID } from "@/types";
import type { TimerSelectionType } from "@/constants/timerSelection";

type NoteState =
  | { status: "loading" }
  | { status: "awaiting_password"; timer: TimerSelectionType }
  | { status: "decrypted"; content: string; timer: TimerSelectionType }
  | { status: "invalid_password" }
  | { status: "not_found" }
  | { status: "error" };

function NoteView() {
  const { note_id } = useParams<{ note_id: UUID }>();
  const noteService = useMemo(() => buildNoteService(), []);

  const [noteState, setNoteState] = useState<NoteState>({ status: "loading" });

  useEffect(() => {
    noteService
      .fetchNote(note_id!)
      .then((timer) => setNoteState({ status: "awaiting_password", timer }))
      .catch((err: unknown) => {
        const status = err instanceof Error && "status" in err ? (err as { status: number }).status : null;
        setNoteState(status === 404 ? { status: "not_found" } : { status: "error" });
      });
  }, [note_id, noteService]);

  const handlePasswordConfirm = async (password: string) => {
    if (noteState.status !== "awaiting_password") return;
    try {
      const content = await noteService.decryptNote(note_id!, password);
      setNoteState({ status: "decrypted", content, timer: noteState.timer });
      await noteService.deleteNote(note_id!);
    } catch {
      setNoteState({ status: "invalid_password" });
    }
  };

  return (
    <section id="main">
      <div className="writer-content">
        {noteState.status === "loading" && <p className={styles.message}>Loading...</p>}

        {noteState.status === "not_found" && (
          <NoteStatusMessage message="Note not found or already destroyed." />
        )}

        {noteState.status === "error" && (
          <NoteStatusMessage message="Something went wrong. Please try again." />
        )}

        {noteState.status === "invalid_password" && <NoteStatusMessage message="Invalid password." />}

        {noteState.status === "decrypted" && (
          <>
            <p className={styles.disappearHint}>
              This note will disappear <span>{TimerDestroyLabel[noteState.timer]}</span>
            </p>
            <div className="note-container">
              <NoteTextField
                value={noteState.content}
                disabled
              />
            </div>
            <div className={styles.actions}>
              <UrlButton
                label="Create secret note"
                to="/"
              />
            </div>
          </>
        )}
      </div>

      {noteState.status === "awaiting_password" && (
        <PasswordModal
          description="Enter the password to decrypt and read the note."
          onConfirm={handlePasswordConfirm}
          onCancel={() => setNoteState({ status: "not_found" })}
        />
      )}
    </section>
  );
}

export default NoteView;
