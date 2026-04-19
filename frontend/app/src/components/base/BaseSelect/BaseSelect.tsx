import styles from "./BaseSelect.module.css";

import { useState } from "react";

export interface SelectStyles {
  select?: string;
  active?: string;
  title?: string;
  content?: string;
  label?: string;
  checked?: string;
}
export interface SelectOption {
  value: string;
  label: string;
}

interface BaseSelectProps {
  options: SelectOption[];
  customStyles?: SelectStyles;
  onChange?: (value: string) => void;
}

function BaseSelect({ options, customStyles, onChange }: BaseSelectProps) {
  const selectStyles: SelectStyles = {
    select: customStyles?.select ? customStyles.select : styles.select,
    active: customStyles?.active ? customStyles.active : styles.active,
    title: customStyles?.title ? customStyles.title : styles.title,
    content: customStyles?.content ? customStyles.content : styles.content,
    label: customStyles?.label ? customStyles.label : styles.label,
    checked: customStyles?.checked ? customStyles.checked : styles.checked,
  };

  const [isOpen, setIsOpen] = useState(false);
  const [selected, setSelected] = useState<SelectOption>(options[0]);

  const handleSelect = (option: SelectOption) => {
    setSelected(option);
    onChange?.(option.value);
    setIsOpen(false);
  };

  return (
    <div className={`${selectStyles.select} ${isOpen ? selectStyles.active : ""}`}>
      <div
        className={selectStyles.title}
        onClick={() => setIsOpen((v) => !v)}
      >
        {selected.label}
      </div>
      <div className={selectStyles.content}>
        {options.map((option) => (
          <div
            key={option.value}
            className={`${selectStyles.label} ${selected.value === option.value ? selectStyles.checked : ""}`}
            onClick={() => handleSelect(option)}
          >
            {option.label}
          </div>
        ))}
      </div>
    </div>
  );
}

export default BaseSelect;
