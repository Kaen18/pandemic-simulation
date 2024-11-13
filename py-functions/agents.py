import random
import math

class CovidAgent:
    def __init__(self, agent_id, config, grid_size=(10, 10)):
        self.agent_id = agent_id
        self.state = "Susceptible"
        self.infected = False
        self.config = config

        # Distribución de características
        self.age_group = self.random_age_group(config["distribution"]["poblationalAge"])
        self.health_condition = self.random_health_condition(config["distribution"]["healthCondition"])
        self.mobility = self.random_mobility(config["distribution"]["movility"])
        self.attention = self.random_attention(config["distribution"]["atention"])
        self.wealth = self.random_wealth(config["distribution"]["wealthyDistribution"])
        self.profession = self.random_profession(config["distribution"]["profesionalActivity"])

        # Inicialización de las coordenadas del agente en la cuadrícula
        self.x, self.y = random.randint(0, grid_size[0] - 1), random.randint(0, grid_size[1] - 1)
        self.grid_size = grid_size

        # Calcular la probabilidad de infección (β), tiempo de recuperación (T_rec) y tasa de mortalidad (γ)
        self.infection_probability = self.calculate_infection_probability()
        self.recovery_time = self.calculate_recovery_time()
        self.mortality_rate = self.calculate_mortality_rate()

        # Inmunidad
        self.immunity_duration = 0
        self.immunity_expired = False

    def calculate_infection_probability(self):
        # Calcular β_n (probabilidad de infección) en el rango [0, 0.3]
        age_factor = self.get_age_score()
        activity_factor = 1 if self.profession == "active" else 0.5
        mobility_factor = {"constant": 0.3, "intermitent": 0.6, "restricted": 0.1}.get(self.mobility, 0.5)
        attention_factor = {"low": 0.2, "medium": 0.5, "high": 0.8}.get(self.attention, 0.5)
        
        beta = (age_factor + activity_factor + mobility_factor + attention_factor) / 4
        return beta * 0.3  # Escalar al rango [0, 0.3]

    def calculate_recovery_time(self):
        # Calcular T_rec,n (tiempo de recuperación) en el rango [10, 21] días
        health_factor = {"good": 0.8, "average": 0.5, "poor": 0.2}.get(self.health_condition, 0.5)
        wealth_factor = {"low": 0.3, "medium": 0.6, "high": 0.9}.get(self.wealth, 0.5)
        attention_factor = {"low": 0.2, "medium": 0.5, "high": 0.8}.get(self.attention, 0.5)
        
        avg_score = (health_factor + wealth_factor + attention_factor) / 3
        return 10 + (21 - 10) * avg_score  # Mapear al rango [10, 21] días

    def calculate_mortality_rate(self):
        # Calcular γ_n (tasa de mortalidad) en el rango [10^-4, 10^-2]
        health_factor = {"good": 0.8, "average": 0.5, "poor": 0.2}.get(self.health_condition, 0.5)
        wealth_factor = {"low": 0.3, "medium": 0.6, "high": 0.9}.get(self.wealth, 0.5)
        
        avg_score = (health_factor + wealth_factor) / 2
        return 10**-4 + (10**-2 - 10**-4) * avg_score  # Mapear al rango [10^-4, 10^-2]

    def get_age_score(self):
        # Asignar un puntaje de edad basado en el grupo etario
        age_scores = {
            "neonatal": 0.9,
            "young": 0.7,
            "adult": 0.5,
            "old": 0.8,
            "oldest": 1.0
        }
        return age_scores.get(self.age_group, 0.5)

    # Métodos para inicializar las características del agente
    def random_age_group(self, age_distribution):
        return random.choices(list(age_distribution.keys()), list(age_distribution.values()))[0]

    def random_health_condition(self, health_condition_distribution):
        return random.choices(list(health_condition_distribution.keys()), list(health_condition_distribution.values()))[0]

    def random_mobility(self, mobility_distribution):
        return random.choices(list(mobility_distribution.keys()), list(mobility_distribution.values()))[0]

    def random_attention(self, attention_distribution):
        return random.choices(list(attention_distribution.keys()), list(attention_distribution.values()))[0]

    def random_wealth(self, wealth_distribution):
        return random.choices(list(wealth_distribution.keys()), list(wealth_distribution.values()))[0]

    def random_profession(self, profession_distribution):
        return random.choices(list(profession_distribution.keys()), list(profession_distribution.values()))[0]

    # Método para mover al agente
    def move(self):
        if self.immunity_expired:
            return  # No se mueve si la inmunidad ha expirado

        move_probability = self.calculate_move_probability()
        
        if random.random() < move_probability:
            self.x, self.y = self.random_move()

    def calculate_move_probability(self):
        if self.mobility == "constant":
            return 1.0
        elif self.mobility == "intermitent":
            return 0.5
        elif self.mobility == "restricted":
            return 0.2
        return 0.0

    def random_move(self):
        direction = random.choice(["up", "down", "left", "right"])
        if direction == "up" and self.y > 0:
            self.y -= 1
        elif direction == "down" and self.y < self.grid_size[1] - 1:
            self.y += 1
        elif direction == "left" and self.x > 0:
            self.x -= 1
        elif direction == "right" and self.x < self.grid_size[0] - 1:
            self.x += 1
        return self.x, self.y

    # Método para actualizar el estado del agente
    def update_state(self, agents):
        # Contabiliza los agentes infectados cercanos
        nearby_infected_count = sum(
            1 for agent in agents
            if agent != self and agent.state == "Infectious" and self.calculate_distance(agent) < 1.5
        )

        # Cambio de estado basado en exposición
        if self.state == "Susceptible" and random.random() < self.exposure_chance(nearby_infected_count):
            self.state = "Exposed"
        elif self.state == "Exposed" and random.random() < self.infection_probability:
            self.state = "Infectious"

        if self.state == "Infectious":
            self.recovery_time -= 1
            if self.recovery_time <= 0:
                if random.random() < self.mortality_rate:
                    self.state = "Deceased"
                else:
                    self.state = "Recovered"
                    self.immunity_duration = random.randint(self.config["inmunityTime"]["minimum"], self.config["inmunityTime"]["maximum"])
                    self.immunity_expired = False

        elif self.state == "Recovered":
            if self.immunity_duration > 0:
                self.immunity_duration -= 1
            else:
                self.immunity_expired = True

                 # Reinfección con probabilidad
                random_val = random.random()
                if random_val < 0.05:  # 5% de probabilidad de reinfección después de que la inmunidad caduque
                    self.state = "Infectious"
                if random_val > 0.55: # 60% de probabilidad de ser susceptible nuevamente
                    self.state = "Susceptible"
                
        elif self.state == "Deceased":
            pass

    def exposure_chance(self, nearby_infected_count):
        base_exposure = random.uniform(self.config["contagiousPercentage"]["minimum"], self.config["contagiousPercentage"]["maximum"])
        return base_exposure * (nearby_infected_count / 4)  # Asume que el máximo de vecinos cercanos posibles es 4

    def calculate_distance(self, agent):
        return math.sqrt((self.x - agent.x) ** 2 + (self.y - agent.y) ** 2)

    def get_state(self):
        return {
            "id": self.agent_id,
            "state": self.state,
            "age_group": self.age_group,
            "health_condition": self.health_condition,
            "mobility": self.mobility,
            "attention": self.attention,
            "wealth": self.wealth,
            "profession": self.profession,
            "position": (self.x, self.y),
            "immunity_expired": self.immunity_expired,
        }
