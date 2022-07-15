from abc import ABC

import numpy as np
import pandas as pd

from OpenFinPriGen.StockGen import StockGen


class HestonGen(StockGen, ABC):
    """
        Subclass of StockGen, that generates the stock
        as it is specified by Heston assumptions.
    """

    def __init__(self, N: int, T: int, r: float, q: float, s0: float, sigma: float, dt: float, kappa: float,
                 theta: float, volvol: float, rho: float):
        StockGen.__init__(self, N, T)
        self.r = r
        self.q = q
        self.s0 = s0
        self.sigma = sigma
        self.dt = dt
        self.kappa = kappa
        self.theta = theta
        self.volvol = volvol
        self.rho = rho

    def PathGenerate(self):
        price = np.zeros(shape=(self.N, self.T))
        volatility = np.zeros(shape=(self.N, self.T))
        price[:, 0] = self.s0
        volatility[:, 0] = self.sigma

        means = [0, 0]
        stdevs = [1, 1]
        covs = [[stdevs[0] ** 2, stdevs[0] * stdevs[1] * self.rho],
                [stdevs[0] * stdevs[1] * self.rho, stdevs[1] ** 2]]

        Z = np.random.multivariate_normal(means, covs, (self.T, self.N))

        for i in range(1, self.T):
            # Use Z2 to calculate Vt
            Z2 = Z[i - 1]
            volatility[:, i] = np.maximum(volatility[:, i - 1] +
                                          self.kappa * (self.theta - volatility[:, i - 1]) * self.dt + self.volvol
                                          * np.sqrt(volatility[:, i - 1] * self.dt) * Z2[:, 1], 0)
            # print(volatility)

            # Use all V_t calculated to find the value of S_t
            price[:, i] = price[:, i - 1] + self.r * price[:, i - 1] * self.dt + np.sqrt(volatility[:, i - 1] * self.dt) \
                          * price[:, i - 1] * Z2[:, 0]
            # print(price)
        price = pd.DataFrame(price)
        print(price)
        volatility = pd.DataFrame(volatility)
        return price, volatility
