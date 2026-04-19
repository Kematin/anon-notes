import type { UUID } from "./common";
import type { TimerSelectionType } from "@/constants/timerSelection";

export interface PostCreateNote {
  encrypted_content: string;
  destroy_after_read?: boolean;
  timing_for_destroy?: TimerSelectionType;
}

export interface GetEncryptedNote {
  id: UUID;
  encrypted_content: string;
}

export interface PostCreatedNoteId {
  created_id: UUID;
}
