// socketConfig.ts
import { Server as SocketIOServer, Socket } from "socket.io";

// Configuración de eventos para el socket
export function setupSocket(io: SocketIOServer) {
    io.on("connection", (socket: Socket) => {
        console.log("Cliente conectado");

        // Escucha el evento "simulation_update" desde el cliente
        socket.on("simulation_update", (data) => {
            console.log("Actualización de simulación recibida:", data);
            // Aquí puedes procesar o almacenar los datos recibidos
        });

        socket.on("disconnect", () => {
            console.log("Cliente desconectado");
        });
    });
}
