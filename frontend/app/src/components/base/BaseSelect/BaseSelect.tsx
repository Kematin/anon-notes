export interface SelectOption {
  value: string;
  label: string;
}

interface BaseSelectProps {
  options: SelectOption[];
  name?: string;
  onChange?: (value: string) => void;
}

function BaseSelect({ options, name = "select", onChange }: BaseSelectProps) {
  return (
    <select
      name={name}
      onChange={(e) => onChange?.(e.target.value)}
    >
      {options.map((option) => (
        <option
          key={option.value}
          value={option.value}
        >
          {option.label}
        </option>
      ))}
    </select>
  );
}

export default BaseSelect;
