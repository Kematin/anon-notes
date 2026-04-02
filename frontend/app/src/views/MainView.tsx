import "@/assets/styles/MainView.css";

import cat from "@/assets/images/cat.png";
import gramophone from "@/assets/images/gramophone.png";

import NoteTextField from "../components/NoteTextField/NoteTextField";
import TimerSelect from "../components/TimerSelect/TimerSelect";
import ActionButton from "../components/ActionButton/ActionButton";
import Image from "../components/Image/Image";

function MainView() {
  const createNote = () => {
    console.log("send note");
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
          <NoteTextField />
        </div>
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
