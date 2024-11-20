import { io } from "../config/socket";
import { AmbientalParameters, SimulationConfig } from "../types";
import { PythonService } from "./python";


// {
//     "agents": 1000,
//     "infected": 5,
//     "distribution": {
//         "poblationalAge": {
//             "neonatal": 0.05,
//             "kid": 0.2,
//             "young": 0.15,
//             "adult": 0.35,
//             "old": 0.2,
//             "oldest": 0.05
//         },
//         "healthCondition": {
//             "athetic": 0.2,
//             "healthy": 0.4,
//             "sedentary": 0.3,
//             "comorbility": 0.1
//         },
//         "movility": {
//             "restricted": 0.3,
//             "constant": 0.4,
//             "intermitent": 0.3
//         },
//         "atention": {
//             "low": 0.2,
//             "medium": 0.5,
//             "high": 0.3
//         },
//         "wealthyDistribution": {
//             "halfMinimumSalary": 0.4,
//             "minimumSalary": 0.3,
//             "twoMinimumSalary": 0.2,
//             "threeMinimumSalary": 0.06,
//             "fiveMinimumSalary": 0.02,
//             "tenMinimumSalary": 0.015,
//             "moreThanTwelveMinimumSalary": 0.005
//         },
//         "profesionalActivity": {
//             "healthProfesional": 0.05,
//             "essentialProfesional": 0.2,
//             "normalProfesional": 0.2,
//             "student": 0.3,
//             "retired": 0.05,
//             "inactive": 0.1,
//             "domestic": 0.1
//         }
//     },
//     "ambientalParameters": {
//         "quarentine": true,
//         "maskUse": true,
//         "socialDistance": true
//     },
//     "contagiousPercentage": {
//         "minimum": 0.15,
//         "maximum": 0.45
//     },
//     "recoveryTime": {
//         "minimum": 15,
//         "maximum": 21
//     },
//     "inmunityTime": {
//         "minimum": 30,
//         "maximum": 60
//     },
//     "deathPercentage": {
//         "minimum": 0.15,
//         "maximum": 0.45
//     },
//     "simulation_time": 120
// }

export default class PandemiaService {
    public start(data: SimulationConfig): any {
        const pythonService = new PythonService();
        const result = pythonService.executePythonScript(data);

        return result;
    }

    public pause(): void {
        console.log('Pausando o activando simulación');
        io?.emit('pause_simulation');
    }

    private manageParameters(data: SimulationConfig): any {
        // Aquí puedes validar y procesar los datos recibidos
        const { agents, infected, distribution, ambientalParameters, contagiousPercentage, recoveryTime, inmunityTime, deathPercentage, simulation_time } = data;

        if (typeof agents !== 'number' || agents < 1) {
            throw new Error('El número de agentes debe ser un número mayor a 0');
        }

        if (typeof infected !== 'number' || infected < 1) {
            throw new Error('El número de infectados debe ser un número mayor a 0');
        }

        // Valida la estructura de la distribución
        if (!distribution || typeof distribution !== 'object') {
            throw new Error('La distribución de la población es requerida');
        }

        this.validateAmbientalParameters(ambientalParameters);

        // Valida la estructura de la distribución de la edad
        const { poblationalAge } = distribution;
        if (!poblationalAge || typeof poblationalAge !== 'object') {
            throw new Error('La distribución de la edad es requerida');
        }


        return data
    }

    private validateAmbientalParameters(data: AmbientalParameters): any {
        const { quarentine, maskUse, socialDistance } = data || {};

        if (typeof quarentine !== 'boolean') {
            throw new Error('El parámetro de cuarentena es requerido');
        }

        if (typeof maskUse !== 'boolean') {
            throw new Error('El parámetro de uso de mascarilla es requerido');
        }

        if (typeof socialDistance !== 'boolean') {
            throw new Error('El parámetro de distanciamiento social es requerido');
        }

        return data;
    }
}