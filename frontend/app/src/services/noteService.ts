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
  private encryptedContentCache = new Map<UUID, string>();

  constructor(cryptoService: CryptoService) {
    this.cryptoService = cryptoService;
  }

  async fetchNote(noteId: UUID): Promise<TimerSelectionType> {
    const { encrypted_content, destroy_after_read, timing_for_destroy } =
      await apiClient.get<GetEncryptedNote>(API_ENDPOINTS.NOTES + `/${noteId}`);
    this.encryptedContentCache.set(noteId, encrypted_content);
    return destroy_after_read ? TimerSelection.Momentum : (timing_for_destroy ?? TimerSelection.Momentum);
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
    const cached = this.encryptedContentCache.get(noteId);
    if (!cached) throw new Error("Note not fetched");
    this.encryptedContentCache.delete(noteId);
    return this.cryptoService.decryptNote(cached, password);
  }

  async deleteNote(noteId: UUID): Promise<void> {
    await apiClient.delete(API_ENDPOINTS.NOTES + `/${noteId}`);
    logger.info("Note deleted");
  }
}

export const buildNoteService = (): NoteService => {
  const cryptoService = buildCryptoService();
  const noteService = new NoteService(cryptoService);
  return noteService;
};
