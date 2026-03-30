import { createBrowserRouter } from "react-router-dom";

export const router = createBrowserRouter([
  {
    path: "/",
    lazy: async () => {
      const { default: Component } = await import("@/views/MainView");
      return { Component };
    },
  },
  {
    path: "/note/:note_id",
    lazy: async () => {
      const { default: Component } = await import("@/views/NoteView");
      return { Component };
    },
  },
]);
