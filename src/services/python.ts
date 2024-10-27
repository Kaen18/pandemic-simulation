// /backend/services/PythonService.ts
import { exec } from 'child_process';

export class PythonService {
  // Este método ejecuta el script Python y obtiene el resultado
  executePythonScript(): Promise<string> {
    return new Promise((resolve, reject) => {
      exec('python ./py-functions/data_provider.py', (error, stdout, stderr) => {
        if (error) {
          console.error(`Error ejecutando script: ${error}`);
          reject(error);
          return;
        }

        if (stderr) {
          console.error(`Error en Python: ${stderr}`);
          reject(stderr);
          return;
        }

        // stdout contiene el resultado del script Python
        resolve(stdout);
      });
    });
  }
}
