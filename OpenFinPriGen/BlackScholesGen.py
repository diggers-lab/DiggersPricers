import numpy as np
import pandas as pd

from OpenFinPriGen.StockGen import StockGen


class BlackScholesGen(StockGen):
    """
        Subclass of ModelGenerator, that generates the stock as a Geometric Browninan Motion (log-normal distribution)
        as it is specified by Black-Scholes assumptions.
        @param r: risk-free rate, float
        @param q: dividend yield, float
        @param s0: stock value at time t=0, float
        @param sigma: value of the volatility considered, float
        @param dt: discretiration step, float
    """

    def __init__(self, N: int, T: int, r: float, q: float, s0: float, sigma: float, dt: float):
        StockGen.__init__(self, N, T)
        self.r = r
        self.q = q
        self.s0 = s0
        self.sigma = sigma
        self.dt = dt

    def PathGenerate(self):
        price = np.zeros(shape=(self.N, self.T))
        price[:, 0] = self.s0
        Z = np.random.normal(0, 1, size=(self.N, self.T))

        for i in range(self.N):
            for t in range(1, self.T):
                price[i, t] = price[i, t - 1] * np.exp(
                    (self.r - self.q - 0.5 * self.sigma ** 2) * self.dt + self.sigma * np.sqrt(self.dt) * Z[i, t])
        underlying = pd.DataFrame(price)

        return underlying


