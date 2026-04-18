export const TimerSelection = {
  Momentum: "momentum",
  Minute: "minute",
  Hour: "hour",
  Day: "day",
  Week: "week",
};

export const TimerSelectionOptions: {
  value: string;
  timer: TimerSelectionType;
  name: string;
}[] = [
  {
    value: "momentum",
    timer: TimerSelection.Momentum,
    name: "Destroy after read",
  },
  {
    value: "minute",
    timer: TimerSelection.Minute,
    name: "Destroy after 1 minute",
  },
  {
    value: "hour",
    timer: TimerSelection.Hour,
    name: "Destroy after 1 hour",
  },
  {
    value: "day",
    timer: TimerSelection.Day,
    name: "Destroy after 1 day",
  },
  {
    value: "week",
    timer: TimerSelection.Week,
    name: "Destroy after 1 week",
  },
];

export type TimerSelectionType = (typeof TimerSelection)[keyof typeof TimerSelection];
