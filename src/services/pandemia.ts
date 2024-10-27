import { PythonService } from "./python";

export default class PandemiaService {
    public async start() {
        const pythonService = new PythonService();
        const result = await pythonService.executePythonScript();

        return JSON.parse(result);
    }
}