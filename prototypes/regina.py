import random

class Tractor(ap.Agent):
    def setup(self):
        self.water_capacity = self.p['water_capacity']
        self.fuel_capacity = self.p['fuel_capacity']
        self.wheat_capacity = self.p['wheat_capacity']
        self.water_level = self.water_capacity
        self.fuel_level = self.fuel_capacity
        self.wheat_level = 0
        self.task = "idle"
        self.position = None
        self.q_table = {}  # Q-table for storing state-action values
        self.alpha = 0.1  # Learning rate
        self.gamma = 0.9  # Discount factor
        self.epsilon = 0.1  # Exploration rate

    def get_state(self):
        return self.position

    def get_possible_actions(self):
        x, y = self.position
        actions = []
        for dx, dy, action in [(0, 1, 'down'), (0, -1, 'up'), (1, 0, 'right'), (-1, 0, 'left')]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                if (new_x < PATH_WIDTH or new_x >= GRID_SIZE - PATH_WIDTH or
                        new_y < PATH_WIDTH or new_y >= GRID_SIZE - PATH_WIDTH):
                    actions.append(action)
        return actions

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:  # Explore
            return random.choice(self.get_possible_actions())
        else:  # Exploit
            return max(self.q_table.get(state, {}), key=lambda a: self.q_table[state].get(a, 0), default=None)

    def update_q_table(self, state, action, reward, next_state):
        if state not in self.q_table:
            self.q_table[state] = {}
        if action not in self.q_table[state]:
            self.q_table[state][action] = 0

        max_next_q = max(self.q_table.get(next_state, {}).values(), default=0)
        self.q_table[state][action] += self.alpha * (reward + self.gamma * max_next_q - self.q_table[state][action])

    def move(self):
        state = self.get_state()
        action = self.choose_action(state)

        dx, dy = {'up': (0, -1), 'down': (0, 1), 'left': (-1, 0), 'right': (1, 0)}[action]
        new_x, new_y = self.position[0] + dx, self.position[1] + dy

        if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
            next_state = (new_x, new_y)
            reward = -1  # Default negative reward for fuel consumption
            self.position = next_state

            # Check for interactions
            if self.task == "watering":
                plant = next((p for p in self.model.plants if p.position == self.position), None)
                if plant and plant.needs_water():
                    reward = 10  # Positive reward for watering
                    self.perform_task(plant)
            elif self.task == "harvesting":
                plant = next((p for p in self.model.plants if p.position == self.position), None)
                if plant and plant.is_ready_for_harvest():
                    reward = 10  # Positive reward for harvesting
                    self.perform_task(plant)
            elif self.task == "depositing" and self.position == self.model.silo.position:
                reward = 20  # Higher reward for depositing wheat
                self.deposit_wheat()

            self.update_q_table(state, action, reward, next_state)

