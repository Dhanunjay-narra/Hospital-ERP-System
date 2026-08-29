const { createServer } = require("http");
const next = require("next");

const dev = true;
const hostname = "127.0.0.1";
const port = 3000;
const app = next({ dev, hostname, port });
const handle = app.getRequestHandler();

console.log("Starting Next.js server listener...");

const server = createServer(async (req, res) => {
  try {
    await handle(req, res);
  } catch (err) {
    console.error("Error occurred handling", req.url, err);
    res.statusCode = 500;
    res.end("internal server error");
  }
});

server.listen(port, hostname, () => {
  console.log(`> Ready and listening immediately on http://${hostname}:${port}`);
});

app.prepare().then(() => {
  console.log("> Next.js app preparation finished.");
}).catch((err) => {
  console.error("Next.js app preparation error:", err);
});
