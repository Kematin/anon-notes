import "@/assets/styles/MainView.css";

import NoteTextField from "../components/NoteTextField/NoteTextField";
import TimerSelect from "../components/TimerSelect/TimerSelect";
import ActionButton from "../components/ActionButton/ActionButton";
import Image from "../components/Image/Image";

function MainView() {
  return (
    <section id="main">
      <Image />
      <Image />
      <div className="writer-content">
        <NoteTextField />
        <div className="note-options">
          <TimerSelect />
          <ActionButton />
        </div>
      </div>
    </section>
  );
}

export default MainView;
