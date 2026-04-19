import { apiClient } from "@/services";
import { API_ENDPOINTS } from "@/config/api";
import { CryptoService, buildCryptoService } from "./cryptoService";

import type { UUID } from "@/types";
import type { PostCreateNote, GetEncryptedNote, PostCreatedNoteId } from "@/types/note";
import type { TimerSelectionType } from "@/constants/timerSelection";

import { TimerSelection } from "@/constants/timerSelection";
import { logger } from "@/utils/logger";

class NoteService {
  private cryptoService: CryptoService;

  constructor(cryptoService: CryptoService) {
    this.cryptoService = cryptoService;
  }

  private async getEncryptedNote(noteId: UUID): Promise<GetEncryptedNote> {
    const encryptedNote = await apiClient.get<GetEncryptedNote>(API_ENDPOINTS.NOTES + `/${noteId}`);
    return encryptedNote;
  }

  async createNote(note: string, selectedTimer: TimerSelectionType, password: string): Promise<UUID> {
    const encryptedNote = await this.cryptoService.encryptNote(note, password);

    const isMomentum = selectedTimer === TimerSelection.Momentum;
    const noteCreateData: PostCreateNote = isMomentum
      ? { encrypted_content: encryptedNote, destroy_after_read: true }
      : { encrypted_content: encryptedNote, timing_for_destroy: selectedTimer };

    const { created_id } = await apiClient.post<PostCreatedNoteId>(API_ENDPOINTS.NOTES, noteCreateData);
    logger.info("Send note to server");
    return created_id;
  }

  async decryptNote(noteId: UUID, password: string): Promise<string> {
    const encryptedNote = await this.getEncryptedNote(noteId);
    const note = await this.cryptoService.decryptNote(encryptedNote.encrypted_content, password);
    return note;
  }
}

export const buildNoteService = (): NoteService => {
  const cryptoService = buildCryptoService();
  const noteService = new NoteService(cryptoService);
  return noteService;
};
