from abc import ABC

import numpy as np
import pandas as pd

from OpenFinPriGen.ModelGenerator import ModelGenerator


class InterestRateGen(ModelGenerator, ABC):
    """
        Subclass of ModelGenerator, that generates interest rates as a dataframe from a model specified

    """

    def __init__(self, N: int, T: int):
        ModelGenerator.__init__(self, N, T)

    def vasicek(self, r0, k, theta, sigma):
        rates = np.zeros(shape=(self.N, self.T))
        dt = 1.0 / self.T
        Z = np.random.normal(0, np.sqrt(dt), size=(self.N, self.T))
        rates[:, 0] = r0
        for i in range(self.N):
            for j in range(1, self.T):
                rates[i, j] = rates[i, j - 1] + k * (theta - rates[i, j - 1]) * dt + sigma * Z[i, j]
        rates = pd.DataFrame(rates)
        return rates
