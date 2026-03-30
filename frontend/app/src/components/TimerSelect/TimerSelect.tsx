import BaseSelect from "../base/BaseSelect/BaseSelect";
import type { SelectOption } from "../base/BaseSelect/BaseSelect";
import { TimerSelectionOptions } from "@/constants/timerSelection";

function TimerSelect() {
  const options: SelectOption[] = TimerSelectionOptions.map((option) => ({
    value: option.value,
    label: option.name,
  }));
  return <BaseSelect options={options} />;
}

export default TimerSelect;
