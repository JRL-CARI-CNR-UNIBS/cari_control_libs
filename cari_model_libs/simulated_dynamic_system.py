import numpy as np
from abc import ABC, abstractmethod

class SimulatedDynamicSystem(ABC):
    """
    Abstract base class for simulating continuous-time dynamic systems using
    numerical integration (e.g., Runge-Kutta). Subclasses must implement the
    state_function and output_function.
    """

    def __init__(self, sampling_period, state_dim, input_dim, output_dim):
        assert sampling_period > 0, "Sampling period must be positive."
        assert state_dim >= 1, "System must have at least one state."
        assert input_dim >= 0, "Input dimension must be non-negative."
        assert output_dim >= 0, "Output dimension must be non-negative."

        self.st = sampling_period
        self.order = state_dim
        self.num_input = input_dim
        self.num_output = output_dim

        self.x = np.zeros(self.order)
        self.x0 = np.zeros(self.order)
        self.u = np.zeros(self.num_input)
        self.u0 = np.zeros(self.num_input)

        self.umax = np.ones(self.num_input) * 5.0
        self.sigma_y = 0.0
        self.t = 0.0
        self.scenario = None

        self.input_names = [f"input_{i+1}" for i in range(self.num_input)]
        self.output_names = [f"output_{i+1}" for i in range(self.num_output)]

    def initialize(self):
        self.x = self.x0.copy()
        self.u = self.u0.copy()
        self.t = 0.0

    def set_scenario(self, scenario_id):
        self.scenario = scenario_id

    def write_actuator_value(self, u):
        u = np.array(u)
        assert u.shape == (self.num_input,), f"Input must be of shape ({self.num_input},)"
        self.u = u

    def read_actuator_value(self):
        return self.u

    def read_sensor_value(self):
        y = self.output_function()
        y = np.atleast_1d(y)
        assert y.shape == (self.num_output,), f"Output must be of shape ({self.num_output},)"
        return y

    def simulate(self):
        u_sat = self.saturation_control_action(self.u)
        assert u_sat.shape == (self.num_input,), "Saturated input shape mismatch."

        n_steps = 10
        dt = self.st / n_steps
        for i in range(n_steps):
            self.ode_solver(u_sat, dt, self.t + i * dt)
        self.t += self.st

    def ode_solver(self, u, dt, t):
        x = self.x
        k1 = self.state_function(x, u, t)
        k2 = self.state_function(x + 0.5 * dt * k1, u, t)
        k3 = self.state_function(x + 0.5 * dt * k2, u, t)
        k4 = self.state_function(x + dt * k3, u, t)

        for k in [k1, k2, k3, k4]:
            assert k.shape == (self.order,), "State function must return array of shape (state_dim,)"

        self.x += (1/6) * (k1 + 2*k2 + 2*k3 + k4) * dt

    def saturation_control_action(self, u):
        return np.clip(u, -self.umax, self.umax)

    def get_state(self):
        return self.x

    def get_time(self):
        return self.t

    def get_input_names(self):
        return self.input_names

    def get_output_names(self):
        return self.output_names

    @abstractmethod
    def state_function(self, x, u, t):
        """
        Must return dx/dt as a NumPy array of shape (state_dim,)
        """
        pass

    @abstractmethod
    def output_function(self):
        """
        Must return output as a NumPy array of shape (output_dim,)
        """
        pass
