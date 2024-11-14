// socketConfig.ts
import { Server as SocketIOServer, Socket } from "socket.io";
import { newCicle } from "../services";

// Exporta una variable `io` que contendrá la instancia del socket
export let io: SocketIOServer | null = null;

// Función para inicializar y configurar el socket
export function setupSocket(server: any) {
    // Inicializa el servidor de socket
    io = new SocketIOServer(server);

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
