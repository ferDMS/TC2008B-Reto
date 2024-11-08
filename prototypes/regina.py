import agentpy as ap
import numpy as np

# PlotModel to represent each plot of crops in the field
class PlotModel(ap.Agent):
    def setup(self):
        self.location = (self.random.randint(0, self.model.length), self.random.randint(0, self.model.height))
        self.madurez = self.random.randint(0, 12)  # Crop maturity levels from 0 to 11
        self.angle = self.random.uniform(0, 360)   # Directional orientation of the plot

    def update_maturity(self):
        if self.madurez < 10:
            self.madurez += 1  # Simulate crop growth over time

# SiloModel to represent storage silos
class SiloModel(ap.Agent):
    def setup(self):
        self.location = (self.random.randint(0, self.model.length), self.random.randint(0, self.model.height))
        self.max_storage = 1000  # Maximum storage capacity
        self.current_storage = 0  # Current amount of stored harvest

    def store_crop(self, amount):
        available_space = self.max_storage - self.current_storage
        self.current_storage += min(amount, available_space)
        return max(0, amount - available_space)  # Return any leftover crop

# Harvester Model for each crop harvester
class HarvesterModel(ap.Agent):
    def setup(self):
        self.max_gas = 100
        self.gas_level = 100
        self.max_storage = 50
        self.crop_storage = 0
        self.distance_traveled = 0
        self.plot = None  # The current plot where the harvester is located

    def move(self, target_plot):
        # Move to the plot with mature crops and update distance and gas
        self.distance_traveled += np.linalg.norm(np.array(self.plot.location) - np.array(target_plot.location))
        self.plot = target_plot
        self.gas_level -= 1  # Assume 1 unit of gas per move
        self.harvest(target_plot)

    def harvest(self, plot):
        if plot.madurez >= 10:
            amount = min(plot.madurez, self.max_storage - self.crop_storage)
            plot.madurez = 0  # Reset plot maturity after harvest
            self.crop_storage += amount

# ContainerModel for each storage truck
class ContainerModel(ap.Agent):
    def setup(self):
        self.max_gas = 150
        self.gas_level = 150
        self.max_storage = 200
        self.crop_storage = 0
        self.distance_traveled = 0
        self.harvester_pair = None
        self.closest_silo = None  # Reference to nearest silo

    def follow_harvester(self):
        # Moves along with paired harvester, if possible
        if self.harvester_pair:
            self.distance_traveled += 1  # Simulate moving with the harvester
            self.gas_level -= 1  # Gas consumption

    def transfer_to_silo(self):
        # Transfer crops to silo if container is full
        if self.closest_silo and self.crop_storage >= self.max_storage:
            self.crop_storage = self.closest_silo.store_crop(self.crop_storage)

# --- Farm Model ---

class FarmModel(ap.Model):
    def setup(self):
        self.length = 50  # Length of the farm field
        self.height = 50  # Width of the farm field
        self.harvesters = ap.AgentList(self, 5, HarvesterModel)
        self.containers = ap.AgentList(self, 5, ContainerModel)
        self.plots = ap.AgentList(self, 100, PlotModel)
        self.silos = ap.AgentList(self, 2, SiloModel)

        # Pair each harvester with a container and assign nearest silo
        for harvester, container in zip(self.harvesters, self.containers):
            container.harvester_pair = harvester
            container.closest_silo = self.silos[self.random.randint(len(self.silos))]

    def step(self):
        # Update maturity of crops in each plot
        for plot in self.plots:
            plot.update_maturity()

        # Each harvester makes a decision about moving and harvesting
        for harvester in self.harvesters:
            # Find the nearest plot with mature crops
            mature_plots = [plot for plot in self.plots if plot.madurez >= 10]
            if mature_plots:
                closest_plot = min(mature_plots, key=lambda p: np.linalg.norm(np.array(p.location) - np.array(harvester.plot.location)))
                harvester.move(closest_plot)

        # Each container follows its harvester and delivers crops to silo if needed
        for container in self.containers:
            container.follow_harvester()
            container.transfer_to_silo()

# --- Running the Simulation ---

parameters = {
    'steps': 100
}

model = FarmModel(parameters)
results = model.run()
