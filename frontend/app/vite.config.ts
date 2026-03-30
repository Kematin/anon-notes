import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { fileURLToPath, URL } from "node:url";
import type { Connect } from "vite";
import { defineConfig, loadEnv } from "vite";

function createLogHandler(): Connect.NextHandleFunction {
  return function logHandler(req, res, next) {
    if (req.url === "/log" && req.method === "POST") {
      let body = "";
      req.on("data", (chunk) => {
        body += chunk.toString();
      });
      req.on("end", () => {
        try {
          const logData = JSON.parse(body);
          switch (logData.type) {
            case "log":
              console.log("[BROWSER]:", ...logData.message);
              break;
            case "warn":
              console.warn("[BROWSER]:", ...logData.message);
              break;
            case "error":
              console.error("[BROWSER]:", ...logData.message);
              break;
          }
          res.statusCode = 200;
          res.setHeader("Content-Type", "application/json");
          res.end(JSON.stringify({ status: "ok" }));
        } catch (e) {
          console.error("Error processing log:", e);
          res.statusCode = 500;
          res.setHeader("Content-Type", "application/json");
          res.end(JSON.stringify({ error: "Failed to process log" }));
        }
      });
    } else {
      next();
    }
  };
}

const envDir = fileURLToPath(new URL("../", import.meta.url));
const projectRoot = fileURLToPath(new URL("./", import.meta.url));

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, envDir, "");
  const allowedHost = env.API_HOST;
  const devMode = env.VITE_DEV_MODE === "true" ? true : false;

  console.log("envDir: ", envDir);
  console.log("projectRoot: ", projectRoot);
  console.log("DevMode: ", devMode);
  console.log("Allowed host: ", allowedHost);

  return {
    envDir: envDir,
    plugins: [react(), tailwindcss()],
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
    },
    assetsInclude: ["**/*.html"],
    server: {
      host: "0.0.0.0",
      port: 5173,
      strictPort: true,
      cors: true,
      proxy: {
        "/media": {
          target: "http://localhost:80",
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/media/, "/media"),
          configure: (proxy) => {
            proxy.on("proxyReq", (_proxyReq, req) => {
              console.log("Proxying media request:", {
                path: req.url,
                target: env.BASE_API_URL,
              });
            });
          },
        },
      },
      hmr: {
        overlay: devMode,
      },
      allowedHosts: allowedHost ? [allowedHost, env.API_HOST] : [],
      assetsInclude: ["**/*.ttf", "**/*.woff", "**/*.woff2"],
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      configureServer(server: any) {
        server.middlewares.use(createLogHandler());
      },
    },
    test: {
      environment: "jsdom",
      globals: true,
      setupFiles: ["./tests/setup.ts"],
      include: ["**/*.{test,spec}.{js,ts,jsx,tsx}"],
    },
  };
});
