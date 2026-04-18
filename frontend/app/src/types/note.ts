import type { UUID } from "./common";
import type { TimerSelectionType } from "@/constants/timerSelection";

export interface NoteCreate {
  encrypted_content: string;
  destroy_after_read?: boolean;
  timing_for_destroy?: TimerSelectionType;
}

export interface EncryptedNote {
  id: UUID;
  encrypted_content: string;
}
