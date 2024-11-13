// socketConfig.ts
import { Server as SocketIOServer, Socket } from "socket.io";
import { newCicle } from "../services";

// Configuración de eventos para el socket
export function setupSocket(io: SocketIOServer) {
    io.on("connection", (socket: Socket) => {
        console.log("Cliente conectado");

        // Escucha el evento "simulation_update" desde el cliente
        socket.on("newCicle", async (result) => {
            try {
                console.log("newCicle on", result);
                // Llama a la función newCicle del servicio sockets
                await newCicle(result, socket);
            } catch (error) {
                console.error(error);
            }
        });

        socket.on("disconnect", () => {
            console.log("Cliente desconectado");
        });


    });
}
