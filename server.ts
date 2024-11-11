import "dotenv/config";
import express from "express";
import cors from "cors";
import { router } from "./src/routes";
import { Server, Socket } from 'socket.io';
import http from 'http';

const PORT = process.env.PORT || 3000;
const app = express();
app.use(
  cors({
    origin: "*",
  })
);
app.use(express.json())
app.use(router);
const server = http.createServer(app);
const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"]
  }
});
io.on('connection', (socket) => {
  console.log('a user connected');
  socket.on('newCycle', (result) => {
    socket.broadcast.emit('newCycle', result)
  });
  sendMockupSocket(socket);
});
server.listen(PORT, () => console.log(`Listen in port ${PORT}`));

function getRandomInt(max: number) {
  return Math.floor(Math.random() * max);
}

async function sendMockupSocket(socket: Socket) {
  for (let i = 0; i < 100; i++) {
    await new Promise(resolve => setTimeout(resolve, 10000));
    console.log('Emito');
    socket.broadcast.emit('newCycle', { cycle: i, healthy: getRandomInt(100), sick: getRandomInt(100), recovered: getRandomInt(100), dead: getRandomInt(100)})
  }
}