const TimerSelection = {
  Momentum: 0,
  Minute: 1,
  Hour: 60,
  Day: 60 * 24,
  Week: 60 * 24 * 7,
};

export const TimerSelectionOptions: {
  value: string;
  timer: TimerSelection;
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

export type TimerSelection = (typeof TimerSelection)[keyof typeof TimerSelection];
