# main.py
import time
import json
import socketio
import sys
from model import CovidModel

# Inicializar socketio para comunicarse con el servidor Node.js
sio = socketio.Client()

# Conectarse al servidor Node.js en el puerto configurado (ejemplo: localhost:5000)
sio.connect("http://localhost:3000")

# Estado de la simulación
is_paused = False
remaining_time = None  # Para guardar el tiempo restante cuando se pausa
start_time = None

# Función para enviar datos al servidor
def send_results_to_server(data):
    sio.emit("newCicle", data)

# Leer la configuración desde el argumento
if len(sys.argv) < 2:
    raise ValueError("La configuración de la simulación no se proporcionó como argumento.")
config = json.loads(sys.argv[1])

# Configuración de parámetros de simulación
# config = {
#     "agents": 1000,
#     "infected": 5,
#     "distribution": {
#         "poblationalAge": { "neonatal": 0.05, "kid": 0.2, "young": 0.15, "adult": 0.35, "old": 0.2, "oldest": 0.05 },
#         "healthCondition": { "athetic": 0.2, "healthy": 0.4, "sedentary": 0.3, "comorbility": 0.1 },
#         "movility": { "restricted": 0.3, "constant": 0.4, "intermitent": 0.3 },
#         "atention": { "low": 0.2, "medium": 0.5, "high": 0.3 },
#         "wealthyDistribution": { "halfMinimumSalary": 0.4, "minimumSalary": 0.3, "twoMinimumSalary": 0.2, "threeMinimumSalary": 0.06,
#             "fiveMinimumSalary": 0.02, "tenMinimumSalary": 0.015, "moreThanTwelveMinimumSalary": 0.005 },
#         "profesionalActivity": { "healthProfesional": 0.05, "essentialProfesional": 0.2, "normalProfesional": 0.2, "student": 0.3,
#             "retired": 0.05, "inactive": 0.1, "domestic": 0.1 }
#     },
#     "ambientalParameters": {
#         "quarentine": True, "maskUse": True, "socialDistance": True
#     },
#     "contagiousPercentage": { "minimum": 0.15, "maximum": 0.45 },
#     "recoveryTime": { "minimum": 15, "maximum": 21 },
#     "inmunityTime": { "minimum": 30, "maximum": 60 },
#     "deathPercentage": { "minimum": 0.15, "maximum": 0.45 },
#     "simulation_time": 120,
# }

# Inicialización y ejecución del modelo
model = CovidModel(config)
  
# agregar socket on

# Evento para pausar la simulación
@sio.on("pause_simulation")
def on_pause_simulation():
    global is_paused, remaining_time
    is_paused = not is_paused
    print(f"La simulación ha sido {'pausada' if is_paused else 'reanudada'}.")
    if is_paused:
        remaining_time = config["simulation_time"] - (time.time() - start_time)
    else:
        # Ajustar el tiempo de inicio para continuar donde quedó
        config["simulation_time"] = remaining_time
        remaining_time = None

# Tiempo de inicio de la simulación
start_time = time.time()

# Ejecutar simulación hasta alcanzar el tiempo configurado o hasta que todos los agentes mueran o se recuperen
while time.time() - start_time < config["simulation_time"]:
    if is_paused:
        # Pausar el ciclo si la simulación está en pausa
        time.sleep(1)
        continue

    elapsed_time = time.time() - start_time
    step = int(elapsed_time)  # Calcular el número de ciclos transcurridos
    print(f"\n--- Ciclo de simulación {step + 1} ---")
    model.step()

    # Recolectar y mostrar los resultados en formato JSON
    state_counts = {
        "sick": model.count_state("Infectious"),
        "healthy": model.count_state("Exposed"),
        "dead": model.count_state("Deceased"),
        "susceptible": model.count_state("Susceptible"),
        "recovered": model.count_state("Recovered")
    }

    # Enviar los resultados al servidor Node.js
    send_results_to_server(state_counts)

    # Imprimir los resultados en formato JSON
    print(json.dumps(state_counts, indent=4))

    # Verificar si toda la población ha muerto o se ha recuperado
    total_agents = config["agents"]
    if state_counts["dead"] == total_agents or state_counts["recovered"] == total_agents:
        print("La simulación ha terminado porque todos los agentes han muerto o se han recuperado.")
        break

    time.sleep(1)

# Resultados finales de la simulación
print("\n--- Resultados finales de la simulación ---")
state_counts_final = {
        "sick": model.count_state("Infectious"),
        "healthy": model.count_state("Exposed"),
        "dead": model.count_state("Deceased"),
        "susceptible": model.count_state("Susceptible"),
        "recovered": model.count_state("Recovered")
    }

# Imprimir los resultados en formato JSON
print(json.dumps(state_counts_final, indent=4))
# Enviar los resultados al servidor Node.js
send_results_to_server(state_counts_final)
final_results = model.get_results()
array_results = []
for result in final_results[-1]:
    array_results.append(result)
# print(json.dumps(array_results, indent=4))
