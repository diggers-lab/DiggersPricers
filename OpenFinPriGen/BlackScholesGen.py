import numpy as np
import pandas as pd
from scipy.stats import stats
from OpenFinPriGen import ModelGenerator


class BlackScholesGen(ModelGenerator):

    def __init__(self, N: int, T: int, r: float, q: float, s0: float, sigma: float, dt: float):
        ModelGenerator.__init__(self, N, T)
        self.r = r
        self.q = q
        self.s0 = s0
        self.sigma = sigma
        self.dt = dt

    def path_generate(self):
        price_tab = np.zeros(shape=(self.N, self.T))
        for i in range(self.N):
            price_tab[i][0] = self.s0
        for t in range(1, self.T):
            for i in range(self.N):
                Z = np.random.normal(size=self.N)
                price_tab[i][t] = price_tab[i][t - 1] * np.exp(
                    (self.r - self.q - 0.5 * self.sigma ** 2) * self.dt + self.sigma * np.sqrt(self.dt) * Z[i])
        df_underlying = pd.DataFrame(price_tab)

        return df_underlying
