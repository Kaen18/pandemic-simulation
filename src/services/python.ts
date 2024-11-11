import { spawn } from 'child_process';

export class PythonService {
  // Este método ejecuta el script Python de manera asíncrona
  executePythonScript(config: any): void {
    const configStr = JSON.stringify(config);

    // Ejecuta el proceso en segundo plano sin esperar respuesta
    const pythonProcess = spawn('python3.11', ['./py-functions/main.py', configStr]);

    pythonProcess.stdout.on('data', (data) => {
      console.log(`Salida del script Python: ${data.toString()}`);
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error(`Error en Python: ${data.toString()}`);
    });

    pythonProcess.on('close', (code) => {
      console.log(`El proceso de Python terminó con el código: ${code}`);
    });
  }
}
