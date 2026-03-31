import "@/assets/styles/MainView.css";

import cat from "@/assets/images/cat.png";
import gramophone from "@/assets/images/gramophone.png";

import { useMemo } from "react";

import NoteTextField from "../components/NoteTextField/NoteTextField";
import TimerSelect from "../components/TimerSelect/TimerSelect";
import ActionButton from "../components/ActionButton/ActionButton";
import AbsoluteImage from "../components/AbsoluteImage/AbsoluteImage";

import type { ImageCoordinates } from "@/types/imageCoord";
import { calculateCatImage, calculateGramophoneImage } from "@/utils/calculateNoteImages";

function MainView() {
  const createNote = () => {
    console.log("send note");
  };

  const catCoord = useMemo<ImageCoordinates>(() => calculateCatImage(), []);
  const gramophoneCoord = useMemo<ImageCoordinates>(() => calculateGramophoneImage(), []);

  return (
    <section id="main">
      <AbsoluteImage
        src={cat}
        width={426}
        height={689}
        top={catCoord.top}
        left={catCoord.left}
      />
      <AbsoluteImage
        src={gramophone}
        width={300}
        height={300}
        top={gramophoneCoord.top}
        left={gramophoneCoord.left}
      />
      <div className="writer-content">
        <NoteTextField />
        <div className="note-options">
          <TimerSelect />
          <ActionButton
            label="Send"
            action={createNote}
          />
        </div>
      </div>
    </section>
  );
}

export default MainView;
