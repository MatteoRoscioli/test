
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 20, 100)
plt.plot(x, np.sin(x))
plt.show()

class AirplaneSimulator:
    def __init__(self):
        self.position = np.array([0, 0, 0])  # x, y, z
        self.velocity = np.array([0, 0, 0])  # vx, vy, vz
        self.acceleration = np.array([0, 0, 0])  # ax, ay, az
        self.orientation = np.array([0, 0, 0])  # pitch, roll, yaw
        self.angular_velocity = np.array([0, 0, 0])  # pitch rate, roll rate, yaw rate
        self.mass = 1000  # kg
        self.thrust = 0
        self.lift = 0
        self.drag = 0
        self.gravity = 9.81  # m/s^2
        self.time = 0
        self.dt = 0.1  # time step

    def update(self):
        # Update position and velocity
        self.velocity += self.acceleration * self.dt
        self.position += self.velocity * self.dt

        # Update orientation
        self.orientation += self.angular_velocity * self.dt

        # Update time
        self.time += self.dt

    def calculate_forces(self):
        # Simplified force calculations
        self.lift = 0.5 * self.velocity[1]**2  # Simplified lift formula
        self.drag = 0.1 * np.linalg.norm(self.velocity)**2  # Simplified drag formula
        
        # Calculate net force
        force = np.array([
            self.thrust - self.drag,
            0,
            self.lift - self.mass * self.gravity
        ])
        
        self.acceleration = force / self.mass

    def set_thrust(self, thrust):
        self.thrust = thrust

    def simulate(self, duration):
        positions = []
        for _ in range(int(duration / self.dt)):
            self.calculate_forces()
            self.update()
            positions.append(self.position.copy())
        return np.array(positions)

    def plot_trajectory(self, positions):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(positions[:, 0], positions[:, 1], positions[:, 2])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title('Airplane Trajectory')
        plt.show()

# Example usage
simulator = AirplaneSimulator()
simulator.set_thrust(20000)  # Set initial thrust
simulator.velocity = np.array([100, 0, 0])  # Set initial velocity
positions = simulator.simulate(60)  # Simulate for 60 seconds
simulator.plot_trajectory(positions)