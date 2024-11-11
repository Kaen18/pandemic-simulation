# main.py
import time
import json
from model import CovidModel

# Configuración de parámetros de simulación
config = {
    "agents": 1000,
    "infected": 5,
    "distribution": {
        "poblationalAge": { "neonatal": 0.05, "kid": 0.2, "young": 0.15, "adult": 0.35, "old": 0.2, "oldest": 0.05 },
        "healthCondition": { "athetic": 0.2, "healthy": 0.4, "sedentary": 0.3, "comorbility": 0.1 },
        "movility": { "restricted": 0.3, "constant": 0.4, "intermitent": 0.3 },
        "atention": { "low": 0.2, "medium": 0.5, "high": 0.3 },
        "wealthyDistribution": { "halfMinimumSalary": 0.4, "minimumSalary": 0.3, "twoMinimumSalary": 0.2, "threeMinimumSalary": 0.06,
            "fiveMinimumSalary": 0.02, "tenMinimumSalary": 0.015, "moreThanTwelveMinimumSalary": 0.005 },
        "profesionalActivity": { "healthProfesional": 0.05, "essentialProfesional": 0.2, "normalProfesional": 0.2, "student": 0.3,
            "retired": 0.05, "inactive": 0.1, "domestic": 0.1 }
    },
    "ambientalParameters": {
        "quarentine": True, "maskUse": True, "socialDistance": True
    },
    "contagiousPercentage": { "minimum": 0.15, "maximum": 0.45 },
    "recoveryTime": { "minimum": 15, "maximum": 21 },
    "inmunityTime": { "minimum": 30, "maximum": 60 },
    "deathPercentage": { "minimum": 0.15, "maximum": 0.45 },
    "simulation_time": 120,
}

# Inicialización y ejecución del modelo
model = CovidModel(config)

# Tiempo de inicio de la simulación
start_time = time.time()

# Ejecutar simulación hasta alcanzar el tiempo configurado o hasta que todos los agentes mueran o se recuperen
while time.time() - start_time < config["simulation_time"]:
    elapsed_time = time.time() - start_time
    step = int(elapsed_time)  # Calcular el número de ciclos transcurridos
    print(f"\n--- Ciclo de simulación {step + 1} ---")
    model.step()

    # Recolectar y mostrar los resultados en formato JSON
    state_counts = {
        "infected": model.count_state("Infectious"),
        "exposed": model.count_state("Exposed"),
        "deceased": model.count_state("Deceased"),
        "susceptible": model.count_state("Susceptible"),
        "recovered": model.count_state("Recovered")
    }

    # Imprimir los resultados en formato JSON
    print(json.dumps(state_counts, indent=4))

    # Verificar si toda la población ha muerto o se ha recuperado
    total_agents = config["agents"]
    if state_counts["deceased"] == total_agents or state_counts["recovered"] == total_agents:
        print("La simulación ha terminado porque todos los agentes han muerto o se han recuperado.")
        break

    time.sleep(1)

# Resultados finales de la simulación
print("\n--- Resultados finales de la simulación ---")
state_counts_final = {
        "infected": model.count_state("Infectious"),
        "exposed": model.count_state("Exposed"),
        "deceased": model.count_state("Deceased"),
        "susceptible": model.count_state("Susceptible"),
        "recovered": model.count_state("Recovered")
    }

# Imprimir los resultados en formato JSON
print(json.dumps(state_counts_final, indent=4))
final_results = model.get_results()
array_results = []
for result in final_results[-1]:
    array_results.append(result)
# print(json.dumps(array_results, indent=4))
