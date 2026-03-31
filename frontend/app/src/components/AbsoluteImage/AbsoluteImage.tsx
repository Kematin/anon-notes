import styles from "./AbsoluteImage.module.css";

interface AbsoluteImageProps {
  src: string;
  alt?: string;
  top?: number;
  left?: number;
  width?: number;
  height?: number;
}

function AbsoluteImage({ src, alt = "Image", top, left, width, height }: AbsoluteImageProps) {
  return (
    <div
      className={styles.wrapper}
      style={{ top, left, width, height }}
    >
      <img
        src={src}
        alt={alt}
        className={styles.image}
      />
    </div>
  );
}

export default AbsoluteImage;
