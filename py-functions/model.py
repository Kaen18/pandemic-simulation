# models/model.py
import random
from agents import CovidAgent

class CovidModel:
    def __init__(self, config):
        self.config = config
        self.grid_size = 10  # Tamaño de la cuadrícula, se puede ajustar
        self.agents = []
        self.grid = self.initialize_grid(self.grid_size)
        self.history = []  # Para almacenar el historial de los estados de los agentes
        self.initialize_agents(config)

    def initialize_grid(self, size):
        return [[None for _ in range(size)] for _ in range(size)]

    def initialize_agents(self, config):
        for i in range(config["agents"]):
            agent = CovidAgent(i, config)
            self.agents.append(agent)
            # Inicialización de los agentes infectados
            if i < config["infected"]:
                agent.state = "Infectious"
                agent.infected = True

    def step(self):
        """Realiza un ciclo de simulación, actualizando el estado de los agentes."""
        for agent in self.agents:
            agent.move()
            agent.update_state()

        self.history.append([agent.get_state() for agent in self.agents])

    def count_state(self, state):
        """Cuenta cuántos agentes están en un estado determinado."""
        return sum(1 for agent in self.agents if agent.state == state)

    def get_results(self):
        return self.history
