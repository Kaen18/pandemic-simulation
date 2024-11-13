import "dotenv/config";
import express from "express";
import cors from "cors";
import { createServer } from "http";
import { router } from "./src/routes";
import { Server as SocketIOServer } from "socket.io";
import { setupSocket } from "./src/config/socket";
const PORT = process.env.PORT || 3000;
const app = express();
app.use(
  cors({
    origin: "*",
  })
);
app.use(express.json())
app.use(router);
const server = createServer(app);
const io = new SocketIOServer(server);
// Configura el socket utilizando la función importada
setupSocket(io);
server.listen(PORT, () => console.log(`Listen in port ${PORT}`));