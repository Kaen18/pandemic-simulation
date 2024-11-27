import { Socket } from "socket.io";
import { Totalizer } from "../types";

export const newCicle = async (result: any, socket: Socket): Promise<void> => {
    // socket.broadcast.emit('newCycle', result)

    console.log('newCicle', result)
    const { healthy = 0, sick = 0, recovered = 0, dead = 0} = result || {}
    const totalizer: Totalizer = { healthy, sick, recovered, dead }
    _sendMockupSocket(socket, totalizer)

}

// Private functions
const _sendMockupSocket = (socket: Socket, result: Totalizer) => {
    socket.broadcast.emit('newCycleFront', result)
}

