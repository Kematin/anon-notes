import BaseSelect from "../base/BaseSelect/BaseSelect";
import type { SelectOption } from "../base/BaseSelect/BaseSelect";
import { TimerSelectionOptions } from "@/constants/timerSelection";

interface TimerSelectProps {
  onChange: (value: string) => void;
}

function TimerSelect({ onChange }: TimerSelectProps) {
  const options: SelectOption[] = TimerSelectionOptions.map((option) => ({
    value: option.value,
    label: option.name,
  }));
  return (
    <BaseSelect
      options={options}
      onChange={onChange}
    />
  );
}

export default TimerSelect;
