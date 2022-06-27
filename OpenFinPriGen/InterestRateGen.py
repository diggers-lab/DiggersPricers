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
        rates_tab = np.zeros(shape=(self.N, self.T))
        dt = 1.0 / self.T
        Z = np.random.normal(0, np.sqrt(dt), size=(self.N, self.T))
        rates_tab[:, 0] = r0
        for i in range(self.N):
            for j in range(1, self.T):
                rates_tab[i, j] = rates_tab[i, j - 1] + k * (theta - rates_tab[i, j - 1]) * dt + sigma * Z[i, j]
        df_rates_vasicek = pd.DataFrame(rates_tab)
        return df_rates_vasicek
