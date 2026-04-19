import "@/assets/styles/MainView.css";
import styles from "./Undefined.module.css";

import UrlButton from "@/components/base/UrlButton/UrlButton";

function Undefined() {
  return (
    <section id="main">
      <div className={styles.content}>
        <p className={styles.code}>404</p>
        <p className={styles.message}>Page not found.</p>
        <UrlButton
          label="Go to main page"
          to="/"
        />
      </div>
    </section>
  );
}

export default Undefined;
