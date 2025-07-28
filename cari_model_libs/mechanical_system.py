import numpy as np
from cari_model_libs import SimulatedDynamicSystem  # Assuming it's in a separate file

class MechanicalSystem(SimulatedDynamicSystem):
    """
    A concrete implementation of SimulatedDynamicSystem representing a generic mechanical system.
    """

    def __init__(self, st):
        super().__init__(
            sampling_period=st,
            state_dim=2,
            input_dim=1,
            output_dim=1
        )
        self.x0 = np.zeros(self.order)
        self.u0 = np.zeros(self.num_input)
        self.x = self.x0.copy()
        self.u = self.u0.copy()
        self.umax = np.array([5.0])
        self.sigma_y = 0.0
        self.scenario = 1

    def state_function(self, x, u, t):
        """
        Define the system's state derivative dx/dt = f(x, u).
        Override this in a subclass or edit to match the actual dynamics.
        """
        return np.zeros_like(x)

    def output_function(self):
        """
        Define the output of the system y = h(x) + noise.
        """
        noise = self.sigma_y * np.random.randn(self.num_output)
        return self.x + noise
