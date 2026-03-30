import { router } from "./router/index.ts";
import { RouterProvider } from "react-router-dom";

import "./assets/styles/App.css";

function App() {
  return (
    <div id="app">
      <div className="app-bg"></div>
      <RouterProvider router={router} />
    </div>
  );
}

export default App;
