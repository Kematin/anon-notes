import styles from "./Image.module.css";

interface AbsoluteImageProps {
  src: string;
  alt?: string;
  wrapperStyles?: string;
}

function Image({ src, alt = "Image", wrapperStyles = styles.wrapper }: AbsoluteImageProps) {
  return (
    <div className={wrapperStyles}>
      <img
        src={src}
        alt={alt}
        className={styles.image}
      />
    </div>
  );
}

export default Image;
