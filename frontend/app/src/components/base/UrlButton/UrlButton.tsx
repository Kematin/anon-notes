import { Link } from "react-router-dom";

import styles from "./UrlButton.module.css";

interface UrlButtonProps {
  label: string;
  to: string;
  className?: string;
}

function UrlButton({ label, to, className = styles.urlButton }: UrlButtonProps) {
  return (
    <Link
      to={to}
      className={className}
    >
      {label}
    </Link>
  );
}

export default UrlButton;
